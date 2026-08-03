# 学生管理系统

基于 Flask + SQLite 的 Web 学生信息管理系统，支持用户注册/登录、学生信息增删改查（CRUD）、关键字搜索。

## 功能

- 🔐 用户注册与登录（密码 SHA256 + 盐值加密）
- 📋 学生信息管理（增删改查）
- 🔍 按姓名/专业模糊搜索
- 🛡️ 登录保护（未登录无法访问功能页）
- 🎨 Bootstrap 5 响应式界面（手机/平板/桌面自适应）
- ✅ PRG 模式（避免表单重复提交）+ Flash 消息

## 技术栈

- **后端**: Python 3.x + Flask
- **数据库**: SQLite3（标准库，无需额外安装）
- **前端**: Bootstrap 5 CDN
- **测试**: pytest

## 快速开始

```bash
# 1. 克隆项目
git clone <repo-url>
cd day15_wrapup

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动服务器
python day15_solution.py

# 4. 浏览器访问
# http://localhost:5000
```

**测试账号**: `admin` / `admin123`

## 项目结构

```
day15_wrapup/
├── day15_exercise.py     # 练习（带 TODO）
├── day15_solution.py     # 参考答案（完整功能）
├── day15_notes.py        # 学习笔记
├── test_app.py           # 自动化测试（pytest）
├── templates/            # Jinja2 模板
│   ├── layout.html       # 基础布局（Bootstrap 导航栏）
│   ├── index.html        # 首页
│   ├── login.html        # 登录页
│   ├── register.html     # 注册页
│   ├── student_list.html # 学生列表 + 搜索
│   ├── add_student.html  # 添加学生表单
│   └── edit_student.html # 编辑学生表单
├── requirements.txt      # Python 依赖清单
├── README.md             # 项目说明
└── .gitignore            # Git 忽略规则
```

## 路由说明

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/` | 首页 |
| GET/POST | `/login` | 登录 |
| GET | `/logout` | 退出 |
| GET/POST | `/register` | 注册 |
| GET | `/students` | 学生列表 + 搜索（`?q=关键字`） |
| GET/POST | `/students/add` | 添加学生 |
| GET/POST | `/students/<id>/edit` | 编辑学生 |
| POST | `/students/<id>/delete` | 删除学生 |

## 运行测试

```bash
cd day15_wrapup
pytest test_app.py -v
```

## 学习路径

本项目是 6 周 Python 学习计划的一部分：
- Day 9-10: CLI 认证 + CRUD 基础
- Day 11: pytest 单元测试
- Day 12-13: Flask Web 框架入门 + 数据库整合
- Day 14: Web CRUD 完成（RESTful 路由 / Flash / PRG）
- **Day 15: 项目收尾（Bootstrap 美化 + 工程化规范）** 👈 你在这里
