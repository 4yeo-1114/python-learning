"""
============================================================
Day 3 参考答案：文件操作 + 字符串 + 异常处理
============================================================
做完练习后再看哦！
"""

# ============================================================
# 练习 1：字符串方法 — 姓名格式化
# ============================================================

def format_name(full_name):
    """格式化姓名：去空格，首字母大写"""
    return full_name.strip().title()

print("=== 练习1: 姓名格式化 ===")
print(format_name("  张三  "))
print(format_name("zhang san"))
print(format_name("  wang  xiao ming  "))


# ============================================================
# 练习 2：字符串分割与连接 — CSV 解析
# ============================================================

data = "101,张三,20,计算机科学,北京"

# a) 分割
fields = data.split(",")
print(f"\n=== 练习2: CSV 解析 ===")
print(f"分割: {fields}")

# b) 连接
joined = " | ".join(fields)
print(f"连接: {joined}")


# ============================================================
# 练习 3：文件写入 — 生成学生数据文件
# ============================================================

def generate_student_file(filename, students):
    """把学生列表写入文件"""
    with open(filename, "w", encoding="utf-8") as f:
        for s in students:
            f.write(f"{s['id']},{s['name']},{s['score']}\n")
    print(f"[OK] 已生成 {filename}，共 {len(students)} 条记录")

print(f"\n=== 练习3: 生成学生数据文件 ===")
test_students = [
    {"id": "101", "name": "张三", "score": 85},
    {"id": "102", "name": "李四", "score": 92},
    {"id": "103", "name": "王五", "score": 78},
]
generate_student_file("students.csv", test_students)

# 验证：读出来看看
with open("students.csv", "r", encoding="utf-8") as f:
    print(f.read())


# ============================================================
# 练习 4：文件读取 — 词频统计器
# ============================================================

def count_words(filename):
    """统计文件中每个单词的出现次数"""
    word_count = {}
    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                # 简单处理：去掉标点，分割单词
                # 先全部转小写
                line = line.lower()
                # 去掉常见标点（简单版）
                for ch in ".,!?;:\"'()[]{}":
                    line = line.replace(ch, " ")
                # 分割并统计
                for word in line.split():
                    if word in word_count:
                        word_count[word] += 1
                    else:
                        word_count[word] = 1
    except FileNotFoundError:
        print(f"[错误] 文件 {filename} 不存在")
        return {}
    return word_count

print(f"\n=== 练习4: 词频统计器 ===")
# 先创建一个测试文件
test_text = """Hello World
Hello Python
Python is great
Hello from Python World"""

with open("wordcount_test.txt", "w", encoding="utf-8") as f:
    f.write(test_text)

result = count_words("wordcount_test.txt")

# 按频率从高到低排序打印
print("词频统计结果:")
for word, count in sorted(result.items(), key=lambda x: x[1], reverse=True):
    print(f"  {word}: {count}")


# ============================================================
# 练习 5：异常处理 — 安全的数字输入
# ============================================================

def get_number(prompt):
    """反复提示直到输入合法数字"""
    while True:
        user_input = input(prompt)
        try:
            return float(user_input)
        except ValueError:
            print("请输入有效的数字！")

# 注意：因为这是 solution 文件，直接运行会让用户输入
# 所以这里注释掉，同学们自己取消注释测试
# print(f"\n=== 练习5: 安全的数字输入 ===")
# num = get_number("请输入一个数字: ")
# print(f"你输入的数字是: {num}")


# ============================================================
# 练习 6：异常处理 — 安全的文件读取器
# ============================================================

def read_file_safely(filepath):
    """安全读取文件，处理各种异常"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"[提示] 文件不存在: {filepath}")
        return None
    except PermissionError:
        print(f"[错误] 没有读取权限: {filepath}")
        return None
    except UnicodeDecodeError:
        # utf-8 失败，试试 gbk（Windows 常用编码）
        print(f"[提示] utf-8 解码失败，尝试用 gbk 编码...")
        try:
            with open(filepath, "r", encoding="gbk") as f:
                return f.read()
        except Exception as e:
            print(f"[错误] gbk 也失败了: {e}")
            return None
    except Exception as e:
        print(f"[错误] 未知错误: {e}")
        return None

print(f"\n=== 练习6: 安全的文件读取器 ===")
# 测试不存在的文件
result = read_file_safely("不存在.txt")
print(f"不存在文件: {result}")

# 测试存在的文件
result = read_file_safely("students.csv")
if result:
    print(f"students.csv 内容:\n{result}")


# ============================================================
# 练习 7（综合挑战）：文件版通讯录升级
# ============================================================

CONTACTS_FILE = "my_contacts.txt"

def load_contacts(filepath=CONTACTS_FILE):
    """从文件加载通讯录"""
    contacts = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(",")
                if len(parts) >= 3:
                    contacts.append({
                        "id": int(parts[0]),
                        "name": parts[1],
                        "phone": parts[2],
                        "email": parts[3] if len(parts) > 3 else ""
                    })
        print(f"[加载] 从 {filepath} 读取了 {len(contacts)} 条记录")
    except FileNotFoundError:
        print(f"[提示] {filepath} 不存在，从空通讯录开始")
    return contacts


def save_contacts(contacts, filepath=CONTACTS_FILE):
    """保存通讯录到文件"""
    with open(filepath, "w", encoding="utf-8") as f:
        for c in contacts:
            f.write(f"{c['id']},{c['name']},{c['phone']},{c.get('email', '')}\n")


def get_next_id(contacts):
    """获取下一个可用 ID"""
    if not contacts:
        return 1
    return max(c["id"] for c in contacts) + 1


def add_contact(contacts, name, phone, email=""):
    """添加联系人并自动保存"""
    contact = {
        "id": get_next_id(contacts),
        "name": name,
        "phone": phone,
        "email": email
    }
    contacts.append(contact)
    save_contacts(contacts)
    print(f"[OK] 已添加: {name} (ID: {contact['id']})")


def find_contact(contacts, keyword):
    """按姓名或电话模糊查找"""
    results = []
    keyword = keyword.lower()
    for c in contacts:
        if keyword in c["name"].lower() or keyword in c["phone"]:
            results.append(c)
    return results


def delete_contact(contacts, contact_id):
    """按 ID 删除联系人"""
    for i, c in enumerate(contacts):
        if c["id"] == contact_id:
            removed = contacts.pop(i)
            save_contacts(contacts)
            print(f"[OK] 已删除: {removed['name']}")
            return True
    print(f"[失败] 未找到 ID: {contact_id}")
    return False


def list_contacts(contacts):
    """显示所有联系人"""
    if not contacts:
        print("通讯录为空")
        return
    print("\n====== 通讯录 ======")
    for c in contacts:
        print(f"  [{c['id']}] {c['name']} | {c['phone']} | {c['email']}")
    print(f"共 {len(contacts)} 人\n")


def run_menu():
    """命令行主菜单"""
    contacts = load_contacts()

    while True:
        print("\n======== 通讯录管理系统 ========")
        print("1. 查看所有联系人")
        print("2. 添加联系人")
        print("3. 查找联系人")
        print("4. 删除联系人")
        print("5. 退出")
        print("================================")

        choice = input("请选择 (1-5): ").strip()

        if choice == "1":
            list_contacts(contacts)

        elif choice == "2":
            name = input("姓名: ").strip()
            if not name:
                print("姓名不能为空！")
                continue
            phone = input("电话: ").strip()
            if not phone:
                print("电话不能为空！")
                continue
            email = input("邮箱 (可选): ").strip()
            add_contact(contacts, name, phone, email)

        elif choice == "3":
            keyword = input("输入姓名或电话搜索: ").strip()
            results = find_contact(contacts, keyword)
            if results:
                print(f"\n找到 {len(results)} 条记录:")
                for c in results:
                    print(f"  [{c['id']}] {c['name']} | {c['phone']} | {c['email']}")
            else:
                print("未找到匹配的联系人")

        elif choice == "4":
            try:
                cid = int(input("输入要删除的联系人 ID: "))
                delete_contact(contacts, cid)
            except ValueError:
                print("请输入有效的数字 ID！")

        elif choice == "5":
            print("再见！")
            break

        else:
            print("无效选项，请选择 1-5")


# 如果直接运行本文件，启动菜单
if __name__ == "__main__":
    print("\n=== 练习7: 文件版通讯录 ===")
    print("提示：因为这是 solution 文件，运行 run_menu() 会启动交互菜单")
    print("你可以取消下面的注释来测试：")
    print("  # run_menu()")
    # run_menu()  # ← 取消这行的注释来启动通讯录

print("\n[Congrats!] Day 3 练习完成！")
