"""批次爬取多個學期的基本課程資訊"""
import sys
sys.path.insert(0, '.')
from nycu_crawler import NYCUCrawler

# 要爬取的學期列表
semesters = [
    (112, 1),
    (112, 2),
    (113, 1),
    (113, 2),
    (114, 1),
]

print("=" * 70)
print("批次爬取基本課程資訊")
print("=" * 70)
print(f"總共 {len(semesters)} 個學期")
print()

for i, (year, sem) in enumerate(semesters):
    print(f"\n[{i+1}/{len(semesters)}] 爬取 {year}-{sem} 學期...")
    print("-" * 70)
    
    crawler = NYCUCrawler(year, sem, fetch_outline=False)
    crawler.crawl()
    
    print()

print("\n" + "=" * 70)
print("批次爬取完成！")
print("=" * 70)
