import time
from urllib.parse import urljoin
import requests


class Crawler:
    """
    Crawler cho trang books.toscrape.com
    Dùng requests.Session với headers chuẩn, tuân thủ rate limit và timeout an toàn.
    Không dùng Playwright vì trang web hoàn toàn là HTML tĩnh.
    """
    BASE_URL = "https://books.toscrape.com/catalogue/"
    START_URL = "https://books.toscrape.com/catalogue/page-1.html"

    def __init__(self, delay_seconds: float = 0.5):
        self.delay_seconds = delay_seconds
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "DS102-LearningCrawler/1.0 (UIT DS102 Machine Learning Assignment)",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        })

    def get_page_url(self, page_number: int) -> str:
        return f"{self.BASE_URL}page-{page_number}.html"

    def fetch_page(self, page_number: int) -> str:
        url = self.get_page_url(page_number)
        response = self.session.get(url, timeout=(10, 30))
        if response.status_code == 404:
            return ""
        response.raise_for_status()

        content_type = response.headers.get("Content-Type", "").lower()
        if "html" not in content_type:
            raise ValueError(f"Phản hồi từ {url} không phải HTML.")

        return response.text

    def crawl_pages(self, max_pages: int = 50):
        """
        Duyệt lần lượt các trang từ 1 đến max_pages.
        Mỗi trang có 20 cuốn sách. Tổng cộng 50 trang = 1.000 cuốn sách.
        """
        pages_content = []
        for page in range(1, max_pages + 1):
            if page > 1 and self.delay_seconds > 0:
                time.sleep(self.delay_seconds)

            url = self.get_page_url(page)
            print(f"[*] Đang tải trang {page}/{max_pages}: {url}")
            try:
                html = self.fetch_page(page)
                if not html:
                    print(f"[*] Hết trang tại trang {page}. Dừng crawl.")
                    break
                pages_content.append((page, url, html))
            except Exception as e:
                print(f"[!] Lỗi khi tải trang {page}: {e}")
                break

        return pages_content
