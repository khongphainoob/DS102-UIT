import time
from pathlib import Path
from typing import Any, Dict, List
import requests
from src.collectors.base import get_session, save_jsonl, get_current_utc_iso


SUBJECTS = [
    "computer_science",
    "science_fiction",
    "history",
    "artificial_intelligence",
    "psychology",
    "philosophy",
    "fantasy",
    "mathematics",
    "physics",
    "economics",
]


class OpenLibraryCollector:
    """
    Thu thập dữ liệu từ Open Library Search API (https://openlibrary.org/search.json).
    - API trả dữ liệu ở cấp độ Work và Edition.
    - Duyệt qua 10 chủ đề đa dạng để lấy sách phong phú.
    - Không cần browser automation.
    - Lưu toàn bộ JSON docs thô vào openlibrary_1000_raw.jsonl.
    """
    SEARCH_URL = "https://openlibrary.org/search.json"

    def __init__(self, raw_dir: Path, delay_seconds: float = 1.0):
        self.raw_dir = Path(raw_dir)
        self.delay_seconds = delay_seconds
        self.session = get_session(
            "DS102-OpenLibraryCollector/1.0 (UIT DS102 Project - contact: student@uit.edu.vn)"
        )

    def collect(self, target_count: int = 1000) -> Path:
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        raw_items: List[Dict[str, Any]] = []
        seen_keys = set()
        items_per_subject = max(target_count // len(SUBJECTS), 100)

        print(f"[*] [OpenLibraryCollector] Bắt đầu thu thập mục tiêu {target_count} tác phẩm (Work-level)...")

        for subj in SUBJECTS:
            if len(raw_items) >= target_count:
                break

            print(f"[*] Đang lấy chủ đề '{subj}' (limit={items_per_subject})...")
            params = {
                "q": f"subject:{subj}",
                "fields": "key,title,author_name,first_publish_year,edition_count,language,publisher,subject,number_of_pages_median,cover_i,ebook_access,has_fulltext,isbn,publish_year,edition_key",
                "limit": items_per_subject,
                "page": 1,
            }

            try:
                resp = self.session.get(self.SEARCH_URL, params=params, timeout=(15, 45))
                resp.raise_for_status()
                data = resp.json()
                docs = data.get("docs", [])

                added = 0
                for d in docs:
                    key = d.get("key")
                    if not key or key in seen_keys:
                        continue
                    seen_keys.add(key)

                    d["queried_subject"] = subj
                    d["retrieved_at"] = get_current_utc_iso()
                    raw_items.append(d)
                    added += 1

                print(f"[+] Lấy thành công {added} tác phẩm từ chủ đề '{subj}'. Tổng: {len(raw_items)}")
            except Exception as e:
                print(f"[!] Lỗi khi lấy chủ đề {subj}: {e}")

            time.sleep(self.delay_seconds)

        out_path = self.raw_dir / "openlibrary_1000_raw.jsonl"
        save_jsonl(raw_items, out_path)
        print(f"[+] [OpenLibraryCollector] Đã lưu {len(raw_items)} tác phẩm thô vào {out_path}")
        return out_path
