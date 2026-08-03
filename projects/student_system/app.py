"""
学生管理系统 — Flask + SQLite + Bootstrap
=========================================
功能：用户注册/登录、学生信息 CRUD、搜索、权限保护
启动：python app.py  →  http://localhost:5000
测试账号：admin / admin123
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
app.secret_key = "student-system-secret-key-2024"


# ============================================================
# 数据库层
# ============================================================

class UserDB:
    """用户表：username / password_hash / salt / role"""

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
    """学生表：name / age / grade / major / created_at，支持 CRUD + 搜索"""

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


# 全局数据库实例（同一文件存用户表和学生表）
user_db = UserDB()
student_db = StudentDB()


# ============================================================
# 登录保护装饰器
# ============================================================

def login_required(func):
    """未登录用户重定向到登录页"""
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
    """首页：已登录显示功能入口，未登录显示登录/注册按钮"""
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """登录：POST 验证用户名密码，成功写入 session"""
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
    """退出：清除 session，重定向到首页"""
    session.clear()
    flash("已安全退出", "info")
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    """注册：验证表单 → 写入数据库 → 重定向到登录页"""
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
    """学生列表：支持 ?q=关键字 模糊搜索姓名/专业"""
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
    """添加学生：GET 显示表单，POST 验证并写入（PRG 模式）"""
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        age_str = request.form.get("age", "").strip()
        grade = request.form.get("grade", "").strip()
        major = request.form.get("major", "").strip()

        if not name:
            flash("姓名不能为空", "error")
            return render_template("add_student.html",
                                   name=name, age=age_str, grade=grade, major=major)
        if not age_str.isdigit():
            flash("年龄必须是正整数", "error")
            return render_template("add_student.html",
                                   name=name, age=age_str, grade=grade, major=major)
        age = int(age_str)
        if age < 1 or age > 150:
            flash("年龄必须在 1-150 之间", "error")
            return render_template("add_student.html",
                                   name=name, age=age_str, grade=grade, major=major)

        ok, result = student_db.add_student(name, age, grade, major)
        if ok:
            flash(f"学生「{name}」添加成功！", "success")
            return redirect(url_for("student_list"))
        else:
            flash(f"添加失败: {result}", "error")
            return render_template("add_student.html",
                                   name=name, age=age_str, grade=grade, major=major)

    return render_template("add_student.html",
                           name="", age="", grade="", major="")


@app.route("/students/<int:student_id>/edit", methods=["GET", "POST"])
@login_required
def edit_student(student_id):
    """编辑学生：GET 预填表单，POST 验证并更新（PRG 模式）"""
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
    """删除学生：仅接受 POST，前端 confirm 确认后提交"""
    ok, msg = student_db.delete_student(student_id)
    if ok:
        flash("学生删除成功", "success")
    else:
        flash(msg, "error")
    return redirect(url_for("student_list"))


# ============================================================
# 测试数据 & 启动
# ============================================================

def init_test_data():
    """首次运行时创建管理员账号和示例学生数据"""
    user_db.register("admin", "admin123", role="admin")
    if student_db.count_students() == 0:
        student_db.add_student("张三", 20, "2024级1班", "计算机科学")
        student_db.add_student("李四", 19, "2024级2班", "软件工程")
        student_db.add_student("王五", 21, "2023级1班", "人工智能")
        student_db.add_student("赵六", 22, "2023级2班", "数据科学")
        student_db.add_student("陈七", 19, "2024级3班", "计算机科学")


if __name__ == "__main__":
    init_test_data()
    print("学生管理系统已启动 → http://localhost:5000")
    print("测试账号: admin / admin123")
    app.run(debug=True)
