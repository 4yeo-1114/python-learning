"""
============================================================
Day 3: 文件操作 + 字符串方法 + 异常处理 + 模块导入（C++ 对比版）
============================================================
目标：掌握 Python 文件读写、字符串处理、异常捕获、模块组织
"""

# ============================================================
# 1. 字符串方法 — 更深入的字符串操作
# ============================================================
# Day 1 学了基础：f-string, input(), print()
# 今天学更强大的字符串处理能力

print("=== 1. 字符串方法 ===")

# 1.1 大小写转换
s = "Hello Python World"
print(f"原始:   '{s}'")
print(f"upper:  '{s.upper()}'")       # 全大写
print(f"lower:  '{s.lower()}'")       # 全小写
print(f"title:  '{s.title()}'")       # 每个单词首字母大写
print(f"swapcase: '{s.swapcase()}'")   # 大小写反转

# 1.2 空白处理
s2 = "   张三   "
print(f"\n原始:     '{s2}'")
print(f"strip:   '{s2.strip()}'")     # 去两端空白
print(f"lstrip:  '{s2.lstrip()}'")    # 去左端空白
print(f"rstrip:  '{s2.rstrip()}'")    # 去右端空白

# 1.3 查找与替换
text = "Python 很有趣，Python 很强大"
print(f"\ntext: '{text}'")
print(f"find 'Python': {text.find('Python')}")      # 第一个出现的索引，找不到返回 -1
print(f"rfind 'Python': {text.rfind('Python')}")    # 最后一个出现的索引
print(f"count 'Python': {text.count('Python')}")     # 出现次数
print(f"replace: '{text.replace('Python', 'Java')}'")  # 替换所有
print(f"replace once: '{text.replace('Python', 'Java', 1)}'")  # 只替换第一个

# 对比 C++：std::string 有 find/rfind，但 replace 是位置+长度，Python 是内容替换

# 1.4 判断方法（返回 True/False）— 数据校验超好用！
print(f"\n=== 字符串判断 ===")
print(f"'123'.isdigit()  = {'123'.isdigit()}")     # 全是数字？
print(f"'abc'.isalpha()  = {'abc'.isalpha()}")     # 全是字母？
print(f"'abc123'.isalnum() = {'abc123'.isalnum()}") # 全是字母或数字？
print(f"'  '.isspace()   = {'  '.isspace()}")      # 全是空白？
print(f"'Hello'.startswith('He') = {'Hello'.startswith('He')}")
print(f"'hello.py'.endswith('.py') = {'hello.py'.endswith('.py')}")

# 1.5 分割与连接 — 字符串 ↔ 列表的桥梁
print(f"\n=== 分割与连接 ===")
# split() — 字符串 → 列表
csv_line = "张三,20,计算机科学,北京"
fields = csv_line.split(",")           # 按逗号分割
print(f"split ',' : {fields}")

sentence = "Python   is   awesome"
words = sentence.split()               # 不传参数 = 按任意空白分割
print(f"split 空白: {words}")

# join() — 列表 → 字符串
joined = " | ".join(fields)            # 用 " | " 把列表连起来
print(f"join ' | ': '{joined}'")

path_parts = ["home", "user", "docs", "file.txt"]
path = "/".join(path_parts)            # 拼接路径
print(f"路径拼接: {path}")

# C++ 对比：split ≈ stringstream 循环，join ≈ 循环 + 手动添加分隔符


# ============================================================
# 2. 文件操作 — open() 和 with 上下文管理器
# ============================================================
# Python 的文件操作比 C++ 简洁太多了！
# C++ 需要 #include <fstream>，ofstream/ifstream，检查 .is_open()

print(f"\n=== 2. 文件操作 ===")

# 2.1 打开模式
# "r" — 只读（默认），文件不存在会报错
# "w" — 只写，文件存在则清空，不存在则创建
# "a" — 追加，在文件末尾添加
# "r+" — 读写，文件必须存在
# 加上 "b" 表示二进制模式，如 "rb", "wb"
# 加上 encoding="utf-8" 指定编码（处理中文必备！）

# 2.2 写入文件
with open("day03_demo.txt", "w", encoding="utf-8") as f:
    f.write("第一行:Hello Python!\n")
    f.write("第二行：文件操作很简单\n")
    f.writelines(["第三行：列表写入\n", "第四行：一行一个\n"])

print("文件已写入: day03_demo.txt")

# 2.3 读取文件（多种方式）
print("\n--- 方式1: f.read() — 一次读全部 ---")
with open("day03_demo.txt", "r", encoding="utf-8") as f:
    content = f.read()              # 整个文件读成一个字符串
    print(content)

print("--- 方式2: f.readlines() — 一次读到列表 ---")
with open("day03_demo.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()           # 每行是一个元素（含 \n）
    for i, line in enumerate(lines, 1):
        print(f"  行{i}: {line.rstrip()}")  # rstrip 去掉末尾换行

print("--- 方式3: 逐行迭代（推荐！省内存） ---")
with open("day03_demo.txt", "r", encoding="utf-8") as f:
    for line in f:                  # 文件对象本身可迭代！
        print(f"  > {line.rstrip()}")

# C++ 对比：
# ifstream fin("file.txt");
# string line;
# while (getline(fin, line)) { cout << line << endl; }

# 2.4 ⚠️ with 语句是关键！千万别用裸 open()
#
# ❌ 错误写法（C++ 习惯）：
# f = open("file.txt", "r")
# content = f.read()
# f.close()        # 容易忘记！中途出错也不会执行
#
# ✅ 正确写法（Python 风格）：
# with open("file.txt", "r") as f:
#     content = f.read()
# # 缩进结束后自动关闭文件，即使中途出错也会关！
#
# with = C++ 的 RAII（资源获取即初始化），离开作用域自动释放

# 2.5 追加模式
with open("day03_demo.txt", "a", encoding="utf-8") as f:
    f.write("这是追加的内容\n")
print("已在文件末尾追加一行")


# ============================================================
# 3. 异常处理 — try/except
# ============================================================
# C++ 对比：try/catch/throw → Python 的 try/except/raise

print(f"\n=== 3. 异常处理 ===")

# 3.1 基本结构
print("\n--- 基本异常捕获 ---")
try:
    num = int(input("请输入一个整数: "))
    result = 100 / num
    print(f"100 / {num} = {result}")
except ValueError:
    print("❌ 输入的不是整数！")
except ZeroDivisionError:
    print("❌ 不能除以 0！")
except Exception as e:
    print(f"❌ 未知错误: {e}")
else:
    print("✅ 没有异常时执行 else 块")     # C++ 没有 else 块！
finally:
    print("无论如何都会执行 finally 块")    # 类似 C++ 的 finally（C++没有，需要手动）

# 3.2 常见的异常类型
# ValueError      — 类型转换失败
# ZeroDivisionError — 除以 0
# FileNotFoundError — 文件不存在
# KeyError        — 字典键不存在
# IndexError      — 列表索引越界
# TypeError       — 类型不匹配
# PermissionError — 权限不足

# 3.3 文件操作一定要加异常处理！
print("\n--- 安全的文件读取 ---")
def safe_read_file(filepath):
    """安全读取文件内容"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ 文件不存在: {filepath}")
        return None
    except PermissionError:
        print(f"❌ 没有读取权限: {filepath}")
        return None
    except Exception as e:
        print(f"❌ 读取失败: {e}")
        return None

content = safe_read_file("不存在的文件.txt")
print(f"读取结果: {content}")

content = safe_read_file("day03_demo.txt")
print(f"读取成功!前20字符: {content[:20] if content else 'None'}...")


# ============================================================
# 4. 模块导入 — import
# ============================================================
# C++ 对比：#include → Python 的 import
# #include 是文本复制粘贴，import 是运行时加载模块对象

print(f"\n=== 4. 模块导入 ===")

# 4.1 导入标准库模块
import os                            # 操作系统接口
import math                          # 数学函数
import json                          # JSON 处理
import random                        # 随机数

print(f"当前目录: {os.getcwd()}")
print(f"圆周率: {math.pi:.5f}")
print(f"随机数: {random.randint(1, 100)}")

# 4.2 导入方式对比
# 方式1: import 模块名 → 使用时加模块前缀
import datetime
today = datetime.date.today()
print(f"今天: {today}")

# 方式2: from 模块 import 具体内容 → 直接使用
from datetime import timedelta
tomorrow = today + timedelta(days=1)
print(f"明天: {tomorrow}")

# 方式3: from 模块 import * → 全部导入（不推荐！命名污染）
# from math import *

# 方式4: import 模块 as 别名 → 常用简称
import numpy as np                  # 数据分析库的约定别名
print(f"np 模块: {np}")              # 没有安装也没关系，只是演示语法

# 4.3 ⚠️ import vs #include 的关键区别
# C++ #include：预处理阶段把整个头文件内容复制粘贴过来
# Python import：运行时加载模块，创建一个模块对象，赋给同名变量
# → Python 的模块是真正的"对象"，可以打印、传递、查看属性

# 4.4 __name__ — 这个文件是被导入还是直接运行的？
print(f"\n当前模块的 __name__: {__name__}")
# 如果直接运行这个文件：__name__ == "__main__"
# 如果被别的文件 import：__name__ == "day03_notes"

# 标准写法（几乎每个 Python 文件都有）：
if __name__ == "__main__":
    print("这个文件是直接运行的，不是被 import 的")
    print("通常在这里放测试代码")


# ============================================================
# 5. 实战技巧：用文件存储数据
# ============================================================

print(f"\n=== 5. 实战：文件版通讯录 ===")

def save_contacts_to_file(contacts, filepath="contacts.txt"):
    """把通讯录列表保存到文件"""
    with open(filepath, "w", encoding="utf-8") as f:
        for contact in contacts:
            # 把每个联系人的字典转成一行文本
            line = f"{contact['name']},{contact['phone']},{contact.get('email', '')}\n"
            f.write(line)
    print(f"[OK] 已保存 {len(contacts)} 条记录到 {filepath}")

def load_contacts_from_file(filepath="contacts.txt"):
    """从文件加载通讯录"""
    contacts = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:           # 跳过空行
                    continue
                parts = line.split(",")
                if len(parts) >= 2:
                    contacts.append({
                        "name": parts[0],
                        "phone": parts[1],
                        "email": parts[2] if len(parts) > 2 else ""
                    })
        print(f"[OK] 已从 {filepath} 加载 {len(contacts)} 条记录")
    except FileNotFoundError:
        print(f"[提示] {filepath} 不存在，返回空列表")
    return contacts

# 演示：保存 → 加载
demo_contacts = [
    {"name": "张三", "phone": "13800138000", "email": "zhang@mail.com"},
    {"name": "李四", "phone": "13900139000", "email": "li@mail.com"},
]
save_contacts_to_file(demo_contacts)
loaded = load_contacts_from_file()
print(f"加载结果: {loaded}")


# ============================================================
# C++ → Python 速查表（文件操作 + 异常）
# ============================================================
"""
┌──────────────────────┬──────────────────────────┬──────────────────────────┐
│ 操作                  │ C++                       │ Python                    │
├──────────────────────┼──────────────────────────┼──────────────────────────┤
│ 读文件                │ ifstream fin("f.txt");    │ with open("f.txt") as f: │
│ 写文件                │ ofstream fout("f.txt");   │ with open("f.txt","w")   │
│ 读一行                │ getline(fin, line);       │ line = f.readline()      │
│ 读全部                │ stringstream + rdbuf      │ content = f.read()       │
│ 文件自动关闭           │ RAII（作用域结束）          │ with 语句离开缩进         │
│ 异常处理              │ try/catch/throw           │ try/except/raise         │
│ 分割字符串             │ stringstream + getline    │ s.split(",")             │
│ 连接字符串             │ 循环 + +                  │ "sep".join(list)         │
│ 去空白                │ trim（需自己写或 boost）    │ s.strip()                │
│ 查找子串              │ s.find("x")               │ s.find("x")              │
│ 模块/头文件           │ #include "file.h"         │ import module            │
└──────────────────────┴──────────────────────────┴──────────────────────────┘
"""

# ============================================================
# 常见问题解答（Q&A）
# ============================================================
print(f"\n=== 常见问题解答 ===")

# Q1: with open() 缩进结束了还能访问变量吗？
print("\n--- Q1: with 作用域 ---")
with open("day03_demo.txt", "r", encoding="utf-8") as f:
    data = f.read()
# 这里文件已关闭，但 data 变量还在！
print(f"文件已关闭，但 data 还在: {data[:30]}...")
# Python 没有块级作用域！with/if/for 都不创建新作用域
# 只有函数和类会创建新作用域 ← 和 C++ 完全不同！

# Q2: open 的 encoding 参数为什么重要？
print("\n--- Q2: encoding 参数 ---")
# Windows 默认编码是 gbk/cp936，不是 utf-8
# 不指定 encoding 可能导致：
# - 中文乱码
# - UnicodeDecodeError
# ⚠️ 读中文文件一律加 encoding="utf-8"

# Q3: Python 有 switch/case 吗？
print("\n--- Q3: switch/case ---")
# Python 3.10 之前没有，用 if/elif/else
# Python 3.10+ 有 match/case（模式匹配，比 switch 强大多了）
# 我们目前用 Python 3.14，可以用 match/case：
lang = "Python"
match lang:
    case "Python":
        print("你在学 Python")
    case "C++":
        print("这是你的母语")
    case _:                            # _ 是默认分支，类似 default
        print("其他语言")

print("\n[OK] Day 3 笔记结束！打开 day03_exercise.py 做练习吧。")
