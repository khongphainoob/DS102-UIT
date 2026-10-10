import json
import re
from pathlib import Path
import pandas as pd
import numpy as np
from src.collectors.base import save_to_sqlite, get_current_utc_iso


SELECTED_COLUMNS = [
    "id",
    "host_id",
    "host_since",
    "host_response_rate",
    "host_acceptance_rate",
    "host_is_superhost",
    "host_listings_count",
    "neighbourhood_cleansed",
    "latitude",
    "longitude",
    "property_type",
    "room_type",
    "accommodates",
    "bathrooms_text",
    "bedrooms",
    "beds",
    "amenities",
    "price",
    "minimum_nights",
    "maximum_nights",
    "availability_30",
    "availability_60",
    "availability_90",
    "availability_365",
    "number_of_reviews",
    "number_of_reviews_ltm",
    "reviews_per_month",
    "review_scores_rating",
    "review_scores_accuracy",
    "review_scores_cleanliness",
    "review_scores_checkin",
    "review_scores_communication",
    "review_scores_location",
    "review_scores_value",
    "instant_bookable",
    "calculated_host_listings_count",
]


class AirbnbCleaner:
    def __init__(self, raw_csv_path: Path, processed_dir: Path):
        self.raw_csv_path = Path(raw_csv_path)
        self.processed_dir = Path(processed_dir)

    def clean(self, target_rows: int = 1000) -> pd.DataFrame:
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        print(f"[*] [AirbnbCleaner] Đọc file thô: {self.raw_csv_path}...")

        # Đọc dữ liệu (chỉ lấy các cột quan tâm để tối ưu bộ nhớ)
        df = pd.read_csv(self.raw_csv_path, usecols=lambda c: c in SELECTED_COLUMNS, low_memory=False)

        # 1. Chuyển đổi giá tiền chuỗi sang số ($120.00 -> 120.0)
        def parse_price(val):
            if pd.isna(val):
                return np.nan
            s = str(val).replace("$", "").replace(",", "").strip()
            try:
                return float(s)
            except ValueError:
                return np.nan

        df["price_numeric"] = df["price"].apply(parse_price)

        # 2. Làm sạch tỷ lệ (95% -> 0.95)
        def parse_pct(val):
            if pd.isna(val):
                return np.nan
            s = str(val).replace("%", "").strip()
            try:
                return float(s) / 100.0
            except ValueError:
                return np.nan

        if "host_response_rate" in df.columns:
            df["host_response_rate"] = df["host_response_rate"].apply(parse_pct)
        if "host_acceptance_rate" in df.columns:
            df["host_acceptance_rate"] = df["host_acceptance_rate"].apply(parse_pct)

        # 3. Chuyển đổi boolean 't'/'f'
        for bool_col in ["host_is_superhost", "instant_bookable"]:
            if bool_col in df.columns:
                df[bool_col] = df[bool_col].map({"t": 1, "f": 0, True: 1, False: 0})

        # 4. Parse amenities và đếm số lượng tiện ích
        def parse_amenities_count(val):
            if pd.isna(val):
                return 0
            try:
                items = json.loads(val)
                return len(items) if isinstance(items, list) else 0
            except Exception:
                return len(str(val).split(","))

        df["amenities_count"] = df["amenities"].apply(parse_amenities_count)

        # 5. Lọc các dòng thiếu price, latitude, longitude
        df = df.dropna(subset=["price_numeric", "latitude", "longitude"]).copy()

        # 6. Loại bỏ giá bất hợp lý / winsorize (chỉ lấy giá từ $10 đến $1500)
        df = df[(df["price_numeric"] >= 10.0) & (df["price_numeric"] <= 1500.0)].copy()

        # 7. Deduplicate theo id
        df = df.drop_duplicates(subset=["id"]).copy()

        # 8. Cắt đúng target_rows (1000 dòng sạch)
        df_1000 = df.head(target_rows).copy()

        # 9. Thêm log1p(price) làm target cho regression
        df_1000["log_price"] = np.log1p(df_1000["price_numeric"])
        df_1000["retrieved_at"] = get_current_utc_iso()

        # Đổi tên cột price sạch
        df_1000["price"] = df_1000["price_numeric"]
        df_1000 = df_1000.drop(columns=["price_numeric"])

        # Xuất file
        csv_path = self.processed_dir / "airbnb_1000_clean.csv"
        db_path = self.processed_dir / "airbnb_1000.db"

        df_1000.to_csv(csv_path, index=False, encoding="utf-8-sig")
        save_to_sqlite(df_1000, "listings", db_path)

        print(f"[+] [AirbnbCleaner] Đã làm sạch {len(df_1000)} listing -> {csv_path} và {db_path}")
        return df_1000
