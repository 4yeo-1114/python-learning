"""
============================================================
Day 14 参考答案：Web CRUD 完成
============================================================
这是 day14_exercise.py 的完整参考答案。
做完练习后再看这个文件，对比你的实现和参考答案。

运行方式：
  python day14_solution.py
  浏览器访问: http://localhost:5000
  测试账号: admin / admin123
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
app.secret_key = "day14-secret-key-for-flash-and-session"


# ============================================================
# 数据库类
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
    """学生数据库 — 包含完整 CRUD + 搜索"""

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

    # ── 已有的方法 ──

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

    # ── 练习 1 新增的方法 ──

    def get_student(self, student_id):
        """
        根据 id 获取单个学生。
        返回 dict 或 None（不存在时）。
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(
                "SELECT id, name, age, grade, major, created_at "
                "FROM students WHERE id = ?",
                (student_id,)
            ).fetchone()
            return dict(row) if row else None

    def update_student(self, student_id, name, age, grade, major):
        """
        更新学生信息。
        返回 (bool, msg)。
        """
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
        """
        根据 id 删除学生。
        返回 (bool, msg)。
        """
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
        """
        按姓名或专业模糊搜索。
        返回 list[dict]。
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            # LIKE 需要 % 通配符做模糊匹配
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
    """登录保护：未登录用户重定向到 /login，并 flash 提示"""
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("请先登录后再操作", "error")
            return redirect(url_for("login"))
        return func(*args, **kwargs)
    return decorated_function


# ============================================================
# 基础路由（Day 13 的内容）
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


# ============================================================
# 练习 3 答案：学生列表（含搜索）— 升级版
# ============================================================

@app.route("/students")
@login_required
def student_list():
    """
    学生列表 — 支持搜索功能。
    有 ?q=xxx 时搜索，没有时显示全部。
    """
    keyword = request.args.get("q", "").strip()

    if keyword:
        students = student_db.search_students(keyword)
    else:
        students = student_db.get_all_students()

    return render_template(
        "student_list.html",
        students=students,
        username=session.get("username"),
        keyword=keyword  # 回填搜索框
    )


# ============================================================
# 练习 1 答案：添加学生（PRG 模式）
# ============================================================

@app.route("/students/add", methods=["GET", "POST"])
@login_required
def add_student():
    """
    添加学生 — GET 显示表单，POST 验证并添加。
    遵循 PRG 模式：POST 成功后 redirect，不直接渲染页面。
    """
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        age_str = request.form.get("age", "").strip()
        grade = request.form.get("grade", "").strip()
        major = request.form.get("major", "").strip()

        # ── 表单验证 ──
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

        # ── 数据库操作 ──
        ok, result = student_db.add_student(name, age, grade, major)
        if ok:
            flash(f"学生「{name}」添加成功！", "success")
            # ★ PRG 模式：重定向到列表页
            return redirect(url_for("student_list"))
        else:
            flash(f"添加失败: {result}", "error")
            return render_template("add_student.html",
                                   name=name, age=age_str,
                                   grade=grade, major=major)

    # GET 请求 — 显示空白表单
    return render_template("add_student.html",
                           name="", age="", grade="", major="")


# ============================================================
# 练习 2 答案：编辑 + 删除学生
# ============================================================

@app.route("/students/<int:student_id>/edit", methods=["GET", "POST"])
@login_required
def edit_student(student_id):
    """
    编辑学生 — GET 显示预填表单，POST 更新数据。
    遵循 PRG 模式。
    """
    student = student_db.get_student(student_id)

    # 学生不存在 → 返回列表
    if student is None:
        flash("学生不存在", "error")
        return redirect(url_for("student_list"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        age_str = request.form.get("age", "").strip()
        grade = request.form.get("grade", "").strip()
        major = request.form.get("major", "").strip()

        # ── 表单验证（和添加学生一致）──
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

        # ── 更新数据库 ──
        ok, msg = student_db.update_student(student_id, name, age, grade, major)
        if ok:
            flash(f"学生「{name}」更新成功！", "success")
            # ★ PRG 模式
            return redirect(url_for("student_list"))
        else:
            flash(msg, "error")
            return render_template("edit_student.html", student=student)

    # GET 请求 — 显示预填表单
    return render_template("edit_student.html", student=student)


@app.route("/students/<int:student_id>/delete", methods=["POST"])
@login_required
def delete_student(student_id):
    """
    删除学生 — 只用 POST（防止爬虫误删）。
    遵循 PRG 模式。
    """
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
    print("Day 14 Web CRUD 参考答案服务器启动中...")
    print("=" * 60)
    init_test_data()
    print()
    print("可用路由（RESTful）：")
    print("  GET  /                      首页")
    print("  GET  /students              学生列表 + 搜索（?q=xxx）")
    print("  GET  /students/add          添加学生表单")
    print("  POST /students/add          提交添加 → PRG")
    print("  GET  /students/<id>/edit    编辑学生表单")
    print("  POST /students/<id>/edit    提交编辑 → PRG")
    print("  POST /students/<id>/delete  删除学生 → PRG")
    print("  GET  /login /logout /register")
    print()
    print("测试账号: admin / admin123")
    print("体验重点：")
    print("  1. 添加学生后看 flash 消息")
    print("  2. 刷新页面看消息是否消失")
    print("  3. 编辑学生 → 按 F5 不会重复提交")
    print("  4. 搜索 '计算机' → 看到模糊匹配结果")
    print("  5. 删除学生 → 有确认对话框")
    print("按 Ctrl+C 停止服务器")
    print("=" * 60)
    app.run(debug=True)
