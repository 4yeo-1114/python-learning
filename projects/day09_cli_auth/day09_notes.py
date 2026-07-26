"""
============================================================
Day 9: CLI 学生管理系统 — 项目架构与用户认证（C++ 对比版）
============================================================
目标：学会组织 Python 项目结构，构建命令行交互界面，
      实现用户注册/登录模块（密码哈希 + SQLite）
      Week 4 正式开始 — 把前面学的全部串起来！
"""

# ============================================================
# 第一部分：Python 项目结构 — 从脚本到工程
# ============================================================

print("=" * 60)
print("第一部分：Python 项目结构")
print("=" * 60)

# 1.1 从"单文件脚本"到"多模块工程"
# 之前我们所有的代码都写在一个 .py 文件里
# 当项目变复杂后（学生管理系统预计 500+ 行），需要拆分

"""
典型的 Python 项目结构：

student_system/           <-- 项目根目录（也是 Python 包）
├── __init__.py           <-- 标识这是一个包（可以为空）
├── main.py               <-- 入口文件（用户从这里启动）
├── auth.py               <-- 认证模块（注册/登录）
├── student_manager.py    <-- 学生管理模块（CRUD）
├── database.py           <-- 数据库操作（SQLite 封装）
└── utils.py              <-- 工具函数（输入验证、格式化等）

C++ 对比：
C++ 项目通常有 include/ src/ 分离，用 CMakeLists.txt 管理编译
Python 项目结构更扁平，import 机制让组织更灵活
"""

# 1.2 包（Package）vs 模块（Module）
"""
┌────────────┬──────────────────────────────────────┐
│ 概念        │ 说明                                  │
├────────────┼──────────────────────────────────────┤
│ 模块 module │ 一个 .py 文件就是一个模块               │
│ 包 package  │ 一个含 __init__.py 的目录就是包         │
│ 子模块      │ 包里面的 .py 文件                      │
└────────────┴──────────────────────────────────────┘

导入方式：
  import module              # 导入整个模块
  from package import module  # 从包里导入模块
  from module import func     # 从模块里导入函数
  from package.module import Class  # 从包的模块里导入类
"""

# 1.3 __init__.py 的作用
"""
__init__.py 有三个作用：
1. 标识目录是 Python 包（Python 3.3+ 可省略，但建议保留）
2. 包被导入时自动执行（初始化代码）
3. 控制 from package import * 的行为（__all__ 变量）

C++ 对比：
类似 C++ 的头文件，但 __init__.py 是运行时执行的，
不像 .h 文件那样声明接口。Python 的"接口"靠约定和文档。
"""

# 1.4 分离关注点（Separation of Concerns）
"""
好的项目会把不同职责分到不同模块：

┌──────────────────┬──────────────────────────────┐
│ 模块              │ 职责                          │
├──────────────────┼──────────────────────────────┤
│ database.py      │ 数据库连接、建表、基础 CRUD     │
│ auth.py          │ 注册逻辑、登录逻辑、密码处理     │
│ student_manager  │ 学生信息的增删改查业务逻辑       │
│ cli.py           │ 菜单显示、用户输入、结果展示     │
│ main.py          │ 程序入口，组装各模块             │
└──────────────────┴──────────────────────────────┘

为什么要分？
- 修改数据库不影响菜单显示
- 测试时可以单独测每个模块
- 多人协作时不会冲突
"""

print("\n[OK] 了解项目结构即可，实际搭建在后面练习中做")


# ============================================================
# 第二部分：CLI 菜单系统 — 命令行交互界面
# ============================================================

print("\n" + "=" * 60)
print("第二部分：CLI 菜单系统")
print("=" * 60)

# 2.1 最简单的菜单循环
print("\n=== 2.1 基础菜单循环 ===")

def simple_menu():
    """一个最简单的菜单示例"""
    while True:
        print("\n" + "-" * 30)
        print("  学生管理系统")
        print("-" * 30)
        print("1. 查看学生")
        print("2. 添加学生")
        print("3. 退出")
        print("-" * 30)

        choice = input("请选择 (1-3): ").strip()

        if choice == "1":
            print(">>> 执行：查看学生（功能未实现）")
        elif choice == "2":
            print(">>> 执行：添加学生（功能未实现）")
        elif choice == "3":
            print("再见！")
            break
        else:
            print("输入无效，请重新选择！")

# 运行试试（注释掉避免干扰笔记输出）
# simple_menu()


# 2.2 用字典映射代替 if-elif 链（更优雅）
print("\n=== 2.2 字典映射菜单 ===")

def menu_with_dict():
    """用字典替代长 if-elif 链"""
    def show_students():
        print(">>> 查看学生（功能未实现）")

    def add_student():
        print(">>> 添加学生（功能未实现）")

    def exit_system():
        print("再见！")
        return "exit"  # 返回特殊值表示退出

    # 字典映射：选项 → (描述, 函数)
    menu_options = {
        "1": ("查看学生", show_students),
        "2": ("添加学生", add_student),
        "3": ("退出", exit_system),
    }

    while True:
        print("\n" + "-" * 30)
        print("  学生管理系统")
        print("-" * 30)
        for key, (desc, _) in menu_options.items():
            print(f"{key}. {desc}")
        print("-" * 30)

        choice = input("请选择: ").strip()

        if choice in menu_options:
            result = menu_options[choice][1]()
            if result == "exit":
                break
        else:
            print(f"无效选项: {choice}，请重新输入")

# menu_with_dict()


# 2.3 输入验证辅助函数
print("\n=== 2.3 输入验证 ===")

def get_input(prompt, validator=None, error_msg="输入无效，请重试"):
    """
    获取用户输入并验证
    prompt: 提示文字
    validator: 验证函数，返回 True/False
    error_msg: 验证失败时的提示
    """
    while True:
        value = input(prompt).strip()
        if value == "":  # 不允许空输入
            print("输入不能为空！")
            continue
        if validator is None or validator(value):
            return value
        print(error_msg)

# 使用示例：
# name = get_input("请输入姓名: ")
# age = get_input("请输入年龄: ",
#                 validator=lambda x: x.isdigit() and 0 < int(x) < 150,
#                 error_msg="年龄必须是 1-149 之间的整数")

print("定义了 get_input() 辅助函数，后面练习会用到")


# 2.4 格式化输出 — 让 CLI 更好看
print("\n=== 2.4 格式化输出 ===")

def print_table(headers, rows, col_widths=None):
    """
    打印对齐的表格
    headers: 列名列表 ["姓名", "年龄", "成绩"]
    rows: 数据行列表 [["张三", "20", "85"], ...]
    col_widths: 列宽列表，None 时自动计算
    """
    if col_widths is None:
        # 自动计算列宽（取表头和数据中每列最大宽度）
        col_widths = []
        for i, h in enumerate(headers):
            max_w = len(str(h))
            for row in rows:
                if i < len(row):
                    max_w = max(max_w, len(str(row[i])))
            col_widths.append(max_w + 2)  # +2 留边距

    # 打印分隔线
    total_width = sum(col_widths) + len(col_widths) - 1
    print("+" + "-" * total_width + "+")

    # 打印表头
    header_parts = []
    for h, w in zip(headers, col_widths):
        header_parts.append(f"{h:^{w}}") #^居中对齐 字段宽度为w
    print("|" + "|".join(header_parts) + "|")

    # 打印表头分隔线
    print("+" + "-" * total_width + "+")

    # 打印数据行
    for row in rows:
        parts = []
        for i, w in enumerate(col_widths):
            val = str(row[i]) if i < len(row) else ""
            parts.append(f"{val:<{w}}")
        print("|" + "|".join(parts) + "|")

    # 打印底部分隔线
    print("+" + "-" * total_width + "+")

# 演示
demo_headers = ["姓名", "年龄", "成绩"]
demo_rows = [
    ["张三", 20, 85],
    ["李四", 22, 92],
    ["王五", 21, 78],
]
print_table(demo_headers, demo_rows)

print("\nC++ 对比：")
print("  C++ 要用 iomanip (setw, left, right) 手动控制格式")
print("  Python 用 f-string 的格式化说明符：{value:^10} 居中对齐宽度10")


# ============================================================
# 第三部分：用户认证 — 注册与登录
# ============================================================

print("\n" + "=" * 60)
print("第三部分：用户认证（注册/登录）")
print("=" * 60)

import sqlite3
import hashlib

# 3.1 密码安全基础 — 为什么不能存明文？
print("\n=== 3.1 密码安全 ===")

"""
问题：如果数据库被泄露，明文密码直接暴露
     很多人多个网站用同一个密码…

解决：存密码的"哈希值"而不是明文

哈希（Hash）的特点：
  1. 固定长度输出（SHA-256 永远是 64 个十六进制字符）
  2. 不可逆（从哈希值推不出原文）
  3. 雪崩效应（原文改一点点，哈希值完全不同）
  4. 确定性（同一输入永远得同一输出）

验证流程：
  注册时：密码 → SHA-256 → 存哈希值到数据库
  登录时：用户输入密码 → SHA-256 → 和数据库的哈希值比较
         相同 → 密码正确；不同 → 密码错误
"""

# 演示哈希
password = "hello123"
hashed = hashlib.sha256(password.encode()).hexdigest()
print(f"原文: {password}")
print(f"SHA-256: {hashed}")
print(f"哈希长度: {len(hashed)} 字符")

# 雪崩效应演示
password2 = "hello124"  # 只改了一个字符
hashed2 = hashlib.sha256(password2.encode()).hexdigest()
print(f"\n雪崩效应演示:")
print(f"  hello123 → {hashed[:20]}...")
print(f"  hello124 → {hashed2[:20]}...")
print(f"  完全不同！")


# 3.2 加盐（Salt）— 防止彩虹表攻击
print("\n=== 3.2 加盐（Salt）===")

"""
纯哈希的问题：相同的密码 → 相同的哈希值
  如果"张三"和"李四"都用 "123456" 做密码
  它们的哈希值一样 → 黑客一眼看出谁用弱密码

彩虹表攻击：黑客预先算好常见密码的哈希值
  "123456" → e150a1ec... → 查表就知道你用的是 "123456"

加盐解决：
  为每个用户生成一个随机"盐值"
  密码 + 盐值 → 一起哈希 → 存"盐值"和"哈希值"
  即使两个用户密码相同，因为盐值不同，哈希值也不同
"""

import os

#这就是个类型注释 给开发者看的函数需要什么类型 放回什么类型
def hash_password(password: str) -> tuple[str, str]:
    """
    安全的密码存储
    返回: (salt, hashed_password)
    """
    salt = os.urandom(16).hex()  # 16 字节随机盐
    # 密码 + 盐 → SHA-256
    hashed = hashlib.sha256((password + salt).encode()).hexdigest()
    return salt, hashed

def verify_password(password: str, salt: str, stored_hash: str) -> bool:
    """验证密码是否正确"""
    return hashlib.sha256((password + salt).encode()).hexdigest() == stored_hash

# 演示
salt, pw_hash = hash_password("mypassword")
print(f"盐值: {salt}")
print(f"哈希: {pw_hash}")
print(f"验证正确密码: {verify_password('mypassword', salt, pw_hash)}")
print(f"验证错误密码: {verify_password('wrongpass', salt, pw_hash)}")

print("\nC++ 对比：")
print("  C++ 可以用 OpenSSL 库做 SHA-256 哈希")
print("  Python hashlib 内置，一行搞定！")


# 3.3 用户数据库 — 建表 + 用户 DAO
print("\n=== 3.3 用户数据库 ===")

DB_PATH = "student_system.db"

def init_user_db(db_path=DB_PATH):
    """初始化用户表"""
    with sqlite3.connect(db_path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                role TEXT DEFAULT 'student',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
    print("用户表已就绪")

init_user_db()


# 3.4 用户注册
print("\n=== 3.4 用户注册 ===")

def register_user(username: str, password: str, role: str = "student",
                  db_path=DB_PATH) -> bool:
    """
    注册新用户
    返回 True 表示成功，False 表示用户名已存在
    """
    salt, pw_hash = hash_password(password)

    try:
        with sqlite3.connect(db_path) as conn:
            conn.execute(
                "INSERT INTO users (username, password_hash, salt, role) "
                "VALUES (?, ?, ?, ?)",
                (username, pw_hash, salt, role)
            )
        print(f"用户 '{username}' 注册成功！")
        return True
    except sqlite3.IntegrityError:
        # UNIQUE 约束冲突 → 用户名已存在
        print(f"用户名 '{username}' 已被占用，请换一个")
        return False

# 测试（首次运行会成功，第二次会提示已存在）
# register_user("admin", "admin123", role="admin")
# register_user("zhangsan", "pass123")


# 3.5 用户登录
print("\n=== 3.5 用户登录 ===")

def login_user(username: str, password: str, db_path=DB_PATH) -> dict | None:
    """
    验证用户登录
    返回用户信息 dict（不含密码）或 None
    """
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            "SELECT id, username, password_hash, salt, role FROM users "
            "WHERE username = ?",
            (username,)
        ).fetchone()

        if row is None:
            print("用户名不存在")
            return None

        if not verify_password(password, row["salt"], row["password_hash"]):
            print("密码错误")
            return None

        print(f"欢迎回来，{row['username']}（{row['role']}）！")
        return {
            "id": row["id"],
            "username": row["username"],
            "role": row["role"],
        }

# 测试
# login_user("admin", "admin123")   # 应该成功
# login_user("admin", "wrongpass")  # 应该失败


# 3.6 会话管理 — 记住"谁登录了"
print("\n=== 3.6 会话管理 ===")

"""
CLI 应用没有 HTTP Session/Cookie，我们用全局变量模拟：
"""

class Session:
    """简单的会话管理（CLI 版本用全局变量即可）"""
    current_user = None  # 类变量，全局共享

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
        return cls.current_user and cls.current_user["role"] == "admin"

    @classmethod
    def get_username(cls) -> str:
        return cls.current_user["username"] if cls.current_user else "未登录"


# 使用示例
# Session.login({"id": 1, "username": "admin", "role": "admin"})
# print(f"当前用户: {Session.get_username()}")
# print(f"是管理员: {Session.is_admin()}")


# ============================================================
# 第四部分：整合 — 一个完整的认证 CLI 程序
# ============================================================

print("\n" + "=" * 60)
print("第四部分：完整认证 CLI")
print("=" * 60)

# 把所有知识串起来！
# 注意：这是演示代码，实际运行时注释掉避免和练习冲突

def run_auth_cli():
    """完整的认证命令行程序"""
    init_user_db()

    # 确保有一个默认管理员账号
    register_user("admin", "admin123", role="admin")

    while True:
        # 未登录菜单
        if not Session.is_logged_in():
            print("\n" + "=" * 40)
            print("  学生管理系统 - 请先登录")
            print("=" * 40)
            print("1. 登录")
            print("2. 注册")
            print("3. 退出")
            print("-" * 40)

            choice = input("请选择: ").strip()

            if choice == "1":
                username = input("用户名: ").strip()
                password = input("密码: ").strip()
                user = login_user(username, password)
                if user:
                    Session.login(user)

            elif choice == "2":
                username = input("用户名: ").strip()
                password = input("密码: ").strip()
                confirm = input("确认密码: ").strip()
                if password != confirm:
                    print("两次密码不一致！")
                elif len(password) < 6:
                    print("密码至少 6 位！")
                else:
                    register_user(username, password)

            elif choice == "3":
                print("再见！")
                break
            else:
                print("无效选项")

        # 已登录菜单
        else:
            print(f"\n{'=' * 40}")
            print(f"  欢迎，{Session.get_username()}（{Session.current_user['role']}）")
            print(f"{'=' * 40}")
            print("1. 学生管理（TODO）")
            print("2. 修改密码（TODO）")
            if Session.is_admin():
                print("3. 用户管理（管理员专属）")
            print("0. 注销登录")
            print("-" * 40)

            choice = input("请选择: ").strip()

            if choice == "0":
                Session.logout()
                print("已注销")
            elif choice == "1":
                print("学生管理功能尚未实现，敬请期待 Day10！")
            elif choice == "2":
                print("修改密码功能尚未实现，敬请期待 Day10！")
            elif choice == "3" and Session.is_admin():
                print("用户管理功能尚未实现，敬请期待 Day10！")
            else:
                print("无效选项")

# run_auth_cli()  # 取消注释来体验完整流程


# ============================================================
# C++ → Python 速查表（Day 9 主题）
# ============================================================
"""
┌──────────────────────┬─────────────────────────────────────┬─────────────────────────────┐
│ 概念                  │ C++                                  │ Python                      │
├──────────────────────┼─────────────────────────────────────┼─────────────────────────────┤
│ 项目结构              │ CMake + include/src 分离               │ 包/模块 + import             │
│ 模块化                │ #include "header.h"                  │ import module               │
│ 控制台输入            │ std::cin >> var / std::getline        │ input(prompt)               │
│ 字符串格式化           │ std::format (C++20) / printf          │ f-string f"{var:^10}"       │
│ SHA-256 哈希          │ OpenSSL / Crypto++ 第三方库            │ hashlib.sha256() 内置        │
│ 随机数                │ <random> 引擎 + 分布                   │ os.urandom(n) / secrets      │
│ 空值                  │ nullptr / std::optional                │ None                        │
│ 静态成员              │ static 类成员                          │ 类变量（cls.xxx）             │
│ 循环菜单              │ while(true) + switch/case             │ while True + dict 映射       │
│ 异常处理              │ try/catch/throw                       │ try/except/raise            │
│ 字符串拼接            │ + 或 std::stringstream                 │ f-string（推荐）或 +          │
└──────────────────────┴─────────────────────────────────────┴─────────────────────────────┘
"""


# ============================================================
# 常见问题解答（Q&A）
# ============================================================
print("\n" + "=" * 60)
print("常见问题解答")
print("=" * 60)

# Q1: 为什么用 while True 而不是 do-while？
print("\n--- Q1: while True + break vs C++ do-while ---")
print("Python 没有 do-while 循环！")
print("用 while True + break 模拟，这是 Python 的标准做法")
print("")
print("C++:                                  Python:")
print("  do {                                  while True:")
print("    // 循环体                              # 循环体")
print("  } while (condition);                   if not condition:")
print("                                            break")

# Q2: __init__.py 一定要写内容吗？
print("\n--- Q2: __init__.py 的内容 ---")
print("可以完全为空！大多数项目就是空文件")
print("需要时才加内容：")
print("  - __all__ = ['auth', 'database']  # 控制 from package import *")
print("  - 导入子模块方便外部使用")
print("  - 包级别的初始化代码")

# Q3: hashlib vs bcrypt？
print("\n--- Q3: hashlib vs bcrypt/argon2 ---")
print("hashlib.sha256 + salt：学习用途，速度太快（可被暴力破解）")
print("bcrypt / argon2：生产环境推荐，故意慢（增加暴力破解成本）")
print("本课程用 hashlib 理解原理，实际项目用 bcrypt")

# Q4: 导入模块时，代码会被执行吗？
print("\n--- Q4: import 会执行代码吗？ ---")
print("会！import 时 Python 会执行整个模块文件")
print("这也是为什么用 if __name__ == '__main__': 保护测试代码")
print("")
print("  # module.py")
print("  print('模块被导入了！')  # import module 时会打印")
print("")
print("  if __name__ == '__main__':")
print("      print('直接运行 module.py 时才打印')")
print("  # __name__ 在被 import 时是模块名，直接运行时是 '__main__'")

# Q5: 为什么 register_user 返回 bool？
print("\n--- Q5: 返回值设计 ---")
print("方案1：返回 bool → 调用方自己处理成功/失败")
print("方案2：抛异常 → 调用方必须 try/except")
print("方案3：返回 Result 对象（Rust 风格）→ Python 少见")
print("")
print("注册场景用 bool 就够了（只关心成功/失败）")
print("复杂场景可以返回 (bool, str) 表示(成功?, 消息)")

# Q6: 输入密码时能不能不显示（像 Linux sudo）？
print("\n--- Q6: 密码输入隐藏 ---")
print("可以！用 getpass 模块：")
print("  from getpass import getpass")
print("  password = getpass('密码: ')  # 输入时不回显")
print("注意：在 PyCharm 等 IDE 中可能不生效，终端里正常")

print("\n[OK] Day 9 笔记结束！打开 day09_exercise.py 做练习吧。")
