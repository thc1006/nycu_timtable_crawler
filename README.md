# NYCU 課程爬蟲

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org)
[![License](https://img.shields.io/badge/License-Apache%202.0-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-v4.0/v4.1-brightgreen.svg)]()

國立陽明交通大學課程資訊爬蟲 | NYCU Timetable Crawler

## ✨ 功能

- **雙版本**：單線程穩定版 + 4線程高性能版
- **雙模式**：基本資訊（2-3 分鐘） / 完整綱要（40-60 分鐘）
- **陣列格式 v2.0**：結構化時間、教室、學分等資料
- **自動去重、智能重試、斷點續爬**
- **66,149 門課程**覆蓋 9 個學期（723 MB）

---

## 📦 快速開始

### 安裝 & 使用

```bash
# 安裝依賴
pip install -r requirements.txt

# 方式 1: 單線程版本（穩定性優先）
python nycu_crawler.py                              # 基本資訊（預設 114-1）
python nycu_crawler.py --year 113 --semester 2     # 爬取特定學期
python nycu_crawler.py --outline                    # 爬取完整綱要

# 方式 2: 4線程版本（性能優先，推薦）
python nycu_crawler_multithreaded.py                # 基本資訊
python nycu_crawler_multithreaded.py --outline      # 完整綱要
python nycu_crawler_multithreaded.py --threads 8   # 自訂線程數

# 範例腳本
python examples/analyze_statistics.py    # 統計分析
python examples/check_conflicts.py       # 衝堂檢測
python examples/search_courses.py        # 課程搜尋
```

---

## ⚙️ 命令行參數

| 參數 | 說明 | 預設 |
|------|------|------|
| `--year` | 學年度 (100-200) | 114 |
| `--semester` | 學期 (1=上, 2=下) | 1 |
| `--outline` | 爬取完整課程綱要 | False |
| `--threads` | 線程數 (1-16，4線程版本) | 4 |
| `--timeout` | 超時秒數 (4線程版本) | 600 |
| `--help` | 顯示幫助 | - |
| `--version` | 顯示版本 | - |

---

## 📈 性能 & 精確度

| 項目 | 基本資訊 | 完整綱要 |
|------|---------|---------|
| **執行時間** | 2-3 分鐘 | 40-60 分鐘 |
| **檔案大小** | 5-6 MB | 43-63 MB |
| **解析成功率** | 100% | >95% |

- 單個學期：7,000-8,000 門課程
- 全部 9 學期：66,149 門課程，723 MB
- 去重率：100% | 時間表解析：>99%

---

## 📁 專案結構

```
nycu_timtable_crawler/
├── nycu_crawler.py                  # 單線程版本
├── nycu_crawler_multithreaded.py    # 4線程版本
├── examples/
│   ├── analyze_statistics.py        # 統計分析
│   ├── check_conflicts.py          # 衝堂檢測
│   └── search_courses.py           # 課程搜尋
├── notebooks/                       # Jupyter Notebook
├── course_data/                     # 爬蟲數據 (723 MB)
│   ├── basic/                       # 基本資訊 (54 MB)
│   └── with_outline/                # 完整綱要 (676 MB)
└── requirements.txt, LICENSE, README.md
```

---

## 📊 資料格式 (v2.0)

JSON 包含 `metadata` 和 `courses` 陣列：

```json
{
  "metadata": {
    "semester": "114-1",
    "total_courses": 8028,
    "crawler_version": "4.0",
    "data_format_version": "2.0"
  },
  "courses": [
    {
      "id": "515002",
      "name": "微分方程",
      "teacher": "楊春美",
      "credit": 3.0,
      "type": "必修",
      "enrollment": {"limit": 55, "current": 66},
      "schedule": [
        {
          "day": 1,
          "periods": [3, 4],
          "time_start": "10:10",
          "classroom": "EE102"
        }
      ]
    }
  ]
}
```

**改進**：陣列格式、數字型別、結構化時間、完整 metadata、RESTful API 標準

---

## 🚀 常用場景

| 需求 | 建議命令 | 耗時 |
|------|---------|------|
| 快速取得課表 | `python nycu_crawler_multithreaded.py` | 2-3 分鐘 |
| 穩定爬取 | `python nycu_crawler.py` | 2-3 分鐘 |
| 完整綱要 | `python nycu_crawler_multithreaded.py --outline` | 40-50 分鐘 |
| 特定學期 | `python nycu_crawler.py --year 113 --semester 2` | 2-3 分鐘 |
| 統計分析 | `python examples/analyze_statistics.py` | - |
| 衝堂檢測 | `python examples/check_conflicts.py` | - |

---

## 💡 常見問題

**Q: 單線程 vs 4線程？** → 單線程更穩定，4線程更快（特別是綱要爬取）

**Q: 爬取綱要需要多久？** → 單線程 50-60 分鐘，4線程 40-50 分鐘

**Q: 如何爬取特定學期？**
```bash
python nycu_crawler.py --year 113 --semester 2  # 113年第2學期
```

**Q: 完整綱要包含什麼？** → 課程描述、先修科目、評分方式、教科書、16-18週授課進度

**Q: 線程數越多越好？** → 建議 2-8，過多可能被限流。使用 `--threads 8`

**Q: 資料更新頻率？** → 建議每學期開學前 1-2 週爬取一次

---

## 🔧 技術細節

**時間解析**：原始格式 `M34W2-EE102[GF]` → 結構化 `{day:1, periods:[3,4], time_start:"10:10", classroom:"EE102"}`

**星期代碼**：M/T/W/R/F/S/U = 一/二/三/四/五/六/日

**節次對應**：1=08:00, 2=09:00, 3=10:10, 4=11:10, 5=13:20, 6=14:20, 7=15:30, 8=16:30, 9=17:30, a=18:25, b=19:20, c=20:15, d=21:10

**爬取策略**：類型→類別→學院→系所→課程、智能去重、指數退避重試、備選HTML解析、斷點續爬

---

## 📚 範例腳本

| 腳本 | 功能 |
|------|------|
| `analyze_statistics.py` | 統計學分分布、課程類型、授課語言、熱門時段、額滿課程等 |
| `check_conflicts.py` | 檢測兩門課程是否衝突、檢查選課清單衝堂 |
| `search_courses.py` | 按名稱、教師、學分、星期搜尋課程 |

---

## 📝 版本歷史

| 版本 | 發布日期 | 主要功能 |
|------|---------|---------|
| v4.1 | 2025-01-20 | 4線程版本、ThreadPoolExecutor、Thread-safe、性能 +20-30% |
| v4.0 | 2025-10-20 | 陣列格式v2.0、結構化時間、argparse參數、metadata |
| v3.0 | - | 斷點續爬、錯誤重試、進度顯示、網絡優化 |
| v2.0 | - | 完整綱要支援、批次爬取、多學期自動化 |
| v1.0 | - | 基本課程資訊爬取 |

---

## 📜 授權與貢獻

**授權**：Apache License 2.0 | [詳見 LICENSE](LICENSE)

**聯絡**：hctsai@linux.com | [GitHub Issues](https://github.com/thc1006/nycu_timtable_crawler/issues)

**相關文件**：[IMPLEMENTATION_REPORT.md](IMPLEMENTATION_REPORT.md)

---

## 📊 項目統計

| 項目 | 統計 |
|------|------|
| Python 源碼 | 2,052 行（1,735 主程式 + 317 範例） |
| 課程數據 | 66,149 門課程（9 個學期） |
| 數據大小 | 723.4 MB（基本 54 MB + 綱要 676 MB） |
| 環境等級 | Production Grade ✓ |

**最後更新**：2025-10-20 | v4.0/v4.1 | v2.0 格式
