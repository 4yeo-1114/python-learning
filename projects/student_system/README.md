# 学生管理系统

基于 Flask + SQLite + Bootstrap 5 的 Web 学生信息管理系统。

## 功能

- 用户注册与登录（SHA256 + 盐值加密）
- 学生信息增删改查（CRUD）
- 按姓名/专业模糊搜索
- 登录保护（未登录自动跳转）
- Bootstrap 5 响应式界面（手机/平板/桌面适配）

## 技术栈

| 层 | 技术 |
|---|---|
| 后端 | Python 3 + Flask |
| 数据库 | SQLite3（标准库，零配置） |
| 前端 | Bootstrap 5 CDN |
| 安全 | session 登录态 + PRG 防重复提交 |

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动
python app.py

# 3. 浏览器打开
http://localhost:5000
```

**测试账号**: `admin` / `admin123`

## 项目结构

```
student_system/
├── app.py              # 主程序
├── templates/          # Jinja2 模板（Bootstrap 5）
│   ├── layout.html     # 基础布局
│   ├── index.html      # 首页
│   ├── login.html      # 登录
│   ├── register.html   # 注册
│   ├── student_list.html  # 列表 + 搜索
│   ├── add_student.html   # 添加
│   └── edit_student.html  # 编辑
├── requirements.txt    # Python 依赖
├── .gitignore          # Git 忽略规则
└── README.md           # 本文件
```

## API 路由

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/` | 首页 |
| GET/POST | `/login` | 登录 |
| GET | `/logout` | 退出 |
| GET/POST | `/register` | 注册 |
| GET | `/students` | 列表 `?q=关键字` 搜索 |
| GET/POST | `/students/add` | 添加 |
| GET/POST | `/students/<id>/edit` | 编辑 |
| POST | `/students/<id>/delete` | 删除 |
