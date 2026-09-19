import asyncio
from typing import List

class BackgroundTaskManager:
    """后台任务管理器"""
    
    def __init__(self):
        self.tasks:List[asyncio.Task] = []
    
    def add_task(self,coro):
        """添加后台任务"""
        task  = asyncio.create_task(coro)
        self.tasks.append(task)
        return task
    
    async def wait_all(self):
        if self.tasks:
            await asyncio.gather(*self.tasks,return_exceptions=True)
        
    def cancel_all(self):
        for task in self.tasks:
            if not task.done():
                task.cancel()
            

async def send_notification(delay: int, message: str):
    """模拟发送通知的后台任务"""
    await asyncio.sleep(delay)
    print(f"通知已发送: {message}")

async def main():
    manager = BackgroundTaskManager()
    
    manager.add_task(send_notification(1, "消息1"))
    manager.add_task(send_notification(2, "消息2"))
    
    # 主流程继续
    print("主流程执行中...")
    await asyncio.sleep(1)
    
    # 等待所有后台任务完成
    await manager.wait_all()
    print("所有任务完成")

asyncio.run(main())

# ============================================================
# 时间流说明：全程只有一个进程、一个线程
# 事件循环在同一个线程里轮番驱动各个 Task，遇到 await 才换人
# ============================================================
# t=0s  asyncio.run(main())  ← 创建事件循环，进程从这里开始
#       ├─ add_task(消息1)   协程对象包成 Task1 进队列（还没开始跑！）
#       ├─ add_task(消息2)   Task2 同理进队列
#       ├─ print("主流程执行中...")  ← 同步代码，直接打印
#       └─ await sleep(1)    main 挂起，控制权交还事件循环
#
# t=0s  事件循环调度队列：
#       ├─ Task1 开跑：await sleep(1) → 挂起，定 t=1s 的闹钟
#       └─ Task2 开跑：await sleep(2) → 挂起，定 t=2s 的闹钟
#       （全部挂起，事件循环空闲等待闹钟）
#
# t=1s  两个闹钟同时响：main 的和 Task1 的
#       ├─ main 先被唤醒（它的闹钟注册得早）：
#       │    await wait_all() → gather 等 Task1、Task2 都结束，main 再次挂起
#       ├─ Task1 被唤醒：print("通知已发送: 消息1") → 协程结束 → done
#       └─ Task2 还在睡
#
# t=2s  Task2 被唤醒：print("通知已发送: 消息2") → done
#       → gather 发现两个任务都结束 → wait_all 返回
#       → main 继续：print("所有任务完成") → main 结束
#       → asyncio.run 关闭事件循环 → 进程退出
#
# 输出顺序：
#   主流程执行中...
#   通知已发送: 消息1
#   通知已发送: 消息2
#   所有任务完成
#
# 关键点：
# 1. send_notification(1, "消息1") 只是创建协程对象，一行都不会执行；
#    真正开始跑是 asyncio.create_task() 之后，main 下一次 await 交出控制权时。
# 2. 协程函数 return（或抛异常）那一刻，Task 变为 done。
# 3. await 是换人信号：await sleep(1) 不是"卡住 1 秒"，
#    而是"我先睡，1 秒后叫我，这期间你爱干啥干啥"。
# 4. 如果没有 wait_all()，main 提前 return 时事件循环会强制取消
#    还在睡觉的 Task2，"通知已发送: 消息2"永远打不出来。
# ============================================================