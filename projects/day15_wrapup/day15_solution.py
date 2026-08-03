"""
============================================================
Day 15 参考答案：项目收尾 — Bootstrap 美化 / 工程化规范
============================================================
这是 day15_exercise.py 的完整参考答案。
做完练习后再看这个文件，对比你的实现和参考答案。

运行方式：
  python day15_solution.py
  浏览器访问: http://localhost:5000
  测试账号: admin / admin123

今天的目标是把 Day 14 的项目打磨到"可交付"状态：
  1. Bootstrap 5 美化（替换手写 CSS）
  2. 工程化文件（README.md / requirements.txt / .gitignore）
  3. 自动化测试（pytest）
"""

from flask import (
    Flask, render_template, request, redirect, url_for,
    session, flash
)
from functools import wraps
import sqlite3
import hashlib
import os

app = Flask(__name__)
app.secret_key = "day15-solution-secret-key"


# ============================================================
# 数据库类（同 Day 14）
# ============================================================

class UserDB:
    """用户数据库"""

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
    """学生数据库 — 完整 CRUD + 搜索"""

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

    def get_student(self, student_id):
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(
                "SELECT id, name, age, grade, major, created_at "
                "FROM students WHERE id = ?",
                (student_id,)
            ).fetchone()
            return dict(row) if row else None

    def update_student(self, student_id, name, age, grade, major):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    "UPDATE students SET name=?, age=?, grade=?, major=? "
                    "WHERE id=?",
                    (name, age, grade, major, student_id)
                )
                if cursor.rowcount == 0:
                    return False, "学生不存在"
                return True, "更新成功"
        except sqlite3.Error as e:
            return False, f"更新失败: {e}"

    def delete_student(self, student_id):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    "DELETE FROM students WHERE id = ?",
                    (student_id,)
                )
                if cursor.rowcount == 0:
                    return False, "学生不存在"
                return True, "删除成功"
        except sqlite3.Error as e:
            return False, f"删除失败: {e}"

    def search_students(self, keyword):
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            pattern = f"%{keyword}%"
            rows = conn.execute(
                "SELECT id, name, age, grade, major, created_at "
                "FROM students "
                "WHERE name LIKE ? OR major LIKE ? "
                "ORDER BY id",
                (pattern, pattern)
            ).fetchall()
            return [dict(r) for r in rows]


# 全局数据库实例
user_db = UserDB()
student_db = StudentDB()


# ============================================================
# 登录保护装饰器
# ============================================================

def login_required(func):
    """登录保护：未登录用户重定向到 /login"""
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("请先登录后再操作", "error")
            return redirect(url_for("login"))
        return func(*args, **kwargs)
    return decorated_function


# ============================================================
# 路由
# ============================================================

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        if not username or not password:
            return render_template("login.html", error="用户名和密码不能为空")
        ok, result = user_db.login(username, password)
        if ok:
            session["user_id"] = result["id"]
            session["username"] = result["username"]
            session["role"] = result["role"]
            flash(f"欢迎回来, {result['username']}！", "success")
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error=result)
    return render_template("login.html", error=None)


@app.route("/logout")
def logout():
    session.clear()
    flash("已安全退出", "info")
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        confirm = request.form.get("confirm_password", "").strip()
        if not username or not password:
            return render_template("register.html", error="用户名和密码不能为空")
        if password != confirm:
            return render_template("register.html", error="两次密码不一致")
        if len(password) < 6:
            return render_template("register.html", error="密码至少需要 6 位")
        ok, msg = user_db.register(username, password)
        if ok:
            flash("注册成功！请登录", "success")
            return redirect(url_for("login"))
        else:
            return render_template("register.html", error=msg)
    return render_template("register.html", error=None)


@app.route("/students")
@login_required
def student_list():
    keyword = request.args.get("q", "").strip()
    if keyword:
        students = student_db.search_students(keyword)
    else:
        students = student_db.get_all_students()
    return render_template(
        "student_list.html",
        students=students,
        username=session.get("username"),
        keyword=keyword
    )


@app.route("/students/add", methods=["GET", "POST"])
@login_required
def add_student():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        age_str = request.form.get("age", "").strip()
        grade = request.form.get("grade", "").strip()
        major = request.form.get("major", "").strip()

        if not name:
            flash("姓名不能为空", "error")
            return render_template("add_student.html",
                                   name=name, age=age_str,
                                   grade=grade, major=major)
        if not age_str.isdigit():
            flash("年龄必须是正整数", "error")
            return render_template("add_student.html",
                                   name=name, age=age_str,
                                   grade=grade, major=major)
        age = int(age_str)
        if age < 1 or age > 150:
            flash("年龄必须在 1-150 之间", "error")
            return render_template("add_student.html",
                                   name=name, age=age_str,
                                   grade=grade, major=major)

        ok, result = student_db.add_student(name, age, grade, major)
        if ok:
            flash(f"学生「{name}」添加成功！", "success")
            return redirect(url_for("student_list"))
        else:
            flash(f"添加失败: {result}", "error")
            return render_template("add_student.html",
                                   name=name, age=age_str,
                                   grade=grade, major=major)

    return render_template("add_student.html",
                           name="", age="", grade="", major="")


@app.route("/students/<int:student_id>/edit", methods=["GET", "POST"])
@login_required
def edit_student(student_id):
    student = student_db.get_student(student_id)
    if student is None:
        flash("学生不存在", "error")
        return redirect(url_for("student_list"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        age_str = request.form.get("age", "").strip()
        grade = request.form.get("grade", "").strip()
        major = request.form.get("major", "").strip()

        if not name:
            flash("姓名不能为空", "error")
            return render_template("edit_student.html", student=student)
        if not age_str.isdigit():
            flash("年龄必须是正整数", "error")
            return render_template("edit_student.html", student=student)
        age = int(age_str)
        if age < 1 or age > 150:
            flash("年龄必须在 1-150 之间", "error")
            return render_template("edit_student.html", student=student)

        ok, msg = student_db.update_student(student_id, name, age, grade, major)
        if ok:
            flash(f"学生「{name}」更新成功！", "success")
            return redirect(url_for("student_list"))
        else:
            flash(msg, "error")
            return render_template("edit_student.html", student=student)

    return render_template("edit_student.html", student=student)


@app.route("/students/<int:student_id>/delete", methods=["POST"])
@login_required
def delete_student(student_id):
    ok, msg = student_db.delete_student(student_id)
    if ok:
        flash("学生删除成功", "success")
    else:
        flash(msg, "error")
    return redirect(url_for("student_list"))


# ============================================================
# 测试数据初始化
# ============================================================

def init_test_data():
    """初始化测试数据"""
    ok, _ = user_db.register("admin", "admin123", role="admin")
    if ok:
        print("  创建管理员: admin / admin123")
    if student_db.count_students() == 0:
        student_db.add_student("张三", 20, "2024级1班", "计算机科学")
        student_db.add_student("李四", 19, "2024级2班", "软件工程")
        student_db.add_student("王五", 21, "2023级1班", "人工智能")
        student_db.add_student("赵六", 22, "2023级2班", "数据科学")
        student_db.add_student("陈七", 19, "2024级3班", "计算机科学")
        print("  已插入 5 条测试学生数据")


# ============================================================
# 启动服务器
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Day 15 项目收尾 — Bootstrap 美化版")
    print("=" * 60)
    init_test_data()
    print()
    print("Bootstrap 5 美化特性：")
    print("  ✓ 深色导航栏（navbar-dark bg-dark）")
    print("  ✓ 响应式布局（移动端适配）")
    print("  ✓ Bootstrap 表格（table-striped + table-hover）")
    print("  ✓ 可关闭的 alert 消息（alert-dismissible）")
    print("  ✓ 美化的表单控件（form-control）")
    print()
    print("测试账号: admin / admin123")
    print("按 Ctrl+C 停止服务器")
    print("=" * 60)
    app.run(debug=True)


# ══════════════════════════════════════════════════════════════
# 参考答案说明：Bootstrap 模板改造要点
# ══════════════════════════════════════════════════════════════
#
# Python 代码和 Day 14 完全一样，核心改动在模板文件。
# 以下是你应该完成的 Bootstrap 模板改造要点：
#
# ── layout.html 改造要点 ──
#
# 1. 引入 Bootstrap CDN（替代手写 <style>）：
#    <head>
#        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
#              rel="stylesheet">
#    </head>
#    <body>
#        ...
#        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js">
#        </script>
#    </body>
#
# 2. 导航栏用 Bootstrap navbar：
#    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
#        <div class="container-fluid">
#            <a class="navbar-brand" href="{{ url_for('index') }}">🏠 学生管理系统</a>
#            <button class="navbar-toggler" type="button" data-bs-toggle="collapse"
#                    data-bs-target="#navbarNav">
#                <span class="navbar-toggler-icon"></span>
#            </button>
#            <div class="collapse navbar-collapse" id="navbarNav">
#                <div class="navbar-nav me-auto">
#                    {% if session.get("user_id") %}
#                    <a class="nav-link" href="{{ url_for('student_list') }}">📋 学生列表</a>
#                    <a class="nav-link" href="{{ url_for('add_student') }}">➕ 添加学生</a>
#                    {% endif %}
#                </div>
#                <div class="navbar-nav">
#                    {% if session.get("user_id") %}
#                    <span class="navbar-text me-3">
#                        👤 {{ session.get("username") }} ({{ session.get("role") }})
#                    </span>
#                    <a class="nav-link" href="{{ url_for('logout') }}">退出</a>
#                    {% else %}
#                    <a class="nav-link" href="{{ url_for('login') }}">登录</a>
#                    <a class="nav-link" href="{{ url_for('register') }}">注册</a>
#                    {% endif %}
#                </div>
#            </div>
#        </div>
#    </nav>
#
# 3. 容器用 Bootstrap container：
#    <div class="container mt-4">
#
# 4. Flash 消息用 Bootstrap alert（可关闭）：
#    {% with messages = get_flashed_messages(with_categories=true) %}
#    {% if messages %}
#    {% for category, message in messages %}
#    {% set alert_class = {
#        'success': 'alert-success',
#        'error': 'alert-danger',
#        'info': 'alert-info',
#        'warning': 'alert-warning'
#    }.get(category, 'alert-info') %}
#    <div class="alert {{ alert_class }} alert-dismissible fade show">
#        {{ message }}
#        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
#    </div>
#    {% endfor %}
#    {% endif %}
#    {% endwith %}
#
#    关键点：flash 的 category 映射到 Bootstrap alert class：
#      success → alert-success (绿色)
#      error   → alert-danger  (红色)  -- 注意！不是 alert-error
#      info    → alert-info    (蓝色)
#      warning → alert-warning (黄色)
#    alert-dismissible + btn-close + data-bs-dismiss="alert" 让消息可点击关闭
#
# 5. 删掉所有手写 CSS（nav, .container, .flash-xxx, table, .btn, .form-group 等）
#
# ── student_list.html 改造要点 ──
#
# 1. 表格:
#    <table class="table table-striped table-hover">
#
# 2. 搜索表单（用 input-group 替代手写 CSS）:
#    <form method="get" action="{{ url_for('student_list') }}" class="mb-3">
#        <div class="input-group">
#            <input type="text" name="q" class="form-control"
#                   value="{{ keyword or '' }}" placeholder="🔍 搜索姓名或专业...">
#            <button type="submit" class="btn btn-primary">搜索</button>
#            {% if keyword %}
#            <a href="{{ url_for('student_list') }}" class="btn btn-outline-secondary">清除</a>
#            {% endif %}
#        </div>
#    </form>
#
# 3. 按钮:
#    编辑: <a href="..." class="btn btn-sm btn-outline-primary">✏️ 编辑</a>
#    删除: <button class="btn btn-sm btn-outline-danger">🗑️ 删除</button>
#    添加: <a href="..." class="btn btn-success">➕ 添加学生</a>
#
# 4. 空数据提示:
#    <div class="alert alert-info">暂无学生数据</div>
#
# ── add_student.html / edit_student.html 改造要点 ──
#
# 1. 表单字段（用 mb-3 + form-label + form-control）:
#    <div class="mb-3">
#        <label for="name" class="form-label">姓名</label>
#        <input type="text" id="name" name="name"
#               class="form-control" value="{{ name or '' }}" required>
#    </div>
#
# 2. 必填标记用 Bootstrap text-danger:
#    <label class="form-label">姓名 <span class="text-danger">*</span></label>
#
# ── login.html / register.html 改造要点 ──
#
# 1. 居中卡片布局：
#    <div class="row justify-content-center">
#        <div class="col-md-6 col-lg-4">
#            <div class="card">
#                <div class="card-body">
#                    <h3 class="card-title text-center mb-4">🔐 登录</h3>
#                    ...表单...
#                </div>
#            </div>
#        </div>
#    </div>
#
# 2. 错误消息用 alert-danger
# 3. 表单字段同样用 form-control + mb-3
