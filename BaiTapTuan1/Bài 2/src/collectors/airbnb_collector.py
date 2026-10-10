import gzip
import shutil
from pathlib import Path
import requests
from src.collectors.base import compute_checksum, get_current_utc_iso


DEFAULT_AIRBNB_URL = "https://data.insideairbnb.com/the-netherlands/north-holland/amsterdam/2026-09-16/data/listings.csv.gz"


class AirbnbCollector:
    """
    Thu thập dữ liệu Inside Airbnb từ file nén listings.csv.gz chính thức.
    - Không cào trực tiếp giao diện Airbnb (tuân thủ điều khoản và tránh IP ban).
    - Tải snapshot cụ thể, lưu trữ kèm sha256 checksum để đảm bảo tính tái lập (reproducibility).
    - License: Creative Commons Attribution 4.0 International.
    """

    def __init__(self, raw_dir: Path, download_url: str = DEFAULT_AIRBNB_URL):
        self.raw_dir = Path(raw_dir)
        self.download_url = download_url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }

    def collect(self) -> Path:
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        gz_path = self.raw_dir / "listings.csv.gz"
        extracted_csv = self.raw_dir / "listings_raw.csv"

        print(f"[*] [AirbnbCollector] Bắt đầu tải Inside Airbnb snapshot từ: {self.download_url}")
        resp = requests.get(self.download_url, headers=self.headers, stream=True, timeout=(20, 120))
        resp.raise_for_status()

        total_bytes = 0
        with gz_path.open("wb") as f_out:
            for chunk in resp.iter_content(chunk_size=65536):
                if chunk:
                    f_out.write(chunk)
                    total_bytes += len(chunk)

        print(f"[+] Tải thành công {total_bytes / (1024 * 1024):.2f} MB -> {gz_path}")

        # Tính sha256 checksum
        checksum = compute_checksum(gz_path)
        meta_file = self.raw_dir / "metadata.txt"
        meta_file.write_text(
            f"Source URL: {self.download_url}\n"
            f"Retrieved At: {get_current_utc_iso()}\n"
            f"SHA256: {checksum}\n"
            f"License: Creative Commons Attribution 4.0 International\n",
            encoding="utf-8"
        )
        print(f"[+] SHA256 Checksum: {checksum}")

        # Giải nén ra CSV thô
        print(f"[*] Đang giải nén {gz_path.name}...")
        with gzip.open(gz_path, "rb") as f_in:
            with extracted_csv.open("wb") as f_out:
                shutil.copyfileobj(f_in, f_out)

        print(f"[+] [AirbnbCollector] Đã giải nén thành công -> {extracted_csv}")
        return extracted_csv
