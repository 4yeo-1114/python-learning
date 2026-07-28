"""
============================================================
Day 11 练习：单元测试入门（pytest）
============================================================
在开始前，请先阅读 day11_notes.py 理解今天的知识点，
然后完成下面的练习（3 道题，每题约 15-20 分钟）。

今天的主题：**从"写代码"到"验证代码"的思维转换**
你会用到 assert 断言、fixture 夹具、@parametrize 参数化测试
"""

import pytest
import sqlite3
import hashlib
import os

# ============================================================
# 练习 1：为 validate_password 写单元测试（纯函数测试）
# ============================================================
"""
题目：为 Day 9 的 validate_password 函数编写完整的单元测试

你的任务：
1. 先把 validate_password 函数复制过来（从 day09_solution.py）
2. 写一个测试类 TestValidatePassword，包含以下测试方法：

   a) test_password_too_short — 测试密码太短（< 6 位）
      输入: "abc"、"a1"、""（空字符串）
      期望: 都返回 (False, "密码至少需要 6 位")

   b) test_password_all_digits — 测试全数字密码
      输入: "123456"、"00000000"
      期望: 都返回 (False, "密码不能全是数字")

   c) test_password_all_letters — 测试全字母密码
      输入: "abcdef"、"HelloWorld"
      期望: 都返回 (False, "密码不能全是字母")

   d) test_valid_password — 测试有效密码
      输入: "abc123"、"hello123"、"Passw0rd"
      期望: 都返回 (True, "密码有效")

   e) test_edge_cases — 边界测试
      输入: "a1b2c3"（刚好 6 位）、"中文测试12"（包含中文）
      期望: "a1b2c3" → (True, "密码有效")

要求：
- 每个测试方法至少用 2 个不同的输入
- 解包 tuple 后分别 assert ok 和 msg
- 使用 python -m pytest 或 pytest 运行测试

提示：
  - 纯函数测试最简单：给输入 → 断言输出
  - assert ok is False 比 assert not ok 更明确
  - 第一个参数 verbose_name 在 parametrize 中是可选的

预计时间：15 分钟
"""

# TODO: 把 validate_password 函数复制到此处
def validate_password(password: str) -> tuple:
    """
    验证密码强度
    返回: (是否通过, 错误信息)
    """
    if len(password) < 6:
        return False, "密码至少需要 6 位"
    if password.isdigit():
        return False, "密码不能全是数字"
    if password.isalpha():
        return False, "密码不能全是字母"
    return True, "密码有效"



# TODO: 写测试函数/测试类，每个测试至少 2 个用例
class TestValidatePassword:
      def test_password_too_short(self):
         """密码长度小于六位应拒绝"""
         ok1,msg1 = validate_password("abc")
         ok2,msg2  = validate_password("a1")
         ok3,msg3 = validate_password("")
         
         assert ok1 is False
         assert msg1 == "密码至少需要六位"
         assert ok2 is False
         assert msg2 == "密码至少需要 6 位"
         assert ok3 is False
         assert msg3 == "密码至少需要 6 位"
      
      def test_password_all_digits(self):
         ok1,msg1 = validate_password("123456")
         ok2,msg2 = validate_password("00000000")
         
         assert ok1 is False
         assert msg1 == "密码不能全是数字"
         
         assert ok2 is False
         assert msg2 == "密码不能全是数字"
       
      def test_password_all_letters(self):
         """全字母密码应拒绝"""
         ok1, msg1 = validate_password("abcdef")
         ok2, msg2 = validate_password("HelloWorld")
      
         assert ok1 is False
         assert msg1 == "密码不能全是字母"
      
         assert ok2 is False
         assert msg2 == "密码不能全是字母"    
         
      def test_valid_password(self):
        """混合数字和字母的密码应通过"""
        ok1, msg1 = validate_password("abc123")
        ok2, msg2 = validate_password("hello123")
        ok3, msg3 = validate_password("Passw0rd")

        assert ok1 is True
        assert msg1 == "密码有效"

        assert ok2 is True
        assert msg2 == "密码有效"

        assert ok3 is True
        assert msg3 == "密码有效"

      def test_edge_case(self):
         ok,msg = validate_password("a1b2c3")
         assert ok is True
         assert msg == "密码有效"


# ============================================================
# 练习 2：为 UserDB 写测试（fixture 管理测试数据库）
# ============================================================
"""
题目：用 fixture 管理临时数据库，为 UserDB 写测试

你的任务：
1. 把 UserDB 类复制过来（从 day09_solution.py，只需要类定义）
2. 写一个 fixture 函数 user_db()：
   - 用 :memory: 数据库创建 UserDB 实例
   - yield 这个实例给测试函数使用
   - （:memory: 不需要清理，测试结束自动消失）

3. 写以下测试函数（每个接收 user_db 作为参数）：

   a) test_register_success(user_db)
      - 注册一个新用户 "admin" / "admin123"
      - 断言返回 (True, "注册成功")
      - 断言 user_db.count_users() == 1

   b) test_register_duplicate(user_db)
      - 先注册 "admin" / "admin123"
      - 再注册同一个用户名 "admin" / "another"
      - 断言第二次返回 (False, "用户名已存在")
      - 断言 user_db.count_users() == 1（没多出来）

   c) test_login_success(user_db)
      - 先注册一个用户
      - 用正确密码登录
      - 断言返回 (True, user_dict)
      - 断言 user_dict 包含 "id"、"username"、"role" 三个 key
      - 断言 user_dict["role"] == "student"（默认角色）

   d) test_login_wrong_password(user_db)
      - 先注册一个用户
      - 用错误密码登录
      - 断言返回 (False, "密码错误")

   e) test_login_nonexistent_user(user_db)
      - 不注册任何用户，直接登录
      - 断言返回 (False, "用户名不存在")

要求：
- fixture 必须用 yield
- 每个测试函数利用 fixture 注入的 user_db
- 测试之间互相独立（一个的注册不影响另一个的登录测试）



预计时间：20 分钟
"""

# TODO: 把 UserDB 类复制到此处（含所有必要的 import）
class UserDB:
    """用户数据库操作类 — 封装注册/登录的数据库操作"""

    def __init__(self, db_path="calculator.db"):
        self.db_path = db_path
        self._init_table()

    def _init_table(self):
        """初始化用户表"""
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
    def _hash_password(password: str) -> tuple:
        """返回 (salt, hashed_password)"""
        salt = os.urandom(16).hex()
        hashed = hashlib.sha256((password + salt).encode()).hexdigest()
        return salt, hashed

    @staticmethod
    def _verify_password(password: str, salt: str, stored_hash: str) -> bool:
        """验证密码"""
        return hashlib.sha256((password + salt).encode()).hexdigest() == stored_hash

    def register(self, username: str, password: str, role="student") -> tuple:
        """注册新用户，返回 (True, "注册成功") 或 (False, "用户名已存在")"""
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

    def login(self, username: str, password: str) -> tuple:
        """验证登录，返回 (True, user_dict) 或 (False, "错误信息")"""
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

    def count_users(self) -> int:
        """返回用户总数"""
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute("SELECT COUNT(*) FROM users").fetchone()
            return row[0]



# TODO: 写 user_db fixture
#fixture
def user_db(tmp_path):
   """
    创建用临时文件的 UserDB 实例，测试完自动删除。
    注意：不能用 :memory:，因为 UserDB 的每个方法都重新 connect,
    每次 connect(":memory:") 会创建不同的内存数据库。

    tmp_path 是 pytest 内置 fixture,每个测试函数有独立的临时目录,
    测试结束后 pytest 自动清理，不会有 Windows 文件锁问题。
    """
   db_path =str(tmp_path/"test_users.db")
   db = UserDB(db_path)
   return db

class TestUserDB:
   """为UserDB编写的单元测试(使用fixture)"""
   
   def test_register_success(self,user_db):
      """注册新用户应成功"""
      ok,msg = user_db.register("admin","admin123")
      
      # Assert
      assert ok is True
      assert msg == "注册成功"
      assert user_db.count_users() == 1
      
   def test_register_duplicate(self,user_db):
      """重复注册同一用户名应失败"""
      #Arrange
      user_db.register("admin", "admin123")
      #Act
      ok, msg = user_db.register("admin", "another456")
      
      #Assert
      assert ok is False
      assert msg == "用户名已存在"
      assert user_db.count_users() == 1
   
   def test_login_success(self,user_db):
        # Arrange
        user_db.register("student1", "hello123")

        # Act
        ok, result = user_db.login("student1", "hello123")

        # Assert
        assert ok is True
        assert isinstance(result, dict)
        assert "id" in result
        assert "username" in result
        assert "role" in result
        assert result["username"] == "student1"
        assert result["role"] == "student"
     
   def test_login_wrong_password(self,user_db):
      """错误密码登录应失败"""
      # Arrange
      user_db.register("student1", "hello123")

      # Act
      ok, msg = user_db.login("student1", "wrongpass")

      # Assert
      assert ok is False
      assert msg == "密码错误"
   
   def test_login_nonexistent_user(self, user_db):
        """登录不存在的用户应失败"""
        # Act（不需要 Arrange，因为没有注册）
        ok, msg = user_db.login("nobody", "somepass")

        # Assert
        assert ok is False
        assert msg == "用户名不存在"






# TODO: 写 5 个测试函数


# ============================================================
# 练习 3：为 StudentDB 写参数化测试（@parametrize）
# ============================================================
"""
题目：用 @pytest.mark.parametrize 为 StudentDB 写参数化测试

你的任务：
1. 把 StudentDB 类复制过来（从 day10_solution.py，只需要类定义）
2. 写一个 fixture 函数 student_db()：


3. 写参数化测试：

   a) 用 @parametrize 测试 add_student 的正常添加：
      @pytest.mark.parametrize("name,age,grade,major", [
          ("张三", 20, "2024级1班", "计算机科学"),
          ("李四", 19, "2024级2班", "软件工程"),
          ("王五", 22, "", ""),                       # 班级专业可空
      ])
      def test_add_student(student_db, name, age, grade, major):
          ok, new_id = student_db.add_student(name, age, grade, major)
          assert ok is True
          assert new_id is not None
          # 再验证能否查回来
          student = student_db.get_student_by_id(new_id)
          assert student["name"] == name
          assert student["age"] == age

   b) 用 @parametrize 测试 search_students：
      @pytest.mark.parametrize("keyword,expected_count", [
          ("张", 2),     # 张三 + 张三丰
          ("计算机", 1),  # 只有计算机科学
          ("软件", 1),   # 只有软件工程
          ("不存在", 0), # 没有匹配
      ])
      def test_search_students(student_db, keyword, expected_count):
          # 准备数据（Arrange）：先添加几个学生
          student_db.add_student("张三", 20, "2024级1班", "计算机科学")
          student_db.add_student("张三丰", 22, "2023级1班", "人工智能")
          student_db.add_student("李四", 19, "2024级2班", "软件工程")

          # 执行（Act）
          results = student_db.search_students(keyword)

          # 验证（Assert）
          assert len(results) == expected_count

   c) 用 @parametrize 测试 delete_student：
      @pytest.mark.parametrize("delete_id,expected_ok,expected_msg", [
          (1, True, "删除成功"),
          (999, False, "学生不存在"),
      ])
      def test_delete_student(student_db, delete_id, expected_ok, expected_msg):
          # 准备：先加一个学生
          student_db.add_student("测试", 18, "2024级", "测试专业")
          ok, msg = student_db.delete_student(delete_id)
          assert ok == expected_ok
          assert msg == expected_msg

要求：
- 3 个测试都用 @parametrize 装饰器
- 每个测试的 parametrize 至少 3 组数据
- 测试数据准备（Arrange）写在测试函数内部

提示：
  - parametrize 第一个参数是参数字符串（逗号分隔）
  - 第二个参数是数据列表（每个元素是一个 tuple）
  - 如果 StudentDB 不支持 :memory:，手动修改使其支持

预计时间：20 分钟
"""

# TODO: 把 StudentDB 类复制到此处（从 day10_solution.py）
class StudentDB:
    """学生数据库操作类"""

    def __init__(self, db_path: str = "students.db"):
        self.db_path = db_path
        self._init_table()

    def _init_table(self):
        """初始化学生表"""
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

    def add_student(self, name: str, age: int, grade: str = "", major: str = ""):
        """添加学生，返回 (True, new_id) 或 (False, "错误信息")"""
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

    def get_all_students(self) -> list[dict]:
        """返回所有学生，按 id 升序"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT id, name, age, grade, major, created_at "
                "FROM students ORDER BY id"
            ).fetchall()
            return [dict(r) for r in rows]

    def search_students(self, keyword: str) -> list[dict]:
        """按姓名或专业模糊搜索"""
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

    def get_student_by_id(self, student_id: int) -> dict | None:
        """按 id 查找学生，未找到返回 None"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(
                "SELECT id, name, age, grade, major, created_at "
                "FROM students WHERE id = ?",
                (student_id,)
            ).fetchone()
            return dict(row) if row else None

    def update_student(self, student_id: int, **kwargs):
        """更新学生信息，只更新传入的字段"""
        if not kwargs:
            return False, "没有需要更新的字段"

        fields = ", ".join(f"{k} = ?" for k in kwargs.keys())
        values = list(kwargs.values())
        values.append(student_id)

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    f"UPDATE students SET {fields} WHERE id = ?",
                    values
                )
                if cursor.rowcount == 0:
                    return False, "学生不存在"
                return True, "更新成功"
        except sqlite3.Error as e:
            return False, f"更新失败: {e}"

    def delete_student(self, student_id: int):
        """删除学生，返回 (True, "删除成功") 或 (False, "学生不存在")"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "DELETE FROM students WHERE id = ?",
                (student_id,)
            )
            if cursor.rowcount == 0:
                return False, "学生不存在"
            return True, "删除成功"

    def count_students(self) -> int:
        """返回学生总数"""
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute("SELECT COUNT(*) FROM students").fetchone()
            return row[0]


# ---- fixture ----
@pytest.fixture
def student_db(tmp_path):
    """创建用临时文件的 StudentDB 实例，测试完自动删除"""
    db_path = str(tmp_path / "test_students.db")
    db = StudentDB(db_path)
    return db


    @pytest.mark.parametrize("keyword,expected_count", [
        ("张", 2),       # 张三 + 张三丰
        ("计算机", 1),    # 计算机科学
        ("软件", 1),     # 软件工程
        ("不存在", 0),   # 没有匹配
        ("李", 1),       # 李四
    ])
    def test_search_students(self, student_db, keyword, expected_count):
        """搜索学生：验证模糊搜索返回正确数量"""
        # Arrange
        student_db.add_student("张三", 20, "2024级1班", "计算机科学")
        student_db.add_student("张三丰", 22, "2023级1班", "人工智能")
        student_db.add_student("李四", 19, "2024级2班", "软件工程")

        # Act
        results = student_db.search_students(keyword)

        # Assert
        assert len(results) == expected_count, \
            f"搜索 '{keyword}' 期望 {expected_count} 条，实际 {len(results)} 条"

    # 3c: 参数化测试 delete_student
    @pytest.mark.parametrize("delete_id,expected_ok,expected_msg", [
        (1, True, "删除成功"),
        (999, False, "学生不存在"),
    ])
    def test_delete_student(self, student_db, delete_id, expected_ok, expected_msg):
        """删除学生：测试正常删除和删除不存在的记录"""
        # Arrange
        student_db.add_student("测试学生", 18, "2024级", "测试专业")

        # Act
        ok, msg = student_db.delete_student(delete_id)

        # Assert
        assert ok == expected_ok, f"删除 id={delete_id} 期望 ok={expected_ok}"
        assert msg == expected_msg

    # 额外：测试 update_student 的参数化
    @pytest.mark.parametrize("update_kwargs,expected_name,expected_age", [
        ({"name": "新名字"}, "新名字", 20),           # 只改名字
        ({"age": 25}, "张三", 25),                   # 只改年龄
        ({"name": "改名", "age": 30}, "改名", 30),    # 同时改两个
    ])
    def test_update_student(self, student_db, update_kwargs,
                            expected_name, expected_age):
        """更新学生：验证部分字段更新"""
        # Arrange
        student_db.add_student("张三", 20, "2024级1班", "计算机科学")

        # Act
        ok, msg = student_db.update_student(1, **update_kwargs)

        # Assert
        assert ok is True
        assert msg == "更新成功"

        updated = student_db.get_student_by_id(1)
        assert updated["name"] == expected_name
        assert updated["age"] == expected_age


# TODO: 写 3 个参数化测试函数
class TestStudentDB:
   @pytest.mark.parametrize("name,age,grade,major",
      [("张三",20,"2024级1班", "计算机科学"),
       ("李四", 19, "2024级2班", "软件工程"),
        ("王五", 22, "", ""), 
         ("Alice", 25, "2023级", "人工智能"),
      ])
   def test_add_student(self,student_db,name,age,grade,major):
      """添加学生：验证插入成功且数据能查回"""
      #Act
      ok,new_id = student_db.add_student(name,age,grade,major)
      
      #Assert
      assert ok is True,f"添加{name}应成功"
      assert isinstance(new_id,int),f"new_id应为整数"
      assert new_id >= 1
      
      #验证能查回来
      student = student_db.get_student_by_id(new_id)
      assert student is not None
      assert student["name"] == name
      assert student["age"] == age
      assert student["grade"] == grade
      assert student["major"] == major     




if __name__ == "__main__":
    print("请用 pytest 运行本文件：")
    print("  python -m pytest day11_solution.py -v")
    print()
    print("或运行单个测试：")
    print("  python -m pytest day11_solution.py::TestValidatePassword -v")
    print("  python -m pytest day11_solution.py::TestUserDB -v")
    print("  python -m pytest day11_solution.py::TestStudentDB -v")
