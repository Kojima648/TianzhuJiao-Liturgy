# 脚本名称：generate_books_list.py
# 功能描述：根据 parsed_json 目录生成总导航文件 books_list.json，供前端显示书籍列表使用

import os
import json

# 当前脚本路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# 源书籍数据目录
PARSED_JSON_DIR = os.path.join(SCRIPT_DIR, "..", "..", "parsed_json")

# 输出 books_list.json 文件路径
OUTPUT_PATH = os.path.join(SCRIPT_DIR, "..", "..", "books_list.json")

# 每本书的索引文件访问路径（供前端加载章节）
INDEX_BASE_URL = "/static/index"  # 你也可以用完整 CDN 地址替换

book_list = []

for filename in os.listdir(PARSED_JSON_DIR):
    if not filename.startswith("book_") or not filename.endswith(".json"):
        continue

    book_id = filename.replace(".json", "")
    json_path = os.path.join(PARSED_JSON_DIR, filename)

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    info = data.get("info", {})

    book_entry = {
        "book_id": book_id,
        "title": info.get("title", ""),
        "summary": info.get("summary", ""),
        "update": info.get("update", ""),
        "cover": info.get("cover", ""),
        "index_path": f"{INDEX_BASE_URL}/{book_id}_index.json"
    }

    book_list.append(book_entry)

# 保存最终书籍列表 JSON
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(book_list, f, ensure_ascii=False, indent=2)

print(f"✅ 总书籍导航已生成：{OUTPUT_PATH}")
