#!/usr/bin/env python3
"""
使用優化後的爬蟲重新爬取所有學期
目標：至少 90% 成功率
"""
import sys
sys.path.insert(0, '.')
from nycu_crawler import NYCUCrawler
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from datetime import datetime

# 所有學期
ALL_SEMESTERS = [
    (110, 1), (110, 2),
    (111, 1), (111, 2),
    (112, 1), (112, 2),
    (113, 1), (113, 2),
    (114, 1),
]

NUM_THREADS = 4

def crawl_semester_with_stats(year, sem, index, total):
    """爬取單一學期並返回詳細統計"""
    semester_name = f"{year}-{sem}"
    try:
        print(f"\n[{index+1}/{total}] 開始爬取 {semester_name}（優化版）")
        start_time = time.time()

        crawler = NYCUCrawler(year, sem, fetch_outline=True)
        crawler.crawl()

        elapsed = time.time() - start_time
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)

        total_courses = len(crawler.courses_list)
        success = crawler.stats['outline_success']
        failed = crawler.stats['outline_fail']
        success_rate = (success / total_courses * 100) if total_courses > 0 else 0

        print(f"\n[{index+1}/{total}] {semester_name} 完成！")
        print(f"  耗時: {minutes}分{seconds}秒")
        print(f"  總課程: {total_courses}")
        print(f"  成功: {success} ({success_rate:.1f}%)")
        print(f"  失敗: {failed}")

        return {
            'semester': semester_name,
            'year': year,
            'sem': sem,
            'success': True,
            'total_courses': total_courses,
            'outline_success': success,
            'outline_fail': failed,
            'success_rate': success_rate,
            'elapsed_minutes': minutes + seconds / 60
        }

    except Exception as e:
        print(f"\n[{index+1}/{total}] {semester_name} 失敗：{str(e)}")
        return {
            'semester': semester_name,
            'success': False,
            'error': str(e)
        }

def main():
    print("=" * 70)
    print("NYCU 課程爬蟲 - 全面重新爬取（優化版）")
    print("=" * 70)
    print(f"目標學期：{len(ALL_SEMESTERS)} 個")
    print(f"執行緒數：{NUM_THREADS}")
    print(f"目標成功率：>= 90%")
    print("=" * 70)
    print("\n優化特性：")
    print("  [v] 適應性錯誤處理（處理 API 返回 False/None）")
    print("  [v] 部分成功也算成功（任一 API 成功即可）")
    print("  [v] 速度提升 4 倍（延遲 0.2s -> 0.05s）")
    print("  [v] 靜默失敗（減少無用警告）")
    print("=" * 70)

    overall_start = time.time()

    # 使用多執行緒並行爬取
    results = []
    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        futures = {
            executor.submit(crawl_semester_with_stats, year, sem, i, len(ALL_SEMESTERS)): (year, sem)
            for i, (year, sem) in enumerate(ALL_SEMESTERS)
        }

        for future in as_completed(futures):
            year, sem = futures[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print(f"\n執行緒錯誤 {year}-{sem}: {e}")
                results.append({
                    'semester': f"{year}-{sem}",
                    'success': False,
                    'error': str(e)
                })

    # 總結報告
    overall_elapsed = time.time() - overall_start
    overall_minutes = int(overall_elapsed // 60)
    overall_seconds = int(overall_elapsed % 60)

    print("\n" + "=" * 70)
    print("全部爬取完成 - 詳細統計")
    print("=" * 70)

    success_semesters = [r for r in results if r.get('success')]
    total_courses_all = sum(r.get('total_courses', 0) for r in success_semesters)
    total_outline_success = sum(r.get('outline_success', 0) for r in success_semesters)
    total_outline_fail = sum(r.get('outline_fail', 0) for r in success_semesters)

    overall_success_rate = (total_outline_success / total_courses_all * 100) if total_courses_all > 0 else 0

    print(f"\n成功學期：{len(success_semesters)}/{len(ALL_SEMESTERS)}")
    print(f"總課程數：{total_courses_all}")
    print(f"綱要成功：{total_outline_success}")
    print(f"綱要失敗：{total_outline_fail}")
    print(f"\n整體成功率：{overall_success_rate:.1f}%")

    if overall_success_rate >= 90:
        print("達到目標！成功率 >= 90%")
    else:
        print(f"未達目標，需要進一步優化")

    print(f"\n總耗時：{overall_minutes} 分 {overall_seconds} 秒")

    # 各學期詳細資料
    print("\n" + "-" * 70)
    print("各學期詳細統計：")
    print("-" * 70)
    for r in sorted(success_semesters, key=lambda x: x['semester']):
        status = "[OK]" if r['success_rate'] >= 90 else "[!]"
        print(f"{status} {r['semester']}: {r['outline_success']}/{r['total_courses']} "
              f"({r['success_rate']:.1f}%) - {r['elapsed_minutes']:.1f}分鐘")

    print("=" * 70)

if __name__ == "__main__":
    main()
