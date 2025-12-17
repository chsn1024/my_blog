# from flask import Flask, render_template, abort
# import os
# import markdown
# import frontmatter  # 用于解析 Markdown 文件中的元数据
#
# app = Flask(__name__)
# POSTS_DIR = 'posts'
#
#
# def load_posts():
#     """
#     加载并解析 posts/ 目录下的所有 Markdown 文件。
#     它假设每篇文章的文件名就是文章的 ID（例如：1.md -> id=1）。
#     它期望每篇 Markdown 文件都包含 YAML Front Matter 来定义标题和日期。
#     ---
#     title: 文章标题
#     date: YYYY-MM-DD
#     ---
#     文章正文...
#     """
#     all_posts = []
#
#     # 检查 posts 目录是否存在
#     if not os.path.exists(POSTS_DIR):
#         print(f"Error: Directory '{POSTS_DIR}' not found.")
#         return all_posts
#
#     # 遍历 posts 目录下的所有文件
#     for filename in os.listdir(POSTS_DIR):
#         if filename.endswith(".md"):
#             filepath = os.path.join(POSTS_DIR, filename)
#
#             # 尝试从文件名中解析 ID (例如 '1.md' -> 1)
#             try:
#                 # 假设文件名是 数字.md 格式
#                 post_id = int(os.path.splitext(filename)[0])
#             except ValueError:
#                 print(f"Warning: Skipping file '{filename}'. File name must be a number followed by .md.")
#                 continue
#
#             try:
#                 # 使用 frontmatter 库解析文件
#                 with open(filepath, 'r', encoding='utf-8') as f:
#                     post = frontmatter.load(f)
#
#                 # 将解析出的数据存储为一个字典
#                 post_data = {
#                     "id": post_id,
#                     "title": post.get('title', f"No Title (ID: {post_id})"),  # 获取 Front Matter 中的 title
#                     "date": post.get('date', 'Unknown Date'),  # 获取 Front Matter 中的 date
#                     "content": post.content,  # Markdown 正文
#                     "filename": filename  # 原始文件名
#
#                 }
#                 all_posts.append(post_data)
#
#             except Exception as e:
#                 print(f"Error loading file '{filename}': {e}")
#                 continue
#
#     # 按 ID 降序排序 (可选：通常按日期排序更好，但这里用 ID 方便演示)
#     all_posts.sort(key=lambda p: p['id'], reverse=True)
#
#     return all_posts
#
#
# # 在应用启动时加载所有博客数据
# # 注意：在生产环境中，这应该只在启动时加载一次，或者实现缓存机制。
# # 如果您需要在应用运行时实时更新，则需要在每次请求时调用 load_posts()，但这会牺牲性能。
# # 对于简易博客，我们保持简单，只在全局加载。
# POSTS = load_posts()
#
#
# # @app.route("/")
# # def index():
# #     """
# #     显示博客列表页。
# #     """
# #     # 只需要传递包含 id, title, date 的列表
# #     return render_template("index.html", posts=POSTS)
# #
# #
# # @app.route("/post/<int:post_id>")
# # def post_detail(post_id):
# #     """
# #     显示单篇博客文章详情页。
# #     """
# #     # 根据 post_id 查找对应的文章
# #     post = next((p for p in POSTS if p["id"] == post_id), None)
# #
# #     if post is None:
# #         # 使用 abort(404) 更好，它会自动返回 Flask 的 404 页面
# #         abort(404)
# #
# #         # 将 Markdown 正文内容渲染成 HTML
# #     html_content = markdown.markdown(
# #         post["content"],
# #         extensions=["fenced_code", "tables"]  # 启用代码块和表格扩展
# #     )
# #
# #     # 传递 post 的元数据和渲染后的 HTML 内容
# #     return render_template("post.html", post=post, content=html_content)
#
# @app.route("/")
# def index():
#     posts = load_posts()
#     return render_template("index.html", posts=posts)
#
# @app.route("/post/<int:post_id>")
# def post_detail(post_id):
#     posts = load_posts()
#     post = next((p for p in posts if p["id"] == post_id), None)
#     if post is None:
#         abort(404)
#     html_content = markdown.markdown(
#         post["content"],
#         extensions=["fenced_code", "tables"]
#     )
#     return render_template("post.html", post=post, content=html_content)
#
# @app.errorhandler(404)
# def page_not_found(error):
#     """
#     处理 404 错误。
#     """
#     return render_template('404.html'), 404  # 假定您有一个 404.html 模板
#
#
# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, render_template, abort
import os
import markdown
import frontmatter
import json  # ⭐ 引入 json 模块

app = Flask(__name__)
POSTS_DIR = 'posts'
VIEWS_FILE = 'views.json'  # ⭐ 定义浏览量数据文件名


# --- 浏览量数据持久化辅助函数 ---

def load_views():
    """从 views.json 文件中加载浏览量数据。"""
    if not os.path.exists(VIEWS_FILE):
        return {}  # 如果文件不存在，返回空字典
    try:
        with open(VIEWS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error reading {VIEWS_FILE}: {e}")
        return {}


def save_views(views_data):
    """将当前的浏览量数据保存到 views.json 文件。"""
    try:
        # 使用 w 模式写入文件
        with open(VIEWS_FILE, 'w', encoding='utf-8') as f:
            # 格式化输出 JSON，方便人类阅读
            json.dump(views_data, f, indent=4)
    except Exception as e:
        print(f"Error writing to {VIEWS_FILE}: {e}")


# --- 文章加载和应用启动 ---

def load_posts():
    """加载文章元数据，并合并浏览量。"""
    all_posts = []
    # 每次加载文章时，也加载最新的 views 数据
    current_views = load_views()

    # ... (文件检查和遍历逻辑保持不变) ...
    if not os.path.exists(POSTS_DIR):
        print(f"Error: Directory '{POSTS_DIR}' not found.")
        return all_posts

    for filename in os.listdir(POSTS_DIR):
        if filename.endswith(".md"):
            filepath = os.path.join(POSTS_DIR, filename)

            try:
                post_id_int = int(os.path.splitext(filename)[0])
                post_id_str = str(post_id_int)  # 使用字符串作为 JSON 字典的键
            except ValueError:
                continue

            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    post = frontmatter.load(f)

                post_data = {
                    "id": post_id_int,
                    "title": post.get('title', f"No Title (ID: {post_id_int})"),
                    "date": post.get('date', 'Unknown Date'),
                    "content": post.content,
                    "filename": filename,
                    # ⭐ 关键：从加载的 views 字典中获取浏览量，如果不存在则为 0
                    "views": current_views.get(post_id_str, 0)
                }
                all_posts.append(post_data)

            except Exception as e:
                print(f"Error loading file '{filename}': {e}")
                continue

    all_posts.sort(key=lambda p: p['id'], reverse=True)
    return all_posts


# ⭐ 全局加载文章元数据，但这次 views 字段将包含文件中的持久化数据
# posts = load_posts()


# --- 路由逻辑 ---

@app.route("/")
def index():
    posts = load_posts()
    """显示博客列表页。"""
    return render_template("index.html", posts=posts)


@app.route("/post/<int:post_id>")
def post_detail(post_id):
    """显示单篇博客文章详情页，并更新浏览量。"""
    posts = load_posts()
    post = next((p for p in posts if p["id"] == post_id), None)
    post_id_str = str(post_id)

    if post is None:
        abort(404)

        # 1. ⭐ 更新内存中的 POSTS 数据
    post["views"] += 1

    # 2. ⭐ 更新持久化文件
    current_views = load_views()
    current_views[post_id_str] = post["views"]
    save_views(current_views)

    # 渲染 Markdown 内容 (保持不变)
    html_content = markdown.markdown(
        post["content"],
        extensions=["fenced_code", "tables"]
    )

    return render_template("post.html", post=post, content=html_content)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == "__main__":
    # ⭐ 确保 views.json 文件在第一次运行时被创建
    if not os.path.exists(VIEWS_FILE):
        save_views({})

    app.run(debug=True)

