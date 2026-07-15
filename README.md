# Python 学习笔记

从 C++ 转 Python 的学习记录，跟着一个 6 周的自学计划走，目标是能用 Python 独立写一个学生登录管理系统。

## 进度

- [x] **Day 1** — 环境搭建 & 基础语法（print、注释、缩进）
- [x] **Day 2** — 数据结构（list / tuple / dict / set、切片、推导式）
- [ ] Day 3~7 — 控制流、函数、文件操作…
- [ ] Week 2 — 面向对象、异常处理、装饰器
- [ ] Week 3 — SQLite、JSON/CSV、pathlib
- [ ] Week 4 — 命令行版学生管理系统
- [ ] Week 5 — GUI（Tkinter）或 Web（Flask）
- [ ] Week 6 — 重构、扩展、收尾

## 目录结构

```
.
├── 学习计划.md              # 完整的 6 周学习路线
├── projects/
│   ├── day01_basics/        # Day 1：基础语法
│   ├── day02_data_structures/  # Day 2：数据结构
│   └── student_system_cli/  # 最终项目（进行中）
└── README.md
```

每个 day 文件夹里一般是：
- `dayXX_notes.py` — 当天学到的知识点和代码片段
- `dayXX_exercise.py` — 练习题（里面只有 TODO，答案在 solution 文件里）

## 背景

之前写 C++，想补一手 Python。这个仓库就是边学边练的记录，从最基础的语法一路写到能做个完整的项目。

对比 C++ 和 Python 的写法差异是主要的学习方式——很多 Python 里"为什么这么写"的问题，放回 C++ 的语境里就很好理解。

## 最终项目

一个带命令行界面的**学生登录管理系统**，大概包含：

- 用户注册 / 登录（密码哈希存储）
- 学生信息的增删查改
- 管理员 vs 普通学生的权限区分
- SQLite 做数据持久化
- 后续可能会加 GUI 或 Web 界面

## 参考资料

- [Python 官方教程](https://docs.python.org/zh-cn/3/tutorial/)
- 《流畅的 Python》(Fluent Python)
- [Real Python](https://realpython.com/)
