# 脚本名称：generate_per_book_index.py
# 功能描述：为每一本书（book_xx.json）生成独立的章节索引 JSON：book_xx_index.json

import os
import json

# 当前脚本路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# 源数据目录
PARSED_JSON_DIR = os.path.join(SCRIPT_DIR, "..", "..", "parsed_json")

# 输出目录
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "..", "book_indexes")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Markdown 文件基路径（前端用）
BASE_MD_PATH = "/static/markdown"

for filename in os.listdir(PARSED_JSON_DIR):
    if not filename.startswith("book_") or not filename.endswith(".json"):
        continue

    book_id = filename.replace(".json", "")
    json_path = os.path.join(PARSED_JSON_DIR, filename)

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    book_info = data.get("info", {})
    sections = data.get("sections", [])

    output_data = {
        "book_id": book_id,
        "title": book_info.get("title", ""),
        "update": book_info.get("update", ""),
        "summary": book_info.get("summary", ""),
        "cover": book_info.get("cover", ""),
        "sections": []
    }

    for section in sections:
        url = section.get("url", "")
        chapter_id = url.strip("/").split("/")[-1]
        output_data["sections"].append({
            "title": section.get("title", ""),
            "category": section.get("category", ""),
            "path": f"{BASE_MD_PATH}/{book_id}/{chapter_id}.md"
        })

    # 写入独立 JSON 文件
    output_path = os.path.join(OUTPUT_DIR, f"{book_id}_index.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"✅ 已生成索引：{output_path}")
