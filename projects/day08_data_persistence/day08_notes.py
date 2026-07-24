"""
============================================================
Day 8: 数据持久化 — JSON + CSV + SQLite（C++ 对比版）
============================================================
目标：掌握 Python 三大数据持久化方案，为后续学生管理系统打基础
       Week 3 正式开始！
"""

# ============================================================
# 第一部分：JSON — 轻量级数据交换格式
# ============================================================

print("=" * 60)
print("第一部分：JSON（JavaScript Object Notation）")
print("=" * 60)

# 1.1 什么是 JSON？为什么用？
# JSON = 一种用纯文本表示结构化数据的格式
# 特点：人类可读、语言无关、几乎所有语言都支持

# Python 类型 ↔ JSON 类型 对照表：
"""
┌──────────────┬─────────────┐
│ Python       │ JSON        │
├──────────────┼─────────────┤
│ dict         │ object      │
│ list/tuple   │ array       │
│ str          │ string      │
│ int/float    │ number      │
│ True/False   │ true/false  │
│ None         │ null        │
└──────────────┴─────────────┘
"""

# 1.2 json.dumps() — Python 对象 → JSON 字符串（序列化）
print("\n=== 1.2 json.dumps() — 序列化 ===")
import json

# 一个典型的 Python 数据结构
student = {
    "name": "张三",
    "age": 20,
    "scores": [85, 92, 78],
    "is_active": True,
    "address": None,
}

# 序列化为 JSON 字符串
json_str = json.dumps(student)
print(f"默认（无格式化）:\n{json_str}")

# 美化输出（indent 参数）
json_pretty = json.dumps(student, indent=2)
print(f"\n美化输出（indent=2）:\n{json_pretty}")

# 处理中文（ensure_ascii=False）
chinese_data = {"姓名": "张三", "城市": "北京"}
print(f"\nensure_ascii=True（默认）: {json.dumps(chinese_data)}")
print(f"ensure_ascii=False:         {json.dumps(chinese_data, ensure_ascii=False)}")
# [!] 不加 ensure_ascii=False 中文会变成 \uXXXX 转义序列！

# 排序键（sort_keys=True）
print(f"\nsort_keys=True:\n{json.dumps(student, indent=2, sort_keys=True, ensure_ascii=False)}")


# 1.3 json.loads() — JSON 字符串 → Python 对象（反序列化）
print("\n=== 1.3 json.loads() — 反序列化 ===")

json_string = '{"name": "李四", "age": 22, "scores": [90, 88, 95]}'
data = json.loads(json_string)
print(f"类型: {type(data)}")             # <class 'dict'>
print(f"姓名: {data['name']}")
print(f"年龄: {data['age']}")
print(f"成绩: {data['scores']}")

# C++ 对比：
# C++ 需要引入第三方库（如 nlohmann/json）或手动解析字符串
# nlohmann::json j = nlohmann::json::parse(json_string);
# Python 内置 json 模块，一行搞定！


# 1.4 json.dump() / json.load() — 直接读写文件
print("\n=== 1.4 json.dump() / json.load() — 文件读写 ===")

# 写入 JSON 文件
users = [
    {"id": 1, "name": "张三", "role": "admin"},
    {"id": 2, "name": "李四", "role": "student"},
    {"id": 3, "name": "王五", "role": "student"},
]

with open("users.json", "w", encoding="utf-8") as f:
    json.dump(users, f, indent=2, ensure_ascii=False)
print("已写入 users.json")

# 读取 JSON 文件
with open("users.json", "r", encoding="utf-8") as f:
    loaded_users = json.load(f)
print(f"从文件读取: {loaded_users}")
print(f"第一个用户: {loaded_users[0]['name']}")

# 技巧记忆：
# dumps / loads → 带 s 的是处理"字符串"（string）
# dump  / load  → 不带 s 的是处理"文件"（file pointer）


# 1.5 自定义 JSON 编码器
print("\n=== 1.5 自定义 JSON 编码器 ===")

from datetime import datetime

# 问题：datetime 对象不能直接序列化
now = datetime.now()
# json.dumps(now)  # TypeError: Object of type datetime is not JSON serializable

# 解决方案1：自定义 encoder（继承 JSONEncoder）
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        return super().default(obj)

data_with_time = {"event": "登录", "time": now}
json_with_time = json.dumps(data_with_time, cls=DateTimeEncoder, ensure_ascii=False)
print(f"自定义编码器: {json_with_time}")

# 解决方案2：default 参数（更简洁）
json_with_time2 = json.dumps(
    data_with_time,
    default=lambda obj: obj.strftime("%Y-%m-%d %H:%M:%S") if isinstance(obj, datetime) else obj,
    ensure_ascii=False
)
print(f"default 参数:  {json_with_time2}")


# 1.6 JSON 实际应用场景
print("\n=== 1.6 应用场景 ===")
print("1. Web API 数据传输（前后端通信）")
print("2. 配置文件（如 package.json, settings.json）")
print("3. 程序间数据交换（语言无关）")
print("4. 数据存储（小规模、需要人类可读性）")
print("5. 日志文件（结构化日志）")


# ============================================================
# 第二部分：CSV — 表格数据处理
# ============================================================

print("\n" + "=" * 60)
print("第二部分：CSV（Comma-Separated Values）")
print("=" * 60)

import csv

# 2.1 什么是 CSV？
# CSV = 用逗号分隔值的纯文本表格格式
# Excel 可以直接打开，是最通用的表格交换格式
# 每一行是一条记录，每个字段用逗号分隔
"""
示例 CSV 内容：
姓名,年龄,成绩
张三,20,85
李四,22,92
王五,21,78
"""

# 2.2 csv.writer — 写入 CSV 文件
print("\n=== 2.2 csv.writer — 写入 CSV ===")

# 准备数据：学生成绩表
students_data = [
    ["姓名", "年龄", "语文", "数学", "英语"],          # 表头
    ["张三", 20, 85, 92, 78],
    ["李四", 22, 90, 88, 95],
    ["王五", 21, 78, 85, 82],
    ["赵六", 20, 92, 95, 90],
]

with open("students.csv", "w", newline="", encoding="utf-8-sig") as f:
    # newline="" 防止 Windows 下出现多余空行
    # utf-8-sig 加了 BOM，让 Excel 能正确识别中文
    writer = csv.writer(f) #writer = csv.writer(f)
    writer.writerows(students_data)     # 一次写入多行
    # 也可以用 writer.writerow(row) 逐行写入
print("已写入 students.csv（可用 Excel 打开）")


# 2.3 csv.reader — 读取 CSV 文件
print("\n=== 2.3 csv.reader — 读取 CSV ===")

with open("students.csv", "r", encoding="utf-8-sig") as f:
    reader = csv.reader(f) #reader = csv.reader(f)
    for row in reader:
        print(f"  {row}")

# 跳过表头
print("\n跳过表头读取:")
with open("students.csv", "r", encoding="utf-8-sig") as f:
    reader = csv.reader(f)
    header = next(reader)               # 先读表头
    print(f"表头: {header}")
    for row in reader:
        print(f"  数据行: {row}")


# 2.4 csv.DictWriter / DictReader — 字典方式（推荐！）
print("\n=== 2.4 DictWriter / DictReader — 字典方式 ===")
# 使用字典方式更直观，不容易搞错列顺序

# DictWriter 写入
fieldnames = ["name", "age", "score"]

with open("students_dict.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()                # 写入表头
    writer.writerow({"name": "张三", "age": 20, "score": 85})
    writer.writerow({"name": "李四", "age": 22, "score": 92})
    writer.writerow({"name": "王五", "age": 21, "score": 78})
print("已写入 students_dict.csv")

# DictReader 读取
print("DictReader 读取:")
with open("students_dict.csv", "r", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        # row 是一个 OrderedDict / dict，键是表头
        print(f"  {row['name']}, {row['age']}岁, 成绩={row['score']}")



# 2.5 CSV 应用场景
print("\n=== 2.5 CSV 应用场景 ===")
print("1. 导出数据给 Excel 用户")
print("2. 批量导入数据到数据库")
print("3. 数据分析和报表的中间格式")
print("4. 与其他系统（如财务软件）的数据交换")
print("5. 日志和监控数据导出")


# C++ 对比：
# C++ 没有内置 CSV 库，需要手动 parse 或用第三方
# Python csv 模块内置，DictReader/DictWriter 特别方便


# ============================================================
# 第三部分：SQLite — 嵌入式关系型数据库
# ============================================================

print("\n" + "=" * 60)
print("第三部分：SQLite — 轻量级数据库")
print("=" * 60)

# 3.1 什么是 SQLite？
# SQLite = 一个不需要服务器的、零配置的、嵌入式的 SQL 数据库
# 整个数据库就是一个 .db 文件，不需要安装 MySQL/PostgreSQL
# Python 标准库内置 sqlite3 模块，开箱即用！

# SQLite vs 其他数据库：
"""
┌──────────────────┬─────────────────────┬───────────────────────┐
│ 特性              │ SQLite               │ MySQL/PostgreSQL       │
├──────────────────┼─────────────────────┼───────────────────────┤
│ 安装配置          │ 无需（库内嵌）        │ 需要安装服务端          │
│ 数据库文件        │ 单个 .db 文件         │ 多个文件/目录           │
│ 并发写入          │ 单写（锁整个库）       │ 多写（行级锁）          │
│ 适用场景          │ 桌面应用/手机/嵌入式   │ Web 服务/高并发         │
│ 数据量            │ TB 级别也没问题        │ TB 级别也没问题         │
│ 网络访问          │ 不支持（本地文件）     │ 支持（TCP/IP）          │
└──────────────────┴─────────────────────┴───────────────────────┘
"""

# 对于学生管理系统（单机桌面应用），SQLite 是最佳选择！


# 3.2 创建数据库连接和游标
print("\n=== 3.2 连接数据库 + 创建表 ===")
import sqlite3

# 连接数据库（如果文件不存在会自动创建）
conn = sqlite3.connect("school.db")
print(f"已连接 school.db，类型: {type(conn)}")

# 创建游标（cursor = 执行 SQL 的"笔"）
cursor = conn.cursor()
print(f"游标: {type(cursor)}")

# 创建表
cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER,
        grade TEXT DEFAULT '未分班',
        score REAL DEFAULT 0.0
    )
""")
print("表 students 已创建（或已存在）")



# 3.3 CRUD 操作 — 增删改查
print("\n=== 3.3 CRUD 操作 ===")

# --- CREATE（插入数据）---
print("--- 插入数据 ---")

# 方法1：用 ? 占位符（推荐，防 SQL 注入）
cursor.execute(
    "INSERT INTO students (name, age, grade, score) VALUES (?, ?, ?, ?)",
    ("张三", 20, "一班", 85.5)
)

# 方法2：批量插入
new_students = [
    ("李四", 22, "一班", 92.0),
    ("王五", 21, "二班", 78.5),
    ("赵六", 20, "二班", 88.0),
    ("孙七", 23, "一班", 95.5),
]
cursor.executemany(
    "INSERT INTO students (name, age, grade, score) VALUES (?, ?, ?, ?)",
    new_students
)
print(f"插入了 {cursor.rowcount} 条记录（最后批量）")

# [!] 为什么用 ? 而不是 f-string？
# 错误写法：f"INSERT INTO students VALUES ('{name}', {age})"
# 危险！如果 name = "'); DROP TABLE students; --" → SQL 注入攻击
# 正确写法：用 ? 占位符，sqlite3 会自动转义

# 提交事务（SQLite 默认需要手动提交）
conn.commit()
print("事务已提交")


# --- READ（查询数据）---
print("\n--- 查询数据 ---")

# 查询所有记录
cursor.execute("SELECT * FROM students")
all_students = cursor.fetchall()
print("所有学生:")
for row in all_students:
    print(f"  {row}")

# 条件查询
cursor.execute("SELECT name, score FROM students WHERE score >= ?", (90,))
print("\n成绩 >= 90 的学生:")
for row in cursor.fetchall():
    print(f"  {row}")

# 查询单条
cursor.execute("SELECT * FROM students WHERE name = ?", ("张三",))
zhang_san = cursor.fetchone()
print(f"\n张三: {zhang_san}")

# fetchmany(n) — 分批获取
cursor.execute("SELECT * FROM students ORDER BY score DESC")
top3 = cursor.fetchmany(3)
print(f"\n成绩前3名（fetchmany(3)）:")
for row in top3:
    print(f"  {row}")


# --- UPDATE（更新数据）---
print("\n--- 更新数据 ---")

cursor.execute(
    "UPDATE students SET score = ? WHERE name = ?",
    (99.0, "张三")
)
print(f"更新了 {cursor.rowcount} 条记录")
conn.commit()


# --- DELETE（删除数据）---
print("\n--- 删除数据 ---")

cursor.execute("DELETE FROM students WHERE name = ?", ("赵六",))
print(f"删除了 {cursor.rowcount} 条记录")
conn.commit()

# 验证
cursor.execute("SELECT name, score FROM students")
print("当前数据:")
for row in cursor.fetchall():
    print(f"  {row}")


# 3.4 使用 with 语句（上下文管理器）
print("\n=== 3.4 使用 with 语句 ===")
# conn 支持上下文管理器，退出时自动 commit 或 rollback

def add_student_safe(name, age, grade, score):
    """安全添加学生，出错自动回滚"""
    with sqlite3.connect("school.db") as conn:
        conn.execute(
            "INSERT INTO students (name, age, grade, score) VALUES (?, ?, ?, ?)",
            (name, age, grade, score)
        )
    # 正常退出自动 commit，抛异常自动 rollback

add_student_safe("周八", 19, "三班", 76.0)
print("通过 with 语句添加成功")


# 3.5 行工厂 — 让查询结果更像字典
print("\n=== 3.5 行工厂 — Row Factory ===")

# 默认：查询结果是 tuple → row[0], row[1] 不直观
# 改进：用 Row factory → row["name"], row["score"] 很直观

conn.row_factory = sqlite3.Row      # 设置行工厂
cursor = conn.cursor()

cursor.execute("SELECT name, age, grade, score FROM students WHERE score >= ?", (80,))
print("成绩 >= 80 的学生（字典风格访问）:")
for row in cursor.fetchall():
    print(f"  {row['name']}, {row['age']}岁, {row['grade']}, {row['score']}分")

# 也可以转为普通 dict
cursor.execute("SELECT * FROM students WHERE name = ?", ("张三",))
row = cursor.fetchone()
if row:
    print(f"\n张三（转为 dict）: {dict(row)}")


# 3.6 WHERE 子句 + ORDER BY + LIMIT
print("\n=== 3.6 常用 SQL 查询 ===")

# 排序 + 限制
cursor.execute("""
    SELECT name, age, score
    FROM students
    ORDER BY score DESC
    LIMIT 3
""")
print("成绩 Top 3:")
for row in cursor.fetchall():
    print(f"  {dict(row)}")

# 模糊搜索
cursor.execute("SELECT name, grade FROM students WHERE name LIKE ?", ("%三%",))
print("\n名字含'三'的:")
for row in cursor.fetchall():
    print(f"  {dict(row)}")


# 3.7 完整示例：一个简单的学生数据访问层
print("\n=== 3.7 完整示例：学生数据访问层 ===")

class StudentDB:
    """学生数据库操作类 — 封装常见的 CRUD 操作"""

    def __init__(self, db_path="school.db"):
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
                    grade TEXT DEFAULT '未分班',
                    score REAL DEFAULT 0.0
                )
            """)

    def add(self, name, age, grade="未分班", score=0.0):
        """添加学生"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO students (name, age, grade, score) VALUES (?, ?, ?, ?)",
                (name, age, grade, score)
            )

    def get_all(self):
        """获取所有学生"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute("SELECT * FROM students ORDER BY id").fetchall()
            return [dict(r) for r in rows]

    def get_by_name(self, name):
        """按姓名查找"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(
                "SELECT * FROM students WHERE name = ?", (name,)
            ).fetchone()
            return dict(row) if row else None

    def update_score(self, name, new_score):
        """更新成绩"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "UPDATE students SET score = ? WHERE name = ?",
                (new_score, name)
            )

    def delete(self, name):
        """删除学生"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM students WHERE name = ?", (name,))

    def get_top(self, n=3):
        """成绩前 N 名"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT * FROM students ORDER BY score DESC LIMIT ?", (n,)
            ).fetchall()
            return [dict(r) for r in rows]


# 使用 StudentDB
db = StudentDB("school.db")

print("当前所有学生:")
for s in db.get_all():
    print(f"  {s['name']}: {s['score']}分, {s['grade']}")

print(f"\n张三的信息: {db.get_by_name('张三')}")

print("\n成绩 Top 3:")
for s in db.get_top(3):
    print(f"  {s['name']}: {s['score']}分")


# 3.8 SQLite 数据类型速查
print("\n=== 3.8 SQLite 数据类型 ===")
"""
SQLite 有 5 种存储类型（动态类型，列不强制类型！）：
┌───────────┬────────────────────────────────────┐
│ 类型       │ 说明                                │
├───────────┼────────────────────────────────────┤
│ NULL      │ 空值                                │
│ INTEGER   │ 整数（1, 2, 3, 4, 6, 8 字节自动选） │
│ REAL      │ 浮点数（8 字节 IEEE 754）            │
│ TEXT      │ 字符串（UTF-8 / UTF-16BE / UTF-16LE）│
│ BLOB      │ 二进制数据，原样存储                  │
└───────────┴────────────────────────────────────┘

注意：SQLite 是动态类型的！你可以在 INTEGER 列插入 TEXT
     （实际开发中不要这样做，保持数据一致性）
"""


# ============================================================
# 三种持久化方案对比
# ============================================================

print("\n" + "=" * 60)
print("三种方案对比")
print("=" * 60)

"""
┌──────────┬──────────┬───────────┬──────────────┬──────────────────┐
│ 方案      │ 格式      │ 人类可读    │ 查询能力      │ 适用场景          │
├──────────┼──────────┼───────────┼──────────────┼──────────────────┤
│ JSON     │ 文本      │ ✅ 很好     │ ❌ 无         │ 配置、API、小数据  │
│ CSV      │ 文本      │ ✅ 很好     │ ❌ 无         │ 表格导出、Excel    │
│ SQLite   │ 二进制    │ ❌ 需要工具  │ ✅ 完整 SQL   │ 应用数据、查询频繁  │
└──────────┴──────────┴───────────┴──────────────┴──────────────────┘

选择建议：
- 配置文件 → JSON
- 数据导出/报表 → CSV
- 应用数据（增删改查多）→ SQLite
- 学生管理系统 → SQLite 为主 + CSV 导出功能
"""


# ============================================================
# C++ → Python 速查表（Day 8 主题）
# ============================================================
"""
┌──────────────────────┬───────────────────────────────────┬──────────────────────────────┐
│ 概念                  │ C++                                │ Python                       │
├──────────────────────┼───────────────────────────────────┼──────────────────────────────┤
│ JSON 解析            │ nlohmann/json 等第三方库             │ import json（内置）           │
│ JSON 序列化           │ j.dump() / j.dumps()               │ json.dumps(obj)              │
│ JSON 反序列化         │ json::parse(str)                   │ json.loads(str)              │
│ CSV 读写             │ 手动解析 或 第三方库                  │ import csv（内置）            │
│ CSV 字典模式          │ 需自己实现                          │ csv.DictReader/DictWriter    │
│ 数据库               │ SQLite C API / ODBC                 │ import sqlite3（内置）        │
│ SQL 占位符            │ ? 或 $1（视库而定）                  │ ?（推荐）或 :name（命名参数）   │
│ 事务控制              │ BEGIN/COMMIT/ROLLBACK（手动）        │ conn.commit() / conn.rollback()│
│ 上下文管理器           │ RAII（析构函数）                     │ with 语句                     │
└──────────────────────┴───────────────────────────────────┴──────────────────────────────┘
"""

# ============================================================
# 常见问题解答（Q&A）
# ============================================================
print("\n" + "=" * 60)
print("常见问题解答")
print("=" * 60)

# Q1: JSON、CSV、SQLite 该选哪个？
print("\n--- Q1: 该选哪个？ ---")
print("记住：JSON 给人看，CSV 给 Excel 看，SQLite 给程序看")
print("学生管理系统：主数据存 SQLite，导出报表用 CSV，配置用 JSON")

# Q2: SQLite 能处理多少数据？
print("\n--- Q2: SQLite 能处理多少数据？ ---")
print("SQLite 官方说支持 140 TB 的数据库文件")
print("单表几百万行毫无压力，做好索引即可")
print("对于我们的学生管理系统，绰绰有余")

# Q3: 为什么 SQL 参数要用 ? 而不是 f-string？
print("\n--- Q3: 参数化查询 vs 字符串拼接 ---")
print("安全：f'...{name}...' → name='; DROP TABLE students; -- → SQL 注入")
print("性能：? 占位符允许 SQLite 缓存查询计划")
print("简洁：不需要手动处理引号转义")
print("记住：永远不要用字符串拼接构造 SQL！")

# Q4: cursor.fetchall() vs fetchone() vs fetchmany()？
print("\n--- Q4: fetch 方法选择 ---")
print("fetchone()  → 取一行，返回 tuple 或 None")
print("fetchmany(n)→ 取 n 行，返回 list（结果不够 n 行就返回实际数量）")
print("fetchall()  → 取全部，大数据量时小心内存！")
print("大数据量时用 for row in cursor 逐行迭代（cursor 本身可迭代！）")

# Q5: json.dumps 和 json.dump 的区别？
print("\n--- Q5: dumps vs dump ---")
print("有 s → 处理 String（字符串）：json.dumps(obj) 返回 str")
print("无 s → 处理 File（文件）：json.dump(obj, f) 写入文件")
print("loads/load 同理")

# Q6: 中文变成 \uXXXX 是什么编码？
print("\n--- Q6: \\uXXXX 是什么？ ---")
print("\\uXXXX 是 Unicode 转义序列（Unicode Escape Sequence）")
print("例如：'张' → \\u5f20，'三' → \\u4e09")
print("\\u 后面跟 4 位十六进制数，表示一个 Unicode 码点")
print("")
print("这是 JSON 标准规定的：JSON 字符串中非 ASCII 字符")
print("可以用 \\uXXXX 形式表示，保证所有系统都能正确传输")
print("")
print("Python 的 json.dumps() 默认 ensure_ascii=True：")
print("  中文 → 自动转成 \\uXXXX（ASCII 安全，但人类读不了）")
print("  ensure_ascii=False → 保留原始中文（人类可读）")
print("")
print("示例：")
print("  json.dumps({'姓名':'张三'})")
print("  → '{\"\\u59d3\\u540d\": \"\\u5f20\\u4e09\"}'  # 人读不了")
print("  json.dumps({'姓名':'张三'}, ensure_ascii=False)")
print("  → '{\"姓名\": \"张三\"}'                      # 人可读")
print("")
print("建议：存文件/打印日志时加 ensure_ascii=False")
print("      网络传输时用默认值（兼容性好）")

# Q7: sort_keys=True 按什么排序？
print("\n--- Q7: sort_keys 按什么排序？ ---")
print("按字典 key 的字符串字典序（lexicographic order），")
print("即逐个字符比较 Unicode 码点值。不是按你定义 key 的先后顺序！")
print("")
print("示例：")
data = {"c": 3, "a": 1, "b": 2}
print(f"  原始定义顺序: {list(data.keys())}")
print(f"  实际可能为:    {list(data.keys())}  # Python 3.7+ 保留插入顺序")
print(f"  sort_keys=True: {json.dumps(data, sort_keys=True)}")
print("  → {\"a\": 1, \"b\": 2, \"c\": 3}  # a < b < c 字典序")
print("")
print("数字 key 也按字符串比较（'10' < '2'，因为 '1' < '2'）：")
data2 = {"2": "b", "10": "a"}
print(f"  sort_keys=True: {json.dumps(data2, sort_keys=True)}")
print("  → {\"10\": \"a\", \"2\": \"b\"}   # '1' < '2'，所以 '10' 排前面")
print("")
print("为什么要用？")
print("  - 输出稳定可复现（版本控制 diff 友好）")
print("  - 方便肉眼查找 key")
print("  - 测试断言时不用管 key 顺序")

# Q8: 为什么 execute() 参数里 (90,) 要加逗号？
print("\n--- Q8: 为什么 (90,) 要加逗号？ ---")
print("因为 Python 语法：(90) 不是元组，只是带括号的整数 90")
print("")
print("  type((90))   → <class 'int'>   # 括号只是分组！")
print("  type((90,))  → <class 'tuple'>  # 逗号才表示元组")
print("")
print("sqlite3 的 execute(sql, params) 要求第二个参数是")
print("可迭代对象（tuple 或 list），用来按顺序替换 SQL 中的 ?")
print("")
print("  # [X] 错误写法")
print("  cursor.execute('SELECT ... WHERE score >= ?', (90))")
print("  # (90) → int，不是可迭代对象")
print("  # sqlite3 会尝试 for val in 90: ... → TypeError!")
print("")
print("  # [OK] 正确写法")
print("  cursor.execute('SELECT ... WHERE score >= ?', (90,))")
print("  # (90,) → 单元素元组，可迭代，产出 90")
print("")
print("同理：")
print("  execute(sql, ('张三',))       # 单个字符串参数")
print("  execute(sql, ('张三', 20))    # 多个参数")
print("  execute(sql, ['张三'])        # 用 list 也行，但 tuple 更常见")
print("")
print("记忆技巧：元组的灵魂是逗号，不是括号！")

print("\n[OK] Day 8 笔记结束！打开 day08_exercise.py 做练习吧。")
print("清理临时文件...")

# 清理练习中创建的临时文件（保留 school.db 供练习使用）
import os
for temp_file in ["users.json", "students.csv", "students_dict.csv"]:
    try:
        os.remove(temp_file)
    except FileNotFoundError:
        pass
print("临时文件已清理")
