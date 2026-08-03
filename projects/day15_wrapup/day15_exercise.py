"""
============================================================
Day 15 练习：项目收尾 — Bootstrap 美化 / 工程化规范
============================================================
先阅读 day15_notes.py 了解今天的知识点，再完成 3 道练习。

今天不是写新功能，而是把 Day 14 的项目打磨到"可交付"水平。
核心 Python 代码和 Day 14 一样，你的工作是：

  练习 1：Bootstrap 美化页面（替换手写 CSS）
  练习 2：编写 README.md + requirements.txt + .gitignore
  练习 3：整体测试 + 修复遗留问题

运行方式：
  python day15_exercise.py
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
app.secret_key = "day15-secret-key-for-bootstrap"


# ============================================================
# 数据库类（Day 9-14 的内容，已经写好，不用修改）
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
    """登录保护:未登录用户重定向到/login"""
    @wraps(func)
    def decorated_function(*args,**kwargs):
        if "user_id" not in session:
            flash("请先登录后再操作","error")
            return redirect(url_for("login"))
        return func(*args,**kwargs)
    return decorated_function

# ============================================================
# 路由（Day 13-14 的内容，不用修改）
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
    print("Day 15 项目收尾 — 练习服务器启动中...")
    print("=" * 60)
    init_test_data()
    print()
    print("当前模板用的是 Day 14 的手写 CSS 版本")
    print("完成练习 1 后，页面将升级为 Bootstrap 风格")
    print()
    print("测试账号: admin / admin123")
    print("按 Ctrl+C 停止服务器")
    print("=" * 60)
    app.run(debug=True)


# ============================================================
# 练习 1：Bootstrap 美化页面
# ============================================================
"""
题目：把 templates/ 下的所有页面从手写 CSS 改为 Bootstrap 5

你的任务清单（按顺序做，最多 25 分钟）：

1. 修改 layout.html（最关键，占 60% 工作量）：
   a) 在 <head> 中引入 Bootstrap 5 CDN：
      <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
            rel="stylesheet">
   b) 删掉 <style> 标签中的全部手写 CSS（保留一个空的 <style> 以备自定义）
   c) 把导航栏改成 Bootstrap navbar：
      <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
          <div class="container-fluid">
              <a class="navbar-brand" href="/">🏠 学生管理系统</a>
              <div class="navbar-nav me-auto">
                  ...链接...
              </div>
              <div class="navbar-nav">
                  ...登录/用户信息...
              </div>
          </div>
      </nav>
      提示：导航链接用 class="nav-link"，当前用户信息用 class="navbar-text"
   d) 把 .container 改成 Bootstrap 的：
      <div class="container mt-4">
   e) 把 flash 消息的 <div class="flash-xxx"> 改成 Bootstrap alert：
      <div class="alert alert-success alert-dismissible fade show">
          {{ message }}
          <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
      </div>
      映射关系：
        flash-success  → alert-success
        flash-error    → alert-danger
        flash-info     → alert-info
        flash-warning  → alert-warning
   f) 在 </body> 前引入 Bootstrap JS（导航栏和 alert 关闭需要）：
      <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js">
      </script>
   g) 删掉 footer（或者保留但用 Bootstrap 的 text-center text-muted）

2. 修改 student_list.html：
   a) <table> 加 Bootstrap class: class="table table-striped table-hover"
   b) 搜索表单的 <input> 加 class="form-control"
   c) 按钮统一用 Bootstrap: class="btn btn-primary" / "btn btn-success" / "btn btn-danger"
   d) 搜索框和按钮放在 Bootstrap input-group 中会更紧凑：
      <div class="input-group mb-3">
          <input type="text" name="q" class="form-control" ...>
          <button type="submit" class="btn btn-primary">🔍 搜索</button>
      </div>

3. 修改 add_student.html 和 edit_student.html：
   a) 每个表单字段用 Bootstrap 结构：
      <div class="mb-3">
          <label for="name" class="form-label">姓名</label>
          <input type="text" id="name" name="name"
                 class="form-control" value="{{ name or '' }}" required>
      </div>
   b) 按钮用 Bootstrap: class="btn btn-success" / "btn btn-secondary"

4. 修改 login.html 和 register.html：
   a) 表单字段同样用 Bootstrap form-control + mb-3
   b) 错误消息用 Bootstrap alert-danger
   c) 页面居中可以用 Bootstrap grid:
      <div class="row justify-content-center">
          <div class="col-md-6">
              ...表单...
          </div>
      </div>

5. 修改 index.html：
   a) 按钮用 Bootstrap 风格：class="btn btn-primary btn-lg"
   b) 未登录时按钮组可以用 Bootstrap 的 d-grid gap-2

提示：
  - 改完 layout.html 后刷新浏览器，所有页面都会变化（因为都继承 layout）
  - Bootstrap navbar 的 nav-link 会自动给链接加样式，不需要 btn 类
  - alert-dismissible + btn-close + data-bs-dismiss="alert" 让消息可点击关闭
  - 参考笔记中的"常用组件速查表"
  - 遇到样式不对，先用浏览器 F12 看 CSS 是否生效

预计时间：25 分钟
"""


# ============================================================
# 练习 2：编写 README.md + requirements.txt + .gitignore
# ============================================================
"""
题目：为项目创建三个工程化文件

你的任务（10 分钟）：

1. 在 day15_wrapup/ 目录下创建 requirements.txt：
   内容包含：
   Flask==3.1.2
   pytest==9.1.1
   （版本号可以用 pip list 查看你当前安装的版本）

2. 在 day15_wrapup/ 目录下创建 README.md：
   用 Markdown 格式写项目说明，必须包含：
   - # 标题：学生管理系统
   - ## 功能 章节：列出主要功能（注册/登录/CRUD/搜索）
   - ## 技术栈 章节：Python / Flask / SQLite / Bootstrap
   - ## 快速开始 章节：clone → pip install → python → 浏览器
   - ## 项目结构 章节：文件树
   - 测试账号信息

3. 在 day15_wrapup/ 目录下创建 .gitignore：
   必须忽略：
   - __pycache__/ 和 *.pyc
   - *.db（数据库文件）
   - .pytest_cache/
   - venv/ 和 .venv/
   可选忽略：
   - .vscode/ 和 .idea/（IDE 配置）
   - .DS_Store 和 Thumbs.db（系统文件）

4. 验证 .gitignore 是否生效：
   git status 看看 *.db 和 __pycache__ 是否不再显示

提示：
  - requirements.txt 只写项目直接依赖的包，不要 pip freeze 全部导出
  - .gitignore 在 Windows 上如果无法直接创建，可以在 VS Code 中新建文件
  - README.md 写完后可以在 GitHub 上预览效果（把文件拖到浏览器看 Markdown 渲染）
  - 参考笔记中的模板

预计时间：10 分钟
"""


# ============================================================
# 练习 3：整体测试 + 修复遗留问题
# ============================================================
"""
题目：用 pytest 为 StudentDB 写测试，验证应用完整性

你的任务（20 分钟）：

1. 在 day15_wrapup/ 目录下创建 test_app.py：
   用 pytest + fixture 做测试（参考 Day 11 的做法）

   a) 创建 fixture，使用临时数据库（:memory: 或 test.db）
   b) 测试 add_student：添加后 count 应该为 1
   c) 测试 search_students：
      - 添加 "张三"(计算机科学) 和 "李四"(软件工程)
      - 搜索 "计算机" 应该返回 1 条（张三）
      - 搜索 "李四" 应该返回 1 条
      - 搜索 "不存在" 应该返回 0 条
   d) 测试 update_student：修改后 get_student 应返回新数据
   e) 测试 delete_student：删除后 get_student 应返回 None

   测试文件框架：
   ```python
   import pytest
   import sys
   sys.path.insert(0, '.')  # 让 pytest 能导入 day15_exercise

   from day15_exercise import StudentDB

   @pytest.fixture
   def db():
       # 创建使用内存数据库的 StudentDB
       test_db = StudentDB(db_path=":memory:")
       return test_db

   def test_add_student(db):
       ok, sid = db.add_student("张三", 20, "1班", "CS")
       assert ok
       assert db.count_students() == 1

   def test_search_students(db):
       # TODO: 写搜索测试
       pass

   def test_update_student(db):
       # TODO: 写更新测试
       pass

   def test_delete_student(db):
       # TODO: 写删除测试
       pass
   ```

2. 运行测试：
   cd day15_wrapup
   pytest test_app.py -v

3. 手动验证完整流程（浏览器）：
   a) 访问 http://localhost:5000 → 看到 Bootstrap 美化后的首页
   b) 用 admin/admin123 登录 → 看到 flash 欢迎消息
   c) 查看学生列表（5 条）
   d) 搜索"计算机" → 看到 2 条结果（张三 + 陈七）
   e) 添加一个学生 → flash 成功 → 重定向到列表
   f) 编辑刚添加的学生 → 修改后保存
   g) 删除该学生 → 确认对话框 → 删除成功
   h) 退出登录 → flash 退出消息

提示：
  - 用 :memory: 作为数据库路径会创建临时内存数据库，测试结束自动销毁
  - search_students 测试要验证返回数量、学生姓名
  - 如果测试失败，检查是否 import 路径正确
  - 如果 get_student 返回 None，检查数据库是否已提交（sqlite3 自动提交没问题）
  - 参考 Day 11 test_app.py 的写法

预计时间：20 分钟
"""
