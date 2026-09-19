import asyncio

class TaskLimiter:
    """限制并发任务数量"""
    
    def __init__(self,max_concurrent:int):
        # 信号量 = 计数器 + FIFO 队列，初始发放 max_concurrent 个"令牌"
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.tasks = []

    async def add_task(self,coro):
        """添加任务 （受并发限制）"""
        # 拿令牌才能进：有令牌就立刻拿（计数-1）；没有就挂起排队，等别人归还
        async with self.semaphore:
            return await coro
        # 离开 with 块 = 自动归还令牌（计数+1），并唤醒队列头部的第一个排队者

    async def run_tasks(self,coros):
        """运行多个任务"""
        # 把 10 个协程一次性全部包成 Task 提交：前 3 个抢到令牌开工，
        # 剩下 7 个堵在信号量门口排队
        tasks = [asyncio.create_task(self.add_task(coro)) for coro in coros]
        # gather 会等所有任务（含还在排队的）全部完成才返回
        return await asyncio.gather(*tasks)
    
async def fetch_data(url:str):
    """模拟发送请求的后台任务"""
    await asyncio.sleep(2)
    print(f"请求已发送: {url}")

async def main():
    limiter = TaskLimiter(max_concurrent = 3)
    
    coros = [fetch_data(f"url{i}")for i in range(10)]
    
    results = await limiter.run_tasks(coros)
    return results

asyncio.run(main())

# ============================================================
# 并发限制是怎么实现的（TaskLimiter 逻辑）
# ============================================================
# 核心就一个东西：asyncio.Semaphore(3) —— 计数器 + FIFO 排队队列
#
#   进入 async with   → 拿令牌：计数 > 0 就减 1 直接放行；
#                       计数 == 0 就把协程挂起，排到队列末尾
#                       （是"挂起排队"，不是 while 循环空转轮询）
#   退出 async with   → 还令牌：计数 +1，唤醒队列头部的第一个协程
#
# 注意：全程依然只有一个线程。限制的只是"同一时刻有多少协程
# 处于 semaphore 块内部"，与进程/线程无关。
#
# 时间流（10 个任务 × 每个 2 秒，令牌 3 个）：
#
# t=0s   10 个 add_task 被 create_task 一次性全部提交，
#        依次运行到 async with 这一行：
#        ├─ 任务0/1/2 拿到令牌（计数 3→0）→ 进入 fetch_data，睡 2 秒
#        └─ 任务3~9 拿不到令牌，挂在信号量门口排队（队列顺序 3,4,...,9）
#
# t=2s   任务0/1/2 同时醒来 → 打印 → 协程 return → 退出 with 块，
#        每退出一个就还一枚令牌，唤醒队列头部一个等待者：
#        ├─ 任务0 归还 → 唤醒任务3
#        ├─ 任务1 归还 → 唤醒任务4
#        └─ 任务2 归还 → 唤醒任务5
#        任务6~9 继续排队
#
# t=4s   任务3/4/5 完成 → 同样接力唤醒任务6/7/8
# t=6s   任务6/7/8 完成 → 唤醒任务9
# t=8s   任务9 完成 → 10 个任务全部 done → gather 返回 → main 结束
#
# 波形图（每波最多 3 个并发）：
#   0~2s   任务0 1 2      ← 第 1 波
#   2~4s   任务3 4 5      ← 第 2 波
#   4~6s   任务6 7 8      ← 第 3 波
#   6~8s   任务9          ← 第 4 波
# 总耗时 8 秒：既不排成一串（20 秒），也不一拥而上（2 秒）
#
# 关键点：
# 1. 限制范围由 async with 块的大小决定——这里包住整个 await coro，
#    即限制的是"整个任务"；若只想限制其中一小段（如只限制网络请求），
#    就把 semaphore 的 with 块挪到那一小段。
# 2. create_task 必须一次全提交：所有任务先"都想跑"，信号量才有排队可言；
#    如果改成顺序 await，就成了串行执行，信号量形同虚设。
# 3. fetch_data 没有 return 语句，所以 run_tasks 返回的
#    results 是 10 个 None 组成的列表。
# ============================================================