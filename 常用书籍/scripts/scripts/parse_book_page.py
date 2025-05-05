# 脚本名称：parse_all_books.py
# 功能描述：批量解析 goclone 下载的书籍 HTML 页面，将结构化 JSON 导出到 parsed_json 目录

import os
import json
from bs4 import BeautifulSoup

# 当前脚本目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# 所有 book_x 文件夹路径
BOOKS_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", "books"))

# 输出 JSON 的统一目录
OUTPUT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", "parsed_json"))
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 扫描所有 book_xx 目录
for folder_name in os.listdir(BOOKS_DIR):
    folder_path = os.path.join(BOOKS_DIR, folder_name)
    if not os.path.isdir(folder_path) or not folder_name.startswith("book_"):
        continue

    html_path = os.path.join(folder_path, "www.zhouzhidiocese.com", "index.html")
    if not os.path.exists(html_path):
        print(f"⚠️ 跳过：未找到 {html_path}")
        continue

    print(f"📖 解析中：{folder_name}")

    with open(html_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    result = {}

    # info 部分
    info_block = soup.select_one(".left-content .info.flex-col")
    if info_block:
        title = info_block.select_one(".title")
        update_date = info_block.select_one(".intro-text")
        summary = info_block.select_one(".summary")
        cover_img = info_block.select_one("img.cover")

        result["info"] = {
            "title": title.get_text(strip=True) if title else "",
            "update": update_date.get_text(strip=True) if update_date else "",
            "summary": summary.get_text(strip=True) if summary else "",
            "cover": cover_img["src"] if cover_img and cover_img.has_attr("src") else ""
        }

    # sections 部分
    book_sections = []
    current_category = ""
    for div in soup.select(".left-content .book.layui-row > div"):
        if "item-cate" in div.get("class", []):
            current_category = div.get_text(strip=True)
        elif "item-link" in div.get("class", []):
            a_tag = div.find("a")
            if a_tag and a_tag.has_attr("href"):
                book_sections.append({
                    "category": current_category,
                    "title": a_tag.get_text(strip=True),
                    "url": a_tag["href"]
                })

    result["sections"] = book_sections

    # 保存到 parsed_json/book_xx.json
    json_path = os.path.join(OUTPUT_DIR, f"{folder_name}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"✅ 保存：{json_path}")

print("🎉 所有解析完成")
