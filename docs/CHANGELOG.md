# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [4.0.0] - 2025-10-20

### 🎉 Major Release - Complete Refactoring

#### Added
- **Multi-threading Support**: 4-thread parallel crawling for 3-4x performance improvement
- **Structured Schedule Parsing**: Parse time-classroom strings into structured objects
  - Day names (Monday-Sunday in Chinese)
  - Time periods (1-15, y, z)
  - Exact start/end times (HH:MM format)
  - Classroom with floor information
- **Batch Processing Scripts**:
  - `crawl_basic_batch_multithreaded.py` - Batch crawl basic course data
  - `crawl_outline_batch_multithreaded.py` - Batch crawl complete outlines
- **Resume Capability**: Checkpoint system for interrupted crawls
- **Example Scripts**:
  - `examples/search_courses.py` - Course search demonstrations
  - `examples/analyze_statistics.py` - Statistical analysis examples
  - `examples/check_conflicts.py` - Schedule conflict detection
- **Google Colab Support**: Updated notebooks for cloud execution
- **Progress Monitoring**: `check_progress.py` for tracking crawl progress

#### Changed
- **Data Format v2.0**: Migrated from object format to array format with metadata
  ```json
  {
    "metadata": {
      "semester": "114-1",
      "total_courses": 8028,
      "last_updated": "2025-10-20T...",
      "data_format_version": "2.0"
    },
    "courses": [...]
  }
  ```
- **Type Conversion**: Changed numeric strings to proper number types
  - `credit`: "3.00" → 3.0
  - `hours`: "3.00" → 3.0
  - `enrollment.limit`: "60" → 60
  - `enrollment.current`: "45" → 45
- **Schedule Structure**: Enhanced from simple strings to structured arrays
- **Error Handling**: Improved retry mechanism with configurable attempts
- **Code Comments**: All comments converted to Traditional Chinese

#### Documentation
- **README.md**: Complete rewrite with v4.0 features and badges
- **CONTRIBUTING.md**: NYCU-localized contributing guide
- **LICENSE**: Changed from MIT to Apache-2.0
- **requirements.txt**: Added dependency management
- **Repository SEO**: Optimized description and topics for NYCU student discovery

#### Performance
- Multi-threading reduces crawl time from ~20 min to ~3 min for 9 semesters
- Crawled 110-1 to 114-1 (9 semesters, 66,149 courses, 47.4 MB)

---

## [3.0.0] - 2024-XX-XX

### Added
- Complete outline crawling mode
- Enhanced error handling
- Progress indicators

### Changed
- Improved data validation
- Better logging system

---

## [2.0.0] - 2024-XX-XX

### Added
- Array-based data format
- Metadata header

### Changed
- Migrated from object-based to array-based JSON structure
- Standardized field names

---

## [1.0.0] - 2024-XX-XX

### Added
- Initial release
- Basic course information crawler
- Object-based JSON output format
- Single-semester crawling
- Command-line interface

### Features
- Crawl course basic information from NYCU timetable system
- Export to JSON format
- Support for different semesters
- Automatic language detection

---

## Data Format Evolution

### v1.0 (Object Format)
```json
{
  "COURSE_ID": {
    "name": "課程名稱",
    "teacher": "教師"
  }
}
```

### v2.0 (Array Format with Metadata)
```json
{
  "metadata": {
    "semester": "114-1",
    "total_courses": 8028
  },
  "courses": [
    {
      "id": "COURSE_ID",
      "name": "課程名稱",
      "teacher": "教師",
      "schedule": [
        {
          "day": 1,
          "day_name": "Monday",
          "periods": [3, 4],
          "time_start": "10:10",
          "time_end": "12:00",
          "classroom": "EE102",
          "floor": "1F"
        }
      ]
    }
  ]
}
```

---

## Contact

**Project Maintainer**: hctsai@linux.com

For questions, suggestions, or contributions, please:
- Open an [Issue](https://github.com/thc1006/nycu_timtable_crawler/issues)
- Submit a [Pull Request](https://github.com/thc1006/nycu_timtable_crawler/pulls)
- Email: hctsai@linux.com

---

## Acknowledgments

感謝所有陽明交通大學的貢獻者與使用者！

Special thanks to:
- NYCU students who provided feedback
- Contributors who helped improve the codebase
- The open-source community

---

*Last Updated: 2025-10-20*
