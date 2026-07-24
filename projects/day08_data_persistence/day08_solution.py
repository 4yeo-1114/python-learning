"""
============================================================
Day 8 练习答案：JSON + CSV + SQLite
============================================================
"""

import json
import csv
import sqlite3
import os


# ============================================================
# 练习 1：JSON — 任务管理器的数据存取
# ============================================================

def save_tasks(tasks, filename):
    """
    将任务列表保存为 JSON 文件。

    Args:
        tasks: list[dict]，每个 dict 包含 id, title, done, priority
        filename: 保存路径
    Returns:
        bool: 保存成功返回 True
    """
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=2, ensure_ascii=False, sort_keys=True)
        return True
    except Exception as e:
        print(f"保存失败: {e}")
        return False


def load_tasks(filename):
    """
    从 JSON 文件加载任务列表。

    Args:
        filename: JSON 文件路径
    Returns:
        list[dict]: 任务列表，文件不存在时返回空列表
    """
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def add_task(tasks, title, priority="中"):
    """
    向任务列表添加一条新任务。

    Args:
        tasks: 当前任务列表
        title: 任务标题
        priority: 优先级，可选 "高"/"中"/"低"，默认 "中"
    Returns:
        list[dict]: 更新后的任务列表
    """
    # 自动分配 id
    if tasks:
        max_id = max(task["id"] for task in tasks)
    else:
        max_id = 0

    new_task = {
        "id": max_id + 1,
        "title": title,
        "done": False,
        "priority": priority,
    }
    tasks.append(new_task)
    return tasks


# ============================================================
# 练习 2：CSV — 学生成绩表读写
# ============================================================

def write_grades_csv(filename, students):
    """
    用 DictWriter 将学生成绩列表写入 CSV 文件。

    Args:
        filename: CSV 文件路径
        students: list[dict]，每个 dict 的键: 姓名, 语文, 数学, 英语
    Returns:
        int: 写入的数据行数（不含表头）
    """
    fieldnames = ["姓名", "语文", "数学", "英语"]
    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(students)
    return len(students)


def read_grades_csv(filename):
    """
    用 DictReader 从 CSV 文件读取学生成绩。

    Args:
        filename: CSV 文件路径
    Returns:
        list[dict]: 学生成绩列表
    """
    with open(filename, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        return list(reader)


def calc_averages(students):
    """
    为每个学生计算平均分并添加"平均分"字段。
    注意：CSV 读取的值是字符串，需要转换为数值。

    Args:
        students: list[dict]
    Returns:
        list[dict]: 添加了"平均分"字段的学生列表
    """
    for s in students:
        chinese = float(s["语文"])
        math = float(s["数学"])
        english = float(s["英语"])
        s["平均分"] = round((chinese + math + english) / 3, 1)
    return students


# ============================================================
# 练习 3：SQLite — 学生数据库 CRUD
# ============================================================

class StudentDB:
    """学生数据库操作类 — 封装常见 CRUD 操作"""

    def __init__(self, db_path):
        self.db_path = db_path
        self._init_table()

    def _init_table(self):
        """初始化表结构"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    age INTEGER,
                    grade TEXT,
                    score REAL
                )
            """)

    def add(self, name, age, grade, score):
        """添加学生"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO students (name, age, grade, score) VALUES (?, ?, ?, ?)",
                (name, age, grade, score)
            )

    def get_all(self):
        """获取所有学生，按 id 升序"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT * FROM students ORDER BY id"
            ).fetchall()
            return [dict(r) for r in rows]

    def get_by_name(self, name):
        """按姓名查找学生"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(
                "SELECT * FROM students WHERE name = ?", (name,)
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
# 测试代码
# ============================================================
if __name__ == '__main__':
    print("=" * 60)
    print("练习 1：JSON — 任务管理器的数据存取")
    print("=" * 60)

    tasks = []
    tasks = add_task(tasks, "完成Python作业", "高")
    tasks = add_task(tasks, "跑步30分钟", "中")
    tasks = add_task(tasks, "复习数据库知识", "高")
    print("当前任务列表:")
    for t in tasks:
        done_mark = "[OK]" if t["done"] else "[ ]"
    print(f"  [{t['priority']}] {t['title']} {done_mark}")

    save_tasks(tasks, "tasks.json")
    loaded = load_tasks("tasks.json")
    print(f"\n从文件加载: {len(loaded)} 条任务")

    # 测试文件不存在
    empty = load_tasks("nonexistent.json")
    print(f"不存在的文件返回: {empty}")

    # 清理
    os.remove("tasks.json")

    print("\n" + "=" * 60)
    print("练习 2：CSV — 学生成绩表读写")
    print("=" * 60)

    students = [
        {"姓名": "张三", "语文": 85, "数学": 92, "英语": 78},
        {"姓名": "李四", "语文": 90, "数学": 88, "英语": 95},
        {"姓名": "王五", "语文": 78, "数学": 85, "英语": 82},
    ]

    n = write_grades_csv("grades.csv", students)
    print(f"写入了 {n} 行")

    loaded = read_grades_csv("grades.csv")
    result = calc_averages(loaded)
    print("成绩表（含平均分）:")
    for s in result:
        print(f"  {s['姓名']}: 语文{s['语文']} 数学{s['数学']} 英语{s['英语']} → 平均分{s['平均分']}")

    # 清理
    os.remove("grades.csv")

    print("\n" + "=" * 60)
    print("练习 3：SQLite — 学生数据库 CRUD")
    print("=" * 60)

    db = StudentDB("test_school.db")

    # 添加数据
    db.add("张三", 20, "一班", 85.5)
    db.add("李四", 22, "一班", 92.0)
    db.add("王五", 21, "二班", 78.5)
    db.add("赵六", 20, "二班", 88.0)

    print("所有学生:")
    for s in db.get_all():
        print(f"  [{s['id']}] {s['name']}, {s['age']}岁, {s['grade']}, {s['score']}分")

    print(f"\n查找'张三': {db.get_by_name('张三')}")

    db.update_score("张三", 99.0)
    zhang = db.get_by_name("张三")
    print(f"更新后张三的成绩: {zhang['score']}分")

    print(f"一班人数: {db.count_by_grade('一班')}")
    print(f"二班人数: {db.count_by_grade('二班')}")

    db.delete("王五")
    print(f"删除王五后，剩余 {len(db.get_all())} 人")

    # 清理（Windows 下删除前确保连接完全关闭）
    try:
        os.remove("test_school.db")
    except PermissionError:
        pass

    print("\n" + "=" * 60)
    print("练习 4：CSV <-> SQLite 数据导入导出")
    print("=" * 60)

    # 准备测试 CSV
    with open("import_students.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["姓名", "年龄", "班级", "成绩"])
        writer.writerows([
            ["导入A", 19, "三班", 76.0],
            ["导入B", 20, "三班", 82.5],
            ["导入C", 21, "四班", 91.0],
        ])

    # 导入
    db2 = StudentDB("import_test.db")
    n = import_from_csv(db2, "import_students.csv")
    print(f"从 CSV 导入了 {n} 条记录")

    print("数据库内容:")
    for s in db2.get_all():
        print(f"  {s['name']}, {s['age']}岁, {s['grade']}, {s['score']}分")

    # 导出全部
    n2 = export_to_csv(db2, "export_all.csv")
    print(f"\n导出全部: {n2} 条")

    # 导出指定班级
    n3 = export_to_csv(db2, "export_三班.csv", grade="三班")
    print(f"导出三班: {n3} 条")

    # 验证导出文件
    print("\n导出文件内容（export_三班.csv）:")
    with open("export_三班.csv", "r", encoding="utf-8-sig") as f:
        print(f.read())

    # 清理
    for f in ["import_students.csv", "export_all.csv", "export_三班.csv", "import_test.db"]:
        try:
            os.remove(f)
        except PermissionError:
            pass

    print("\n[OK] Day 8 全部练习测试通过！")
