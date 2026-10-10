import json
import re
from pathlib import Path
import pandas as pd
from src.collectors.base import save_to_sqlite

RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}


class BooksCleaner:
    def __init__(self, raw_path: Path, processed_dir: Path):
        self.raw_path = Path(raw_path)
        self.processed_dir = Path(processed_dir)

    def clean(self) -> pd.DataFrame:
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        rows = []
        with self.raw_path.open("r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    rows.append(json.loads(line))

        df = pd.DataFrame(rows)

        # 1. Tên sách
        df["title"] = df["raw_title"].fillna("").astype(str).str.strip()

        # 2. Giá (£ -> float)
        def parse_price(val):
            if not isinstance(val, str):
                return None
            m = re.search(r"([0-9]+\.[0-9]+|[0-9]+)", val)
            return float(m.group(1)) if m else None

        df["price_gbp"] = df["raw_price"].apply(parse_price)

        # 3. Đánh giá số sao
        def parse_rating(classes):
            if isinstance(classes, list):
                for c in classes:
                    if c in RATING_MAP:
                        return RATING_MAP[c]
            return None

        df["rating_star"] = df["raw_rating_classes"].apply(parse_rating)

        # 4. Trạng thái còn hàng (boolean)
        df["is_in_stock"] = df["raw_availability"].astype(str).str.lower().str.contains("in stock")

        # 5. Loại bỏ duplicate nếu có
        df = df.drop_duplicates(subset=["product_url"]).copy()

        # Lựa chọn các cột chuẩn
        clean_cols = [
            "title",
            "price_gbp",
            "rating_star",
            "is_in_stock",
            "product_url",
            "thumbnail_url",
            "page_number",
            "retrieved_at",
        ]
        df_clean = df[clean_cols]

        # Xuất file
        csv_path = self.processed_dir / "books_1000_clean.csv"
        db_path = self.processed_dir / "books_1000.db"

        df_clean.to_csv(csv_path, index=False, encoding="utf-8-sig")
        save_to_sqlite(df_clean, "books", db_path)

        print(f"[+] [BooksCleaner] Đã làm sạch {len(df_clean)} cuốn sách -> {csv_path}")
        return df_clean
