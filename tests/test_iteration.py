#!/usr/bin/env python3
"""
自動化迭代測試框架 - 測試成功率改進
目標：快速測試單個學期，評估改進效果
"""
import sys
sys.path.insert(0, '.')
from nycu_crawler import NYCUCrawler
import time
import json
import os

def test_semester(year, sem, sample_size=300, iteration_num=0):
    """快速測試單個學期的成功率"""

    semester_name = f"{year}-{sem}"
    checkpoint_file = f"course_data/with_outline/{semester_name}_checkpoint.json"

    print(f"\n[Iteration {iteration_num}] Testing {semester_name} ({sample_size} courses)")
    print("=" * 70)

    start_time = time.time()

    # 建立爬蟲
    crawler = NYCUCrawler(year, sem, fetch_outline=True)

    # 如果有 checkpoint，載入已爬取的課程
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, 'r', encoding='utf-8') as f:
            checkpoint = json.load(f)

        # 只測試沒有綱要的課程中的一部分
        failed_courses = [c for c in checkpoint['courses'] if not c.get('outline')]
        test_courses = failed_courses[:sample_size]

        print(f"Testing {len(test_courses)} failed courses (out of {len(failed_courses)} failed)")

        success_count = 0
        for idx, course in enumerate(test_courses):
            cos_id = course.get('id')
            outline = crawler.get_course_outline(cos_id)

            if outline:
                success_count += 1

            if (idx + 1) % 50 == 0:
                rate = (success_count / (idx + 1) * 100)
                elapsed = time.time() - start_time
                rate_per_sec = (idx + 1) / elapsed
                print(f"  Progress: {idx+1}/{len(test_courses)} | Success: {success_count}/{idx+1} ({rate:.1f}%) | Speed: {rate_per_sec:.2f} courses/sec")

        elapsed = time.time() - start_time
        success_rate = (success_count / len(test_courses) * 100) if test_courses else 0

        print("\n" + "=" * 70)
        print(f"[Iteration {iteration_num}] Results:")
        print(f"  Total Tested: {len(test_courses)}")
        print(f"  Successful: {success_count}")
        print(f"  Success Rate: {success_rate:.1f}%")
        print(f"  Total Time: {elapsed:.1f} seconds")
        print(f"  Speed: {len(test_courses)/elapsed:.2f} courses/sec")
        print("=" * 70)

        return success_rate
    else:
        print(f"No checkpoint found for {semester_name}")
        return 0

def main():
    print("=" * 70)
    print("Automated Iteration Testing - Success Rate Improvement")
    print("=" * 70)

    # Test on 113-1 (hasn't been crawled yet)
    # Or use 110-1 which is mostly failed

    for iteration in range(1, 3):  # Test first 2 iterations
        print(f"\n[ITERATION {iteration}]")
        success_rate = test_semester(110, 1, sample_size=100, iteration_num=iteration)

        if success_rate >= 80:
            print(f"\nSuccess! Reached 80% target on iteration {iteration}")
            break

        input(f"\nPress Enter to continue to iteration {iteration+1}...")

if __name__ == "__main__":
    main()
