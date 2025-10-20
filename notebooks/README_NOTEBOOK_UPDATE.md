# Notebook 更新說明

## 狀態

Jupyter Notebook 檔案（`NYCU_Crawler_Basic.ipynb` 和 `NYCU_Crawler_WithOutline.ipynb`）目前使用舊版爬蟲程式碼（v3.0）。

## 如何使用新版爬蟲（v4.0）

### 方法一：使用主要爬蟲程式（推薦）

直接使用專案根目錄的 `nycu_crawler.py`，它已更新為 v4.0，包含：
- ✅ 新資料格式 v2.0（陣列格式）
- ✅ 結構化時間/教室解析
- ✅ 數字型別標準化
- ✅ 完整 metadata

```python
# 在 Colab 中
!git clone https://github.com/YOUR_REPO/nycu_timtable_crawler.git
%cd nycu_timtable_crawler

# 安裝套件
!pip install requests

# 執行爬蟲
!python nycu_crawler.py

# 下載結果
from google.colab import files
files.download('course_data/basic/114-1_data.json')
```

### 方法二：複製主程式碼到 Notebook

如果需要在 Notebook 中使用，請參考 `nycu_crawler.py` 的最新程式碼。

## 主要變更

### 1. 資料結構

**舊格式（物件）**：
```json
{
  "1141_515002": {
    "id": "515002",
    "credit": "3.00",  // 字串
    "time": ["M3", "M4"]  // 簡單陣列
  }
}
```

**新格式（陣列）**：
```json
{
  "metadata": { "semester": "114-1", "total_courses": 8028 },
  "courses": [
    {
      "id": "515002",
      "credit": 3.0,  // 數字
      "schedule": [  // 結構化
        {
          "day": 1,
          "day_name": "Monday",
          "periods": [3, 4],
          "time_start": "10:10",
          "time_end": "12:00",
          "classroom": "EE102"
        }
      ]
    }
  ]
}
```

### 2. 新增功能

- **結構化時間解析**：`parse_schedule_structured()` 方法
- **Metadata**：`create_metadata()` 方法
- **改進的綱要解析**：`parse_outline_weekly_schedule()` 和 `parse_outline_unit_hours()`

## 自行更新 Notebook（進階）

如果需要自行更新 Notebook 檔案：

1. 開啟 `.ipynb` 檔案（JSON 格式）
2. 找到包含 `NYCUCrawler` 類別定義的 cell
3. 複製 `nycu_crawler.py` 的最新程式碼
4. 更新該 cell 的 `source` 欄位
5. 儲存檔案

## 快速測試

在 Colab 中測試新版爬蟲：

```python
!wget https://raw.githubusercontent.com/YOUR_REPO/nycu_timtable_crawler/main/nycu_crawler.py
!python nycu_crawler.py
```

---

**更新日期**: 2025-01-19
**爬蟲版本**: v4.0
**資料格式**: v2.0
