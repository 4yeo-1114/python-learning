"""
============================================================
Day 13 练习：Flask + 数据库整合
============================================================
在开始前，请先阅读 day13_notes.py 理解今天的知识点，
然后完成下面的练习（3 道题，每题约 15-20 分钟）。

今天的主题：**把 Day 9/10 的数据库整合到 Web 中**
你会用到 Flask session、登录保护装饰器、模板中渲染数据库数据

运行方式：
  在终端执行：python day13_exercise.py
  然后浏览器打开：http://localhost:5000
"""

from flask import Flask, render_template, request, redirect, url_for, session
from functools import wraps
import sqlite3
import hashlib
import os

app = Flask(__name__)
app.secret_key = "day13-secret-key-for-session"  # session 加密密钥

# ============================================================
# 数据库类（从 Day 9/10 搬过来的，已经写好，你可以直接用）
# ============================================================

class UserDB:
    """用户数据库（Day 9 的内容）"""

    def __init__(self, db_path="students.db"):
        self.db_path = db_path
        self._init_table()

    def _init_table(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    salt TEXT NOT NULL,
                    role TEXT DEFAULT 'student'
                )
            """)

    @staticmethod
    def _hash_password(password):
        salt = os.urandom(16).hex()
        hashed = hashlib.sha256((password + salt).encode()).hexdigest()
        return salt, hashed

    @staticmethod
    def _verify_password(password, salt, stored_hash):
        return hashlib.sha256((password + salt).encode()).hexdigest() == stored_hash

    def register(self, username, password, role="student"):
        salt, pw_hash = self._hash_password(password)
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    "INSERT INTO users (username, password_hash, salt, role) VALUES (?, ?, ?, ?)",
                    (username, pw_hash, salt, role)
                )
            return True, "注册成功"
        except sqlite3.IntegrityError:
            return False, "用户名已存在"

    def login(self, username, password):
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(
                "SELECT id, username, password_hash, salt, role FROM users WHERE username = ?",
                (username,)
            ).fetchone()
            if row is None:
                return False, "用户名不存在"
            if not self._verify_password(password, row["salt"], row["password_hash"]):
                return False, "密码错误"
            return True, {"id": row["id"], "username": row["username"], "role": row["role"]}


class StudentDB:
    """学生数据库（Day 10 的内容）"""

    def __init__(self, db_path="students.db"):
        self.db_path = db_path
        self._init_table()

    def _init_table(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    age INTEGER,
                    grade TEXT DEFAULT '',
                    major TEXT DEFAULT '',
                    created_at TEXT DEFAULT (datetime('now', 'localtime'))
                )
            """)

    def add_student(self, name, age, grade="", major=""):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    "INSERT INTO students (name, age, grade, major) VALUES (?, ?, ?, ?)",
                    (name, age, grade, major)
                )
                return True, cursor.lastrowid
        except sqlite3.Error as e:
            return False, f"添加失败: {e}"

    def get_all_students(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT id, name, age, grade, major, created_at FROM students ORDER BY id"
            ).fetchall()
            return [dict(r) for r in rows]

    def count_students(self):
        with sqlite3.connect(self.db_path) as conn:
            return conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]


# 创建全局数据库实例
user_db = UserDB()
student_db = StudentDB()


# ============================================================
# 练习 1：实现 Web 登录页面
# ============================================================
"""
题目：实现 Web 端的登录功能（Flask + UserDB）

你的任务：
1. 完成 "/" 首页路由：
   - 如果已登录（session 中有 user_id），显示用户名 + 退出链接
   - 如果未登录，显示"请先登录" + 跳转链接
   - 提示: 用 session.get("user_id") 检查登录状态

2. 完成 "/login" 路由（支持 GET 和 POST）：
   GET 请求：
   - 渲染 login.html 模板（空白表单）
   POST 请求：
   - 从 request.form 获取 username 和 password
   - 调用 user_db.login(username, password) 验证
   - 登录成功：把用户信息存到 session，重定向到首页
     提示: session["user_id"] = user["id"]
           session["username"] = user["username"]
           session["role"] = user["role"]
   - 登录失败：重新渲染 login.html，传入错误信息
     提示: render_template("login.html", error="用户名或密码错误")

3. 完成 "/logout" 路由：
   - 清除 session（session.clear()）
   - 重定向到首页

要求：
- 登录表单 method="POST"
- 用户名输入框 name="username"
- 密码输入框 name="password"（type="password"）
- 登录成功后重定向，不要停留在 /login 页

提示：
  - Flask session 像字典一样用
  - session 数据在请求之间自动保持（通过加密 cookie）
  - 重定向用 return redirect(url_for("路由函数名"))

预计时间：20 分钟
"""

# --- 首页路由 ---
@app.route("/")
def index():
    # TODO: 检查登录状态，返回欢迎信息或提示登录
    if session.get("user_id"):
        return render_template("index.html")
    else:
        return render_template("index.html")


# --- 登录路由 ---
@app.route("/login", methods=["GET", "POST"])
def login():
    # TODO: GET 显示表单，POST 验证登录
    if request.method == "POST":
        username = request.form.get("username","").strip()
        password = request.form.get("password","").strip()
        
        
        
        if not username or not password:
            return render_template("login.html", error="用户名和密码不能为空")
        
        ok,result = user_db.login(username,password)
        if ok:
            #登录成功 存入session
            session["user_id"] = result["id"]
            session["username"] = result["username"]
            session["role"] =  result["role"]
            return redirect(url_for("index"))
        else:
            #登录失败
            return render_template("login.html",error = result)
    
    #GET请求 显示空白登录页面
    return render_template("login.html",error=None)


# --- 退出路由 ---
@app.route("/logout")
def logout():
    # TODO: 清除 session，重定向到首页
    session.clear()
    return redirect(url_for("index"))


# ============================================================
# 练习 2：注册页面 + 登录保护装饰器
# ============================================================
"""
题目：实现注册功能，并创建 @login_required 装饰器保护需要登录的页面

你的任务：
1. 完成 "/register" 路由（支持 GET 和 POST）：
   GET 请求：
   - 渲染 register.html 模板（空白表单）
   POST 请求：
   - 从 request.form 获取 username, password, confirm_password
   - 检查两次密码是否一致
   - 检查密码长度 >= 6
   - 调用 user_db.register(username, password)
   - 注册成功：重定向到 /login（让用户去登录）
   - 注册失败：重新渲染 register.html，传入错误信息
     提示: render_template("register.html", error="错误信息")

2. 完成 login_required 装饰器（下面的 TODO）：
   - 参考 day13_notes.py 第二部分
   - 检查 session 中是否有 "user_id"
   - 未登录：重定向到 /login
   - 已登录：执行被装饰的原函数

3. 用 @login_required 保护 /students 路由：
   @app.route("/students")
   @login_required   ← 放在 @app.route 下面（内层先执行）
   def student_list():
       ...

要求：
- 注册表单 method="POST"
- confirm_password 字段用于确认密码
- 装饰器用 @wraps(func) 保留原函数元信息
- @login_required 必须放在 @app.route 和 def 之间

提示：
  - from functools import wraps（已经在顶部导入）
  - 装饰器的顺序：@app.route 是最外层，@login_required 是内层
  - 注册成功后不需要自动登录，让用户自己去 /login

预计时间：20 分钟
"""

# TODO: 完成 login_required 装饰器
def login_required(func):
    """登录保护装饰器：未登录用户重定向到 /login"""
    # @wraps(func)
    # def decorated_function(*args, **kwargs):
    #     if "user_id" not in session:
    #         return redirect(url_for("login"))
    #     return func(*args, **kwargs)
    # return decorated_function
    @wraps(func)
    def decorated_function(*args,**kargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return func(*args,**kargs)
    return decorated_function


# --- 注册路由 ---
@app.route("/register", methods=["GET", "POST"])
def register():
    # TODO: GET 显示表单，POST 处理注册
    if request.method == "POST":
        username = request.form.get("username","").strip()
        password = request.form.get("password","").strip()
        confirm = request.form.get("confirm_password","").strip()
        
        if not username or not password:
            return render_template("register.html",error="用户名和密码不能为空")
        
        if password != confirm:
            return render_template("register.html",error = "两次密码不一致")
        
        if len(password)<6:
            return render_template("register.html",error="密码至少需要六位")
        
        ok,msg = user_db.register(username,password)
        
        if ok:
            #注册成功
            return redirect(url_for("login"))
        else:
            return render_template("register.html",error=msg)
    
    #GET请求 显示空白注册页面
    return render_template("register.html",error=None)



# ============================================================
# 练习 3：登录后显示学生列表（数据库 → HTML 表格）
# ============================================================
"""
题目：登录后访问 /students 查看所有学生，数据来自 SQLite 数据库

你的任务：
1. 完成 "/students" 路由（需要登录保护）：
   - 调用 student_db.get_all_students() 获取所有学生
   - 每个学生是 dict：{"id": 1, "name": "张三", "age": 20, "grade": "2024级1班", "major": "计算机科学", "created_at": "..."}
   - 把学生列表传给模板：render_template("student_list.html", students=students)
   - 同时把当前用户名也传过去，让模板显示"欢迎, xxx"

2. 完成 student_list.html 模板（templates/ 目录下已创建）：
   - 继承 layout.html
   - 用 {% for student in students %} 循环遍历学生
   - 用 <table> 表格显示学生信息
   - 显示字段：ID、姓名、年龄、班级、专业、创建时间
   - students 为空时显示一行提示（用 {% if students %} ... {% else %} ... {% endif %}）

3. 先往数据库插入一些测试数据，再访问 /students：
   在浏览器访问 / 时会自动检查，如果没有测试数据就插入几条。
   或者在 Python 终端手动执行：
   >>> from day13_exercise import student_db
   >>> student_db.add_student("张三", 20, "2024级1班", "计算机科学")
   >>> student_db.add_student("李四", 19, "2024级2班", "软件工程")
   >>> student_db.add_student("王五", 21, "2023级1班", "人工智能")

4. 测试完整流程：
   a) 访问 http://localhost:5000/students（未登录 → 应重定向到 /login）
   b) 登录（admin / admin123 或你注册的账号）
   c) 再次访问 /students（已登录 → 显示学生列表表格）
   d) 退出登录，再次访问 /students（应再次重定向到 /login）

要求：
- /students 路由必须用 @login_required 保护
- 表格数据来自 SQLite 数据库
- 学生列表按 id 排序
- 表格用 <thead> + <tbody> 结构

提示：
  - 模板中的 for 循环：{% for s in students %} ... {% endfor %}
  - 访问字典属性：{{ s.name }} 或 {{ s["name"] }}
  - 如果 {{ }} 里的变量是 None，模板不会报错，显示空字符串
  - layout.html 已提供 {% block content %}{% endblock %} 插槽

预计时间：20 分钟
"""

# --- 学生列表路由（受保护） ---
@app.route("/students")
# TODO: 添加 @login_required 装饰器 必须是在session存在的用户才能使用下面的函数
@login_required
def student_list():
    # TODO: 从数据库获取学生列表，传给模板
    students = student_db.get_all_students()
    return render_template(
        "student_list.html",
        students = students,
        username = session.get("username")
    )


# ============================================================
# 测试数据初始化
# ============================================================

def init_test_data():
    """初始化测试数据：创建一个管理员账号 + 几条学生数据"""
    # 创建默认管理员（如果不存在）
    ok, _ = user_db.register("admin", "admin123", role="admin")
    if ok:
        print(f"  创建管理员: admin / admin123")

    # 插入几条测试学生数据（如果表是空的）
    if student_db.count_students() == 0:
        student_db.add_student("张三", 20, "2024级1班", "计算机科学")
        student_db.add_student("李四", 19, "2024级2班", "软件工程")
        student_db.add_student("王五", 21, "2023级1班", "人工智能")
        student_db.add_student("赵六", 22, "2023级2班", "数据科学")
        print("  已插入 4 条测试学生数据")


# ============================================================
# 启动服务器
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Day 13 Flask + 数据库整合 练习服务器启动中...")
    print("=" * 60)
    init_test_data()
    print()
    print("可用路由：")
    print("  http://localhost:5000/           首页")
    print("  http://localhost:5000/login       登录页")
    print("  http://localhost:5000/register    注册页")
    print("  http://localhost:5000/logout      退出")
    print("  http://localhost:5000/students    学生列表（需登录）")
    print()
    print("测试账号: admin / admin123")
    print("按 Ctrl+C 停止服务器")
    print("=" * 60)
    app.run(debug=True)
