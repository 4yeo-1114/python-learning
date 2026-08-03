"""
============================================================
Day 15 笔记：项目收尾 — Bootstrap 美化 / 工程化规范
============================================================
今天是冲刺阶段的最后一天！把 Day 14 的 CRUD 项目打磨成"可交付"的状态。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
一、Bootstrap — 前端 CSS 框架
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**是什么？**
    Bootstrap 是 Twitter 开源的前端 UI 框架。提供了一套预定义 CSS 类，
    你只需要给 HTML 元素加上 class="xxx"，就能获得漂亮的样式。
    不需要自己写 CSS！

**为什么用 Bootstrap？**
    1. 手写 CSS 费时间，而且不同浏览器效果不一致
    2. Bootstrap 自带响应式设计（手机/平板/桌面自适应）
    3. 组件丰富：导航栏、表格、按钮、表单、警告框、卡片...
    4. 学习成本低 — 复制官方示例，改改文字就能用

**两种引入方式：**

    # 方式 1：CDN（推荐，无需下载）
    # 在 HTML <head> 中加一行：
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
          rel="stylesheet">
    # 在 </body> 前加 JS：
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js">
    </script>

    # 方式 2：下载到本地（离线可用）
    # pip install bootstrap-flask  # 有专门的 Flask 扩展
    # 但我们用 CDN 就够了，简单且加载快

**核心概念：**

    1. 栅格系统（Grid System）
       Bootstrap 把页面分成 12 列，通过 class 控制元素占几列：
       <div class="container">
           <div class="row">
               <div class="col-md-6">左侧占 6 列（50%）</div>
               <div class="col-md-6">右侧占 6 列（50%）</div>
           </div>
       </div>
       断点：col- (手机) / col-sm- (平板竖) / col-md- (平板横) / col-lg- (桌面)

    2. 常用组件速查表：

       导航栏：
       <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
           <div class="container-fluid">
               <a class="navbar-brand" href="#">品牌名</a>
               <div class="navbar-nav">
                   <a class="nav-link" href="#">链接</a>
               </div>
           </div>
       </nav>

       按钮：
       <button class="btn btn-primary">主要</button>
       <button class="btn btn-success">成功</button>
       <button class="btn btn-danger">危险</button>
       <button class="btn btn-warning">警告</button>
       <a href="#" class="btn btn-outline-primary">轮廓按钮</a>
       尺寸：btn-sm(小) / btn(默认) / btn-lg(大)

       表格：
       <table class="table table-striped table-hover">
       table-striped = 斑马纹 / table-hover = 鼠标悬停高亮

       表单：
       <div class="mb-3">
           <label class="form-label">姓名</label>
           <input type="text" class="form-control">
       </div>
       mb-3 = margin-bottom（间距）/ form-control = 美化输入框

       警告框（替代手写 flash 样式）：
       <div class="alert alert-success">成功消息</div>
       <div class="alert alert-danger">错误消息</div>
       <div class="alert alert-warning">警告消息</div>
       <div class="alert alert-info">提示消息</div>
       可关闭的警告框：
       <div class="alert alert-warning alert-dismissible fade show">
           内容
           <button class="btn-close" data-bs-dismiss="alert"></button>
       </div>

    3. 工具类（Utility Classes）：
       - 间距：mt-3(上) mb-3(下) ms-3(左) me-3(右) p-3(内边距)
       - 文字：text-center text-muted text-danger fw-bold
       - 背景：bg-light bg-dark bg-white
       - 边框：border rounded shadow

**从手写 CSS 迁移到 Bootstrap 的思路：**
    1. 删掉 <style> 标签中的所有手写 CSS
    2. 给 HTML 元素加上对应的 Bootstrap class
    3. <button class="btn"> → <button class="btn btn-primary">
    4. <table> → <table class="table table-striped table-hover">
    5. flash 消息 → Bootstrap alert
    6. 导航栏 → Bootstrap navbar
    7. 如果某种样式 Bootstrap 没有 → 再写一小段自定义 CSS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
二、requirements.txt — 依赖管理
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**是什么？**
    一个文本文件，列出项目依赖的 Python 包及版本。
    别人拿到代码后，执行 pip install -r requirements.txt 就能一键安装所有依赖。

**如何生成？**
    # 方法 1：用 pip freeze（导出当前环境所有包）
    pip freeze > requirements.txt
    # 问题：会把所有包都导出，包括项目没直接用的

    # 方法 2：手动编写（推荐，只写项目真正需要的）
    # 创建 requirements.txt，内容：
    Flask==3.1.2
    pytest==9.1.1

**如何安装？**
    pip install -r requirements.txt

**Flask 项目最小 requirements.txt：**
    Flask==3.1.2
    # 如果用了数据库，不需要额外包（sqlite3 是 Python 标准库）
    # 如果用了测试：
    pytest==9.1.1

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
三、README.md — 项目说明文档
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**README.md 是项目的"门面"。** 别人打开你的 GitHub 仓库第一眼看到的就是它。

**一个好的 README 应该包含：**

    # 项目名称
    一句话描述项目做什么

    ## 功能
    - 用户注册/登录
    - 学生信息增删改查
    - 搜索...

    ## 技术栈
    - Python 3.14 + Flask + SQLite
    - Bootstrap 5（前端）

    ## 快速开始
    1. git clone xxx
    2. pip install -r requirements.txt
    3. python app.py
    4. 浏览器打开 http://localhost:5000
    5. 测试账号: admin / admin123

    ## 项目结构
    app.py             主程序
    templates/         HTML 模板
    README.md          项目说明

    ## 路由说明
    GET  /              首页
    ...

**Markdown 基本语法：**
    # 一级标题   ## 二级标题   ### 三级标题
    **粗体**   *斜体*   `行内代码`
    - 无序列表   1. 有序列表
    [链接文字](URL)   ![图片描述](图片URL)
    ```python
    代码块
    ```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
四、.gitignore — 告诉 Git 忽略哪些文件
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**为什么需要？**
    有些文件不应该提交到 Git：
    - __pycache__/      Python 编译缓存
    - *.db              SQLite 数据库文件（包含真实数据）
    - .pytest_cache/    pytest 缓存
    - venv/             虚拟环境（太大，用 requirements.txt 替代）

**Python 项目标准 .gitignore：**
    # Python
    __pycache__/
    *.py[cod]
    *.pyo
    *.db

    # Virtual Environment
    venv/
    .venv/

    # IDE
    .vscode/
    .idea/

    # Testing
    .pytest_cache/

    # OS
    .DS_Store
    Thumbs.db

**使用方式：**
    在项目根目录创建 .gitignore 文件，每行一个匹配规则。
    Git 会自动忽略匹配的文件和目录。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
五、Python 项目目录结构规范
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**小型 Flask 项目的推荐结构：**
    project/
    ├── app.py              # 主入口文件（或 run.py）
    ├── templates/          # Jinja2 模板（Flask 自动找这个目录）
    │   ├── layout.html     # 基础模板（其他模板继承它）
    │   ├── index.html      # 首页
    │   ├── login.html      # 登录页
    │   └── ...
    ├── static/             # 静态文件（CSS/JS/图片）
    │   └── style.css       # 自定义样式（如果用 Bootstrap CDN 则可无）
    ├── requirements.txt    # 依赖清单
    ├── README.md           # 项目说明
    ├── .gitignore          # Git 忽略规则
    └── tests/              # 测试文件（可选）
        └── test_app.py

**什么是 static 目录？**
    Flask 会自动把 static/ 目录下的文件映射到 /static URL：
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
    → 生成 /static/style.css

    如果用 Bootstrap CDN，就不需要 static 目录。
    但如果有自定义 CSS/JS/图片，放 static/ 里。

**命名建议：**
    - 主文件叫 app.py 或 run.py（约定俗成）
    - 模块用下划线命名: user_db.py, student_db.py
    - 模板用下划线命名: student_list.html, add_student.html
    - 不要用中文命名文件和目录（某些系统会出问题）

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
六、CSS 框架对比（拓展知识）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    框架        特点                    适用场景
    ────────    ────────                ────────
    Bootstrap   最流行，组件最多         快速原型、后台管理
    Tailwind    工具类优先，高度可定制    追求独特设计
    Bulma       纯 CSS，无 JS 依赖      简单项目
    Picocss     极简，自动美化原生 HTML   学习/小项目

    我们选 Bootstrap 是因为：
    - 资料最多，中文教程丰富
    - 组件最全面（navbar/table/form/alert 开箱即用）
    - 适合学生管理系统这样的 CRUD 后台

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
今日学习要点总结
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Bootstrap CDN：一行 <link> 引入，用 class 控制样式
2. 核心组件：navbar / table / btn / form-control / alert
3. requirements.txt：记录依赖，pip install -r 一键安装
4. README.md：项目的门面，告诉别人怎么用
5. .gitignore：避免把缓存、数据库、虚拟环境提交到 Git
6. 项目结构：app.py + templates/ + static/ + requirements.txt + README.md
"""
