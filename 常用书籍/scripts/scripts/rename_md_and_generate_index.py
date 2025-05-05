# 脚本名称：rename_md_and_generate_index.py
# 功能描述：为每本书的 Markdown 文件重新编号 + 命名，并生成新的章节导航 JSON

import os
import re
import json
import shutil

# 脚本路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# JSON 配置目录
PARSED_JSON_DIR = os.path.join(SCRIPT_DIR, "..", "..", "parsed_json")

# 原始 Markdown 文件目录
MD_INPUT_ROOT = os.path.join(SCRIPT_DIR, "..", "..", "parsed_md")

# 输出 Markdown 文件目录（新的命名）
MD_OUTPUT_ROOT = os.path.join(SCRIPT_DIR, "..", "..", "renamed_md")
os.makedirs(MD_OUTPUT_ROOT, exist_ok=True)

# 导航索引输出目录
INDEX_OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "..", "book_indexes_renamed")
os.makedirs(INDEX_OUTPUT_DIR, exist_ok=True)

# 前端可访问的 base path
BASE_MD_URL = "/static/markdown_renamed"

# 合法化文件名
def sanitize_filename(name):
    name = re.sub(r'[\\/*?:"<>|]', '', name)  # 去除非法字符
    name = re.sub(r'\s+', '_', name.strip())  # 替换空格为 _
    return name[:30]  # 最长保留30字符

# 遍历所有书籍 JSON
for filename in os.listdir(PARSED_JSON_DIR):
    if not filename.startswith("book_") or not filename.endswith(".json"):
        continue

    book_id = filename.replace(".json", "")
    json_path = os.path.join(PARSED_JSON_DIR, filename)
    md_input_dir = os.path.join(MD_INPUT_ROOT, book_id)
    md_output_dir = os.path.join(MD_OUTPUT_ROOT, book_id)
    os.makedirs(md_output_dir, exist_ok=True)

    print(f"\n📘 处理书籍：{book_id}")

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    book_info = data.get("info", {})
    sections = data.get("sections", [])

    index_json = {
        "book_id": book_id,
        "title": book_info.get("title", ""),
        "update": book_info.get("update", ""),
        "summary": book_info.get("summary", ""),
        "cover": book_info.get("cover", ""),
        "sections": []
    }

    for idx, section in enumerate(sections):
        title = section.get("title", "").strip()
        category = section.get("category", "")
        old_url = section.get("url", "")
        old_id = old_url.strip("/").split("/")[-1]
        old_md_path = os.path.join(md_input_dir, f"{old_id}.md")

        if not os.path.exists(old_md_path):
            print(f"⚠️ 缺失 Markdown：{old_md_path}，跳过")
            continue

        new_filename = f"{idx+1:03d}_{sanitize_filename(title)}.md"
        new_md_path = os.path.join(md_output_dir, new_filename)

        # 拷贝并重命名文件
        shutil.copyfile(old_md_path, new_md_path)

        index_json["sections"].append({
            "title": title,
            "category": category,
            "path": f"{BASE_MD_URL}/{book_id}/{new_filename}"
        })

        print(f"✅ {old_id}.md → {new_filename}")

    # 写入新的导航 JSON
    index_path = os.path.join(INDEX_OUTPUT_DIR, f"{book_id}_index.json")
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index_json, f, ensure_ascii=False, indent=2)

    print(f"📄 导航索引已生成：{index_path}")
