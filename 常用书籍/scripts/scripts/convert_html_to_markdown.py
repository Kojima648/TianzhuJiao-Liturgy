# 脚本名称：convert_all_books_to_markdown.py
# 功能描述：批量处理所有 book_xx 的章节 HTML，提取 class="text" 内容并保存为 Markdown 文件

import os
import re
from bs4 import BeautifulSoup
from markdownify import markdownify as md

# 脚本所在目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# 所有章节页面目录
DOWNLOAD_BASE = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", "downloaded_pages"))

# 输出 markdown 目录
OUTPUT_BASE = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", "parsed_md"))
os.makedirs(OUTPUT_BASE, exist_ok=True)

# 遍历所有 book_xx 目录
for book_dir in os.listdir(DOWNLOAD_BASE):
    book_path = os.path.join(DOWNLOAD_BASE, book_dir)
    if not os.path.isdir(book_path) or not book_dir.startswith("book_"):
        continue

    print(f"\n📘 处理书籍：{book_dir}")

    output_book_path = os.path.join(OUTPUT_BASE, book_dir)
    os.makedirs(output_book_path, exist_ok=True)

    for chapter_id in os.listdir(book_path):
        html_path = os.path.join(book_path, chapter_id, "index.html")
        if not os.path.exists(html_path):
            continue

        try:
            with open(html_path, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f, "html.parser")

            content_div = soup.select_one("div.text")
            if not content_div:
                print(f"⚠️ 跳过：{chapter_id} 中未找到 .text 区块")
                continue

            # 转换 HTML → Markdown
            html_content = str(content_div)
            markdown_content = md(html_content, heading_style="ATX")
            markdown_content = re.sub(r'\n{3,}', '\n\n', markdown_content).strip()

            md_path = os.path.join(output_book_path, f"{chapter_id}.md")
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(markdown_content)

            print(f"✅ {book_dir}/{chapter_id}.md 已生成")

        except Exception as e:
            print(f"❌ 错误：{book_dir}/{chapter_id} 解析失败 -> {e}")
