# 脚本名称：generate_books_list_for_renamed.py
# 功能描述：根据重命名后的章节索引文件，生成首页导航用的 books_list.json

import os
import json

# 当前脚本目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# 输入目录（已重命名的每本书索引）
RENAMED_INDEX_DIR = os.path.join(SCRIPT_DIR, "..", "..", "book_indexes_renamed")

# 输出文件路径
OUTPUT_PATH = os.path.join(SCRIPT_DIR, "..", "..", "books_list.json")

# 每本书 index.json 在前端的访问路径（小程序侧）
INDEX_BASE_URL = "/static/index"

books = []

for filename in os.listdir(RENAMED_INDEX_DIR):
    if not filename.startswith("book_") or not filename.endswith("_index.json"):
        continue

    path = os.path.join(RENAMED_INDEX_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    book_id = data.get("book_id")
    books.append({
        "book_id": book_id,
        "title": data.get("title", ""),
        "summary": data.get("summary", ""),
        "update": data.get("update", ""),
        "cover": data.get("cover", ""),
        "index_path": f"{INDEX_BASE_URL}/{filename}"
    })

# 写入首页导航列表
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(books, f, ensure_ascii=False, indent=2)

print(f"✅ 首页导航 books_list.json 已生成：{OUTPUT_PATH}")
