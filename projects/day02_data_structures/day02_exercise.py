"""
============================================================
Day 2 练习题：核心数据结构 + 函数
============================================================
请完成以下练习，巩固今天学的内容。
答案在 day02_solution.py，做完再看！
"""

# ============================================================
# 练习 1：列表基础操作
# 创建一个空列表 shopping_list，依次添加 "牛奶"、"面包"、"鸡蛋"
# 然后在 "面包" 后面插入 "黄油"，最后删除 "鸡蛋"
# 打印每一步的结果
# ============================================================

# TODO: 在这里写你的代码
shopping_list  = {}
shopping_list.append("牛奶")
shopping_list.append("面包")
shopping_list.append("鸡蛋")
print(f"{shopping_list}")

shopping_list.insert(1,"黄油")
print(f"{shopping_list}")

shopping_list.remove("鸡蛋")
print(f"{shopping_list}")




# ============================================================
# 练习 2：切片操作
# 有一个列表 nums = [10, 20, 30, 40, 50, 60, 70, 80]
# 请用切片分别获取：
#   a) 前 3 个元素
#   b) 后 3 个元素
#   c) 索引 2 到 5（不含）的元素
#   d) 反转后的列表
# ============================================================

# TODO: 在这里写你的代码
nums = [10, 20, 30, 40, 50, 60, 70, 80]
print(f"{nums[:3]}")
print(f"{nums[-3:]}")
print(f"{nums[2:5:]}")
print(f"{nums[::-1]}")



# ============================================================
# 练习 3：字典操作 — 学生成绩簿
# 创建一个字典 scores，包含三个学生的成绩：
#   "张三": 85, "李四": 92, "王五": 78
# 然后：
#   a) 添加 "赵六": 88
#   b) 把 "王五" 的成绩改为 80
#   c) 计算所有学生的平均分
#   d) 找出最高分的学生姓名和分数
# ============================================================

# TODO: 在这里写你的代码
scores = {
    "张三": 85,
    "李四": 92, 
    "王五": 78
    
}
#scores.append("赵六",80)
scores["赵六"] = 80
scores["王五"]  = 80

average   = sum(scores.values())/ len(scores)
#保留一位小数
print(f"平均分:{average:.1f}")


top_student = max(scores,key=scores.get)

print(f"最高分:{top_student}({scores[top_student]})")




# ============================================================
# 练习 4：集合 — 共同兴趣爱好
# 小明喜欢：{"篮球", "编程", "音乐", "游戏"}
# 小红喜欢：{"画画", "音乐", "旅行", "编程"}
# 请找出：
#   a) 两人共同的爱好（交集）
#   b) 两人所有的爱好（并集）
#   c) 只有小明喜欢的爱好（差集）
# ============================================================

# TODO: 在这里写你的代码
a  = {"篮球", "编程", "音乐", "游戏"}
b = {"画画", "音乐", "旅行", "编程"}
print(f"{a|b}")
print(f"{a&b}") #并集&
print(f"{a-b}")



# ============================================================
# 练习 5：列表推导式
# 用列表推导式完成以下任务：
#   a) 生成 1~20 中所有偶数的立方 [8, 64, 216, ...]
#   b) 把列表 words = ["hello", "world", "python", "code"] 中
#      所有长度 >= 5 的单词转为大写
# ============================================================

# TODO: 在这里写你的代码

num = [i**3 for i in range(1,21) if i%2==0]
words = ["hello", "world", "python", "code"]

upper  = [upper(c) for c in words if len(c)>=5]
print(f"长单词大写{upper}")


# ============================================================
# 练习 6：函数编写 — 学生管理系统工具函数
# 编写以下函数（这些将来会用在你的学生管理系统中！）：
#
#   a) calculate_grade(score) — 输入分数返回等级
#      >=90: A, >=80: B, >=70: C, >=60: D, <60: F
#
#   b) validate_name(name) — 验证姓名不为空且长度≥2
#      返回 True/False
#
#   c) format_student(name, age, major="未定", **extras) —
#      返回格式化字符串，如：
#      "姓名:张三 | 年龄:20 | 专业:计算机科学 | 电话:138..."
#      extras 里可能包含 phone, email 等额外字段
# ============================================================

# TODO: 在这里写你的代码

def format_student(name,age,major = "未定",**extras):
        result  = f"姓名：{name}|年龄：{age}|专业:{major}"
        for key,value in extras.items():
            result += f"|{key}:{value}"
        return result







# ============================================================
# 练习 7（综合挑战）：简易通讯录
# 用列表 + 字典做一个通讯录管理程序：
#
# contacts = []  每个元素是一个字典 {"name": ..., "phone": ..., "email": ...}
#
# 实现以下功能（用函数包装）：
#   a) add_contact(contacts, name, phone, email) — 添加联系人
#   b) find_contact(contacts, name) — 按姓名查找，返回字典或 None
#   c) delete_contact(contacts, name) — 按姓名删除，返回 True/False
#   d) list_contacts(contacts) — 打印所有联系人
#   e) 在你的代码最后写一段测试，演示所有功能
# ============================================================

# TODO: 在这里写你的代码
contacts = []

def add_contact(contacts,name,phone,email = ""):
    contact  = {"name":name,"phone":phone,"email":email}
    contacts.append(contact)
    print(f"已添加练习人:{name}")

def find_contact(contacts,name):
    for contact in contacts:
        if contact["name"] == name:
            return contact
    return None

def delete_contacts(contacts,name):
    for i, contact in enumerate(contacts):
        if contact["name"] == name:
            contact.pop(i)
            return True
    return False

def list_contacts(contacts):
    if not contacts:
        print("通讯录为空")
        return
    print("\n====通讯录====")
    for i ,contact in enumerate(contacts,1):
        print(f"{i}.{contact['name']}|{contact['phone']}|{contact['email']}")
    print(f"共{len(contacts)}人\n")






print("\n[Congrats!] Day 2 练习完成！答案见 day02_solution.py")
