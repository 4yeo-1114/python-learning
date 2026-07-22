"""
============================================================
Day 6 练习：面向对象编程
============================================================
说明：完成以下 4 道练习，每道题有对应的 TODO 标记。
      完成后对照 day06_solution.py 查看参考答案。
      每题下方已预留空行，方便你写代码。
============================================================
"""

# ============================================================
# 练习 1：Rectangle 类（基础：__init__ + 实例方法）
# ============================================================
"""
定义一个 Rectangle 类，包含：
  - __init__(self, width, height)：初始化宽和高
  - area(self)：返回面积
  - perimeter(self)：返回周长
  - describe(self)：返回字符串 "Rectangle(宽x高) — 面积=xx, 周长=xx"

示例输出：
  rect = Rectangle(5, 3)
  rect.area()       → 15
  rect.perimeter()  → 16
  rect.describe()   → "Rectangle(5x3) — 面积=15, 周长=16"
"""

# TODO: 在这里定义 Rectangle 类
class Rectangle:
    def __init__(self,width,height):
      self.width = width
      self.height = height
      
    def area(self):
      return self.width* self.height
    
    def perimeter(self):
      return 2*(self.width + self.height)
    
    def describe(self):
      return f"Rectangle({self.width}X{self.height}) 面积={self.area()}, 周长={self.perimeter()}"
    





rect = Rectangle(5, 3)
print(f"面积: {rect.area()}")
print(f"周长: {rect.perimeter()}")
print(rect.describe())


# ============================================================
# 练习 2：BankAccount 类（@property + 封装）
# ============================================================
"""
定义一个 BankAccount 类，包含：
  - __init__(self, owner, balance=0)：初始化户主和余额，余额不能为负数
  - deposit(amount)：存款，amount 必须 > 0，否则抛出 ValueError
  - withdraw(amount)：取款，amount 必须 > 0 且不能超过余额，否则抛出 ValueError
  - balance 属性（用 @property）：只读属性，返回当前余额
  - info 属性（用 @property）：只读属性，返回 "户主: xxx, 余额: ￥xxx"

要求：
  1. 余额用 _balance（受保护属性）存储
  2. 通过 @property 暴露 balance（只读）
  3. __init__ 里用 self.balance = balance（走 setter 验证），还是 self._balance = balance？
     思考：如果 __init__ 走 self.balance = balance，但你没有定义 setter（只读），
     会怎样？写出你的理解和处理方式。

示例输出：
  acc = BankAccount("张三", 1000)
  acc.deposit(500)
  acc.withdraw(200)
  print(acc.balance)    → 1300
  print(acc.info)       → "户主: 张三, 余额: ￥1300"
  acc.balance = 2000    → AttributeError（只读）
"""

# TODO: 在这里定义 BankAccount 类

class BankAccount:
    def __init__(self,owner,balance = 0):
      self.owner = owner
       # 因为这里 balance 是只读属性（只有 @property，没有 @balance.setter）
      if balance < 0:
        raise ValueError(f"初始余额不能为负数:{balance}")
      self._balance = balance
    def deposit(self,amount):
      if amount < 0:
        raise ValueError(f"存款金额必须>0,收到:{amount}")
      self._balance += amount
      print(f"存入{amount},当前余额{self._balance}")

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
      return self._balance
    
    @property
    def info(self):
      return f"户主:{self.owner},余额:{self._balance}"



acc = BankAccount("张三", 1000)
acc.deposit(500)
acc.withdraw(200)
print(f"余额: {acc.balance}")
print(acc.info)

try:
    acc = BankAccount("李四", -500)
except ValueError as e:
    print(f"创建失败（预期）: {e}")

try:
    acc.withdraw(99999)
except ValueError as e:
    print(f"取款失败（预期）: {e}")


# ============================================================
# 练习 3：继承体系 — Person → Student / Teacher
# ============================================================
"""
设计一个继承体系：

1. Person（基类）：
   - __init__(self, name, age)：初始化姓名和年龄
   - __str__(self)：返回 "姓名(name), 年龄(age)岁"
   - describe(self)：返回 "这是一个人"

2. Student（继承自 Person）：
   - __init__(self, name, age, student_id, major)：
       调用父类 __init__，再初始化学号和专业
   - __str__(self)：返回 "[学号] 姓名, 年龄岁 — 专业专业"
   - describe(self)：返回 "学生 [学号]，正在学习专业"
   - study(self)：返回 "姓名 正在学习..."

3. Teacher（继承自 Person）：
   - __init__(self, name, age, teacher_id, title)：
       调用父类 __init__，再初始化工号和职称
   - __str__(self)：返回 "[工号] 姓名, 年龄岁 — 职称"
   - describe(self)：返回 "教师 [工号]，职称"
   - teach(self)：返回 "姓名 老师正在上课..."

示例输出：
  stu = Student("张三", 20, "S001", "计算机")
  print(stu)            → "[S001] 张三, 20岁 — 计算机专业"
  print(stu.describe()) → "学生 [S001]，正在学习计算机"
  print(stu.study())    → "张三 正在学习..."

  tea = Teacher("李教授", 45, "T001", "教授")
  print(tea)            → "[T001] 李教授, 45岁 — 教授"
  print(tea.teach())    → "李教授 老师正在上课..."
"""

# TODO: 在这里定义 Person、Student、Teacher 三个类

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
# 练习 4（综合）：Task 类 — 魔法方法 + 属性
# ============================================================
"""
定义一个 Task 类，模拟一个待办任务：

属性：
  - title：任务标题
  - priority：优先级（1~5，1 最高）
  - done：是否完成（默认 False）

魔法方法（全部实现）：
  - __str__：返回友好格式，如 "[完成] 完成" 或 "[未完成] 进行中"
    示例："[优先级3] 背单词 [未完成]"
  - __repr__：返回能重建对象的字符串
    示例："Task('背单词', priority=3, done=False)"
  - __eq__：两个 Task 的 title 相同则认为相等（忽略优先级和完成状态）
  - __lt__：优先级数字小的 < 优先级数字大的（即高优先级排前面）
  - __len__：返回标题的字数（提示：len(self.title)）

方法：
  - mark_done()：将 done 标记为 True
  - mark_undo()：将 done 标记为 False

要求：
  - priority 用 @property 实现，保证赋值时在 1~5 范围内，否则抛出 ValueError
  - __eq__ 中用 isinstance 做类型检查

示例输出：
  t1 = Task("背单词", priority=3)
  t2 = Task("刷算法题", priority=1)
  t3 = Task("背单词", priority=5)  # 和 t1 标题相同

  print(t1)           → "[优先级3] 背单词 [未完成]"
  t1.mark_done()
  print(t1)           → "[优先级3] 背单词 [完成]"
  print(repr(t1))     → "Task('背单词', priority=3, done=True)"
  print(len(t1))      → 3

  print(t1 == t3)     → True（标题相同）
  print(t1 == t2)     → False

  # 排序：优先级高的排前面
  tasks = [t1, t2, Task("写报告", priority=2)]
  tasks.sort()
  for t in tasks:
      print(t)
  # 输出顺序应为：刷算法题(1) → 写报告(2) → 背单词(3)
"""

# TODO: 在这里定义 Task 类
class Task:
    def __init__(self,title,priority = 3,done =False):
      self.title = title
      self.priority = priority
      self.done = done
    
    @property
    def priority(self):
      return self._priority
    
    @priority.setter
    def priority(self, value):
      if not 1<= value <= 5:
          raise ValueError(f"优先级必须在1~5之间,收到:{value}")
      self._priority  =value
      
    def mark_done(self):
        self.done = True

    def mark_undo(self):
        self.done = False
        
    def __str__(self):
      status = "[完成]" if self.done else "[未完成]"
      return f"[优先级{self.priority}]{self.title}{status}"
    
    def __repr__(self):
        return f"Task('{self.title}', priority={self.priority}, done={self.done})"
    
    def __eq__(self,other):
      if not isinstance(other,Task):
        return False
      return self.title == other.title
    
    def __lt__(self,other):
      if not isinstance(other,Task):
        return False
      return self.priority < other.priority
    
    def __len__(self):
      return len(self.title)





# 测试代码（写完类后取消注释运行）
# t1 = Task("背单词", priority=3)
# t2 = Task("刷算法题", priority=1)
# t3 = Task("背单词", priority=5)
#
# print("--- __str__ ---")
# print(t1)
# t1.mark_done()
# print(t1)
#
# print("\n--- __repr__ ---")
# print(repr(t1))
#
# print("\n--- __len__ ---")
# print(f"len(t1) = {len(t1)}")   # 3
# print(f"len(t2) = {len(t2)}")   # 4
#
# print("\n--- __eq__ ---")
# print(f"t1 == t3: {t1 == t3}")   # True
# print(f"t1 == t2: {t1 == t2}")   # False
#
# print("\n--- __lt__（按优先级排序） ---")
# tasks = [t1, t2, Task("写报告", priority=2)]
# tasks.sort()
# for t in tasks:
#     print(t)
#
# print("\n--- priority 验证 ---")
# try:
#     bad = Task("test", priority=10)
# except ValueError as e:
#     print(f"创建失败（预期）: {e}")

print("\n[OK] 练习写完啦！对照 day06_solution.py 看答案吧。")
