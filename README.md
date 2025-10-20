# NYCU 課程爬蟲 v4.0

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org)
[![License](https://img.shields.io/badge/License-Apache%202.0-green.svg)](LICENSE)
[![NYCU](https://img.shields.io/badge/NYCU-陽明交大-orange.svg)](https://www.nycu.edu.tw)
[![GitHub stars](https://img.shields.io/github/stars/thc1006/nycu_timtable_crawler)](https://github.com/thc1006/nycu_timtable_crawler/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/thc1006/nycu_timtable_crawler)](https://github.com/thc1006/nycu_timtable_crawler/network)
[![GitHub issues](https://img.shields.io/github/issues/thc1006/nycu_timtable_crawler)](https://github.com/thc1006/nycu_timtable_crawler/issues)
[![GitHub last commit](https://img.shields.io/github/last-commit/thc1006/nycu_timtable_crawler)](https://github.com/thc1006/nycu_timtable_crawler/commits)

國立陽明交通大學課程資訊爬蟲系統

## 🎯 功能特色

- ✅ **雙模式爬取**：基本資訊 / 完整課程綱要
- ✅ **新資料格式**：陣列格式 v2.0（易於資料分析與使用）
- ✅ **多執行緒支援**：4 執行緒並行，速度提升 3-4 倍
- ✅ **結構化資料**：時間、教室、學分等自動解析
- ✅ **斷點續爬**：支援中斷後繼續爬取
- ✅ **錯誤重試**：自動重試機制，提高成功率

## 📦 快速開始

### 1. 安裝相依套件

```bash
pip install requests
```

### 2. 爬取單一學期（基本資訊）

```bash
python nycu_crawler.py
```

修改 `nycu_crawler.py` 的參數：
```python
YEAR = 114          # 學年度
SEMESTER = 1        # 學期 (1=上學期, 2=下學期)
FETCH_OUTLINE = False  # False=基本資訊, True=完整綱要
```

### 3. 批次爬取多個學期（推薦，使用多執行緒）

```bash
python scripts/crawl_basic_batch_multithreaded.py
```

### 4. 使用 Google Colab (免安裝環境)

**基本資訊版（已更新至 v4.0）**：
1. 開啟 `notebooks/NYCU_Crawler_Basic.ipynb`
2. 上傳到 [Google Colab](https://colab.research.google.com/)
3. 依序執行所有 cells
4. 下載生成的 JSON 檔案

**優點**：
- 無需安裝 Python 環境
- 雲端執行，不佔用本機資源
- 已包含 v4.0 所有新功能

**完整綱要版**：
- 參考 `notebooks/README_NOTEBOOK_UPDATE.md`

## 📊 資料格式說明

### 新格式 v2.0（陣列格式）

輸出檔案包含 `metadata` 和 `courses` 兩部分：

```json
{
  "metadata": {
    "semester": "114-1",
    "semester_name": "113學年度上學期",
    "total_courses": 8028,
    "last_updated": "2025-10-20T10:30:00Z",
    "data_format_version": "2.0"
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
      "tags": ["工程數學"]
    }
  ]
}
```

### 主要改進

| 項目 | 舊格式 | 新格式 v2.0 |
|------|--------|-------------|
| **資料結構** | 物件（Object） | 陣列（Array） |
| **學分/時數** | 字串 `"3.00"` | 數字 `3.0` |
| **時間表** | 字串 `["M3", "M4"]` | 結構化物件（含星期、節次、時間、教室） |
| **人數資訊** | 兩個欄位 | 巢狀物件 `enrollment` |
| **Metadata** | 無 | 完整學期資訊 |

## 📁 專案結構

```
nycu_timtable_crawler/
├── nycu_crawler.py                    # 主要爬蟲程式 (v4.0)
├── check_progress.py                  # 進度監控工具
├── scripts/
│   ├── crawl_basic_batch_multithreaded.py      # 基本資訊（多執行緒，推薦）
│   ├── crawl_outline_batch_multithreaded.py    # 完整綱要（多執行緒）
│   └── single_thread/
│       ├── crawl_basic_batch.py                # 批次爬取（單執行緒）
│       └── crawl_with_outline.py               # 完整綱要（單執行緒）
├── course_data/
│   ├── basic/                         # 基本課程資訊（已完成）
│   │   ├── 110-1_data.json           # 7,055 門課程
│   │   ├── 110-2_data.json           # 7,298 門課程
│   │   ├── 111-1_data.json           # 7,197 門課程
│   │   ├── 111-2_data.json           # 7,075 門課程
│   │   ├── 112-1_data.json           # 7,853 門課程
│   │   ├── 112-2_data.json           # 7,261 門課程
│   │   ├── 113-1_data.json           # 7,997 門課程
│   │   ├── 113-2_data.json           # 7,385 門課程
│   │   └── 114-1_data.json           # 8,028 門課程
│   └── with_outline/                  # 完整課程綱要（爬取中）
├── notebooks/                         # Jupyter Notebook 版本
│   ├── NYCU_Crawler_Basic.ipynb      # 基本資訊版（已更新至 v4.0）
│   ├── NYCU_Crawler_WithOutline.ipynb  # 完整綱要版
│   └── README_NOTEBOOK_UPDATE.md     # Notebook 說明文件
└── README.md
```

## 🚀 使用案例

### 基本資訊模式

**適用於**：
- 課表排課工具
- 課程搜尋系統
- 選課助手
- 時間衝堂檢查

**爬取速度**：每學期約 2-3 分鐘（約 7,000-8,000 門課程）

### 完整綱要模式

**適用於**：
- 課程內容研究
- 教學大綱資料庫
- 課程推薦系統
- 先修課程分析

**爬取速度**：每學期約 50-60 分鐘（需呼叫 4 個額外 API）

**額外包含**：
- 課程描述、先修科目
- 評分方式、教科書
- 每週授課進度（16-18 週）
- 單元時數分配

## 💡 常見問題

### Q: 如何只爬取最新學期？

修改 `nycu_crawler.py` 並直接執行：
```python
YEAR = 114
SEMESTER = 1
```

### Q: 如何爬取完整綱要？

方法一：修改主程式
```python
FETCH_OUTLINE = True  # 改為 True
```

方法二：使用專用腳本
```bash
python scripts/single_thread/crawl_with_outline.py
```

### Q: 資料更新頻率？

建議每學期開學前 1-2 週爬取一次，課程資訊較穩定。

### Q: 為什麼使用陣列格式？

陣列格式符合業界標準（RESTful API），易於：
- 分頁、排序、篩選
- 匯入資料庫（PostgreSQL/MongoDB）
- 前端框架使用（React/Vue）
- 資料分析（Pandas）

## 📈 效能數據

| 學期 | 課程數 | 檔案大小 | 爬取時間 |
|------|--------|----------|----------|
| 110-1 | 7,055 | 5.3 MB | 2分36秒 |
| 110-2 | 7,298 | 5.0 MB | 3分03秒 |
| 111-1 | 7,197 | 5.2 MB | 2分57秒 |
| 111-2 | 7,075 | 5.1 MB | 3分10秒 |
| 112-1 | 7,853 | 5.7 MB | 3分09秒 |
| 112-2 | 7,261 | 5.2 MB | 2分51秒 |
| 113-1 | 7,997 | 5.8 MB | 3分03秒 |
| 113-2 | 7,385 | 5.3 MB | 3分07秒 |
| 114-1 | 8,028 | 5.8 MB | 2分34秒 |

**總計**：66,149 門課程，47.4 MB，使用多執行緒約 3 分鐘完成全部

## 🔧 技術細節

### 結構化時間解析

原始格式：`"M34W2-EE102[GF]"`

解析為：
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

- **星期代碼**：M=一, T=二, W=三, R=四, F=五, S=六, U=日
- **節次代碼**：
  - y = 06:00-06:50
  - z = 07:00-07:50
  - 1-9 = 08:00-18:20
  - n = 12:10-13:00
  - a-d = 18:25-22:00

## 📝 版本歷史

### v4.0 (2025-10-20)
- ✨ 全新陣列格式 v2.0
- ✨ 結構化時間/教室解析
- ✨ 多執行緒批次爬取
- ✨ 型別標準化（數字改用 number）
- ✨ 加入 metadata 資訊
- ✨ 範例腳本（課程搜尋、統計分析、衝堂檢測）

### v3.0
- 支援斷點續爬
- 錯誤重試機制
- 進度顯示與 ETA

### v2.0
- 加入完整課程綱要支援
- 批次爬取功能

### v1.0
- 基本課程資訊爬取

## 📚 使用範例

我們提供了實用的範例腳本，位於 `examples/` 目錄：

### 1. 課程搜尋 (`search_courses.py`)
```bash
python examples/search_courses.py
```
示範如何：
- 依課程名稱搜尋（如「微積分」）
- 依教師姓名搜尋
- 依學分數搜尋
- 依上課時間搜尋（如星期一的課）

### 2. 統計分析 (`analyze_statistics.py`)
```bash
python examples/analyze_statistics.py
```
提供：
- 學分分布圖表
- 課程類型統計
- 授課語言比例
- 熱門上課時段
- 選課熱門度分析

### 3. 衝堂檢測 (`check_conflicts.py`)
```bash
python examples/check_conflicts.py
```
功能：
- 檢查兩門課程是否衝突
- 找出選課清單中的所有衝突
- 尋找不衝突的課程組合

詳細說明請參閱各腳本內的註解。

## 📜 授權

Apache License 2.0

詳見 [LICENSE](LICENSE) 檔案。

## 🙋 問題回報與貢獻

- 問題回報：請開 [Issue](https://github.com/thc1006/nycu_timtable_crawler/issues)
- 貢獻指南：參閱 [CONTRIBUTING.md](CONTRIBUTING.md)
- 版本歷史：參閱 [CHANGELOG.md](CHANGELOG.md)
- 聯絡信箱：hctsai@linux.com

歡迎陽明交大的同學們一起參與貢獻！

---

**更新日期**: 2025-10-20
**爬蟲版本**: v4.0
**資料格式**: v2.0 (陣列格式)
**資料集**: 110-1 至 114-1 學期（66,149 門課程）
