# 脚本名称：download_books.py
# 功能描述：使用 goclone.exe 直接下载电子书页面，每个页面保存到独立文件夹中（无额外参数）

import os
import subprocess

# 获取当前脚本所在目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# goclone.exe 位于 scripts/scripts 的上上一级
GOCLONE_PATH = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", "goclone.exe"))

# 检查 goclone.exe 是否存在
if not os.path.isfile(GOCLONE_PATH):
    raise FileNotFoundError(f"未找到 goclone.exe: {GOCLONE_PATH}")

# 下载输出目录（books 与 goclone.exe 同级）
OUTPUT_BASE = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", "books"))
os.makedirs(OUTPUT_BASE, exist_ok=True)

# 电子书页面 URL 列表
BOOK_URLS = [
    "https://www.zhouzhidiocese.com/book/16",
    "https://www.zhouzhidiocese.com/book/6",
    "https://www.zhouzhidiocese.com/book/8",
    "https://www.zhouzhidiocese.com/book/3",
    "https://www.zhouzhidiocese.com/book/4",
    "https://www.zhouzhidiocese.com/book/7"
]

# 逐个下载
for url in BOOK_URLS:
    book_id = url.rstrip("/").split("/")[-1]
    save_dir = os.path.join(OUTPUT_BASE, f"book_{book_id}")
    os.makedirs(save_dir, exist_ok=True)

    print(f"📥 正在下载: {url} 到 {save_dir}")

    try:
        # 在 save_dir 下执行 goclone "url"
        subprocess.run(
            [GOCLONE_PATH, url],
            cwd=save_dir,
            check=True
        )
        print(f"✅ 下载完成: {save_dir}")
    except subprocess.CalledProcessError as e:
        print(f"❌ 下载失败: {url}\n错误信息: {e}")
