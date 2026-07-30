"""
============================================================
Day 12: Flask Web 框架入门 — 从 CLI 到 Web 的范式转换
============================================================
目标：学会用 Flask 创建 Web 应用，理解路由、模板、HTTP 方法
      这是从"命令行交互"到"浏览器交互"的范式转换
"""

# ============================================================
# 第一部分：什么是 Web 框架？为什么需要 Flask？
# ============================================================

print("=" * 60)
print("第一部分：Web 框架的概念")
print("=" * 60)

"""
1.1 之前的学习模式（CLI）
  用户 → 终端输入 → Python 读取 → 处理 → print 输出

  问题：
    - 只能在本机使用
    - 界面是纯文本，不好看
    - 无法多人同时使用
    - 不能点按钮、填表单

1.2 Web 模式（Flask）
  浏览器 → HTTP 请求 → Flask 路由 → 处理 → HTTP 响应 → 浏览器渲染

  优势：
    - 任何人通过浏览器就能访问
    - 界面可以很漂亮（HTML/CSS）
    - 天然支持多人
    - 可以做成真正的"网站"

1.3 Flask 是什么？
  Flask 是一个 Python 的"微框架"（micro-framework）：
    - 核心很小（路由 + 模板 + 请求/响应）
    - 需要什么功能就装什么扩展（插件式）
    - 学习曲线平缓，适合入门

  C++ 对比：
    C++ 中没有 Flask 这样的轻量 Web 框架（C++ Web 开发通常很重）。
    但概念类似：
      Flask 路由 ≈ C++ 中的函数指针表/回调注册
      Flask 模板 ≈ 格式化字符串的高级版
      Flask 请求/响应 ≈ 网络编程中的 recv/send，但 Flask 帮你封装好了
"""


# ============================================================
# 第二部分：最小 Flask 应用 — 从 5 行代码开始
# ============================================================

print("\n" + "=" * 60)
print("第二部分：最小 Flask 应用")
print("=" * 60)

"""
2.1 最简单的 Flask 应用（5 行代码）

    from flask import Flask       # 1. 导入 Flask
    app = Flask(__name__)         # 2. 创建应用实例

    @app.route("/")               # 3. 注册路由（URL → 函数）
    def index():
        return "<h1>Hello!</h1>"  # 4. 返回 HTML

    app.run(debug=True)           # 5. 启动服务器

2.2 这段代码在做什么？

  Flask(__name__)
    → 创建一个 WSGI 应用（Web Server Gateway Interface）
    → __name__ 告诉 Flask 当前模块名，用于定位模板/静态文件

  @app.route("/")
    → 这是一个"装饰器"（decorator，Day 7 学过！）
    → 它把 URL 路径 "/" 映射到 index 函数
    → 当用户访问 http://localhost:5000/ 时，Flask 调用 index()

  app.run(debug=True)
    → 启动内置开发服务器，监听 5000 端口
    → debug=True 表示修改代码后自动重载（开发用，生产环境不要开）

2.3 装饰器本质复习（来自 Day 7）
    @app.route("/")     等价于    index = app.route("/")(index)
    即：把函数注册到 Flask 的 URL 路由表中

2.4 路由规则
    @app.route("/")              → 匹配 /
    @app.route("/about")         → 匹配 /about
    @app.route("/user/<name>")   → 匹配 /user/alice, /user/bob 等
                                    <name> 是动态部分，传给函数参数
    @app.route("/post/<int:id>") → 匹配 /post/1, /post/123
                                    <int:id> 限定必须是整数

    动态路由的类型转换器：
      <string:name>  → 字符串（默认）
      <int:id>       → 整数
      <float:value>  → 浮点数
      <path:subpath> → 可包含斜杠的路径
"""


# ============================================================
# 第三部分：Jinja2 模板 — 把 HTML 和 Python 分离
# ============================================================

print("\n" + "=" * 60)
print("第三部分：Jinja2 模板引擎")
print("=" * 60)

"""
3.1 为什么不直接 return HTML 字符串？
   return "<h1>你好, " + name + "</h1>"  # 丑、难维护、容易 XSS

   正确的做法：用模板文件（.html） + render_template()

3.2 模板文件放哪？
   项目根目录下的 templates/ 文件夹（Flask 默认查找位置）
   项目/
   ├── app.py              ← Flask 应用代码
   └── templates/          ← 模板文件夹（必须是这个名字）
       ├── layout.html     ← 基础模板（骨架）
       ├── index.html      ← 首页
       └── about.html      ← 关于页

3.3 基本语法（三种标记）

   ① {{ 变量 }}                    — 输出变量值
     <h1>你好, {{ username }}</h1>
     → 渲染后: <h1>你好, Alice</h1>

   ② {% 语句 %}                    — 控制流（if/for/block）
     {% if user %}
       <p>欢迎回来, {{ user }}</p>
     {% else %}
       <p>请先登录</p>
     {% endif %}

     {% for item in items %}
       <li>{{ item }}</li>
     {% endfor %}

   ③ {# 注释 #}                    — 不会出现在输出的 HTML 中

3.4 模板继承 — 最重要的概念！

   为什么需要继承？
     每个页面都有相同的头部（导航栏）和底部（版权信息），
     如果每页都写一遍，改一个就要改所有文件。

   解决方案：layout.html（父模板） + 子模板

   layout.html（骨架）:
     <!DOCTYPE html>
     <html>
     <head><title>{% block title %}默认标题{% endblock %}</title></head>
     <body>
       <nav>导航栏（所有页面共享）</nav>
       {% block content %}{% endblock %}
       <footer>底部版权（所有页面共享）</footer>
     </body>
     </html>

   index.html（子模板，覆盖 block）:
     {% extends "layout.html" %}
     {% block title %}首页{% endblock %}
     {% block content %}
       <h1>欢迎!</h1>
       <p>这是首页内容</p>
     {% endblock %}

   关键：
     - {% extends "layout.html" %} 必须是子模板的第一行
     - {% block xxx %} 定义可被覆盖的"插槽"
     - 子模板只写自己不同的部分，其他自动继承

3.5 render_template() 用法
   from flask import render_template

   @app.route("/")
   def index():
       return render_template("index.html", title="首页", username="Alice")
       #                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
       #                                    关键字参数会自动传给模板
"""


# ============================================================
# 第四部分：GET vs POST — HTTP 方法
# ============================================================

print("\n" + "=" * 60)
print("第四部分：GET 和 POST 请求")
print("=" * 60)

"""
4.1 什么是 HTTP 方法？
  浏览器访问网页时，会发送一个 HTTP 请求，其中包含"方法"字段：

  GET  — 获取数据（读操作）
    - 访问网页、点链接、搜索
    - 参数在 URL 中可见（?name=alice&age=20）
    - 可以加书签、分享链接
    - 有长度限制（约 2000 字符）

  POST — 提交数据（写操作）
    - 提交表单、登录、注册
    - 参数在请求体中（URL 不可见）
    - 不能加书签
    - 没有长度限制

4.2 Flask 中处理 GET 和 POST

   方式 1：同一个路由处理 GET 和 POST
     @app.route("/login", methods=["GET", "POST"])
     def login():
         if request.method == "POST":
             # 处理表单提交
             username = request.form["username"]
             password = request.form["password"]
             return f"登录成功: {username}"
         else:
             # 显示登录页面
             return render_template("login.html")

   方式 2：分开两个路由（更清晰，但 URL 不同）
     @app.route("/login")           # GET — 显示表单
     def login_page():
         return render_template("login.html")

     @app.route("/login", methods=["POST"])  # POST — 处理提交
     def login_submit():
         ...

4.3 request 对象
   from flask import request

   request.method       → "GET" 或 "POST"
   request.form["key"]  → 获取 POST 表单数据
   request.args["key"]  → 获取 URL 查询参数（?key=value）

4.4 HTML 表单基础
   <form method="POST" action="/submit">
     <input type="text" name="username" placeholder="输入用户名">
     <input type="password" name="password" placeholder="输入密码">
     <button type="submit">提交</button>
   </form>

   关键：
     - name 属性对应 request.form 中的 key
     - method="POST" 让数据不在 URL 中显示
     - action 指定提交到哪个 URL
"""


# ============================================================
# 第五部分：url_for — 动态生成 URL
# ============================================================

print("\n" + "=" * 60)
print("第五部分：url_for() 函数")
print("=" * 60)

"""
5.1 为什么需要 url_for？
   ❌ 硬编码 URL: <a href="/about">关于</a>
   ✅ url_for:    <a href="{{ url_for('about') }}">关于</a>

   好处：
     - 如果改了路由路径，只需改一处（装饰器参数）
     - url_for('函数名') 自动生成正确 URL
     - 带参数的: url_for('user_page', name='alice') → /user/alice

5.2 在模板和 Python 中都能用
   模板中:
     <a href="{{ url_for('index') }}">首页</a>

   Python 中:
     from flask import url_for
     return redirect(url_for('index'))
"""


# ============================================================
# 第六部分：Flask 项目结构演进（预告）
# ============================================================

print("\n" + "=" * 60)
print("第六部分：项目结构")
print("=" * 60)

"""
6.1 今天学习的简单结构（单文件 + 模板）
   day12_flask/
   ├── app.py              ← 所有路由在一个文件
   └── templates/
       ├── layout.html
       └── ...

6.2 后续 Day 13-14 会演进为
   student_system_web/
   ├── app.py              ← 主应用
   ├── models.py           ← 数据模型（数据库操作）
   ├── auth.py             ← 登录认证相关
   └── templates/
       ├── layout.html
       ├── login.html
       ├── students.html
       └── ...

6.3 Flask vs Django 定位
   Flask: 微框架 → 灵活，自己选组件
   Django: 全栈框架 → 开箱即用，但限制较多
   学习 Flask 能帮你理解 Web 开发的底层原理


C++ 对比总结：
┌──────────────────┬────────────────────┬─────────────────────┐
│ 概念               │ C++ 世界            │ Python Flask         │
├──────────────────┼────────────────────┼─────────────────────┤
│ Web 框架           │ CppCMS, Drogon     │ Flask, Django       │
│ URL 路由          │ 手动注册回调         │ @app.route 装饰器    │
│ 模板               │ 无标准库支持        │ Jinja2（内置集成）    │
│ HTTP 请求/响应     │ 需第三方库          │ request/response    │
│ 开发效率           │ 编译-运行-调试循环   │ 修改即刷新(debug)    │
│ 部署               │ 编译成可执行文件     │ WSGI 服务器部署      │
└──────────────────┴────────────────────┴─────────────────────┘
"""

print("\n[OK] Day 12 笔记阅读完毕，开始做练习吧！")
print("练习文件: day12_exercise.py")
print()
print("今天的新概念：")
print("  1. Flask 路由 @app.route() — URL 映射到 Python 函数")
print("  2. Jinja2 模板 — {{ 变量 }} / {% 语句 %} / 模板继承")
print("  3. GET vs POST — 获取数据 vs 提交数据")
print("  4. url_for() — 动态生成 URL，避免硬编码")
print("  5. 从 CLI 到 Web 的思维转换 — 请求-响应模型")
