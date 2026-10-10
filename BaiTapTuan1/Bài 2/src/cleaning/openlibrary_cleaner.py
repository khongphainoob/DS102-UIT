import json
from pathlib import Path
from typing import Any, Dict, List
import pandas as pd
import numpy as np
from src.collectors.base import save_to_sqlite


class OpenLibraryCleaner:
    def __init__(self, raw_path: Path, processed_dir: Path):
        self.raw_path = Path(raw_path)
        self.processed_dir = Path(processed_dir)

    def clean(self) -> pd.DataFrame:
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        raw_records = []
        with self.raw_path.open("r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    raw_records.append(json.loads(line))

        main_rows = []
        rel_authors = []
        rel_subjects = []
        seen_works = set()

        for d in raw_records:
            work_key = d.get("key", "")
            if not work_key or work_key in seen_works:
                continue
            seen_works.add(work_key)

            title = str(d.get("title", "")).strip()
            if not title:
                continue

            # Authors
            authors = d.get("author_name") or []
            if isinstance(authors, str):
                authors = [authors]
            for author in authors:
                rel_authors.append({"work_key": work_key, "author_name": str(author).strip()})

            # Subjects
            subjects = d.get("subject") or []
            if isinstance(subjects, str):
                subjects = [subjects]
            if not subjects and d.get("queried_subject"):
                subjects = [d["queried_subject"]]

            for subj in subjects[:20]:  # Giới hạn 20 subject hàng đầu
                rel_subjects.append({"work_key": work_key, "subject": str(subj).strip()})

            # Languages
            languages = d.get("language") or []
            if isinstance(languages, str):
                languages = [languages]

            # Publishers
            publishers = d.get("publisher") or []
            if isinstance(publishers, str):
                publishers = [publishers]

            # Years
            publish_years = d.get("publish_year") or []
            pub_min = min(publish_years) if publish_years else np.nan
            pub_max = max(publish_years) if publish_years else np.nan

            edition_keys = d.get("edition_key") or []
            isbns = d.get("isbn") or []

            main_rows.append({
                "work_key": work_key,
                "edition_key": edition_keys[0] if edition_keys else np.nan,
                "title": title,
                "author_names": ", ".join(authors[:5]) if authors else np.nan,
                "author_count": len(authors),
                "first_publish_year": d.get("first_publish_year", np.nan),
                "publish_year_min": pub_min,
                "publish_year_max": pub_max,
                "edition_count": d.get("edition_count", 1),
                "language_count": len(languages),
                "languages": ", ".join(languages[:5]) if languages else np.nan,
                "publisher_count": len(publishers),
                "publishers": ", ".join(publishers[:3]) if publishers else np.nan,
                "subject_count": len(subjects),
                "subjects": "; ".join(subjects[:10]) if subjects else np.nan,
                "place_count": len(d.get("place", [])),
                "people_count": len(d.get("person", [])),
                "times_seen_in_search": d.get("readinglog_count", np.nan),
                "has_fulltext": bool(d.get("has_fulltext", False)),
                "ebook_access": d.get("ebook_access", np.nan),
                "cover_i": d.get("cover_i", np.nan),
                "isbn_count": len(isbns),
                "number_of_pages_median": d.get("number_of_pages_median", np.nan),
                "retrieved_at": d.get("retrieved_at", ""),
            })

        df_main = pd.DataFrame(main_rows)
        df_authors = pd.DataFrame(rel_authors, columns=["work_key", "author_name"]) if rel_authors else pd.DataFrame(columns=["work_key", "author_name"])
        df_subjects = pd.DataFrame(rel_subjects, columns=["work_key", "subject"]) if rel_subjects else pd.DataFrame(columns=["work_key", "subject"])

        # Xuất các bảng chính và bảng quan hệ
        main_csv = self.processed_dir / "openlibrary_1000_clean.csv"
        authors_csv = self.processed_dir / "openlibrary_authors.csv"
        subjects_csv = self.processed_dir / "openlibrary_subjects.csv"
        db_path = self.processed_dir / "openlibrary_1000.db"

        df_main.to_csv(main_csv, index=False, encoding="utf-8-sig")
        df_authors.to_csv(authors_csv, index=False, encoding="utf-8-sig")
        df_subjects.to_csv(subjects_csv, index=False, encoding="utf-8-sig")

        save_to_sqlite(df_main, "works", db_path)
        save_to_sqlite(df_authors, "work_authors", db_path)
        save_to_sqlite(df_subjects, "work_subjects", db_path)

        print(f"[+] [OpenLibraryCleaner] Đã làm sạch {len(df_main)} tác phẩm -> {main_csv} và {db_path}")
        print(f"[+] [OpenLibraryCleaner] Bảng quan hệ: {len(df_authors)} tác giả, {len(df_subjects)} chủ đề")
        return df_main
