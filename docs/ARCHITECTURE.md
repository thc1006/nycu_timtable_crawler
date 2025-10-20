# 專案架構說明

## 📂 目錄結構

```
nycu_timtable_crawler/
│
├── 📄 README.md                    # 主要文檔（使用說明）
├── 📄 LICENSE                      # Apache 2.0 授權
├── 📄 requirements.txt             # Python 依賴
├── 📄 .gitignore                   # Git 忽略規則
│
├── 🐍 核心爬蟲
│   └── nycu_crawler.py             # 主爬蟲引擎 (v4.0)
│
├── 📁 scripts/                     # 生產環境指令稿
│   ├── crawl_basic_batch_multithreaded.py      # ✅ 推薦：多執行緒爬取基本資訊
│   ├── crawl_outline_batch_multithreaded.py    # ✅ 推薦：多執行緒爬取完整綱要
│   └── monitor_progress.sh                     # ✅ 進度監控 (Shell 腳本)
│
├── 📁 examples/                    # 使用範例
│   ├── search_courses.py           # 課程搜尋示例
│   ├── analyze_statistics.py       # 統計分析示例
│   └── check_conflicts.py          # 衝堂檢查示例
│
├── 📁 notebooks/                   # Jupyter 筆記本
│   ├── NYCU_Crawler_Basic.ipynb    # Google Colab 版（基本資訊）
│   ├── NYCU_Crawler_WithOutline.ipynb  # Google Colab 版（完整綱要）
│   └── README_NOTEBOOK_UPDATE.md   # 筆記本說明
│
├── 📁 course_data/                 # 課程資料存儲
│   ├── basic/                      # 基本資訊 (9 個學期)
│   │   ├── 110-1_data.json         # ~5.2 MB
│   │   ├── 110-2_data.json         # ~5.0 MB
│   │   ├── ... (7 個其他學期)
│   │   └── .gitkeep
│   │
│   └── with_outline/               # 完整綱要 (進行中)
│       ├── 110-1_data_with_outline.json    # ~49 MB
│       ├── 110-2_data_with_outline.json    # ~44 MB
│       ├── ... (進行中)
│       ├── 114-1_data_with_outline.json    # ~65 MB
│       └── .gitkeep
│
├── 📁 tests/                       # 測試檔案
│   ├── test_*.py                   # 功能測試
│   ├── quick_check.py              # 快速檢查工具
│   ├── analyze_failures.py         # 失敗分析工具
│   └── README.md                   # 測試說明
│
├── 📁 experimental/                # 實驗工具 (非生產)
│   ├── auto_optimize_engine.py     # 自動優化引擎
│   ├── breakthrough_outline_extractor.py   # 綱要提取器
│   ├── recrawl_all_improved.py     # 改進的爬蟲
│   └── README.md                   # 實驗說明
│
├── 📁 docs/                        # 文檔
│   ├── CHANGELOG.md                # 版本歷史
│   ├── CONTRIBUTING.md             # 貢獻指南
│   ├── FILE_STRUCTURE.md           # 舊檔案結構說明
│   ├── PROJECT_SUMMARY.md          # 專案摘要
│   ├── ARCHITECTURE.md             # 本檔案
│   ├── sample_data_format_v2.json  # 資料格式示例
│   └── README.md                   # 文檔說明
│
├── 📁 logs/                        # 日誌檔案
│   ├── outline_*.log               # 爬蟲執行日誌
│   ├── recrawl_*.log               # 重新爬取日誌
│   └── .gitkeep
│
└── .git/                           # Git 版本控制
```

## 🔄 依賴關係

```
requests >= 2.31.0
    ↓
nycu_crawler.py (核心引擎)
    ↓
    ├─→ scripts/*.py         (生產環境使用)
    ├─→ examples/*.py        (示例程式)
    ├─→ notebooks/*.ipynb    (Colab 使用)
    ├─→ tests/*.py           (開發測試)
    └─→ experimental/*.py    (實驗工具)
    ↓
course_data/
    ├─→ basic/*.json         (基本資訊)
    └─→ with_outline/*.json  (完整綱要)
```

## 🚀 使用流程

### 快速開始（推薦）

```bash
# 1. 安裝依賴
pip install -r requirements.txt

# 2. 爬取基本資訊（多執行緒，快速）
python scripts/crawl_basic_batch_multithreaded.py

# 3. 檢查進度
python check_progress.py

# 4. 查看數據
python examples/search_courses.py
```

### 完整綱要爬取

```bash
# 需要更多時間，使用多執行緒
python scripts/crawl_outline_batch_multithreaded.py
```

### 開發和測試

```bash
# 執行測試
python tests/test_improved_crawler.py

# 快速檢查
python tests/quick_check.py

# 分析失敗
python tests/analyze_failures.py
```

## 📊 資料格式

所有課程資料採用 **v2.0 陣列格式** 儲存：

```json
{
  "metadata": {
    "semester": "114-1",
    "semester_name": "113學年度上學期",
    "total_courses": 8028,
    "last_updated": "2025-10-20T...",
    "data_format_version": "2.0"
  },
  "courses": [
    {
      "id": "515002",
      "name": "微分方程",
      "teacher": "楊春美",
      "credit": 3.0,
      "schedule": [
        {
          "day": 1,
          "day_name": "Monday",
          "periods": [3, 4],
          "time_start": "10:10",
          "time_end": "12:00",
          "classroom": "EE102",
          "floor": "GF"
        }
      ]
    }
  ]
}
```

## 🔧 主要功能

| 功能 | 檔案 | 說明 |
|------|------|------|
| 基本爬取 | `nycu_crawler.py` | 爬取課程基本資訊 |
| 綱要爬取 | `nycu_crawler.py` | 爬取完整課程綱要 |
| 多執行緒 | `scripts/crawl_*.py` | 並行爬取多個學期 |
| 進度監控 | `check_progress.py` | 監控爬取進度 |
| 課程搜尋 | `examples/search_courses.py` | 搜尋課程 |
| 統計分析 | `examples/analyze_statistics.py` | 分析課程統計 |
| 衝堂檢查 | `examples/check_conflicts.py` | 檢查課程衝突 |

## 📈 性能指標

- **基本資訊**：~2-3 分鐘/學期（使用多執行緒）
- **完整綱要**：~50-60 分鐘/學期
- **總資料量**：66,149 門課程，~47.4 MB（基本）
- **已爬取學期**：110-1 至 114-1（9 個學期）

## 🛠️ 維護和貢獻

- 問題回報：[GitHub Issues](https://github.com/thc1006/nycu_timtable_crawler/issues)
- 貢獻指南：見 `docs/CONTRIBUTING.md`
- 版本歷史：見 `docs/CHANGELOG.md`

---

**最後更新**: 2025-10-20
**版本**: v4.0
**資料格式**: v2.0
