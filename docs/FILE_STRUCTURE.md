# 專案檔案結構

```
nycu_timtable_crawler/
│
├── 📄 README.md                          # 主要文檔（使用說明、API、範例）
├── 📄 PROJECT_SUMMARY.md                 # 專案總結（統計、特色、品質）
├── 📄 .gitignore                         # Git 忽略規則
│
├── 🐍 nycu_crawler.py                    # 主爬蟲程式
├── 🐍 crawl_basic_batch.py               # 批次爬取工具
│
├── 📓 NYCU_Crawler_Basic.ipynb           # Google Colab 版（基本資訊）
├── 📓 NYCU_Crawler_WithOutline.ipynb     # Google Colab 版（完整綱要）
│
├── 🌐 index.html                         # 網頁介面
├── 🌐 app.js                             # 前端 JavaScript
├── 🌐 style.css                          # 網頁樣式
│
└── 📁 course_data/                       # 課程資料目錄
    ├── 📄 README.md                      # 資料目錄說明
    │
    ├── 📁 basic/                         # 基本資訊（5 學期）
    │   ├── 112-1_data.json              # 3,584 門課程 (1.54 MB)
    │   ├── 112-2_data.json              # 3,623 門課程 (1.54 MB)
    │   ├── 113-1_data.json              # 3,642 門課程 (1.56 MB)
    │   ├── 113-2_data.json              # 3,562 門課程 (1.52 MB)
    │   └── 114-1_data.json              # 3,619 門課程 (1.55 MB)
    │
    └── 📁 with_outline/                  # 完整綱要
        └── 114-1_data_with_outline.json  # 3,550 門課程 (26.93 MB)
```

## 檔案說明

### 📄 文檔檔案

| 檔案 | 大小 | 說明 |
|------|------|------|
| `README.md` | 9 KB | 主要使用文檔，包含快速開始、API 說明、範例 |
| `PROJECT_SUMMARY.md` | 3 KB | 專案總結，包含統計資料、特色、品質指標 |
| `FILE_STRUCTURE.md` | - | 本檔案，專案檔案結構說明 |
| `.gitignore` | 0.6 KB | Git 版本控制忽略規則 |

### 🐍 Python 程式

| 檔案 | 行數 | 說明 |
|------|------|------|
| `nycu_crawler.py` | ~500 | 主爬蟲程式，支援基本/完整兩種模式 |
| `crawl_basic_batch.py` | ~20 | 批次爬取多學期基本資訊工具 |

### 📓 Jupyter Notebooks

| 檔案 | 大小 | 說明 |
|------|------|------|
| `NYCU_Crawler_Basic.ipynb` | 16 KB | Google Colab 版本（基本資訊模式）|
| `NYCU_Crawler_WithOutline.ipynb` | 26 KB | Google Colab 版本（完整綱要模式）|

### 🌐 網頁檔案

| 檔案 | 大小 | 說明 |
|------|------|------|
| `index.html` | 5.4 KB | 課程選課模擬系統網頁介面 |
| `app.js` | 17 KB | 前端 JavaScript 邏輯 |
| `style.css` | 178 B | 網頁樣式表 |

### 📁 資料目錄

#### basic/ (基本資訊)
包含 5 個學期的基本課程資訊，每個檔案約 1.5 MB。

#### with_outline/ (完整綱要)
包含 114-1 學期的完整課程綱要，檔案約 27 MB。

## 統計資訊

### 程式碼統計
- **總檔案數**：12 個
- **Python 檔案**：2 個
- **Notebook 檔案**：2 個
- **網頁檔案**：3 個
- **文檔檔案**：5 個

### 資料統計
- **資料檔案**：6 個
- **總資料量**：約 35 MB
- **課程總數**：18,030 門（基本）+ 3,550 門（完整）

### 程式碼行數
- **Python 總行數**：約 520 行
- **主爬蟲**：約 500 行
- **批次工具**：約 20 行

## 乾淨度檢查

✅ 無 `__pycache__/` 目錄  
✅ 無 `.pyc` 編譯檔案  
✅ 無測試/臨時檔案  
✅ 無重複資料檔案  
✅ `.gitignore` 已設定  
✅ 所有檔案已分類整理  

## 版本資訊

- **專案版本**：1.0.0 Production
- **最後更新**：2025-01-19
- **Python 版本**：3.7+
- **授權**：MIT License

---

**狀態**：✅ Ready for Production / Sharing
