"""
============================================================
Day 9 练习：CLI 菜单 + 用户认证
============================================================
在开始前，请先阅读 day09_notes.py 理解今天的知识点，
然后完成下面的练习（每道题 15-25 分钟）。
"""

# ============================================================
# 练习 1：构建命令行菜单系统
# ============================================================
"""
题目：实现一个简易计算器菜单

要求：
1. 用 while True 循环保持菜单运行，直到用户选择"退出"
2. 显示以下菜单选项：
   ┌─────────────────────┐
   │  简易计算器          │
   │  1. 加法             │
   │  2. 减法             │
   │  3. 乘法             │
   │  4. 除法             │
   │  5. 退出             │
   └─────────────────────┘
3. 用户选择 1-4 后，提示输入两个数字，输出计算结果
4. 除法时检查除数是否为 0，给出提示
5. 输入无效选项时给出"无效选项"提示
6. 使用字典映射来处理菜单（参考笔记 2.2）

提示：
  - choice = input("请选择: ").strip()
  - 把操作函数存在 dict 里，key 是菜单编号
  - 用 try/except 处理非数字输入
"""

# TODO: 在这里写练习 1 的代码

def calculator_menu():
   
   def add():
      a = float(input("第一个数:"))
      b = float(input("第二个数:"))
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
      print("谢谢使用,再见！")
      return "exit"
   
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
      
      choice = input("请选择(1-5):").strip()
      
      if choice in menu:
         try:
            result = menu[choice]()
            if result == "exit":
               break
         except ValueError:
            print("输入错误：请输入有效的数字")
      else:
         print(f"无效选项: {choice}，请输入 1-5")
 
#calculator_menu()


# ============================================================
# 练习 2：密码验证器
# ============================================================
"""
题目：实现密码强度验证和确认密码功能

要求：
1. 写一个函数 validate_password(password: str) -> tuple[bool, str]
   - 返回 (是否通过, 错误信息)
   - 规则：
     a) 长度至少 6 位 → 否则返回 "密码至少需要 6 位"
     b) 不能全是数字   → 否则返回 "密码不能全是数字"
     c) 不能全是字母   → 否则返回 "密码不能全是字母"

2. 写一个注册流程函数 register_flow()
   - 提示输入用户名（不能为空）
   - 提示输入密码，调用 validate_password 验证
   - 提示确认密码，两次输入必须一致
   - 全部通过后打印 "注册成功！用户名: xxx"
   - 任何一步失败都重新开始（当前步骤重试即可）

提示：
  - password.isdigit() → 是否全是数字
  - password.isalpha() → 是否全是字母
  - 用 while 循环处理每步的输入验证

额外挑战（选做）：
  - 再加一个规则：密码必须包含至少一个数字 → "密码必须包含数字"
"""

# TODO: 在这里写练习 2 的代码

def validate_password(password:str) -> tuple:
   if len(password) <6:
      return False,"密码至少需要6位"
   
   if password.isdigit():
      return False,"密码不能全是数字"
   
   if password.isalpha():
      return False,"密码不能全是字母"
   
   return True,"密码有效"

def register_flow():
   print(f"\n===用户注册===")
   
   #输入用户名
   while True:
      username = input("用户名：").strip()
      if username:
         break
      print("用户名不能为空")
      
   #输入密码
   while True:
      password = input("密码:").strip()
      ok,msg = validate_password(password)
      if ok:
         break
      print(f"密码不合格:{msg}")
      
   while True:
      confirm = input("确认密码: ").strip()
      if confirm == password:
               break
      print("两次密码不一致，请重新输入确认密码")
    
   print(f"\n注册成功！用户名: {username}")
   return username, password 
     
     


# ============================================================
# 练习 3：用户数据库操作类
# ============================================================
"""
题目：实现 UserDB 类，封装用户注册和登录的数据库操作

要求：
1. 创建 UserDB 类，__init__ 接受 db_path 参数，并初始化用户表
   - 表名: users
   - 字段: id (自增主键), username (唯一), password_hash, salt, role

2. 实现 register(username, password, role="student") 方法
   - 用 hashlib.sha256 + os.urandom(16) 做加盐哈希
   - 返回 (True, "注册成功") 或 (False, "用户名已存在")
   - 用 try/except IntegrityError 处理重复用户名

3. 实现 login(username, password) 方法
   - 返回 (True, user_dict) 或 (False, "错误信息")
   - user_dict 包含 id, username, role（不含密码相关字段）

4. 写测试代码验证：
   - 注册一个用户 → 输出结果
   - 用正确密码登录 → 输出用户名和角色
   - 用错误密码登录 → 输出错误信息
   - 重复注册 → 输出用户名已存在

提示：
  - 参考 day09_notes.py 中的 hash_password / verify_password 函数
  - 数据库连接用 with sqlite3.connect(...) as conn:
  - conn.row_factory = sqlite3.Row 让查询结果支持字典访问

额外挑战（选做）：
  - 实现 change_password(username, old_pw, new_pw) 方法
"""

import sqlite3
import hashlib
import os

# TODO: 在这里写练习 3 的代码
class UserDB:
   def __init__(self,db_path="calculator.db"):
      self.db_path = db_path
      self._init_table()
   
   def _init_table(self):
      with sqlite3.connect(self.db_path) as conn:
         conn.execute(
            """CREATE TABLE IF NOT EXISTS users(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               username TEXT UNIQUE NOT NULL,
               password_hash TEXT NOT NULL,
               salt TEXT NOT NULL,
               role TEXT DEFAULT 'student'
            
            )
            
            
            """        
         )

   @staticmethod
   def _hash_password(password:str)-> tuple:
      salt = os.urandom(16).hex()
      hashed = hashlib.sha256((password+salt).encode()).hexdigest()
      return salt,hashed
   
   @staticmethod
   def _verify_password(password:str,salt:str,stored_hash:str)->bool:
      return hashlib.sha256((password + salt).encode()).hexdigest() == stored_hash
   
   #注册
   def register(self,username: str, password: str, role="student") ->tuple:
      salt,pw_hash = self._hash_password(password)
      try:
         with sqlite3.connect(self.db_path) as conn:
            conn.execute(
               "INSERT INTO users (username,password_hash,salt,role)"
               "VALUES (?,?,?,?)",
               (username,pw_hash,salt,role)
               
            )
         return True,"注册成功"
      except sqlite3.IntegrityError:
         return False,"用户已存在"

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
   
   #获取所有用户
   def get_all_user(self):
      with sqlite3.connect(self.db_path) as conn:
         conn.row_factory = sqlite3.Row
         rows = conn.execute(
            "SELECT id,username,role FROM users  ORDER BY id"
         
         ).fetchall()
         return [dict(r) for r in rows]
   
   def count_users(self) -> int:
           """返回用户总数"""
           with sqlite3.connect(self.db_path) as conn:
               row = conn.execute("SELECT COUNT(*) FROM users").fetchone()
               return row[0]
   

print("\n[OK] 练习已准备就绪，开始写代码吧！")
print("提示：先通读所有题目，从练习 1 开始逐个完成。")
print("每道题预计 20-30 分钟，共 3 题。")
