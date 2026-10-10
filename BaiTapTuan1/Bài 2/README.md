# BÀI TẬP TUẦN 1 — THU THẬP DỮ LIỆU TỪ WEB (WEB SCRAPING)

**Môn học**: DS102 – Học máy thống kê  
**Bài tập**: Bài 2  
**Yêu cầu đề bài**: *Thực hiện thu thập dữ liệu từ một trang web bất kỳ. Lưu dữ liệu dưới dạng các file TSV, CSV, hoặc JSON.*  
**Trang web lựa chọn**: [Books to Scrape](https://books.toscrape.com/)  

---

## 1. Phương Pháp & Kỹ Thuật Thực Hiện

1. **Giao thức & Công nghệ**:
   - Sử dụng `requests.Session` kết hợp `BeautifulSoup4` bóc tách HTML tĩnh.
   - **Không sử dụng Playwright / Selenium**: Giúp chương trình tinh gọn, tốc độ cao (chạy toàn bộ 50 trang ~20 giây), không phụ thuộc môi trường trình duyệt bên ngoài.
2. **Quy mô thu thập**:
   - Duyệt qua toàn bộ **50 trang** danh mục (mỗi trang 20 cuốn sách), thu thập đủ **1.000 cuốn sách**.
3. **Các thuộc tính thu thập**:
   - `title`: Tên sách đầy đủ (lấy từ thuộc tính `title` thẻ `<a>` để tránh bị cắt ngắn chuỗi `...`).
   - `price_gbp`: Giá bán dạng số thực (loại bỏ ký tự `£`, regex chuyển thành float).
   - `price_text`: Chuỗi giá nguyên bản phục vụ kiểm tra đối chiếu.
   - `rating_star`: Ánh xạ từ CSS class số sao (`One` $\rightarrow$ 1, `Two` $\rightarrow$ 2, ..., `Five` $\rightarrow$ 5).
   - `is_in_stock`: Biến boolean kiểm tra tình trạng còn hàng (`In stock`).
   - `product_url`: Đường dẫn chi tiết cuốn sách (URL tuyệt đối).
   - `thumbnail_url`: Đường dẫn ảnh bìa sách.
   - `page_number`: Số thứ tự trang danh mục (1 – 50).
   - `retrieved_at`: Dấu thời gian thu thập dữ liệu (ISO 8601 UTC).

---

## 2. Kết Quả Định Dạng Xuất File (Theo Đúng Yêu Cầu Đề Bài)

Toàn bộ dữ liệu được lưu tại thư mục `data/` với đầy đủ các định dạng:

| Tên file | Định dạng | Số lượng dòng | Mô tả |
| :--- | :---: | :---: | :--- |
| `data/books.tsv` / `products.tsv` | **TSV** | **1.000** | Phân tách bằng tab (`\t`), mã hóa UTF-8 |
| `data/books.csv` / `products.csv` | **CSV** | **1.000** | Phân tách bằng dấu phẩy, UTF-8 có BOM |
| `data/books.json` / `products.json` | **JSON** | **1.000** | JSON Array, thụt dòng đẹp |
| `data/books.db` | **SQLite** | **1.000** | Cơ sở dữ liệu quan hệ, bảng `books` |

---

## 3. Cấu Trúc Thư Mục `Bài 2`

```text
BaiTapTuan1/Bài 2/
├── data/
│   ├── books.tsv / products.tsv     # File TSV (đúng đề bài)
│   ├── books.csv / products.csv     # File CSV (đúng đề bài)
│   ├── books.json / products.json   # File JSON (đúng đề bài)
│   ├── books.db                     # Cơ sở dữ liệu SQLite
│   └── other_datasets/              # Dữ liệu mở rộng (Open Food Facts, Airbnb, Open Library)
├── src/
│   ├── crawler.py                   # HTTP Session, Pagination 50 trang
│   ├── parser.py                    # BeautifulSoup: DOM traversal, rating map, regex price
│   ├── exporter.py                  # Xuất dữ liệu đa định dạng (TSV, CSV, JSON, SQLite)
│   ├── collectors/                  # Module thu thập mở rộng
│   ├── cleaning/                    # Module làm sạch dữ liệu mở rộng
│   └── features/                    # Module trích xuất đặc trưng Machine Learning
├── data_dictionary.md               # Từ điển dữ liệu chi tiết
├── summary_report.md                # Báo cáo tổng kết phương pháp luận
├── main.py                          # File thực thi chính
└── README.md
```

---

## 4. Hướng Dẫn Chạy Chương Trình

Từ thư mục `BaiTapTuan1/Bài 2`, chạy lệnh:

```bash
# Thu thập toàn bộ 50 trang (1.000 cuốn sách) ra TSV, CSV, JSON, SQLite
python main.py

# Hoặc thu thập thử nghiệm 5 trang (100 cuốn sách)
python main.py --pages 5
```

Mở notebook khảo sát và trực quan hóa dữ liệu tại: `BaiTapTuan1/notebooks/01_thuc_nghiem_books.ipynb`.
