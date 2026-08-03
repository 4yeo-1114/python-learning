"""
============================================================
Day 15 练习 3 参考答案：StudentDB 单元测试
============================================================
测试 StudentDB 的 CRUD + 搜索功能。
使用临时文件数据库，测试结束后自动删除，不影响真实数据。

运行方式：
  cd day15_wrapup
  pytest test_app.py -v

注意：不能用 :memory: 做 db_path，因为 StudentDB 每个方法
都会创建新的 sqlite3 连接，而 :memory: 的新连接 = 新数据库，
导致表丢失。用临时文件可以解决这个问题。
"""

import pytest

# 从同目录的 day15_solution 或 day15_exercise 导入 StudentDB
# （两边类代码一样，任选一个即可）
from day15_exercise import StudentDB


@pytest.fixture
def db(tmp_path):
    """
    创建使用临时文件数据库的 StudentDB 实例。
    使用 pytest 内置的 tmp_path fixture，每个测试有独立的临时目录，
    测试结束后 pytest 自动清理临时目录。

    借助 tmp_path 避免 Windows 文件锁和测试间数据污染问题。
    不能用 :memory:，因为 StudentDB 每个方法都创建新连接，
    而每个 :memory: 连接都会创建一个全新的空白内存数据库。
    """
    db_path = str(tmp_path / "test.db")
    return StudentDB(db_path=db_path)


# ── 练习 3a: 测试添加学生 ──

def test_add_student(db):
    """添加学生后，count 应该增加"""
    ok, sid = db.add_student("张三", 20, "1班", "计算机科学")
    assert ok
    assert sid == 1  # 第一个学生的 ID 是 1
    assert db.count_students() == 1

    # 再添加一个
    ok, sid = db.add_student("李四", 19, "2班", "软件工程")
    assert ok
    assert sid == 2
    assert db.count_students() == 2


def test_add_student_minimal(db):
    """grade 和 major 可以为空（默认值）"""
    ok, sid = db.add_student("王五", 18)
    assert ok
    student = db.get_student(sid)
    assert student["name"] == "王五"
    assert student["grade"] == ""
    assert student["major"] == ""


# ── 练习 3b: 测试搜索 ──

def test_search_students(db):
    """搜索按姓名和专业模糊匹配"""
    db.add_student("张三", 20, "1班", "计算机科学")
    db.add_student("李四", 19, "2班", "软件工程")
    db.add_student("王五", 21, "3班", "人工智能")

    # 按专业搜索
    results = db.search_students("计算机")
    assert len(results) == 1
    assert results[0]["name"] == "张三"

    # 按姓名搜索
    results = db.search_students("李四")
    assert len(results) == 1
    assert results[0]["major"] == "软件工程"

    # 搜索不存在的关键字
    results = db.search_students("不存在")
    assert len(results) == 0

    # 搜索"工程" — 软件工程应该匹配
    results = db.search_students("工程")
    assert len(results) == 1
    assert results[0]["name"] == "李四"


def test_search_case_sensitive(db):
    """LIKE 默认不区分大小写（SQLite 行为取决于 PRAGMA）"""
    db.add_student("Alice", 20, "A班", "Computer Science")
    results = db.search_students("computer")
    # SQLite LIKE 对 ASCII 默认不区分大小写
    assert len(results) == 1


def test_search_partial_match(db):
    """模糊搜索：搜索部分字符串也能匹配"""
    db.add_student("张三丰", 20, "1班", "武术")
    db.add_student("张三", 19, "2班", "文学")

    # 搜索 "张三" 应该匹配 "张三丰" 和 "张三"
    results = db.search_students("张三")
    assert len(results) == 2


# ── 练习 3c: 测试更新 ──

def test_update_student(db):
    """更新后 get_student 应返回新数据"""
    db.add_student("张三", 20, "1班", "CS")
    ok, msg = db.update_student(1, "张三改", 21, "2班", "AI")
    assert ok
    assert msg == "更新成功"

    updated = db.get_student(1)
    assert updated["name"] == "张三改"
    assert updated["age"] == 21
    assert updated["grade"] == "2班"
    assert updated["major"] == "AI"


def test_update_nonexistent(db):
    """更新不存在的学生应返回失败"""
    ok, msg = db.update_student(999, "某人", 20, "X班", "Y")
    assert not ok
    assert "不存在" in msg


# ── 练习 3d: 测试删除 ──

def test_delete_student(db):
    """删除后 get_student 应返回 None，count 应减少"""
    db.add_student("张三", 20, "1班", "CS")
    db.add_student("李四", 19, "2班", "SE")
    assert db.count_students() == 2

    ok, msg = db.delete_student(1)
    assert ok
    assert msg == "删除成功"
    assert db.count_students() == 1
    assert db.get_student(1) is None  # 已删除，查不到
    assert db.get_student(2) is not None  # 李四还在


def test_delete_nonexistent(db):
    """删除不存在的学生应返回失败"""
    ok, msg = db.delete_student(999)
    assert not ok
    assert "不存在" in msg


# ── 补充测试: get_all_students 排序 ──

def test_get_all_students_order(db):
    """应按照 id 排序返回"""
    db.add_student("C", 20)
    db.add_student("A", 19)
    db.add_student("B", 21)

    students = db.get_all_students()
    assert len(students) == 3
    # 按 id 排序，所以顺序是 C, A, B（按插入顺序）
    assert students[0]["name"] == "C"
    assert students[1]["name"] == "A"
    assert students[2]["name"] == "B"


# ── 补充测试: get_student 返回的字段完整性 ──

def test_get_student_fields(db):
    """返回的 dict 应包含所有字段"""
    db.add_student("张三", 20, "1班", "计算机科学")
    student = db.get_student(1)

    assert "id" in student
    assert "name" in student
    assert "age" in student
    assert "grade" in student
    assert "major" in student
    assert "created_at" in student
    assert student["id"] == 1
    assert student["name"] == "张三"
