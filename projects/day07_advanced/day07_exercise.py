"""
============================================================
Day 7 练习：异常处理 + 生成器 + 装饰器
============================================================
完成以下 4 道练习题，巩固今天所学的三大主题。
答案见 day07_solution.py
"""

# ============================================================
# 练习 1：安全的计算器
# ============================================================
"""
题目：实现一个 safe_calculator() 函数，模拟一个简单的计算器。

要求：
1. 实现函数 safe_calculate(a, b, operator)，参数：
   - a, b: 两个数字
   - operator: 字符串，取值为 '+', '-', '*', '/'
2. 使用 try/except/else/finally 处理以下异常：
   - 除法时 b 为 0 → 捕获 ZeroDivisionError，返回错误信息
   - a 或 b 不是数字（如传入字符串）→ 捕获 TypeError，返回错误信息
   - operator 不是四个运算符之一 → 用 raise 抛出 ValueError
3. else 分支打印 "计算成功"
4. finally 分支打印 "计算结束"

调用示例：
safe_calculate(10, 2, '+')   → 返回 12
safe_calculate(10, 0, '/')   → 返回 "错误：不能除以零"
safe_calculate(10, 'abc', '+') → 返回 "错误：操作数类型不正确"
safe_calculate(10, 2, '^')   → 抛出 ValueError
"""

# TODO: 在这里实现 safe_calculate 函数
def safe_calculate(a,b,operator):
   if operator not in ('+','-','*','/'):
      raise ValueError(f"不支持的运算符：'{operator}'，只支持 + - * /")
   
   try:
           if operator == '+':
               result = a + b
           elif operator == '-':
               result = a - b
           elif operator == '*':
               result = a * b
           elif operator == '/':
               result = a / b
   except ZeroDivisionError:
      return "错误：不能除以零"
   except TypeError:
      return 错误：操作数类型不正确"
   else:
           print("计算成功")
           return result
       finally:
           print("计算结束")
   

# ============================================================
# 练习 2：斐波那契生成器 + 过滤
# ============================================================
"""
题目：用生成器实现斐波那契数列的过滤流水线。

要求：
1. 实现生成器函数 fibonacci_gen(n)，生成前 n 个斐波那契数
   （斐波那契数列：0, 1, 1, 2, 3, 5, 8, 13, 21, ...）
2. 实现生成器函数 filter_odd(gen)，从一个数字生成器中过滤出奇数
3. 用"管道"方式组合：生成前 20 个斐波那契数，从中筛选出所有奇数

调用示例：
list(filter_odd(fibonacci_gen(10)))
→ [1, 1, 3, 5, 13, 21]

# 提示：
# - a, b = 0, 1 作为起始
# - a, b = b, a + b 更新
# - 奇数判断：n % 2 == 1
"""

# TODO: 在这里实现 fibonacci_gen 函数
def fibonacci_gen(n):
   a,b = 0,1
   for _ in range(n):
      yield a
      a,b = b, a+b
   

# TODO: 在这里实现 filter_odd 函数

def filter_odd(gen):
   """gen: 数字生成器（或任何可迭代对象）"""
   for num in gen:
        if num % 2 == 1:
            yield num


# ============================================================
# 练习 3：装饰器 — 日志 + 限速
# ============================================================
"""
题目：实现两个装饰器。

第一个装饰器 @log_call：
- 每次调用被装饰的函数时，打印日志：
  "[LOG] 调用 {函数名}(参数...)"
- 函数返回时，打印：
  "[LOG] {函数名} 返回 {返回值}"
- 提示：用 functools.wraps 保留原函数元数据

第二个装饰器 @rate_limit(max_per_second)（带参数的装饰器）：
- 限制函数每秒最多被调用 max_per_second 次
- 如果超过限制，抛出 RuntimeError("调用太频繁！")
- 提示：用 time.time() 记录每次调用时间，用闭包保存调用历史

使用示例：
@log_call
def add(a, b):
    return a + b

add(3, 5)
# 输出：
# [LOG] 调用 add(3, 5)
# [LOG] add 返回 8

@rate_limit(max_per_second=2)
def ping():
    return "pong"

ping()  # 第1次，OK
ping()  # 第2次，OK
ping()  # 第3次（1秒内），RuntimeError!
"""

import time
from functools import wraps

# TODO: 在这里实现 @log_call 装饰器

# TODO: 在这里实现 @rate_limit(max_per_second) 装饰器

def log_call(func):
   @wraps(func)
   def wrapper(*args,**kwargs):
      #格式化参数
      arg_str = ",".join(
         [repr(a) for a in args]+
         {f"{k}={v!r}" for k , v in kwargs.items()}
      )
      print(f"[LOG]调用 {func.__name__}{arg_str}")
      result = func(*args,**kwargs)
      print(f"[LOG] {func.__name__} 返回 {result!r}")
      return result
   return wrapper



def rate_limit(max_per_second):
   """
   装饰器工厂：限制函数每秒最多被调用 max_per_second 次。
   
   用闭包维护调用时间戳列表，每次检查最近 1 秒内的调用次数。
   
   """
   def decorator(func):
      call_times = [] #闭包变量 记录时间戳
      
      @wraps(func)
      def wrapper(*args,**kwargs):
         now =  time.time()
         #清理一秒前的记录
         call_times[:] = [t for t in call_times if now - t < 1.0]
         
         if len(call_times) >= max_per_second:
            raise RuntimeError(f"调用太频繁!:{func.__name__} 每秒最多{max_per_second}次")
         call_times.append(now)
         return func(*args,**kwargs)
      
      return wrapper
   return decorator
   

# ============================================================
# 练习 4（综合题）：带重试和缓存的网页内容获取器
# ============================================================
"""
题目：综合运用异常处理、生成器、装饰器，模拟一个健壮的"网页内容获取器"。

背景：
你有一个数据源列表，有些数据源能正常获取（返回内容），
有些会超时或失败。你需要一个健壮的获取器。

要求：
1. 定义自定义异常 FetchError（继承 Exception），包含 url 和 reason 属性

2. 实现 @retry_on_failure(max_retries) 装饰器：
   - 被装饰函数如果抛出了 FetchError，自动重试
   - 达到 max_retries 后仍失败 → 抛出原始异常
   - 每次重试时打印 "  重试 {n}/{max_retries}..."

3. 实现生成器函数 fetch_all(urls)：
   - 遍历 urls 列表
   - 对每个 url，模拟获取（import random; random.random() < 0.4 则失败）
   - 成功时 yield {'url': url, 'content': f'{url}的内容'}
   - 失败时 raise FetchError(url, '网络超时')
   - 提示：用 @retry_on_failure(max_retries=2) 装饰这个函数

4. 实现 safe_fetch_all(urls) 函数：
   - 使用 fetch_all 生成器获取数据
   - 用 try/except 捕获 FetchError，打印错误信息，继续处理下一个
   - 收集成功获取的内容到列表并返回

使用示例：
urls = ['/api/a', '/api/b', '/api/c', '/api/d']
results = safe_fetch_all(urls)
# 可能输出（取决于随机）：
# [/api/a] OK
# [/api/b] 失败: 网络超时
#   重试 1/2...
# [/api/b] OK
# [/api/c] OK
# [/api/d] 失败: 网络超时
#   重试 1/2...
#   重试 2/2...
# [/api/d] 最终失败，跳过
#
# 成功获取: 3 条

提示：
- random.random() 返回 [0, 1) 之间的随机浮点数
- 装饰器 + 生成器的组合：wrapper 内部需要是生成器（用 yield from）
"""

import random
from functools import wraps

# TODO: 在这里定义 FetchError 异常类

# TODO: 在这里实现 @retry_on_failure(max_retries) 装饰器

# TODO: 在这里实现 fetch_all(urls) 生成器（用 @retry_on_failure）

# TODO: 在这里实现 safe_fetch_all(urls) 函数


# ============================================================
# 测试入口
# ============================================================
if __name__ == '__main__':
    print("=" * 60)
    print("Day 7 练习 — 请逐个完成各题，答案见 day07_solution.py")
    print("=" * 60)
