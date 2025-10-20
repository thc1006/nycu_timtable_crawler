#!/usr/bin/env python3
"""
直接測試失敗的課程是否真的有綱要
"""
import json
import requests
import time
from collections import defaultdict

def test_course_outline(semester_code, cos_id):
    """直接從 API 測試單個課程的綱要"""

    # NYCU API endpoints
    base_url = "https://timetable.nycu.edu.tw"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': f'{base_url}/'
    }

    endpoints = {
        'base': f'/?r=main/get_course_detail&semester_code={semester_code}&course_id={cos_id}',
        'description': f'/?r=main/get_course_description&semester_code={semester_code}&course_id={cos_id}',
        'schedule': f'/?r=main/get_course_schedule&semester_code={semester_code}&course_id={cos_id}',
        'syllabus': f'/?r=main/get_course_syllabus&semester_code={semester_code}&course_id={cos_id}',
    }

    results = {}

    for endpoint_name, endpoint_url in endpoints.items():
        try:
            url = base_url + endpoint_url
            response = requests.get(url, headers=headers, timeout=5)

            if response.status_code == 200:
                data = response.json()
                # Check if data is not empty/false
                if isinstance(data, dict) and data:
                    results[endpoint_name] = 'OK'
                elif isinstance(data, list) and data:
                    results[endpoint_name] = 'OK'
                elif data is True:
                    results[endpoint_name] = 'OK (True)'
                else:
                    results[endpoint_name] = f'EMPTY ({type(data).__name__})'
            else:
                results[endpoint_name] = f'HTTP {response.status_code}'

            time.sleep(0.1)

        except Exception as e:
            results[endpoint_name] = f'ERROR: {str(e)[:30]}'

    return results

def main():
    print("=" * 70)
    print("Testing Failed Courses")
    print("=" * 70)

    # Get failed samples
    semesters = ['110-1', '110-2', '111-1']

    for semester_name in semesters:
        checkpoint_file = f"course_data/with_outline/{semester_name}_checkpoint.json"

        try:
            with open(checkpoint_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            semester_code = data['metadata']['semester_code'] if 'semester_code' in data['metadata'] else None

            if not semester_code:
                # Extract from filename
                year, term = semester_name.split('-')
                semester_code = f"{int(year)}{int(term)}"  # e.g., "1101"

            # Get failed courses
            failed = [c for c in data['courses'] if not c.get('outline')]

            print(f"\n[{semester_name}] Testing {min(5, len(failed))} failed courses (out of {len(failed)})")

            for i, course in enumerate(failed[:5]):
                cos_id = course.get('id')
                cos_name = course.get('name', 'Unknown')[:40]

                results = test_course_outline(semester_code, cos_id)

                # Check if any endpoint returned data
                has_data = any('OK' in str(v) for v in results.values())
                status = "HAS DATA" if has_data else "NO DATA"

                print(f"  {i+1}. [{status}] ID={cos_id} | {cos_name}")
                print(f"     {results}")

        except Exception as e:
            print(f"Error processing {semester_name}: {e}")

    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
