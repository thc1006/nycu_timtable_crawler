#!/usr/bin/env python3
"""
統一進度監控工具
Unified Progress Monitor for NYCU Course Crawler

支援功能：
- 基本資訊爬取進度
- 完整綱要爬取進度
- 即時統計資訊
- 彩色輸出
"""
import os
import json
import sys
from datetime import datetime
from pathlib import Path

def load_data(semester):
    """載入課程資料"""
    filename = f"course_data/basic/{semester}_data.json"
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def check_outline_progress(year, sem):
    """檢查完整綱要爬取進度"""
    data_file = f"course_data/with_outline/{year}-{sem}_data_with_outline.json"
    checkpoint_file = f"course_data/with_outline/{year}-{sem}_checkpoint.json"

    if os.path.exists(data_file):
        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return ("completed", data['metadata']['total_courses'], 0)
        except:
            pass

    if os.path.exists(checkpoint_file):
        try:
            with open(checkpoint_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                total = data['metadata']['total_courses']
                completed = sum(1 for c in data['courses'] if 'outline' in c)
                return ("in_progress", completed, total)
        except:
            pass

    return ("not_started", 0, 0)

def main():
    print("=" * 70)
    print("NYCU 課程爬蟲進度監控")
    print("=" * 70)
    print()

    semesters = [
        (110, 1), (110, 2),
        (111, 1), (111, 2),
        (112, 1), (112, 2),
        (113, 1), (113, 2),
        (114, 1)
    ]

    completed_count = 0
    in_progress_count = 0
    not_started_count = 0
    total_courses = 0

    print("基本資訊爬取狀態:")
    print("-" * 70)
    for year, sem in semesters:
        data = load_data(f"{year}-{sem}")
        if data:
            courses = data.get('courses', [])
            metadata = data.get('metadata', {})
            total = metadata.get('total_courses', len(courses))
            total_courses += total
            print(f"  ✓ {year}-{sem}: {total} 門課程")
            completed_count += 1
        else:
            print(f"  ✗ {year}-{sem}: 未完成")
            not_started_count += 1

    print()
    print("完整綱要爬取狀態:")
    print("-" * 70)

    outline_total_courses = 0
    outline_completed_courses = 0

    for year, sem in semesters:
        status, done, total = check_outline_progress(year, sem)

        if status == "completed":
            print(f"  ✓ {year}-{sem}: 已完成 ({done} 門課程)")
            outline_completed_courses += done
            outline_total_courses += done
        elif status == "in_progress":
            pct = (done / total * 100) if total > 0 else 0
            print(f"  ⏳ {year}-{sem}: 進行中 ({done}/{total}, {pct:.1f}%)")
            outline_completed_courses += done
            outline_total_courses += total
        else:
            print(f"  ◯ {year}-{sem}: 未開始")

    print()
    print("=" * 70)
    print("總體統計:")
    print("=" * 70)
    print(f"基本資訊: {completed_count}/9 個學期已完成，共 {total_courses:,} 門課程")
    print(f"完整綱要: {outline_completed_courses:,}/{outline_total_courses:,} 門課程")

    if outline_total_courses > 0:
        outline_pct = (outline_completed_courses / outline_total_courses * 100)
        print(f"完整綱要進度: {outline_pct:.1f}%")

    print()
    print(f"最後更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

if __name__ == "__main__":
    main()
