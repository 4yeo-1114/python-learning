"""
============================================================
Day 4: 函数进阶 + 内置函数 + 作用域（C++ 对比版）
============================================================
目标：掌握 Python 函数的特殊能力——这些是 C++ 没有或差别很大的地方！
"""

# ============================================================
# 1. 函数参数进阶 — Python 的参数灵活性远超 C++
# ============================================================

print("=== 1. 函数参数进阶 ===")

# 1.1 默认参数 — C++ 也有，但 Python 有个著名陷阱！
print("\n--- 默认参数 ---")

# 基本用法：和 C++ 一样
def greet(name, greeting="你好"):
    """默认参数：调用者可以不传 greeting"""
    return f"{greeting},{name}!"

print(greet("张三"))              # 使用默认值
print(greet("李四", "早上好"))    # 覆盖默认值


# ⚠️ 【重要陷阱】可变默认参数！
# C++ 中每次调用函数，默认参数都是新的。Python 只在定义时计算一次！

print("\n⚠️ 可变默认参数陷阱：")

# ❌ 错误写法（踩坑！）
def add_to_list_bad(item, my_list=[]):
    """陷阱：默认列表在多次调用间共享！"""
    my_list.append(item)
    return my_list

print(add_to_list_bad("A"))  # ['A']
print(add_to_list_bad("B"))  # ['A', 'B'] ← 不是 ['B']！
print(add_to_list_bad("C"))  # ['A', 'B', 'C'] ← 越来越长！

# ✅ 正确写法（Python 惯例）
def add_to_list_good(item, my_list=None):
    """用 None 做哨兵值，函数内部创建新列表"""
    if my_list is None:
        my_list = []
    my_list.append(item)
    return my_list

print(add_to_list_good("A"))  # ['A']
print(add_to_list_good("B"))  # ['B'] ← 正确！
print(add_to_list_good("C"))  # ['C'] ← 正确！

# C++ 对比：C++ 每次调用都重新求值默认参数，不存在此问题


# 1.2 关键字参数 — 按名字传参，顺序自由！
print("\n--- 关键字参数 ---")

def create_student(name, age, major, city="北京"):
    """Python 支持按参数名传参"""
    return f"{name},{age}岁,{major}专业，来自{city}"

# 按位置传参（C++ 风格）
print(create_student("张三", 20, "计算机"))

# 按关键字传参 — 顺序可以任意！
print(create_student(age=22, major="数学", name="李四"))

# 混合使用：位置参数在前，关键字参数在后
print(create_student("王五", 19, major="物理", city="上海"))

# C++ 对比：C++ 没有关键字参数！必须按声明顺序传参
# → Python 函数如果有 5 个参数但只需改最后一个，关键字参数超方便


# 1.3 *args — 接收任意数量的位置参数
print("\n--- *args(可变位置参数)---")

def sum_all(*args):
    """*args 把传入的所有位置参数打包成一个元组"""
    print(f"  接收到 {len(args)} 个参数: {args}")
    return sum(args)

print(f"sum_all(1, 2, 3)    = {sum_all(1, 2, 3)}")
print(f"sum_all(10, 20)      = {sum_all(10, 20)}")
print(f"sum_all()            = {sum_all()}")  # 0 个参数也可以

# *args 还可以用在调用时——解包
nums = [1, 2, 3, 4, 5]
print(f"sum_all(*nums)       = {sum_all(*nums)}")  # *解包列表 → sum(1,2,3,4,5)

# C++ 对比：C++ 的可变参数（variadic templates / va_list）复杂得多


# 1.4 **kwargs — 接收任意数量的关键字参数
print("\n--- **kwargs(可变关键字参数)---")

def print_info(**kwargs):
    """**kwargs 把传入的关键字参数打包成一个字典"""
    for key, value in kwargs.items():
        print(f"  {key}: {value}")

print_info(name="张三", age=20, major="计算机科学")
print_info(title="Python 学习", day=4)

# C++ 对比：C++ 没有类似功能，需要用 map 或结构体模拟


# 1.5 参数顺序规则
print("\n--- 参数顺序规则 ---")
# 完整顺序：普通参数 → *args → 关键字-only参数 → **kwargs
def full_demo(a, b, *args, c=10, **kwargs):
    print(f"  普通参数: a={a}, b={b}")
    print(f"  *args: {args}")
    print(f"  关键字-only: c={c}")
    print(f"  **kwargs: {kwargs}")

full_demo(1, 2, 3, 4, 5, c=99, name="test", value=42)
# a=1, b=2 → 前两个按位置
# args=(3,4,5) → 剩下的位置参数
# c=99 → 只能通过关键字传入（因为它在 *args 后面）
# kwargs={'name':'test', 'value':42} → 剩余的关键字参数


# ============================================================
# 2. 函数是一等公民 — Python 函数是对象！
# ============================================================

print("\n=== 2. 函数是一等公民 ===")

# 2.1 把函数赋值给变量
def hello():
    return "Hello World!"

greet_func = hello           # 不是调用！是把函数对象赋给变量
print(f"hello 的类型: {type(hello)}")  # <class 'function'>
print(f"通过 greet_func 调用: {greet_func()}")  # 等价于 hello()

# 2.2 函数作为参数传递（高阶函数）
print("\n--- 函数作为参数 ---")

def apply_to_list(func, data):
    """对列表中每个元素调用 func"""
    return [func(x) for x in data]

def square(x):
    return x * x

data = [1, 2, 3, 4, 5]
print(f"apply square: {apply_to_list(square, data)}")

# 用 lambda 可以更简洁（后面细讲）
print(f"apply lambda: {apply_to_list(lambda x: x ** 3, data)}")

# 2.3 函数作为返回值（闭包的基础）
print("\n--- 函数作为返回值 ---")

def make_multiplier(n):
    """返回一个 '乘以 n' 的函数"""
    def multiply(x):
        return x * n          # n 来自外层函数的作用域！
    return multiply

double = make_multiplier(2)   # double 是一个函数
triple = make_multiplier(3)   # triple 是另一个函数

print(f"double(10) = {double(10)}")    # 20
print(f"triple(10) = {triple(10)}")    # 30

# 这就是"闭包"（closure）：内层函数记住了外层函数的变量 n
# C++ 对比：类似 C++ lambda 的捕获 [=]，但 Python 语法更自然


# ============================================================
# 3. lambda 表达式 — 匿名函数
# ============================================================

print("\n=== 3. lambda 表达式 ===")

# 语法：lambda 参数: 返回值表达式
# 对比 C++：[](int x) { return x * 2; }  →  lambda x: x * 2

# 3.1 基础用法
add = lambda a, b: a + b
print(f"lambda add: {add(3, 5)}")  # 8

# 3.2 lambda 最常用于 sorted/max/min 的 key 参数
print("\n--- sorted 的 key 参数 ---")

students = [
    {"name": "张三", "score": 85},
    {"name": "李四", "score": 92},
    {"name": "王五", "score": 78},
]

# 按成绩排序
sorted_by_score = sorted(students, key=lambda s: s["score"])
print("按成绩升序:", [s["name"] for s in sorted_by_score])

# 按姓名字段排序
sorted_by_name = sorted(students, key=lambda s: s["name"])
print("按姓名排序:", [s["name"] for s in sorted_by_name])

# 3.3 lambda 的限制
# lambda 只能写一个表达式，不能包含语句（if/for/赋值等）
# 如果逻辑复杂，还是定义 def 函数

# ❌ 不能这么写：
# bad_lambda = lambda x: if x > 0: return "正" else: return "负"
# ✅ 可以用三目表达式（条件表达式）：
sign = lambda x: "正" if x > 0 else ("负" if x < 0 else "零")
print(f"sign(-5)={sign(-5)}, sign(0)={sign(0)}, sign(5)={sign(5)}")


# ============================================================
# 4. 常用内置高阶函数 — map, filter, zip, any, all
# ============================================================

print("\n=== 4. 常用内置函数 ===")

# 4.1 map() — 对每个元素应用函数
print("\n--- map() ---")

nums = [1, 2, 3, 4, 5]

# 传统写法
squares1 = []
for n in nums:
    squares1.append(n ** 2)

# map 写法（返回迭代器，用 list() 转换）
squares2 = list(map(lambda x: x ** 2, nums))

# 最 Python 的写法：列表推导式
squares3 = [x ** 2 for x in nums]

print(f"传统:   {squares1}")
print(f"map:    {squares2}")
print(f"推导式: {squares3}")

# ⚠️ 提示：Python 中列表推导式比 map() 更常用、更可读

# 4.2 filter() — 过滤元素
print("\n--- filter() ---")

# filter 写法
even_nums = list(filter(lambda x: x % 2 == 0, nums))
# 推导式写法（更推荐）
even_nums2 = [x for x in nums if x % 2 == 0]

print(f"偶数 (filter): {even_nums}")
print(f"偶数 (推导式): {even_nums2}")

# 4.3 zip() — 并行迭代多个序列
print("\n--- zip() ---")

names = ["张三", "李四", "王五"]
scores = [85, 92, 78]

# 并行遍历两个列表
for name, score in zip(names, scores):
    print(f"  {name}: {score} 分")

# 创建字典
score_dict = dict(zip(names, scores))
print(f"zip 转字典: {score_dict}")

# C++ 对比：没有直接的 zip，需要手动索引遍历

# 4.4 enumerate() — 获取索引和值（Day 2 提过，复习一下）
print("\n--- enumerate() ---")
# C++ 对比：类似 range-based for + 手动计数器
for i, name in enumerate(names, 1):  # 从 1 开始编号
    print(f"  第 {i} 名: {name}")

# 4.5 any() / all() — 检查可迭代对象
print("\n--- any() / all() ---")

checks = [True, False, True, True]
print(f"any({checks}) = {any(checks)}")   # 有任意 True → True
print(f"all({checks}) = {all(checks)}")   # 全部 True → True

# 实用场景：检查列表中是否有负数
numbers = [1, 5, -3, 8, 0]
print(f"有负数？ {any(n < 0 for n in numbers)}")   # True
print(f"全为正？ {all(n > 0 for n in numbers)}")   # False

# 注意：传入的是生成器表达式（不是列表推导式），省内存

# 4.6 sorted() 的高级用法
print("\n--- sorted() 进阶 ---")

words = ["Python", "java", "C++", "Rust", "go"]
# 忽略大小写排序
print(f"忽略大小写: {sorted(words, key=str.lower)}")
# 按长度排序
print(f"按长度:     {sorted(words, key=len)}")
# 按长度降序
print(f"长度降序:   {sorted(words, key=len, reverse=True)}")


# ============================================================
# 5. 作用域 LEGB 规则 — Python 的变量查找顺序
# ============================================================

print("\n=== 5. 作用域 LEGB ===")

# Python 的变量查找按 LEGB 顺序：
# L — Local（函数内部）
# E — Enclosing（外层函数）
# G — Global（模块级别）
# B — Built-in（内建，如 print, len）

# C++ 对比：C++ 是块级作用域 + 名字空间，Python 是函数级作用域

# 5.1 Local 和 Global 基本演示
print("\n--- Local vs Global ---")

name = "全局张三"            # 全局变量

def show_name():
    name = "局部李四"        # 局部变量（不会修改全局的！）
    print(f"  函数内部: {name}")

show_name()
print(f"  函数外部: {name}")  # 全局变量没有改变

# 5.2 在函数内修改全局变量 — global 关键字
print("\n--- global 关键字 ---")

counter = 0

def increment():
    global counter            # 声明"我要用全局的 counter"
    counter += 1
    print(f"  内部: {counter}")

increment()
increment()
print(f"  外部: {counter}")   # 2

# C++ 对比：C++ 中全局变量直接访问，不需要额外声明
# Python 必须加 global，否则 counter += 1 会创建局部变量并报错

# 5.3 Enclosing 作用域 — nonlocal 关键字
print("\n--- nonlocal 关键字 ---")

def outer():
    count = 0                 # outer 的局部变量

    def inner():
        nonlocal count        # 声明"我要用外层函数的 count"
        count += 1            # 不是 local，也不是 global
        return count

    return inner

counter_func = outer()
print(f"第1次: {counter_func()}")  # 1
print(f"第2次: {counter_func()}")  # 2
print(f"第3次: {counter_func()}")  # 3

# 没有 nonlocal 会怎样？
def outer_bad():
    count = 0
    def inner():
        # count += 1          # ❌ UnboundLocalError！
        pass                  # Python 看到 += 会认为 count 是 local 变量
    inner()

# C++ 对比：没有直接对应，最接近的是 lambda 捕获 [&count]

# 5.4 LEGB 查找演示
print("\n--- LEGB 查找演示 ---")

x = "Global"                  # G - Global

def outer():
    x = "Enclosing"           # E - Enclosing
    def inner():
        # x = "Local"         # L - Local（注释掉，观察查找顺序）
        print(f"  inner 中的 x: {x}")  # 先找 L → 没有 → 找 E → 找到！
    inner()

outer()

# 如果 Local 和 Enclosing 都没有，就找 Global
# 如果 Global 也没有，就找 Built-in（如 print, len）


# ============================================================
# 6. 实战技巧：列表推导式 vs map/filter
# ============================================================

print("\n=== 6. 实战：数据处理风格对比 ===")

students_data = [
    {"name": "张三", "score": 85, "city": "北京"},
    {"name": "李四", "score": 92, "city": "上海"},
    {"name": "王五", "score": 78, "city": "北京"},
    {"name": "赵六", "score": 88, "city": "广州"},
    {"name": "钱七", "score": 95, "city": "上海"},
]

# 任务：找出 score >= 85 的学生，按名字格式化输出
# 要求输出格式："{name} ({city}) — {score}分"

# 风格 1：传统 for 循环（C++ 风格）
print("--- 传统 for 循环 ---")
passed = []
for s in students_data:
    if s["score"] >= 85:
        passed.append(f"{s['name']} ({s['city']}) — {s['score']}分")
for item in passed:
    print(f"  {item}")

# 风格 2：map + filter（函数式风格）
print("\n--- 函数式风格 ---")
passed_func = list(map(
    lambda s: f"{s['name']} ({s['city']}) — {s['score']}分",
    filter(lambda s: s["score"] >= 85, students_data)
))
for item in passed_func:
    print(f"  {item}")

# 风格 3：最 Python 的方式——列表推导式（推荐！）
print("\n--- 列表推导式（✅推荐） ---")
passed_python = [
    f"{s['name']} ({s['city']}) — {s['score']}分"
    for s in students_data
    if s["score"] >= 85
]

for item in passed_python:
    print(f"  {item}")

# 结论：Python 中列表推导式 > map/filter，更清晰易读


# ============================================================
# C++ → Python 速查表（函数 + 内置工具）
# ============================================================
"""
┌──────────────────────┬───────────────────────────────┬──────────────────────────┐
│ 概念                  │ C++                            │ Python                   │
├──────────────────────┼───────────────────────────────┼──────────────────────────┤
│ 默认参数              │ void f(int x=5)                │ def f(x=5):              │
│ 可变默认参数陷阱       │ 不存在                         │ ⚠️ 用 None 做哨兵值        │
│ 关键字参数            │ 无                             │ f(name="张三", age=20)    │
│ 可变参数              │ ... / variadic template        │ *args（打包为元组）         │
│ 可变关键字参数         │ 无                             │ **kwargs（打包为字典）      │
│ lambda               │ [](int x){return x*2;}         │ lambda x: x*2            │
│ 函数作为参数           │ 函数指针 / std::function       │ 直接传函数名               │
│ 闭包                  │ [=] 捕获 lambda               │ 内层函数直接用外层变量       │
│ map                  │ std::transform                │ map(func, iterable)      │
│ filter               │ std::copy_if                  │ filter(func, iterable)   │
│ zip                  │ 手动循环                       │ zip(a, b)                │
│ enumerate            │ 手动计数                       │ enumerate(list, start)   │
│ any / all            │ std::any_of / std::all_of     │ any() / all()            │
│ global 变量           │ 直接访问                       │ 需要 global 声明           │
│ 外层作用域变量         │ 无直接对应                     │ nonlocal 声明             │
│ 列表推导式 ← 推荐！     │ 无（最接近：range-v3）          │ [f(x) for x in L if P(x)]│
└──────────────────────┴───────────────────────────────┴──────────────────────────┘
"""

# ============================================================
# 常见问题解答（Q&A）
# ============================================================
print("\n=== 常见问题解答 ===")

# Q1: *args 和 **kwargs 的名字是固定的吗？
print("\n--- Q1: *args /**kwargs 的名字 ---")
# 不是！* 和 ** 是语法，后面的名字可以随意取
def demo(*whatever, **anything):
    print(f"  位置: {whatever}")
    print(f"  关键字: {anything}")
demo(1, 2, x=3, y=4, z=5)
# 但约定俗成都用 *args 和 **kwargs，这样别人一看就懂

# Q2: 为什么 sorted 用 key 而不是 cmp？
print("\n--- Q2: sorted 为什么用 key ---")
# Python 3 废弃了 cmp 参数，只保留 key
# key 更高效：每个元素只调用一次 key 函数
# C++ 的 std::sort 使用 comparator（类似 cmp），每次比较都调用
words = ["Python", "java", "C++", "Go"]
print(f"key=str.lower: {sorted(words, key=str.lower)}")
# 如果用 cmp，每对元素比较时都要转小写 → 性能差

# Q3: with 能用于多个文件吗？
print("\n--- Q3: 同时打开多个文件 ---")
# 可以！用逗号分隔
# with open("a.txt") as f1, open("b.txt") as f2:
#     ...

# Q4: 什么时候用 lambda 什么时候用 def？
# lambda：一行表达式能写完，作为参数传递（如 sorted 的 key）
# def：多行逻辑、需要复用、需要文档字符串

print("\n[OK] Day 4 笔记结束！打开 day04_exercise.py 做练习吧。")
