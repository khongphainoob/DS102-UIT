import time
from pathlib import Path
from typing import Dict, List, Any
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from src.collectors.base import get_session, save_jsonl, get_current_utc_iso


class BooksCollector:
    """
    Bộ thu thập dữ liệu từ Books to Scrape (http://books.toscrape.com)
    - Kỹ thuật: HTTP GET + BeautifulSoup4
    - Không cần JavaScript / Playwright
    - Phân trang: 50 trang (mỗi trang 20 cuốn = 1.000 cuốn)
    """
    BASE_URL = "https://books.toscrape.com/catalogue/"

    def __init__(self, raw_dir: Path, delay_seconds: float = 0.2):
        self.raw_dir = Path(raw_dir)
        self.delay_seconds = delay_seconds
        self.session = get_session("DS102-BooksCollector/1.0")

    def collect(self, max_pages: int = 50) -> Path:
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        raw_items: List[Dict[str, Any]] = []
        seen_urls = set()

        print(f"[*] [BooksCollector] Bắt đầu thu thập tối đa {max_pages} trang...")

        for page in range(1, max_pages + 1):
            if page > 1 and self.delay_seconds > 0:
                time.sleep(self.delay_seconds)

            url = f"{self.BASE_URL}page-{page}.html"
            try:
                resp = self.session.get(url, timeout=(10, 30))
                if resp.status_code == 404:
                    print(f"[*] Hết trang tại {page}. Dừng.")
                    break
                resp.raise_for_status()

                soup = BeautifulSoup(resp.text, "html.parser")
                cards = soup.select("article.product_pod")

                for card in cards:
                    title_tag = card.select_one("h3 a")
                    if not title_tag:
                        continue
                    title_full = title_tag.get("title") or title_tag.get_text(strip=True)
                    rel_url = title_tag.get("href", "")
                    prod_url = urljoin(url, rel_url)

                    if prod_url in seen_urls:
                        continue
                    seen_urls.add(prod_url)

                    price_tag = card.select_one("p.price_color")
                    price_raw = price_tag.get_text(strip=True) if price_tag else ""

                    rating_tag = card.select_one("p.star-rating")
                    rating_classes = rating_tag.get("class", []) if rating_tag else []

                    avail_tag = card.select_one("p.instock.availability")
                    avail_raw = avail_tag.get_text(strip=True) if avail_tag else ""

                    img_tag = card.select_one("div.image_container img.thumbnail")
                    img_src = img_tag.get("src", "") if img_tag else ""
                    thumb_url = urljoin(url, img_src) if img_src else ""

                    raw_items.append({
                        "raw_title": title_full,
                        "raw_price": price_raw,
                        "raw_rating_classes": rating_classes,
                        "raw_availability": avail_raw,
                        "product_url": prod_url,
                        "thumbnail_url": thumb_url,
                        "page_number": page,
                        "retrieved_at": get_current_utc_iso(),
                    })
            except Exception as e:
                print(f"[!] Lỗi khi crawl trang {page}: {e}")
                break

        out_path = self.raw_dir / "books_1000_raw.jsonl"
        save_jsonl(raw_items, out_path)
        print(f"[+] [BooksCollector] Đã lưu {len(raw_items)} bản ghi thô vào {out_path}")
        return out_path
