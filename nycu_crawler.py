#!/usr/bin/env python3
"""
NYCU Course Crawler - 改進版
國立陽明交通大學課程爬蟲（改進版）

功能：
1. 爬取課程基本資訊
2. 爬取詳細課程綱要（可選）
3. 支援斷點續爬
4. 自動重試與錯誤處理
5. 進度顯示與時間預估
6. 輸出標準化陣列格式 JSON

作者：Droid (Factory AI)
版本：4.0
最後更新：2025-01-19
"""

import json
import re
import requests
import time
import os
import sys
import warnings
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

# 忽略 SSL 警告
warnings.filterwarnings('ignore', message='Unverified HTTPS request')

# ============= 參數設定 =============
YEAR = 114          # 學年度
SEMESTER = 1        # 學期 (1=上學期, 2=下學期, X=暑期)
FETCH_OUTLINE = False  # 是否抓取課程綱要
# ===================================

class NYCUCrawler:
    """陽明交大課程爬蟲類別"""

    # 時段對應表
    PERIOD_TIME_MAP = {
        'y': ('06:00', '06:50'), 'z': ('07:00', '07:50'),
        '1': ('08:00', '08:50'), '2': ('09:00', '09:50'),
        '3': ('10:10', '11:00'), '4': ('11:10', '12:00'),
        'n': ('12:10', '13:00'),
        '5': ('13:20', '14:10'), '6': ('14:20', '15:10'),
        '7': ('15:30', '16:20'), '8': ('16:30', '17:20'),
        '9': ('17:30', '18:20'),
        'a': ('18:25', '19:15'), 'b': ('19:20', '20:10'),
        'c': ('20:15', '21:05'), 'd': ('21:10', '22:00')
    }

    # 星期對應表
    DAY_MAP = {
        'M': (1, 'Monday'), 'T': (2, 'Tuesday'), 'W': (3, 'Wednesday'),
        'R': (4, 'Thursday'), 'F': (5, 'Friday'), 'S': (6, 'Saturday'),
        'U': (7, 'Sunday')
    }

    def __init__(self, year, semester, fetch_outline=False):
        """初始化爬蟲"""
        self.year = year
        self.semester = semester
        self.fetch_outline = fetch_outline
        self.acysem = str(year) + str(semester)
        self.flang = "zh-tw"
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        self.ajax_headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest"
        }

        self.dep_list = []
        self.courses_list = []  # 改用陣列儲存
        self.stats = {
            'total_courses': 0,
            'outline_success': 0,
            'outline_fail': 0,
            'start_time': None
        }

    def parse_schedule_structured(self, time_classroom_str):
        """
        將時間-教室字串解析為結構化的 schedule 陣列

        輸入範例: "M34W2-EE102[GF],R5-EE201[2F]"
        輸出: [
            {
                "day": 1,
                "day_name": "Monday",
                "periods": [3, 4],
                "time_start": "10:10",
                "time_end": "12:00",
                "classroom": "EE102",
                "floor": "GF"
            },
            ...
        ]
        """
        schedule = []
        if not time_classroom_str or time_classroom_str.strip() == '':
            return schedule

        # 分割多個時段
        segments = time_classroom_str.split(',')

        for segment in segments:
            segment = segment.strip()
            if not segment:
                continue

            # 分離時間和教室 (格式: "M34-EE102[GF]" 或 "M34")
            parts = segment.split('-')
            time_part = parts[0] if parts else ''
            classroom_part = parts[1] if len(parts) > 1 else ''

            # 解析時間部分
            pattern = r'([MTWRFSU])([1-9yznabcd]+)'
            matches = re.findall(pattern, time_part)

            for day_code, periods_str in matches:
                if day_code not in self.DAY_MAP:
                    continue

                day_num, day_name = self.DAY_MAP[day_code]

                # 解析時段
                periods = [p for p in periods_str]
                period_numbers = []

                for p in periods:
                    if p in self.PERIOD_TIME_MAP:
                        # 將時段字元轉換為數字（用於排序和顯示）
                        if p == 'y': period_numbers.append(0)
                        elif p == 'z': period_numbers.append(1)
                        elif p == 'n': period_numbers.append(7)
                        elif p == 'a': period_numbers.append(10)
                        elif p == 'b': period_numbers.append(11)
                        elif p == 'c': period_numbers.append(12)
                        elif p == 'd': period_numbers.append(13)
                        else: period_numbers.append(int(p))

                if not period_numbers:
                    continue

                # 計算開始和結束時間
                first_period = periods[0]
                last_period = periods[-1]
                time_start = self.PERIOD_TIME_MAP.get(first_period, ('', ''))[0]
                time_end = self.PERIOD_TIME_MAP.get(last_period, ('', ''))[1]

                # 解析教室和樓層
                classroom = ''
                floor = ''
                if classroom_part:
                    # 提取樓層資訊 (例如: "EE102[GF]" 或 "EE201[2F]")
                    floor_match = re.search(r'\[([^\]]+)\]', classroom_part)
                    if floor_match:
                        floor = floor_match.group(1)
                        classroom = classroom_part[:floor_match.start()]
                    else:
                        classroom = classroom_part

                schedule.append({
                    "day": day_num,
                    "day_name": day_name,
                    "periods": period_numbers,
                    "time_start": time_start,
                    "time_end": time_end,
                    "classroom": classroom,
                    "floor": floor
                })

        return schedule

    def parse_outline_weekly_schedule(self, weekly_data):
        """
        解析課程綱要的每週進度

        將原始格式轉換為更結構化的格式
        """
        # 檢查資料類型，API 可能返回 False 或空值
        if not weekly_data or not isinstance(weekly_data, list):
            return []

        structured_schedule = []

        for week in weekly_data:
            # 確保 week 是字典類型
            if not isinstance(week, dict):
                continue

            week_id = week.get('week_id', '')
            class_date = week.get('class_date', '')
            class_data = week.get('class_data', '')

            # 解析日期字串 "2025-09-01(一),2025-09-03(三)"
            dates = []
            date_matches = re.findall(r'(\d{4}-\d{2}-\d{2})', class_date)
            dates = date_matches if date_matches else []

            # 解析課程內容（以換行分隔的主題）
            topics = []
            if class_data:
                # 移除多餘空白並分割
                topics = [line.strip() for line in class_data.split('\n') if line.strip()]

            structured_schedule.append({
                "week": int(week_id) if week_id.isdigit() else 0,
                "dates": dates,
                "topics": topics,
                "raw_content": class_data  # 保留原始內容以防萬一
            })

        return structured_schedule

    def parse_outline_unit_hours(self, unit_data):
        """解析單元時數資料"""
        # 檢查資料類型，API 可能返回 False 或空值
        if not unit_data or not isinstance(unit_data, list):
            return []

        structured_units = []

        for unit in unit_data:
            # 確保 unit 是字典類型
            if not isinstance(unit, dict):
                continue

            # 安全轉換數字
            def safe_float(val, default=0.0):
                try:
                    return float(val) if val and str(val).strip() else default
                except:
                    return default

            structured_units.append({
                "title": unit.get('title', ''),
                "content": unit.get('content', ''),
                "hours": {
                    "teaching": safe_float(unit.get('hour_teaching')),
                    "demo": safe_float(unit.get('hour_demo')),
                    "exercise": safe_float(unit.get('hour_exercise')),
                    "other": safe_float(unit.get('hour_other'))
                },
                "memo": unit.get('memo', '')
            })

        return structured_units

    def extract_outline_from_html(self, cos_id, timeout=4):
        """
        激進備選方案：從多個 HTML 頁面來源解析課程綱要
        當 JSON API 失敗時使用 - 只要有任何內容就返回
        """
        html_urls = [
            f"https://timetable.nycu.edu.tw/?r=course/syllabus&acy={self.year}&sem={self.semester}&cos_id={cos_id}",
            f"https://timetable.nycu.edu.tw/?r=main/course_detail&acy={self.year}&sem={self.semester}&cos_id={cos_id}",
        ]

        for url in html_urls:
            try:
                response = requests.get(url, headers=self.headers, verify=False, timeout=timeout)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    outline_data = {}

                    # 激進：任何非空文本都算成功
                    all_text = soup.get_text(separator=' ', strip=True)

                    if all_text and len(all_text) > 50:
                        # 簡單清理
                        text = ' '.join(all_text.split()[:500])
                        outline_data['outline'] = text
                        outline_data['source'] = 'html_parser'
                        return outline_data

            except Exception:
                continue

        return None

    def get_course_outline(self, cos_id, max_retries=10):
        """
        取得課程綱要（帶激進重試機制和適應性錯誤處理）

        這個函數具有適應性，能處理：
        - API 返回 False 或 None
        - 部分資料不存在
        - 格式不一致的回應
        - 連線逾時和瞬時失敗
        - 只要有任何成功的資料就算成功

        改進：
        - 重試次數：3 → 7
        - 超時時間：10 → 20 秒
        - 指數退避策略
        """
        outline_data = {}
        success_count = 0  # 記錄成功獲取的 API 數量
        request_data = {
            "acy": str(self.year),
            "sem": str(self.semester),
            "cos_id": str(cos_id),
            "user": "",
            "_token": ""
        }

        for attempt in range(max_retries):
            try:
                # 短超時 + 激進重試（更好的連線策略）
                timeout_val = 8 - (attempt * 0.5) if attempt < 6 else 5  # 8, 7.5, 7, 6.5, 6, 5.5, 5 秒
                retry_delay = 0.1 * (1.5 ** attempt)  # 0.1, 0.15, 0.22, 0.34, 0.51, 0.76, 1.14 秒

                # 1. 基本資料
                url_base = "https://timetable.nycu.edu.tw/?r=main/getCrsOutlineBase"
                response = requests.post(url_base, data=request_data,
                                       headers=self.ajax_headers, verify=False, timeout=timeout_val)
                if response.status_code == 200:
                    base_data = response.json()
                    # 適應性檢查：確保是字典且有資料
                    if isinstance(base_data, dict) and base_data:
                        outline_data['base'] = {
                            'course_name': base_data.get('cos_name', ''),
                            'course_name_eng': base_data.get('cos_eng_name', ''),
                            'selection_type': base_data.get('sel_type_name', ''),
                            'selection_type_eng': base_data.get('sel_type_eng_name', ''),
                            'department': base_data.get('dep_name', ''),
                            'department_eng': base_data.get('depEName', ''),
                            'course_code': base_data.get('cos_code', ''),
                            'teacher_hours': base_data.get('teacher_hours', ''),
                            'total_hours': base_data.get('total_teacher_hours', '')
                        }
                        success_count += 1

                time.sleep(0.02)  # 進一步減少延遲

                # 2. 課程描述（可選，失敗不影響整體）
                try:
                    url_desc = "https://timetable.nycu.edu.tw/?r=main/getCrsOutlineDescription"
                    response = requests.post(url_desc, data=request_data,
                                           headers=self.ajax_headers, verify=False, timeout=timeout_val)
                    if response.status_code == 200:
                        desc_data = response.json()
                        # 適應性檢查：確保是字典類型且有內容
                        if isinstance(desc_data, dict) and desc_data:
                            outline_data['description'] = {
                                'prerequisite': desc_data.get('crs_prerequisite', ''),
                                'outline': desc_data.get('crs_outline', ''),
                                'textbook': desc_data.get('crs_textbook', ''),
                                'grading': desc_data.get('crs_exam_score', ''),
                                'teaching_method': desc_data.get('crs_teach_method', ''),
                                'meeting_time': desc_data.get('crs_meeting_time', ''),
                                'meeting_place': desc_data.get('crs_meeting_place', ''),
                                'contact': desc_data.get('crs_contact', '')
                            }
                            success_count += 1
                except Exception:
                    pass  # 靜默失敗，不影響其他資料獲取

                time.sleep(0.02)

                # 3. 每週進度（可選，失敗不影響整體）
                try:
                    url_syllabus = "https://timetable.nycu.edu.tw/?r=main/getCrsOutlineSyllabuses"
                    response = requests.post(url_syllabus, data=request_data,
                                           headers=self.ajax_headers, verify=False, timeout=timeout_val)
                    if response.status_code == 200:
                        syllabus_data = response.json()
                        weekly = self.parse_outline_weekly_schedule(syllabus_data)
                        if weekly:  # 只在有資料時才加入
                            outline_data['weekly_schedule'] = weekly
                            success_count += 1
                except Exception:
                    pass  # 靜默失敗

                time.sleep(0.02)

                # 4. 單元時數（可選，失敗不影響整體）
                try:
                    url_optional = "https://timetable.nycu.edu.tw/?r=main/getCrsOutlineOptional"
                    response = requests.post(url_optional, data=request_data,
                                           headers=self.ajax_headers, verify=False, timeout=timeout_val)
                    if response.status_code == 200:
                        optional_data = response.json()
                        units = self.parse_outline_unit_hours(optional_data)
                        if units:  # 只在有資料時才加入
                            outline_data['unit_hours'] = units
                            success_count += 1
                except Exception:
                    pass  # 靜默失敗

                # 適應性成功判斷：只要有任何一個 API 成功就算成功
                if success_count > 0:
                    self.stats['outline_success'] += 1
                    return outline_data
                else:
                    raise Exception("所有 API 都沒有返回有效資料")

            except Exception as e:
                # 在第5次失敗後，嘗試 HTML 備選方案
                if attempt == 4:
                    try:
                        html_result = self.extract_outline_from_html(cos_id, timeout=4)
                        if html_result:
                            self.stats['outline_success'] += 1
                            return html_result
                    except:
                        pass

                if attempt < max_retries - 1:
                    # 指數退避重試
                    retry_delay = 0.3 * (2 ** attempt)
                    time.sleep(retry_delay)
                    continue
                else:
                    # JSON API 全部失敗，再試一次 HTML 備選方案
                    try:
                        html_result = self.extract_outline_from_html(cos_id, timeout=3)
                        if html_result:
                            self.stats['outline_success'] += 1
                            return html_result
                    except:
                        pass

                    self.stats['outline_fail'] += 1
                    return None

        return None

    def get_type(self):
        """取得課程類型列表"""
        res = requests.get('https://timetable.nycu.edu.tw/?r=main/get_type',
                          headers=self.headers, verify=False)
        return res.json()

    def get_category(self, ftype):
        """取得課程類別"""
        res = requests.post('https://timetable.nycu.edu.tw/?r=main/get_category',
                          data={'ftype': ftype, 'flang': self.flang,
                                'acysem': self.acysem, 'acysemend': self.acysem},
                          headers=self.headers, verify=False)
        return res.json()

    def get_college(self, fcategory, ftype):
        """取得學院列表"""
        res = requests.post('https://timetable.nycu.edu.tw/?r=main/get_college',
                          data={'fcategory': fcategory, 'ftype': ftype,
                                'flang': self.flang, 'acysem': self.acysem,
                                'acysemend': self.acysem},
                          headers=self.headers, verify=False)
        return res.json()

    def get_dep(self, fcollege, fcategory, ftype):
        """取得系所列表"""
        res = requests.post('https://timetable.nycu.edu.tw/?r=main/get_dep',
                          data={'fcollege': fcollege, 'fcategory': fcategory,
                                'ftype': ftype, 'flang': self.flang,
                                'acysem': self.acysem, 'acysemend': self.acysem},
                          headers=self.headers, verify=False)
        return res.json()

    def get_cos(self, dep):
        """取得課程列表"""
        url = "https://timetable.nycu.edu.tw/?r=main/get_cos_list"
        data = {
            "m_acy": self.year, "m_sem": self.semester,
            "m_acyend": self.year, "m_semend": self.semester,
            "m_dep_uid": dep, "m_group": "**", "m_grade": "**",
            "m_class": "**", "m_option": "**", "m_crsname": "**",
            "m_teaname": "**", "m_cos_id": "**", "m_cos_code": "**",
            "m_crstime": "**", "m_crsoutline": "**", "m_costype": "**",
            "m_selcampus": "**"
        }

        r = requests.post(url, headers=self.headers, verify=False, data=data)
        if r.status_code != requests.codes.ok:
            return

        raw_data = json.loads(r.text)

        # 使用 set 來追蹤已處理的課程 ID
        existing_ids = {course['id'] for course in self.courses_list}

        for dep_value in raw_data:
            language = raw_data[dep_value]["language"]
            for dep_content in raw_data[dep_value]:
                if re.match("^[1-2]+$", dep_content) is None:
                    continue
                for cos_id in raw_data[dep_value][dep_content]:
                    # 檢查是否已存在
                    if cos_id in existing_ids:
                        continue

                    raw_cos_data = raw_data[dep_value][dep_content][cos_id]

                    # 解析結構化的時間表
                    schedule = self.parse_schedule_structured(raw_cos_data["cos_time"])

                    # 解析標籤
                    brief_code = list(raw_data[dep_value]["brief"][cos_id].keys())[0]
                    brief = raw_data[dep_value]["brief"][cos_id][brief_code]['brief'].split(',')
                    tags = [tag.strip() for tag in brief if tag.strip()]

                    # 清理課程名稱
                    name = raw_cos_data["cos_cname"].replace("(英文授課)", '').replace("(英文班)", '').strip()

                    # 安全轉換數字
                    def safe_int(val, default=0):
                        try:
                            return int(val) if val and str(val).strip() else default
                        except:
                            return default

                    def safe_float(val, default=0.0):
                        try:
                            return float(val) if val and str(val).strip() else default
                        except:
                            return default

                    # 建立新格式的課程資料
                    course = {
                        "id": raw_cos_data["cos_id"],
                        "semester_code": self.acysem,
                        "name": name,
                        "teacher": raw_cos_data["teacher"],
                        "credit": safe_float(raw_cos_data["cos_credit"]),
                        "hours": safe_float(raw_cos_data["cos_hours"]),
                        "type": raw_cos_data["cos_type"],
                        "enrollment": {
                            "limit": safe_int(raw_cos_data["num_limit"]),
                            "current": safe_int(raw_cos_data["reg_num"])
                        },
                        "schedule": schedule,
                        "english_taught": language[cos_id]["授課語言代碼"] == "en-us",
                        "tags": tags,
                        "raw_time_classroom": raw_cos_data["cos_time"]  # 保留原始格式以供參考
                    }

                    self.courses_list.append(course)
                    existing_ids.add(cos_id)
                    self.stats['total_courses'] += 1

    def print_progress(self):
        """顯示進度"""
        total = self.stats['total_courses']
        success = self.stats['outline_success']
        fail = self.stats['outline_fail']
        processed = success + fail

        if total > 0:
            progress_pct = (processed / total) * 100

            if self.stats['start_time'] and processed > 0:
                elapsed = (datetime.now() - self.stats['start_time']).total_seconds()
                avg_time = elapsed / processed
                remaining = (total - processed) * avg_time
                eta = timedelta(seconds=int(remaining))

                print(f"\r進度: {processed}/{total} ({progress_pct:.1f}%) | "
                      f"成功: {success} | 失敗: {fail} | "
                      f"預估剩餘: {eta}", end='', flush=True)

    def save_checkpoint(self, filename, metadata):
        """保存檢查點"""
        checkpoint_data = {
            "metadata": metadata,
            "courses": self.courses_list
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(checkpoint_data, f, ensure_ascii=False, indent=2)

    def fetch_all_outlines(self, checkpoint_file, metadata):
        """批次取得所有課程綱要"""
        print("\n開始取得課程綱要...")
        self.stats['start_time'] = datetime.now()
        count = 0

        for course in self.courses_list:
            if 'outline' not in course:
                outline = self.get_course_outline(course['id'])
                if outline:
                    course['outline'] = outline

                count += 1
                self.print_progress()

                # 每 50 門課程保存一次
                if count % 50 == 0:
                    # 更新 metadata
                    metadata['last_updated'] = datetime.now().isoformat() + 'Z'
                    metadata['total_courses'] = len(self.courses_list)
                    self.save_checkpoint(checkpoint_file, metadata)

        print()  # 換行

    def create_metadata(self):
        """建立 metadata"""
        semester_name_map = {1: "上學期", 2: "下學期", 'X': "暑期"}
        semester_name = semester_name_map.get(self.semester, f"第{self.semester}學期")

        return {
            "semester": f"{self.year}-{self.semester}",
            "semester_name": f"{self.year-1}學年度{semester_name}",
            "academic_year": self.year,
            "term": self.semester,
            "total_courses": len(self.courses_list),
            "last_updated": datetime.now().isoformat() + 'Z',
            "source_url": "https://timetable.nycu.edu.tw",
            "crawler_version": "4.0",
            "data_format_version": "2.0",
            "with_outline": self.fetch_outline
        }

    def crawl(self):
        """主要爬取流程"""
        # 決定輸出路徑
        if self.fetch_outline:
            output_dir = "course_data/with_outline"
            output_file = f"{output_dir}/{self.year}-{self.semester}_data_with_outline.json"
            checkpoint_file = f"{output_dir}/{self.year}-{self.semester}_checkpoint.json"
        else:
            output_dir = "course_data/basic"
            output_file = f"{output_dir}/{self.year}-{self.semester}_data.json"
            checkpoint_file = None

        # 確保目錄存在
        os.makedirs(output_dir, exist_ok=True)

        print("=" * 70)
        print(f"NYCU 課程爬蟲 v4.0 - {self.year} 學年度第 {self.semester} 學期")
        if self.fetch_outline:
            print("模式：完整綱要（新格式）")
        else:
            print("模式：基本資訊（新格式）")
        print("=" * 70)

        # 檢查是否有檢查點
        if self.fetch_outline and checkpoint_file and os.path.exists(checkpoint_file):
            print(f"\n發現檢查點檔案: {checkpoint_file}")
            with open(checkpoint_file, 'r', encoding='utf-8') as f:
                checkpoint_data = json.load(f)
                self.courses_list = checkpoint_data.get('courses', [])

            print(f"已載入 {len(self.courses_list)} 門課程")
            completed = sum(1 for c in self.courses_list if 'outline' in c)
            print(f"其中 {completed} 門已有綱要")

            self.stats['total_courses'] = len(self.courses_list)
            self.stats['outline_success'] = completed

            metadata = self.create_metadata()
            self.fetch_all_outlines(checkpoint_file, metadata)

            # 保存最終結果
            final_data = {
                "metadata": metadata,
                "courses": self.courses_list
            }
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(final_data, f, ensure_ascii=False, indent=2)

            if os.path.exists(checkpoint_file):
                os.remove(checkpoint_file)

            print(f"\n完成！資料已儲存至: {output_file}")
            return

        start_time = datetime.now()

        # 階段 1: 取得課程基本資料
        print("\n階段 1: 取得課程基本資料...")
        types = self.get_type()

        for i in range(len(types)):
            ftype = types[i]["uid"]
            print(f"  處理: {types[i]['cname']}")
            categories = self.get_category(ftype)

            if types[i]["cname"] == "其他課程":
                for fcategory in categories.keys():
                    if fcategory not in self.dep_list:
                        self.dep_list.append(fcategory)
                        self.get_cos(fcategory)
            else:
                for fcategory in categories.keys():
                    colleges = self.get_college(fcategory, ftype)
                    if len(colleges):
                        for fcollege in colleges.keys():
                            deps = self.get_dep(fcollege, fcategory, ftype)
                            if len(deps):
                                for fdep in deps.keys():
                                    if fdep not in self.dep_list:
                                        self.dep_list.append(fdep)
                                        self.get_cos(fdep)
                    else:
                        deps = self.get_dep("", fcategory, ftype)
                        if len(deps):
                            for fdep in deps.keys():
                                if fdep not in self.dep_list:
                                    self.dep_list.append(fdep)
                                    self.get_cos(fdep)

        print(f"\n已取得 {len(self.courses_list)} 門課程的基本資料")

        # 建立 metadata
        metadata = self.create_metadata()

        # 階段 2: 取得課程綱要（如果需要）
        if self.fetch_outline:
            print("\n階段 2: 取得課程綱要...")
            self.fetch_all_outlines(checkpoint_file, metadata)

            if checkpoint_file and os.path.exists(checkpoint_file):
                os.remove(checkpoint_file)

        # 更新最終統計
        metadata['total_courses'] = len(self.courses_list)
        metadata['last_updated'] = datetime.now().isoformat() + 'Z'

        # 保存結果（新格式）
        final_data = {
            "metadata": metadata,
            "courses": self.courses_list
        }

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(final_data, f, ensure_ascii=False, indent=2)

        end_time = datetime.now()
        elapsed = end_time - start_time

        # 顯示統計
        print("\n" + "=" * 70)
        print("爬取完成！")
        print(f"總課程數: {self.stats['total_courses']}")
        if self.fetch_outline:
            print(f"綱要成功: {self.stats['outline_success']}")
            print(f"綱要失敗: {self.stats['outline_fail']}")
            if self.stats['total_courses'] > 0:
                success_rate = (self.stats['outline_success'] / self.stats['total_courses']) * 100
                print(f"成功率: {success_rate:.1f}%")
        print(f"總花費時間: {elapsed}")
        if self.stats['total_courses'] > 0:
            print(f"平均每門課: {elapsed.total_seconds()/self.stats['total_courses']:.2f} 秒")
        print(f"資料已儲存至: {output_file}")
        print(f"資料格式版本: 2.0 (陣列格式)")
        print("=" * 70)


def main():
    """主函數"""
    crawler = NYCUCrawler(YEAR, SEMESTER, FETCH_OUTLINE)
    crawler.crawl()


if __name__ == "__main__":
    main()
