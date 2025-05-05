#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
列出指定目录的三层树状结构并输出为 JSON。

用法:
    python list_dir_structure.py [目录路径]

如果不提供目录路径，则默认使用脚本所在目录（项目根目录）。
输出：
  - 在终端打印最多三层的树状结构
  - 在脚本所在目录下生成 `dir_structure.json` 保存结构
"""
import os
import sys
import json

# 最大深度（根目录为 0，最多到深度 2 即三层）
MAX_DEPTH = 2


def get_structure(path, depth=0):
    """
    递归获取目录结构，最多递归到 MAX_DEPTH。
    返回嵌套字典：{'name': ..., 'type': 'dir'/'file', 'children': [...]}
    """
    name = os.path.basename(path) or path
    if os.path.isdir(path):
        node = {'name': name, 'type': 'dir'}
        if depth < MAX_DEPTH:
            children = []
            try:
                for entry in sorted(os.listdir(path)):
                    full = os.path.join(path, entry)
                    children.append(get_structure(full, depth+1))
            except PermissionError:
                pass
            node['children'] = children
        else:
            node['children'] = []
        return node
    else:
        return {'name': name, 'type': 'file'}


def print_tree(node, prefix=''):
    """
    打印树状目录结构。
    """
    print(prefix + node['name'] + ('/' if node['type'] == 'dir' else ''))
    if node['type'] == 'dir' and node.get('children'):
        for i, child in enumerate(node['children']):
            is_last = (i == len(node['children']) - 1)
            branch = '└── ' if is_last else '├── '
            next_prefix = prefix + ('    ' if is_last else '│   ')
            print(prefix + branch, end='')
            print_tree(child, next_prefix)


def main():
    # 根目录：命令行参数或脚本所在目录
    root = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
    if not os.path.exists(root):
        print(f"❌ 路径不存在: {root}")
        sys.exit(1)

    tree = get_structure(root)
    print(f"目录树（最多三层，根目录：{root}）：")
    # 打印根节点
    print(tree['name'] + '/')
    for i, child in enumerate(tree.get('children', [])):
        is_last = (i == len(tree['children']) - 1)
        branch = '└── ' if is_last else '├── '
        next_prefix = '' if is_last else '│   '
        print(branch, end='')
        print_tree(child, next_prefix)

    # 保存 JSON
    outfile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dir_structure.json')
    with open(outfile, 'w', encoding='utf-8') as f:
        json.dump(tree, f, ensure_ascii=False, indent=2)
    print(f"目录结构已保存为 JSON: {outfile}")


if __name__ == '__main__':
    main()
