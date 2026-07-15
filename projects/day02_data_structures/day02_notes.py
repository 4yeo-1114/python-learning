"""
============================================================
Day 2: Python 核心数据结构 + 函数（C++ 对比版）
============================================================
目标：掌握 Python 四大核心数据结构（list/tuple/dict/set）
      以及函数定义与参数
"""

# ============================================================
# 1. 列表 List — Python 最常用的数据结构
# ============================================================
# 类似 C++ 的 std::vector，但可以混合存放不同类型！

# 创建列表
empty_list = []
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True]      # Python 列表可以混合类型（C++ 做不到）
names = ["张三", "李四", "王五"]

print("=== 1. 列表基础 ===")
print(f"空列表: {empty_list}")
print(f"数字列表: {numbers}")
print(f"混合列表: {mixed}")
print(f"列表长度: {len(numbers)}")      # len() 获取长度，相当于 C++ 的 .size()

# 访问元素（索引从 0 开始，和 C++ 一样）
print(f"第一个元素: {names[0]}")
print(f"最后一个元素: {names[-1]}")     # Python 独有：负数索引从末尾开始！
print(f"倒数第二个: {names[-2]}")

# 切片（Slice）— Python 最强大的特性之一！
# 语法: list[起始:结束:步长]，返回新列表
print(f"\n=== 切片操作 ===")
nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
print(f"原列表: {nums}")
print(f"nums[2:5]  = {nums[2:5]}")     # [2, 3, 4] — 索引 2,3,4（不含5）
print(f"nums[:4]   = {nums[:4]}")      # [0, 1, 2, 3] — 开头到索引3
print(f"nums[6:]   = {nums[6:]}")      # [6, 7, 8, 9] — 索引6到末尾
print(f"nums[::2]  = {nums[::2]}")     # [0, 2, 4, 6, 8] — 每隔一个
print(f"nums[::-1] = {nums[::-1]}")    # [9, 8, ..., 0] — 反转列表！

# C++ 对比：没有切片语法，需要循环或 STL 算法
# std::vector<int> sub(nums.begin()+2, nums.begin()+5);

# ============================================================
# 2. 列表的增删改查（CRUD 操作）
# ============================================================
print(f"\n=== 2. 列表 CRUD ===")

fruits = ["苹果", "香蕉"]
print(f"初始: {fruits}")

# 增加
fruits.append("橘子")                  # 末尾添加 → 类似 push_back()
print(f"append 后: {fruits}")
fruits.insert(1, "西瓜")               # 在索引1位置插入
print(f"insert 后: {fruits}")
fruits.extend(["葡萄", "草莓"])         # 合并另一个列表
print(f"extend 后: {fruits}")

# 删除
removed = fruits.pop()                 # 删除并返回最后一个元素
print(f"pop 后: {fruits}, 被删除: {removed}")
fruits.pop(0)                          # 删除索引 0 的元素
print(f"pop(0) 后: {fruits}")
fruits.remove("西瓜")                  # 按值删除（只删第一个匹配项）
print(f"remove 后: {fruits}")

# 查找
print(f"'香蕉' 在列表中吗? {'香蕉' in fruits}")     # in 运算符 → True/False
print(f"'火龙果' 在列表中吗? {'火龙果' in fruits}")
print(f"'香蕉' 的索引: {fruits.index('香蕉')}")    # 找不到会报错！

# 修改
fruits[0] = "榴莲"                     # 直接赋值
print(f"修改后: {fruits}")

# C++ 对比：
# push_back()  → append()
# insert(pos)  → insert(pos)
# 没有 in 运算符，需要 std::find 或循环

# ============================================================
# 3. 列表遍历
# ============================================================
print(f"\n=== 3. 列表遍历 ===")

# 方式1：for-in（最常用）
for fruit in fruits:
    print(fruit, end=" ")
print()

# 方式2：带索引遍历 enumerate()
for i, fruit in enumerate(fruits):
    print(f"[{i}] = {fruit}", end="  ")
print()

# 方式3：用 range 模拟 C++ 风格
for i in range(len(fruits)):
    print(fruits[i], end=" ")
print()

# ============================================================
# 4. 元组 Tuple — 不可变的列表
# ============================================================
# 类似 C++ 的 const std::array 或 std::tuple
# 一旦创建就不能修改！（不可增删改）

print(f"\n=== 4. 元组 ===")

# 创建元组
point = (3, 4)
person = ("张三", 20, "北京")

print(f"坐标: {point}")
print(f"个人信息: {person}")
print(f"x = {point[0]}, y = {point[1]}")

# point[0] = 10  # ❌ 这行会报错！元组不可修改

# 元组的用处：
# 1. 函数返回多个值（实际上返回的就是元组）
# 2. 作为字典的键（列表不能做键，元组能）
# 3. 保护数据不被意外修改

# 解包（Unpacking）→ Python 超好用！
name, age, city = person
print(f"解包: {name=}, {age=}, {city=}")

# 交换两个变量（不需要临时变量！）
a, b = 10, 20
a, b = b, a                           # 一行交换！
print(f"交换: a={a}, b={b}")

# C++ 对比：
# std::tuple<int, int> point = std::make_tuple(3, 4);
# int x = std::get<0>(point);  // 麻烦！Python 直接解包


# ============================================================
# 5. 字典 Dict — 键值对，Python 的哈希表
# ============================================================
# 类似 C++ 的 std::unordered_map 或 std::map

print(f"\n=== 5. 字典 ===")

# 创建字典
student = {
    "name": "张三",
    "age": 20,
    "major": "计算机科学",
    "scores": [85, 90, 78]
}

print(f"学生信息: {student}")
print(f"姓名: {student['name']}")     # 用键来访问值
print(f"年龄: {student['age']}")

# 使用 get() 方法更安全 — 键不存在返回 None 而不是报错
print(f"姓名: {student.get('name')}")
print(f"电话号码: {student.get('phone', '未填写')}")   # 可以设置默认值

# 增删改查
student["phone"] = "13800138000"      # 添加新键值对
student["age"] = 21                    # 修改已有键的值
del student["major"]                   # 删除键值对
print(f"更新后: {student}")

# 遍历字典
print("\n遍历字典:")
for key in student:                   # 遍历键
    print(f"  {key}", end=" ")
print()

for key, value in student.items():    # 同时遍历键和值（最常用）
    print(f"  {key} → {value}")

for value in student.values():        # 遍历值
    print(f"  {value}", end=" ")
print()

# 检查键是否存在
print(f"有 'name' 键吗? {'name' in student}")
print(f"有 'email' 键吗? {'email' in student}")

# C++ 对比：
# std::unordered_map<std::string, int> scores;
# scores["张三"] = 95;
# if (scores.find("李四") != scores.end()) { ... }  // 冗长！


# ============================================================
# 6. 集合 Set — 去重 + 集合运算
# ============================================================
# 类似 C++ 的 std::unordered_set
# 特点：无序、不重复、自动去重

print(f"\n=== 6. 集合 ===")

# 创建集合
empty_set = set()                      # 注意：{} 创建的是空字典，不是空集合！
fruits_set = {"苹果", "香蕉", "橘子"}

print(f"空集合: {empty_set}")
print(f"水果集合: {fruits_set}")

# 自动去重
nums = [1, 2, 2, 3, 3, 3, 4, 5, 5]
unique_nums = list(set(nums))          # 去重的经典方法
print(f"原列表: {nums}")
print(f"去重后: {unique_nums}")

# 集合运算（比 C++ 方便太多！）
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

print(f"\n集合运算:")
print(f"  a = {a}, b = {b}")
print(f"  并集 a | b = {a | b}")      # {1, 2, 3, 4, 5, 6}
print(f"  交集 a & b = {a & b}")      # {3, 4}
print(f"  差集 a - b = {a - b}")      # {1, 2} (在 a 但不在 b)
print(f"  对称差 a ^ b = {a ^ b}")    # {1, 2, 5, 6} (只在一边的)

# 增删操作
fruits_set.add("草莓")
fruits_set.remove("香蕉")              # 元素不存在会报错
fruits_set.discard("火龙果")           # 安全删除，不存在也不报错
print(f"集合更新后: {fruits_set}")

# 检查成员
print(f"'苹果' 在集合中? {'苹果' in fruits_set}")

# C++ 对比：
# std::set_union, std::set_intersection 需要 <algorithm> + 迭代器，很繁琐


# ============================================================
# 7. 列表推导式 List Comprehension
# ============================================================
# Python 最标志性的语法！一行代码生成列表

print(f"\n=== 7. 列表推导式 ===")

# 传统方式：用循环
squares_old = []
for i in range(1, 11):
    squares_old.append(i ** 2)
print(f"传统方式: {squares_old}")

# 列表推导式：一行搞定！
squares = [i ** 2 for i in range(1, 11)]
print(f"推导式:   {squares}")

# 带条件过滤
even_squares = [i ** 2 for i in range(1, 11) if i % 2 == 0]
print(f"偶数的平方: {even_squares}")

# 嵌套循环（相当于双重 for 循环）
pairs = [(x, y) for x in range(1, 4) for y in range(1, 4)]
print(f"坐标对: {pairs}")

# 字典推导式
word = "hello"
char_count = {c: word.count(c) for c in set(word)}
print(f"字符计数: {char_count}")

# 集合推导式
squares_set = {i ** 2 for i in range(1, 6)}
print(f"平方集合: {squares_set}")

# C++ 对比：
# 没有直接的推导式语法，需要循环或 std::transform


# ============================================================
# 8. 函数 — def 定义
# ============================================================
# Python 用 def 定义函数，不需要声明返回类型

print(f"\n=== 8. 函数 ===")

# 基本函数定义
def greet(name):
    """这是一个文档字符串（docstring），说明函数做什么"""
    return f"你好，{name}！"

print(greet("张三"))
print(greet("李四"))

# 多个参数
def add(a, b):
    return a + b

print(f"add(3, 5) = {add(3, 5)}")

# C++ 对比：
# string greet(string name) {
#     return "你好，" + name + "！";
# }
# 注意：Python 不需要写类型！


# ============================================================
# 9. 函数参数 — Python 的灵活性
# ============================================================
print(f"\n=== 9. 函数参数 ===")

# 9.1 默认参数 — 和 C++ 类似
def power(base, exp=2):               # exp 默认值为 2
    return base ** exp

print(f"power(3)    = {power(3)}")     # 3^2 = 9
print(f"power(3, 3) = {power(3, 3)}") # 3^3 = 27

# ⚠️⚠️⚠️ 陷阱：默认参数不能用可变对象！（Python 最经典的坑）
#
# 核心原因：Python 的默认参数在 def 定义时只计算一次，不是每次调用都重新创建。
# 而 C++ 的默认参数是每次调用时重新构造，所以 C++ 没有这个问题。
#
# 演示：
# def bad_append(item, my_list=[]):  # ← 这个 [] 在 def 时就创建好了
#     my_list.append(item)
#     return my_list
#
# bad_append(1)  → [1]
# bad_append(2)  → [1, 2]  ← 不是 [2]！还是同一个列表对象！
# bad_append(3)  → [1, 2, 3] ← 会一直累积下去！
#
# 所有可变类型都有这个坑：[]  {}  set()  统统不能做默认参数！
# 只有不可变类型才安全：None  数字  字符串  元组
#
# C++ 对比（为什么 C++ 没这个问题）：
# void bad(int item, vector<int>& lst = vector<int>{}) {
#     lst.push_back(item);  // 每次调用都执行 {}，创建全新 vector
# }
#
# 正确做法：默认值用 None，函数内部判断后再创建新对象
def good_append(item, my_list=None):
    if my_list is None:            # is 比 == 更精确（None 是全局单例）
        my_list = []               # 确定没传参，才创建新列表
    my_list.append(item)
    return my_list

print(f"good_append(1) = {good_append(1)}")   # [1]
print(f"good_append(2) = {good_append(2)}")   # [2] ← 每次都是新列表！
print(f"good_append(3) = {good_append(3)}")   # [3]

# 9.2 关键字参数 — 按名字传参（C++ 没有！）
def student_info(name, age, city="未知"):
    return f"{name}, {age}岁, 来自{city}"

print(student_info("张三", 20))
print(student_info(age=22, name="李四"))          # 可以打乱顺序！
print(student_info("王五", age=18, city="上海"))   # 混合使用

# 9.3 *args — 接收任意数量的位置参数（打包成元组）
def sum_all(*args):
    total = 0
    for num in args:
        total += num
    return total

print(f"sum_all(1,2,3)    = {sum_all(1, 2, 3)}")
print(f"sum_all(1,2,3,4,5) = {sum_all(1, 2, 3, 4, 5)}")

# 9.4 **kwargs — 接收任意数量的关键字参数（打包成字典）
def print_info(**kwargs):
    for key, value in kwargs.items():
        print(f"  {key} → {value}")

print("print_info 输出:")
print_info(name="张三", age=20, job="程序员")

# 9.5 全部组合起来
def full_demo(a, b, *args, default="默认值", **kwargs):
    print(f"a={a}, b={b}")
    print(f"args={args}")
    print(f"default={default}")
    print(f"kwargs={kwargs}")

print("\nfull_demo 输出:")
full_demo(1, 2, 3, 4, 5, default="自定义", name="测试", value=42)

# C++ 对比：
# *args 类似 C++ 的 variadic templates / va_list，但 Python 简单得多
# **kwargs 没有 C++ 直接对应物
# 关键字参数是 Python 独有的便利特性


# ============================================================
# 10. 常用内置函数速览
# ============================================================
print(f"\n=== 10. 常用内置函数 ===")

nums = [3, 1, 4, 1, 5, 9, 2, 6]

print(f"列表: {nums}")
print(f"sum()   = {sum(nums)}")        # 求和
print(f"max()   = {max(nums)}")        # 最大值
print(f"min()   = {min(nums)}")        # 最小值
print(f"sorted()= {sorted(nums)}")     # 排序，返回新列表
print(f"any()   = {any(n > 5 for n in nums)}")  # 任一为真？
print(f"all()   = {all(n > 0 for n in nums)}")  # 全部为真？
print(f"zip()   = {list(zip('abc', [1, 2, 3]))}")   # 打包

# sorted() 不修改原列表
nums.sort()                            # 原地排序（修改原列表）
print(f"sort() 后: {nums}")

# enumerate() — 遍历时同时获取索引和值
print("\n带索引遍历:")
for idx, val in enumerate(['a', 'b', 'c'], start=1):  # start=1 让索引从 1 开始
    print(f"  [{idx}] {val}")


# ============================================================
# 核心差异速查表（C++ → Python 数据结构篇）
# ============================================================
"""
┌──────────────────────┬──────────────────────────┬──────────────────────────┐
│ 数据结构              │ C++                       │ Python                    │
├──────────────────────┼──────────────────────────┼──────────────────────────┤
│ 动态数组              │ std::vector<T>            │ list [1, 2, 3]            │
│ 定长数组              │ std::array<T, N>          │ tuple (1, 2, 3)           │
│ 哈希表                │ std::unordered_map<K,V>   │ dict {"k": v}             │
│ 有序映射              │ std::map<K,V>             │ collections.OrderedDict   │
│ 集合（哈希）           │ std::unordered_set<T>     │ set {1, 2, 3}             │
│ 混合类型              │ std::variant / std::any   │ 原生支持 [1, "a", True]    │
│ 切片                  │ 需要循环或算法             │ list[2:5]                 │
│ 推导式                │ 无（用循环 + push_back）   │ [x*2 for x in list]       │
│ 解包                  │ std::tie 或结构化绑定      │ a, b, c = tuple           │
│ in 运算符             │ std::find 或 .count()     │ x in list → True/False    │
└──────────────────────┴──────────────────────────┴──────────────────────────┘
"""

# ============================================================
# 11. 常见问题解答（Q&A）
# ============================================================
print(f"\n=== 11. 常见问题解答 ===")

# ----------------------------------------------------------
# Q1: 字典添加元素能用 scores.append("赵六", 80) 吗？
# ----------------------------------------------------------
# ❌ 不行！字典没有 .append() 方法，那是列表（list）的方法。
#
# 原因：
#   - 列表是有序的序列，用 .append() 把元素加到末尾
#   - 字典是键值对（key → value），没有"末尾"这个概念
#   - 字典直接用 方括号赋值 来添加/更新元素

# 对比演示：
print("\n--- Q1: 字典添加 ---")
# 列表添加
my_list = [1, 2, 3]
my_list.append(4)
print(f"列表 append: {my_list}")          # [1, 2, 3, 4]

# 字典添加
scores = {"张三": 85}
scores["赵六"] = 88                       # ✅ 正确：dict[key] = value
print(f"字典添加: {scores}")              # {'张三': 85, '赵六': 88}

# scores.append("赵六", 88)              # ❌ AttributeError: 'dict' object has no attribute 'append'

# 速记：
#   列表 → .append(item)     一次性把一个元素加到末尾
#   字典 → d[key] = value    用键来"挂"一个值


# ----------------------------------------------------------
# Q2: max(scores, key=scores.get) 语法详解
# ----------------------------------------------------------
# 拆开来理解：
#
# max(iterable, key=函数)
#   - max 会遍历 iterable 中的每个元素
#   - 对每个元素调用 key 指定的函数，得到"比较用的值"
#   - 返回的是原始元素（不是比较值），但比较依据是 key 函数的返回值
#
# scores.get 是字典的一个方法：
#   - scores.get("张三") 返回 85
#   - scores.get("李四") 返回 92
#   - 和 scores["张三"] 效果类似，但 key 不存在时返回 None 不报错

print("\n--- Q2: max + key=scores.get ---")
scores = {"张三": 85, "李四": 92, "王五": 78}

# 逐步理解：
print("scores.get('张三') =", scores.get("张三"))   # 85
print("scores.get('李四') =", scores.get("李四"))   # 92
print("scores.get('王五') =", scores.get("王五"))   # 78

# max 的执行过程（伪代码）：
#   遍历 scores 的键: "张三", "李四", "王五"
#   对每个键调用 scores.get:
#     "张三" → 85
#     "李四" → 92  ← 最大！
#     "王五" → 78
#   返回原始键（不是值！）: "李四"

top_student = max(scores, key=scores.get)
print(f"最高分学生: {top_student}")                      # 李四
print(f"他的分数: {scores[top_student]}")                # 92

# 如果不用 key=scores.get，直接 max(scores) 会比较键本身（字符串）
# "王五" > "李四" > "张三"（按拼音/Unicode编码）
print(f"不加 key: max(scores) = {max(scores)}")          # 王五（不对！）

# 类比 C++：
# 就像给 std::max_element 传一个自定义比较函数
# auto it = std::max_element(m.begin(), m.end(),
#     [](auto& a, auto& b) { return a.second < b.second; });


# ----------------------------------------------------------
# Q3: 字符串方法 vs 独立函数 — upper(c) 还是 c.upper()？
# ----------------------------------------------------------
# ❌ upper(c) 不行！Python 没有叫 upper() 的独立函数。
# ✅ 必须写 c.upper()
#
# Python 中字符串操作都是"方法"（method），要 . 调用：
#   c.upper()   c.lower()   c.strip()   c.split()   c.replace(...)
#
# 这和 C++ 不同！C++ 里 <algorithm> 有独立函数：
#   std::toupper(c)  ← 独立函数
#   std::sort(v.begin(), v.end())  ← 独立函数
#
# Python 的字符串不可变，所有方法都返回新字符串，不修改原字符串。

print("\n--- Q3: 方法调用 vs 独立函数 ---")
words = ["hello", "world", "python", "code"]

# ✅ 正确：c.upper() — 字符串对象调用自己的 upper 方法
upper_correct = [c.upper() for c in words if len(c) >= 5]
print(f"正确写法 c.upper(): {upper_correct}")

# ❌ 错误：upper(c) — 没有这个独立函数
# upper_wrong = [upper(c) for c in words if len(c) >= 5]
# NameError: name 'upper' is not defined

# 速记规则：
#   字符串操作 → "xxx".方法名()
#   列表操作   → [xxx].方法名()
#   字典操作   → {xxx}.方法名()
#   Python 是"面向对象"风格，方法挂在对象上，不是独立函数


# ----------------------------------------------------------
# Q4: name.strip() 是什么意思？
# ----------------------------------------------------------
# .strip() 是字符串方法，作用：去掉字符串两端的空白字符
# 空白字符包括：空格、制表符 \t、换行符 \n 等
#
# 常见用法：
#   - 清理用户输入（去掉首尾不小心打的空格）
#   - 验证输入是否为空（先 strip 再判断）

print("\n--- Q4: strip() 详解 ---")

# 基本用法
s1 = "   Hello World   "
print(f"原始:  '{s1}'")
print(f"strip: '{s1.strip()}'")          # 'Hello World'（两端空格没了）

# 实战例子
name1 = "  张三  "
name2 = "     "        # 全是空格，相当于空输入
name3 = "李四"

print(f"\n'{name1}'.strip() = '{name1.strip()}'")   # '张三'
print(f"'{name2}'.strip() = '{name2.strip()}'")     # ''（空字符串）
print(f"'{name3}'.strip() = '{name3.strip()}'")     # '李四'（没空格，不变）

# 在验证函数中的作用（见练习 6b）：
def validate_name(name):
    """验证姓名：不为空且长度至少2个字符"""
    return bool(name) and len(name.strip()) >= 2
    #                  ^^^^^^^^^^^^^^^^
    #                  先去掉首尾空格再判断长度
    #                  否则用户输入 "  " 也能通过 len()>=2

print(f"\nvalidate_name('   ')  = {validate_name('   ')}")   # False（strip后为空）
print(f"validate_name(' 张三 ') = {validate_name(' 张三 ')}") # True（strip后='张三'，长度2）

# strip 家族：
#   .strip()   — 去掉两端空白
#   .lstrip()  — 只去掉左边（left）空白
#   .rstrip()  — 只去掉右边（right）空白
text = "==Hello=="
print(f"\n'{text}'.strip('=')  = '{text.strip('=')}'")      # 'Hello'（可指定要去掉的字符）
print(f"'{text}'.lstrip('=') = '{text.lstrip('=')}'")      # 'Hello=='
print(f"'{text}'.rstrip('=') = '{text.rstrip('=')}'")      # '==Hello'


print("\n[OK] Day 2 笔记结束！运行 day02_exercise.py 来练习吧。")
