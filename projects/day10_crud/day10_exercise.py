"""
============================================================
Day 10 练习：学生信息 CRUD 操作
============================================================
在开始前，请先阅读 day10_notes.py 理解今天的知识点，
然后完成下面的练习（3 道题，每题约 15-20 分钟）。
"""

import sqlite3
from datetime import datetime

# ============================================================
# 练习 1：StudentDB 类 — 建表 + 添加学生
# ============================================================
"""
题目：创建 StudentDB 类，实现数据库初始化和添加学生功能

要求：
1. 创建 StudentDB 类，__init__ 接受 db_path 参数
2. 实现 _init_table() 方法，创建 students 表：
   - id: INTEGER 自增主键
   - name: TEXT NOT NULL
   - age: INTEGER
   - grade: TEXT（班级，默认空字符串）
   - major: TEXT（专业，默认空字符串）
   - created_at: TEXT（默认当前时间 datetime('now','localtime')）

3. 实现 add_student(name, age, grade="", major="") 方法
   - 用参数化查询（? 占位符，不要字符串拼接！）
   - 返回 (True, new_id) 或 (False, "错误信息")
   - 用 try/except 捕获异常

4. 实现 count_students() 方法，返回学生总数
   - 用 SELECT COUNT(*) 查询

提示：
  - CREATE TABLE IF NOT EXISTS ... 确保不重复建表
  - INSERT INTO students (name, age, grade, major) VALUES (?, ?, ?, ?)
  - cursor.lastrowid 可以获取刚插入记录的自增 id
"""
class StudentDB:
   def __init__(self,db_path:str="students.db"):
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

   def add_student(self,name,age,grade,str,major):
      try:
         with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
               "INSERT INTO students (name,age,grade,major) VALUES (?,?,?,?)",
               (name,age,grade,major)
            )
         return True,cursor.lastrowid
      except sqlite3.Error as e:
         return False,f"添加失败:{e}"
      
   def count_student(self):
      with sqlite3.connect(self.db_path) as conn:
               row = conn.execute("SELECT COUNT(*) FROM students").fetchone()
               return row[0]
         



# 测试代码（写完 StudentDB 后取消注释运行）
# db = StudentDB("test_students.db")  # 用文件路径，不要用 :memory:（每次连接会丢失）
# ok, result = db.add_student("张三", 20, "2024级1班", "计算机科学")
# print(f"添加结果: {ok}, id={result}")
# db.add_student("李四", 19, "2024级2班", "软件工程")
# print(f"学生总数: {db.count_students()}")
# 期望输出: 添加结果: True, id=1
#          学生总数: 2


# ============================================================
# 练习 2：查询学生 — 全量查询 + 关键词搜索
# ============================================================
"""
题目：给 StudentDB 添加查询功能

要求：
1. 实现 get_all_students() 方法
   - 返回所有学生，按 id 升序
   - 每条记录以字典形式返回：{"id": 1, "name": "张三", ...}
   - 提示：conn.row_factory = sqlite3.Row 让查询结果支持字典访问

2. 实现 search_students(keyword: str) 方法
   - 按关键词搜索 name 或 major 字段（用 LIKE 模糊匹配）
   - 返回匹配的学生列表（也是字典列表）
   - 提示：WHERE name LIKE ? OR major LIKE ?

3. 实现 get_student_by_id(student_id: int) 方法
   - 按 id 精确查找
   - 找到返回 dict，找不到返回 None

提示：
  - 模糊搜索的 % 通配符写在 Python 参数里，不写在 SQL 里
  - 记得 conn.row_factory = sqlite3.Row
"""

# TODO: 在这里写练习 2 的代码（在练习 1 的 StudentDB 类里添加方法）
def get_all_students(self) -> list[dict]:
      with sqlite3.connect(self.db_path) as conn:
         conn.row_factory = sqlite3.Row
         rows = conn.execute(
            "SELECT id,name,age,grade,major,created_at"
            "FROM students ORDER BY id"
            
         ).fetchall()
         return [dict(r) for r in rows]
      
def search_student(self,keyword:str)->list[dict]:
      with sqlite3.connect(self.db_path) as conn:
            conn.row_factory  =sqlite3.Row
            pattern = f"%{keyword}%"
            rows = conn.execute(
               "SELECT id,name,age,grade,major,created_at"
               "FROM students"
               "WHERE name LIKE ? OR major LIKE ?"
               (pattern,pattern)
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


# 测试代码（写完方法后取消注释运行）
# db = StudentDB("test_students.db")
# db.add_student("张三", 20, "2024级1班", "计算机科学")
# db.add_student("张三丰", 22, "2023级1班", "人工智能")
# db.add_student("李四", 19, "2024级2班", "软件工程")
#
# print("=== 全部学生 ===")
# for s in db.get_all_students():
#     print(f"  {s['id']}: {s['name']}, {s['major']}")
#
# print("=== 搜索'张' ===")
# for s in db.search_students("张"):
#     print(f"  {s['name']} - {s['major']}")
#
# print("=== 搜索'软件' ===")
# for s in db.search_students("软件"):
#     print(f"  {s['name']} - {s['major']}")
#
# student = db.get_student_by_id(1)
# print(f"ID=1 的学生: {student['name']}")
# 期望输出:
# === 全部学生 ===
#   1: 张三, 计算机科学
#   2: 张三丰, 人工智能
#   3: 李四, 软件工程
# === 搜索'张' ===
#   张三 - 计算机科学, 张三丰 - 人工智能
# === 搜索'软件' ===
#   李四 - 软件工程
# ID=1 的学生: 张三


# ============================================================
# 练习 3：更新 + 删除学生
# ============================================================
"""
题目：给 StudentDB 添加更新和删除功能

要求：
1. 实现 update_student(student_id: int, **kwargs) 方法
   - 支持只更新传入的字段（动态构建 SQL）
   - 例如 update_student(1, name="新名字", grade="新班级")
   - 返回 (True, "更新成功") 或 (False, "错误信息")
   - 如果 kwargs 为空，返回 (False, "没有需要更新的字段")

2. 实现 delete_student(student_id: int) 方法
   - 删除指定 id 的学生
   - 返回 (True, "删除成功") 或 (False, "学生不存在")
   - 提示：用 cursor.rowcount 判断是否真的删除了记录

提示：
  - 动态 UPDATE: ", ".join(f"{k} = ?" for k in kwargs.keys())
  - cursor.rowcount: 受影响的行数（>0 表示操作成功）
  - 删除前可以先检查学生是否存在

额外挑战（选做）：
  - 添加输入验证：name 不能为空，age 必须是正整数
  - 添加一个方法，让年龄增加 1 岁（批量升级）
"""

# TODO: 在这里写练习 3 的代码（在 StudentDB 类里继续添加方法）


def update_student(self,student_id:int,**kwargs):
   if not kwargs:
      return False,"没有需要更新的字段"

   fields = ", ".join(f"{k}= ?" for k in kwargs.keys())
   values = list(kwargs.values())
   values.append(student_id)
   
   try:
      with sqlite3.connect(self.db_path) as conn:
         cursor = conn.execute(
            f"UPDATE student SET {fields} where id = ?",
            values
         )
         if cursor.rowcount == 0:
            return False,"学生不存在"
         else :
            return True,"更新成功"
   except sqlite3.Error as e:
         return False,f"更新失败：{e}"


def delete_student(self,student_id:int):
   with sqlite3.connect(self.db_path) as conn:
               cursor = conn.execute(
                   "DELETE FROM students WHERE id = ?",
                   (student_id,)
               )
               if cursor.rowcount == 0:
                   return False, "学生不存在"
               return True, "删除成功"







# 测试代码（写完方法后取消注释运行）
# db = StudentDB("test_students.db")
# db.add_student("王五", 21, "2023级1班", "数据科学")
# db.add_student("赵六", 20, "2024级3班", "网络工程")
#
# print("=== 更新前 ===")
# print(f"王五信息: {db.get_student_by_id(1)}")
#
# ok, msg = db.update_student(1, name="王五五", age=22)
# print(f"更新结果: {ok}, {msg}")
# print(f"更新后: {db.get_student_by_id(1)}")
#
# print("\n=== 删除测试 ===")
# ok, msg = db.delete_student(2)
# print(f"删除 id=2: {ok}, {msg}")
# print(f"剩余学生数: {db.count_students()}")
# ok, msg = db.delete_student(999)  # 不存在的 id
# print(f"删除 id=999: {ok}, {msg}")
# 期望输出:
# === 更新前 ===
# 王五信息: {'id': 1, 'name': '王五', 'age': 21, ...}
# 更新结果: True, 更新成功
# 更新后: {'id': 1, 'name': '王五五', 'age': 22, ...}
# === 删除测试 ===
# 删除 id=2: True, 删除成功
# 剩余学生数: 1
# 删除 id=999: False, 学生不存在


print("\n[OK] 练习已准备就绪！")
print("提示：3 道题层层递进，建议按顺序完成。")
print("答案见 day10_solution.py")
print(f"预计时间：约 50-60 分钟（每题 15-20 分钟）")
