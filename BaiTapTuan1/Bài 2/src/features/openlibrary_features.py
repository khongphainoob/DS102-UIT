from pathlib import Path
import pandas as pd
import numpy as np


class OpenLibraryFeatureEngineer:
    """
    Tạo các đặc trưng cho Open Library:
    - Target Classification: publish_decade (nhóm thập kỷ xuất bản).
    - Text Features: Độ dài tiêu đề, số từ.
    - Diversity Features: Đa dạng chủ đề, đa ngôn ngữ.
    - Leakage Prevention: Cảnh báo loại bỏ first_publish_year khi dự đoán decade.
    """
    def __init__(self, clean_path: Path, output_path: Path):
        self.clean_path = Path(clean_path)
        self.output_path = Path(output_path)

    def extract_features(self) -> pd.DataFrame:
        df = pd.read_csv(self.clean_path)

        # 1. Target phân loại thập kỷ xuất bản (Decade)
        def map_decade(year):
            if pd.isna(year):
                return np.nan
            y = int(year)
            if y < 1960:
                return "pre-1960"
            elif y < 1980:
                return "1960s-1970s"
            elif y < 2000:
                return "1980s-1990s"
            elif y < 2010:
                return "2000s"
            else:
                return "2010s-present"

        df["publish_decade"] = df["first_publish_year"].apply(map_decade)

        # 2. Text Feature cho bài toán NLP / Recommendation
        df["title_char_length"] = df["title"].str.len()
        df["title_word_count"] = df["title"].str.split().str.len()

        # 3. Indicator flags
        df["is_multilingual"] = (df["language_count"] > 1).astype(int)
        df["is_multi_author"] = (df["author_count"] > 1).astype(int)
        df["has_cover_image"] = df["cover_i"].notna().astype(int)

        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(self.output_path, index=False, encoding="utf-8-sig")
        print(f"[+] [OpenLibraryFeatureEngineer] Đã tạo đặc trưng cho {len(df)} tác phẩm -> {self.output_path}")
        return df
