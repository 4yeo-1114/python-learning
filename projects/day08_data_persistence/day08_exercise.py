"""
============================================================
Day 8 练习：JSON + CSV + SQLite
============================================================
完成以下 4 道练习题，巩固今天所学的三大数据持久化方案。
答案见 day08_solution.py
"""

import json
import csv
import sqlite3
import os

# ============================================================
# 练习 1：JSON — 任务管理器的数据存取
# ============================================================
"""
题目：实现任务管理器的 JSON 存取功能。

要求：
1. 实现函数 save_tasks(tasks, filename)，将任务列表保存为 JSON 文件
   - tasks 是 list[dict]，每个 dict 包含: id, title, done, priority
   - 保存时使用 indent=2, ensure_ascii=False, sort_keys=True
   - 如果保存成功返回 True

2. 实现函数 load_tasks(filename)，从 JSON 文件加载任务列表
   - 返回 list[dict]
   - 如果文件不存在返回空列表 []

3. 实现函数 add_task(tasks, title, priority)，向任务列表添加一条新任务
   - 自动分配 id（取当前最大 id + 1，空列表时 id=1）
   - done 默认为 False
   - priority 可选值为 "高"/"中"/"低"，默认为 "中"
   - 返回更新后的 tasks 列表

调用示例：
tasks = []
tasks = add_task(tasks, "完成Python作业", "高")
tasks = add_task(tasks, "跑步30分钟", "中")
save_tasks(tasks, "tasks.json")        # → True
loaded = load_tasks("tasks.json")
print(loaded)
# [{"done": false, "id": 1, "priority": "高", "title": "完成Python作业"},
#  {"done": false, "id": 2, "priority": "中", "title": "跑步30分钟"}]
"""

# TODO: 在这里实现 save_tasks 函数
def save_tasks(tasks, filename):
   try:
      with  open(filename,"w",encoding="utf-8") as f:
         json.dump(tasks,f,indent=2,ensure_ascii=False,sort_keys=True)
      return True
   except Exception as e:
      print(f"保存失败:{e}")
      return False
   
def load_tasks(filename):
   if not os.path.exists(filename):
      return []
   try:
      with open(filename,"r",encoding="utf-8") as f:
         return json.load(f)
   except(json.JSONDecodeError,FileNotFoundError):
      return []
   
   

# TODO: 在这里实现 add_task 函数
def add_task(tasks, title, priority="中"):
   #自动分配id
   if tasks:
      max_id = max(task["id"] for task in tasks)
   else:
      max_id = 0
   
   new_task ={
      "id": max_id+1,
      "title":title,
      "done":False,
      "priority":priority,
   }
   tasks.append(new_task)
   return tasks


# ============================================================
# 练习 2：CSV — 学生成绩表读写
# ============================================================
"""
题目：用 CSV 模块读写学生成绩表。

要求：
1. 实现函数 write_grades_csv(filename, students)
   - students 是 list[dict]，每个 dict 有: 姓名, 语文, 数学, 英语
   - 用 csv.DictWriter 写入 CSV 文件
   - 表头为: 姓名, 语文, 数学, 英语
   - 返回写入的行数（不含表头）

2. 实现函数 read_grades_csv(filename)
   - 用 csv.DictReader 读取 CSV 文件
   - 返回 list[dict]

3. 实现函数 calc_averages(students)
   - 计算每个学生的平均分（语文+数学+英语）/ 3
   - 为每个学生 dict 添加 "平均分" 字段（保留一位小数）
   - 返回更新后的 students 列表

调用示例：
students = [
    {"姓名": "张三", "语文": 85, "数学": 92, "英语": 78},
    {"姓名": "李四", "语文": 90, "数学": 88, "英语": 95},
]
write_grades_csv("grades.csv", students)  # → 2
loaded = read_grades_csv("grades.csv")
result = calc_averages(loaded)
# result[0]["平均分"] → 85.0
# result[1]["平均分"] → 91.0
"""


# TODO: 在这里实现 write_grades_csv 函数
def write_grades_csv(filename, students):
   """用 DictWriter 将学生成绩列表写入 CSV 文件"""
   fieldnames = ["姓名", "语文", "数学", "英语"]
   with open(filename,"w",newline="",encoding="utf-8-sig") as f:
      writer = csv.DictWriter(f,fieldnames=fieldnames)
      writer.writerheader()
      writer.writerrows(students)
   return len(students)
      
    
    
    
# TODO: 在这里实现 read_grades_csv 函数
def read_grades_csv(filename):
   """用 DictReader 从 CSV 文件读取学生成绩"""
   
   with open(filename,"r",encoding="utf-8-sig") as f:
      reader =csv.DictReader(f)
      return list(reader)

# TODO: 在这里实现 calc_averages 函数
def calc_averages(students):
   """为每个学生计算平均分并添加"平均分"字段"""
   
   for s in students:
      chinese = float(s["语文"])
      math = float(s["数学"])
      english = float(s["英语"])
      #round是四舍五入函数 1表示保留一位小数
      s["平均分"] = round((chinese + math + english) / 3, 1)
   return students


# ============================================================
# 练习 3：SQLite — 学生数据库 CRUD
# ============================================================
"""
题目：实现一个完整的学生数据库操作类 StudentDB。

要求（参考 day08_notes.py 中的 StudentDB 示例，但要自己实现）：

1. __init__(self, db_path)：
   - 保存 db_path
   - 调用 self._init_table() 初始化表

2. _init_table(self)：
   - 创建 students 表（如果不存在）
   - 字段：id (INTEGER PRIMARY KEY AUTOINCREMENT),
          name (TEXT NOT NULL),
          age (INTEGER),
          grade (TEXT),
          score (REAL)
   - 使用 with 语句管理连接

3. add(self, name, age, grade, score)：
   - 插入一条学生记录
   - 使用 ? 占位符，不要用 f-string！

4. get_all(self)：
   - 返回所有学生，每条为 dict
   - 按 id 升序排列
   - 提示：设置 conn.row_factory = sqlite3.Row

5. get_by_name(self, name)：
   - 按姓名查找，返回 dict 或 None

6. update_score(self, name, new_score)：
   - 按姓名更新成绩

7. delete(self, name)：
   - 按姓名删除学生

8. count_by_grade(self, grade)：
   - 统计某班级的学生人数
   - 返回 int

调用示例：
db = StudentDB("test_school.db")
db.add("张三", 20, "一班", 85.5)
db.add("李四", 22, "一班", 92.0)
db.add("王五", 21, "二班", 78.5)
print(db.get_all())                    # 3 条记录
print(db.get_by_name("张三"))          # {'id': 1, 'name': '张三', ...}
db.update_score("张三", 99.0)
print(db.count_by_grade("一班"))       # 2
db.delete("王五")
"""

# TODO: 在这里实现 StudentDB 类
class StudentDB:
   def __init__(self,db_path):
      self.db_path  = db_path
      self._init_table()
      
   def _init_table(self):
      #初始化表结构
      with sqlite3.connect(self.db_path) as conn:
         conn.execute("""
            CREATE TABLE IF NOT EXISTS students(
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  age INTEGER,
                  grade TEXT,
                  score REAL
               )"""  
         )
   def add(self,name,age,grade,score):
      with sqlite3.connect(self.db_path) as conn:
         conn.execute(
            "INSERT INTO students(name,age,grade,score) VALUES(?,?,?,?)",
            (name,age,grade,score)
         )
   def get_all(self):
      #获取所有的学生按id升序
      with sqlite3.connect(self.db_path) as conn:
         conn.row_factory = sqlite3.Row
         rows = conn.execute(
            "SELECT * FROM students ORDER BY id"
         ).fetchall()
         return [dict(r) for r in rows]
   
   def get_by_name(self,name):
      with sqlite3.connect(self.db_path) as conn:
         conn.row_factory =sqlite3.Row
         row = conn.execute(
            "SELECT * FROM students WHERE name = ?",
            (name,)
         ).fetchone()
         return dict(row) if row else None
   
   def update_score(self, name, new_score):
           """更新学生成绩"""
           with sqlite3.connect(self.db_path) as conn:
               conn.execute(
                   "UPDATE students SET score = ? WHERE name = ?",
                   (new_score, name)
               )
   
   def delete(self, name):
           """删除学生"""
           with sqlite3.connect(self.db_path) as conn:
               conn.execute(
                   "DELETE FROM students WHERE name = ?", (name,)
               )
   
   def count_by_grade(self, grade):
           """统计某班级的学生人数"""
           with sqlite3.connect(self.db_path) as conn:
               row = conn.execute(
                   "SELECT COUNT(*) FROM students WHERE grade = ?", (grade,)
               ).fetchone()
               return row[0]

# ============================================================
# 练习 4（综合题）：CSV ↔ SQLite 数据导入导出
# ============================================================
"""
题目：结合 CSV 和 SQLite，实现学生数据的导入导出功能。

场景：你有一个 CSV 文件存储学生数据，需要导入到 SQLite 数据库中；
      同时，也需要将数据库中的数据导出为 CSV 文件方便 Excel 查看。

要求：
1. 实现函数 import_from_csv(db, csv_filename)
   - 从 CSV 文件读取学生数据
   - CSV 表头：姓名,年龄,班级,成绩
   - 将每行数据插入到 StudentDB（练习3的类）中
   - 返回成功导入的条数
   - 如果 CSV 文件不存在，打印提示并返回 0

2. 实现函数 export_to_csv(db, csv_filename, grade=None)
   - 将数据库中的学生数据导出为 CSV 文件
   - 如果 grade 不为 None，只导出指定班级的学生
   - 如果 grade 为 None，导出全部学生
   - CSV 表头：姓名,年龄,班级,成绩
   - 返回导出的条数

提示：
- CSV 读取的数值可能是字符串，记得转换 age 为 int，score 为 float
- 导入时可以跳过 CSV 的表头行

调用示例：
# 先准备一个测试 CSV
with open("import_students.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["姓名", "年龄", "班级", "成绩"])
    writer.writerows([
        ["导入A", 19, "三班", 76.0],
        ["导入B", 20, "三班", 82.5],
    ])

db = StudentDB("import_test.db")
n = import_from_csv(db, "import_students.csv")   # → 2
print(f"导入了 {n} 条")

n2 = export_to_csv(db, "export_all.csv")          # → 导出全部
print(f"导出了 {n2} 条")

n3 = export_to_csv(db, "export_三班.csv", grade="三班")  # → 2
print(f"导出了 {n3} 条三班学生")
"""

def import_from_csv(db, csv_filename):
    """
    从 CSV 文件导入学生数据到数据库。

    CSV 表头：姓名,年龄,班级,成绩

    Args:
        db: StudentDB 实例
        csv_filename: CSV 文件路径
    Returns:
        int: 成功导入的条数
    """
    if not os.path.exists(csv_filename):
        print(f"文件不存在: {csv_filename}")
        return 0

    count = 0
    with open(csv_filename, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["姓名"]
            age = int(row["年龄"])           # CSV 读出来是字符串，要转换
            grade = row["班级"]
            score = float(row["成绩"])       # 同理转 float
            db.add(name, age, grade, score)
            count += 1
    return count


def export_to_csv(db, csv_filename, grade=None):
    """
    将数据库中的学生数据导出为 CSV 文件。

    Args:
        db: StudentDB 实例
        csv_filename: 导出路径
        grade: 指定班级，None 表示导出全部
    Returns:
        int: 导出的条数
    """
    # 获取数据：全部或按班级筛选
    if grade is None:
        students = db.get_all()
    else:
        students = [s for s in db.get_all() if s["grade"] == grade]

    # 写入 CSV
    fieldnames = ["姓名", "年龄", "班级", "成绩"]
    with open(csv_filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for s in students:
            writer.writerow({
                "姓名": s["name"],
                "年龄": s["age"],
                "班级": s["grade"],
                "成绩": s["score"],
            })

    return len(students)

# ============================================================
# 测试入口
# ============================================================
if __name__ == '__main__':
    print("=" * 60)
    print("Day 8 练习 — 请逐个完成各题，答案见 day08_solution.py")
    print("=" * 60)
