import re
from datetime import datetime, timezone
from urllib.parse import urljoin
from bs4 import BeautifulSoup


RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}


class Parser:
    """
    Parser bóc tách dữ liệu từ HTML trang Books to Scrape.
    Trích xuất: title, price_gbp, rating_star, is_in_stock, url, thumbnail_url.
    """

    def __init__(self, base_url: str = "https://books.toscrape.com/catalogue/"):
        self.base_url = base_url
        self.product_selector = "article.product_pod"
        self.title_selector = "h3 a"
        self.price_selector = "p.price_color"
        self.rating_selector = "p.star-rating"
        self.availability_selector = "p.instock.availability"
        self.thumbnail_selector = "div.image_container img.thumbnail"

    def clean_text(self, text: str) -> str:
        if not text:
            return ""
        return " ".join(text.split())

    def convert_price(self, text: str) -> float | None:
        """
        Làm sạch ký tự tiền tệ (£) và chuyển sang float.
        Ví dụ: '£51.77' -> 51.77
        """
        cleaned = self.clean_text(text)
        match = re.search(r"([0-9]+\.[0-9]+|[0-9]+)", cleaned)
        if match:
            return float(match.group(1))
        return None

    def extract_rating(self, rating_tag) -> int | None:
        """
        Chuyển class dạng ['star-rating', 'Three'] thành số nguyên 3.
        """
        if not rating_tag:
            return None
        classes = rating_tag.get("class", [])
        for cls in classes:
            if cls in RATING_MAP:
                return RATING_MAP[cls]
        return None

    def parse(self, html: str, current_page_url: str, page_number: int = 1):
        soup = BeautifulSoup(html, "html.parser")
        cards = soup.select(self.product_selector)

        if not cards:
            return []

        products = []
        now_iso = datetime.now(timezone.utc).isoformat()

        for card in cards:
            # 1. Tên sách: Lấy thuộc tính 'title' để tránh bị cắt chuỗi '...'
            title_tag = card.select_one(self.title_selector)
            if not title_tag:
                continue

            title = title_tag.get("title") or self.clean_text(title_tag.get_text())
            href = title_tag.get("href", "")
            product_url = urljoin(current_page_url, href)

            # 2. Giá tiền
            price_tag = card.select_one(self.price_selector)
            price_text = self.clean_text(price_tag.get_text()) if price_tag else ""
            price_gbp = self.convert_price(price_text)

            # 3. Đánh giá số sao (1-5)
            rating_tag = card.select_one(self.rating_selector)
            rating_star = self.extract_rating(rating_tag)

            # 4. Trạng thái còn hàng
            avail_tag = card.select_one(self.availability_selector)
            avail_text = self.clean_text(avail_tag.get_text()) if avail_tag else ""
            is_in_stock = "in stock" in avail_text.lower()

            # 5. Thumbnail URL
            thumb_tag = card.select_one(self.thumbnail_selector)
            thumb_src = thumb_tag.get("src", "") if thumb_tag else ""
            thumbnail_url = urljoin(current_page_url, thumb_src) if thumb_src else ""

            products.append({
                "title": title,
                "price_gbp": price_gbp,
                "price_text": price_text,
                "rating_star": rating_star,
                "is_in_stock": is_in_stock,
                "product_url": product_url,
                "thumbnail_url": thumbnail_url,
                "page_number": page_number,
                "retrieved_at": now_iso,
            })

        return products
