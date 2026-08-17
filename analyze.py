# -*- coding: utf-8 -*-
"""分析碼錶與字型覆蓋率。結果寫入 UTF-8 檔案，避免 console 編碼問題。"""
from fontTools.ttLib import TTFont

DICT = "cangjie5.dict.yaml"
FONT = "草书.ttf"
OUT = "report.txt"

lines = []
lines = open(DICT, encoding="utf-8").read().splitlines()
data_start = 0
for i, l in enumerate(lines):
    if l.strip() == "...":
        data_start = i + 1
        break

entries = []
for l in lines[data_start:]:
    if not l.strip():
        continue
    parts = l.split("\t")
    if len(parts) < 2:
        continue
    entries.append((parts[0], parts[1]))

single = [(t, c) for t, c in entries if len(t) == 1]
uniq = {}
for t, c in single:
    if t not in uniq:
        uniq[t] = c

font = TTFont(FONT)
cmap = font.getBestCmap()

def is_cjk(cp):
    return (
        0x4E00 <= cp <= 0x9FFF      # CJK Unified Ideographs
        or 0x3400 <= cp <= 0x4DBF   # Ext A
        or 0x20000 <= cp <= 0x2EBEF # Ext B-F
        or 0xF900 <= cp <= 0xFAFF   # Compatibility Ideographs
    )

font_hanzi = [cp for cp in cmap if is_cjk(cp)]
font_nonhanzi = [cp for cp in cmap if not is_cjk(cp)]

covered = [ch for ch in uniq if ord(ch) in cmap and is_cjk(ord(ch))]
missing = [ch for ch in uniq if ord(ch) not in cmap]
# 字型裡的漢字但不在碼錶
in_font_not_dict = [chr(cp) for cp in font_hanzi if chr(cp) not in uniq]

ordered = sorted(covered, key=lambda ch: uniq[ch])

r = []
r.append("== 碼錶 (cangjie5.dict.yaml) ==")
r.append(f"資料列總數: {len(entries)}")
r.append(f"單字列數: {len(single)}")
r.append(f"去重後單字數: {len(uniq)}")
r.append("")
r.append("== 字型 (草书.ttf) ==")
r.append(f"cmap 總碼點: {len(cmap)}")
r.append(f"其中漢字(含擴展/相容): {len(font_hanzi)}")
r.append(f"其中非漢字(標點/符號/西文等): {len(font_nonhanzi)}")
r.append("")
r.append("== 覆蓋率 ==")
r.append(f"碼錶單字中被字型覆蓋(漢字): {len(covered)}")
r.append(f"碼錶單字中未被覆蓋: {len(missing)}")
r.append(f"覆蓋率(覆蓋/碼錶單字): {len(covered)/len(uniq)*100:.2f}%")
r.append(f"字型漢字但不在碼錶: {len(in_font_not_dict)}")
r.append("")
r.append("未覆蓋樣本(前60): " + "".join(missing[:60]))
r.append("字型有但碼錶無(前60): " + "".join(in_font_not_dict[:60]))
r.append("")
r.append("排序後首20字: " + "".join(ordered[:20]))
r.append("排序後末20字: " + "".join(ordered[-20:]))

open(OUT, "w", encoding="utf-8").write("\n".join(r))

# 寫出最終要渲染的字 + 碼
with open("covered_chars.txt", "w", encoding="utf-8") as f:
    for ch in ordered:
        f.write(f"{ch}\t{uniq[ch]}\n")

print(f"report written to {OUT}")
print(f"covered chars: {len(ordered)}")
