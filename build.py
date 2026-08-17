# -*- coding: utf-8 -*-
"""產生部落格 index.html 與 README.md（極簡 + 字型進度遮罩版）。

單一靜態 HTML：
- 全部漢字依倉頡碼順序平鋪成列表（26 個字母分節 + 補遺）
- 每字以草書字型呈現，下方以字母標註其倉頡碼
- 搜尋交給瀏覽器內建 Ctrl+F
- 唯一瓶頸（2.25 MB 字型檔）以全螢幕遮罩 + fetch 真實進度條呈現：
  - 拔掉 @font-face/preload，改用 fetch() 下載（可算 bytes 進度）
  - 下載完以 CSS Font Loading API（new FontFace + document.fonts.add）掛上
  - 全程僅此一段極簡 JS；無 JS 時由 <noscript> 隱藏遮罩、以襯線兜底
- content-visibility 跳過屏外渲染；行動版適配
"""
from fontTools.ttLib import TTFont
import html as _html
import json

FONT = "草书.ttf"
CHARS = "covered_chars.txt"
INTRO = "mikhailcai_cursivecinese.txt"
COV = "coverage_stats.json"

def esc(s):
    return _html.escape(s, quote=True)

# 倉頡字母 → 字根漢字（24 字母 + 難 x、重 z）
CJ = {
    'a': '日', 'b': '月', 'c': '金', 'd': '木', 'e': '水', 'f': '火', 'g': '土',
    'h': '竹', 'i': '戈', 'j': '十', 'k': '大', 'l': '中', 'm': '一', 'n': '弓',
    'o': '人', 'p': '心', 'q': '手', 'r': '口', 's': '尸', 't': '廿', 'u': '山',
    'v': '女', 'w': '田', 'x': '難', 'y': '卜', 'z': '重',
}

def cj_display(code):
    return ''.join(CJ.get(c, c) for c in code)

# ---- 讀取已覆蓋字 + 碼（covered_chars.txt 已按碼排序）----
items = []
for line in open(CHARS, encoding="utf-8"):
    line = line.rstrip("\n")
    if not line:
        continue
    p = line.split("\t")
    if len(p) >= 2:
        items.append((p[0], p[1]))

# ---- 字型有漢字但碼錶無碼（補遺） ----
font = TTFont(FONT)
cmap = font.getBestCmap()
def is_cjk(cp):
    return (0x4E00 <= cp <= 0x9FFF or 0x3400 <= cp <= 0x4DBF
            or 0x20000 <= cp <= 0x2EBEF or 0xF900 <= cp <= 0xFAFF)
have = {ch for ch, _ in items}
extras = sorted(chr(cp) for cp in cmap if is_cjk(cp) and chr(cp) not in have)

total_hanzi = len(items) + len(extras)

# ---- 臺港覆蓋率（僅供 README） ----
cov = json.load(open(COV, encoding="utf-8"))
def pct(x):
    return f"{x['rate']*100:.2f}%"
tw_c = cov["tw_common"]; tw_l = cov["tw_less_common"]; hk = cov["hk_common"]

# ---- 依首字母分組 ----
groups = []  # [(首字母, [(字, 碼), ...])]
cur = None
for ch, code in items:
    L = code[0]
    if L != cur:
        groups.append([L, []])
        cur = L
    groups[-1][1].append((ch, code))

def cell_html(ch, code):
    if code:
        return (f'<div class="cell"><span class="h">{esc(ch)}</span>'
                f'<span class="c">{esc(code)}</span></div>')
    return f'<div class="cell"><span class="h">{esc(ch)}</span></div>'

sections_html = []
for L, cells in groups:
    body = "".join(cell_html(ch, code) for ch, code in cells)
    sections_html.append(
        f'<section id="{esc(L)}"><h2><span class="l">{esc(L)} · {len(cells)}</span></h2>'
        f'<div class="grid">{body}</div></section>')

extras_body = "".join(cell_html(ch, None) for ch in extras)
extras_html = (f'<section id="extras"><h2><span class="l">Extras · in font, no code · {len(extras)}</span></h2>'
               f'<div class="grid">{extras_body}</div></section>')

sections_all = "\n".join(sections_html) + "\n" + extras_html

# ---- CSS（極簡；遮罩；content-visibility；行動版） ----
css = """
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:#fbf9f3;color:#221b12;
  font-family:"Songti TC","Noto Serif CJK TC","PMingLiU",Georgia,"Times New Roman",serif;
  line-height:1.5}
header{text-align:center;padding:44px 16px 6px}
h1{margin:0;font-size:34px;letter-spacing:.22em;font-weight:500}
.sub{margin:10px auto 0;max-width:700px;font-size:14px;color:#837763;padding:0 8px}
.readme{margin:16px auto 0}
.readme a{color:#b23a2e;font-size:14px;text-decoration:none;border-bottom:1px solid #e7c9c4}
.readme a:hover{border-color:#b23a2e}
main{max-width:1240px;margin:0 auto;padding:0 14px 70px}
section{content-visibility:auto;contain-intrinsic-size:auto 600px}
h2{margin:16px 0 8px;padding:7px 12px;font-size:17px;font-weight:500;
  background:#fbf9f3;border-bottom:1px solid #e7dfcd;letter-spacing:.05em}
h2 .l{color:#9a8f7a;font-weight:500;font-size:14px;letter-spacing:.06em}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(64px,1fr));gap:8px}
.cell{background:#fff;border:1px solid #ece5d3;border-radius:6px;
  padding:7px 2px 5px;text-align:center}
.cell .h{display:block;font-family:"caoshu",serif;font-size:40px;line-height:1.2;color:#221b12}
.cell .c{display:block;font-size:11px;color:#9a8f7a;
  font-family:"Songti TC","PMingLiU",serif;letter-spacing:.02em;margin-top:2px}
#top{position:fixed;right:16px;bottom:16px;z-index:100;background:#221b12;color:#fbf9f3;
  text-decoration:none;padding:9px 13px;border-radius:999px;font-size:13px}
#top:hover{background:#b23a2e}
/* font download mask */
#mask{position:fixed;inset:0;z-index:999;background:#fbf9f3;display:flex;flex-direction:column;
  align-items:center;justify-content:center;gap:18px;transition:opacity .3s}
#mask .brand{font-size:60px;color:#b23a2e;font-family:"Songti TC","PMingLiU",serif}
#mask .bar{width:200px;height:2px;background:#e7dfcd;overflow:hidden}
#mask #fill{display:block;height:100%;width:0;background:#b23a2e;transition:width .1s linear}
#mask #fill.indet{width:40%;animation:indet 1.2s linear infinite}
#mask #pct{font-size:13px;color:#837763;min-width:48px;text-align:center}
@keyframes indet{0%{margin-left:-40%}100%{margin-left:100%}}
@media (max-width:640px){
  header{padding:30px 12px 4px}
  h1{font-size:26px;letter-spacing:.16em}
  .sub{font-size:13px}
  main{padding:0 8px 60px}
  h2{font-size:15px;padding:6px 10px;margin:12px 0 6px}
  .grid{grid-template-columns:repeat(auto-fill,minmax(50px,1fr));gap:6px}
  .cell{padding:5px 1px 4px;border-radius:5px}
  .cell .h{font-size:29px}
  .cell .c{font-size:10px}
  #top{right:12px;bottom:12px;padding:8px 11px;font-size:12px}
}
"""

# ---- JS（唯一一段：fetch 字型 + 真實進度 + FontFace 掛載） ----
js = """
(function(){
  var m=document.getElementById('mask'),f=document.getElementById('fill'),p=document.getElementById('pct'),done=false;
  function hide(){if(done)return;done=true;m.style.opacity='0';setTimeout(function(){m.remove();},300);}
  function fallback(){
    var s=document.createElement('style');
    s.textContent='@font-face{font-family:"caoshu";src:url("caoshu.woff2") format("woff2");font-display:swap}';
    document.head.appendChild(s);
    f.classList.add('indet');p.textContent='Loading…';
    var pr=(document.fonts&&document.fonts.load)?document.fonts.load('40px "caoshu"','草'):Promise.resolve();
    pr.then(hide,hide);
  }
  fetch('caoshu.woff2').then(function(r){
    if(!r.ok) throw new Error(r.status);
    var t=+r.headers.get('Content-Length')||0,n=0,c=[],rd=r.body.getReader();
    if(!t){f.classList.add('indet');p.textContent='Loading…';}
    function go(){return rd.read().then(function(x){
      if(x.done){
        return new Blob(c).arrayBuffer().then(function(ab){
          var font=new FontFace('caoshu',ab);
          document.fonts.add(font);
          return font.load().then(hide);
        });
      }
      c.push(x.value);n+=x.value.length;
      if(t){var q=Math.round(n/t*100);f.style.width=q+'%';p.textContent=q+'%';}
      return go();
    });}
    return go();
  }).catch(fallback);
})();
"""

# ---- HTML ----
html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>tsao — Cursive Font · All Hanzi</title>
<meta name="description" content="All {total_hanzi} hanzi in the cursive font (Sun Guoting style), in Cangjie code order.">
<style>{css}</style>
</head>
<body>
<div id="mask"><div class="brand">tsao</div><div class="bar"><i id="fill"></i></div><div id="pct">0%</div></div>
<noscript><style>#mask{{display:none}}</style></noscript>
<header>
  <h1>tsao</h1>
  <p class="sub">All {total_hanzi} hanzi in cursive · sorted by Cangjie code · search with Ctrl+F</p>
  <p class="readme"><a href="https://github.com/sujmao/tsao" target="_blank" rel="noopener">Read the README →</a></p>
</header>
<main>
{sections_all}
</main>
<a id="top" href="#">↑ Top</a>
<script>{js}</script>
</body>
</html>
"""

open("index.html", "w", encoding="utf-8").write(html)

# ---- README ----
intro_txt = open(INTRO, encoding="utf-8").read().strip()

readme = f"""# tsao — 草書字型全漢字部落格

以「草書」字型依**倉頡碼的字母順序**，把字型收錄的全部漢字平鋪於一頁的極簡靜態部落格。釋出於 GitHub Pages。

## 這是什麼

- 字型：**草書**（草书.ttf），由字體吧（百度貼吧）網友 **mikhailcai** 製作，模仿**孫過庭**狂草書風，約 17,000 餘字，作者已**放棄版權**、可免費商用。
- 碼錶：**倉頡五代單字碼表**（cangjie5.dict.yaml，GPL），作為排序依據。
- 展示方式：單一靜態 HTML。全部漢字依倉頡碼字母順序平鋪成列表（每字以草書呈現，下方以字母標註其倉頡碼）；無自訂搜尋，直接使用瀏覽器內建 Ctrl+F。
- 載入體驗：頁面開啟即顯示**全螢幕遮罩 + 真實下載進度**——用 `fetch()` 下載字型（約 2.25 MB）並計算進度，完成後以 CSS Font Loading API 掛上草書字型、淡出遮罩。全程僅一段極簡 JS；無 JS 時以系統襯線兜底。`content-visibility` 跳過屏外渲染、支援行動版。

## 覆蓋率

| 項目 | 數量 |
|------|------|
| 字型收錄漢字（含擴展/相容） | **{total_hanzi}** |
| 其中可對應碼錶單字 | {len(items)} |
| 字型有、碼錶無碼（補遺） | {len(extras)} |
| 碼錶單字總數 | 75,208 |
| 覆蓋率 | **22.84%** |

### 常用字表覆蓋率

| 常用字表 | 覆蓋 | 比例 |
|----------|------|------|
| 臺灣常用字（甲表 4808） | {tw_c['covered']} / {tw_c['total']} | **{pct(tw_c)}** |
| 臺灣次常用字（乙表 6334） | {tw_l['covered']} / {tw_l['total']} | **{pct(tw_l)}** |
| 香港常用字字形表（4762 條，含異體 4825 字） | {hk['covered']} / {hk['total']} | **{pct(hk)}** |

未覆蓋字已輸出至 `missing_tw_common.txt`、`missing_tw_less_common.txt`、`missing_hk_common.txt`。

## 線上預覽

開啟 `index.html` 即可，或透過 GitHub Pages 檢視：

```
https://sujmao.github.io/tsao/
```

## 檔案

- `index.html` —— 部落格本體（內嵌樣式與字型）
- `caoshu.woff2` —— 由草书.ttf 轉出的網頁字型
- `草书.ttf` —— 原始字型
- `cangjie5.dict.yaml` —— 倉頡五代碼錶（排序依據）
- `variant-WordCharacter.json` / `hk_common_raw.txt` —— 臺港常用字表原始資料
- `coverage.py` / `build.py` / `analyze.py` —— 分析與產生腳本

## 字型來源

{intro_txt}
"""

open("README.md", "w", encoding="utf-8").write(readme)

print(f"done. total_hanzi={total_hanzi}, coded={len(items)}, extras={len(extras)}")
print(f"TW common {pct(tw_c)}, TW less {pct(tw_l)}, HK {pct(hk)}")
