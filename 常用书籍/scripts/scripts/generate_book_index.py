# 脚本名称：generate_book_index.py
# 功能描述：汇总所有 parsed_json/book_xx.json，生成书籍导航索引 JSON，输出为 book_index.json

import os
import json

# 当前脚本路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# JSON 来源目录
PARSED_JSON_DIR = os.path.join(SCRIPT_DIR, "..", "..", "parsed_json")

# 输出文件路径
OUTPUT_PATH = os.path.join(SCRIPT_DIR, "..", "..", "book_index.json")

# Markdown 基础访问路径（给前端用）
BASE_MD_URL = "/static/markdown"  # 你可以根据实际情况改为完整路径或 CDN 地址

book_list = []

for filename in os.listdir(PARSED_JSON_DIR):
    if not filename.startswith("book_") or not filename.endswith(".json"):
        continue

    book_id = filename.replace(".json", "")
    json_path = os.path.join(PARSED_JSON_DIR, filename)

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    book_info = data.get("info", {})
    sections = data.get("sections", [])

    entry = {
        "book_id": book_id,
        "title": book_info.get("title", ""),
        "update": book_info.get("update", ""),
        "summary": book_info.get("summary", ""),
        "cover": book_info.get("cover", ""),
        "sections": []
    }

    for sec in sections:
        chapter_id = sec.get("url", "").strip("/").split("/")[-1]
        entry["sections"].append({
            "title": sec.get("title", ""),
            "category": sec.get("category", ""),
            "path": f"{BASE_MD_URL}/{book_id}/{chapter_id}.md"
        })

    book_list.append(entry)

# 写入输出文件
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(book_list, f, ensure_ascii=False, indent=2)

print(f"✅ 导航索引已生成：{OUTPUT_PATH}")
