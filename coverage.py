# -*- coding: utf-8 -*-
"""計算字型對臺灣甲/乙表與香港常用字字形表的覆蓋率，並輸出未覆蓋字。"""
import json
from fontTools.ttLib import TTFont

FONT = "草书.ttf"
TW_JSON = "variant-WordCharacter.json"
HK_RAW = "hk_common_raw.txt"

font = TTFont(FONT)
cmap = font.getBestCmap()

def has(ch):
    return ord(ch) in cmap

# ---- 臺灣 甲表(常用字 A) / 乙表(次常用字 B) ----
tw = json.load(open(TW_JSON, encoding="utf-8"))
tw_a = [ch for k, ch in tw.items() if k.startswith("A")]  # 常用字
tw_b = [ch for k, ch in tw.items() if k.startswith("B")]  # 次常用字

# ---- 香港 常用字字形表（含異體，同索引多字） ----
hk_chars = []
for line in open(HK_RAW, encoding="utf-8"):
    line = line.rstrip("\n")
    if "\t" not in line:
        continue
    ch = line.split("\t")[0]
    if ch:
        hk_chars.append(ch)
hk = list(dict.fromkeys(hk_chars))  # 去重保序

def uniq(chars):
    return list(dict.fromkeys(chars))

def cover(chars):
    chars = uniq(chars)
    cov = [ch for ch in chars if has(ch)]
    miss = [ch for ch in chars if not has(ch)]
    return len(cov), len(chars), cov, miss

tables = {
    "tw_common":      ("臺灣常用字(甲表)", tw_a),
    "tw_less_common": ("臺灣次常用字(乙表)", tw_b),
    "hk_common":      ("香港常用字字形表", hk),
}

res = {}
summary_lines = []
for name, (label, chars) in tables.items():
    cov, total, covlist, miss = cover(chars)
    res[name] = {"label": label, "total": total, "covered": cov,
                 "rate": cov / total if total else 0.0, "missing": len(miss)}
    print(f"{name} ({label}): {cov}/{total} = {cov/total*100:.2f}%  (缺 {len(miss)})")

    # 乾淨清單（一字一行）
    with open(f"list_{name}.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(chars) + "\n")
    # 未覆蓋字（一字一行）
    with open(f"missing_{name}.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(miss) + "\n")
    summary_lines.append(f"{label}：{cov}/{total} = {cov/total*100:.2f}%，未覆蓋 {len(miss)} 字：")
    summary_lines.append("".join(miss))
    summary_lines.append("")

json.dump(res, open("coverage_stats.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
open("coverage_missing.txt", "w", encoding="utf-8").write("\n".join(summary_lines))
print("saved: coverage_stats.json, list_*.txt, missing_*.txt, coverage_missing.txt")
