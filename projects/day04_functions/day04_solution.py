"""
============================================================
Day 4 参考答案：函数进阶 + lambda + 作用域
============================================================
做完练习后再看哦！
"""

# ============================================================
# 练习 1：灵活的函数参数 — 格式化输出工具
# ============================================================

print("=== 练习 1：格式化输出工具 ===\n")

def print_table(title, headers, *rows, align="left"):
    """打印格式化表格"""
    # 计算每列的最大宽度（标题也要考虑）
    col_widths = []
    for i, header in enumerate(headers):
        # 该列所有数据项的最大宽度
        max_w = len(header)  # 至少和标题一样宽
        for row in rows:
            if i < len(row):
                max_w = max(max_w, len(str(row[i])))
        col_widths.append(max_w)

    # 打印标题
    print(f"=== {title} ===")

    # 打印表头
    header_parts = []
    for i, header in enumerate(headers):
        if align == "left":
            header_parts.append(f"{header:<{col_widths[i]}}")
        else:
            header_parts.append(f"{header:^{col_widths[i]}}")
    print(" | ".join(header_parts))

    # 打印分隔线
    print("-" * (sum(col_widths) + 3 * (len(headers) - 1)))

    # 打印数据行
    for row in rows:
        row_parts = []
        for i, cell in enumerate(row):
            cell_str = str(cell) if i < len(row) else ""
            if align == "left":
                row_parts.append(f"{cell_str:<{col_widths[i]}}")
            else:
                row_parts.append(f"{cell_str:^{col_widths[i]}}")
        print(" | ".join(row_parts))

    # 打印结尾
    print("=" * (sum(col_widths) + 3 * (len(headers) - 1) + 4))
    print()


print_table("学生列表", ["姓名", "年龄"], ("张三", 20), ("李四", 22), ("王五", 19))

print_table("成绩表", ["姓名", "语文", "数学", "英语"],
            ("张三", 85, 92, 78),
            ("李四", 90, 88, 95),
            align="left")


# ============================================================
# 练习 2：lambda + sorted + map — 学生成绩处理
# ============================================================

print("=== 练习 2：学生成绩处理 ===\n")

students = [
    {"name": "张三", "math": 85, "english": 78, "python": 92},
    {"name": "李四", "math": 92, "english": 88, "python": 85},
    {"name": "王五", "math": 78, "english": 95, "python": 80},
    {"name": "赵六", "math": 90, "english": 72, "python": 88},
]

# 任务 a：按 python 成绩从高到低排序，只打印名字
print("--- a) 按 Python 成绩排序 ---")
sorted_by_python = sorted(students, key=lambda s: s["python"], reverse=True)
print([s["name"] for s in sorted_by_python])

# 任务 b：计算总分并排序
print("\n--- b) 按总分排序 ---")
# 方法1：用列表推导式（推荐）
total_scores = [
    (s["name"], s["math"] + s["english"] + s["python"])
    for s in students
]
total_scores.sort(key=lambda x: x[1], reverse=True)
for name, total in total_scores:
    print(f"  {name}: {total}分")

# 方法2：用 map（函数式风格，了解一下即可）
# total_scores2 = list(map(
#     lambda s: (s["name"], s["math"] + s["english"] + s["python"]),
#     students
# ))

# 任务 c：所有科目都 >= 80 分
print("\n--- c) 全科 80+ ---")
all_pass = [s["name"] for s in students
            if all(score >= 80 for score in [s["math"], s["english"], s["python"]])]
print(f"全科 80 分以上: {all_pass}")

# 另一种写法（更通用，适用于科目数量可变的情况）：
all_pass2 = []
for s in students:
    scores = [s["math"], s["english"], s["python"]]
    if all(score >= 80 for score in scores):
        all_pass2.append(s["name"])
print(f"验证: {all_pass2}")

print()


# ============================================================
# 练习 3：作用域与闭包 — 计数器工厂
# ============================================================

print("=== 练习 3：计数器工厂 ===\n")

def make_counter(start=0, step=1):
    """返回一个每次调用递增的计数器函数"""
    count = start - step    # 第一次调用时变成 start

    def counter():
        nonlocal count       # 声明要修改外层函数的 count
        # 注意：如果只是读取 count（不赋值），不需要 nonlocal
        # 但因为 count += step 包含赋值操作，所以必须声明
        nonlocal count
        count += step
        return count

    return counter


# 测试
c1 = make_counter()
print(f"c1(): {c1()}")  # 0
print(f"c1(): {c1()}")  # 1
print(f"c1(): {c1()}")  # 2

c2 = make_counter(100, 10)
print(f"c2(): {c2()}")  # 100
print(f"c2(): {c2()}")  # 110
print(f"c2(): {c2()}")  # 120

# c1 不受 c2 影响（每个闭包有自己独立的 count）
print(f"c1() 还是: {c1()}")  # 3

print()


# ============================================================
# 练习 4（综合）：文件版学生成绩分析器
# ============================================================

print("=== 练习 4：学生成绩分析器 ===\n")

def load_scores(filename):
    """从文件读取成绩数据"""
    students = []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(",")
                if len(parts) >= 4:
                    students.append({
                        "name": parts[0],
                        "math": int(parts[1]),
                        "english": int(parts[2]),
                        "python": int(parts[3]),
                    })
        print(f"[加载] 从 {filename} 读取了 {len(students)} 条记录")
    except FileNotFoundError:
        print(f"[提示] {filename} 不存在，返回空列表")
    except ValueError:
        print(f"[错误] {filename} 格式有问题")
    return students


def analyze(students):
    """分析成绩数据，返回分析结果字典"""
    if not students:
        print("[提示] 没有学生数据可以分析")
        return {}

    total = len(students)

    # 计算各科平均分
    avg_math = sum(s["math"] for s in students) / total
    avg_english = sum(s["english"] for s in students) / total
    avg_python = sum(s["python"] for s in students) / total


    # 总分最高的学生
    top_student = max(students, key=lambda s: s["math"] + s["english"] + s["python"])

    # 所有科目都及格的人数
    all_pass_count = sum(
        1 for s in students
        if all(score >= 60 for score in [s["math"], s["english"], s["python"]])
    )

    result = {
        "total": total,
        "avg_math": round(avg_math, 1),
        "avg_english": round(avg_english, 1),
        "avg_python": round(avg_python, 1),
        "top_student": top_student["name"],
        "all_pass": all_pass_count,
    }

    # 打印分析报告
    print("\n" + "=" * 30)
    print("      📊 成绩分析报告")
    print("=" * 30)
    print(f"  总人数:        {result['total']}")
    print(f"  数学平均分:    {result['avg_math']}")
    print(f"  英语平均分:    {result['avg_english']}")
    print(f"  Python 平均分: {result['avg_python']}")
    print(f"  总分第一名:    {result['top_student']}")
    print(f"  全科及格人数:  {result['all_pass']}")
    print("=" * 30 + "\n")

    return result


def save_report(analysis, filename):
    """把分析结果保存到文件"""
    if not analysis:
        print("[提示] 没有分析结果可以保存")
        return

    with open(filename, "w", encoding="utf-8") as f:
        f.write("=== 成绩分析报告 ===\n")
        f.write(f"总人数: {analysis['total']}\n")
        f.write(f"数学平均分: {analysis['avg_math']}\n")
        f.write(f"英语平均分: {analysis['avg_english']}\n")
        f.write(f"Python 平均分: {analysis['avg_python']}\n")
        f.write(f"总分第一名: {analysis['top_student']}\n")
        f.write(f"全科及格人数: {analysis['all_pass']}\n")
    print(f"[保存] 报告已保存到 {filename}")


def main():
    """主流程"""
    # 1. 先创建测试数据文件
    test_data = """张三,85,78,92
李四,92,88,85
王五,78,95,80
赵六,90,72,88
钱七,55,61,70
孙八,88,90,94"""

    data_file = "day04_scores.txt"
    with open(data_file, "w", encoding="utf-8") as f:
        f.write(test_data)
    print(f"[创建] 测试数据已写入 {data_file}")

    # 2. 加载 → 分析 → 保存
    students = load_scores(data_file)
    result = analyze(students)
    save_report(result, "day04_report.txt")

    # 3. 验证报告文件内容
    print("\n--- 报告文件内容预览 ---")
    try:
        with open("day04_report.txt", "r", encoding="utf-8") as f:
            print(f.read())
    except FileNotFoundError:
        print("报告文件不存在")


# 运行主流程
if __name__ == "__main__":
    main()

print("\n[Congrats!] Day 4 练习完成！")
