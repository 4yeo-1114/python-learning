"""
============================================================
Day 5: 控制流 — if / for / while / break & continue（C++ 对比版）
============================================================
目标：系统掌握 Python 的控制流语句，感受和 C++ 的核心差异
"""

# ============================================================
# 1. if / elif / else — 条件分支
# ============================================================

print("=== 1. if / elif / else ===")

# 基本语法（注意：没有 {}，没有括号！）
score = 85

if score >= 90:
    grade = "A"
elif score >= 80:           # ← Python 用 elif，不是 else if！
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"

print(f"分数 {score} → 等级 {grade}")

# C++ 对比：
# if (score >= 90)      grade = "A";
# else if (score >= 80) grade = "B";   // C++ 是 else if（两个单词）
# else                  grade = "F";

# Python 独有：三目表达式（条件表达式）
# 语法：值1 if 条件 else 值2
age = 18
status = "成年" if age >= 18 else "未成年"
print(f"{age}岁 → {status}")

# C++ 对比：status = (age >= 18) ? "成年" : "未成年";

# 链式比较 — Python 独有，非常易读！
x = 50
if 0 < x < 100:             # 等价于 if x > 0 and x < 100
    print(f"{x} 在 0~100 之间")

# C++ 对比：if (x > 0 && x < 100)  — 不能写成 if (0 < x < 100)


# ============================================================
# 2. for 循环 — 和 C++ 完全不同！
# ============================================================

print("\n=== 2. for 循环 ===")

# Python 的 for 遍历的是"可迭代对象"，不是用计数器
# C++:  for (int i = 0; i < n; i++)
# Python: for item in iterable:

# 2.1 range() — 生成数字序列
print("\n--- range() ---")

# range(stop)       → 0, 1, 2, ..., stop-1
print("range(5):  ", list(range(5)))        # [0, 1, 2, 3, 4]

# range(start, stop) → start, start+1, ..., stop-1
print("range(2,7):", list(range(2, 7)))     # [2, 3, 4, 5, 6]

# range(start, stop, step) → 带步长
print("range(1,10,2):", list(range(1, 10, 2)))  # [1, 3, 5, 7, 9]

# 倒序遍历
print("range(5,0,-1):", list(range(5, 0, -1)))  # [5, 4, 3, 2, 1]

# 最常用：遍历 N 次
for i in range(3):
    print(f"  第 {i+1} 次循环")

# C++ 对比：
# for (int i = 0; i < 3; i++)  →  for i in range(3)
# for (int i = 5; i > 0; i--)  →  for i in range(5, 0, -1)

# 2.2 遍历列表（最 Python 的方式）
print("\n--- 遍历列表 ---")

fruits = ["苹果", "香蕉", "橘子"]

# 方式1：直接遍历元素（推荐！）
for fruit in fruits:
    print(f"  {fruit}", end=" ")
print()

# 方式2：需要索引时用 enumerate()
for i, fruit in enumerate(fruits, 1):   # 从 1 开始编号
    print(f"  {i}. {fruit}")

# 方式3：用 range(len()) — 不推荐，不 Python
# for i in range(len(fruits)):
#     print(fruits[i])

# C++ 对比：
# // C++11 range-based for
# for (const auto& fruit : fruits) { ... }
# // 传统 for
# for (size_t i = 0; i < fruits.size(); i++) { ... }

# 2.3 zip() — 并行遍历多个序列
print("\n--- zip() 并行遍历 ---")

names = ["张三", "李四", "王五"]
scores = [85, 92, 78]
cities = ["北京", "上海", "广州"]

for name, score, city in zip(names, scores, cities):
    print(f"  {name} — {score}分 — {city}")

# C++ 对比：没有内建 zip，需要手动索引或 Boost

# 2.4 遍历字典
print("\n--- 遍历字典 ---")

student = {"name": "张三", "age": 20, "major": "计算机"}

# 遍历键
for key in student:
    print(f"  {key}", end=" ")
print()

# 遍历键和值（推荐）
for key, value in student.items():
    print(f"  {key}: {value}")

# C++ 对比：for (auto& [k, v] : map)  — C++17 结构化绑定


# ============================================================
# 3. while 循环 — 和 C++ 最像的部分
# ============================================================

print("\n=== 3. while 循环 ===")

# 3.1 基本 while（和 C++ 几乎一样）
count = 0
while count < 3:
    print(f"  count = {count}")
    count += 1

# C++ 对比：几乎相同，只是 {} 换成缩进 + 冒号

# 3.2 while True — 无限循环 + break
print("\n--- while True 模式 ---")

# 这是 Python 最常用的循环模式之一！
# C++ 中可能用 while(1) 或 for(;;)

attempt = 0
while True:                 # 无限循环
    attempt += 1
    print(f"  尝试第 {attempt} 次")
    if attempt >= 3:
        print("  → 达到上限，退出")
        break               # 跳出循环


# ============================================================
# 4. break / continue — 循环控制
# ============================================================

print("\n=== 4. break / continue ===")

# 和 C++ 行为完全一样，只是语法略有不同

# break：立即跳出整个循环
print("--- break ---")
for i in range(10):
    if i == 4:
        print(f"  遇到 {i}，break！")
        break
    print(f"  {i}", end=" ")
print()

# continue：跳过本次迭代，进入下一次
print("\n--- continue ---")
for i in range(1, 8):
    if i % 2 == 0:            # 跳过偶数
        continue
    print(f"  {i}", end=" ")  # 只打印奇数
print()

# Python 独有：for/while 可以带 else！
print("\n--- for...else（Python 独有！） ---")

# else 在循环正常结束（没有被 break 打断）时执行
# 常用于"查找"场景

def find_student(name, students):
    """在列表中查找学生，演示 for...else"""
    for s in students:
        if s == name:
            print(f"  找到了：{name}")
            break
    else:                       # 注意缩进！else 属于 for，不是 if
        print(f"  没找到：{name}")

find_student("张三", ["李四", "王五", "赵六"])
find_student("张三", ["李四", "张三", "王五"])

# C++ 对比：C++ 没有 for...else，需要用 bool 标志位模拟


# ============================================================
# 5. pass 语句 — 占位符
# ============================================================

print("\n=== 5. pass 语句 ===")

# pass 什么都不做，用于占位
# 当你还没想好函数/类/if 里面写什么时，用 pass 避免语法错误

def todo_function():
    pass           # TODO: 以后实现

if True:
    pass           # 什么都不做，但语法正确

# C++ 对比：C++ 中空函数体写 {} 即可，不需要占位符


# ============================================================
# 6. 实战：猜数字游戏（逻辑拆解）
# ============================================================

print("\n=== 6. 猜数字游戏 — 逻辑拆解 ===")

import random

target = random.randint(1, 100)   # 生成 1~100 之间的随机数
guess = None
attempts = 0
MAX_ATTEMPTS = 7

print(f"我已想好一个 1~100 的数，你有 {MAX_ATTEMPTS} 次机会！")

# 下面是游戏逻辑骨架（完整版在练习里写）
# while attempts < MAX_ATTEMPTS:
#     guess = int(input("猜一个数: "))
#     attempts += 1
#     if guess == target:
#         print(f"对了！用了 {attempts} 次")
#         break
#     elif guess < target:
#         print("太小了！")
#     else:
#         print("太大了！")
# else:
#     print(f"机会用完了！答案是 {target}")


# ============================================================
# C++ → Python 速查表（控制流）
# ============================================================
"""
┌──────────────────────────┬───────────────────────────────┬────────────────────────────┐
│ 概念                      │ C++                            │ Python                     │
├──────────────────────────┼───────────────────────────────┼────────────────────────────┤
│ if-else if-else          │ if/else if/else                │ if/elif/else               │
│ 三目运算符                │ x > 0 ? "正" : "负"            │ "正" if x > 0 else "负"    │
│ 链式比较                  │ if (x>0 && x<100)              │ if 0 < x < 100             │
│ 计数 for                 │ for (int i=0; i<n; i++)        │ for i in range(n)          │
│ 遍历容器                  │ for (auto& x : vec)            │ for x in list              │
│ 带索引遍历                │ for (int i=0;i<n;i++)          │ for i,x in enumerate(lst)  │
│ 并行遍历                  │ 手动索引                       │ for a,b in zip(A,B)        │
│ while                    │ while (cond) {...}              │ while cond:                │
│ 无限循环                  │ while(1)/for(;;)               │ while True:                │
│ break / continue         │ break; / continue;             │ break / continue           │
│ for...else               │ 无（需标志位模拟）               │ for item in X: ... else:   │
│ 空语句                    │ ; 或 {}                        │ pass                       │
└──────────────────────────┴───────────────────────────────┴────────────────────────────┘
"""

print("\n[OK] Day 5 笔记结束！打开 day05_exercise.py 做练习吧。")
