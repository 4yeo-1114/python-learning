"""
============================================================
Day 7 练习答案：异常处理 + 生成器 + 装饰器
============================================================
"""

import time
import random
from functools import wraps


# ============================================================
# 练习 1：安全的计算器
# ============================================================

def safe_calculate(a, b, operator):
    """
    安全计算器，能处理除零和类型错误。

    参数:
        a, b: 操作数
        operator: '+', '-', '*', '/'
    返回:
        计算结果 或 错误信息字符串
    """
    # 先验证运算符
    if operator not in ('+', '-', '*', '/'):
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
        return "错误：操作数类型不正确"
    else:
        print("计算成功")
        return result
    finally:
        print("计算结束")


# ============================================================
# 练习 2：斐波那契生成器 + 过滤
# ============================================================

def fibonacci_gen(n):
    """
    生成器：生成前 n 个斐波那契数。

    Args:
        n: 要生成的个数
    Yields:
        斐波那契数列的第 i 项
    """
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b


def filter_odd(gen):
    """
    生成器：从数字生成器中过滤出奇数。

    Args:
        gen: 数字生成器（或任何可迭代对象）
    Yields:
        奇数
    """
    for num in gen:
        if num % 2 == 1:
            yield num


# ============================================================
# 练习 3：装饰器 — 日志 + 限速
# ============================================================

def log_call(func):
    """装饰器：记录函数的调用和返回。"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 格式化参数
        arg_str = ", ".join(
            [repr(a) for a in args] +
            [f"{k}={v!r}" for k, v in kwargs.items()]
        )
        print(f"[LOG] 调用 {func.__name__}({arg_str})")
        result = func(*args, **kwargs)
        print(f"[LOG] {func.__name__} 返回 {result!r}")
        return result
    return wrapper


def rate_limit(max_per_second):
    """
    装饰器工厂：限制函数每秒最多被调用 max_per_second 次。

    用闭包维护调用时间戳列表，每次检查最近 1 秒内的调用次数。
    """
    def decorator(func):
        call_times = []  # 闭包变量：记录调用时间戳

        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            # 清理 1 秒之前的记录
            call_times[:] = [t for t in call_times if now - t < 1.0]

            if len(call_times) >= max_per_second:
                raise RuntimeError(
                    f"调用太频繁！{func.__name__} 每秒最多 {max_per_second} 次"
                )

            call_times.append(now)
            return func(*args, **kwargs)

        return wrapper
    return decorator


# ============================================================
# 练习 4（综合题）：带重试和缓存的网页内容获取器
# ============================================================

class FetchError(Exception):
    """自定义异常：获取数据失败。"""
    def __init__(self, url, reason):
        self.url = url
        self.reason = reason
        super().__init__(f"获取 {url} 失败：{reason}")


def retry_on_failure(max_retries):
    """
    装饰器工厂：失败自动重试（仅对 FetchError 生效）。

    装饰器内部是一个生成器包装器，用 yield from 委托给原生成器，
    确保装饰后的函数仍然是生成器。
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 原函数是生成器，wrapper 也应该是生成器
            # 但重试逻辑需要在"消费"层面处理
            # 这里的设计是：wrapper 返回生成器，重试在 safe_fetch_all 层完成
            # 简化处理：直接在 wrapper 中消费原生成器，逐个 yield 并处理异常
            gen = func(*args, **kwargs)
            while True:
                try:
                    item = next(gen)
                    yield item
                except StopIteration:
                    break
                except FetchError as e:
                    # 当前版本的简化处理：直接传播
                    # 重试逻辑在 safe_fetch_all 中手动处理
                    raise

        return wrapper
    return decorator


# 为了正确实现重试，我们提供一个更合理的版本：
# 把重试逻辑放在 safe_fetch_all 函数中，而不是装饰器中
# 因为生成器函数内的异常需要在消费端处理

def fetch_all(urls):
    """
    生成器：逐条获取 URL 内容。

    模拟：40% 概率失败。

    Args:
        urls: URL 列表
    Yields:
        dict: {'url': url, 'content': '...'}
    Raises:
        FetchError: 获取失败时抛出
    """
    for url in urls:
        if random.random() < 0.4:  # 40% 概率失败
            raise FetchError(url, "网络超时")
        yield {'url': url, 'content': f'{url}的内容'}


def safe_fetch_all(urls, max_retries=2):
    """
    安全获取所有 URL 的内容，带重试机制。

    Args:
        urls: URL 列表
        max_retries: 每个 URL 最大重试次数
    Returns:
        list: 成功获取的内容列表
    """
    results = []

    for url in urls:
        success = False
        for attempt in range(1, max_retries + 2):  # 首次 + N 次重试
            try:
                # 重新创建生成器（每次重试都从头开始）
                gen = fetch_all([url])
                item = next(gen) #拿到第一个结果
                results.append(item)
                print(f"[{url}] OK")
                success = True
                break
            except FetchError as e:
                if attempt <= max_retries:
                    print(f"[{url}] 失败: {e.reason}")
                    print(f"  重试 {attempt}/{max_retries}...")
                else:
                    print(f"[{url}] 最终失败，跳过")

    return results


# ============================================================
# 测试代码
# ============================================================
if __name__ == '__main__':
    print("=" * 60)
    print("练习 1：安全的计算器")
    print("=" * 60)
    print("safe_calculate(10, 2, '+'):", safe_calculate(10, 2, '+'))
    print()
    print("safe_calculate(10, 0, '/'):", safe_calculate(10, 0, '/'))
    print()
    print("safe_calculate(10, 'abc', '+'):", safe_calculate(10, 'abc', '+'))
    print()
    try:
        safe_calculate(10, 2, '^')
    except ValueError as e:
        print(f"捕获 ValueError: {e}")

    print("\n" + "=" * 60)
    print("练习 2：斐波那契生成器 + 过滤")
    print("=" * 60)
    print("前 20 个斐波那契数:", list(fibonacci_gen(20)))
    print("前 20 个斐波那契数中的奇数:", list(filter_odd(fibonacci_gen(20))))

    print("\n" + "=" * 60)
    print("练习 3：装饰器 — 日志 + 限速")
    print("=" * 60)

    @log_call
    def add(a, b):
        return a + b

    print("测试 @log_call:")
    result = add(3, 5)
    print()

    @log_call
    def greet(name, greeting="你好"):
        return f"{greeting}，{name}！"

    greet("张三")
    print()

    print("测试 @rate_limit(max_per_second=2):")
    @rate_limit(max_per_second=2)
    def ping():
        return "pong"

    print("  第1次:", ping())
    print("  第2次:", ping())
    try:
        print("  第3次:", ping())  # 应该失败
    except RuntimeError as e:
        print(f"  第3次: RuntimeError — {e}")

    print(f"\n  等待 1 秒后重试...")
    time.sleep(1.1)
    print("  第4次:", ping())    # 应该成功

    print("\n" + "=" * 60)
    print("练习 4：带重试的网页内容获取器")
    print("=" * 60)
    random.seed(42)  # 固定随机种子，保证可复现
    urls = ['/api/a', '/api/b', '/api/c', '/api/d', '/api/e']
    results = safe_fetch_all(urls, max_retries=2)
    print(f"\n成功获取: {len(results)} 条")
    for item in results:
        print(f"  {item}")
