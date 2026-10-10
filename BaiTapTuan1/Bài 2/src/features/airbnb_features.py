from pathlib import Path
import pandas as pd
import numpy as np


class AirbnbFeatureEngineer:
    """
    Tạo các đặc trưng ML cho bài toán Spatial Regression và Classification:
    - Multi-hot các tiện ích phổ biến (Wifi, Kitchen, Workspace, Air conditioning).
    - Đặc trưng khoảng cách tâm thành phố (Amsterdam Centraal: 52.3791, 4.9003).
    - Phân nhóm khoảng giá (price bins).
    - Lưu ý chống Target Leakage: Không đưa biến phản hồi sau thuê vào dự đoán giá ban đầu.
    """
    # Tọa độ trung tâm Amsterdam
    CENTER_LAT = 52.3791
    CENTER_LON = 4.9003

    def __init__(self, clean_path: Path, output_path: Path):
        self.clean_path = Path(clean_path)
        self.output_path = Path(output_path)

    def extract_features(self) -> pd.DataFrame:
        df = pd.read_csv(self.clean_path)

        # 1. Spatial feature: Khoảng cách Euclid xấp xỉ tới trung tâm thành phố (đơn vị độ)
        df["dist_to_center"] = np.sqrt(
            (df["latitude"] - self.CENTER_LAT) ** 2 + (df["longitude"] - self.CENTER_LON) ** 2
        )

        # 2. Tiện ích phổ biến (Multi-hot)
        amenities_str = df["amenities"].fillna("").str.lower()
        df["has_wifi"] = amenities_str.str.contains("wifi").astype(int)
        df["has_kitchen"] = amenities_str.str.contains("kitchen").astype(int)
        df["has_workspace"] = amenities_str.str.contains("workspace").astype(int)
        df["has_air_con"] = amenities_str.str.contains("air conditioning").astype(int)

        # 3. Phân loại phòng (Categorical encoding)
        df["is_entire_home"] = (df["room_type"] == "Entire home/apt").astype(int)

        # 4. Target phân loại khoảng giá (Low, Medium, High)
        df["price_category"] = pd.qcut(df["price"], q=3, labels=["low", "medium", "high"])

        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(self.output_path, index=False, encoding="utf-8-sig")
        print(f"[+] [AirbnbFeatureEngineer] Đã tạo đặc trưng cho {len(df)} listing -> {self.output_path}")
        return df
