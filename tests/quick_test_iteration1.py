#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')
from nycu_crawler import NYCUCrawler
import json
import time

try:
    checkpoint_file = 'course_data/with_outline/110-1_checkpoint.json'
    with open(checkpoint_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    failed = [c for c in data['courses'] if not c.get('outline')]
    test_courses = failed[:50]

    print("ITERATION 1 - Quick Test (50 courses)")
    print("=" * 60)

    crawler = NYCUCrawler(110, 1, fetch_outline=True)
    success_count = 0
    start = time.time()

    for idx, course in enumerate(test_courses):
        cos_id = course.get('id')
        outline = crawler.get_course_outline(cos_id)
        if outline:
            success_count += 1

        if (idx + 1) % 10 == 0:
            rate = success_count / (idx + 1) * 100
            elapsed = time.time() - start
            print(f'{idx+1}/50: {success_count} success ({rate:.1f}%)')

    elapsed = time.time() - start
    final_rate = (success_count / len(test_courses) * 100)

    print("=" * 60)
    print(f'Result: {success_count}/{len(test_courses)} ({final_rate:.1f}%)')
    print(f'Time: {elapsed:.1f}s')

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
