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
 
calculator_menu()

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


print("\n[OK] 练习已准备就绪，开始写代码吧！")
print("提示：先通读所有题目，从练习 1 开始逐个完成。")
print("每道题预计 20-30 分钟，共 3 题。")
