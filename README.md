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

### Tuần 3: Linear Regression & OLS (`BaiTapTuan3/`)
* **Lý thuyết (`preliminaries.ipynb`)**:
  * Định nghĩa bài toán hồi quy xấp xỉ hàm, hàm lỗi tổng bình phương (Sum-of-Square Error / MSE).
  * Ước lượng OLS (Ordinary Least Squares) $\hat{\beta} = (X^T X)^{-1} X^T y$.
  * Định lý Gauss-Markov: OLS là ước lượng tuyến tính không chệch tốt nhất (BLUE - Best Linear Unbiased Estimator).
  * Góc nhìn Maximum Likelihood (ML) với giả định nhiễu Gaussian và Maximum A Posteriori (MAP) với tiên nghiệm Gaussian dẫn đến chuẩn hóa $L_2$ (Ridge / Weight Decay).
* **Bài tập thực hành (`assignments.ipynb`)**:
  * **Assignment 1 (3đ)**: Xây dựng lớp `LinearRegressionNumPy` thuần NumPy giải Normal Equation qua nghiệm đóng $\hat{\beta} = (X^T X)^{-1} X^T y$. Huấn luyện và đánh giá trên bộ dữ liệu thực tế **Forest Fires** (517 mẫu), vẽ biểu đồ Scatter Plot $y_{test}$ vs $\hat{y}$.
  * **Assignment 2 (3đ)**: Chuẩn hóa dữ liệu Z-score ($Mean=0, Var=1$), phân tích tính bất biến hình học của nghiệm đóng OLS và sự cải thiện vượt bậc của chỉ số điều kiện ma trận $\kappa(X^T X)$ (từ $\approx 20,600$ xuống $\approx 22$).
  * **Assignment 3 (2đ)**: Khử đa cộng tuyến (Collinearity) qua phân tích ma trận tương quan Pearson và bẫy biến giả (Dummy Variable Trap). Loại bỏ đặc trưng tương quan cao (`DC` & `DMC`) giúp ma trận $X^T X$ ổn định và hạn chế nguy cơ thổi phồng phương sai (Variance Inflation).
  * **Assignment 4 (2đ)**: Cài đặt và đối chiếu với `sklearn.linear_model.LinearRegression`. Độ lệch giữa nghiệm tự viết bằng NumPy và Scikit-Learn đạt mức $< 10^{-8}$, chứng minh tính chính xác tuyệt đối.

### Tuần 4: Support Vector Machine (SVM) & Thuật toán SMO (`BaiTapTuan4/`)
* **Lý thuyết (`lagrange-KTT-multiplier.ipynb`, `preliminaries.ipynb`, `SMO.ipynb`)**:
  * Cơ sở toán học nhân tử Lagrange và điều kiện KKT (Karush-Kuhn-Tucker) trong bài toán tối ưu có ràng buộc đẳng thức và bất đẳng thức.
  * Biểu diễn đối ngẫu (Dual representation), Định lý Mercer và Kernel trick (Linear Kernel, Gaussian RBF Kernel).
  * Mô hình Hard-margin & Soft-margin SVM, bản chất hình học của khoảng cách lề (Margin) và các Support Vectors.
* **Bài tập thực hành (`assignments.ipynb`)**:
  * **Phần 1: Kernel Functions**: Cài đặt `linear_kernel` và `rbf_kernel` từ số 0 bằng NumPy.
  * **Phần 2: Thuật toán SMO**: Tự cài đặt thuật toán **Sequential Minimal Optimization (SMO)** cập nhật giải tích từng cặp $(\alpha_i, \alpha_j)$, cắt ngọn theo cận $[L, H]$, và cập nhật hệ số chặn $b$ theo điều kiện KKT.
  * **Phần 3 & 4: Thực nghiệm & Trực quan hóa**:
    * Huấn luyện trên tập dữ liệu phi tuyến `make_moons` (đạt 98.00% Test Accuracy).
    * Huấn luyện trên tập dữ liệu tuyến tính `make_blobs` (đạt 100.00% Test Accuracy).
    * Vẽ đồ thị Decision Boundary và khoanh tròn các Support Vectors nằm trên đường biên.
  * **Phần 5: Thực nghiệm trên bộ dữ liệu thực tế nhiều chiều (Breast Cancer Wisconsin - 30 đặc trưng)**:
    * Thử nghiệm trên 569 bệnh nhân chẩn đoán ung thư vú nhị phân (Ác tính / Lành tính).
    * Chuẩn hóa `StandardScaler` và huấn luyện `SVM_SMO` (RBF Kernel), trực quan hóa Decision Boundary qua phép chiếu giảm chiều PCA (2D).
    * Đạt độ chính xác **97.90%** và F1-Score **0.9832**.
  * **Phần 6 & 7: Đối chiếu & Đánh giá**:
    * So sánh toàn diện với `sklearn.svm.SVC`: Test Accuracy (97.90%), F1-Score (0.9832), Confusion Matrix và số lượng Support Vectors (đúng 93 SVs) khớp chính xác 100%.


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

4. **Chạy Bài Tập Tuần 3**:
   * Mở và thực thi: `BaiTapTuan3/assignments.ipynb` (Nhiệm vụ Linear Regression & OLS - 10 điểm)

5. **Chạy Bài Tập Tuần 4**:
   * Mở và thực thi: `BaiTapTuan4/assignments.ipynb` (Nhiệm vụ SVM & Thuật toán SMO - 10 điểm)


