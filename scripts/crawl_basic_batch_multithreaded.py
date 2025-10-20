"""
批次爬取多個學期的基本課程資訊（多執行緒版本）

使用方式：
    python crawl_basic_batch_multithreaded.py

功能：
    使用多執行緒同時爬取多個學期的課程資訊
    預設使用 4 個執行緒，可提升約 3-4 倍速度
"""
import sys
sys.path.insert(0, '.')
from nycu_crawler import NYCUCrawler
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

# ============= 參數設定 =============
NUM_THREADS = 4  # 執行緒數量（建議 4-8）
# ===================================

# 要爬取的學期列表
semesters = [
    (110, 1),  # 110 學年度上學期
    (110, 2),  # 110 學年度下學期
    (111, 1),  # 111 學年度上學期
    (111, 2),  # 111 學年度下學期
    (112, 1),  # 112 學年度上學期
    (112, 2),  # 112 學年度下學期
    (113, 1),  # 113 學年度上學期
    (113, 2),  # 113 學年度下學期
    (114, 1),  # 114 學年度上學期
]

def crawl_semester(year, sem, index, total):
    """爬取單一學期的課程資訊"""
    try:
        print(f"\n[執行緒 {index+1}/{total}] 開始爬取 {year}-{sem}")
        crawler = NYCUCrawler(year, sem, fetch_outline=False)
        crawler.crawl()
        print(f"[執行緒 {index+1}/{total}] ✓ {year}-{sem} 完成")
        return (year, sem, True, None)
    except Exception as e:
        print(f"[執行緒 {index+1}/{total}] ✗ {year}-{sem} 失敗: {str(e)}")
        return (year, sem, False, str(e))

print("=" * 70)
print("NYCU 課程爬蟲 v4.0 - 多執行緒批次爬取模式")
print("=" * 70)
print(f"總共 {len(semesters)} 個學期")
print(f"執行緒數量: {NUM_THREADS}")
print(f"模式: 基本資訊（不含課程綱要）")
print(f"格式: 陣列格式 v2.0")
print("=" * 70)
print()

start_time = datetime.now()

# 使用 ThreadPoolExecutor 進行多執行緒爬取
results = []
with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
    # 提交所有任務
    futures = {
        executor.submit(crawl_semester, year, sem, i, len(semesters)): (year, sem)
        for i, (year, sem) in enumerate(semesters)
    }

    # 等待完成
    for future in as_completed(futures):
        result = future.result()
        results.append(result)

end_time = datetime.now()
elapsed = end_time - start_time

# 統計結果
successful = [r for r in results if r[2]]
failed = [r for r in results if not r[2]]

print("\n" + "=" * 70)
print("批次爬取完成！")
print("=" * 70)
print(f"總花費時間: {elapsed}")
print(f"成功: {len(successful)}/{len(semesters)} 個學期")
if failed:
    print(f"失敗: {len(failed)} 個學期")
    for year, sem, _, error in failed:
        print(f"  - {year}-{sem}: {error}")
print()
print("輸出目錄: course_data/basic/")
print()
print("成功爬取的檔案:")
for year, sem, _, _ in successful:
    print(f"  ✓ {year}-{sem}_data.json")
print("=" * 70)
print(f"\n平均每學期: {elapsed.total_seconds()/len(semesters):.1f} 秒")
print(f"速度提升: 約 {NUM_THREADS}x (相比單執行緒)")
