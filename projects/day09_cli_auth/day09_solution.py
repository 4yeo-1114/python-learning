"""
============================================================
Day 9 解答：CLI 菜单 + 用户认证
============================================================
"""

# ============================================================
# 练习 1：构建命令行菜单系统
# ============================================================

def calculator_menu():
    """简易计算器 - 字典映射版"""

    def add():
        a = float(input("第一个数: "))
        b = float(input("第二个数: "))
        print(f"  {a} + {b} = {a + b}")

    def subtract():
        a = float(input("第一个数: "))
        b = float(input("第二个数: "))
        print(f"  {a} - {b} = {a - b}")

    def multiply():
        a = float(input("第一个数: "))
        b = float(input("第二个数: "))
        print(f"  {a} × {b} = {a * b}")

    def divide():
        a = float(input("被除数: "))
        b = float(input("除数: "))
        if b == 0:
            print("  错误：除数不能为 0！")
        else:
            print(f"  {a} ÷ {b} = {a / b}")

    def exit_prog():
        print("谢谢使用，再见！")
        return "exit"

    # 字典映射：选项 → 函数
    menu = {
        "1": add,
        "2": subtract,
        "3": multiply,
        "4": divide,
        "5": exit_prog,
    }

    while True:
        print("\n┌─────────────────────┐")
        print("│  简易计算器          │")
        print("│  1. 加法             │")
        print("│  2. 减法             │")
        print("│  3. 乘法             │")
        print("│  4. 除法             │")
        print("│  5. 退出             │")
        print("└─────────────────────┘")

        choice = input("请选择 (1-5): ").strip()

        if choice in menu:
            try:
                result = menu[choice]()
                if result == "exit":
                    break
            except ValueError:
                print("输入错误：请输入有效的数字！")
        else:
            print(f"无效选项: {choice}，请输入 1-5")


# 测试（取消注释运行）
# calculator_menu()


# ============================================================
# 练习 2：密码验证器
# ============================================================

def validate_password(password: str) -> tuple:
    """
    验证密码强度
    返回: (是否通过, 错误信息)
    """
    # 规则 a: 长度至少 6 位
    if len(password) < 6:
        return False, "密码至少需要 6 位"

    # 规则 b: 不能全是数字
    if password.isdigit():
        return False, "密码不能全是数字"

    # 规则 c: 不能全是字母
    if password.isalpha():
        return False, "密码不能全是字母"

    return True, "密码有效"


def register_flow():
    """注册流程：用户名 → 密码 → 确认密码"""
    print("\n=== 用户注册 ===")

    # 输入用户名
    while True:
        username = input("用户名: ").strip()
        if username:
            break
        print("用户名不能为空！")

    # 输入密码（带验证）
    while True:
        password = input("密码: ").strip()
        ok, msg = validate_password(password)
        if ok:
            break
        print(f"密码不合格：{msg}")

    # 确认密码
    while True:
        confirm = input("确认密码: ").strip()
        if confirm == password:
            break
        print("两次密码不一致，请重新输入确认密码")

    print(f"\n注册成功！用户名: {username}")
    return username, password


# 测试（取消注释运行）
# register_flow()


# ============================================================
# 练习 3：用户数据库操作类
# ============================================================

import sqlite3
import hashlib
import os


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

    # ---------- 密码哈希 ----------
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

    # ---------- 注册 ----------
    def register(self, username: str, password: str, role="student") -> tuple:
        """
        注册新用户
        返回: (True, "注册成功") 或 (False, "用户名已存在")
        """
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

    # ---------- 登录 ----------
    def login(self, username: str, password: str) -> tuple:
        """
        验证登录
        返回: (True, user_dict) 或 (False, "错误信息")
        """
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

    # ---------- 辅助：获取所有用户 ----------
    def get_all_users(self):
        """获取所有用户列表（管理员功能）"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT id, username, role FROM users ORDER BY id"
            ).fetchall()
            return [dict(r) for r in rows]

    # ---------- 辅助：统计用户数 ----------
    def count_users(self) -> int:
        """返回用户总数"""
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute("SELECT COUNT(*) FROM users").fetchone()
            return row[0]


# ---------- 测试代码 ----------
def test_user_db():
    """测试 UserDB 的各项功能"""
    print("=== 测试 UserDB ===")

    # 用临时数据库，避免污染正式数据
    db = UserDB("test_calc.db")

    # 测试 1：注册
    ok, msg = db.register("admin", "admin123", role="admin")
    print(f"注册 admin: {msg}")  # 注册成功

    ok, msg = db.register("zhangsan", "hello123")
    print(f"注册 zhangsan: {msg}")  # 注册成功

    # 测试 2：重复注册
    ok, msg = db.register("admin", "another")
    print(f"重复注册 admin: {msg}")  # 用户名已存在

    # 测试 3：正确密码登录
    ok, result = db.login("admin", "admin123")
    if ok:
        print(f"登录 admin 成功: {result['username']}（{result['role']}）")
    else:
        print(f"登录 admin 失败: {result}")

    # 测试 4：错误密码登录
    ok, result = db.login("admin", "wrongpass")
    print(f"错误密码登录: {result}")  # 密码错误

    # 测试 5：不存在用户
    ok, result = db.login("nobody", "pass")
    print(f"不存在用户登录: {result}")  # 用户名不存在

    # 测试 6：获取所有用户
    users = db.get_all_users()
    print(f"\n所有用户 ({len(users)} 人):")
    for u in users:
        print(f"  {u['id']}. {u['username']} ({u['role']})")

    # 清理测试数据库
    os.remove("test_calc.db")
    print("\n测试完成，临时数据库已清理")


# test_user_db()


# ============================================================
# [附录] Session 类 — 供后续项目使用
# ============================================================

class Session:
    """简单的会话管理（Day10 整合时会用到）"""
    current_user = None

    @classmethod
    def login(cls, user: dict):
        cls.current_user = user

    @classmethod
    def logout(cls):
        cls.current_user = None

    @classmethod
    def is_logged_in(cls) -> bool:
        return cls.current_user is not None

    @classmethod
    def is_admin(cls) -> bool:
        return cls.current_user and cls.current_user.get("role") == "admin"

    @classmethod
    def get_username(cls) -> str:
        return cls.current_user["username"] if cls.current_user else "未登录"


# ========== 程序入口 ==========
if __name__ == "__main__":
    print("运行 test_user_db() 测试练习 3...")
    test_user_db()
