#!/usr/bin/env python3
"""
測試優化後的爬蟲
Test the improved adaptive crawler
"""
import sys
from nycu_crawler import NYCUCrawler
import time

def test_single_semester():
    """測試單一學期的爬取（使用 113-1 測試）"""
    print("=" * 70)
    print("測試優化後的爬蟲 - 113-1 學期")
    print("=" * 70)

    start_time = time.time()

    # 創建爬蟲實例
    crawler = NYCUCrawler(113, 1, fetch_outline=True)

    print(f"\n開始爬取 113-1 學期...")
    print(f"預期改進：")
    print(f"  1. 不再出現 'bool' object has no attribute 'get' 錯誤")
    print(f"  2. 成功率大幅提升（部分資料也算成功）")
    print(f"  3. 速度提升約 75%（延遲從 0.2秒降到 0.05秒）")
    print(f"\n")

    # 執行爬取
    try:
        crawler.crawl()

        elapsed = time.time() - start_time
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)

        print("\n" + "=" * 70)
        print("爬取完成！")
        print("=" * 70)
        print(f"總耗時: {minutes} 分 {seconds} 秒")
        print(f"總課程數: {len(crawler.courses_list)}")
        print(f"成功獲取綱要: {crawler.stats['outline_success']} 門")
        print(f"失敗: {crawler.stats['outline_fail']} 門")

        success_rate = (crawler.stats['outline_success'] / len(crawler.courses_list) * 100) if crawler.courses_list else 0
        print(f"成功率: {success_rate:.1f}%")

        print("\n預期成功率應該大幅提升（從 10-35% 提升到 70-90%）")

    except Exception as e:
        print(f"\n錯誤: {e}")
        return False

    return True

if __name__ == "__main__":
    success = test_single_semester()
    sys.exit(0 if success else 1)
