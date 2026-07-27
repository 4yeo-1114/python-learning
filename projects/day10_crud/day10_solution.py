"""
============================================================
Day 10 参考答案：学生信息 CRUD 操作
============================================================
注意：请先独立完成 day10_exercise.py 再对照此答案！
"""

import sqlite3
from datetime import datetime


# ============================================================
# 练习 1：StudentDB 类 — 建表 + 添加学生
# ============================================================

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
        """
        添加学生
        返回: (True, new_id) 或 (False, "错误信息")
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    "INSERT INTO students (name, age, grade, major) VALUES (?, ?, ?, ?)",
                    (name, age, grade, major)
                )
                return True, cursor.lastrowid
        except sqlite3.Error as e:
            return False, f"添加失败: {e}"

    def count_students(self) -> int:
        """返回学生总数"""
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute("SELECT COUNT(*) FROM students").fetchone()
            return row[0]


# ============================================================
# 练习 2：查询功能
# ============================================================

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
        """
        按姓名或专业模糊搜索
        返回匹配的学生字典列表
        """
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


# ============================================================
# 练习 3：更新 + 删除
# ============================================================

    def update_student(self, student_id: int, **kwargs):
        """
        更新学生信息，只更新传入的字段
        返回: (True, "更新成功") 或 (False, "错误信息")
        """
        if not kwargs:
            return False, "没有需要更新的字段"

        # 动态构建 SET 子句
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
        """
        删除学生
        返回: (True, "删除成功") 或 (False, "学生不存在")
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "DELETE FROM students WHERE id = ?",
                (student_id,)
            )
            if cursor.rowcount == 0:
                return False, "学生不存在"
            return True, "删除成功"


# ============================================================
# 测试代码（全部练习）
# ============================================================

if __name__ == "__main__":
    import os
    db_path = os.path.join(os.path.dirname(__file__), "_test_students.db")
    db = StudentDB(db_path)


    # --- 练习 1 测试 ---
    print("=" * 50)
    print("练习 1：建表 + 添加学生")
    print("=" * 50)

    ok, result = db.add_student("张三", 20, "2024级1班", "计算机科学")
    print(f"添加结果: {ok}, id={result}")

    db.add_student("张三丰", 22, "2023级1班", "人工智能")
    db.add_student("李四", 19, "2024级2班", "软件工程")
    print(f"学生总数: {db.count_students()}")

    # --- 练习 2 测试 ---
    print("\n" + "=" * 50)
    print("练习 2：查询功能")
    print("=" * 50)

    print("=== 全部学生 ===")
    for s in db.get_all_students():
        print(f"  {s['id']}: {s['name']}, {s['age']}岁, {s['grade']}, {s['major']}")

    print("=== 搜索 '张' ===")
    for s in db.search_students("张"):
        print(f"  {s['name']} - {s['major']}")

    print("=== 搜索 '软件' ===")
    for s in db.search_students("软件"):
        print(f"  {s['name']} - {s['major']}")

    student = db.get_student_by_id(1)
    print(f"ID=1: {student['name']}")

    # --- 练习 3 测试 ---
    print("\n" + "=" * 50)
    print("练习 3：更新 + 删除")
    print("=" * 50)

    print("=== 更新测试 ===")
    print(f"更新前: {db.get_student_by_id(1)['name']}")
    ok, msg = db.update_student(1, name="张三三", age=21)
    print(f"更新结果: {ok}, {msg}")
    updated = db.get_student_by_id(1)
    print(f"更新后: {updated['name']}, {updated['age']}岁")

    # 空字段测试
    ok, msg = db.update_student(1)
    print(f"空字段测试: {ok}, {msg}")

    # 不存在学生测试
    ok, msg = db.update_student(999, name="nobody")
    print(f"不存在测试: {ok}, {msg}")

    print("\n=== 删除测试 ===")
    print(f"删除前总数: {db.count_students()}")
    ok, msg = db.delete_student(2)
    print(f"删除 id=2: {ok}, {msg}")
    print(f"删除后总数: {db.count_students()}")

    ok, msg = db.delete_student(999)
    print(f"删除 id=999: {ok}, {msg}")
