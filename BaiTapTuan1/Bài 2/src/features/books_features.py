from pathlib import Path
import pandas as pd
import numpy as np


class BooksFeatureEngineer:
    def __init__(self, clean_path: Path, output_path: Path):
        self.clean_path = Path(clean_path)
        self.output_path = Path(output_path)

    def extract_features(self) -> pd.DataFrame:
        df = pd.read_csv(self.clean_path)

        # 1. Feature kỹ thuật từ văn bản tiêu đề
        df["title_char_length"] = df["title"].str.len()
        df["title_word_count"] = df["title"].str.split().str.len()

        # 2. Phân khoảng giá (Binning cho bài toán phân loại)
        bins = [0, 20, 40, np.inf]
        labels = ["budget", "standard", "premium"]
        df["price_tier"] = pd.cut(df["price_gbp"], bins=bins, labels=labels)

        # 3. Target phân loại sao (High rating vs Normal rating)
        df["is_high_rated"] = (df["rating_star"] >= 4).astype(int)

        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(self.output_path, index=False, encoding="utf-8-sig")
        print(f"[+] [BooksFeatureEngineer] Trích xuất đặc trưng hoàn tất: {len(df)} dòng -> {self.output_path}")
        return df
