#!/usr/bin/env python3
"""
单线程测试 113-1
"""
import sys
sys.path.insert(0, '.')
from nycu_crawler import NYCUCrawler
import time
from datetime import datetime

print("=" * 80)
print("SINGLE-THREADED TEST - 113-1 Only")
print(f"Start: {datetime.now().strftime('%H:%M:%S')}")
print("=" * 80)

start_time = time.time()

try:
    crawler = NYCUCrawler(113, 1, fetch_outline=True)
    print("\nCrawling 113-1...")
    crawler.crawl()

    elapsed = time.time() - start_time
    minutes = int(elapsed // 60)
    seconds = int(elapsed % 60)

    total = len(crawler.courses_list)
    success = crawler.stats['outline_success']
    failed = crawler.stats['outline_fail']
    rate = (success / total * 100) if total > 0 else 0

    print("\n" + "=" * 80)
    print("RESULT:")
    print("=" * 80)
    print(f"Total Courses: {total}")
    print(f"Success: {success} ({rate:.1f}%)")
    print(f"Failed: {failed}")
    print(f"Time: {minutes}m {seconds}s")
    print(f"Speed: {total/elapsed:.1f} courses/sec")
    print("=" * 80)

except Exception as e:
    print(f"\nERROR: {e}")
    print("=" * 80)
