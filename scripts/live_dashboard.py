#!/usr/bin/env python3
"""實時進度 DASHBOARD - 混合方案監控"""
import json
import os
import time
from datetime import datetime

def get_current_stats():
    """獲取當前統計"""
    semesters = ['110-1', '110-2', '111-1', '111-2', '112-1', '112-2', '113-1', '113-2', '114-1']

    stats = {}
    total_courses = 0
    total_success = 0

    for sem in semesters:
        checkpoint = f'course_data/with_outline/{sem}_checkpoint.json'
        if os.path.exists(checkpoint):
            try:
                with open(checkpoint, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                total = data['metadata']['total_courses']
                completed = len(data['courses'])
                success = sum(1 for c in data['courses'] if c.get('outline'))

                total_courses += total
                total_success += success

                success_rate = (success / completed * 100) if completed > 0 else 0
                progress = (completed / total * 100) if total > 0 else 0

                stats[sem] = {
                    'total': total,
                    'completed': completed,
                    'success': success,
                    'rate': success_rate,
                    'progress': progress,
                    'status': 'COMPLETE' if completed == total else f'{progress:.0f}%'
                }
            except:
                stats[sem] = {'status': 'ERROR'}
        else:
            stats[sem] = {'status': 'PENDING'}

    return stats, total_courses, total_success

def print_dashboard():
    """打印儀表板"""
    stats, total_courses, total_success = get_current_stats()

    now = datetime.now().strftime('%H:%M:%S')
    print(f"\n[{now}] AGGRESSIVE RECRAWL - LIVE DASHBOARD")
    print("=" * 100)

    for sem in ['110-1', '110-2', '111-1', '111-2', '112-1', '112-2', '113-1', '113-2', '114-1']:
        if sem in stats and 'rate' in stats[sem]:
            s = stats[sem]
            bar_length = int(s['progress'] / 5)
            bar = '[' + '=' * bar_length + ' ' * (20 - bar_length) + ']'
            print(f"{sem:8} {bar} {s['status']:>6} | Success: {s['success']:5}/{s['completed']:5} ({s['rate']:5.1f}%)")
        else:
            s = stats.get(sem, {})
            print(f"{sem:8} {'['.ljust(23)} | {s.get('status', 'PENDING'):>6}")

    print("=" * 100)

    if total_courses > 0:
        overall_rate = (total_success / total_courses * 100)
        print(f"OVERALL: {total_success}/{total_courses} = {overall_rate:.1f}%")

        if overall_rate >= 80:
            print(f"\n[SUCCESS] REACHED 80% TARGET!")
            return True
        elif overall_rate >= 50:
            print(f"[MILESTONE] 50% Milestone Reached!")

    return False

def monitor():
    """主監控循環"""
    print("Starting Aggressive Recrawl Monitor...")
    print("Checking every 30 seconds for 30 minutes...")

    start_time = time.time()
    timeout = 30 * 60  # 30 minutes

    while time.time() - start_time < timeout:
        if print_dashboard():
            break
        time.sleep(30)

    print("\n[FINAL REPORT]")
    print_dashboard()
    print("\nMonitoring complete!")

if __name__ == "__main__":
    monitor()
