"""
============================================================
Day 7: 异常处理 + 生成器 + 装饰器（C++ 对比版）
============================================================
目标：掌握 Python 三大进阶特性，补齐 Week 2 高级特性最后一块
"""

# ============================================================
# 第一部分：异常处理 — try / except / else / finally / raise
# ============================================================

print("=" * 60)
print("第一部分：异常处理")
print("=" * 60)

# 1.1 为什么需要异常处理？
# C++ 也有 try/catch/throw，概念相似，但 Python 的风格更简洁

# Python 哲学："请求原谅比请求许可更容易"（EAFP）
# Easier to Ask for Forgiveness than Permission
# 先尝试执行，出错了再处理 — 而不是执行前各种 if 判断

# C++ 可能这样写：
# if (file_exists(path)) {
#     if (has_permission(path)) {
#         open_file(path);
#     }
# }
# Python 风格：
# try:
#     open_file(path)
# except FileNotFoundError:
#     handle_error()

print("\n=== 1.1 基本 try/except ===")

# 最基础的异常捕获
try:
    result = 10 / 0       # ZeroDivisionError
except ZeroDivisionError:
    print("[!] 不能除以零！")

# 捕获多种异常
try:
    num = int("abc")      # ValueError
    result = 10 / 0       # 不会执行到这里
except ValueError:
    print("[!] 无法将 'abc' 转为整数")
except ZeroDivisionError:
    print("[!] 不能除以零")

# 一次捕获多种异常（用元组）
try:
    value = int("xyz")
except (ValueError, TypeError) as e:
    print(f"[!] 出错：{type(e).__name__} — {e}")

# 捕获所有异常（谨慎使用！）
try:
    x = 1 / 0
except Exception as e:              # Exception 是所有内置异常的基类
    print(f"[!] 捕获到异常：{type(e).__name__}: {e}")

# C++ 对比：
# try {
#     int x = 1 / 0;           // C++ 中除零是未定义行为，不抛异常！
#     throw runtime_error("...");
# } catch (const exception& e) {
#     cout << e.what() << endl;
# }

# [!] 关键差异：
# 1. Python 除零会抛 ZeroDivisionError，C++ 是未定义行为
# 2. Python 用 except 而不是 catch
# 3. Python 的 as 等价于 C++ 的 catch (const T& e)


# 1.2 else 和 finally
print("\n=== 1.2 else 和 finally ===")

# else：try 块没有异常时才执行
# finally：无论如何都执行（清理资源）

def safe_divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print(f"[!] {a} / {b}：除数为零")
        return None
    except TypeError:
        print(f"[!] 类型错误：{a} 和 {b} 不能做除法")
        return None
    else:
        print(f"[OK] 计算成功：{a} / {b} = {result}")
        return result
    finally:
        print(f"    [finally] 本次调用结束 a={a}, b={b}")

print("测试1：正常情况")
safe_divide(10, 2)
print("\n测试2：除零")
safe_divide(10, 0)
print("\n测试3：类型错误")
safe_divide(10, "2")

# 执行顺序：
# 正常：try → else → finally
# 异常：try → except → finally
# Python 独有 else 分支，C++ 没有


# 1.3 raise — 抛出异常
print("\n=== 1.3 raise — 抛出异常 ===")

def set_age(age):
    if age < 0:
        raise ValueError(f"年龄不能为负数：{age}")  # ← raise = C++ 的 throw
    if age > 150:
        raise ValueError(f"年龄不可能这么大：{age}")
    print(f"年龄设置为 {age}")

try:
    set_age(-5)
except ValueError as e:
    print(f"[!] {e}")

# raise 不带参数 → 重新抛出当前异常（用于记录后继续传播）
print("\n--- raise 重新抛出 ---")
try:
    try:
        1 / 0
    except ZeroDivisionError:
        print("[!] 记录日志...")
        raise               # 重新抛出同一个异常
except ZeroDivisionError:
    print("[!] 上层也捕获到了")

# C++ 对比：
# throw ValueError("年龄不能为负数");  →  raise ValueError("年龄不能为负数")
# throw;  // 重新抛出                  →  raise


# 1.4 自定义异常
print("\n=== 1.4 自定义异常 ===")

# 自定义异常只需继承 Exception
class InsufficientBalanceError(Exception):
    """余额不足异常"""
    def __init__(self, balance, amount):
        self.balance = balance
        self.amount = amount
        super().__init__(f"余额不足：当前 {balance} 元，需要 {amount} 元")

class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientBalanceError(self.balance, amount)
        self.balance -= amount
        return self.balance

acc = BankAccount("张三", 1000)
try:
    acc.withdraw(2000)
except InsufficientBalanceError as e:
    print(f"[!] 取款失败：{e}")
    print(f"    账户余额: {e.balance}, 需要: {e.amount}")

# C++ 对比：
# class InsufficientBalanceError : public std::exception {
#     int balance, amount;
# public:
#     InsufficientBalanceError(int b, int a) : balance(b), amount(a) {}
#     const char* what() const noexcept override { ... }
# };


# ============================================================
# 第二部分：生成器 — yield 和生成器表达式
# ============================================================

print("\n" + "=" * 60)
print("第二部分：生成器（Generator）")
print("=" * 60)

# 2.1 什么是生成器？为什么需要它？
# 生成器 = 一种"惰性求值"的迭代器
# 它不一次性生成所有数据，而是"用到时才生成"

# 问题场景：生成前 100 万个斐波那契数
# 列表方式：一次性占用大量内存
# 生成器方式：每次只计算一个，内存占用极小

print("\n=== 2.1 yield — 把函数变成生成器 ===")

# 普通函数：return 返回所有结果（一次性）
def fibonacci_list(n):
    """返回斐波那契数列前 n 项的列表 — 一次性全算出来"""
    result = []
    a, b = 0, 1
    for _ in range(n):
        result.append(a)
        a, b = b, a + b
    return result

# 生成器函数：yield 逐个产出结果（惰性）
def fibonacci_gen(n):
    """生成斐波那契数列前 n 项 — 用到才计算"""
    a, b = 0, 1
    for _ in range(n):
        yield a             # ← yield！不是 return！
        a, b = b, a + b

# 使用对比
print("列表方式（全部在内存里）:")
fib_list = fibonacci_list(10)
print(f"  {fib_list}")
print(f"  类型: {type(fib_list)}")

print("\n生成器方式（惰性）:")
fib_gen = fibonacci_gen(10)
print(f"  类型: {type(fib_gen)}")  # <class 'generator'>
print(f"  下一个: {next(fib_gen)}")  # 0
print(f"  下一个: {next(fib_gen)}")  # 1
print(f"  下一个: {next(fib_gen)}")  # 1
print(f"  剩余用 for 遍历: ", end="")
for num in fib_gen:                   # 从第 4 个开始继续
    print(num, end=" ")
print()

# yield 的执行模型（关键理解！）：
# 1. 调用 fibonacci_gen(10) 不执行函数体，返回一个生成器对象
# 2. 每次 next() 或 for 迭代，执行到下一个 yield，暂停并返回值
# 3. 下次继续从暂停处往后执行
# 4. 函数执行完毕时自动抛出 StopIteration（for 循环自动处理）

# 可视化执行过程
print("\n--- yield 执行过程 ---")
def demo_yield():
    print("  开始")
    yield 1
    print("  恢复，准备 yield 2")
    yield 2
    print("  恢复，准备 yield 3")
    yield 3
    print("  结束")

gen = demo_yield()
print("  next #1:", next(gen))
print("  next #2:", next(gen))
print("  next #3:", next(gen))
# next(gen)  # 会抛 StopIteration

# C++ 对比：最接近的是 C++20 的 coroutine（co_yield）
# 或者自己写迭代器类，保存状态、重载 operator++ 和 operator*
# Python 的 yield 比 C++ 简洁太多！


# 2.2 生成器表达式 — 列表推导式的"惰性版"
print("\n=== 2.2 生成器表达式 ===")

# 列表推导式：用 []，立即求值
squares_list = [x**2 for x in range(10)]
print(f"列表推导式: {squares_list}")    # 全部在内存中
print(f"  类型: {type(squares_list)}")

# 生成器表达式：用 ()，惰性求值
squares_gen = (x**2 for x in range(10))
print(f"生成器表达式: {squares_gen}")    # 只是一个生成器对象
print(f"  类型: {type(squares_gen)}")

# 逐个消费
print("  逐个消费:", end=" ")
for sq in squares_gen:
    print(sq, end=" ")
print()

# 生成器表达式可以直接传给 sum/max/min 等函数（省内存！）
print(f"sum(x**2 for x in range(10)) = {sum(x**2 for x in range(10))}")
# 注意：传给函数时如果只有这一个参数，可以省略外层的 ()

# 对比内存占用（概念演示）：
# 列表：[x**2 for x in range(1000000)]    → ~8MB
# 生成器：(x**2 for x in range(1000000))  → ~80 bytes
# 生成器不持有数据，只持有"如何生成下一个数据"的规则

# C++ 对比：
# C++20 ranges/views 可以做到类似效果：
# auto squares = views::iota(0, 10) | views::transform([](int x){ return x*x; });


# 2.3 实用生成器模式
print("\n=== 2.3 实用生成器模式 ===")

# 模式1：无限序列
print("--- 无限序列 ---")
def infinite_counter(start=0):
    """无限计数器 — 永远不会自己停止"""
    n = start
    while True:
        yield n
        n += 1

counter = infinite_counter(100)
print(f"  {[next(counter) for _ in range(5)]}")  # [100, 101, 102, 103, 104]

# 模式2：逐行读取大文件（内存友好）
print("--- 逐行读取（模拟） ---")
def read_large_file_simulated():
    """模拟逐行读取大文件 — 一次只读一行到内存"""
    lines = ["第1行内容", "第2行内容", "第3行内容"]
    for line in lines:
        yield line.strip()

for line in read_large_file_simulated():
    print(f"  处理: {line}")

# 模式3：管道式数据处理
print("--- 管道式数据处理 ---")
def numbers():
    for i in range(1, 21):
        yield i

def filter_even(gen):
    for n in gen:
        if n % 2 == 0:
            yield n

def square(gen):
    for n in gen:
        yield n * n

# 管道：numbers → filter_even → square
pipeline = square(filter_even(numbers()))
print(f"  结果: {list(pipeline)}")  # [4, 16, 36, 64, 100, 144, 196, 256, 324, 400]

# 每个阶段都是惰性的，内存高效！


# ============================================================
# 第三部分：装饰器 — @decorator
# ============================================================
#
# 装饰器快速理解（先看这个！）：
#
#   第一层：函数就是"东西"，可以传来传去
#       f = say_hello    # 把函数赋给变量（没有括号！）
#       f()              # 调用它
#       → Python 的函数是一等公民，和数字、字符串一样可以赋值、传参
#
#   第二层：函数可以包一层"壳"
#       def add_lines(func):       # 接收"被包装的函数"
#           def wrapper():          # 造一个"壳函数"
#               print("---")       # 前面加点料
#               func()             # 调用原函数
#               print("---")       # 后面加点料
#           return wrapper          # 返回这个壳
#
#       say_hello = add_lines(say_hello)  # 包起来
#       → 这个 add_lines 就是装饰器的本质！
#       → 接收一个函数，返回一个"加强版"函数
#
#   第三层：@ 只是简写
#       @add_lines            ≈  say_hello = add_lines(say_hello)
#       def say_hello():
#           ...
#       → @ 语法糖，自动完成"包一层再重新赋值"
#       → 没有黑魔法，就这么简单
#
#   第四层：被装饰的函数有参数怎么办？
#       壳函数里用 *args, **kwargs 照单全收：
#       def wrapper(*args, **kwargs):
#           result = func(*args, **kwargs)   # 原样传入
#           return result
#       → *args = 所有位置参数打包
#       → **kwargs = 所有关键字参数打包
#       → 写装饰器时这俩几乎总是标配
#
#   第五层：装饰器自己也想要参数？（如 @rate_limit(max_per_second=2)）
#       再加一层！从"两层嵌套"变成"三层嵌套"：
#
#       def rate_limit(max_per_second):     # 第1层：接收装饰器参数
#           def decorator(func):            # 第2层：接收被装饰函数
#               def wrapper(*args, **kwargs): # 第3层：壳函数
#                   return func(*args, **kwargs)
#               return wrapper
#           return decorator
#
#       记忆技巧：
#       ┌─────────────────────┬────────────┬──────────────────┐
#       │ 写法                 │ 嵌套层数    │ 谁接收谁          │
#       ├─────────────────────┼────────────┼──────────────────┤
#       │ @timer              │ 2 层       │ func → wrapper   │
#       │ @timer(verbose=True)│ 3 层       │ 参数 → func → wrapper │
#       └─────────────────────┴────────────┴──────────────────┘
#
#   总结一句话：装饰器 = 闭包 + 函数作为参数
#   三步写装饰器：
#     1. 写一个函数，接收 func 参数
#     2. 里面定义 wrapper(*args, **kwargs)，调用 func 前后加点料
#     3. 返回 wrapper（别忘了 @wraps(func)）


print("\n" + "=" * 60)
print("第三部分：装饰器（Decorator）")
print("=" * 60)

# 3.0 前置知识：函数是一等公民
print("\n=== 3.0 前置：函数是一等公民 ===")

# 在 Python 中，函数就是对象！可以：
# 1. 赋值给变量
# 2. 作为参数传递
# 3. 从函数中返回
# 4. 存储在数据结构中

def greet(name):
    return f"你好，{name}！"

say_hello = greet               # 函数赋值给变量
print(say_hello("张三"))        # 通过变量调用
print(f"函数名: {greet.__name__}")     # greet

def call_twice(func, arg):
    """接收函数作为参数"""
    return func(arg) + " " + func(arg)

print(call_twice(greet, "李四"))

# C++ 对比：函数指针、std::function、lambda
# void (*ptr)(int) = &foo;       // C 风格函数指针
# std::function<void(int)> f;    // C++11
# Python 的函数对象更简单直接


# 3.1 闭包复习 — 装饰器的基础
print("\n=== 3.1 闭包（Closure）复习 ===")

def make_multiplier(n):
    """返回一个能乘以 n 的函数"""
    def multiplier(x):
        return x * n            # n 来自外层函数，被"捕获"了
    return multiplier

times_3 = make_multiplier(3)
times_5 = make_multiplier(5)
print(f"times_3(10) = {times_3(10)}")   # 30
print(f"times_5(10) = {times_5(10)}")   # 50

# 闭包 = 函数 + 它捕获的外部变量
# C++ 对比：lambda 捕获 [n](int x) { return x * n; }


# 3.2 什么是装饰器？
print("\n=== 3.2 什么是装饰器？ ===")

# 装饰器 = 一个函数，它接收一个函数，返回一个新函数
# 用于在不修改原函数代码的情况下，给函数添加功能

# 需求：记录函数的调用日志
# 不用装饰器的方式（啰嗦）：
import time

def slow_function():
    time.sleep(0.5)
    return "完成"

# 每次调用都要手动写 log...
# start = time.time()
# result = slow_function()
# print(f"slow_function 耗时：{time.time() - start:.2f}s")

# 用装饰器的方式（优雅）：

def timer(func):
    """装饰器：测量函数执行时间"""
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)       # 调用原函数
        elapsed = time.time() - start
        print(f"[timer] {func.__name__} 耗时 {elapsed:.3f}s")
        return result
    return wrapper                          # 返回包装后的函数

# 使用装饰器（语法糖 @）
@timer
def slow_function():
    time.sleep(0.5)
    return "完成"

print(slow_function())

# 等价于：
# slow_function = timer(slow_function)

# 装饰器的本质：
# @decorator
# def func():
#     ...
# 等价于 ↓
# func = decorator(func)


# 3.3 装饰器执行顺序和叠加
print("\n=== 3.3 装饰器叠加 ===")

def bold(func):
    def wrapper(*args, **kwargs):
        return f"<b>{func(*args, **kwargs)}</b>"
    return wrapper

def italic(func):
    def wrapper(*args, **kwargs):
        return f"<i>{func(*args, **kwargs)}</i>"
    return wrapper

@bold
@italic                             # 从下往上执行！
def hello(name):
    return f"Hello, {name}!"

print(hello("World"))               # <b><i>Hello, World!</i></b>
# 执行顺序：
# 1. hello = italic(hello)        → hello 变成 italic 包装版
# 2. hello = bold(italic版hello)  → hello 变成 bold 包装 italic 版
# 3. 调用：bold.wrapper → italic.wrapper → 原始hello


# 3.4 带参数的装饰器
print("\n=== 3.4 带参数的装饰器 ===")

# 需求：想让 @timer 可以指定是否打印详细信息
# 这需要三层嵌套！

def timer_advanced(verbose=True):
    """装饰器工厂：返回一个装饰器"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            elapsed = time.time() - start
            if verbose:
                print(f"[timer] {func.__name__}({args}, {kwargs}) → {elapsed:.3f}s")
            else:
                print(f"[timer] {func.__name__} → {elapsed:.3f}s")
            return result
        return wrapper
    return decorator

@timer_advanced(verbose=True)       # 先调用 timer_advanced(verbose=True)，返回 decorator，再装饰
def compute(n):
    total = sum(range(n))
    return total

@timer_advanced(verbose=False)
def compute_silent(n):
    total = sum(range(n))
    return total

print(f"compute(1000000) = {compute(1000000)}")
print(f"compute_silent(1000000) = {compute_silent(1000000)}")

# 三层嵌套的拆解：
# timer_advanced(verbose=True) → 返回 decorator
# decorator(func)              → 返回 wrapper
# wrapper(*args, **kwargs)      → 执行原函数 + 计时


# 3.5 functools.wraps — 保留原函数信息
print("\n=== 3.5 functools.wraps — 保留元数据 ===")

# 问题：装饰后函数丢失了原来的名字和文档
def bad_decorator(func):
    def wrapper(*args, **kwargs):
        """我是 wrapper 的文档"""
        return func(*args, **kwargs)
    return wrapper

@bad_decorator
def my_func():
    """我是 my_func 的文档"""
    pass

print(f"没有 wraps:")
print(f"  __name__: {my_func.__name__}")   # wrapper（丢失了原名！）
print(f"  __doc__ : {my_func.__doc__}")    # 我是 wrapper 的文档

# 解决方案：functools.wraps
from functools import wraps

def good_decorator(func):
    @wraps(func)                # ← 复制原函数的元数据
    def wrapper(*args, **kwargs):
        """我是 wrapper 的文档"""
        return func(*args, **kwargs)
    return wrapper

@good_decorator
def my_func2():
    """我是 my_func2 的文档"""
    pass

print(f"\n有 wraps:")
print(f"  __name__: {my_func2.__name__}")   # my_func2（保留了！）
print(f"  __doc__ : {my_func2.__doc__}")     # 我是 my_func2 的文档

# 写装饰器时，总是用 @wraps(func) ！


# 3.6 常用内置装饰器
print("\n=== 3.6 常用内置装饰器 ===")

# @staticmethod  @classmethod  @property — Day 6 学过
# 这里再补充几个

# @lru_cache — 缓存函数结果（Memoization）
print("--- @lru_cache ---")
from functools import lru_cache

call_count = 0

@lru_cache(maxsize=128)         # 缓存最近 128 次调用结果
def fibonacci(n):
    global call_count
    call_count += 1
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(f"fib(30) = {fibonacci(30)}")
print(f"实际计算次数: {call_count}")  # 31（没有缓存的话要算 269 万次！）

# [!] 缓存前：fib(30) 要递归计算约 269 万次
# 缓存后：每个 n 只算一次，共 31 次！
# 这就是动态规划的表驱动 vs 递归的本质区别


# ============================================================
# 综合示例：模拟一个"请求 API → 失败重试 → 收集数据"的流程
# ============================================================
#
# 场景设定：
#   你要从远程 API 拉取学生列表。网络不稳定，偶尔会失败。
#   你希望：失败了自动重试，最后把所有拿到的数据汇总。
#
# 用到的知识点：
#   - 自定义异常：NetworkError
#   - 装饰器：@retry_on_network_error（失败自动重试）
#   - 生成器：fetch_students_page()（惰性分页，用到了才请求下一页）
#   - 异常处理：try/except 捕获错误后决定"继续"还是"放弃"
#
# 整体关系图：
#
#   ┌─────────────────────────────────────────┐
#   │  collect_all_students()   ← 总调度      │
#   │  @retry_on_network_error(max_tries=3)    │
#   │                                          │
#   │  try:                                    │
#   │    for data in fetch_students_page():    │
#   │      收集 data                           │
#   │  except NetworkError:                    │
#   │    跳过这一页，继续下一页                  │
#   └───────┬─────────────────────────────────┘
#           │ 调用（每次迭代触发）
#           ▼
#   ┌──────────────────────┐
#   │  fetch_students_page │  ← 分页生成器
#   │  yield 第1页         │
#   │  yield 第2页         │    30% 概率 raise NetworkError
#   │  yield 第3页         │
#   └──────────────────────┘
#
# 注意：装饰器不能直接装饰生成器！
# 原因：调用生成器函数只返回一个 generator 对象，不执行函数体。
#      真正执行（可能抛异常）发生在 for 循环迭代时。
#      所以这里的 @retry 装饰在 collect_all_students（普通函数）上，
#      而不是 fetch_students_page（生成器）上。

print("\n" + "=" * 60)
print("综合示例：装饰器 + 异常处理 + 生成器")
print("=" * 60)

import random

# ── 第 1 块：自定义异常 ──
print("\n--- 第 1 块：自定义异常 ---")

class NetworkError(Exception):
    """网络请求失败"""
    pass

# 就一行：继承 Exception，搞定。C++ 要写整个类体，Python 一个 pass 就行。

# ── 第 2 块：生成器（分页获取数据） ──
print("--- 第 2 块：分页获取（生成器） ---")

def fetch_students_page(url, total_pages=3):
    """
    生成器函数：一页一页地从 API 拉数据。
    每页 30% 概率失败（模拟网络不稳定）。

    关键：用 yield 而不是 return！
    → 调用者"要一页"，才去"请求一页"
    → 不是一口气把所有页都拉回来
    """
    for page in range(1, total_pages + 1):
        # 模拟：30% 概率网络故障
        if random.random() < 0.3:
            raise NetworkError(f"请求 {url}?page={page} 时网络超时")
        # 成功：返回这一页的数据
        students = [f"student_{page}_{i}" for i in range(1, 4)]
        yield {"page": page, "students": students}
        #      ↑ yield = "给你，我在这儿暂停，下次从这继续"

# 演示生成器的"暂停-恢复"特性
# 固定随机种子，让前两页一定成功（方便演示）
random.seed(42)
gen = fetch_students_page("/api/students", total_pages=3)
print(f"生成器对象: {gen}")
try:
    print(f"  next #1: {next(gen)}")  # 第1页 → 执行到第一个 yield，暂停
    print(f"  next #2: {next(gen)}")  # 第2页 → 从暂停处继续，再次暂停
    # 不再调用 next(gen)，第3页永远不会被请求！
    # 这就是"惰性"：不请求就不会浪费资源
except NetworkError:
    print("  (演示中遇到了随机失败，这不影响理解生成器的暂停-恢复机制)")

# ── 第 3 块：带重试的装饰器 ──
print("\n--- 第 3 块：@retry_on_network_error 装饰器 ---")

def retry_on_network_error(max_tries=3, delay=0.1):
    """
    装饰器：被装饰的函数如果抛出 NetworkError，自动重试。

    这不是装饰生成器的！是装饰 collect_all_students 这种"调度函数"的。
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(1, max_tries + 1):      # 第1次、第2次、第3次
                try:
                    result = func(*args, **kwargs)       # 调用被装饰的函数
                    return result                         # 成功 → 直接返回
                except NetworkError as e:
                    last_error = e
                    print(f"  [重试 {attempt}/{max_tries}] {e}")
                    if attempt < max_tries:
                        time.sleep(delay)                 # 等一会儿再试
            # 所有尝试都失败了
            raise last_error
        return wrapper
    return decorator

# ── 第 4 块：用装饰器和生成器拼出完整逻辑 ──
print("--- 第 4 块：组合在一起 ---")

@retry_on_network_error(max_tries=3)
def collect_all_students(url, total_pages=3):
    """
    收集所有分页的学生数据。

    逻辑很简单：
      遍历生成器的每一页 → 成功就存起来 → 某页失败？
      NetworkError 会被 @retry_on_network_error 捕获，整个函数重来一遍。
    """
    all_students = []
    for page_data in fetch_students_page(url, total_pages):
        print(f"  [OK] 第{page_data['page']}页: {page_data['students']}")
        all_students.extend(page_data['students'])
    return all_students

# ── 测试 ──
print("\n=== 开始测试 ===")
random.seed(123)  # 固定随机种子，结果可复现

try:
    result = collect_all_students("/api/students", total_pages=3)
    print(f"\n最终收集到 {len(result)} 个学生: {result}")
except NetworkError:
    print(f"\n[!] 重试 3 次全部失败，放弃")

print("\n=== 另一种写法：逐页容错 ===\n")
# 如果你不想"整个函数重试"，而是"失败一页跳过，继续下一页"：

def collect_skip_on_error(url, total_pages=3):
    """逐页处理：某一页失败 → 跳过它，继续拿后面的"""
    all_students = []
    for page in range(1, total_pages + 1):
        try:
            gen = fetch_students_page(url, total_pages)
            # 跳过前面已处理过的页
            for _ in range(page - 1):
                next(gen)
            page_data = next(gen)
            all_students.extend(page_data['students'])
            print(f"  [OK] 第{page}页获取成功")
        except NetworkError as e:
            print(f"  [SKIP] 第{page}页失败: {e}，跳过")
    return all_students

random.seed(456)
result2 = collect_skip_on_error("/api/students", total_pages=3)
print(f"逐页容错模式收集到 {len(result2)} 个学生: {result2}")

# ── 关键要点总结 ──
print("\n" + "=" * 60)
print("综合示例要点回顾")
print("=" * 60)
print("""
1. 装饰器不能直接装饰生成器 — 生成器在 for 迭代时才执行，
   装饰器的 wrapper 只包裹了"创建生成器"这一步，捕获不到迭代时的异常。

2. 两种错误处理策略：
   - 整体重试：@retry 装饰在调度函数上，失败整个重来
   - 逐页跳过：try/except 包住单次迭代，失败就跳过

3. 生成器的优势：不必一次性拉回全部数据，惰性获取，
   如果提前退出（break/异常），后面的页根本不会请求。

4. 装饰器的优势：重试逻辑只写一次，@ 一行加到任何函数上就行。
""")


# ============================================================
# C++ → Python 速查表（Day 7 主题）
# ============================================================
"""
┌──────────────────────┬───────────────────────────────┬──────────────────────────────┐
│ 概念                  │ C++                            │ Python                       │
├──────────────────────┼───────────────────────────────┼──────────────────────────────┤
│ 异常捕获              │ try { } catch (T& e) { }       │ try: except T as e:          │
│ 抛出异常              │ throw T(args);                 │ raise T(args)                │
│ 重新抛出              │ throw;                         │ raise                        │
│ 自定义异常            │ class E : public exception {}   │ class E(Exception): pass     │
│ 获取异常信息          │ e.what()                       │ str(e) / type(e).__name__     │
│ 无异常时执行           │ 无                             │ else:（Python 独有）           │
│ 总是执行              │ finally { }                    │ finally:                     │
│ 惰性迭代器            │ C++20 coroutine / 手写迭代器    │ yield（生成器）               │
│ 生成器表达式           │ ranges/views（C++20）           │ (x**2 for x in range(10))    │
│ 消耗生成器            │ 迭代器自增                     │ next(gen) / for x in gen     │
│ 函数作为参数           │ std::function / 函数指针       │ 函数名直接传递                │
│ 装饰器                │ 无直接等价（靠宏/代理模式）       │ @decorator（语法糖）           │
│ 缓存/Memoization      │ 自己实现                       │ @lru_cache                   │
│ 保留元数据            │ 不适用                         │ @wraps(func)                 │
│ 重试机制              │ 手写循环                       │ 用装饰器封装                  │
└──────────────────────┴───────────────────────────────┴──────────────────────────────┘
"""

# ============================================================
# 常见问题解答（Q&A）
# ============================================================
print("\n" + "=" * 60)
print("常见问题解答")
print("=" * 60)

# Q1: 什么时候该捕获异常，什么时候该让它崩溃？
print("\n--- Q1: 异常处理策略 ---")
print("能处理 → 捕获（如重试、给默认值、提示用户）")
print("处理不了 → 不捕获，让上层处理（Fail Fast 原则）")
print("不要写空的 except: pass，会隐藏 bug！")

# Q2: yield 和 return 能同时用吗？
print("\n--- Q2: yield 和 return ---")
print("Python 3.3+ 可以在生成器里写 return xxx")
print("return 的值存在 StopIteration.value 中")
print("但 for 循环会自动忽略它，需要手动 next() 获取")
print("一般还是只用 yield，需要早期退出时用 return（不带值）")

# Q3: 装饰器好难理解，怎么学？
print("\n--- Q3: 装饰器学习建议 ---")
print("1. 先理解函数是一等公民（可以当参数传）")
print("2. 再理解闭包（内层函数捕获外层变量）")
print("3. 然后理解无参装饰器（timer = 闭包 + 函数参数）")
print("4. 最后理解有参装饰器（再加一层！）")
print("5. 自己动手写几个就懂了")

# Q4: 什么时候用生成器而不是列表？
print("\n--- Q4: 生成器 vs 列表 ---")
print("用生成器的场景：处理大文件、无限序列、管道处理")
print("用列表的场景：需要多次遍历、随机访问、数据量小的结果集")
print("简单判断：数据量可能很大 → 用生成器；否则用列表")

print("\n[OK] Day 7 笔记结束！打开 day07_exercise.py 做练习吧。")
