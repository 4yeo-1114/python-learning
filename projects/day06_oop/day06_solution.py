"""
============================================================
Day 6 练习参考答案
============================================================
提示：先独立完成 day06_exercise.py，再看这里！
============================================================
"""

# ============================================================
# 练习 1：Rectangle 类
# ============================================================

class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

    def describe(self):
        return f"Rectangle({self.width}x{self.height}) — 面积={self.area()}, 周长={self.perimeter()}"


# 测试
print("=== 练习 1：Rectangle ===")
rect = Rectangle(5, 3)
print(f"面积: {rect.area()}")
print(f"周长: {rect.perimeter()}")
print(rect.describe())


# ============================================================
# 练习 2：BankAccount 类
# ============================================================

class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        # 关键：__init__ 里直接给 _balance 赋值，不走 balance setter
        # 因为这里 balance 是只读属性（只有 @property，没有 @balance.setter）
        if balance < 0:
            raise ValueError(f"初始余额不能为负数：{balance}")
        self._balance = balance

    def deposit(self, amount):
        """存款"""
        if amount <= 0:
            raise ValueError(f"存款金额必须 > 0，收到：{amount}")
        self._balance += amount
        print(f"  存入 ￥{amount}，当前余额 ￥{self._balance}")

    def withdraw(self, amount):
        """取款"""
        if amount <= 0:
            raise ValueError(f"取款金额必须 > 0，收到：{amount}")
        if amount > self._balance:
            raise ValueError(f"余额不足！余额 ￥{self._balance}，尝试取款 ￥{amount}")
        self._balance -= amount
        print(f"  取出 ￥{amount}，当前余额 ￥{self._balance}")

    @property
    def balance(self):
        """余额 — 只读属性"""
        return self._balance

    @property
    def info(self):
        """账户信息 — 只读属性"""
        return f"户主: {self.owner}, 余额: ￥{self._balance}"


# 测试
print("\n=== 练习 2：BankAccount ===")
acc = BankAccount("张三", 1000)
acc.deposit(500)
acc.withdraw(200)
print(f"余额: {acc.balance}")
print(acc.info)

try:
    acc_bad = BankAccount("李四", -500)
except ValueError as e:
    print(f"创建失败（预期）: {e}")

try:
    acc.withdraw(99999)
except ValueError as e:
    print(f"取款失败（预期）: {e}")

# 试图修改只读属性
try:
    acc.balance = 2000
except AttributeError as e:
    print(f"修改只读属性失败（预期）: {e}")


# ============================================================
# 练习 3：继承体系 — Person → Student / Teacher
# ============================================================

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"姓名({self.name}), 年龄({self.age}岁)"

    def describe(self):
        return f"这是一个人"


class Student(Person):
    def __init__(self, name, age, student_id, major):
        super().__init__(name, age)      # 调用父类 __init__
        self.student_id = student_id
        self.major = major

    def __str__(self):
        return f"[{self.student_id}] {self.name}, {self.age}岁 — {self.major}专业"

    def describe(self):
        return f"学生 [{self.student_id}]，正在学习{self.major}"

    def study(self):
        return f"{self.name} 正在学习..."


class Teacher(Person):
    def __init__(self, name, age, teacher_id, title):
        super().__init__(name, age)
        self.teacher_id = teacher_id
        self.title = title

    def __str__(self):
        return f"[{self.teacher_id}] {self.name}, {self.age}岁 — {self.title}"

    def describe(self):
        return f"教师 [{self.teacher_id}]，{self.title}"

    def teach(self):
        return f"{self.name} 老师正在上课..."


# 测试
print("\n=== 练习 3：继承体系 ===")
stu = Student("张三", 20, "S001", "计算机")
tea = Teacher("李教授", 45, "T001", "教授")

print(stu)
print(stu.describe())
print(stu.study())
print()
print(tea)
print(tea.describe())
print(tea.teach())

# isinstance 验证
print(f"\nstu 是 Student? {isinstance(stu, Student)}")
print(f"stu 是 Person?  {isinstance(stu, Person)}")
print(f"tea 是 Student? {isinstance(tea, Student)}")


# ============================================================
# 练习 4（综合）：Task 类
# ============================================================

class Task:
    def __init__(self, title, priority=3, done=False):
        self.title = title
        self.priority = priority     # 走 property setter 验证
        self.done = done

    # --- property：优先级验证 ---
    @property
    def priority(self):
        return self._priority

    @priority.setter
    def priority(self, value):
        if not 1 <= value <= 5:
            raise ValueError(f"优先级必须在 1~5 之间，收到：{value}")
        self._priority = value

    # --- 方法 ---
    def mark_done(self):
        self.done = True

    def mark_undo(self):
        self.done = False

    # --- 魔法方法 ---
    def __str__(self):
        status = "[完成]" if self.done else "[未完成]"
        return f"[优先级{self.priority}] {self.title} {status}"

    def __repr__(self):
        return f"Task('{self.title}', priority={self.priority}, done={self.done})"

    def __eq__(self, other):
        if not isinstance(other, Task):
            return False
        return self.title == other.title

    def __lt__(self, other):
        # 优先级数字越小越靠前
        if not isinstance(other, Task):
            return NotImplemented
        return self.priority < other.priority

    def __len__(self):
        return len(self.title)


# 测试
print("\n=== 练习 4：Task 类 ===")

t1 = Task("背单词", priority=3)
t2 = Task("刷算法题", priority=1)
t3 = Task("背单词", priority=5)

print("--- __str__ ---")
print(t1)
t1.mark_done()
print(t1)

print("\n--- __repr__ ---")
print(repr(t1))

print("\n--- __len__ ---")
print(f"len(t1) = {len(t1)}")
print(f"len(t2) = {len(t2)}")

print("\n--- __eq__ ---")
print(f"t1 == t3: {t1 == t3}")   # True
print(f"t1 == t2: {t1 == t2}")   # False

print("\n--- __lt__（按优先级排序） ---")
tasks = [t1, t2, Task("写报告", priority=2)]
tasks.sort()
for t in tasks:
    print(t)

print("\n--- priority 验证 ---")
try:
    bad = Task("test", priority=10)
except ValueError as e:
    print(f"创建失败（预期）: {e}")

print("\n[OK] 答案完毕！对比自己的代码看看哪里可以改进。")
