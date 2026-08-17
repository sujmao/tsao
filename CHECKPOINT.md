# tsao — 草書字型全漢字部落格 · Checkpoint

> 建立時間：2026-08-17
> 工作空間：`D:\Downloads\tsao260817\ct`
> 狀態：**內容與頁面已完成；本次設計變更（v5：極簡平鋪列表＋字型進度遮罩）已實作，尚未上傳 GitHub Pages**（待使用者確認後釋出）

## 一、專案目標

以「草書」字型（模仿孫過庭書風）依**倉頡碼字母順序**，把字型收錄的全部漢字渲染並展示於一頁部落格，釋出到 GitHub Pages，題目「tsao」。

## 二、三個原始檔案

| 檔案 | 說明 |
|------|------|
| `草书.ttf`（7.6 MB） | 草書字型，作者 mikhailcai，免費放棄版權，約 17,000 餘字 |
| `cangjie5.dict.yaml`（868 KB） | 倉頡五代單字碼表（GPL），排序依據 |
| `mikhailcai_cursivecinese.txt` | 字型來源與介紹（供 README 使用） |

## 三、核心數據

### 字型覆蓋率（對碼錶）
- 字型 cmap 總碼點：18,065
- 其中漢字（含擴展／相容）：**17,183**
- 可對應碼錶單字：17,175；字型有、碼錶無碼（補遺）：8 字
- 碼錶單字總數：75,208
- 覆蓋率：**22.84%**

### 臺港常用字表覆蓋率
| 常用字表 | 覆蓋 | 比例 |
|----------|------|------|
| 臺灣常用字（甲表 4808） | 4798 / 4808 | 99.79% |
| 臺灣次常用字（乙表 6334） | 6114 / 6334 | 96.53% |
| 香港常用字字形表（4762 條） | 4802 / 4825 | 99.52% |

### 碼錶碼長
- 碼長分佈：1 碼 29、2 碼 426、3 碼 2273、4 碼 8884、5 碼 5563（**最多 5 碼**）
- 字母 a–y 都有出現；**x（難）出現 296 次**、z（重）未出現（標準倉頡仍含難、重）

## 四、已產生的檔案

### 網站（GitHub Pages 會用到）
| 檔案 | 說明 |
|------|------|
| `index.html`（約 1.5 MB） | 部落格本體，內嵌極簡 CSS／JS（約 0.9 KB），平鋪展示全部 17,183 漢字 |
| `caoshu.woff2`（2.36 MB） | 由 草书.ttf 轉出的網頁字型 |
| `README.md` | 專案說明（含來源、覆蓋率、使用方式） |

### 腳本
| 檔案 | 說明 |
|------|------|
| `analyze.py` | 解析碼錶＋字型覆蓋率 → `covered_chars.txt`、`report.txt` |
| `coverage.py` | 計算臺港覆蓋率 → `coverage_stats.json`、`list_*.txt`、`missing_*.txt` |
| `build.py` | 產生 `index.html` 與 `README.md`（主要產生器） |

### 資料／產出
| 檔案 | 說明 |
|------|------|
| `covered_chars.txt` | 17,175 個已覆蓋字＋倉頡碼（`字\t碼`，按碼排序） |
| `variant-WordCharacter.json` | 臺灣《國字標準字體表》甲乙丙表（A=甲/B=乙/C=丙） |
| `hk_common_raw.txt` | 香港《常用字字形表》（`字\t索引`） |
| `coverage_stats.json` | 臺港覆蓋率統計 |
| `list_tw_common.txt` / `list_tw_less_common.txt` / `list_hk_common.txt` | 乾淨字表 |
| `missing_tw_common.txt`（10 字）/ `missing_tw_less_common.txt`（220 字）/ `missing_hk_common.txt`（23 字） | 未覆蓋字 |
| `coverage_missing.txt` | 未覆蓋字摘要 |

### 備份（統一置於 `backup/` 子資料夾，`.gitignore` 排除）
| 檔案 | 說明 |
|------|------|
| `backup/index.v1.backup.html` | 第一版（單字母導覽、無亮暗色） |
| `backup/index.v2.backup.html` | 第二版（5 級下鑽篩選＋亮暗色＋臺港覆蓋率） |
| `backup/index.v3.backup.html` | 第三版（去鍵盤＋混合搜尋） |
| `backup/index.v4.backup.html` | 字根預覽去草書（混合搜尋小修正） |
| `backup/index.v5.backup.html` | v4 樹狀摺疊＋只找漢字（v5 前狀態） |
| `backup/build.v1.backup.py` | 原始（含虛擬鍵盤） |
| `backup/build.v2.backup.py` | 去鍵盤、未修字根預覽字型 |
| `backup/build.v3.backup.py` | 修字根預覽字型、混合搜尋 |
| `backup/build.v4.backup.py` | v4 樹狀摺疊＋只找漢字（v5 前狀態） |
| `backup/CHECKPOINT.v1.backup.md` | 含虛擬鍵盤舊設計 |
| `backup/CHECKPOINT.v2.backup.md` | v4 前備份（含混合搜尋舊設計） |
| `backup/CHECKPOINT.v3.backup.md` | v5 前備份（含 v4 樹狀設計） |
| `backup/.gitignore.v1.backup` | 初始 .gitignore 備份 |

## 五、index.html 功能

> ⚠️ **本次設計變更（v5）**：回歸極簡——去掉樹狀摺疊、自訂搜尋、虛擬鍵盤，全部漢字依倉頡碼順序**平鋪成列表**；搜尋交給瀏覽器內建 Ctrl+F。唯一速度瓶頸（約 2.25 MB 字型檔）以**全螢幕遮罩＋fetch 真實進度條**呈現。`build.py`／`index.html` 已據此重產。

1. **全部漢字平鋪展示**：17,183 個漢字（17,175 有碼 + 8 補遺），依倉頡碼字母順序平鋪；24 字母分節（難 x、重 z 不作首碼，故無其分節）。
2. **倉頡碼以字根漢字顯示**：每字卡片下方以字根漢字標註其倉頡碼（日月金木…，含難、重）。
3. **字型進度遮罩（v5）**：開啟即顯示全螢幕遮罩（草＋細進度條＋百分比）；用 `fetch()` 下載字型算真實 bytes 進度，完成後以 CSS Font Loading API（`new FontFace`＋`document.fonts.add`）掛上、淡出遮罩。無 `@font-face`／`preload`（避免重複下載）；無 JS 時以 `<noscript>` 隱藏遮罩、系統襯線兜底。
4. **極簡 JS**：全頁僅此一段（約 0.9 KB），其餘零 JS。
5. **速度與行動版**：`content-visibility: auto` 跳過屏外渲染、`@media (max-width:640px)` 適配、回頂部按鈕。

## 六、待辦（釋出階段）

> ⚠️ 尚未執行，待使用者確認後進行。

1. 初始化 git repo（`git init -b main`）。
2. `git add -A` + commit（`.gitignore` 已排除 `__pycache__/`、`*.pyc`、`backup/`、`report.txt`）。
3. `gh repo create tsao --public --source . --push`（repo 名稱預設 `tsao`、公開；已登入帳號 `sujmao`）。
4. 啟用 GitHub Pages（main 分支根目錄）。
5. 回報網址：`https://sujmao.github.io/tsao/`。

## 七、資料來源

- 字型：mikhailcai《草書》（孫過庭書風，免費放棄版權）
- 碼錶：倉頡五代單字碼表 `cangjie5.dict.yaml`（GPL）
- 臺灣字表：教育部《國字標準字體表》甲／乙表 → [gitqwerty777/Chinese-Characters-Standards](https://github.com/gitqwerty777/Chinese-Characters-Standards)
- 香港字表：教育局《常用字字形表》 → [leonsilicon/list-of-graphemes-of-commonly-used-chinese-characters](https://github.com/leonsilicon/list-of-graphemes-of-commonly-used-chinese-characters)
