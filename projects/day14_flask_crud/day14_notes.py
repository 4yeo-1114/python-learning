"""
============================================================
Day 14 笔记：Web CRUD 完成 — RESTful 路由 / Flash 消息 / PRG 模式
============================================================
今天在 Day 13 的基础上，把 Web 端的完整 CRUD 补齐。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
一、RESTful 路由设计
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

REST (Representational State Transfer) 是一种 Web 架构风格。
核心思想：**把 URL 看作"资源"，用 HTTP 方法表达操作**。

对比传统做法 vs RESTful 做法：

    功能          传统做法                    RESTful 做法
    ────────      ──────────                 ────────────
    查看学生列表   /get_students              GET  /students
    添加学生       /add_student               POST /students
    查看单个学生   /get_student?id=5          GET  /students/5
    编辑学生       /edit_student?id=5         PUT  /students/5
    删除学生       /delete_student?id=5       DELETE /students/5

关键规则：
    - URL 用名词（资源名），不用动词
    - HTTP 方法表达操作：GET(查) POST(增) PUT/PATCH(改) DELETE(删)
    - 资源 ID 放在 URL 路径中：/students/<id>

Flask 中实现 RESTful 路由：

    @app.route("/students/<int:student_id>")
    def get_student(student_id):       # student_id 自动从 URL 提取
        ...

    @app.route("/students/<int:student_id>/edit", methods=["GET", "POST"])
    def edit_student(student_id):      # 同一个函数处理查看和提交
        ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
二、Flash 消息（一次性提示消息）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

flash() 是 Flask 提供的一个机制，用于在**重定向后**向用户显示一次性消息。
典型场景："添加学生成功"、"删除失败"——这些消息只在下一页显示一次。

**为什么需要 flash？**
    当用户 POST 提交表单后，我们会 redirect 到另一个页面。
    普通的变量无法跨请求传递（HTTP 是无状态的）。
    用 session 存消息太麻烦（要手动清理）。
    flash 自动处理"显示一次就消失"的逻辑。

**使用方式：**

    后端（Python）：
        from flask import flash            # 1. 导入

        flash("学生添加成功！", "success")  # 2. 发送消息
        #               消息文本     消息类别（可选，用于 CSS 样式）
        return redirect(url_for("student_list"))

    前端（Jinja2 模板）：
        {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
        {% for category, message in messages %}
            <div class="flash-{{ category }}">{{ message }}</div>
        {% endfor %}
        {% endif %}
        {% endwith %}

**消息类别：**
    "success"  — 成功（绿色）
    "error"    — 错误（红色）
    "warning"  — 警告（黄色）
    "info"     — 提示（蓝色）
    不传第二个参数 → 默认 "message"

**关键点：flash 消息只在"下一次请求"中可见，刷新后就消失了。**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
三、PRG 模式（Post-Redirect-Get）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PRG = Post → Redirect → Get

**问题场景（不用 PRG）：**
    1. 用户在 /students/add 填写表单，点击提交（POST）
    2. 服务器处理后，直接 render_template("student_list.html")
    3. 浏览器地址栏仍然是 /students/add
    4. 用户按 F5 刷新 → 浏览器提示"是否重新提交表单？"
    5. 确认 → 同一条数据被重复添加 ❌

**PRG 模式解决方案：**
    1. POST：处理表单数据（保存到数据库）
        ↓
    2. Redirect：重定向到列表页（HTTP 302）
        return redirect(url_for("student_list"))
        ↓
    3. GET：浏览器自动请求列表页（HTTP GET），显示最新数据
        ✓ 地址栏变成 /students（不是 /students/add）
        ✓ 刷新页面只是重新 GET 列表，不会重复提交

**PRG 模式是 Web 开发的黄金法则：POST 请求永远不要直接返回页面内容，必须 redirect。**

对比代码：

    # ❌ 错误做法（不遵循 PRG）
    @app.route("/students/add", methods=["POST"])
    def add_student():
        student_db.add_student(...)
        students = student_db.get_all_students()
        return render_template("student_list.html", students=students)
        # 问题：地址栏是 /students/add，F5 会重复添加

    # ✓ 正确做法（遵循 PRG）
    @app.route("/students/add", methods=["POST"])
    def add_student():
        student_db.add_student(...)
        flash("添加成功", "success")
        return redirect(url_for("student_list"))
        # 浏览器地址变成 /students，F5 安全

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
四、Flask 路由中的动态参数
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Flask 支持在 URL 中捕获变量：

    @app.route("/students/<int:student_id>")
    def show_student(student_id):
        # student_id 是 int 类型
        student = student_db.get_student(student_id)
        ...

转换器类型：
    <int:id>      整数（常用）
    <string:name> 字符串（默认，可以省略写成 <name>）
    <float:price> 浮点数
    <path:filepath> 带斜杠的路径
    <uuid:id>     UUID

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
五、HTML 表单中的 method="POST" 与隐藏字段
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

虽然 RESTful 建议用 PUT/DELETE，但 HTML 表单只支持 GET 和 POST。
对于编辑和删除操作，我们通常用 POST + 路径区分：

    编辑：POST /students/5/edit
    删除：POST /students/5/delete

    或者用隐藏字段标识意图：
    <form method="post" action="/students/{{ s.id }}/delete">
        <input type="hidden" name="_method" value="DELETE">
        <button type="submit">删除</button>
    </form>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
今日学习要点总结
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. RESTful 路由：URL 是资源名 + HTTP 方法表达操作
2. flash 消息：跨重定向的一次性提示
3. PRG 模式：POST 后必须 redirect，不要直接 render
4. <int:xxx> 转换器：从 URL 路径提取参数
5. POST + redirect + flash 是 Web CRUD 的标准三板斧
"""
