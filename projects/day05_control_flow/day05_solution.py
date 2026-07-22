"""
============================================================
Day 5 练习题答案 — 控制流
============================================================
先自己做完再看答案！
"""

# ============================================================
# 练习 1：猜数字游戏
# ============================================================

import random

target = random.randint(1, 100)
MAX_ATTEMPTS = 7
attempts = 0

print(f"我已想好一个 1~100 的数，你有 {MAX_ATTEMPTS} 次机会！")

while attempts < MAX_ATTEMPTS:
    guess = int(input("猜一个数: "))
    attempts += 1

    if guess == target:
        print(f"对了！你用了 {attempts} 次就猜对了 🎉")
        break
    elif guess < target:
        print("太小了！")
    else:
        print("太大了！")
else:
    # while...else: 循环没有被 break 中断时执行
    print(f"机会用完了！答案是 {target}")


# ============================================================
# 练习 2：FizzBuzz 变体
# ============================================================

print("\n" + "=" * 40)
print("FizzBuzz (1~50)")
print("=" * 40)

for i in range(1, 51):
    if i % 3 == 0 and i % 5 == 0:
        print("FizzBuzz", end=" ")
    elif i % 3 == 0:
        print("Fizz", end=" ")
    elif i % 5 == 0:
        print("Buzz", end=" ")
    else:
        print(i, end=" ")

    # 每 10 个换行
    if i % 10 == 0:
        print()

print()  # 最后的换行


# ============================================================
# 练习 3：通讯录命令行工具
# ============================================================

import os

CONTACTS_FILE = "contacts.txt"


def load_contacts(filename):
    """从文件加载通讯录，返回列表"""
    contacts = []
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split(",")
                    if len(parts) == 2:
                        contacts.append({
                            "name": parts[0],
                            "phone": parts[1]
                        })
    return contacts


def save_contacts(contacts, filename):
    """保存通讯录到文件"""
    with open(filename, "w", encoding="utf-8") as f:
        for c in contacts:
            f.write(f"{c['name']},{c['phone']}\n")


def search_contact(contacts, keyword):
    """搜索联系人，返回匹配的列表"""
    results = []
    for c in contacts:
        if keyword in c["name"]:         # 支持模糊搜索
            results.append(c)
    return results


def main():
    contacts = load_contacts(CONTACTS_FILE)

    while True:
        print("\n=== 通讯录 ===")
        print("1.添加  2.查看  3.搜索  4.退出")
        cmd = input("> ").strip()

        if cmd == "1":
            name = input("姓名: ").strip()
            phone = input("电话: ").strip()
            if name and phone:
                contacts.append({"name": name, "phone": phone})
                print("已添加！")
            else:
                print("姓名和电话不能为空！")

        elif cmd == "2":
            if not contacts:
                print("通讯录为空")
            else:
                for i, c in enumerate(contacts, 1):
                    print(f"  {i}. {c['name']} — {c['phone']}")

        elif cmd == "3":
            keyword = input("搜索: ").strip()
            results = search_contact(contacts, keyword)
            if results:
                for c in results:
                    print(f"  找到: {c['name']} — {c['phone']}")
            else:
                print(f"  没找到与 '{keyword}' 相关的联系人")

        elif cmd == "4":
            save_contacts(contacts, CONTACTS_FILE)
            print("已保存，再见！")
            break

        else:
            print("无效命令，请输入 1~4")


if __name__ == "__main__":
    main()
