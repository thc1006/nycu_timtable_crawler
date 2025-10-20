#!/usr/bin/env python3
"""實時進度監控 - 追蹤改進效果"""
import json
import os
import time
from datetime import datetime

def check_progress():
    """檢查當前進度"""
    semesters = ['110-1', '110-2', '111-1', '111-2', '112-1', '112-2', '113-1', '113-2', '114-1']

    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Progress Update")
    print("=" * 80)

    total_tested = 0
    total_success = 0
    all_complete = True

    for sem in semesters:
        checkpoint = f'course_data/with_outline/{sem}_checkpoint.json'

        if os.path.exists(checkpoint):
            try:
                with open(checkpoint, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                total = data['metadata']['total_courses']
                completed = len(data['courses'])
                success = sum(1 for c in data['courses'] if c.get('outline'))

                pct = (completed / total * 100) if total > 0 else 0
                success_rate = (success / completed * 100) if completed > 0 else 0

                if completed == total:
                    status = "DONE"
                else:
                    status = f"{pct:.0f}%"
                    all_complete = False

                total_tested += completed
                total_success += success

                print(f"{sem:8} | {completed:5}/{total:5} ({status:>5}) | Success: {success:5} ({success_rate:5.1f}%)")

            except Exception as e:
                all_complete = False
                print(f"{sem:8} | Error: {str(e)[:30]}")
        else:
            all_complete = False
            print(f"{sem:8} | Not started")

    print("=" * 80)

    if total_tested > 0:
        overall_rate = (total_success / total_tested * 100)
        print(f"Overall: {total_success}/{total_tested} ({overall_rate:.1f}%)")

        if overall_rate >= 80:
            print(f"\n[SUCCESS] Reached 80% target! ({overall_rate:.1f}%)")
            return True

    if all_complete:
        print(f"\n[COMPLETE] All semesters finished!")
        return True

    return False

if __name__ == "__main__":
    start_time = time.time()
    timeout = 15 * 60  # 15 minutes

    while time.time() - start_time < timeout:
        if check_progress():
            break
        time.sleep(30)

    if time.time() - start_time >= timeout:
        print(f"\n[TIMEOUT] 15 minutes elapsed")
        check_progress()
