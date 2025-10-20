#!/usr/bin/env python3
"""
課程統計分析範例
Example: Analyze course statistics
"""
import json
from collections import Counter

def load_data(semester="114-1"):
    """載入課程資料"""
    filename = f"../course_data/basic/{semester}_data.json"
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def analyze_courses(data):
    """分析課程統計"""
    courses = data['courses']

    print("=" * 60)
    print(f"NYCU {data['metadata']['semester']} 課程統計分析")
    print("=" * 60)

    # 基本統計
    print(f"\n【基本統計】")
    print(f"總課程數: {len(courses)}")
    print(f"資料格式版本: {data['metadata']['data_format_version']}")
    print(f"最後更新: {data['metadata']['last_updated']}")

    # 學分分布
    print(f"\n【學分分布】")
    credit_counter = Counter(c['credit'] for c in courses)
    for credit, count in sorted(credit_counter.items()):
        percentage = count / len(courses) * 100
        bar = "█" * int(percentage / 2)
        print(f"{credit:>4.1f} 學分: {count:>4} 門 ({percentage:>5.1f}%) {bar}")

    # 課程類型
    print(f"\n【課程類型】")
    type_counter = Counter(c['type'] for c in courses)
    for ctype, count in type_counter.most_common():
        percentage = count / len(courses) * 100
        print(f"{ctype:>6}: {count:>4} 門 ({percentage:>5.1f}%)")

    # 英文授課
    print(f"\n【授課語言】")
    english_count = sum(1 for c in courses if c['english_taught'])
    chinese_count = len(courses) - english_count
    print(f"中文授課: {chinese_count:>4} 門 ({chinese_count/len(courses)*100:>5.1f}%)")
    print(f"英文授課: {english_count:>4} 門 ({english_count/len(courses)*100:>5.1f}%)")

    # 熱門上課時段
    print(f"\n【熱門上課時段】")
    day_counter = Counter()
    for c in courses:
        for s in c['schedule']:
            day_counter[s['day_name']] += 1

    for day, count in day_counter.most_common():
        print(f"{day:>10}: {count:>4} 堂課")

    # 選課熱門度（額滿程度）
    print(f"\n【選課熱門度】")
    full_courses = []
    for c in courses:
        if c['enrollment']['limit'] > 0:
            ratio = c['enrollment']['current'] / c['enrollment']['limit']
            if ratio >= 1.0:
                full_courses.append(c)

    print(f"已額滿課程: {len(full_courses)} 門")

    # 最熱門的課程（選課人數最多）
    print(f"\n【選課人數最多的課程 TOP 5】")
    top_courses = sorted(courses, key=lambda x: x['enrollment']['current'], reverse=True)[:5]
    for i, c in enumerate(top_courses, 1):
        print(f"{i}. {c['name']} - {c['teacher']}")
        print(f"   {c['enrollment']['current']}/{c['enrollment']['limit']} 人")

def main():
    data = load_data("114-1")
    analyze_courses(data)

if __name__ == "__main__":
    main()
