import aiofiles
import asyncio
from pathlib import Path
import asyncpg


#批量文件处理
#异步

async def async_process_files(file_paths):
    #定义一个异步处理文件的协程函数
    async def process_file(path):
        async with aiofiles.open(path,'r') as f:
            content = await f.read()
        return content

    tasks  = [process_file(path) for path in file_paths]
    result = await asyncio.gather(*tasks)
    return result

#异步数据库操作
async def fetch_users():
    conn = await asyncpg.connect('postgresql://..')
    try:
        users = await conn.fetch('SELECT * FROM users')
        return users
    finally:
        await conn.close()
        
# 并发查询多个表
async def fetch_all_data():
    users, posts, comments = await asyncio.gather(
        fetch_users(),
        fetch_posts(),
        fetch_comments()
    )
    return users, posts, comments
