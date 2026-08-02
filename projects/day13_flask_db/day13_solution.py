"""
============================================================
Day 13 参考答案：Flask + 数据库整合
============================================================
这是 day13_exercise.py 的完整参考答案。
做完练习后再看这个文件，对比你的实现和参考答案。

运行方式：
  python day13_solution.py
  浏览器访问: http://localhost:5000
  测试账号: admin / admin123
"""

from flask import Flask, render_template, request, redirect, url_for, session
from functools import wraps
import sqlite3
import hashlib
import os

app = Flask(__name__)
app.secret_key = "day13-secret-key-for-session"


# ============================================================
# 数据库类（重用 Day 9/10 的代码）
# ============================================================

class UserDB:
    """用户数据库 — Day 9 的内容"""

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
                    "INSERT INTO users (username, password_hash, salt, role) "
                    "VALUES (?, ?, ?, ?)",
                    (username, pw_hash, salt, role)
                )
            return True, "注册成功"
        except sqlite3.IntegrityError:
            return False, "用户名已存在"

    def login(self, username, password):
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(
                "SELECT id, username, password_hash, salt, role "
                "FROM users WHERE username = ?",
                (username,)
            ).fetchone()

            if row is None:
                return False, "用户名不存在"
            if not self._verify_password(password, row["salt"], row["password_hash"]):
                return False, "密码错误"

            return True, {
                "id": row["id"],
                "username": row["username"],
                "role": row["role"],
            }


class StudentDB:
    """学生数据库 — Day 10 的内容"""

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
                    "INSERT INTO students (name, age, grade, major) "
                    "VALUES (?, ?, ?, ?)",
                    (name, age, grade, major)
                )
                return True, cursor.lastrowid
        except sqlite3.Error as e:
            return False, f"添加失败: {e}"

    def get_all_students(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT id, name, age, grade, major, created_at "
                "FROM students ORDER BY id"
            ).fetchall()
            return [dict(r) for r in rows]

    def count_students(self):
        with sqlite3.connect(self.db_path) as conn:
            return conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]


# 全局数据库实例
user_db = UserDB()
student_db = StudentDB()


# ============================================================
# 练习 2 答案：登录保护装饰器
# ============================================================

def login_required(func):
    """
    登录保护装饰器
    原理：检查 session 中是否有 user_id
    未登录 → 重定向到 /login
    已登录 → 正常执行原函数
    """
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return func(*args, **kwargs)
    return decorated_function


# ============================================================
# 练习 1 答案：首页 + 登录 + 退出
# ============================================================

@app.route("/")
def index():
    """
    首页 — 根据登录状态显示不同内容
    """
    if session.get("user_id"):
        return render_template("index.html")
    else:
        return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    登录页 — GET 显示表单，POST 验证登录
    """
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        # 基本验证
        if not username or not password:
            return render_template("login.html", error="用户名和密码不能为空")

        # 数据库验证
        ok, result = user_db.login(username, password)
        if ok:
            # 登录成功 → 存入 session
            session["user_id"] = result["id"]
            session["username"] = result["username"]
            session["role"] = result["role"]
            return redirect(url_for("index"))
        else:
            # 登录失败 → 显示错误
            return render_template("login.html", error=result)

    # GET 请求 → 显示空白登录表单
    return render_template("login.html", error=None)


@app.route("/logout")
def logout():
    """
    退出登录 — 清除 session，重定向到首页
    """
    session.clear()
    return redirect(url_for("index"))


# ============================================================
# 练习 2 答案：注册
# ============================================================

@app.route("/register", methods=["GET", "POST"])
def register():
    """
    注册页 — GET 显示表单，POST 处理注册
    """
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        confirm = request.form.get("confirm_password", "").strip()

        # 验证 1：不能为空
        if not username or not password:
            return render_template("register.html", error="用户名和密码不能为空")

        # 验证 2：两次密码一致
        if password != confirm:
            return render_template("register.html", error="两次密码不一致")

        # 验证 3：密码长度
        if len(password) < 6:
            return render_template("register.html", error="密码至少需要 6 位")

        # 数据库操作
        ok, msg = user_db.register(username, password)
        if ok:
            # 注册成功 → 去登录
            return redirect(url_for("login"))
        else:
            return render_template("register.html", error=msg)

    # GET 请求 → 显示空白注册表单
    return render_template("register.html", error=None)


# ============================================================
# 练习 3 答案：学生列表（受保护）
# ============================================================

@app.route("/students")
@login_required
def student_list():
    """
    学生列表 — 必须登录才能访问
    从 SQLite 读取数据，用 HTML 表格展示
    """
    students = student_db.get_all_students()
    return render_template(
        "student_list.html",
        students=students,
        username=session.get("username")
    )


# ============================================================
# 额外的：首页模板（不用 extends 的简单版本，内联渲染）
# ============================================================

@app.route("/raw-index")
def raw_index():
    """
    备选首页 — 纯 Python 字符串渲染，
    展示不用模板时如何在 Python 中判断登录状态
    对比：layout.html 中用 {% if session.get("user_id") %} 做同样的事
    """
    if session.get("user_id"):
        welcome = f"""
        <h1>欢迎回来, {session['username']}!</h1>
        <p>你的角色: {session['role']}</p>
        <p>
            <a href="/students">查看学生列表</a> |
            <a href="/logout">退出登录</a>
        </p>
        """
    else:
        welcome = """
        <h1>欢迎来到学生管理系统</h1>
        <p>请先登录或注册。</p>
        <p>
            <a href="/login">登录</a> |
            <a href="/register">注册</a>
        </p>
        """
    return welcome


# ============================================================
# 测试数据初始化
# ============================================================

def init_test_data():
    """初始化测试数据"""
    # 创建默认管理员
    ok, msg = user_db.register("admin", "admin123", role="admin")
    if ok:
        print(f"  创建管理员: admin / admin123")

    # 插入测试学生
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
    print("Day 13 Flask + 数据库整合 参考答案服务器启动中...")
    print("=" * 60)
    init_test_data()
    print()
    print("可用路由：")
    print("  /              首页")
    print("  /login         登录页 (GET/POST)")
    print("  /register      注册页 (GET/POST)")
    print("  /logout        退出登录")
    print("  /students      学生列表（登录保护）")
    print("  /raw-index     纯 Python 渲染首页（对比版）")
    print()
    print("测试流程：")
    print("  1. 访问 /students → 未登录，自动跳转 /login")
    print("  2. 用 admin/admin123 登录 → 跳转首页")
    print("  3. 访问 /students → 显示学生列表表格")
    print("  4. 点击退出 → 清除 session，回到首页")
    print()
    print("按 Ctrl+C 停止服务器")
    print("=" * 60)
    app.run(debug=True)
