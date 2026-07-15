"""
============================================================
Day 1: Python 基础语法速通（C++ 对比版）
============================================================
目标：快速感受 Python 和 C++ 的核心差异
"""

# ============================================================
# 1. 注释
# ============================================================
# Python 的单行注释用 #（C++ 用 //）
# Python 没有 /* */ 多行注释，但可以用三个引号作为文档字符串

"""
这是多行字符串（通常用作 docstring 文档注释）
功能上类似 C++ 的 /* ... */
实际上它是一个字符串字面量，Python 会把它当作代码的一部分
"""

# C++ 对比：
# // C++ 单行注释
# /* C++ 多行注释 */


# ============================================================
# 2. print() — 输出（C++ 的 cout）
# ============================================================
print("Hello, Python!")           # 自动换行
print("不换行", end="，")          # end 参数替代了默认的 '\n'
print("接在同一行")
print(f"1 + 1 = {1 + 1}")        # f-string：比 C++ 的 printf 方便很多

# C++ 对比：
# cout << "Hello, C++!" << endl;


# ============================================================
# 3. 缩进规则 — Python 最特别的地方！
# ============================================================
# Python 用缩进来表示代码块，不需要 {}
# 标准缩进是 4 个空格（不要用 Tab！）

x = 10
if x > 5:
    print("x 大于 5")     # 缩进 4 格，属于 if 块
    print("还在 if 块里")
print("不在 if 块里了")    # 不缩进，不属于 if 块

# C++ 对比：
# if (x > 5) {
#     cout << "x 大于 5" << endl;
#     cout << "还在 if 块里" << endl;
# }
# cout << "不在 if 块里了" << endl;
# ↑ 注意！C++ 用 {}，Python 用缩进。缩进错了代码就会出错！


# ============================================================
# 4. 变量 — 动态类型（和 C++ 最大的不同！）
# ============================================================
# Python 不需要声明类型，变量只是名字，可以随时指向任何类型的值

name = "张三"           # 字符串
age = 20                # 整数
height = 1.75           # 浮点数
is_student = True       # 布尔值（注意大写 True/False）

print(type(name))       # <class 'str'>
print(type(age))        # <class 'int'>
print(type(height))     # <class 'float'>
print(type(is_student)) # <class 'bool'>

# 变量可以随时改变类型（C++ 做不到）
x = 42
print(f"x 是 {type(x)}")   # int
x = "现在是字符串了"
print(f"x 是 {type(x)}")   # str

# C++ 对比：
# int age = 20;              // 必须声明类型
# string name = "张三";      // 类型固定，不能改变
# auto x = 42;               // C++11 的 auto 有点像，但不完全一样


# ============================================================
# 5. input() — 输入（C++ 的 cin）
# ============================================================
# input() 总是返回字符串，需要自己转换类型！

# name = input("请输入你的名字：")
# print(f"你好，{name}！")

# 如果需要数字，必须手动转换
# age_str = input("请输入你的年龄：")
# age = int(age_str)        # str → int
# print(f"明年你 {age + 1} 岁")

# C++ 对比：
# string name;
# cin >> name;
# int age;
# cin >> age;               // C++ 自动按类型读取


# ============================================================
# 6. 基本数据类型
# ============================================================
# int     — 整数（Python 的 int 无限大！没有 overflow）
# float   — 浮点数（双精度，相当于 C++ 的 double）
# str     — 字符串（用 '' 或 "" 都行，没有 char 类型）
# bool    — 布尔值（True / False，注意大写）
# None    — 空值（类似 C++ 的 nullptr / NULL）

big_number = 2 ** 100       # Python int 可以无限大
print(f"2^100 = {big_number}")

# 字符串可以用单引号或双引号
s1 = '你好'
s2 = "世界"
print(s1 + s2)              # 字符串拼接用 +
print(s1 * 3)               # 字符串重复用 *  → "你好你好你好"
# C++ 做不到 s1 * 3！

# 布尔值
print(True and False)       # False  （C++ 用 &&，Python 用 and）
print(True or False)        # True   （C++ 用 ||，Python 用 or）
print(not True)             # False  （C++ 用 !，Python 用 not）

# None 空值
result = None
print(result is None)       # True，判断 None 用 is，不用 ==

# C++ 对比：
# nullptr / NULL / 0


# ============================================================
# 7. 字符串操作（Python 的字符串超好用）
# ============================================================
text = "  Hello, Python World!  "

# 常用方法
print(text.strip())          # 去首尾空格
print(text.lower())          # 全小写
print(text.upper())          # 全大写
print(text.replace("Python", "C++"))  # 替换
print(text.split(","))       # 按逗号分割 → ['  Hello', ' Python World!  ']

# f-string（Python 3.6+，强烈推荐！）
name = "小明"
score = 95.5
print(f"{name} 的成绩是 {score:.1f} 分")  # .1f 保留一位小数

# C++ 对比：
# // std::string text = "  Hello, C++ World!  ";
# // 很多操作需要 <algorithm> 库，比如 std::replace, boost::split 等
# // Python 字符串操作更方便


# ============================================================
# 8. 条件判断
# ============================================================
score = 85

if score >= 90:
    grade = "A"
elif score >= 80:           # Python 用 elif，不是 else if
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "D"

print(f"成绩等级：{grade}")

# Python 特有的简洁写法
age = 20
status = "成年" if age >= 18 else "未成年"   # 三元表达式
print(status)

# C++ 对比：
# if (score >= 90) grade = "A";
# else if (score >= 80) grade = "B";   // C++ 是 else if
# else grade = "D";


# ============================================================
# 9. 循环
# ============================================================
# for 循环 — Python 的 for 遍历可迭代对象，不像 C++ 的三段式

# 遍历 range
print("\n=== range(5) ===")
for i in range(5):          # 0, 1, 2, 3, 4
    print(i, end=" ")

print("\n\n=== range(2, 5) ===")
for i in range(2, 5):       # 2, 3, 4
    print(i, end=" ")

print("\n\n=== range(0, 10, 2) ===")
for i in range(0, 10, 2):   # 0, 2, 4, 6, 8  (步长 2)
    print(i, end=" ")

# C++ 对比：
# for (int i = 0; i < 5; i++)      →  for i in range(5):
# for (int i = 2; i < 5; i++)      →  for i in range(2, 5):
# for (int i = 0; i < 10; i += 2)  →  for i in range(0, 10, 2):

# while 循环 — 和 C++ 基本一样
print("\n\n=== while 循环 ===")
count = 3
while count > 0:
    print(f"倒计时：{count}")
    count -= 1              # Python 没有 count-- ！

# 遍历字符串
print("\n=== 遍历字符串 ===")
for char in "Python":
    print(char, end=" ")    # P y t h o n

# C++ 对比：
# 没有 count--, count++，用 count -= 1, count += 1


# ============================================================
# 核心差异速查表（C++ → Python）
# ============================================================
"""
┌─────────────────────┬──────────────────────────┬─────────────────────────┐
│ 项目                 │ C++                       │ Python                   │
├─────────────────────┼──────────────────────────┼─────────────────────────┤
│ 语句结束             │ 分号 ;                    │ 换行（不需要分号）        │
│ 代码块               │ 花括号 {}                 │ 缩进（4 个空格）          │
│ 类型系统             │ 静态类型，必须声明         │ 动态类型，自动推断         │
│ 注释                 │ // 和 /* */               │ # 和 '''...'''           │
│ 输出                 │ cout << "hi" << endl;    │ print("hi")              │
│ 输入                 │ cin >> x;                │ x = input("提示:")       │
│ 条件                 │ if/else if/else          │ if/elif/else             │
│ 与或非               │ && / || / !              │ and / or / not           │
│ 循环                 │ for(int i=0;i<n;i++)    │ for i in range(n):       │
│ 自增自减             │ i++, i--                 │ i += 1, i -= 1           │
│ 空值                 │ nullptr / NULL           │ None                     │
│ 整数范围             │ 有限（32/64 位）          │ 无限大！                  │
│ 字符串拼接           │ + 或 stringstream         │ + 或 f"...{var}..."      │
│ 内存管理             │ new/delete               │ 自动垃圾回收              │
│ 编译/运行            │ 编译后执行                │ 解释执行（即时运行）       │
└─────────────────────┴──────────────────────────┴─────────────────────────┘
"""

print("\n[OK] Day 1 笔记结束！运行下一个练习文件 day01_exercise.py 来动手练习吧。")
