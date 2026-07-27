"""
============================================================
Day 10: 学生信息管理 — SQLite CRUD 操作（C++ 对比版）
============================================================
目标：在 Day 9 用户认证基础上，实现学生信息的增删改查
      学会参数化查询、LIKE 模糊搜索、封装数据访问层
"""

# ============================================================
# 第一部分：CRUD 基础 — 数据库四大操作
# ============================================================

print("=" * 60)
print("第一部分：CRUD 是什么")
print("=" * 60)

"""
CRUD = Create / Read / Update / Delete

┌──────────┬──────────┬──────────────────────────────────┐
│ 操作      │ SQL      │ 含义                              │
├──────────┼──────────┼──────────────────────────────────┤
│ Create   │ INSERT   │ 新增一条记录                       │
│ Read     │ SELECT   │ 查询记录（可以带条件、排序）         │
│ Update   │ UPDATE   │ 修改已有记录的字段                  │
│ Delete   │ DELETE   │ 删除记录                           │
└──────────┴──────────┴──────────────────────────────────┘

C++ 对比：
C++ 中你可能用文件读写 + struct 数组来做，Python+SQLite 更简单：
  - 不用自己写排序/查找算法（SQL 帮你做）
  - 数据持久化自动处理（不用手动 fwrite/fread）
  - 多条件查询一条语句搞定
"""


# ============================================================
# 第二部分：参数化查询 — 防 SQL 注入
# ============================================================

print("\n" + "=" * 60)
print("第二部分：参数化查询（重要！）")
print("=" * 60)

# 2.1 错误的写法：字符串拼接 ❌
"""
# 千万不要这样做！
name = input("输入名字: ")
conn.execute(f"SELECT * FROM students WHERE name = '{name}'")
# 用户输入:  '; DROP TABLE students; --
# ↑ 这就是 SQL 注入攻击
"""

# 2.2 正确的写法：参数化查询 ✅
# 用 ? 占位符，参数作为元组传入

import sqlite3

def demo_param_query():
    """演示参数化查询"""
    conn = sqlite3.connect(":memory:")  # 内存数据库，不写文件
    conn.execute("CREATE TABLE test (id INTEGER, name TEXT)")
    conn.execute("INSERT INTO test VALUES (1, '张伟')")
    conn.execute("INSERT INTO test VALUES (2, '李娜')")

    # 正确写法：? 占位 + 参数元组
    name = "张伟"
    row = conn.execute(
        "SELECT * FROM test WHERE name = ?",  # ? 是占位符
        (name,)                                # 参数用元组传入（注意逗号！）
    ).fetchone()
    print(f"查询结果: {row}")

    # 多个参数：
    conn.execute(
        "INSERT INTO test VALUES (?, ?)",
        (3, "王五")
    )

    conn.close()

demo_param_query()

"""
要点：
  - 占位符用 ?（SQLite 语法）
  - 参数放在元组里：(value,) ← 单个值也必须加逗号！
  - 永远不要用 f-string / + 拼接用户输入到 SQL 里
"""


# ============================================================
# 第三部分：LIKE 模糊搜索 — 实现关键词查找
# ============================================================

print("\n" + "=" * 60)
print("第三部分：LIKE 模糊搜索")
print("=" * 60)

def demo_like():
    """演示 LIKE 模糊搜索"""
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE s (name TEXT)")
    conn.execute("INSERT INTO s VALUES ('张三')")
    conn.execute("INSERT INTO s VALUES ('张三丰')")
    conn.execute("INSERT INTO s VALUES ('李四')")

    keyword = "张"
    # % 是通配符，匹配任意字符
    # '%张%' = 包含"张"的任意位置
    # '张%'  = 以"张"开头
    # '%张'  = 以"张"结尾

    rows = conn.execute(
        "SELECT * FROM s WHERE name LIKE ?",
        (f"%{keyword}%",)  # 模糊匹配 — 注意 % 我们自己在参数里加
    ).fetchall()

    print(f"搜索 '{keyword}' 的结果: {rows}")
    # 输出: [('张三',), ('张三丰',)]

    conn.close()

demo_like()


# ============================================================
# 第四部分：StudentDB 类设计 — 封装数据访问层
# ============================================================

print("\n" + "=" * 60)
print("第四部分：StudentDB 类设计")
print("=" * 60)

"""
设计思路（参考 Day 9 的 UserDB）：

StudentDB
├── __init__(db_path)       → 初始化，建表
├── add_student(...)        → CREATE，返回新记录的 id
├── get_all_students()      → READ ALL，返回列表
├── search_students(keyword)→ READ with LIKE，模糊搜索
├── update_student(id, ...) → UPDATE，修改指定字段
├── delete_student(id)      → DELETE，删除指定学生
└── count_students()        → 工具方法，统计总数

students 表结构：
┌─────────────┬──────────┬──────────────────────────┐
│ 字段         │ 类型      │ 说明                      │
├─────────────┼──────────┼──────────────────────────┤
│ id          │ INTEGER  │ 自增主键                   │
│ name        │ TEXT     │ 姓名（必填）                │
│ age         │ INTEGER  │ 年龄                       │
│ grade       │ TEXT     │ 班级，如 "2024级1班"        │
│ major       │ TEXT     │ 专业                       │
│ created_at  │ TEXT     │ 创建时间（默认当前时间）     │
└─────────────┴──────────┴──────────────────────────┘
"""

# 4.1 获取当前时间的 Python 写法
from datetime import datetime

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f"当前时间格式化: {now}")
# C++ 对比: std::put_time + std::localtime，Python 一行搞定

# 4.2 表结构 SQL
CREATE_STUDENTS_TABLE = """
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    grade TEXT DEFAULT '',
    major TEXT DEFAULT '',
    created_at TEXT DEFAULT (datetime('now', 'localtime'))
)
"""

# 4.3 动态 UPDATE — 只更新传入的字段
"""
# 当用户可能只修改部分字段时（比如只改 age，不改 name）：
# 我们希望 UPDATE students SET age = ? WHERE id = ?
# 而不是把所有字段都 SET 一遍

# 技巧：用字典 + 动态构建 SQL
def update_student(self, student_id: int, **kwargs):
    # kwargs = {'name': '新名字', 'grade': '新班级'}
    # 动态组装 SET 子句
    fields = ", ".join(f"{k} = ?" for k in kwargs.keys())
    # → "name = ?, grade = ?"

    values = list(kwargs.values())
    values.append(student_id)

    sql = f"UPDATE students SET {fields} WHERE id = ?"
    conn.execute(sql, values)
"""


# ============================================================
# 第五部分：整合 — 带认证的学生管理系统架构
# ============================================================

print("\n" + "=" * 60)
print("第五部分：系统整合思路")
print("=" * 60)

"""
到 Day 10，我们的系统结构是：

main.py (入口)
├── 登录/注册 → 调用 UserDB (Day 9)
│   └── UserDB.register() / .login()
│
└── 学生管理 → 调用 StudentDB (Day 10)
    ├── StudentDB.add_student()
    ├── StudentDB.get_all_students()
    ├── StudentDB.search_students()
    ├── StudentDB.update_student()
    └── StudentDB.delete_student()

用户流程：
  1. 启动 → 显示主菜单（登录 / 注册 / 退出）
  2. 登录成功 → 显示学生管理菜单（增/删/改/查）
  3. 操作完成 → 返回学生管理菜单，直到退出

这就是一个完整的两层 CLI 应用！
"""

print("\n[OK] Day 10 笔记阅读完毕，开始做练习吧！")
print("练习文件: day10_exercise.py")
