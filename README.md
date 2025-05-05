# TianzhuJiao-Liturgy (天主教礼仪资源)

本仓库旨在集中管理和开源以下内容：

- **思高圣经**（Sigao Bible）HTML 文档与索引
- **教会节日与瞻礼单**（节日配置、文章与预览）
- **常用书籍**（书籍目录与脚本工具）
- **圣人传记**与相关素材
- 目录结构脚本：`list_dir_structure.py`

---

## 📂 仓库目录结构
```plain
TianzhuJiao-Liturgy/            # 项目根目录
├── .git/                       # Git 版本控制信息
├── .gitattributes              # Git 属性配置
├── .gitignore                  # 忽略文件规则
├── .vscode/                    # VSCode 项目设置
├── Bible-Sigao/                # 自动生成的“思高圣经”HTML 与索引
│   ├── catalog.json
│   ├── chapter_count_report.txt
│   ├── index.json
│   ├── index.md
│   ├── 新约/
│   └── 旧约/
├── 其他配置表/                 # 节日与瞻礼相关配置
│   ├── festival_articles.json
│   ├── festival_config.json
│   ├── preview.html
│   └── 完整节日配置_2025.json
├── 常用书籍/                   # 各类书籍列表与脚本
│   ├── book_index.json
│   ├── books_list.json
│   ├── goclone.exe
│   └── scripts/
├── 教会节日和圣人传记/         # 节日与圣人传记素材
│   ├── MonthlyJSON/
│   └── 整理后的图片/
├── LICENSE                     # Apache-2.0 许可证
├── README.md                   # 项目说明文档（当前文件）
├── dir_structure.json          # 最近一次目录结构快照
└── list_dir_structure.py       # 生成目录结构的工具脚本
```

---

## 🚀 快速开始

1. **克隆仓库**：
   ```bash
   git clone https://github.com/<你的用户名>/TianzhuJiao-Liturgy.git
   cd TianzhuJiao-Liturgy
   ```

2. **生成目录结构**（可选）：
   ```bash
   python list_dir_structure.py  # 或指定其他目录路径
   ```
   运行后将在根目录生成 `dir_structure.json`，并在终端打印最多三层的树状结构。

3. **查看“思高圣经”资源**：
   - 打开 `Bible-Sigao/index.md` 阅读全书索引；
   - 打开 `Bible-Sigao/新约/` 和 `Bible-Sigao/旧约/` 浏览 HTML 文档。

4. **使用其他配置表**：
   - `其他配置表/` 包含教会节日相关文章与配置文件；
   - `常用书籍/` 提供书籍列表 (`book_index.json`, `books_list.json`) 及脚本工具；
   - `教会节日和圣人传记/` 存放节日与圣人素材。

---

## 🤝 贡献与扩展

- 欢迎 Issue 报告 bug、提出功能建议；
- Fork 本仓库后提交 Pull Request，即可贡献新资源或脚本；
- 未来计划新增：圣人传记详细文档、教会祷文、音视频资源等。

---

## 📄 许可证

本项目基于 [Apache-2.0 许可证](LICENSE) 开源，欢迎自由使用与分享。
