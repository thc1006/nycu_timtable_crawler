#!/usr/bin/env python3
"""
分析失敗的課程綱要 - 檢查為什麼失敗
"""
import json
import os
from collections import defaultdict

def analyze_failed_courses():
    """分析所有失敗的課程"""

    semesters = [
        (110, 1), (110, 2), (111, 1), (111, 2),
        (112, 1), (112, 2), (113, 2), (114, 1)
    ]

    print("=" * 70)
    print("Failed Courses Analysis")
    print("=" * 70)

    all_failed = []

    for year, sem in semesters:
        semester_name = f"{year}-{sem}"
        checkpoint_file = f"course_data/with_outline/{semester_name}_checkpoint.json"

        if not os.path.exists(checkpoint_file):
            continue

        try:
            with open(checkpoint_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Get failed courses (no outline)
            failed = [c for c in data['courses'] if not c.get('outline')]

            for course in failed[:3]:  # Sample 3 from each semester
                all_failed.append({
                    'semester': semester_name,
                    'cos_id': course.get('cos_id'),
                    'cos_name': course.get('cos_name'),
                    'outline': course.get('outline')
                })

            print(f"\n[{semester_name}] Total failed: {len(failed)}/{len(data['courses'])}")

            # Show sample
            for i, course in enumerate(failed[:3]):
                print(f"  Sample {i+1}: ID={course.get('cos_id')} | {course.get('cos_name', 'N/A')[:40]}")

        except Exception as e:
            print(f"Error reading {semester_name}: {e}")

    print("\n" + "=" * 70)
    print(f"Total failed samples collected: {len(all_failed)}")
    print("=" * 70)

    # Save for further testing
    with open('failed_samples.json', 'w', encoding='utf-8') as f:
        json.dump(all_failed, f, ensure_ascii=False, indent=2)

    return all_failed

if __name__ == "__main__":
    analyze_failed_courses()
