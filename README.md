# DS102 — HỌC MÁY THỐNG KÊ (THỰC HÀNH)

Repository lưu trữ các bài tập thực hành môn **DS102 – Học máy thống kê** (Trường ĐH Công nghệ Thông tin - ĐHQG-HCM).

---

## Danh Sách Bài Tập

### Tuần 1: Bài Tập Tuần 1 (`BaiTapTuan1/`)
* **Bài 1 (`BaiTapTuan1/Bài 1/`)**:
  * Thuật toán tối ưu hóa **Newton-Raphson** đa biến (`newton-raphson.py`).
  * Tìm điểm cực tiểu toàn cục của hàm mục tiêu dựa trên Gradient và ma trận Hessian.
* **Bài 2 (`BaiTapTuan1/Bài 2/`)**:
  * Thu thập dữ liệu web từ **Books to Scrape** (`https://books.toscrape.com`).
  * Bóc tách 50 trang danh mục (1.000 cuốn sách) bằng `requests` và `BeautifulSoup4`.
  * Lưu trữ dữ liệu sạch dưới đầy đủ các định dạng: **TSV, CSV, JSON** và cơ sở dữ liệu **SQLite** (`data/`).
  * Báo cáo và phân tích dữ liệu thực nghiệm trong Notebook (`notebooks/01_thuc_nghiem_books.ipynb`).

---

## Hướng Dẫn Cài Đặt & Chạy

1. **Cài đặt thư viện phụ thuộc**:
   ```bash
   pip install requests beautifulsoup4 pandas numpy
   ```

2. **Chạy Bài 1 (Newton-Raphson)**:
   ```bash
   python "BaiTapTuan1/Bài 1/newton-raphson.py"
   ```

3. **Chạy Bài 2 (Web Scraping)**:
   ```bash
   python "BaiTapTuan1/Bài 2/main.py"
   ```
