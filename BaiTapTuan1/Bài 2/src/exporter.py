import csv
import json
import sqlite3
from pathlib import Path


FIELDS = [
    "title",
    "price_gbp",
    "price_text",
    "rating_star",
    "is_in_stock",
    "product_url",
    "thumbnail_url",
    "page_number",
    "retrieved_at",
]


def safe_cell(value):
    """
    Ngăn chặn CSV formula injection nếu ô bắt đầu bằng =, +, -, @.
    """
    if isinstance(value, str) and value.lstrip().startswith(("=", "+", "-", "@")):
        return "'" + value
    return value


def save_json(products, path: Path):
    with path.open("w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=2)


def save_csv(products, path: Path, delimiter: str = ","):
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS, delimiter=delimiter)
        writer.writeheader()
        for p in products:
            row = {k: safe_cell(p.get(k)) for k in FIELDS}
            writer.writerow(row)


def save_sqlite(products, path: Path):
    conn = sqlite3.connect(str(path))
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            price_gbp REAL,
            price_text TEXT,
            rating_star INTEGER,
            is_in_stock INTEGER,
            product_url TEXT UNIQUE,
            thumbnail_url TEXT,
            page_number INTEGER,
            retrieved_at TEXT
        )
    """)
    for p in products:
        cursor.execute("""
            INSERT OR REPLACE INTO books (
                title, price_gbp, price_text, rating_star, is_in_stock,
                product_url, thumbnail_url, page_number, retrieved_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            p.get("title"),
            p.get("price_gbp"),
            p.get("price_text"),
            p.get("rating_star"),
            1 if p.get("is_in_stock") else 0,
            p.get("product_url"),
            p.get("thumbnail_url"),
            p.get("page_number"),
            p.get("retrieved_at")
        ))
    conn.commit()
    conn.close()


def export_data(products, output_dir: Path):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    save_json(products, output_dir / "books.json")
    save_json(products, output_dir / "products.json")
    save_csv(products, output_dir / "books.csv", delimiter=",")
    save_csv(products, output_dir / "products.csv", delimiter=",")
    save_csv(products, output_dir / "books.tsv", delimiter="\t")
    save_csv(products, output_dir / "products.tsv", delimiter="\t")
    save_sqlite(products, output_dir / "books.db")
    print(f"[+] Đã xuất {len(products)} bản ghi ra TSV, CSV, JSON và SQLite tại {output_dir}")
