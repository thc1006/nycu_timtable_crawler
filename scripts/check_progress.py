"""
檢查完整綱要爬取進度

使用方式：
    python check_progress.py
"""
import os
import json
from datetime import datetime

print("=" * 70)
print("NYCU 完整綱要爬取進度查詢")
print("=" * 70)
print()

semesters = [
    (110, 1), (110, 2),
    (111, 1), (111, 2),
    (112, 1), (112, 2),
    (113, 1), (113, 2),
    (114, 1)
]

completed = []
in_progress = []
not_started = []

for year, sem in semesters:
    data_file = f"course_data/with_outline/{year}-{sem}_data_with_outline.json"
    checkpoint_file = f"course_data/with_outline/{year}-{sem}_checkpoint.json"

    if os.path.exists(data_file):
        # 已完成
        file_size = os.path.getsize(data_file) / 1024 / 1024  # MB
        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                total = data['metadata']['total_courses']
                completed.append((year, sem, total, file_size))
        except:
            completed.append((year, sem, '?', file_size))

    elif os.path.exists(checkpoint_file):
        # 進行中
        try:
            with open(checkpoint_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                total = data['metadata']['total_courses']
                courses_with_outline = sum(1 for c in data['courses'] if 'outline' in c)
                progress = (courses_with_outline / total * 100) if total > 0 else 0
                in_progress.append((year, sem, courses_with_outline, total, progress))
        except:
            in_progress.append((year, sem, '?', '?', 0))

    else:
        # 未開始
        not_started.append((year, sem))

print(f"已完成: {len(completed)}/{len(semesters)}")
if completed:
    print()
    for year, sem, total, size in completed:
        print(f"  [{year}-{sem}] {total} 門課程, {size:.1f} MB")

print(f"\n進行中: {len(in_progress)}/{len(semesters)}")
if in_progress:
    print()
    for year, sem, done, total, progress in in_progress:
        print(f"  [{year}-{sem}] {done}/{total} ({progress:.1f}%)")

print(f"\n未開始: {len(not_started)}/{len(semesters)}")
if not_started:
    print()
    for year, sem in not_started:
        print(f"  [{year}-{sem}]")

print()
print("=" * 70)

# 檢查日誌
log_file = "outline_batch_all.log"
if os.path.exists(log_file):
    print(f"\n最新日誌 (最後 20 行):")
    print("=" * 70)
    with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        for line in lines[-20:]:
            print(line.rstrip())
