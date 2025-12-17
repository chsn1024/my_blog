# 🚀 Simple Flask Blog

这是一个基于 Python Flask 框架开发的极简博客系统。

## 🌟 项目亮点
- **零数据库**：直接读取 `posts/` 文件夹下的 Markdown 文件，无需配置数据库。
- **即插即用**：只需添加 `.md` 文件即可发布新博文。
- **极简架构**：代码结构清晰，非常适合 Flask 初学者参考。

---

## 📂 目录结构
```text
my_blog/
├── app.py              # Flask 主程序
├── posts/              # 存放 Markdown 文章源文件
│   ├── 1.md
│   └── 2.md
├── static/             # 存放 CSS 样式、图片等
└── templates/          # HTML 模板
    ├── index.html      # 博客首页（文章列表）
    └── post.html       # 文章详情页