"""
============================================================
Day 3 参考答案：文件操作 + 字符串 + 异常处理
============================================================
做完练习后再看哦！
"""

# ============================================================
# 练习 1：CSV 解析 + 文件写入
# ============================================================

data = "101,张三,20,计算机科学,北京"

# a) 分割 + 连接
fields = data.split(",")
print(f"分割: {fields}")
print(f"连接: {' | '.join(fields)}")

# b) 写文件
def save_students(filename, students):
    """把学生列表写入文件"""
    with open(filename, "w", encoding="utf-8") as f:
        for s in students:
            f.write(f"{s['id']},{s['name']},{s['score']}\n")
    print(f"[OK] 已保存 {len(students)} 条记录到 {filename}")

print(f"\n=== 练习1 测试 ===")
test_students = [
    {"id": "101", "name": "张三", "score": 85},
    {"id": "102", "name": "李四", "score": 92},
    {"id": "103", "name": "王五", "score": 78},
]
save_students("students.csv", test_students)

# 验证
with open("students.csv", "r", encoding="utf-8") as f:
    print(f.read())


# ============================================================
# 练习 2：词频统计器
# ============================================================

def count_words(filename):
    """统计文件中每个单词的出现次数"""
    word_count = {}
    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.lower()
                for ch in ".,!?;:\"'()[]{}":
                    line = line.replace(ch, " ")
                for word in line.split():
                    word_count[word] = word_count.get(word, 0) + 1
    except FileNotFoundError:
        print(f"[错误] 文件 {filename} 不存在")
        return {}

    # 按频率从高到低打印
    sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
    for word, count in sorted_words:
        print(f"  {word}: {count}")
    return word_count

print(f"\n=== 练习2 测试 ===")
# 创建测试文件
with open("wordcount_test.txt", "w", encoding="utf-8") as f:
    f.write("Hello World\nHello Python\nPython is great\nHello from Python World")

count_words("wordcount_test.txt")


# ============================================================
# 练习 3：安全的文件读取
# ============================================================

def read_file_safely(filepath):
    """安全读取文件，处理各种异常"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"[提示] 文件不存在: {filepath}")
        return None
    except UnicodeDecodeError:
        print(f"[提示] utf-8 解码失败，尝试 gbk...")
        try:
            with open(filepath, "r", encoding="gbk") as f:
                return f.read()
        except Exception as e:
            print(f"[错误] gbk 也失败了: {e}")
            return None
    except Exception as e:
        print(f"[错误] 未知错误: {e}")
        return None

print(f"\n=== 练习3 测试 ===")
print(f"不存在文件: {read_file_safely('不存在.txt')}")
print(f"正常读取: {read_file_safely('students.csv')[:50] if read_file_safely('students.csv') else 'None'}...")


# ============================================================
# 练习 4（综合）：文件版通讯录
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
                if len(parts) >= 2:
                    contacts.append({
                        "name": parts[0],
                        "phone": parts[1],
                        "email": parts[2] if len(parts) > 2 else ""
                    })
        print(f"[加载] 从 {filepath} 读取了 {len(contacts)} 条记录")
    except FileNotFoundError:
        print(f"[提示] {filepath} 不存在，从空通讯录开始")
    return contacts


def save_contacts(contacts, filepath=CONTACTS_FILE):
    """保存通讯录到文件"""
    with open(filepath, "w", encoding="utf-8") as f:
        for c in contacts:
            f.write(f"{c['name']},{c['phone']},{c.get('email', '')}\n")


def add_contact(contacts, name, phone, email=""):
    """添加联系人并自动保存"""
    contacts.append({"name": name, "phone": phone, "email": email})
    save_contacts(contacts)
    print(f"[OK] 已添加: {name}")


def find_contact(contacts, keyword):
    """按姓名或电话模糊查找"""
    results = []
    for c in contacts:
        if keyword.lower() in c["name"].lower() or keyword in c["phone"]:
            results.append(c)
    return results


def list_contacts(contacts):
    """显示所有联系人"""
    if not contacts:
        print("通讯录为空")
        return
    print("\n====== 通讯录 ======")
    for i, c in enumerate(contacts, 1):
        print(f"  {i}. {c['name']} | {c['phone']} | {c.get('email', '')}")
    print(f"共 {len(contacts)} 人\n")


def run_menu():
    """命令行主菜单"""
    contacts = load_contacts()

    while True:
        print("\n==== 通讯录 ====")
        print("1. 查看  2. 添加  3. 查找  4. 退出")
        choice = input("选择: ").strip()

        if choice == "1":
            list_contacts(contacts)
        elif choice == "2":
            name = input("姓名: ").strip()
            phone = input("电话: ").strip()
            email = input("邮箱 (可选): ").strip()
            if name and phone:
                add_contact(contacts, name, phone, email)
            else:
                print("姓名和电话不能为空！")
        elif choice == "3":
            keyword = input("输入姓名或电话搜索: ").strip()
            results = find_contact(contacts, keyword)
            if results:
                for c in results:
                    print(f"  {c['name']} | {c['phone']} | {c.get('email', '')}")
            else:
                print("未找到")
        elif choice == "4":
            print("再见！")
            break
        else:
            print("无效选项")

# 取消注释来启动通讯录
# if __name__ == "__main__":
#     run_menu()

print(f"\n=== 练习4 测试 ===")
# 用代码演示（不用菜单）
demo_contacts = []
add_contact(demo_contacts, "张三", "13800138000", "zhang@mail.com")
add_contact(demo_contacts, "李四", "13900139000")
list_contacts(demo_contacts)
print(f"查找'张': {find_contact(demo_contacts, '张')}")

print("\n[Congrats!] Day 3 练习完成！")
