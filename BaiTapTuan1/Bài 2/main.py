import argparse
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"

# Đảm bảo import được các module trong src/
sys.path.insert(0, str(ROOT))

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from src.crawler import Crawler
from src.exporter import export_data
from src.parser import Parser


def crawl_books(pages_count: int = 50, delay_sec: float = 0.2):
    print("=" * 60)
    print(" BẮT ĐẦU THU THẬP DỮ LIỆU TỪ BOOKS TO SCRAPE")
    print(f" Target: {pages_count} trang (~ {pages_count * 20} cuốn sách)")
    print("=" * 60)

    crawler = Crawler(delay_seconds=delay_sec)
    page_parser = Parser()

    pages = crawler.crawl_pages(max_pages=pages_count)
    if not pages:
        print("[!] Không thu thập được trang nào.")
        return 1

    all_books = []
    seen_urls = set()

    for page_num, page_url, html in pages:
        books = page_parser.parse(html, current_page_url=page_url, page_number=page_num)
        for b in books:
            if b["product_url"] not in seen_urls:
                seen_urls.add(b["product_url"])
                all_books.append(b)

    print(f"\n[+] Tổng số cuốn sách thu thập thành công (unique): {len(all_books)}")

    # Xuất dữ liệu dưới đầy đủ các định dạng: CSV, TSV, JSON và SQLite
    export_data(all_books, DATA_DIR)

    # Thống kê nhanh
    prices = [b["price_gbp"] for b in all_books if b["price_gbp"] is not None]
    ratings = [b["rating_star"] for b in all_books if b["rating_star"] is not None]
    if prices:
        print("\n--- THỐNG KÊ NHANH ---")
        print(f" Giá trung bình: £{sum(prices)/len(prices):.2f}")
        print(f" Giá thấp nhất: £{min(prices):.2f} | Giá cao nhất: £{max(prices):.2f}")
    if ratings:
        print(f" Số sao trung bình: {sum(ratings)/len(ratings):.2f} / 5.0")

    print("\n Hoàn tất! Dữ liệu được lưu tại thư mục:", DATA_DIR)
    return 0


def run_extended_source(source_name: str):
    """
    Hỗ trợ thu thập bổ sung các nguồn dữ liệu nâng cao (Open Food Facts, Inside Airbnb, Open Library)
    """
    raw_dir = DATA_DIR / "raw" / source_name
    processed_dir = DATA_DIR / "other_datasets" / source_name

    if source_name == "openfoodfacts":
        from src.collectors.openfoodfacts_collector import OpenFoodFactsCollector
        from src.cleaning.openfoodfacts_cleaner import OpenFoodFactsCleaner
        from src.features.openfoodfacts_features import OpenFoodFactsFeatureEngineer

        print("\n[*] Đang thu thập Open Food Facts...")
        collector = OpenFoodFactsCollector(raw_dir=raw_dir)
        raw_path = collector.collect(target_count=1000)
        cleaner = OpenFoodFactsCleaner(raw_path=raw_path, processed_dir=processed_dir)
        cleaner.clean()
        engineer = OpenFoodFactsFeatureEngineer(
            clean_path=processed_dir / "openfoodfacts_1000_clean.csv",
            output_path=processed_dir / "openfoodfacts_features.csv"
        )
        engineer.extract_features()

    elif source_name == "airbnb":
        from src.collectors.airbnb_collector import AirbnbCollector
        from src.cleaning.airbnb_cleaner import AirbnbCleaner
        from src.features.airbnb_features import AirbnbFeatureEngineer

        print("\n[*] Đang thu thập Inside Airbnb snapshot...")
        collector = AirbnbCollector(raw_dir=raw_dir)
        raw_path = collector.collect()
        cleaner = AirbnbCleaner(raw_csv_path=raw_path, processed_dir=processed_dir)
        cleaner.clean(target_rows=1000)
        engineer = AirbnbFeatureEngineer(
            clean_path=processed_dir / "airbnb_1000_clean.csv",
            output_path=processed_dir / "airbnb_features.csv"
        )
        engineer.extract_features()

    elif source_name == "openlibrary":
        from src.collectors.openlibrary_collector import OpenLibraryCollector
        from src.cleaning.openlibrary_cleaner import OpenLibraryCleaner
        from src.features.openlibrary_features import OpenLibraryFeatureEngineer

        print("\n[*] Đang thu thập Open Library...")
        collector = OpenLibraryCollector(raw_dir=raw_dir)
        raw_path = collector.collect(target_count=1000)
        cleaner = OpenLibraryCleaner(raw_path=raw_path, processed_dir=processed_dir)
        cleaner.clean()
        engineer = OpenLibraryFeatureEngineer(
            clean_path=processed_dir / "openlibrary_1000_clean.csv",
            output_path=processed_dir / "openlibrary_features.csv"
        )
        engineer.extract_features()

    print(f"[+] Nguồn '{source_name}' đã được lưu tại: {processed_dir}")


def main():
    parser = argparse.ArgumentParser(
        description="Thu thập dữ liệu Web cho Machine Learning (DS102 - Bài 2 Tuần 1)"
    )
    parser.add_argument(
        "--source",
        choices=["books", "openfoodfacts", "airbnb", "openlibrary", "all"],
        default="books",
        help="Nguồn dữ liệu cần thu thập. Mặc định: books (Books to Scrape)",
    )
    parser.add_argument(
        "--pages",
        type=int,
        default=50,
        help="Số trang Books to Scrape (tối đa 50 trang = 1000 sách). Mặc định: 50",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.2,
        help="Thời gian nghỉ (giây) giữa các request. Mặc định: 0.2s",
    )

    args = parser.parse_args()

    if args.source == "books":
        return crawl_books(pages_count=args.pages, delay_sec=args.delay)
    elif args.source == "all":
        crawl_books(pages_count=args.pages, delay_sec=args.delay)
        for s in ["openfoodfacts", "airbnb", "openlibrary"]:
            run_extended_source(s)
    else:
        run_extended_source(args.source)
    return 0


if __name__ == "__main__":
    sys.exit(main())