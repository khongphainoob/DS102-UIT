import time
from pathlib import Path
from typing import Any, Dict, List
import requests
from src.collectors.base import get_session, save_jsonl, get_current_utc_iso


CATEGORIES = [
    "beverages",
    "snacks",
    "dairy-products",
    "cereals-and-potatoes",
    "plant-based-foods-and-beverages",
    "meats",
    "desserts",
    "sauces",
    "biscuits-and-cakes",
    "seafood",
    "groceries",
    "dairies",
    "spreads",
    "canned-foods",
]

FIELDS_QUERY = (
    "code,product_name,brands,countries,categories,labels,packaging,stores,quantity,"
    "nutriments,ingredients_text,allergens,additives_n,nutrition_grades,nutrition_grade_fr,"
    "completeness,last_modified_t,ingredients_analysis_tags"
)


class OpenFoodFactsCollector:
    """
    Thu thập dữ liệu từ Open Food Facts Search API v2.
    - Dùng page_size=50 để tránh lỗi 503 Server Unavailable từ cơ sở dữ liệu Open Food Facts
    - Tự động phân trang và chuyển đổi danh mục cho đến khi đạt đủ target_count (1.000)
    - Rate limit: delay 1.5s - 2.0s
    """
    PRIMARY_URL = "https://world.openfoodfacts.org/api/v2/search"
    FALLBACK_URL = "https://world.openfoodfacts.net/api/v2/search"

    def __init__(self, raw_dir: Path, delay_seconds: float = 1.0):
        self.raw_dir = Path(raw_dir)
        self.delay_seconds = delay_seconds
        self.session = get_session(
            "DS102-StudentCrawler/1.0 (UIT DS102 Statistical Machine Learning Project - contact: student@uit.edu.vn)"
        )

    def _fetch_api(self, params: dict):
        for endpoint in [self.PRIMARY_URL, self.FALLBACK_URL]:
            try:
                resp = self.session.get(endpoint, params=params, timeout=(15, 30))
                if resp.status_code == 200:
                    return resp.json()
            except Exception:
                continue
        return None

    def collect(self, target_count: int = 1000) -> Path:
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        raw_items: List[Dict[str, Any]] = []
        seen_codes = set()
        page_size = 50

        print(f"[*] [OpenFoodFactsCollector] Bắt đầu thu thập mục tiêu {target_count} sản phẩm...")

        cat_idx = 0
        current_page = 1

        while len(raw_items) < target_count and cat_idx < len(CATEGORIES):
            cat = CATEGORIES[cat_idx]
            print(f"[*] Đang lấy danh mục '{cat}' (page {current_page}, size={page_size})...")

            params = {
                "categories_tags": cat,
                "fields": FIELDS_QUERY,
                "page_size": page_size,
                "page": current_page,
            }

            try:
                data = self._fetch_api(params)
                if not data:
                    print(f"[-] Không thể tải danh mục '{cat}'. Chuyển danh mục tiếp theo...")
                    cat_idx += 1
                    current_page = 1
                    time.sleep(1.0)
                    continue

                products = data.get("products", [])
                if not products:
                    cat_idx += 1
                    current_page = 1
                    continue

                added_count = 0
                for p in products:
                    code = str(p.get("code", "")).strip()
                    if not code or code in seen_codes:
                        continue
                    seen_codes.add(code)
                    p["collected_category"] = cat
                    p["retrieved_at"] = get_current_utc_iso()
                    raw_items.append(p)
                    added_count += 1

                print(f"[+] Nhận {added_count} sản phẩm mới từ '{cat}'. Tổng hiện tại: {len(raw_items)}/{target_count}")

                current_page += 1
                if current_page > 3:  # Mỗi danh mục lấy tối đa 3 trang để đảm bảo đa dạng
                    cat_idx += 1
                    current_page = 1

            except Exception as e:
                print(f"[!] Lỗi kết nối khi lấy '{cat}': {e}")
                cat_idx += 1
                current_page = 1

            time.sleep(self.delay_seconds)

        out_path = self.raw_dir / "openfoodfacts_1000_raw.jsonl"
        save_jsonl(raw_items, out_path)
        print(f"[+] [OpenFoodFactsCollector] Đã lưu {len(raw_items)} sản phẩm thô vào {out_path}")
        return out_path
