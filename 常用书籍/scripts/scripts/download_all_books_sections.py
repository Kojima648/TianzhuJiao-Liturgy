# 脚本名称：download_all_books_sections.py
# 功能描述：自动处理 parsed_json 目录下所有书籍 JSON，下载所有章节页面到 downloaded_pages/book_xx/章节/index.html

import os
import json
import requests

# 当前脚本路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# JSON 配置目录
JSON_DIR = os.path.join(SCRIPT_DIR, "..", "..", "parsed_json")

# 下载输出根目录
OUTPUT_ROOT = os.path.join(SCRIPT_DIR, "..", "..", "downloaded_pages")
os.makedirs(OUTPUT_ROOT, exist_ok=True)

# 网站根地址
BASE_URL = "https://www.zhouzhidiocese.com"

# 遍历所有 parsed_json/book_xx.json
for json_file in os.listdir(JSON_DIR):
    if not json_file.startswith("book_") or not json_file.endswith(".json"):
        continue

    book_code = json_file.replace(".json", "")
    json_path = os.path.join(JSON_DIR, json_file)

    # 输出目录
    output_dir = os.path.join(OUTPUT_ROOT, book_code)
    os.makedirs(output_dir, exist_ok=True)

    print(f"\n📘 正在处理：{book_code}")

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for section in data.get("sections", []):
        url_path = section.get("url")
        title = section.get("title", "").strip()
        if not url_path:
            continue

        full_url = BASE_URL + url_path
        page_id = url_path.strip("/").split("/")[-1]

        save_dir = os.path.join(output_dir, page_id)
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, "index.html")

        if os.path.exists(save_path):
            print(f"✅ 已存在，跳过：{book_code}/{page_id}")
            continue

        try:
            print(f"📥 下载：{full_url}")
            response = requests.get(full_url, timeout=10)
            response.raise_for_status()

            with open(save_path, "w", encoding="utf-8") as f:
                f.write(response.text)

            print(f"✅ 成功保存：{book_code}/{page_id}")

        except Exception as e:
            print(f"❌ 下载失败：{full_url} -> {e}")
