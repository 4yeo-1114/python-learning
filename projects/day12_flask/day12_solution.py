"""
============================================================
Day 12 参考答案：Flask Web 框架入门
============================================================
这是 day12_exercise.py 的完整参考答案。
做完练习后再看这个文件，对比你的实现和参考答案。

运行方式：
  python day12_solution.py
  浏览器访问: http://localhost:5000
"""

from flask import Flask, render_template, request, url_for

app = Flask(__name__)


# ============================================================
# 练习 1：创建 Flask app，实现首页 + 多个路由
# ============================================================

@app.route("/")
def index():
    """首页 — 欢迎页面"""
    return render_template("index.html", username=None)


@app.route("/about")
def about():
    """关于页面 — 项目介绍"""
    return render_template("about.html")


@app.route("/user/<name>")
def user_page(name):
    """动态路由 — 根据 URL 中的名字显示个性化欢迎"""
    return render_template("index.html", username=name)


# ============================================================
# 练习 2：用 Jinja2 模板渲染页面
# ============================================================
"""
练习 1 的答案已经使用了 render_template（最佳实践），
所以这里重点解释模板继承的机制：

模板结构:
  templates/
  ├── layout.html      ← 基础骨架（所有页面共享的导航栏和页脚）
  ├── index.html       ← 首页（extends layout.html）
  ├── about.html       ← 关于页（extends layout.html）
  ├── form.html        ← 表单页（extends layout.html）
  └── greet.html       ← 结果页（extends layout.html）

继承流程:
  1. Flask 调用 render_template("index.html")
  2. Jinja2 找到 index.html，看到第一行 {% extends "layout.html" %}
  3. Jinja2 先加载 layout.html
  4. 把 index.html 中 {% block content %}...{% endblock %} 的内容
     填入 layout.html 中 {% block content %}{% endblock %} 的位置
  5. 同理，{% block title %} 也被覆盖

关键语法:
  - {{ variable }}    输出变量（自动转义 HTML，防 XSS）
  - {% if/for %}      控制流
  - {% block name %}  定义可覆盖的区域
  - {% extends %}     指定父模板
  - url_for('函数名')  生成 URL（避免硬编码）
"""


# ============================================================
# 练习 3：实现表单（GET 显示表单 + POST 处理提交）
# ============================================================

@app.route("/form", methods=["GET", "POST"])
def form_page():
    """
    表单页面 — GET 显示表单，POST 处理提交

    GET  /form  → 用户打开表单页面（空白表单）
    POST /form  → 用户提交表单（带数据）
    """
    if request.method == "POST":
        # 获取表单数据
        name = request.form["name"]
        message = request.form["message"]
        color = request.form["color"]

        # 渲染结果页面，把数据传给模板
        return render_template("greet.html",
                               name=name,
                               message=message,
                               color=color)
    else:
        # GET 请求 — 显示空白表单
        return render_template("form.html")


# ============================================================
# 补充：用纯 HTML 字符串的路由（练习 1 的原始写法）
# ============================================================
# 以下是练习 1 不用模板的"原始"写法，供对比参考：

@app.route("/raw")
def raw_index():
    """练习 1 原始写法：直接返回 HTML 字符串（不推荐）"""
    return """
    <h1>欢迎来到 Flask!</h1>
    <p>这是 Day 12 的学习项目 — 用纯 HTML 字符串返回。</p>
    <p>
        <a href='/about'>关于本项目</a> |
        <a href='/user/Alice'>查看 Alice 的主页</a>
    </p>
    <p style='color: red;'>
        缺点：HTML 和 Python 混在一起，难维护，没有模板继承。
    </p>
    """


@app.route("/raw/about")
def raw_about():
    """练习 1 原始写法：关于页"""
    return """
    <h1>关于本项目</h1>
    <p>本项目用于学习 Flask Web 框架。</p>
    <p>路由用 @app.route() 装饰器注册，URL 映射到 Python 函数。</p>
    <p><a href='/raw'>返回首页</a></p>
    """


@app.route("/raw/user/<name>")
def raw_user(name):
    """练习 1 原始写法：动态路由"""
    return f"""
    <h1>你好, {name}!</h1>
    <p>这是通过动态路由 /user/{name} 访问的页面。</p>
    <p>URL 中的 &lt;name&gt; 部分会自动传给函数参数。</p>
    <p><a href='/raw'>返回首页</a></p>
    """


# ============================================================
# 启动服务器
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Day 12 Flask 参考答案服务器启动中...")
    print("请在浏览器中访问: http://localhost:5000")
    print()
    print("可用路由：")
    print("  /              首页（模板渲染）")
    print("  /about         关于页（模板渲染）")
    print("  /user/<name>   动态路由")
    print("  /form          GET/POST 表单")
    print("  /raw           首页（纯 HTML 字符串，对比用）")
    print("  /raw/about     关于页（纯 HTML）")
    print("  /raw/user/<name> 动态路由（纯 HTML）")
    print()
    print("按 Ctrl+C 停止服务器")
    print("=" * 60)
    app.run(debug=True)
