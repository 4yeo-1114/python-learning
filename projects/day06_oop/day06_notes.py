"""
============================================================
Day 6: 面向对象编程 — 类、对象、继承、魔法方法（C++ 对比版）
============================================================
目标：用 C++ 的 OOP 知识快速理解 Python 的面向对象体系
"""

# ============================================================
# 1. 定义类和创建对象 — class 和 __init__
# ============================================================

print("=== 1. 定义类和 __init__ ===")

# Python 类的定义 — 和 C++ 的核心差异：
# 1. 没有头文件 / 声明分离，所有代码写在一起
# 2. self 必须显式写在第一个参数位置
# 3. 构造函数叫 __init__，不是类名
# 4. 没有 private/public/protected 关键字

class Student:
    """学生类 — Python 的类定义"""

    # __init__ 是构造函数（初始化方法）
    # self 等价于 C++ 的 this，但必须显式写出来！
    def __init__(self, name, age, student_id):
        self.name = name            # 实例属性：直接 self.xxx 就创建了
        self.age = age
        self.student_id = student_id

    # 实例方法 — self 永远是第一个参数
    def introduce(self):
        return f"我叫{self.name}，学号{self.student_id}，今年{self.age}岁"


# 创建对象：不需要 new 关键字！
s1 = Student("张三", 20, "S2024001")
s2 = Student("李四", 19, "S2024002")

print(s1.introduce())
print(s2.introduce())

# C++ 对比：
# class Student {
# public:
#     string name;
#     int age;
#     string student_id;
#     Student(string n, int a, string id)
#         : name(n), age(a), student_id(id) {}
#     string introduce() {
#         return "我叫" + name + "，学号" + student_id;
#     }
# };
# Student s1("张三", 20, "S2024001");  // 栈上创建
# auto s2 = new Student("李四", 19, "S2024002");  // 堆上创建（需要 delete）

# [!] 关键差异 1：属性不需要预先声明！
# C++ 必须在类定义里声明所有成员变量，Python 可以在 __init__ 里
# 动态添加（甚至可以事后给对象添加属性，但别这么做，乱）

# [!] 关键差异 2：self 必须显式写
# 在类内部访问属性/方法，全部通过 self.xxx
# C++ 的 this 是可选的，Python 的 self 是必须的


# ============================================================
# 2. 类属性 vs 实例属性
# ============================================================

print("\n=== 2. 类属性 vs 实例属性 ===")

class StudentV2:
    """演示类属性和实例属性的区别"""

    school = "清华大学"           # 类属性：所有实例共享（类似 C++ static）
    count = 0                    # 类属性：统计创建了多少个学生

    def __init__(self, name, age):
        self.name = name         # 实例属性：每个对象各有一份
        self.age = age
        StudentV2.count += 1     # 通过类名访问类属性

    def show(self):
        # self.school 也能访问类属性（通过实例 → 类向上查找）
        return f"{self.name}，{self.age}岁，就读于{self.school}"


s1 = StudentV2("张三", 20)
s2 = StudentV2("李四", 19)

print(f"创建了 {StudentV2.count} 个学生")  # 2
print(s1.show())
print(s2.show())

# [!] 注意：通过实例修改"类属性"是陷阱！
s1.school = "北京大学"           # 这实际上给 s1 创建了一个同名的实例属性！
print(f"s1.school = {s1.school}")  # 北京大学（s1 自己的实例属性）
print(f"s2.school = {s2.school}")  # 清华大学（还是类属性）
print(f"StudentV2.school = {StudentV2.school}")  # 清华大学（类属性没变）

# 正确修改类属性的方式：
StudentV2.school = "浙江大学"
print(f"\n修改类属性后:")
print(f"s2.school = {s2.school}")  # 浙江大学（通过实例也能看到变化）
print(f"s1.school = {s1.school}")  # 北京大学（实例属性遮蔽了类属性！）

# C++ 对比：
# class StudentV2 {
#     static string school;       // ← 类属性 = C++ 的 static 成员
#     static int count;
#     string name;                // ← 实例属性 = C++ 的普通成员
#     int age;
# };


# ============================================================
# 3. 三种方法：实例方法 / 类方法 / 静态方法
# ============================================================

print("\n=== 3. 三种方法 ===")

class Demo:
    value = 100

    def instance_method(self):
        """普通方法（实例方法）：第一个参数是 self，能访问实例和类"""
        return f"实例方法: self={self}, value={self.value}"

    @classmethod
    def class_method(cls):
        """类方法：第一个参数是 cls（类本身），只能访问类级别的东西"""
        return f"类方法: cls={cls}, value={cls.value}"

    @staticmethod
    def static_method(x, y):
        """静态方法：没有 self/cls，就是普通函数，只是放在类里"""
        return f"静态方法: {x} + {y} = {x + y}"


d = Demo()
print(d.instance_method())         # 通过实例调用
print(Demo.class_method())         # 通过类名调用（推荐）
print(Demo.static_method(3, 5))    # 通过类名调用（推荐）

# 什么时候用哪种？
# - 实例方法：需要 self，处理实例数据 → 90% 的情况
# - 类方法：需要创建"工厂方法"（如从 JSON 构建对象）→ 偶尔用
# - 静态方法：工具函数，和类逻辑相关但不需要类数据 → 很少用

# C++ 对比：
# - 实例方法 = C++ 普通成员函数
# - 类方法 ≈ C++ static 成员函数（但 Python 的 cls 能访问类对象）
# - 静态方法 = C++ static 成员函数


# ============================================================
# 4. 魔法方法（Magic Methods / Dunder Methods）
# ============================================================

print('\n=== 4. 魔法方法 — 让对象"像内置类型一样"工作 ===')

# 魔法方法 = 双下划线开头和结尾的方法（__xxx__）
# 它们让自定义类支持 len()、str()、==、+、in 等操作

class Book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages

    # __str__: 给人看的，print() / str() 调用
    def __str__(self):
        return f"《{self.title}》— {self.author}"

    # __repr__: 给开发者看的，交互环境 / repr() 调用
    # 原则：如果可能，应返回能"重建"该对象的字符串
    def __repr__(self):
        return f"Book(title='{self.title}', author='{self.author}', pages={self.pages})"

    # __len__: len() 调用
    def __len__(self):
        return self.pages

    # __eq__: == 比较（默认比较内存地址！）
    def __eq__(self, other):
        if not isinstance(other, Book):
            return False                                # 不是同类 → 不相等
        return self.title == other.title and self.author == other.author

    # __lt__: < 比较（用于排序）
    def __lt__(self, other):
        return self.pages < other.pages

    # __contains__: in 操作符
    def __contains__(self, keyword):
        return keyword in self.title


book1 = Book("三体", "刘慈欣", 500)
book2 = Book("三体", "刘慈欣", 500)   # 内容一样，不同对象
book3 = Book("活着", "余华", 200)

# __str__ vs __repr__
print(f"str:  {str(book1)}")        # 《三体》— 刘慈欣
print(f"repr: {repr(book1)}")       # Book(title='三体', ...)

# __eq__
print(f"\nbook1 == book2: {book1 == book2}")  # True（内容相同）
print(f"book1 == book3: {book1 == book3}")    # False
# 如果没有 __eq__，book1 == book2 会是 False（不同对象，地址不同）

# __len__
print(f"\nlen(book1) = {len(book1)} 页")    # 500

# __lt__
print(f"book1 < book3: {book1 < book3}")     # False（500 < 200 不成立）

# __contains__
print(f"'三' in book1: {'三' in book1}")     # True
print(f"'四' in book1: {'四' in book1}")     # False

# C++ 对比：Python 的魔法方法 ≈ C++ 的运算符重载
# C++:  bool operator==(const Book& other) const { ... }
#       ostream& operator<<(ostream& os, const Book& b) { ... }
# Python 的魔法方法更统一、更丰富

# 常用魔法方法速查：
"""
┌─────────────────┬─────────────────────────┬──────────────────────────┐
│ 魔法方法          │ 触发方式                  │ 用途                     │
├─────────────────┼─────────────────────────┼──────────────────────────┤
│ __init__        │ obj = Class(...)        │ 构造函数                   │
│ __str__         │ str(obj), print(obj)    │ 用户友好的字符串表示        │
│ __repr__        │ repr(obj), 交互环境      │ 开发者友好的字符串表示      │
│ __len__         │ len(obj)                │ 长度/大小                  │
│ __eq__          │ obj1 == obj2            │ 相等比较                   │
│ __lt__ / __gt__ │ < / >                   │ 大小比较（排序用）           │
│ __contains__    │ x in obj                │ 成员检查                   │
│ __getitem__     │ obj[key]                │ 索引/键访问（像 list/dict） │
│ __setitem__     │ obj[key] = value        │ 索引/键赋值                │
│ __iter__        │ for x in obj            │ 迭代                      │
│ __call__        │ obj()                   │ 让对象可调用（像函数）       │
│ __add__         │ obj1 + obj2             │ 加法运算符                  │
│ __enter/exit__  │ with obj as x:          │ 上下文管理器（Day 3 学过的） │
└─────────────────┴─────────────────────────┴──────────────────────────┘
"""


# ============================================================
# 5. 继承 — 单继承和多继承
# ============================================================

print("\n=== 5. 继承 ===")

# 5.1 单继承
print("--- 单继承 ---")

class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return f"{self.name} 发出了声音"

    def eat(self):
        return f"{self.name} 在吃东西"


class Dog(Animal):              # ← Python 用括号表示继承，不用 : public Animal
    def __init__(self, name, breed):
        super().__init__(name)  # ← super() 调用父类 __init__
        self.breed = breed

    def speak(self):            # 重写（override）父类方法
        return f"{self.name} 汪汪叫！"

    def fetch(self):            # 子类新增方法
        return f"{self.name} 去捡球了"


class Cat(Animal):
    def speak(self):
        return f"{self.name} 喵喵叫~"


dog = Dog("旺财", "金毛")
cat = Cat("咪咪")

print(dog.speak())              # 汪汪叫！（自己的 speak）
print(cat.speak())              # 喵喵叫~（自己的 speak）
print(dog.eat())                # 在吃东西（继承自 Animal）
print(dog.fetch())              # 去捡球了（Dog 独有）

# isinstance() 检查继承关系
print(f"\ndog 是 Dog?    {isinstance(dog, Dog)}")      # True
print(f"dog 是 Animal? {isinstance(dog, Animal)}")   # True
print(f"cat 是 Dog?    {isinstance(cat, Dog)}")      # False

# C++ 对比：
# class Dog : public Animal { ... };  ← C++ 有 public/private/protected 继承
# Python 没有这些，所有继承都是"public"的


# 5.2 super() — 调用父类方法
print("\n--- super() 详解 ---")

class A:
    def __init__(self):
        self.a = "A的属性"
        print("A.__init__ 被调用")

class B(A):
    def __init__(self):
        super().__init__()       # 调用 A.__init__
        self.b = "B的属性"
        print("B.__init__ 被调用")

class C(A):
    def __init__(self):
        super().__init__()
        self.c = "C的属性"
        print("C.__init__ 被调用")

b = B()
print(f"b.a = {b.a}, b.b = {b.b}")

# C++ 对比：
# Python 的 super() 比 C++ 的 BaseClass::method() 更强大
# 在多继承中，super() 按 MRO（方法解析顺序）自动找到下一个类


# 5.3 多继承 — Python 支持，但要谨慎使用
print("\n--- 多继承 ---")

class D(B, C):
    def __init__(self):
        super().__init__()       # 按 MRO 顺序调用，只调用一次！
        self.d = "D的属性"
        print("D.__init__ 被调用")

d_obj = D()
print(f"d_obj.a = {d_obj.a}")
print(f"d_obj.b = {d_obj.b}")
print(f"d_obj.c = {d_obj.c}")
print(f"d_obj.d = {d_obj.d}")

# MRO（Method Resolution Order）— 方法解析顺序
print(f"\nD 的 MRO: {[c.__name__ for c in D.__mro__]}")
# [D, B, C, A, object]

# C++ 对比：
# C++ 也有多继承，但有"菱形继承"问题（需要虚继承 virtual）
# Python 通过 MRO（C3 线性化算法）自动解决了菱形继承问题


# ============================================================
# 6. @property — 把方法伪装成属性
# ============================================================

print("\n=== 6. @property — 属性访问控制 ===")

class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self._balance = balance     # 单下划线：约定"受保护的"（实际仍可访问）

    # @property：把方法变成"只读属性"
    @property
    def balance(self):
        """余额 — 只读属性"""
        return self._balance

    # @xxx.setter：定义属性写入时的行为
    @balance.setter
    def balance(self, amount):
        """设置余额 — 带验证"""
        if amount < 0:
            raise ValueError(f"余额不能为负数：{amount}")
        self._balance = amount

    # @xxx.deleter：定义删除属性时的行为
    @balance.deleter
    def balance(self):
        print("[!] 不能删除余额属性")
        raise AttributeError("余额属性不可删除")

    # 只读的计算属性（没有 setter）
    @property
    def info(self):
        return f"{self.owner} 的账户，余额 ￥{self._balance}"


acc = BankAccount("张三", 1000)

# 用起来完全像属性！
print(acc.balance)              # 1000  ← 其实调用了 balance() 方法
print(acc.info)                 # 张三 的账户，余额 ￥1000

acc.balance = 2000              # ← 其实调用了 balance.setter 方法
print(f"更新后: {acc.balance}")  # 2000

try:
    acc.balance = -500          # 触发验证！
except ValueError as e:
    print(f"错误: {e}")

# C++ 对比：
# C++ 需要手动写 get_xxx() / set_xxx()，调用时必须加括号
# Python 的 @property 让外部代码看起来像直接访问属性，
# 但内部可以做验证和计算 — 这就是"统一访问原则"


# ============================================================
# 7. 访问控制 — 约定 vs 名称改写
# ============================================================

print("\n=== 7. 访问控制 ===")

class AccessDemo:
    def __init__(self):
        self.public = "公开属性"            # 公开：谁都能访问
        self._protected = "受保护属性"       # 单下划线：约定"请勿外部访问"
        self.__private = "私有属性"          # 双下划线：名称改写（name mangling）

    def show(self):
        return f"public={self.public}, _protected={self._protected}, __private={self.__private}"


obj = AccessDemo()
print(obj.show())

# 单下划线 _protected：约定而已，实际上仍可访问
print(f"\nobj._protected = {obj._protected}")     # 能访问，但不推荐

# 双下划线 __private：名称改写为 _ClassName__attribute
# print(obj.__private)                            # ❌ AttributeError！
print(f"obj._AccessDemo__private = {obj._AccessDemo__private}")  # [OK] 还是能访问！

# Python 哲学："我们都是成年人了"（We're all consenting adults）
# 没有真正的 private，靠约定和代码审查来保证

# C++ 对比：
# C++ 有真正的 private/public/protected，编译器强制检查
# Python 全靠约定，__ 双下划线只是名称改写，不是真正隐藏


# ============================================================
# 8. __slots__ — 优化内存（可选了解）
# ============================================================

print("\n=== 8. __slots__（进阶，了解即可）===")

class NormalStudent:
    def __init__(self, name, age):
        self.name = name
        self.age = age

class SlotStudent:
    __slots__ = ["name", "age"]    # 限制只能有这两个属性

    def __init__(self, name, age):
        self.name = name
        self.age = age


ns = NormalStudent("张三", 20)
ss = SlotStudent("李四", 19)

# 普通对象可以动态添加属性
ns.grade = "大三"                  # [OK] 可以
print(f"普通对象动态添加: {ns.grade}")

# __slots__ 对象不能添加
try:
    ss.grade = "大三"              # ❌ AttributeError
except AttributeError as e:
    print(f"SlotStudent 不能添加: {e}")

# __slots__ 的好处：
# 1. 节省内存（不用字典存储属性）
# 2. 防止意外添加属性
# 缺点：失去灵活性，不能动态添加属性

# C++ 对比：__slots__ 让 Python 类的内存布局更接近 C++ struct


# ============================================================
# 综合示例：学生管理系统模型
# ============================================================

print("\n=== 综合示例：学生管理系统 OOP 设计 ===")

class Person:
    """人员基类"""
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def __str__(self):
        return f"{self.name}（{self.gender}，{self.age}岁）"


class Student(Person):
    """学生类 — 继承自 Person"""
    def __init__(self, name, age, gender, student_id, major):
        super().__init__(name, age, gender)
        self.student_id = student_id
        self.major = major
        self._scores = {}        # 科目 → 成绩

    def add_score(self, subject, score):
        """添加成绩"""
        if 0 <= score <= 100:
            self._scores[subject] = score
        else:
            raise ValueError(f"成绩 {score} 不在 0~100 范围内")

    def get_average(self):
        """计算平均分"""
        if not self._scores:
            return 0.0
        return sum(self._scores.values()) / len(self._scores)

    @property
    def gpa(self):
        """GPA 计算（简化：90+ → 4.0, 80+ → 3.0, 70+ → 2.0, 60+ → 1.0）"""
        avg = self.get_average()
        if avg >= 90: return 4.0
        if avg >= 80: return 3.0
        if avg >= 70: return 2.0
        if avg >= 60: return 1.0
        return 0.0

    def __str__(self):
        base = super().__str__()
        return f"[{self.student_id}] {base} — {self.major}专业，GPA:{self.gpa:.1f}"

    def __eq__(self, other):
        if not isinstance(other, Student):
            return False
        return self.student_id == other.student_id

    def __lt__(self, other):
        return self.gpa > other.gpa  # GPA 高的排前面


# 测试
stu1 = Student("张三", 20, "男", "S001", "计算机科学")
stu1.add_score("Python", 95)
stu1.add_score("数学", 88)
stu1.add_score("英语", 76)

stu2 = Student("李四", 19, "女", "S002", "数据科学")
stu2.add_score("Python", 92)
stu2.add_score("数学", 85)
stu2.add_score("英语", 90)

print(stu1)
print(stu2)
print(f"stu1 == stu2: {stu1 == stu2}")

# 排序：GPA 高的在前
students = [stu1, stu2]
students.sort()
print(f"\n按 GPA 排名:")
for s in students:
    print(f"  {s.name}: GPA {s.gpa:.1f}")


# ============================================================
# C++ → Python 速查表（OOP）
# ============================================================
"""
┌──────────────────────┬───────────────────────────────┬──────────────────────────────┐
│ 概念                  │ C++                            │ Python                       │
├──────────────────────┼───────────────────────────────┼──────────────────────────────┤
│ 定义类                │ class Foo { ... };             │ class Foo:                   │
│ 构造函数              │ Foo(args) { ... }              │ def __init__(self, args)     │
│ 析构函数              │ ~Foo() { ... }                 │ def __del__(self)            │
│ this/self            │ this->name（可选，隐式）         │ self.name（必须显式）         │
│ 创建对象              │ new Foo() 或 栈上 Foo f()       │ Foo()（不需要 new）           │
│ 公有/私有/保护         │ public:/private:/protected:    │ 约定 _protected, __mangled   │
│ 继承                  │ class B : public A {}          │ class B(A):                  │
│ 多继承                │ 支持（需 virtual 解决菱形问题）   │ 支持（MRO 自动处理）           │
│ 调用父类方法           │ A::method()                    │ super().method()             │
│ 方法重写              │ virtual void foo() override    │ 默认就是虚函数（不需要声明）     │
│ 静态成员              │ static int x;                  │ 类属性 class X: x = 0        │
│ 静态方法              │ static void foo()              │ @staticmethod                │
│ 运算符重载            │ operator+(const T& o)          │ __add__(self, other)         │
│ 相等比较              │ operator==(const T& o)         │ __eq__(self, other)          │
│ 字符串表示            │ operator<<(ostream&, T)        │ __str__ / __repr__           │
│ getter/setter        │ getX() / setX(v)               │ @property / @xxx.setter      │
│ 类型检查              │ dynamic_cast / typeid          │ isinstance() / issubclass()  │
│ 抽象类/接口           │ 纯虚函数 = 0                    │ abc.ABC + @abstractmethod    │
│ 友元                  │ friend class Foo               │ 无（约定决定）                 │
│ const 成员函数        │ void foo() const                │ 无（约定 + 靠自觉）             │
│ 内存管理              │ new/delete, RAII               │ 自动垃圾回收（GC）              │
└──────────────────────┴───────────────────────────────┴──────────────────────────────┘
"""

# ============================================================
# 常见问题解答（Q&A）
# ============================================================
print("\n=== 常见问题解答 ===")

# Q1: __init__ 和 __new__ 有什么区别？
print("\n--- Q1: __init__ vs __new__ ---")
# __new__：创建对象（分配内存），很少需要重写
# __init__：初始化对象（设置属性），99% 的情况用这个
# 可以理解为：__new__ 是 malloc，__init__ 是构造函数体

# Q2: 什么时候用组合，什么时候用继承？
print("\n--- Q2: 组合 vs 继承 ---")
# 优先使用组合（"has-a"关系）
#   例：学生有成绩列表 → 组合
# 只在明确的"is-a"关系时用继承
#   例：大学生"是"学生 → 继承
# Python 社区更偏向组合

# Q3: 为什么 self 必须显式写？
print("\n--- Q3: 为什么 self 必须显式 ---")
# Python 之禅："显式优于隐式"
# 让你清楚知道是在用实例属性还是局部变量
# 也简化了方法绑定机制

print("\n[OK] Day 6 笔记结束！打开 day06_exercise.py 做练习吧。")
