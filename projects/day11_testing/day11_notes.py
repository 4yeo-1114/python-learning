"""
============================================================
Day 11: 单元测试入门 — pytest 框架（C++ 对比版）
============================================================
目标：学会用 pytest 写单元测试，理解"测试驱动"的思维模式
      这是从"写功能"到"验证功能"的思维转换
"""

# ============================================================
# 第一部分：为什么要写测试？
# ============================================================

print("=" * 60)
print("第一部分：为什么要写测试？")
print("=" * 60)

"""
之前的学习模式：
  写代码 → 手动运行 → 眼睛看输出 → 判断对不对

问题：
  - 每次改代码都要手动重跑一遍所有功能
  - 改 A 功能可能破坏 B 功能，你发现不了
  - 一个月后回来看代码，不敢改（怕改坏）

C++ 对比：
  C++ 中手动测试通常写个 main() 调各种函数，跑完看输出。
  Python 的 pytest 自动化了这个过程——你写测试函数，pytest 帮你跑。

测试的核心价值：
  ┌─────────────────────────────────────────────┐
  │  测试不是"找 bug"，而是"防止 bug"            │
  │  它让你在改代码时有安全感                    │
  │  每次改动后跑一遍测试，绿灯 = 没破坏          │
  └─────────────────────────────────────────────┘
"""


# ============================================================
# 第二部分：pytest 快速入门
# ============================================================

print("\n" + "=" * 60)
print("第二部分：pytest 快速入门")
print("=" * 60)

"""
2.1 安装
  pip install pytest

2.2 运行方式
  # 运行当前目录下所有测试
  pytest

  # 运行指定文件
  pytest test_xxx.py

  # 显示详细输出（打印 print 内容）
  pytest -v

  # 只运行包含特定关键词的测试
  pytest -k "password"

2.3 命名规则（pytest 会自动发现）
  - 测试文件必须以 test_ 开头或 _test 结尾：test_xxx.py
  - 测试函数必须以 test_ 开头：def test_xxx():
  - 测试类必须以 Test 开头（不含 __init__）

2.4 最简单的例子
"""

# ---- 被测试的函数 ----
def add(a, b):
    return a + b


# ---- 测试函数 ----
def test_add():
    """测试 add 函数"""
    assert add(1, 2) == 3       # 断言：add(1,2) 必须等于 3
    assert add(-1, 1) == 0      # 断言：add(-1,1) 必须等于 0
    assert add(0, 0) == 0       # 断言：add(0,0) 必须等于 0
    # 如果任何一个 assert 失败，pytest 会报告哪一行、期望什么、实际什么


print("运行: pytest test_add.py -v")
print("结果: test_add PASSED")

"""
C++ 对比：
  C++ 中你可能会用 assert() 宏：
    #include <cassert>
    assert(add(1, 2) == 3);
  Python 的 assert 也是内置关键字，语法一样，但 pytest 会给出更详细的失败信息。

2.5 测试函数 vs 普通函数
  - 测试函数命名描述"测什么"：test_空密码返回错误
  - 每个测试函数只测一件事
  - 用 assert 语句验证结果
  - 不要用 print，用 assert（pytest 只在失败时显示细节）
"""


# ============================================================
# 第三部分：fixture 夹具 — 准备测试环境
# ============================================================

print("\n" + "=" * 60)
print("第三部分：fixture 夹具")
print("=" * 60)

"""
3.1 什么是 fixture？
  正式测试前需要准备的东西——数据库连接、测试数据、临时文件等。

  类比：做化学实验前要准备试管、试剂、烧杯
        fixture 就是帮你准备好"实验器材"

3.2 为什么需要 fixture？
  问题场景：你要测试 UserDB 的注册功能
    → 需要先创建一个数据库
    → 测试完需要清理（删掉/回滚）
    → 每个测试之间不能互相影响

  fixture 帮你：
    - 在测试前自动创建资源
    - 在测试后自动清理资源
    - 多个测试共享同一个 fixture

3.3 fixture 基本用法
"""

import pytest
import sqlite3
import os


@pytest.fixture
def temp_db():
    """创建一个临时数据库，测试完自动删除"""
    db_path = "test_temp.db"
    conn = sqlite3.connect(db_path)
    conn.execute("CREATE TABLE test (id INTEGER, name TEXT)")
    conn.close()

    yield db_path  # ← yield 之前 = 测试前准备，之后 = 测试后清理

    # 清理：删除临时文件
    if os.path.exists(db_path):
        os.remove(db_path)


def test_use_temp_db(temp_db):  # ← 参数名 = fixture 名，pytest 自动注入
    """使用 temp_db fixture 的测试"""
    conn = sqlite3.connect(temp_db)
    conn.execute("INSERT INTO test VALUES (1, 'hello')")
    row = conn.execute("SELECT * FROM test").fetchone()
    conn.close()
    assert row == (1, "hello")
    # 测试结束后 temp_db 的清理代码自动执行


"""
fixture 的生命周期：
  yield 之前 ──→ 测试函数执行 ──→ yield 之后（清理）
  (setup)          (test)           (teardown)

C++ 对比：
  C++ 中你可能会在 SetUp() / TearDown() 方法中做类似的事
  （比如 Google Test 框架的 SetUp/TearDown）
  Python 的 fixture 更灵活——可以按需注入，可以嵌套依赖

3.4 :memory: 数据库 — 更好的测试方案
  测试数据库操作时，用 ':memory:' 代替文件路径：
    conn = sqlite3.connect(':memory:')

  优点：
    - 数据只在内存中，测试结束自动消失
    - 不需要清理文件
    - 速度快（没有磁盘 I/O）
"""


# ============================================================
# 第四部分：参数化测试 @parametrize
# ============================================================

print("\n" + "=" * 60)
print("第四部分：参数化测试")
print("=" * 60)

"""
4.1 什么叫参数化测试？
  同一个测试逻辑，用多组不同的输入/输出来跑。

  比如测试 validate_password：
    - 输入 "abc"   → 期望 (False, "密码至少需要 6 位")
    - 输入 "123456" → 期望 (False, "密码不能全是数字")
    - 输入 "abcdef" → 期望 (False, "密码不能全是字母")
    - 输入 "abc123" → 期望 (True, "密码有效")

  如果不用参数化，你要写 4 个几乎一样的测试函数。
  用 @parametrize，一个函数就能覆盖所有情况。

4.2 用法
"""

@pytest.mark.parametrize("password, expected_ok, expected_msg", [
    ("abc",     False, "密码至少需要 6 位"),
    ("123456",  False, "密码不能全是数字"),
    ("abcdef",  False, "密码不能全是字母"),
    ("abc123",  True,  "密码有效"),
])
def test_validate_password(password, expected_ok, expected_msg):
    """参数化测试：一次定义，多组数据"""
    # 这里调用真实的 validate_password 函数
    # ok, msg = validate_password(password)
    # assert ok == expected_ok
    # assert msg == expected_msg
    pass  # 实际测试在 solution 中


"""
pytest 运行这个测试时，会生成 4 个子测试：
  test_validate_password[abc]
  test_validate_password[123456]
  test_validate_password[abcdef]
  test_validate_password[abc123]

如果某个子测试失败，不影响其他子测试继续运行。

4.3 优点
  - 减少重复代码（DRY 原则）
  - 新增测试用例只需加一行数据
  - 失败时 pytest 明确告诉你哪组数据失败了
"""


# ============================================================
# 第五部分：测试数据库的正确姿势
# ============================================================

print("\n" + "=" * 60)
print("第五部分：测试数据库的正确姿势")
print("=" * 60)

"""
5.1 核心原则：测试之间不能互相影响

  错误做法 ❌：
    def test_register():
        db = UserDB("real.db")  # 操作真实数据库！
        db.register("admin", "pass")
        # 这个用户会一直留在数据库里，影响下次测试

  正确做法 ✅：
    @pytest.fixture
    def user_db():
        db = UserDB(":memory:")     # 或临时文件
        yield db
        # 内存数据库自动清理

    def test_register(user_db):
        user_db.register("admin", "pass")
        # 测试完数据消失，不影响其他测试

5.2 测试策略
  对于数据库操作类，通常测试：
    1. 正常操作 → 验证返回值和数据库状态
    2. 边界情况 → 空输入、重复数据、不存在的记录
    3. 异常情况 → 错误输入被正确处理

5.3 一个测试函数的典型结构（AAA 模式）
  Arrange   → 准备数据和环境
  Act       → 执行被测试的操作
  Assert    → 验证结果

  def test_register_success(user_db):
      # Arrange（准备）
      username, password = "admin", "admin123"

      # Act（执行）
      ok, msg = user_db.register(username, password)

      # Assert（验证）
      assert ok is True
      assert msg == "注册成功"
      assert user_db.count_users() == 1
"""


# ============================================================
# 第六部分：常用 assert 断言技巧
# ============================================================

print("\n" + "=" * 60)
print("第六部分：常用 assert 技巧")
print("=" * 60)

"""
6.1 基本断言
  assert x == y          # 相等
  assert x != y          # 不等
  assert x is True       # 是 True
  assert x is False      # 是 False
  assert x is None       # 是 None
  assert x in y          # x 在 y 中
  assert len(x) == 3     # 长度
  assert isinstance(x, dict)  # 类型检查

6.2 pytest 特有断言（更清晰）
  pytest.raises(Exception): 断言某段代码会抛出异常

  def test_delete_nonexistent(user_db):
      with pytest.raises(ValueError):  # 期望抛出 ValueError
          user_db.delete_student(999)

6.3 失败信息提示
  # 加第二个参数提供自定义失败信息
  assert x == 3, f"期望 3，实际是 {x}"

  # 或者
  assert user["role"] == "admin", f"角色错误: {user}"


C++ 对比总结：
┌─────────────────┬──────────────────────┬──────────────────────────┐
│ 概念              │ C++ (Google Test)    │ Python (pytest)           │
├─────────────────┼──────────────────────┼──────────────────────────┤
│ 断言              │ ASSERT_EQ(a, b)     │ assert a == b            │
│ 测试函数           │ TEST(Suite, Name)   │ def test_name():         │
│ 参数化             │ INSTANTIATE_TEST_   │ @pytest.mark.parametrize │
│ 夹具/准备数据      │ SetUp()/TearDown()  │ @pytest.fixture          │
│ 运行方式           │ 编译后运行可执行文件  │ pytest 命令直接运行       │
└─────────────────┴──────────────────────┴──────────────────────────┘
"""

print("\n[OK] Day 11 笔记阅读完毕，开始做练习吧！")
print("练习文件: day11_exercise.py")
print()
print("今天的新概念：")
print("  1. assert 断言 — 验证代码行为的核心工具")
print("  2. fixture — 自动准备和清理测试环境的机制")
print("  3. @parametrize — 一组数据跑多次测试，减少重复代码")
print("  4. AAA 模式 — Arrange/Act/Assert，组织测试的标准套路")
