# tsao — 草書字型全漢字部落格

以「草書」字型依**倉頡碼的字母順序**，把字型收錄的全部漢字平鋪於一頁的極簡靜態部落格。釋出於 GitHub Pages。

## 這是什麼

- 字型：**草書**（草书.ttf），由字體吧（百度貼吧）網友 **mikhailcai** 製作，模仿**孫過庭**狂草書風，約 17,000 餘字，作者已**放棄版權**、可免費商用。
- 碼錶：**倉頡五代單字碼表**（cangjie5.dict.yaml，GPL），作為排序依據。
- 展示方式：單一靜態 HTML。全部漢字依倉頡碼字母順序平鋪成列表（每字以草書呈現，下方以字根漢字標註其倉頡碼）；無自訂搜尋，直接使用瀏覽器內建 Ctrl+F。
- 載入體驗：頁面開啟即顯示**全螢幕遮罩 + 真實下載進度**——用 `fetch()` 下載字型（約 2.25 MB）並計算進度，完成後以 CSS Font Loading API 掛上草書字型、淡出遮罩。全程僅一段極簡 JS；無 JS 時以系統襯線兜底。`content-visibility` 跳過屏外渲染、支援行動版。

## 覆蓋率

| 項目 | 數量 |
|------|------|
| 字型收錄漢字（含擴展/相容） | **17183** |
| 其中可對應碼錶單字 | 17175 |
| 字型有、碼錶無碼（補遺） | 8 |
| 碼錶單字總數 | 75,208 |
| 覆蓋率 | **22.84%** |

### 常用字表覆蓋率

| 常用字表 | 覆蓋 | 比例 |
|----------|------|------|
| 臺灣常用字（甲表 4808） | 4798 / 4808 | **99.79%** |
| 臺灣次常用字（乙表 6334） | 6114 / 6334 | **96.53%** |
| 香港常用字字形表（4762 條，含異體 4825 字） | 4802 / 4825 | **99.52%** |

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

**原版（繁體中文，僅支援繁體，需切換輸入法）相關 URL 整理**

### 證明資訊來源（作者 mikhailcai、模仿孫過庭、免費放棄版權）
- https://pptland.com/font/info/545  
  （最直接描述：「字體吧（百度貼吧）網友mikhailcai製作的一款模仿孫過庭的狂草字體…17000多個字…作者已放棄版權」並標註「草書.zip (4.50MB)」）

- https://www.maoken.com/freefonts/10811.html  
  （詳細說明原版繁體、作者 mikhailcai、孫過庭來源、免費商用聲明）

- https://font.jz52.com/freefont/994.html  
  （確認貼吧 mikhailcai 製作、免費無版權，附雲端下載）

- https://www.maoken.com/all-fonts  
  （列表中標註 mikhailcai 的「草书」，明確繁體支援 ★★★★★）

- https://www.100font.com/thread-427.htm  
  （簡述貼吧 mikhailcai 製作、免費無版權）

### 原版下載頁面（繁體版，非衍生版）
- https://pptland.com/font/info/545 （直接提供「草書.zip」下載）
- https://www.maoken.com/freefonts/10811.html （原版下載入口，作者 mikhailcai）
- https://font.jz52.com/freefont/994.html （附百度網盤 + 天翼雲盤下載，提取碼：c1id / 29lm）
- https://font.nuanque.com/fanti/1630.html （原版繁體草書下載）

這些連結均指向**原版繁體「草書」**（非简入繁出衍生版），檔案多為 4.5MB 左右的 .zip，安裝後字體名稱顯示為「草書」。
