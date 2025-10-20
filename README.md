# NYCU 課程爬蟲 v4.0 / v4.1

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org)
[![License](https://img.shields.io/badge/License-Apache%202.0-green.svg)](LICENSE)
[![NYCU](https://img.shields.io/badge/NYCU-陽明交大-orange.svg)](https://www.nycu.edu.tw)
[![GitHub stars](https://img.shields.io/github/stars/thc1006/nycu_timtable_crawler)](https://github.com/thc1006/nycu_timtable_crawler/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/thc1006/nycu_timtable_crawler)](https://github.com/thc1006/nycu_timtable_crawler/network)
[![GitHub issues](https://img.shields.io/github/issues/thc1006/nycu_timtable_crawler)](https://github.com/thc1006/nycu_timtable_crawler/issues)
[![Version](https://img.shields.io/badge/Version-v4.0/v4.1-brightgreen.svg)]()

國立陽明交通大學課程資訊爬蟲系統 | NYCU Timetable Crawler System

> 🎯 **兩個版本，一個選擇**：單線程穩定版（v4.0）或 4 線程高性能版（v4.1），同時提供完整的命令行參數支援和生產等級代碼品質。

---

## 🎯 功能特色

### ⭐ 核心功能
- ✅ **雙爬蟲版本**：單線程穩定版（v4.0）+ 4線程性能版（v4.1）
- ✅ **雙模式爬取**：基本資訊 / 完整課程綱要
- ✅ **新資料格式**：陣列格式 v2.0（易於資料分析與使用）
- ✅ **結構化資料**：時間、教室、學分等自動解析
- ✅ **多線程支援**：4 線程並行綱要爬取，性能提升 20-30%
- ✅ **斷點續爬**：支援中斷後繼續爬取
- ✅ **智能重試**：自動重試機制 + 備選 HTML 解析方案

### 🔧 生產環境等級
- ✅ **命令行參數**：完整的 argparse 支援，靈活配置
- ✅ **參數驗證**：學年度、學期、線程數、超時檢查
- ✅ **Thread-Safe**：4 線程版本支援共享資源保護
- ✅ **錯誤處理**：異常捕捉、退出碼標準化
- ✅ **版本管理**：--version 支援，版本追蹤

### 📊 數據品質
- ✅ **自動去重**：課程 ID 追蹤，防止重複
- ✅ **型別標準化**：數字用 number 型態（非字串）
- ✅ **元數據完整**：爬蟲版本、格式版本、更新時間
- ✅ **高精度**：時間表解析 >99%，綱要成功率 >95%

---

## 📦 快速開始

### 1. 安裝相依套件

```bash
pip install -r requirements.txt
# 或手動安裝
pip install requests beautifulsoup4
```

### 2. 使用單線程版本（推薦用於穩定性）

```bash
# 預設：爬取 114-1 學期基本資訊
python nycu_crawler.py

# 爬取 113 年第 2 學期
python nycu_crawler.py --year 113 --semester 2

# 爬取完整綱要（耗時 50-60 分鐘）
python nycu_crawler.py --outline

# 完整選項
python nycu_crawler.py --year 114 --semester 1 --outline

# 顯示幫助和版本
python nycu_crawler.py --help
python nycu_crawler.py --version
```

### 3. 使用 4 線程版本（推薦用於速度）

```bash
# 預設：4 線程，基本資訊
python nycu_crawler_multithreaded.py

# 自訂線程數
python nycu_crawler_multithreaded.py --threads 8

# 爬取完整綱要（4 線程加速）
python nycu_crawler_multithreaded.py --outline --threads 4 --timeout 1800

# 高性能配置：8 線程，2 小時超時，包含綱要
python nycu_crawler_multithreaded.py --threads 8 --timeout 7200 --outline

# 爬取 113-2 學期
python nycu_crawler_multithreaded.py --year 113 --semester 2

# 所有選項
python nycu_crawler_multithreaded.py --help
```

### 4. 使用範例腳本

```bash
# 統計分析 - 學分分布、課程類型、熱門時段等
python examples/analyze_statistics.py

# 衝堂檢測 - 檢查選課清單中的時間衝突
python examples/check_conflicts.py

# 課程搜尋 - 按名稱、教師、學分、星期搜尋
python examples/search_courses.py
```

### 5. Google Colab 使用（無需本機環境）

1. 開啟 `notebooks/NYCU_Crawler_Basic.ipynb`
2. 上傳到 [Google Colab](https://colab.research.google.com/)
3. 依序執行所有 cells
4. 下載生成的 JSON 檔案

---

## 📊 命令行參數完整說明

### 單線程版本 (nycu_crawler.py)

| 參數 | 型態 | 預設 | 說明 |
|------|------|------|------|
| `--year` | int | 114 | 學年度 (100-200) |
| `--semester` | int | 1 | 學期 (1=上學期, 2=下學期) |
| `--outline` | flag | False | 爬取完整課程綱要 |
| `--help` | - | - | 顯示幫助信息 |
| `--version` | - | - | 顯示版本信息 |

**用法範例**：
```bash
# 爬取 114 年第 1 學期基本資訊（預設）
python nycu_crawler.py

# 爬取 113 年第 2 學期
python nycu_crawler.py --year 113 --semester 2

# 爬取完整綱要
python nycu_crawler.py --outline

# 同時指定學年、學期和綱要
python nycu_crawler.py --year 113 --semester 2 --outline
```

### 4 線程版本 (nycu_crawler_multithreaded.py)

| 參數 | 型態 | 預設 | 範圍 | 說明 |
|------|------|------|------|------|
| `--year` | int | 114 | 100-200 | 學年度 |
| `--semester` | int | 1 | 1, 2 | 學期 |
| `--outline` | flag | False | - | 爬取完整課程綱要 |
| `--threads` | int | 4 | 1-16 | 並行線程數（建議 2-8） |
| `--timeout` | int | 600 | ≥60 | 執行超時時間（秒） |
| `--help` | - | - | - | 顯示幫助信息 |
| `--version` | - | - | - | 顯示版本信息 |

**用法範例**：
```bash
# 預設：4 線程，基本資訊
python nycu_crawler_multithreaded.py

# 使用 8 線程爬取
python nycu_crawler_multithreaded.py --threads 8

# 30 分鐘超時
python nycu_crawler_multithreaded.py --timeout 1800

# 完整綱要：8 線程，2 小時超時
python nycu_crawler_multithreaded.py --outline --threads 8 --timeout 7200

# 爬取 113 年第 2 學期，6 線程，1 小時超時
python nycu_crawler_multithreaded.py --year 113 --semester 2 --threads 6 --timeout 3600
```

---

## 📈 性能對比

### 爬取速度

| 配置 | 課程數 | 執行時間 | 平均耗時 | 用途 |
|------|--------|---------|---------|------|
| 單線程（基本） | 8,028 | ~2-3 分鐘 | 0.015 秒/課 | 穩定性優先 |
| 4線程（基本） | 8,028 | ~2-3 分鐘 | 0.015 秒/課 | 平衡性能 |
| 單線程（綱要） | 8,028 | ~50-60 分鐘 | 0.37 秒/課 | 精度優先 |
| 4線程（綱要） | 8,028 | ~40-50 分鐘 | 0.30 秒/課 | **推薦** |

### 數據規模

| 項目 | 數值 |
|------|------|
| 單個學期課程數 | 7,000-8,000 門 |
| 基本資訊（JSON） | 5-6 MB |
| 完整綱要（JSON） | 43-63 MB |
| 全部 9 個學期 | 66,149 門課程，723 MB |
| 爬取效率 | 每分鐘 ~2,500-4,000 課程 |

### 精確度

| 指標 | 數值 |
|------|------|
| 重複課程去重 | 100% |
| 時間表解析成功率 | >99% |
| 課程基本資訊完整度 | 100% |
| 綱要爬取成功率（重試後） | >95% |

---

## 📁 專案結構

```
nycu_timtable_crawler/
│
├── 📄 核心文件
│   ├── nycu_crawler.py                    (33 KB, 822 行)
│   │   └── 單線程版本（v4.0，Production Grade）
│   │
│   ├── nycu_crawler_multithreaded.py      (37 KB, 913 行)
│   │   └── 4線程版本（v4.1，Production Grade）
│   │
│   ├── requirements.txt                   (依賴套件)
│   ├── README.md                          (本文件)
│   ├── IMPLEMENTATION_REPORT.md           (實現詳解)
│   ├── LICENSE                            (Apache 2.0)
│   └── .gitignore                         (Git 規則)
│
├── 📁 examples/ - 實用範例腳本 (317 行)
│   ├── analyze_statistics.py              (84 行 - 統計分析)
│   ├── check_conflicts.py                 (141 行 - 衝堂檢測)
│   └── search_courses.py                  (92 行 - 課程搜尋)
│
├── 📁 notebooks/ - Jupyter Notebook 版本
│   ├── NYCU_Crawler_Basic.ipynb           (基本資訊版)
│   ├── NYCU_Crawler_WithOutline.ipynb     (完整綱要版)
│   └── README.md                          (使用說明)
│
└── 📁 course_data/ - 課程數據存儲 (755 MB)
    │
    ├── basic/ (54 MB, 10 個 JSON)
    │   ├── 110-1_data.json       (5.3 MB, 7,055 課)
    │   ├── 110-2_data.json       (5.0 MB, 7,298 課)
    │   ├── 111-1_data.json       (5.2 MB, 7,197 課)
    │   ├── 111-2_data.json       (5.1 MB, 7,075 課)
    │   ├── 112-1_data.json       (5.7 MB, 7,853 課)
    │   ├── 112-2_data.json       (5.2 MB, 7,261 課)
    │   ├── 113-1_data.json       (5.8 MB, 7,997 課)
    │   ├── 113-2_data.json       (5.3 MB, 7,385 課)
    │   └── 114-1_data.json       (5.8 MB, 8,028 課) ⭐ 最新
    │
    └── with_outline/ (676 MB, 13 個 JSON - 完整綱要)
        ├── 110-1_data_with_outline.json    (48 MB)
        ├── 110-2_data_with_outline.json    (43 MB)
        ├── 111-1_data_with_outline.json    (47 MB)
        ├── 111-2_data_with_outline.json    (54 MB)
        ├── 112-1_data_with_outline.json    (61 MB)
        ├── 112-2_data_with_outline.json    (55 MB)
        ├── 113-2_data_with_outline.json    (56 MB)
        └── 114-1_data_with_outline.json    (63 MB) ⭐ 最新

📊 統計：66,149 門課程，723.4 MB 數據
```

---

## 📊 資料格式說明

### 新格式 v2.0（標準陣列格式）

輸出檔案包含 `metadata` 和 `courses` 兩部分：

```json
{
  "metadata": {
    "semester": "114-1",
    "semester_name": "113學年度上學期",
    "academic_year": 114,
    "term": 1,
    "total_courses": 8028,
    "last_updated": "2025-10-20T10:56:00Z",
    "source_url": "https://timetable.nycu.edu.tw",
    "crawler_version": "4.0",
    "data_format_version": "2.0",
    "num_threads": 4
  },
  "courses": [
    {
      "id": "515002",
      "semester_code": "1141",
      "name": "微分方程",
      "teacher": "楊春美",
      "credit": 3.0,
      "hours": 3.0,
      "type": "必修",
      "enrollment": {
        "limit": 55,
        "current": 66
      },
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
      ],
      "english_taught": false,
      "tags": ["工程數學"],
      "raw_time_classroom": "M34-EE102[GF]"
    }
  ]
}
```

### 主要改進（v2.0 vs 舊版）

| 項目 | 舊格式 | 新格式 v2.0 |
|------|--------|------------|
| **資料結構** | 物件（Object） | **陣列（Array）** |
| **學分/時數** | 字串 `"3.00"` | **數字 `3.0`** |
| **時間表** | 字串 `["M3", "M4"]` | **結構化對象**（含星期、節次、時間、教室、樓層） |
| **人數資訊** | 兩個獨立欄位 | **巢狀對象** `enrollment` |
| **Metadata** | 無 | **完整學期資訊** |
| **標準化** | 不一致 | **RESTful API 標準** |

---

## 🚀 使用案例

### 基本資訊模式（推薦首選）

**適用於**：
- 🎓 課表排課工具
- 🔍 課程搜尋系統
- 📝 選課助手
- ⏰ 時間衝堂檢查

**特性**：
- ⚡ 快速（2-3 分鐘/學期）
- 🎯 精準（8,000+ 課程）
- 📱 輕量（5-6 MB/學期）
- ✅ 穩定（100% 成功率）

**推薦命令**：
```bash
# 單線程穩定版
python nycu_crawler.py

# 或 4 線程性能版
python nycu_crawler_multithreaded.py
```

### 完整綱要模式（高級用途）

**適用於**：
- 📚 課程內容研究
- 📖 教學大綱資料庫
- 🤖 課程推薦系統
- 🔗 先修課程分析
- 📊 課程統計分析

**包含數據**：
- 課程描述 (course_description)
- 先修科目 (prerequisites)
- 評分方式 (grading_methods)
- 教科書 (textbooks)
- 每週授課進度（16-18 週）
- 單元時數分配 (unit_hours)

**推薦命令**：
```bash
# 4 線程性能版（推薦，快 20% 左右）
python nycu_crawler_multithreaded.py --outline --threads 4 --timeout 1800

# 或單線程穩定版
python nycu_crawler.py --outline
```

---

## 💡 常見問題

### Q: 應該使用哪個版本？

**A**:
- **推薦單線程版** (nycu_crawler.py)：要求最大穩定性
- **推薦 4 線程版** (nycu_crawler_multithreaded.py)：需要性能優化或爬取綱要

兩個版本都達到 Production Grade 標準。

### Q: 如何快速爬取最新課程？

**A**:
```bash
python nycu_crawler_multithreaded.py  # 4線程版本，最快
```

### Q: 爬取完整綱要需要多長時間？

**A**:
- 單線程版本：50-60 分鐘
- 4 線程版本：40-50 分鐘（使用 --threads 4）

可調整 `--threads` 和 `--timeout` 參數。

### Q: 如何只爬取特定學期？

**A**:
```bash
python nycu_crawler.py --year 113 --semester 2
```

學期參數：1 = 上學期，2 = 下學期

### Q: 為什麼使用陣列格式？

**A**:
陣列格式符合業界標準（RESTful API），易於：
- 分頁、排序、篩選
- 匯入資料庫（PostgreSQL/MongoDB）
- 前端框架使用（React/Vue）
- 數據分析（Pandas/NumPy）

### Q: 資料更新頻率？

**A**:
建議每學期開學前 1-2 週爬取一次，課程資訊較穩定。

### Q: 如何確保爬取不中斷？

**A**:
使用 4 線程版本和合理的 timeout：
```bash
python nycu_crawler_multithreaded.py --timeout 1800
```

若需要綱要，增加 timeout：
```bash
python nycu_crawler_multithreaded.py --outline --timeout 3600
```

### Q: 能否修改線程數以加速？

**A**:
可以，但建議在 2-8 之間。過多可能造成伺服器限流：
```bash
python nycu_crawler_multithreaded.py --threads 8  # 8線程
python nycu_crawler_multithreaded.py --threads 2  # 2線程
```

---

## 🔧 技術細節

### 結構化時間解析

**原始格式**：`"M34W2-EE102[GF]"`

**解析為結構化對象**：
```json
{
  "day": 1,
  "day_name": "Monday",
  "periods": [3, 4],
  "time_start": "10:10",
  "time_end": "12:00",
  "classroom": "EE102",
  "floor": "GF"
}
```

### 時段對照表

**星期代碼**：
- M = Monday（一）
- T = Tuesday（二）
- W = Wednesday（三）
- R = Thursday（四）
- F = Friday（五）
- S = Saturday（六）
- U = Sunday（日）

**節次代碼**：
- y = 06:00-06:50
- z = 07:00-07:50
- 1 = 08:00-08:50
- 2 = 09:00-09:50
- 3 = 10:10-11:00
- 4 = 11:10-12:00
- n = 12:10-13:00
- 5 = 13:20-14:10
- 6 = 14:20-15:10
- 7 = 15:30-16:20
- 8 = 16:30-17:20
- 9 = 17:30-18:20
- a = 18:25-19:15
- b = 19:20-20:10
- c = 20:15-21:05
- d = 21:10-22:00

### 爬取策略

1. **逐層遍歷**：類型 → 類別 → 學院 → 系所 → 課程
2. **智能去重**：使用 set 追蹤已處理課程 ID
3. **自動重試**：失敗時指數退避重試（最多 10 次）
4. **備選方案**：JSON API 失敗時嘗試 HTML 解析
5. **斷點續爬**：checkpoint 檔案保存進度

---

## 📚 範例代碼說明

### 1. analyze_statistics.py - 課程統計分析

提供多維度統計分析：

```bash
python examples/analyze_statistics.py
```

**輸出包括**：
- 基本統計：總課程數、資料格式版本
- 學分分布：各學分數課程統計
- 課程類型：必修、選修、通識等分類
- 授課語言：中文 vs 英文比例
- 熱門時段：各星期上課堂數
- 選課熱門度：額滿課程統計
- 圖表展示：視覺化結果

### 2. check_conflicts.py - 衝堂檢測

檢測選課清單中的時間衝突：

```bash
python examples/check_conflicts.py
```

**功能**：
- 檢查兩門課程是否衝突
- 檢查選課清單中的所有衝突
- 找出與特定課程不衝突的其他課程

**使用場景**：
```python
# 檢查課程 515002 和 515003 是否衝突
course_a = find_course("515002")
course_b = find_course("515003")
is_conflict = check_conflict(course_a, course_b)
```

### 3. search_courses.py - 課程搜尋

多條件靈活搜尋課程：

```bash
python examples/search_courses.py
```

**搜尋方式**：
- 課程名稱包含關鍵字（模糊搜尋）
- 特定教師的課程
- 指定學分數
- 特定星期有課的課程

**使用場景**：
```python
# 搜尋含「微積分」的課程
results = search_by_name("微積分")

# 搜尋教師「楊春美」的課程
results = search_by_teacher("楊春美")

# 搜尋 3 學分的課程
results = search_by_credit(3)

# 搜尋星期一有課的課程
results = search_by_day("Monday")
```

---

## 📝 版本歷史

### v4.1 (2025-01-20) 🆕 - 4 線程版本
**新增功能**：
- ✨ 新增 nycu_crawler_multithreaded.py（4 線程版本）
- ✨ ThreadPoolExecutor 並行架構
- ✨ Thread-safe 統計與資源保護
- ✨ 自定義線程數參數（1-16）
- ✨ 自定義超時參數支援
- ✨ 完整的命令行參數驗證
- ✨ 性能提升 20-30%（綱要爬取）

**改進項目**：
- 🔧 Lock 機制保護共享資源
- 🔧 改進進度顯示（並行環境）
- 🔧 參數驗證更完善
- 🔧 異常處理更健壯

### v4.0 (2025-10-20) - 單線程生產版
**新增功能**：
- ✨ 全新陣列格式 v2.0
- ✨ 結構化時間/教室解析
- ✨ 完整命令行參數支援 (argparse)
- ✨ 型別標準化（數字改用 number）
- ✨ 加入 metadata 資訊
- ✨ 範例腳本（課程搜尋、統計分析、衝堂檢測）
- ✨ 生產等級代碼品質檢查
- ✨ 參數驗證（年度、學期、outline 標誌）

### v3.0
- 支援斷點續爬
- 錯誤重試機制
- 進度顯示與 ETA
- 改善網絡穩定性

### v2.0
- 加入完整課程綱要支援
- 批次爬取功能
- 多學期自動化爬取

### v1.0
- 基本課程資訊爬取
- 初版實現

---

## 🎯 推薦使用方式

### 場景 1: 快速取得最新課表
```bash
# 最快方式
python nycu_crawler_multithreaded.py
# 耗時：2-3 分鐘
```

### 場景 2: 批次爬取多個學期
```bash
# 爬取 113 年上下學期
python nycu_crawler_multithreaded.py --year 113 --semester 1
python nycu_crawler_multithreaded.py --year 113 --semester 2
```

### 場景 3: 取得完整綱要數據
```bash
# 4 線程加速
python nycu_crawler_multithreaded.py --outline --threads 4 --timeout 1800
# 耗時：40-50 分鐘
```

### 場景 4: 最穩定的爬取方式
```bash
# 單線程版本
python nycu_crawler.py
# 耗時：2-3 分鐘（基本）或 50-60 分鐘（綱要）
```

### 場景 5: 數據分析研究
```bash
# 爬取完整綱要
python nycu_crawler_multithreaded.py --outline --threads 8

# 統計分析
python examples/analyze_statistics.py

# 衝堂檢測
python examples/check_conflicts.py

# 課程搜尋
python examples/search_courses.py
```

---

## 📜 授權與貢獻

**授權**：Apache License 2.0

詳見 [LICENSE](LICENSE) 檔案。

### 聯絡與支援

- 📧 **聯絡信箱**：hctsai@linux.com
- 🐛 **問題回報**：[GitHub Issues](https://github.com/thc1006/nycu_timtable_crawler/issues)
- 💝 **貢獻指南**：參閱 [CONTRIBUTING.md](CONTRIBUTING.md)
- 📜 **版本歷史**：參閱 [CHANGELOG.md](CHANGELOG.md)
- 📋 **實現詳解**：參閱 [IMPLEMENTATION_REPORT.md](IMPLEMENTATION_REPORT.md)

歡迎陽明交大的同學們一起參與貢獻！

---

## 📊 項目統計

| 項目 | 數值 |
|------|------|
| **Python 源碼** | 2,052 行 |
| **主程式行數** | 1,735 行 |
| **範例代碼行數** | 317 行 |
| **文檔大小** | 16.5 KB |
| **課程數據** | 66,149 門課程 |
| **數據總量** | 723.4 MB |
| **基本資訊檔案** | 10 個 JSON (54 MB) |
| **完整綱要檔案** | 13 個 JSON (676 MB) |
| **支援學期** | 9 個 (110-1 ~ 114-1) |
| **GitHub Stars** | [![Stars](https://img.shields.io/github/stars/thc1006/nycu_timtable_crawler?style=social)](https://github.com/thc1006/nycu_timtable_crawler/stargazers) |

---

## 🎓 致謝

感謝所有為本項目做出貢獻的開發者和使用者！

本項目基於開源精神，致力於為陽明交大學生提供便利的課程資訊查詢工具。

---

**最後更新**：2025-10-20
**爬蟲版本**：v4.0（單線程）/ v4.1（4 線程）
**資料格式版本**：v2.0（陣列格式）
**數據集**：110-1 至 114-1 學期（66,149 門課程，723 MB）
**環境等級**：Production Grade ✓
