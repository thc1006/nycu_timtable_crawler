#!/usr/bin/env python3
"""
課程搜尋範例
Example: Search courses by various criteria
"""
import json
import sys

def load_data(semester="114-1"):
    """載入課程資料"""
    filename = f"../course_data/basic/{semester}_data.json"
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"錯誤：找不到 {filename}")
        print(f"請先執行爬蟲取得 {semester} 學期的資料")
        sys.exit(1)

def search_by_name(data, keyword):
    """依課程名稱搜尋"""
    results = [c for c in data['courses'] if keyword in c['name']]
    return results

def search_by_teacher(data, teacher_name):
    """依教師姓名搜尋"""
    results = [c for c in data['courses'] if teacher_name in c['teacher']]
    return results

def search_by_credit(data, credits):
    """依學分數搜尋"""
    results = [c for c in data['courses'] if c['credit'] == credits]
    return results

def search_by_day(data, day):
    """依星期搜尋（1=Monday, 2=Tuesday, ...）"""
    results = []
    for c in data['courses']:
        if any(s['day'] == day for s in c['schedule']):
            results.append(c)
    return results

def print_course_info(course):
    """印出課程資訊"""
    print(f"\n課程名稱: {course['name']}")
    print(f"授課教師: {course['teacher']}")
    print(f"學分: {course['credit']} | 時數: {course['hours']}")
    print(f"類型: {course['type']}")
    print(f"人數: {course['enrollment']['current']}/{course['enrollment']['limit']}")

    if course['schedule']:
        print("上課時間:")
        for s in course['schedule']:
            print(f"  {s['day_name']} {s['time_start']}-{s['time_end']} @ {s['classroom']}")

    if course['english_taught']:
        print("🌐 英文授課")

def main():
    # 載入資料
    data = load_data("114-1")

    print("=" * 60)
    print("NYCU 課程搜尋範例")
    print("=" * 60)

    # 範例 1: 搜尋「微積分」課程
    print("\n【範例 1】搜尋課程名稱包含「微積分」")
    results = search_by_name(data, "微積分")
    print(f"找到 {len(results)} 門課程")
    for course in results[:3]:  # 只顯示前 3 筆
        print_course_info(course)

    # 範例 2: 搜尋特定老師的課
    print("\n\n【範例 2】搜尋特定教師的課程")
    results = search_by_teacher(data, "陳")  # 搜尋姓陳的老師
    print(f"找到 {len(results)} 門課程")

    # 範例 3: 搜尋 3 學分的課
    print("\n\n【範例 3】搜尋 3 學分課程")
    results = search_by_credit(data, 3.0)
    print(f"找到 {len(results)} 門課程")

    # 範例 4: 搜尋星期一有課的課程
    print("\n\n【範例 4】搜尋星期一有課的課程")
    results = search_by_day(data, 1)  # 1 = Monday
    print(f"找到 {len(results)} 門課程")
    for course in results[:2]:
        print_course_info(course)

if __name__ == "__main__":
    main()
