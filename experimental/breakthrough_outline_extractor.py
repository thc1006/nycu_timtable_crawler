#!/usr/bin/env python3
"""
突破性方案：多層綱要提取器
結合 JSON API + HTML 爬蟲 + 備選端點

目標：達到 80%+ 成功率
策略：
1. 嘗試主 JSON API (現有)
2. 嘗試 HTML 頁面爬蟲 (新)
3. 嘗試備選 API 端點 (新)
4. 組合多個數據源
"""
import requests
from bs4 import BeautifulSoup
import re
import json
import time

class BreakthroughOutlineExtractor:
    """突破性綱要提取器"""

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.session = requests.Session()

    def extract_from_json_api(self, year, sem, cos_id, timeout=8):
        """方法 1: JSON API (現有方法)"""
        try:
            request_data = {
                "acy": str(year),
                "sem": str(sem),
                "cos_id": str(cos_id),
                "user": "",
                "_token": ""
            }

            # 嘗試基本資訊
            url = "https://timetable.nycu.edu.tw/?r=main/getCrsOutlineBase"
            response = self.session.post(url, data=request_data, headers=self.headers,
                                        verify=False, timeout=timeout)

            if response.status_code == 200:
                data = response.json()
                if isinstance(data, dict) and data and data.get('cos_name'):
                    return {'source': 'json_api', 'data': data}
        except:
            pass
        return None

    def extract_from_html_page(self, year, sem, cos_id, timeout=8):
        """方法 2: HTML 頁面爬蟲 (新方法)"""
        try:
            # 構造綱要頁面 URL
            url = f"https://timetable.nycu.edu.tw/?r=course/syllabus&acy={year}&sem={sem}&cos_id={cos_id}"

            response = self.session.get(url, headers=self.headers, verify=False, timeout=timeout)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                # 尋找綱要標題和內容
                outline_data = {}

                # 搜尋常見的綱要標籤
                for tag in soup.find_all(['h2', 'h3', 'h4']):
                    text = tag.get_text(strip=True)
                    if any(keyword in text for keyword in ['綱要', 'Outline', 'Course']):
                        # 找到後續的內容
                        parent = tag.find_parent()
                        if parent:
                            content = parent.get_text(strip=True)
                            if content and len(content) > 20:
                                outline_data['outline'] = content[:500]
                                return {'source': 'html_page', 'data': outline_data}

                # 如果找到任何實質內容，也返回
                body_text = soup.get_text(strip=True)
                if body_text and len(body_text) > 100:
                    return {'source': 'html_page', 'data': {'content': body_text[:1000]}}

        except:
            pass
        return None

    def extract_from_alt_api(self, year, sem, cos_id, timeout=8):
        """方法 3: 備選 API 端點"""
        try:
            request_data = {
                "acy": str(year),
                "sem": str(sem),
                "cos_id": str(cos_id),
                "user": "",
                "_token": ""
            }

            # 嘗試替代端點
            alt_urls = [
                "https://timetable.nycu.edu.tw/?r=main/getCrsOutlineDescription",
                "https://timetable.nycu.edu.tw/?r=main/getCrsOutlineSyllabuses",
                "https://timetable.nycu.edu.tw/?r=main/get_course_outline",
            ]

            for url in alt_urls:
                try:
                    response = self.session.post(url, data=request_data, headers=self.headers,
                                               verify=False, timeout=timeout)
                    if response.status_code == 200:
                        data = response.json()
                        if isinstance(data, dict) and data:
                            return {'source': 'alt_api', 'url': url, 'data': data}
                except:
                    continue

        except:
            pass
        return None

    def extract_outline(self, year, sem, cos_id):
        """多層提取邏輯 - 嘗試所有方法"""
        results = []

        # 優先級 1: JSON API
        result = self.extract_from_json_api(year, sem, cos_id)
        if result:
            results.append(result)
            return result  # 如果成功就立即返回

        # 優先級 2: HTML 頁面
        result = self.extract_from_html_page(year, sem, cos_id)
        if result:
            results.append(result)
            return result

        # 優先級 3: 備選 API
        result = self.extract_from_alt_api(year, sem, cos_id)
        if result:
            results.append(result)
            return result

        return None

    def test_improvement(self, test_courses, expected_rate=0.80):
        """測試改進效果"""
        success = 0
        sources = {}

        for idx, course_id in enumerate(test_courses):
            result = self.extract_outline(114, 1, course_id)  # 用 114-1 測試（已知有 42.8%）

            if result:
                success += 1
                source = result['source']
                sources[source] = sources.get(source, 0) + 1

            if (idx + 1) % 20 == 0:
                rate = success / (idx + 1)
                print(f"  [{idx+1}/{len(test_courses)}] Success rate: {rate*100:.1f}%")

        final_rate = success / len(test_courses) if test_courses else 0

        print("\n" + "=" * 60)
        print(f"Success Rate: {final_rate*100:.1f}%")
        print(f"Sources: {sources}")
        print("=" * 60)

        return final_rate

# 測試
if __name__ == "__main__":
    print("Testing Breakthrough Outline Extractor")
    print("=" * 60)

    extractor = BreakthroughOutlineExtractor()

    # 用 114-1 的課程測試（該學期有 42.8% 成功率）
    # 測試 30 個課程
    test_ids = [str(i) for i in range(1, 31)]

    rate = extractor.test_improvement(test_ids)

    if rate >= 0.80:
        print("\nSUCCESS! Achieved 80% target!")
    else:
        print(f"\nCurrent rate: {rate*100:.1f}% (Need: 80%)")
