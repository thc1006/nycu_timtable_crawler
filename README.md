# NYCU 課程爬蟲

國立陽明交通大學課程資料爬蟲工具，支援爬取課程基本資訊與完整課程綱要。

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## ✨ 功能特色

### 基本功能
- ✅ 爬取課程基本資訊（課號、課名、教師、學分、時間、教室等）
- ✅ 爬取完整課程綱要（先修科目、課程概述、教科書、評分方式、每週進度、單元時數）
- ✅ 支援任意學期（修改參數即可）
- ✅ 批次爬取多學期資料

### 進階功能
- ✅ 進度顯示與剩餘時間預估
- ✅ 斷點續爬（中斷後可繼續）
- ✅ 錯誤自動重試（最多3次）
- ✅ 批次保存防止資料丟失
- ✅ Google Colab 支援

## 📊 爬取結果

### 114-1 學期完整爬取
- **總課程數**：3,619 門
- **綱要成功率**：98.1% (3,550/3,619)
- **總耗時**：59 分 35 秒
- **平均速度**：0.99 秒/門課
- **檔案大小**：26.93 MB
- **資料完整性**：所有綱要欄位 100% 完整

### 已收錄學期（基本資訊）
- 112-1：3,584 門課程
- 112-2：3,623 門課程
- 113-1：3,642 門課程
- 113-2：3,562 門課程
- 114-1：3,619 門課程

## 📁 專案結構

```
nycu_timtable_crawler/
├── nycu_crawler.py              # 主要爬蟲程式 (Production)
├── crawl_basic_batch.py         # 批次爬取基本資訊工具
├── NYCU_Crawler_Basic.ipynb    # Google Colab 版本 (基本資訊)
├── NYCU_Crawler_WithOutline.ipynb  # Google Colab 版本 (含綱要)
├── README.md                    # 專案說明文件
├── app.js                       # 前端應用程式
├── index.html                   # 網頁介面
├── style.css                    # 樣式表
└── course_data/                 # 課程資料目錄
    ├── basic/                   # 基本資訊 (112-1 ~ 114-1)
    │   ├── 112-1_data.json
    │   ├── 112-2_data.json
    │   ├── 113-1_data.json
    │   ├── 113-2_data.json
    │   └── 114-1_data.json
    └── with_outline/            # 完整綱要
        └── 114-1_data_with_outline.json
```

### 主要檔案說明

| 檔案 | 說明 | 速度 | 資料完整性 |
|------|------|------|-----------|
| `nycu_crawler.py` | 統一爬蟲程式，可選基本/完整模式 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| `NYCU_Crawler_Basic.ipynb` | Colab版 - 基本資訊 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| `NYCU_Crawler_WithOutline.ipynb` | Colab版 - 完整綱要 | ⭐⭐ | ⭐⭐⭐⭐⭐ |

## 🚀 快速開始

### 方法 1: 本地執行（推薦）

#### 1. 安裝依賴

```bash
pip install requests
```

#### 2. 選擇爬取模式

**基本資訊模式（快速）：**
```python
# 修改 nycu_crawler.py 的參數
YEAR = 114
SEMESTER = 1
FETCH_OUTLINE = False  # 只爬基本資訊
```

```bash
python nycu_crawler.py
```
- 輸出：`course_data/basic/114-1_data.json`
- 耗時：約 2-3 分鐘

**完整綱要模式（詳細）：**
```python
# 修改 nycu_crawler.py 的參數
YEAR = 114
SEMESTER = 1
FETCH_OUTLINE = True  # 爬取完整綱要
```

```bash
python nycu_crawler.py
```
- 輸出：`course_data/with_outline/114-1_data_with_outline.json`
- 耗時：約 40-60 分鐘

#### 3. 批次爬取多學期

使用批次工具一次爬取多學期基本資訊：

```bash
python crawl_basic_batch.py
```

### 方法 2: Google Colab（免安裝）

#### 基本資訊版
1. 開啟 `NYCU_Crawler_Basic.ipynb`
2. 上傳到 Google Colab
3. 依序執行所有儲存格
4. 下載生成的 JSON 檔案

#### 完整綱要版
1. 開啟 `NYCU_Crawler_WithOutline.ipynb`
2. 上傳到 Google Colab
3. 依序執行所有儲存格（需時約 40-60 分鐘）
4. 下載生成的 JSON 檔案

### 斷點續爬

如果爬取過程中斷（僅限完整綱要模式）：

1. 重新執行爬蟲程式
2. 系統會自動偵測檢查點檔案
3. 選擇 `y` 即可從中斷處繼續

## 📄 資料結構

### 基本資訊

```json
{
  "1141_515100": {
    "id": "515100",
    "name": "機率",
    "teacher": "陳志鴻",
    "credit": "3.00",
    "hours": "3.00",
    "time": ["T5", "T6", "F2"],
    "classroom": ["ED103[GF]"],
    "time-classroom": "T56F2-ED103[GF]",
    "num_limit": "55",
    "reg_num": "50",
    "english": true,
    "type": "選修",
    "brief": ["核心通識"]
  }
}
```

### 課程綱要（outline）

```json
{
  "outline": {
    "base": {
      "cos_name": "機率",
      "cos_eng_name": "Probability",
      "dep_name": "資訊工程學系",
      "cos_code": "EEEC10002"
    },
    "description": {
      "prerequisite": "微積分、線性代數、程式設計",
      "outline": "教授以微積分為基礎的機率論理論與應用...",
      "textbook": "Introduction to Probability, 2nd Edition",
      "exam_score": "作業: 30%, 期中考: 30%, 期末考: 40%",
      "teach_method": "講授與習作"
    },
    "weekly_schedule": [
      {
        "week_id": "1",
        "class_date": "2025-09-01(一),2025-09-03(三)",
        "class_data": "課程介紹、組合數學"
      }
    ],
    "unit_hours": [
      {
        "title": "機率基本概念",
        "content": "樣本空間、事件、機率公理",
        "hour_teaching": "3"
      }
    ]
  }
}
```

## 📈 效能分析

### 速度對比

| 模式 | 延遲/API | 單門課程 | 3000門課程預估 |
|------|---------|---------|---------------|
| 基本資訊 | N/A | 0.04秒 | 2-3 分鐘 |
| 完整綱要 | 0.2秒 | 1.0秒 | 50分鐘 |

### 網路負載說明

每門課程需要發送：
- 基本資訊：1 個 API 請求
- 課程綱要：4 個 API 請求（base, description, syllabuses, optional）

## ⚠️ 注意事項

### 1. 網路穩定性
- 建議在穩定的網路環境下執行
- 如遇中斷，可使用斷點續爬功能

### 2. 執行時間
- 基本資訊：約 2-3 分鐘
- 完整綱要：約 40-60 分鐘
- 建議在非高峰時段執行

### 3. 資料完整性
- 部分課程可能未填寫完整綱要資訊
- 系統會自動重試失敗的課程（最多3次）
- 最終成功率通常 > 98%

### 4. 伺服器友善
- 已加入適當延遲，避免對學校伺服器造成負擔
- 請勿修改延遲時間過短
- 請勿同時執行多個爬蟲程式

## 🛠️ 進階使用

### 只爬取特定系所

修改 `nycu_crawler.py` 中的 `get_cos()` 函數：

```python
target_deps = ["資訊工程學系", "電機工程學系"]

# 在系所迴圈中加入過濾
if deps[fdep] in target_deps:
    self.get_cos(fdep)
```

### 調整重試次數

在 `get_course_outline()` 函數中修改：

```python
def get_course_outline(self, cos_id, max_retries=5):  # 改為5次
```

### 修改檢查點保存頻率

在 `fetch_all_outlines()` 函數中修改：

```python
if count % 100 == 0:  # 改為每100門課保存
    self.save_checkpoint(checkpoint_file)
```

## 📊 資料用途

爬取的資料可用於：

- 📅 課程時間表視覺化
- 🔍 課程搜尋系統
- 📈 課程統計分析
- 🤖 課程推薦系統
- 📚 選課輔助工具
- 🎓 課程內容研究

## 🐛 問題排查

### 問題 1：爬取失敗率過高

**可能原因：**
- 網路不穩定
- 學校伺服器繁忙

**解決方法：**
1. 檢查網路連線
2. 增加延遲時間（修改 `time.sleep` 參數）
3. 使用斷點續爬功能重試失敗的課程

### 問題 2：執行速度太慢

**可能原因：**
- 網路速度慢
- 延遲設定過長

**解決方法：**
1. 確認網路速度
2. 適當減少延遲（但不建議低於 0.2 秒）

### 問題 3：中斷後無法續爬

**可能原因：**
- 檢查點檔案損壞

**解決方法：**
1. 刪除 `course_data/with_outline/*_checkpoint.json`
2. 重新執行爬蟲

## 📈 使用統計

### 資料覆蓋範圍
- **學期數**：5 個學期（112-1 ~ 114-1）
- **課程總數**：18,030 門（基本資訊）
- **完整綱要**：3,550 門（114-1）

### 效能指標
- **基本資訊爬取**：0.04 秒/門課
- **完整綱要爬取**：0.99 秒/門課
- **綱要成功率**：98.1%

## 🤝 貢獻指南

歡迎提交 Issue 和 Pull Request！

### 如何貢獻
1. Fork 本專案
2. 建立新分支 (`git checkout -b feature/amazing-feature`)
3. 提交變更 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 開啟 Pull Request

## ⚖️ 免責聲明

1. 本工具僅供**學習研究使用**
2. 請遵守學校相關規定，**合理使用學校資源**
3. 使用者需自行承擔使用本工具的一切責任
4. 請勿將爬取資料用於商業用途

## 📄 授權

本專案採用 MIT 授權條款，詳見 [LICENSE](LICENSE) 檔案。

## 📮 聯絡方式

如有問題或建議，歡迎：
- 提交 [Issue](../../issues)
- 發起 [Discussion](../../discussions)

---

**測試環境**：Python 3.7+  
**相容系統**：Windows / macOS / Linux / Google Colab  
**最後更新**：2025-01-19
