from pathlib import Path
import pandas as pd
import numpy as np


class OpenFoodFactsFeatureEngineer:
    """
    Tạo các đặc trưng phục vụ Machine Learning:
    - Text features: độ dài, số lượng thành phần ước tính từ ingredients_text.
    - Derived features: tỷ lệ dinh dưỡng, cảnh báo đường/muối cao.
    - Leakage-safe features cho bài toán phân loại Nutri-Score.
    """
    def __init__(self, clean_path: Path, output_path: Path):
        self.clean_path = Path(clean_path)
        self.output_path = Path(output_path)

    def extract_features(self) -> pd.DataFrame:
        df = pd.read_csv(self.clean_path)

        # 1. Text feature từ ingredients_text
        df["ingredients_char_len"] = df["ingredients_text"].fillna("").str.len()
        df["ingredients_word_count"] = df["ingredients_text"].fillna("").apply(lambda s: len(s.split()) if s else 0)
        df["ingredients_item_count"] = df["ingredients_text"].fillna("").apply(lambda s: len([x for x in s.split(",") if x.strip()]) if s else 0)

        # 2. Đặc trưng phân loại & nhị phân
        df["has_allergens"] = df["allergens"].notna().astype(int)
        df["has_additives"] = (df["additives_n"].fillna(0) > 0).astype(int)

        # 3. Phân nhóm hàm lượng dinh dưỡng
        # Đường cao theo chuẩn WHO (>10g/100g)
        df["is_high_sugar"] = (df["sugars_100g"] > 10.0).astype(float)
        # Muối cao (>1.5g/100g)
        df["is_high_salt"] = (df["salt_100g"] > 1.5).astype(float)

        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(self.output_path, index=False, encoding="utf-8-sig")
        print(f"[+] [OpenFoodFactsFeatureEngineer] Đã tạo đặc trưng cho {len(df)} sản phẩm -> {self.output_path}")
        return df
