"""
批次爬取多個學期的完整課程綱要（多執行緒版本）

使用方式：
    python crawl_outline_batch_multithreaded.py

功能：
    使用多執行緒同時爬取多個學期的完整課程綱要
    預設使用 4 個執行緒

注意：
    完整綱要爬取需要較長時間（每學期約 50-60 分鐘）
    使用 4 執行緒約可在 2-3 小時內完成 9 個學期
"""
import sys
sys.path.insert(0, '.')
from nycu_crawler import NYCUCrawler
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

# ============= 參數設定 =============
NUM_THREADS = 4  # 執行緒數量（建議 3-4，避免對伺服器負擔過大）
# ===================================

# 要爬取的學期列表
# 注意：112-1, 112-2, 113-1, 113-2 由 crawl_remaining_semesters.py 處理
semesters = [
    (110, 1),  # 110 學年度上學期
    (110, 2),  # 110 學年度下學期
    (111, 1),  # 111 學年度上學期
    (111, 2),  # 111 學年度下學期
    (114, 1),  # 114 學年度上學期
]

def crawl_semester_outline(year, sem, index, total):
    """爬取單一學期的完整課程綱要"""
    try:
        print(f"\n[Thread {index+1}/{total}] Starting {year}-{sem} (with outline)")
        start = datetime.now()

        crawler = NYCUCrawler(year, sem, fetch_outline=True)
        crawler.crawl()

        elapsed = datetime.now() - start
        print(f"[Thread {index+1}/{total}] Finished {year}-{sem} in {elapsed}")
        return (year, sem, True, None)
    except Exception as e:
        print(f"[Thread {index+1}/{total}] Failed {year}-{sem}: {str(e)}")
        return (year, sem, False, str(e))

print("=" * 70)
print("NYCU Course Crawler v4.0 - Multithreaded Batch Crawl (WITH OUTLINE)")
print("=" * 70)
print(f"Total semesters: {len(semesters)}")
print(f"Threads: {NUM_THREADS}")
print(f"Mode: Complete outline (with syllabus, grading, weekly schedule)")
print(f"Format: Array format v2.0")
print("=" * 70)
print()
print("WARNING: This will take approximately 2-3 hours!")
print("Each semester takes about 50-60 minutes.")
print()
print("Starting automatically...")

start_time = datetime.now()

# 使用 ThreadPoolExecutor 進行多執行緒爬取
results = []
with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
    # 提交所有任務
    futures = {
        executor.submit(crawl_semester_outline, year, sem, i, len(semesters)): (year, sem)
        for i, (year, sem) in enumerate(semesters)
    }

    # 等待完成
    for future in as_completed(futures):
        result = future.result()
        results.append(result)

        # 顯示進度
        completed = len(results)
        print(f"\n>>> Progress: {completed}/{len(semesters)} semesters completed")

end_time = datetime.now()
elapsed = end_time - start_time

# 統計結果
successful = [r for r in results if r[2]]
failed = [r for r in results if not r[2]]

print("\n" + "=" * 70)
print("Batch crawl completed!")
print("=" * 70)
print(f"Total time: {elapsed}")
print(f"Average per semester: {elapsed.total_seconds()/len(semesters)/60:.1f} minutes")
print(f"Successful: {len(successful)}/{len(semesters)} semesters")
if failed:
    print(f"Failed: {len(failed)} semesters")
    for year, sem, _, error in failed:
        print(f"  - {year}-{sem}: {error}")
print()
print("Output directory: course_data/with_outline/")
print()
print("Successfully crawled:")
for year, sem, _, _ in successful:
    print(f"  + {year}-{sem}_data_with_outline.json")
print("=" * 70)
