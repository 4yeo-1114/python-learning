"""
============================================================
Day 13: Flask + 数据库整合（C++ 对比版）
============================================================
目标：把 Day 9/10 的 SQLite 数据库整合到 Flask Web 应用中
      学会 Session 管理、登录保护装饰器、Web 模板中展示数据

新概念预告：
  1. Flask Session — 在服务端记住"谁登录了"
  2. 登录保护装饰器 — 用函数包装函数来检查权限
  3. Web 上下文中的数据库操作 — 从 CLI 的 input() 到 Web 的 request.form
"""

# ============================================================
# 第一部分：Flask Session — Web 的"记忆"
# ============================================================

print("=" * 60)
print("第一部分：Flask Session 是什么")
print("=" * 60)

"""
CLI vs Web 的"登录状态"：

CLI 程序（Day 9）：
  Session.current_user = user_dict  # 全局变量记住当前用户
  → 因为同一时间只有一个用户在操作

Web 程序：
  浏览器 A 登录了 Alice
  浏览器 B 登录了 Bob
  → 服务器同时服务多个用户，全局变量会互相覆盖！
  → 需要用 Session（会话）来区分不同用户

Flask Session 原理：
  1. 用户登录 → 服务器把用户信息加密存到 session 字典
  2. 服务器发送一个加密 cookie 给浏览器
  3. 浏览器每次请求自动带上 cookie
  4. 服务器解密 cookie 恢复 session 数据
  5. 不同浏览器有不同的 cookie → 互不干扰

关键代码：
  from flask import session

  # 登录时存入
  session["user_id"] = 1
  session["username"] = "Alice"

  # 后续请求中读取
  username = session.get("username")  # "Alice"

  # 退出时清除
  session.clear()

重要：使用 session 前必须设置 secret_key！
  app.secret_key = "一段随机字符串"  # 用于加密 session
"""

# 快速演示
from flask import Flask, session as flask_session_demo

app_demo = Flask(__name__)
app_demo.secret_key = "demo-secret-key-123"

with app_demo.test_request_context():
    # 模拟一个请求：登录
    flask_session_demo["username"] = "Alice"
    print(f"存入 session: username = {flask_session_demo['username']}")

with app_demo.test_request_context():
    # 模拟另一个请求：读取
    print(f"读取 session: username = {flask_session_demo.get('username')}")
    # 注意：不同 test_request_context 之间的 session 不共享
    # 但在真实浏览器中，同一个用户的请求会共享 session（通过 cookie）


# ============================================================
# 第二部分：登录保护装饰器 — 给路由"加锁"
# ============================================================

print("\n" + "=" * 60)
print("第二部分：装饰器进阶 — @login_required")
print("=" * 60)

"""
回顾：装饰器是什么？
  @app.route("/")   → 把函数注册为路由
  @staticmethod      → 把方法标记为静态方法

装饰器的本质：
  @decorator
  def func(): ...

  等价于：
  func = decorator(func)

  装饰器是一个"接收函数、返回新函数"的函数。

今天要写的 @login_required 装饰器：

  from functools import wraps
  from flask import session, redirect, url_for

  def login_required(f):
      @wraps(f)  # 保留原函数的 __name__ 等属性
      def decorated_function(*args, **kwargs):
          if "user_id" not in session:
              return redirect(url_for("login"))
          return f(*args, **kwargs)
      return decorated_function

  使用：
  @app.route("/students")
  @login_required  # 先检查登录，未登录跳转到 /login
  def student_list():
      return "学生列表页面"

C++ 对比：
  C++ 中没有装饰器语法，类似功能需要用：
    - 基类 + 虚函数（模板方法模式）
    - 函数指针 / std::function 包装
    - RAII guard 对象
  Python 的装饰器语法糖让这类"横切关注点"（cross-cutting concern）
  的实现非常简洁。
"""

from functools import wraps

def demo_decorator():
    """演示装饰器原理（不用 Flask，纯 Python）"""

    def my_decorator(func):
        """这是一个装饰器：接收函数，返回包装后的函数"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"  [装饰器] 调用 {func.__name__} 之前")
            result = func(*args, **kwargs)
            print(f"  [装饰器] 调用 {func.__name__} 之后")
            return result
        return wrapper

    @my_decorator
    def say_hello(name):
        print(f"  你好, {name}!")

    print("调用被装饰的函数:")
    say_hello("世界")

demo_decorator()


# ============================================================
# 第三部分：Web 上下文中的数据库操作
# ============================================================

print("\n" + "=" * 60)
print("第三部分：Web vs CLI — 数据库操作对比")
print("=" * 60)

"""
CLI 模式（Day 9/10）：
  def add_student():
      name = input("姓名: ")       # 从键盘读取
      age = int(input("年龄: "))
      db.add_student(name, age)
      print("添加成功")             # 输出到终端

Web 模式（Day 13）：
  @app.route("/student/add", methods=["GET", "POST"])
  def add_student():
      if request.method == "POST":
          name = request.form["name"]    # 从表单读取
          age = int(request.form["age"])
          db.add_student(name, age)
          return redirect(url_for("student_list"))  # 跳转到列表页
      return render_template("add_student.html")     # 显示表单

关键区别：
  ┌──────────┬─────────────────┬─────────────────┐
  │          │ CLI             │ Web             │
  ├──────────┼─────────────────┼─────────────────┤
  │ 输入     │ input()         │ request.form    │
  │ 输出     │ print()         │ render_template │
  │ 跳转     │ 函数调用         │ redirect()      │
  │ 状态保持  │ 全局变量         │ session         │
  │ 并发     │ 单用户           │ 多用户（每人独立session）│
  └──────────┴─────────────────┴─────────────────┘

PRG 模式（Post-Redirect-Get）：
  1. POST 处理表单提交（如登录、注册、添加数据）
  2. Redirect 重定向到结果页面
  3. GET   浏览器获取结果页面

  好处：用户刷新页面不会重复提交表单！

  示例：
  POST /login → 验证通过 → redirect("/students") → GET /students → 显示页面
  如果用户按 F5 刷新，刷新的是 GET /students，不会重复登录
"""


# ============================================================
# 第四部分：今日项目结构
# ============================================================

print("\n" + "=" * 60)
print("第四部分：今日项目结构")
print("=" * 60)

"""
day13_flask_db/
├── day13_exercise.py    ← 练习文件（你要完成的）
├── day13_solution.py    ← 参考答案
├── day13_notes.py       ← 本文件（知识讲解）
└── templates/           ← Jinja2 模板目录
    ├── layout.html      ← 基础模板（导航栏 + 页脚）
    ├── login.html       ← 登录页面
    ├── register.html    ← 注册页面
    └── student_list.html← 学生列表页面（受保护）

路由设计：
  /            → 首页（公开）
  /login       → 登录（公开，GET=显示表单，POST=处理登录）
  /logout      → 退出（清除 session，跳转首页）
  /register    → 注册（公开，GET=显示表单，POST=处理注册）
  /students    → 学生列表（受保护，需要登录）

今天的三道练习：
  练习 1：实现 Web 登录页面（Flask + UserDB）
  练习 2：实现注册页面 + 登录保护装饰器
  练习 3：登录后显示学生列表（数据库 → HTML 表格）
"""

print("\n[OK] Day 13 笔记阅读完毕，开始做练习吧！")
print("练习文件: day13_exercise.py")
