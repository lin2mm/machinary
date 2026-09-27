#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TRUTH 发布前验证门（见 00-system/02 §6）。任一失败 → 退出码 1。"""
import csv, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
fail = []

def rel(p): return os.path.relpath(p, ROOT)

# 收集 md
mds = []
for base in ['00-system', '10-industry-used-machinery', '20-project-rotary-rig-sea']:
    for r, _, fs in os.walk(os.path.join(ROOT, base)):
        for f in fs:
            if f.endswith('.md'): mds.append(os.path.join(r, f))
readme = os.path.join(ROOT, 'README.md')

# 1) 顶层目录前缀
tops = {d for d in os.listdir(ROOT) if os.path.isdir(os.path.join(ROOT, d)) and not d.startswith('.')}
bad = [d for d in tops if not re.match(r'^(00|10|20|90)-', d)]
if bad: fail.append(f"顶层目录不符合 00/10/20/90 前缀: {bad}")
print(f"[1] 顶层目录: {sorted(tops)}")

# 2) frontmatter 字段
REQ = ['状态', '置信度', '最后核验', '下次复核']
for p in mds:
    t = open(p, encoding='utf-8').read()
    if not t.startswith('---'): fail.append(f"缺 frontmatter: {rel(p)}"); continue
    head = t.split('---', 2)[1]
    for k in REQ:
        if k + ':' not in head and k + ': ' not in head: fail.append(f"{rel(p)} frontmatter 缺 {k}")
print(f"[2] md 数量: {len(mds)}")

# 3) 引用 ID 存在于登记册
reg_ids = set()
with open(os.path.join(ROOT, '00-system/data/source-register.csv'), encoding='utf-8-sig') as f:
    for row in csv.DictReader(f): reg_ids.add(row['ID'])
alltext = {rel(p): open(p, encoding='utf-8').read() for p in mds}
alltext['README.md'] = open(readme, encoding='utf-8').read()
for name, t in alltext.items():
    for m in re.finditer(r'\[([A-F])(\d+)\]', t):
        if m.group(0) not in [f'[{i}]' for i in reg_ids] and (m.group(1)+m.group(2)) not in reg_ids:
            fail.append(f"{name} 引用了不存在的 ID {m.group(0)}")
print(f"[3] 登记册 ID 数: {len(reg_ids)}")

# 4) 相对链接可解析
for name, t in alltext.items():
    base = os.path.dirname(os.path.join(ROOT, name)) if name != 'README.md' else ROOT
    for l in re.findall(r'\]\(([^)#]+\.md)\)', t):
        if not os.path.isfile(os.path.join(base, l)): fail.append(f"{name} 链接失效: {l}")

# 5) CSV 列宽
for r, _, fs in os.walk(ROOT):
    for f in fs:
        if f.endswith('.csv'):
            p = os.path.join(r, f)
            with open(p, encoding='utf-8-sig') as fh: rows = list(csv.reader(fh))
            if len({len(x) for x in rows}) != 1: fail.append(f"CSV 列宽不一致: {rel(p)}")

# 6) [推算] 附近有算式
for name, t in alltext.items():
    lines = t.split('\n')
    for i, ln in enumerate(lines):
        if '[推算]' in ln:
            window = ''.join(lines[max(0, i-1):i+3])
            if not re.search(r'[=−\-×x/÷%≈]', window): fail.append(f"{name} [推算] 无算式 (行{i+1})")

# 7) 表格竖线一致
for name, t in alltext.items():
    block = []
    def chk(b):
        if len(b) < 2: return
        c = {ln.count('|') for _, ln in b}
        if len(c) != 1: fail.append(f"{name} 表格竖线不一致")
    for i, ln in enumerate(t.split('\n'), 1):
        if ln.strip().startswith('|'): block.append((i, ln))
        else: chk(block); block = []
    chk(block)

# 8) 文件/目录名必须纯 ASCII（workspace 查看器对中文名显示 Unknown file）
nonascii = []
for r, ds, fs in os.walk(ROOT):
    if '.git' in r.split(os.sep): continue
    for n in ds + fs:
        if any(ord(c) > 127 for c in n): nonascii.append(rel(os.path.join(r, n)))
if nonascii: fail.append(f"非 ASCII 文件/目录名: {nonascii}")
print(f"[8] 非 ASCII 名称: {len(nonascii)}")

print("\n结果:", "全部通过" if not fail else "FAIL")
for x in fail: print("  -", x)
sys.exit(1 if fail else 0)
