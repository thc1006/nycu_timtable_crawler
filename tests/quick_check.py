#!/usr/bin/env python3
"""快速檢查爬取進度"""
import os
import json
from datetime import datetime

# 檢查 checkpoint 檔案
semesters_all = [
    (110, 1), (110, 2), (111, 1), (111, 2),
    (112, 1), (112, 2), (113, 1), (113, 2), (114, 1)
]

print("=" * 70)
print("NYCU 課程爬蟲 - 即時進度檢查")
print(f"檢查時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 70)

for year, sem in semesters_all:
    semester_name = f"{year}-{sem}"
    checkpoint_file = f"course_data/with_outline/{semester_name}_checkpoint.json"
    data_file = f"course_data/with_outline/{semester_name}_data_with_outline.json"

    if os.path.exists(data_file):
        # 已完成
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            total = data['metadata']['total_courses']
        print(f"[完成] {semester_name}: {total} 門課程 ✓")
    elif os.path.exists(checkpoint_file):
        # 進行中
        try:
            with open(checkpoint_file, 'r', encoding='utf-8') as f:
                checkpoint = json.load(f)
                completed = len(checkpoint['courses'])
                total = checkpoint['metadata']['total_courses']
                percentage = (completed / total * 100) if total > 0 else 0

                # 計算成功/失敗數
                success = sum(1 for c in checkpoint['courses'] if c.get('outline'))
                failed = completed - success

            print(f"[進行中] {semester_name}: {completed}/{total} ({percentage:.1f}%) | 成功: {success}, 失敗: {failed}")
        except Exception as e:
            print(f"[錯誤] {semester_name}: {e}")
    else:
        print(f"[未開始] {semester_name}")

print("=" * 70)
