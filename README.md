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

### Tuần 2: Logistic Regression & Softmax Regression (`BaiTapTuan2/`)
* **Lý thuyết (`preliminaries.ipynb`)**:
  * Suy diễn xác suất hậu nghiệm Bayes, hàm Sigmoid & Softmax từ mô hình Gaussian Likelihood.
  * Đạo hàm tường minh của hàm mất mát Cross-Entropy theo trọng số $W$.
* **Bài tập chính (`assignments.ipynb`)**:
  * **Assignment 1 (4đ)**: Xây dựng Logistic Regression bằng NumPy thuần, huấn luyện bằng Gradient Descent phân loại chữ số 0 và 1 trên MNIST, trực quan hóa đồ thị loss.
  * **Assignment 2 (4đ)**: Xây dựng Softmax Regression bằng NumPy thuần phân loại 10 chữ số (0–9) trên MNIST, trực quan hóa đồ thị loss.
  * **Assignment 3 (2đ)**: Triển khai và đối chiếu bằng thư viện Scikit-Learn.
* **Bài tập mở rộng Bonus (+1 điểm) (`bonus_crawled_data.ipynb`)**:
  * Áp dụng `LogisticRegression` và `SoftmaxRegression` tự cài đặt lên bộ dữ liệu **Open Food Facts** (1.004 sản phẩm dinh dưỡng) thu thập từ Tuần 1.
  * **Binary Classification**: Phân loại thực phẩm lành mạnh (`is_healthy`: Grade A/B vs Grade C/D/E) và phân tích ý nghĩa thống kê của các trọng số dinh dưỡng (đường, muối, chất béo bão hòa, đạm).
  * **Multi-class Classification**: Phân loại chuẩn quốc tế **Nutri-Score** (5 lớp: A, B, C, D, E).


---

## Hướng Dẫn Cài Đặt & Chạy

1. **Cài đặt môi trường & thư viện**:
   ```bash
   pip install requests beautifulsoup4 pandas numpy scikit-learn matplotlib
   ```

2. **Chạy Bài Tập Tuần 1**:
   ```bash
   python "BaiTapTuan1/Bài 1/newton-raphson.py"
   python "BaiTapTuan1/Bài 2/main.py"
   ```

3. **Chạy Bài Tập Tuần 2**:
   * Mở Jupyter Lab / VS Code Notebook và chạy trực tiếp các file trong `BaiTapTuan2/`:
     * `BaiTapTuan2/assignments.ipynb` (Nhiệm vụ MNIST - 10 điểm)
     * `BaiTapTuan2/bonus_crawled_data.ipynb` (Nhiệm vụ Bonus dữ liệu tự crawl - +1 điểm)

