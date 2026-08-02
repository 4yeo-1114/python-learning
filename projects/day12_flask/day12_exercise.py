"""
============================================================
Day 12 练习：Flask Web 框架入门
============================================================
在开始前，请先阅读 day12_notes.py 理解今天的知识点，
然后完成下面的练习（3 道题，每题约 15-20 分钟）。

今天的主题：**从 CLI（命令行）到 Web（浏览器）的范式转换**
你会用到 @app.route 路由、Jinja2 模板、GET/POST 表单

运行方式：
  在终端执行：python day12_exercise.py
  然后浏览器打开：http://localhost:5000
  修改代码后刷新浏览器即可看到效果（debug 模式自动重载）
"""

from flask import Flask, render_template, request, url_for

app = Flask(__name__)


# ============================================================
# 练习 1：创建 Flask app，实现首页 + 多个路由
# ============================================================
"""
题目：创建第一个 Flask 应用，实现以下路由

你的任务：
1. 完成 "/" 路由（首页）：
   - 返回一段 HTML，包含：
     * <h1> 标题："欢迎来到 Flask!"
     * <p> 段落说明这是 Day 12 的学习项目
     * 两个链接：一个到 /about，一个到 /user/你的名字

2. 完成 "/about" 路由（关于页）：
   - 返回一段 HTML，包含：
     * <h1> 标题："关于本项目"
     * <p> 段落简介：说明这个项目用来学习 Flask
     * 链接回首页

3. 完成 "/user/<name>" 动态路由：
   - 接收 URL 中的 name 参数
   - 返回 f"<h1>你好, {name}!</h1><p><a href='/'>返回首页</a></p>"
   - 测试：访问 /user/Alice 和 /user/Bob 看不同结果

要求：
- 使用 @app.route() 装饰器注册路由
- 动态路由参数名和函数参数名必须一致
- 运行 app.run(debug=True) 启动开发服务器

提示：
  - 路由函数返回的字符串会自动变成 HTTP 响应
  - debug=True 让你修改代码后自动重载服务器
  - 用 Ctrl+C 停止服务器

预计时间：15 分钟
"""

# TODO: 完成首页路由 "/"
@app.route("/")
def index():
    # TODO: 返回包含标题、说明、导航链接的 HTML 字符串
    return render_template("index.html",username=None)

@app.route("/about")
def about():
   return render_template("about.html")

@app.route("/user/<name>")
def user_page(name):
   return render_template("index.html",username=name)


# TODO: 完成关于页路由 "/about"
# 提示: 参考首页的模式，返回不同的内容


# TODO: 完成动态路由 "/user/<name>"
# 提示: 函数接收 name 参数，返回个性化的欢迎信息


# ============================================================
# 练习 2：用 Jinja2 模板渲染页面
# ============================================================
"""
题目：用 Jinja2 模板替代手写的 HTML 字符串

准备工作：
  templates/ 目录下已经准备好了以下模板文件：
  - layout.html   → 基础模板（导航栏 + 页脚 + content 插槽）
  - index.html    → 首页（继承 layout，覆盖 content block）
  - about.html    → 关于页（继承 layout，覆盖 content block）

你的任务：
1. 修改首页路由，改用 render_template：
   @app.route("/")
   def index():
       return render_template("index.html", username=None)
   # 提示: 当 username=None 时，模板会显示提示信息

2. 修改关于页路由，改用 render_template：
   @app.route("/about")
   def about():
       return render_template("about.html")

3. 完成 "/user/<name>" 路由的模板渲染：
   @app.route("/user/<name>")
   def user_page(name):
       return render_template("index.html", username=name)
   # 提示: 当 username 不为 None 时，模板会显示 "你好, {username}!"

4. 看懂 layout.html 的继承结构：
   - 打开 templates/layout.html，找到 {% block content %}{% endblock %}
   - 打开 templates/index.html，看它如何用 {% extends %} 和 {% block %}
   - 理解：子模板只需要写 {% block %} 内的内容，其他自动继承

要求：
- 使用 render_template() 而非直接返回 HTML 字符串
- 理解模板继承的机制（layout → 子模板）
- 尝试给 render_template 传不同的变量值看效果

提示：
  - render_template("index.html", username="Alice")
    在模板中可以用 {{ username }} 获取值
  - 所有模板必须放在 templates/ 目录下
  - {% extends "layout.html" %} 必须是模板第一行

预计时间：15 分钟
"""

# TODO: 修改首页路由，使用 render_template
# def index():
#     return render_template("index.html", username=None)


# TODO: 修改关于页路由，使用 render_template


# TODO: 修改动态路由，使用模板（让 username 在首页模板中显示）


# ============================================================
# 练习 3：实现表单（GET 显示表单 + POST 处理提交）
# ============================================================
"""
题目：实现一个完整的表单交互——显示表单 → 提交 → 显示结果

表单说明：
  - 三个字段：名字(name)、留言(message)、喜欢的颜色(color)
  - method="POST"（数据不暴露在 URL 中）
  - 提交到同一个 URL（/form）
  - 提交后跳转到 /greet 显示结果

你的任务：
1. 完成 "/form" 路由（同时支持 GET 和 POST）：
   @app.route("/form", methods=["GET", "POST"])
   def form_page():
       if request.method == "POST":
           # 获取表单数据
           name = request.form["name"]
           message = request.form["message"]
           color = request.form["color"]
           # 渲染结果页
           return render_template("greet.html",
                                  name=name, message=message, color=color)
       else:
           # GET 请求 — 显示表单
           return render_template("form.html")

2. 理解 GET vs POST 的区别：
   - GET: 访问 /form → 显示空白表单（render_template("form.html")）
   - POST: 提交表单 → 获取数据 → 显示结果（render_template("greet.html", ...)）

3. 测试完整流程：
   a) 访问 http://localhost:5000/form（GET → 显示表单）
   b) 填写表单，点击提交（POST → 显示结果）
   c) 检查结果页是否正确显示了刚才输入的内容

4. （可选）在首页导航中添加表单链接：
   在 index.html 中找 <a href="{{ url_for('form_page') }}"> 这个链接
   理解 url_for('函数名') 的作用

要求：
- methods 参数必须包含 "GET" 和 "POST"
- 用 request.method 判断请求类型
- 用 request.form["字段名"] 获取 POST 数据
- 表单中的 name 属性要和 request.form 的 key 一致

提示：
  - 如果只用 GET，request.form 会是空的
  - request.form 是一个类似字典的对象
  - 表单 input 的 name 属性 = request.form 的 key
  - greet.html 模板已经写好，你只需要传正确的变量

预计时间：20 分钟
"""

# TODO: 完成 /form 路由（支持 GET 和 POST）
# 提示: methods=["GET", "POST"]

@app.route("/form",methods=["GET","POST"])
def form_page():
   if request.method == "POST":
      name = request.form["name"]
      message = request.form["message"]
      color = request.form["color"]
      
      return render_template("greet.html",name = name,message = message,color = color)
   
   else:
      return render_template("form.html")


# ============================================================
# 启动服务器
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Day 12 Flask 练习服务器启动中...")
    print("请在浏览器中访问: http://localhost:5000")
    print("按 Ctrl+C 停止服务器")
    print("=" * 60)
    app.run(debug=True)
