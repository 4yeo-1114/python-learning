"""
============================================================
Day 14 练习：Web CRUD 完成
============================================================
在开始前，请先阅读 day14_notes.py 理解今天的知识点，
然后完成下面的练习（3 道题，每题约 15-20 分钟）。

今天的主题：**打通 Web 端完整 CRUD 链路**
你会用到 RESTful 路由、flash 消息、PRG 模式

运行方式：
  在终端执行：python day14_exercise.py
  然后浏览器打开：http://localhost:5000

测试账号: admin / admin123
"""



from flask import(
    Flask,render_template,request,redirect,url_for,
    session,flash
)
from functools import wraps
import sqlite3
import hashlib
import os

app = Flask(__name__)
app.secret_key = "day14-secret-key-for-flash-and-session"


# ============================================================
# 数据库类（Day 9/10/13 的内容，已经写好）
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
    """
    学生数据库
    Day 14 新增：get_student, update_student, delete_student, search_students
    """

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

    # ── Day 14 新增方法（下面 4 个 TODO） ──

    # TODO 1-a: get_student — 根据 id 获取单个学生
    def get_student(self, student_id):
        """根据 id 获取单个学生，返回 dict 或 None"""
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
            return False, f"更新失败：{e}"

    # TODO 1-c: delete_student — 删除学生
    def delete_student(self, student_id):
        """根据 id 删除学生，返回 (bool, msg)"""
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

    # TODO 1-d: search_students — 按关键字搜索
    def search_students(self, keyword):
        """按姓名或专业模糊搜索，返回 list[dict]"""
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
# 登录保护装饰器（Day 13 的内容，直接用）
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
# 基础路由（Day 13 的内容，已经写好）
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
    """
    学生列表支持搜索功能
    有?q=xx 时搜素 没有时显示全部
    """
    keyword = request.args.get("q","").strip()
    
    if keyword:
        students  = student_db.search_students(keyword)
    else:
        students =  student_db.get_all_students()
    
    return render_template(
        "student_list.html",
        students = students,
        username = session.get("username"),
        keyword= keyword
    )
    

# ============================================================
# 练习 1：添加学生页面 + 表单验证 + flash 消息
# ============================================================
"""
题目：实现 /students/add 路由，能够通过 Web 表单添加学生

你的任务：
1. 完成 StudentDB 中的 4 个新方法（先翻到上面 StudentDB 类的 TODO 部分）：
   a) get_student(student_id) → dict|None
      - 用 "SELECT ... WHERE id = ?" 查询
      - 找到返回 dict，找不到返回 None
      - 提示：conn.row_factory = sqlite3.Row; row = conn.execute(...).fetchone()
             如果 row 不是 None，返回 dict(row)

   b) update_student(student_id, name, age, grade, major) → (bool, msg)
      - 用 "UPDATE students SET name=?, age=?, grade=?, major=? WHERE id=?"
      - 返回 (True, "更新成功") 或 (False, str(e))
      - 提示：conn.execute(...) 后用 cursor.rowcount 判断影响行数

   c) delete_student(student_id) → (bool, msg)
      - 用 "DELETE FROM students WHERE id = ?"
      - 返回 (True, "删除成功") 或 (False, str(e))

   d) search_students(keyword) → list[dict]
      - 用 LIKE 模糊匹配姓名和专业
      - SQL: "SELECT ... WHERE name LIKE ? OR major LIKE ? ORDER BY id"
      - 提示：LIKE 需要 % 通配符，写 f"%{keyword}%"

2. 完成 "/students/add" 路由：
   GET 请求：
   - 渲染 add_student.html 模板（空白表单）
   POST 请求（遵循 PRG 模式！）：
   a) 从 request.form 获取 name, age, grade, major
   b) 表单验证（参考 register 的思路）：
      - 姓名不能为空
      - 年龄必须是正整数（提示：age.isdigit()）
      - 年龄在 1-150 之间
      - 如果验证失败，flash 错误消息，重新渲染 add_student.html
        并把用户已输入的值回传给模板（避免重填）
        即：render_template("add_student.html",
                           name=name, age=age, grade=grade, major=major)
   c) 调用 student_db.add_student(name, int(age), grade, major)
   d) 用 flash("学生添加成功！", "success") 发送成功消息
   e) redirect 到 student_list（遵循 PRG 模式！）

3. 完成 add_student.html 模板：
   - 继承 layout.html
   - 表单字段：name(文本), age(数字), grade(文本), major(文本)
   - 每个字段用 <input> 标签，name 属性对应 Python 中的 request.form.get("xxx")
   - 用 value="{{ name }}" 回填用户已输入的值（这样验证失败时不用重新填）
   - 提示：value 设为空字符串默认值，避免 None 报错 --> value="{{ name or '' }}"

要求：
- POST 后必须 redirect（PRG 模式）
- 表单验证未通过时 flash 错误 + 回填数据
- 添加成功后 flash 成功消息 → 重定向到学生列表
- 在 add_student.html 中显示 flash 消息

提示：
  - from flask import flash（已经在顶部导入）
  - 模板中获取 flash: get_flashed_messages(with_categories=true)
  - age 要用 int() 转换：student_db.add_student(name, int(age), grade, major)
  - 参考 register 路由的表单验证模式

预计时间：20 分钟
"""

# --- 添加学生路由 ---
@app.route("/students/add", methods=["GET", "POST"])
@login_required
def add_student():
    # TODO: GET 显示表单，POST 验证并添加（遵循 PRG 模式）
    if request.method  =="POST":
        name = request.form.get("name","").strip()
        age_str = request.form.get("age","").strip()
        grade = request.form.get("grade","").strip()
        major  = request.form.get("major","").strip()

        
        if not name:
            flash("姓名不能为空","error")
            return render_template("add_student.html",name = name,
                                   age = age_str,grade =grade,major =major)
            
        if not age_str.isdigit():
            flash("年龄必须是正整数","error")
            return render_template("add_student.html",name = name,
                                               age = age_str,grade =grade,major =major)
        
        age = int(age_str)
        if age < 1 or age > 150:
            flash("年龄必须在 1-150 之间", "error")
            return render_template("add_student.html",
                                   name=name, age=age_str,
                                   grade=grade, major=major)       
        #数据库操作
        ok,result = student_db.add_student(name,age,grade,major)
        if ok:
            flash(f"学生「{name}」添加成功！","success")
            #PRG 重定向到标签页
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
# 练习 2：编辑/删除学生（带确认）
# ============================================================
"""
题目：实现编辑和删除学生功能

你的任务：
1. 完成 "/students/<int:student_id>/edit" 路由（GET 和 POST）：
   GET 请求：
   a) 用 student_db.get_student(student_id) 获取学生
   b) 如果不存在（None），flash 错误 → redirect 回列表
   c) 如果存在，渲染 edit_student.html，把学生数据传过去做默认值
      render_template("edit_student.html", student=student)
   POST 请求（遵循 PRG）：
   a) 获取表单数据：name, age, grade, major
   b) 表单验证（同添加的规则）
   c) 调用 student_db.update_student(...)
   d) flash 成功消息 → redirect 到 student_list
   e) 更新失败 → flash 错误 → 重新渲染 edit_student.html

2. 完成 "/students/<int:student_id>/delete" 路由（只用 POST）：
   a) 调用 student_db.delete_student(student_id)
   b) flash 成功/失败消息
   c) redirect 到 student_list
   注意：删除只用 POST，不要用 GET（防止搜索引擎爬虫误删）

3. 在 student_list.html 表格中加"操作"列：
   - 编辑按钮：<a href="/students/{{ s.id }}/edit" class="btn">✏️ 编辑</a>
   - 删除按钮：用表单包裹提交按钮
     <form method="post" action="/students/{{ s.id }}/delete"
           onsubmit="return confirm('确定要删除 {{ s.name }} 吗？')">
       <button type="submit" class="btn">🗑️ 删除</button>
     </form>
   提示：onsubmit 中的 confirm() 可以增加 JavaScript 确认对话框

4. 完成 edit_student.html 模板：
   - 继承 layout.html
   - 表单字段和 add_student.html 类似
   - 区别：
     a) 所有字段用 value="{{ student.xxx }}" 预填当前值
     b) 标题写"编辑学生"
     c) action 指向正确的编辑 URL

要求：
- 编辑和删除路由都必须用 @login_required 保护
- 删除前有 JavaScript confirm 确认
- 所有写操作遵循 PRG 模式
- 表单验证规则和添加学生一致

提示：
  - <int:student_id> 转换器自动把 URL 中的数字变成 int
  - 删除路由地址：/students/3/delete（用 student_id 参数）
  - confirm() 返回 true 提交表单 / false 取消

预计时间：20 分钟
"""

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
# 练习 3：搜索功能 + 完整导航菜单
# ============================================================
"""
题目：实现学生搜索功能，完善导航菜单

你的任务：
1. 升级 "/students" 路由支持搜索：
   - 从 request.args 获取查询参数 q（即 URL 中的 ?q=xxx）
   - request.args 是查询参数字典，类似 request.form 但用于 GET 请求
   - 提示：keyword = request.args.get("q", "").strip()
   - 如果 keyword 不为空：调用 student_db.search_students(keyword)
   - 如果 keyword 为空：调用 student_db.get_all_students()
   - 把 keyword 也传给模板，用于回填搜索框

2. 在 student_list.html 顶部添加搜索表单：
   <form method="get" action="/students" class="search-form">
       <input type="text" name="q" value="{{ keyword }}" placeholder="搜索姓名或专业...">
       <button type="submit" class="btn">🔍 搜索</button>
       {% if keyword %}
       <a href="/students" class="btn">清除搜索</a>
       {% endif %}
   </form>
   提示：搜索表单用 GET 方法（因为搜索是"查看"操作）

3. 在 student_list.html 中添加"添加学生"按钮：
   <a href="/students/add" class="btn">➕ 添加学生</a>

4. 完善导航菜单（layout.html）：
   - 确保已登录状态下导航栏有：首页 / 学生列表 / 添加学生
   - 确保搜索结果为空时显示"没有找到匹配的学生"
   - 搜索时显示"搜索 'xxx' 的结果"

要求：
- 搜索支持按姓名和专业模糊匹配
- 搜索框为空时显示全部学生
- 搜索结果页面保留搜索关键字
- 搜索、查看、添加三个功能的导航链接完整

提示：
  - request.args 用于 GET 请求的查询参数（?key=value）
  - request.form 用于 POST 请求的表单数据
  - 搜索表单用 method="get"，数据会附加在 URL 后面
  - Jinja2 中用 {{ keyword or '' }} 处理 None 值

预计时间：15-20 分钟
"""

# --- 升级版学生列表路由（支持搜索） ---
# 注意：这个路由覆盖了上面第 258 行的简单版 /students 路由
# 你只需要修改上面那个 /students 路由即可，不需要新增路由
# 上面第 258 行 @app.route("/students") 下面的 student_list 函数
# 就是你修改的目标！


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
    print("Day 14 Web CRUD 练习服务器启动中...")
    print("=" * 60)
    init_test_data()
    print()
    print("可用路由（RESTful）：")
    print("  GET  /                      首页")
    print("  GET  /students              学生列表 + 搜索")
    print("  GET  /students/add          添加学生表单")
    print("  POST /students/add          提交添加")
    print("  GET  /students/<id>/edit    编辑学生表单")
    print("  POST /students/<id>/edit    提交编辑")
    print("  POST /students/<id>/delete  删除学生")
    print("  GET  /login /logout /register")
    print()
    print("测试账号: admin / admin123")
    print("按 Ctrl+C 停止服务器")
    print("=" * 60)
    app.run(debug=True)
