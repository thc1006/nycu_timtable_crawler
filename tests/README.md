# 測試檔案 (Tests)

此目錄包含所有測試和驗證指令稿。

## 檔案說明

- `test_*.py` - 各種功能測試
- `quick_check.py` - 快速檢查工具
- `analyze_failures.py` - 失敗分析工具

## 使用方式

```bash
# 執行特定測試
python tests/test_improved_crawler.py

# 快速檢查
python tests/quick_check.py

# 分析失敗課程
python tests/analyze_failures.py
```

## 注意

這些檔案主要用於開發和除錯，生產環境應使用 `scripts/` 目錄中的檔案。
