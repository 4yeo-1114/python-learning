"""
============================================================
Day 2 参考答案：核心数据结构 + 函数
============================================================
做完练习后再看哦！
"""

# ============================================================
# 练习 1：列表基础操作
# ============================================================

shopping_list = []
shopping_list.append("牛奶")
shopping_list.append("面包")
shopping_list.append("鸡蛋")
print(f"添加后: {shopping_list}")

shopping_list.insert(2, "黄油")  # 在索引2（"面包"之后）插入
print(f"插入黄油后: {shopping_list}")

shopping_list.remove("鸡蛋")
print(f"删除鸡蛋后: {shopping_list}")


# ============================================================
# 练习 2：切片操作
# ============================================================

nums = [10, 20, 30, 40, 50, 60, 70, 80]

print(f"前3个:  {nums[:3]}")
print(f"后3个:  {nums[-3:]}")
print(f"索引2-5: {nums[2:5]}")
print(f"反转:   {nums[::-1]}")


# ============================================================
# 练习 3：字典操作 — 学生成绩簿
# ============================================================

scores = {
    "张三": 85,
    "李四": 92,
    "王五": 78
}

# a) 添加
scores["赵六"] = 88

# b) 修改
scores["王五"] = 80

print(f"成绩簿: {scores}")

# c) 平均分
average = sum(scores.values()) / len(scores)
print(f"平均分: {average:.1f}")

# d) 最高分
top_student = max(scores, key=scores.get)  # 按值找键
print(f"最高分: {top_student} ({scores[top_student]})")


# ============================================================
# 练习 4：集合 — 共同兴趣爱好
# ============================================================

ming = {"篮球", "编程", "音乐", "游戏"}
hong = {"画画", "音乐", "旅行", "编程"}

print(f"共同爱好: {ming & hong}")
print(f"所有爱好: {ming | hong}")
print(f"只有小明喜欢: {ming - hong}")


# ============================================================
# 练习 5：列表推导式
# ============================================================

# a)
even_cubes = [i ** 3 for i in range(1, 21) if i % 2 == 0]
print(f"偶数立方: {even_cubes}")

# b)
words = ["hello", "world", "python", "code"]
long_upper = [w.upper() for w in words if len(w) >= 5]
print(f"长单词大写: {long_upper}")


# ============================================================
# 练习 6：函数编写 — 学生管理系统工具函数
# ============================================================

def calculate_grade(score):
    """根据分数返回等级"""
    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    elif score >= 70:
        return 'C'
    elif score >= 60:
        return 'D'
    else:
        return 'F'

def validate_name(name):
    """验证姓名：不为空且长度至少2个字符"""
    return bool(name) and len(name.strip()) >= 2

def format_student(name, age, major="未定", **extras):
    """格式化学生信息"""
    result = f"姓名:{name} | 年龄:{age} | 专业:{major}"
    for key, value in extras.items():
        result += f" | {key}:{value}"
    return result

# --- 测试你的函数 ---
print("=== 函数测试 ===")
print(f"calculate_grade(85)  = {calculate_grade(85)}")
print(f"calculate_grade(92)  = {calculate_grade(92)}")
print(f"calculate_grade(58)  = {calculate_grade(58)}")

print(f"validate_name('张三') = {validate_name('张三')}")
print(f"validate_name('')     = {validate_name('')}")
print(f"validate_name('A')    = {validate_name('A')}")

print(format_student("张三", 20, "计算机科学", phone="13800138000", email="zhangsan@example.com"))


# ============================================================
# 练习 7（综合挑战）：简易通讯录
# ============================================================

def add_contact(contacts, name, phone, email=""):
    """添加联系人"""
    contact = {"name": name, "phone": phone, "email": email}
    contacts.append(contact)
    print(f"[OK] 已添加联系人: {name}")

def find_contact(contacts, name):
    """按姓名查找联系人"""
    for contact in contacts:
        if contact["name"] == name:
            return contact
    return None

def delete_contact(contacts, name):
    """按姓名删除联系人"""
    for i, contact in enumerate(contacts):
        if contact["name"] == name:
            contacts.pop(i)
            return True
    return False

def list_contacts(contacts):
    """打印所有联系人"""
    if not contacts:
        print("通讯录为空")
        return
    print("\n=== 通讯录 ===")
    for i, contact in enumerate(contacts, 1):
        print(f"{i}. {contact['name']} | {contact['phone']} | {contact['email']}")
    print(f"共 {len(contacts)} 人\n")


# --- 测试通讯录 ---
print("\n=== 通讯录测试 ===")
my_contacts = []

add_contact(my_contacts, "张三", "13800138000", "zhangsan@mail.com")
add_contact(my_contacts, "李四", "13900139000", "lisi@mail.com")
add_contact(my_contacts, "王五", "13700137000")

list_contacts(my_contacts)

# 查找
result = find_contact(my_contacts, "李四")
print(f"查找 '李四': {result}")

result = find_contact(my_contacts, "赵六")
print(f"查找 '赵六': {result}")

# 删除
deleted = delete_contact(my_contacts, "王五")
print(f"删除 '王五': {'成功' if deleted else '失败'}")

list_contacts(my_contacts)

print("\n[Congrats!] Day 2 练习完成！")
