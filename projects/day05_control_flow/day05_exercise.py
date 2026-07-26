"""
============================================================
Day 5 练习题：控制流 — if / for / while
============================================================
答案在 day05_solution.py，做完再看！
"""

# ============================================================
# 练习 1：猜数字游戏（必做）
# ============================================================
# 写一个完整的猜数字游戏：
#
# 要求：
#   - 程序随机生成 1~100 之间的整数
#   - 玩家最多猜 7 次
#   - 每次猜完后提示"太大了" / "太大了" / "对了！"
#   - 猜对或次数用完时，显示结果并结束
#
# 提示：
#   - import random → random.randint(1, 100)
#   - 如果 7 次都没猜对，用 while...else 打印"机会用完了！答案是 X"
#   - input() 返回字符串，要 int() 转换
#
# 运行示例：
#   我已想好一个 1~100 的数，你有 7 次机会！
#   猜一个数: 50
#   太大了！
#   猜一个数: 25
#   太小了！
#   猜一个数: 37
#   对了！你用了 3 次就猜对了 🎉
# ============================================================

# TODO: 在这里写你的代码
import random
ans  = random.randint(1,100)
guess = 0
attempt = 0
Max_guess = 7
print(f"我已想好一个1~100的数,你有{Max_guess}次机会！")
while attempt<Max_guess:
    guess =  int(input("猜一个数:"))
    attempt += 1
    if guess == ans:
        print(f"对了!你用了{attempt}次就猜对了🎉")
        break
    elif guess < ans:
        print(f"太小了!")
    elif guess > ans:
        print(f"太大了!")
else:
    #while...else 循环没有被break中断时执行
    print(f"机会用完了!答案是{ans}!")

# ============================================================
# 练习 2：FizzBuzz 变体（控制流基础）
# ============================================================
# 打印 1~50 的数字，但：
#   - 遇到 3 的倍数，打印 "Fizz" 而不是数字
#   - 遇到 5 的倍数，打印 "Buzz" 而不是数字
#   - 遇到 3 和 5 的公倍数，打印 "FizzBuzz"
#   - 每打印 10 个就换一行
#
# 前几行预期输出：
#   1 2 Fizz 4 Buzz Fizz 7 8 Fizz Buzz
#   11 Fizz 13 14 FizzBuzz 16 17 Fizz 19 Buzz
#   ...
#
# 提示：
#   - 用 for i in range(1, 51)
#   - 用 if/elif/else 判断
#   - 用 end=" " 控制不换行，每 10 个用 print() 换行
# ============================================================

# TODO: 在这里写你的代码

for i in range(1,51):
    if i%15 ==0:
        print(f"FizzBuzz",end = " ")
    elif i%3==0:
        print(f"Fizz",end=" ")
    elif i%5 == 0:
        print(f"Buzz",end = " ")
    else:
        print(f"{i}",end = " ")
    if i% 10==0:
        print()
        

# ============================================================
# 练习 3：通讯录命令行工具（综合，选做）
# ============================================================
# 把 Day 3 的文件读写和今天的控制流结合起来！
#
# 写一个简单的命令行通讯录，支持以下命令：
#   1. 添加联系人（姓名, 电话）
#   2. 查看所有联系人
#   3. 搜索联系人（按姓名）
#   4. 退出（自动保存到文件 contacts.txt）
#
# 要求：
#   - 用 while True 循环读取用户命令
#   - 用 if/elif 分发命令
#   - 程序启动时从 contacts.txt 加载已有联系人
#   - 程序退出时保存联系人到 contacts.txt（每行：姓名,电话）
#   - 搜索时如果没有找到，打印提示
#
# 数据结构提示：
#   contacts = [{"name": "张三", "phone": "13800138000"}, ...]
#
# 运行示例：
#   === 通讯录 ===
#   1.添加  2.查看  3.搜索  4.退出
#   > 1
#   姓名: 张三
#   电话: 13800138000
#   已添加！
#   > 2
#   1. 张三 — 13800138000
#   > 3
#   搜索: 张三
#   找到: 张三 — 13800138000
#   > 4
#   已保存，再见！
# ============================================================

# TODO: 在这里写你的代码

import os

CONTACTS_FILE = "contacts.txt"

def load_contacts(filename):
    """从文件中加载通讯录 返回列表"""
    contacts = []
    if os.path.exists(filename):
        with open(filename,"r",encoding="utf-8") as f:
            for line in f:
                line  = line.strip()
                if line:
                    parts = line.split(",")
                    if len(parts) ==2:
                        contacts.append({
                            "name" : parts[0],
                            "phone" : parts[1]
                        })
    return contacts

def save_contacts(contacts,filename):
    """保存通讯录到文件"""      
    with open(filename,"w",encoding="utf-8") as f:
        for c in contacts:
            f.write(f"{c["name"]},{c["phone"]}\n")
       
def search_contact(contacts,keyword):
    results = []
    for c in contacts:
        if keyword in c["name"]:
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





print("\n[Congrats!] Day 5 练习完成！对比答案看 day05_solution.py")
