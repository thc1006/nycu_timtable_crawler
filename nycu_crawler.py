#!/usr/bin/env python3
"""
NYCU Course Crawler - Production Version
國立陽明交通大學課程爬蟲（正式版）

功能：
1. 爬取課程基本資訊
2. 爬取詳細課程綱要（可選）
3. 支援斷點續爬
4. 自動重試與錯誤處理
5. 進度顯示與時間預估

作者：Droid (Factory AI)
版本：3.0
最後更新：2025-01-18
"""

import json
import re
import requests
import time
import os
import sys
import warnings
from datetime import datetime, timedelta

# 忽略 SSL 警告
warnings.filterwarnings('ignore', message='Unverified HTTPS request')

# ============= 參數設定 =============
YEAR = 114          # 學年度
SEMESTER = 1        # 學期 (1=上學期, 2=下學期, X=暑期)
FETCH_OUTLINE = True  # 是否抓取課程綱要
# ===================================

class NYCUCrawler:
    def __init__(self, year, semester, fetch_outline=False):
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
        self.course_data = {}
        self.stats = {
            'total_courses': 0,
            'outline_success': 0,
            'outline_fail': 0,
            'start_time': None
        }
        
    def parse_time(self, tc):
        """擷取上課時間"""
        pattern = '[MTWRFSU][1-9yznabcd]+'
        tc_list = tc.split(',')
        time_list = []
        for item in tc_list:
            time = re.findall(pattern, item.split('-')[0])
            for t in time:
                for i in range(len(t)-1):
                    time_list.append(t[0]+t[i+1])
        return time_list

    def parse_classroom(self, tc):
        """擷取上課教室"""
        tc_list = tc.split(',')
        classroom_list = []
        for item in tc_list:
            try:
                classroom = item.split('-')[1]
            except IndexError:
                classroom = ''
            classroom_list.append(classroom)
        return classroom_list

    def get_course_outline(self, cos_id, max_retries=3):
        """取得課程綱要（帶重試機制）"""
        outline_data = {}
        request_data = {
            "acy": str(self.year),
            "sem": str(self.semester),
            "cos_id": str(cos_id),
            "user": "",
            "_token": ""
        }
        
        for attempt in range(max_retries):
            try:
                # 1. 基本資料
                url_base = "https://timetable.nycu.edu.tw/?r=main/getCrsOutlineBase"
                response = requests.post(url_base, data=request_data, 
                                       headers=self.ajax_headers, verify=False, timeout=10)
                if response.status_code == 200:
                    base_data = response.json()
                    outline_data['base'] = {
                        'cos_name': base_data.get('cos_name', ''),
                        'cos_eng_name': base_data.get('cos_eng_name', ''),
                        'sel_type_name': base_data.get('sel_type_name', ''),
                        'sel_type_eng_name': base_data.get('sel_type_eng_name', ''),
                        'dep_name': base_data.get('dep_name', ''),
                        'depEName': base_data.get('depEName', ''),
                        'cos_code': base_data.get('cos_code', ''),
                        'teacher_hours': base_data.get('teacher_hours', ''),
                        'total_teacher_hours': base_data.get('total_teacher_hours', '')
                    }
                
                time.sleep(0.2)
                
                # 2. 課程描述
                url_desc = "https://timetable.nycu.edu.tw/?r=main/getCrsOutlineDescription"
                response = requests.post(url_desc, data=request_data, 
                                       headers=self.ajax_headers, verify=False, timeout=10)
                if response.status_code == 200:
                    desc_data = response.json()
                    outline_data['description'] = {
                        'prerequisite': desc_data.get('crs_prerequisite', ''),
                        'outline': desc_data.get('crs_outline', ''),
                        'textbook': desc_data.get('crs_textbook', ''),
                        'exam_score': desc_data.get('crs_exam_score', ''),
                        'teach_method': desc_data.get('crs_teach_method', ''),
                        'meeting_time': desc_data.get('crs_meeting_time', ''),
                        'meeting_place': desc_data.get('crs_meeting_place', ''),
                        'contact': desc_data.get('crs_contact', '')
                    }
                
                time.sleep(0.2)
                
                # 3. 每週進度
                url_syllabus = "https://timetable.nycu.edu.tw/?r=main/getCrsOutlineSyllabuses"
                response = requests.post(url_syllabus, data=request_data, 
                                       headers=self.ajax_headers, verify=False, timeout=10)
                if response.status_code == 200:
                    syllabus_data = response.json()
                    outline_data['weekly_schedule'] = []
                    for week in syllabus_data:
                        outline_data['weekly_schedule'].append({
                            'week_id': week.get('week_id', ''),
                            'class_date': week.get('class_date', ''),
                            'class_data': week.get('class_data', ''),
                            'teacher_data': week.get('teacherDataJson', '')
                        })
                
                time.sleep(0.2)
                
                # 4. 單元時數
                url_optional = "https://timetable.nycu.edu.tw/?r=main/getCrsOutlineOptional"
                response = requests.post(url_optional, data=request_data, 
                                       headers=self.ajax_headers, verify=False, timeout=10)
                if response.status_code == 200:
                    optional_data = response.json()
                    outline_data['unit_hours'] = []
                    for unit in optional_data:
                        outline_data['unit_hours'].append({
                            'title': unit.get('opt_title', ''),
                            'content': unit.get('opt_content', ''),
                            'hour_teaching': unit.get('opt_hour_teaching', ''),
                            'hour_demo': unit.get('opt_hour_demo', ''),
                            'hour_exercise': unit.get('opt_hour_exercise', ''),
                            'hour_other': unit.get('opt_hour_other', ''),
                            'memo': unit.get('opt_memo', '')
                        })
                
                self.stats['outline_success'] += 1
                return outline_data
                
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(1)
                    continue
                else:
                    self.stats['outline_fail'] += 1
                    return None
        
        return None

    def get_type(self):
        res = requests.get('https://timetable.nycu.edu.tw/?r=main/get_type', 
                          headers=self.headers, verify=False)
        return res.json()

    def get_category(self, ftype):
        res = requests.post('https://timetable.nycu.edu.tw/?r=main/get_category', 
                          data={'ftype': ftype, 'flang': self.flang, 
                                'acysem': self.acysem, 'acysemend': self.acysem},
                          headers=self.headers, verify=False)
        return res.json()

    def get_college(self, fcategory, ftype):
        res = requests.post('https://timetable.nycu.edu.tw/?r=main/get_college',
                          data={'fcategory': fcategory, 'ftype': ftype, 
                                'flang': self.flang, 'acysem': self.acysem, 
                                'acysemend': self.acysem},
                          headers=self.headers, verify=False)
        return res.json()

    def get_dep(self, fcollege, fcategory, ftype):
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
        for dep_value in raw_data:
            language = raw_data[dep_value]["language"]
            for dep_content in raw_data[dep_value]:
                if re.match("^[1-2]+$", dep_content) is None:
                    continue
                for cos_id in raw_data[dep_value][dep_content]:
                    if cos_id in self.course_data:
                        continue
                        
                    raw_cos_data = raw_data[dep_value][dep_content][cos_id]
                    time_list = self.parse_time(raw_cos_data["cos_time"])
                    classroom_list = self.parse_classroom(raw_cos_data["cos_time"])
                    brief_code = list(raw_data[dep_value]["brief"][cos_id].keys())[0]
                    brief = raw_data[dep_value]["brief"][cos_id][brief_code]['brief'].split(',')
                    name = raw_cos_data["cos_cname"].replace("(英文授課)", '').replace("(英文班)", '')
                    
                    self.course_data[cos_id] = {
                        "id": raw_cos_data["cos_id"],
                        "num_limit": raw_cos_data["num_limit"],
                        "reg_num": raw_cos_data["reg_num"],
                        "name": name,
                        "credit": raw_cos_data["cos_credit"],
                        "hours": raw_cos_data["cos_hours"],
                        "teacher": raw_cos_data["teacher"],
                        "time": time_list,
                        "classroom": classroom_list,
                        "time-classroom": raw_cos_data["cos_time"],
                        "english": language[cos_id]["授課語言代碼"] == "en-us",
                        "brief": brief,
                        "type": raw_cos_data["cos_type"],
                    }
                    
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

    def save_checkpoint(self, filename):
        """保存檢查點"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.course_data, f, ensure_ascii=False, indent=2)

    def fetch_all_outlines(self, checkpoint_file):
        """批次取得所有課程綱要"""
        print("\n開始取得課程綱要...")
        self.stats['start_time'] = datetime.now()
        count = 0
        
        for cos_id, course in self.course_data.items():
            if 'outline' not in course:
                outline = self.get_course_outline(course['id'])
                if outline:
                    course['outline'] = outline
                
                count += 1
                self.print_progress()
                
                # 每 50 門課程保存一次
                if count % 50 == 0:
                    self.save_checkpoint(checkpoint_file)
        
        print()  # 換行

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
        print(f"NYCU 課程爬蟲 - {self.year} 學年度第 {self.semester} 學期")
        if self.fetch_outline:
            print("模式：完整綱要")
        else:
            print("模式：基本資訊")
        print("=" * 70)
        
        # 檢查是否有檢查點
        if self.fetch_outline and checkpoint_file and os.path.exists(checkpoint_file):
            print(f"\n發現檢查點檔案: {checkpoint_file}")
            with open(checkpoint_file, 'r', encoding='utf-8') as f:
                self.course_data = json.load(f)
            print(f"已載入 {len(self.course_data)} 門課程")
            completed = sum(1 for c in self.course_data.values() if 'outline' in c)
            print(f"其中 {completed} 門已有綱要")
            
            self.stats['total_courses'] = len(self.course_data)
            self.stats['outline_success'] = completed
            
            self.fetch_all_outlines(checkpoint_file)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(self.course_data, f, ensure_ascii=False, indent=2)
            
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
        
        print(f"\n已取得 {len(self.course_data)} 門課程的基本資料")
        
        # 階段 2: 取得課程綱要（如果需要）
        if self.fetch_outline:
            print("\n階段 2: 取得課程綱要...")
            self.fetch_all_outlines(checkpoint_file)
            
            if checkpoint_file and os.path.exists(checkpoint_file):
                os.remove(checkpoint_file)
        
        # 保存結果
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.course_data, f, ensure_ascii=False, indent=2)
        
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
        print("=" * 70)


def main():
    """主函數"""
    crawler = NYCUCrawler(YEAR, SEMESTER, FETCH_OUTLINE)
    crawler.crawl()


if __name__ == "__main__":
    main()
