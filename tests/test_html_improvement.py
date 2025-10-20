#!/usr/bin/env python3
"""快速測試 HTML 解析改進效果"""
import sys
sys.path.insert(0, '.')
from nycu_crawler import NYCUCrawler
import json
import time

print("Testing HTML Parser Improvement")
print("=" * 70)

# 用 110-1 測試（有失敗的課程）
checkpoint_file = 'course_data/with_outline/110-1_checkpoint.json'

with open(checkpoint_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 只測試之前失敗的課程
failed_courses = [c for c in data['courses'] if not c.get('outline')]
test_sample = failed_courses[:30]  # 30 個課程快速測試

print(f"Testing on 30 previously failed courses from 110-1")
print("=" * 70)

crawler = NYCUCrawler(110, 1, fetch_outline=True)
success_count = 0
html_success = 0
start_time = time.time()

for idx, course in enumerate(test_sample):
    cos_id = course.get('id')
    outline = crawler.get_course_outline(cos_id)

    if outline:
        success_count += 1
        if outline.get('source') == 'html_parser':
            html_success += 1
            print(f"  {idx+1}. [HTML] {cos_id}")
        else:
            print(f"  {idx+1}. [JSON] {cos_id}")

elapsed = time.time() - start_time
success_rate = (success_count / len(test_sample) * 100)

print("\n" + "=" * 70)
print(f"Results:")
print(f"  Total Success: {success_count}/{len(test_sample)} ({success_rate:.1f}%)")
print(f"  From HTML Parser: {html_success}")
print(f"  From JSON API: {success_count - html_success}")
print(f"  Time: {elapsed:.1f}s")
print("=" * 70)

if success_rate > 17.9:  # 比較原有的 17.9%
    improvement = success_rate - 17.9
    print(f"Improvement: +{improvement:.1f}% (from 17.9%)")
else:
    print(f"No improvement from 17.9%")
