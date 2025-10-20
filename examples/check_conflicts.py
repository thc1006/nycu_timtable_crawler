#!/usr/bin/env python3
"""
課程衝堂檢查範例
Example: Check for schedule conflicts between courses
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

def check_conflict(course1, course2):
    """檢查兩門課程是否有時間衝突"""
    for s1 in course1['schedule']:
        for s2 in course2['schedule']:
            # 同一天
            if s1['day'] == s2['day']:
                # 檢查時段是否重疊
                periods1 = set(s1['periods'])
                periods2 = set(s2['periods'])
                if periods1 & periods2:  # 有交集即衝突
                    return True, {
                        'day': s1['day_name'],
                        'periods': sorted(periods1 & periods2),
                        'time': f"{s1['time_start']}-{s2['time_end']}"
                    }
    return False, None

def find_conflicts_in_list(courses):
    """在課程清單中找出所有衝突"""
    conflicts = []
    for i, c1 in enumerate(courses):
        for c2 in courses[i+1:]:
            has_conflict, conflict_info = check_conflict(c1, c2)
            if has_conflict:
                conflicts.append({
                    'course1': c1,
                    'course2': c2,
                    'conflict': conflict_info
                })
    return conflicts

def get_course_by_id(data, course_id):
    """依課程代碼取得課程"""
    for course in data['courses']:
        if course['id'] == course_id:
            return course
    return None

def main():
    # 載入資料
    data = load_data("114-1")

    print("=" * 60)
    print("NYCU 課程衝堂檢查範例")
    print("=" * 60)

    # 範例 1: 檢查兩門特定課程是否衝突
    print("\n【範例 1】檢查兩門課程是否衝突")

    # 假設學生想選這些課程（請替換為實際的課程代碼）
    # 這裡我們用搜尋的方式找課程
    from search_courses import search_by_name

    calc_courses = search_by_name(data, "微積分")[:2]
    if len(calc_courses) >= 2:
        c1, c2 = calc_courses[0], calc_courses[1]

        print(f"\n課程 1: {c1['name']} - {c1['teacher']}")
        for s in c1['schedule']:
            print(f"  {s['day_name']} {s['time_start']}-{s['time_end']}")

        print(f"\n課程 2: {c2['name']} - {c2['teacher']}")
        for s in c2['schedule']:
            print(f"  {s['day_name']} {s['time_start']}-{s['time_end']}")

        has_conflict, conflict_info = check_conflict(c1, c2)
        if has_conflict:
            print(f"\n衝突！")
            print(f"衝突時間: {conflict_info['day']} 第 {conflict_info['periods']} 節")
        else:
            print(f"\n無衝突，可以同時選修")

    # 範例 2: 檢查一組課程清單中的所有衝突
    print("\n\n【範例 2】檢查選課清單中的所有衝突")

    # 建立一個模擬的選課清單
    my_courses = search_by_name(data, "程式")[:3]

    print(f"\n我的選課清單（共 {len(my_courses)} 門課）：")
    for i, course in enumerate(my_courses, 1):
        print(f"{i}. {course['name']} - {course['teacher']}")
        if course['schedule']:
            times = [f"{s['day_name']}{s['periods']}" for s in course['schedule']]
            print(f"   時間: {', '.join(times)}")

    conflicts = find_conflicts_in_list(my_courses)

    if conflicts:
        print(f"\n發現 {len(conflicts)} 個衝突：")
        for i, conflict in enumerate(conflicts, 1):
            print(f"\n衝突 {i}:")
            print(f"  課程 1: {conflict['course1']['name']}")
            print(f"  課程 2: {conflict['course2']['name']}")
            print(f"  衝突時間: {conflict['conflict']['day']} 第 {conflict['conflict']['periods']} 節")
    else:
        print(f"\n沒有衝突！所有課程時間都不重疊")

    # 範例 3: 找出與特定課程不衝突的其他課程
    print("\n\n【範例 3】找出與特定課程不衝突的課程")

    target_course = my_courses[0] if my_courses else None
    if target_course:
        print(f"\n基準課程: {target_course['name']}")

        # 搜尋其他課程
        other_courses = search_by_name(data, "設計")[:10]
        no_conflict_courses = []

        for course in other_courses:
            has_conflict, _ = check_conflict(target_course, course)
            if not has_conflict and course['id'] != target_course['id']:
                no_conflict_courses.append(course)

        print(f"\n找到 {len(no_conflict_courses)} 門不衝突的「設計」相關課程：")
        for course in no_conflict_courses[:5]:  # 只顯示前 5 筆
            print(f"  - {course['name']} ({course['teacher']})")
            if course['schedule']:
                times = [f"{s['day_name']}{s['periods']}" for s in course['schedule']]
                print(f"    時間: {', '.join(times)}")

if __name__ == "__main__":
    main()
