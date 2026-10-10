import json
from pathlib import Path
from typing import Any, Dict, List
import pandas as pd
import numpy as np
from src.collectors.base import save_to_sqlite


NUTRITION_KEYS = [
    ("energy_kcal_100g", ["energy-kcal_100g", "energy-kcal"]),
    ("fat_100g", ["fat_100g", "fat"]),
    ("saturated_fat_100g", ["saturated-fat_100g", "saturated-fat"]),
    ("carbohydrates_100g", ["carbohydrates_100g", "carbohydrates"]),
    ("sugars_100g", ["sugars_100g", "sugars"]),
    ("fiber_100g", ["fiber_100g", "fiber"]),
    ("proteins_100g", ["proteins_100g", "proteins"]),
    ("salt_100g", ["salt_100g", "salt"]),
    ("sodium_100g", ["sodium_100g", "sodium"]),
]


class OpenFoodFactsCleaner:
    def __init__(self, raw_path: Path, processed_dir: Path):
        self.raw_path = Path(raw_path)
        self.processed_dir = Path(processed_dir)

    def _extract_nutriment(self, nutriments: Dict[str, Any], candidates: List[str]):
        if not isinstance(nutriments, dict):
            return np.nan
        for key in candidates:
            if key in nutriments and nutriments[key] is not None:
                try:
                    val = float(nutriments[key])
                    # Kiểm tra khoảng hợp lý (không âm, không quá 100g ngoại trừ energy kcal)
                    if val < 0:
                        return np.nan
                    if "energy" not in key and val > 105:
                        # Outlier bất hợp lý
                        return np.nan
                    return val
                except (ValueError, TypeError):
                    continue
        return np.nan

    def _parse_analysis_tag(self, tags: List[str], target: str) -> bool | None:
        if not isinstance(tags, list):
            return None
        joined = " ".join(tags).lower()
        if f"en:{target}" in joined:
            return True
        if f"en:non-{target}" in joined:
            return False
        return None

    def clean(self) -> pd.DataFrame:
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        raw_records = []
        with self.raw_path.open("r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    raw_records.append(json.loads(line))

        cleaned_rows = []
        for r in raw_records:
            code = str(r.get("code", "")).strip()
            name = str(r.get("product_name", "")).strip()
            if not code or not name:
                continue

            nutriments = r.get("nutriments", {})
            nutri_dict = {}
            valid_nutri_count = 0
            for col_name, candidates in NUTRITION_KEYS:
                val = self._extract_nutriment(nutriments, candidates)
                nutri_dict[col_name] = val
                if not np.isnan(val):
                    valid_nutri_count += 1

            # Lấy nhãn dinh dưỡng (nutrition_grade) A-E
            grade = r.get("nutrition_grades") or r.get("nutrition_grade_fr") or ""
            grade = str(grade).strip().upper()
            if grade not in ("A", "B", "C", "D", "E"):
                grade = np.nan

            analysis_tags = r.get("ingredients_analysis_tags", [])
            vegan = self._parse_analysis_tag(analysis_tags, "vegan")
            vegetarian = self._parse_analysis_tag(analysis_tags, "vegetarian")
            palm_oil_free = self._parse_analysis_tag(analysis_tags, "palm-oil-free")

            # Xử lý text thành phần
            ing_text = r.get("ingredients_text") or ""
            ing_text = " ".join(str(ing_text).split())

            additives = r.get("additives_n")
            try:
                additives_n = int(additives) if additives is not None else np.nan
            except (ValueError, TypeError):
                additives_n = np.nan

            row = {
                "code": code,
                "product_name": name,
                "brands": str(r.get("brands", "")).strip(),
                "countries": str(r.get("countries", "")).strip(),
                "categories": str(r.get("categories", "")).strip(),
                "labels": str(r.get("labels", "")).strip(),
                "packaging": str(r.get("packaging", "")).strip(),
                "stores": str(r.get("stores", "")).strip(),
                "quantity": str(r.get("quantity", "")).strip(),
                **nutri_dict,
                "ingredients_text": ing_text if ing_text else np.nan,
                "allergens": str(r.get("allergens", "")).strip() or np.nan,
                "additives_n": additives_n,
                "nutrition_grade": grade,
                "vegan": vegan,
                "vegetarian": vegetarian,
                "palm_oil_free": palm_oil_free,
                "completeness": r.get("completeness", np.nan),
                "last_modified_t": r.get("last_modified_t", np.nan),
                "retrieved_at": r.get("retrieved_at", ""),
                "valid_nutri_count": valid_nutri_count,
            }
            cleaned_rows.append(row)

        df = pd.DataFrame(cleaned_rows)

        # Deduplicate theo code
        df = df.drop_duplicates(subset=["code"]).copy()

        # Lưu ý quy tắc chuẩn hóa: missing giữ NaN, không ép thành 0
        df = df.drop(columns=["valid_nutri_count"])

        csv_path = self.processed_dir / "openfoodfacts_1000_clean.csv"
        db_path = self.processed_dir / "openfoodfacts_1000.db"

        df.to_csv(csv_path, index=False, encoding="utf-8-sig")
        save_to_sqlite(df, "food_products", db_path)

        print(f"[+] [OpenFoodFactsCleaner] Đã làm sạch {len(df)} sản phẩm -> {csv_path}")
        return df
