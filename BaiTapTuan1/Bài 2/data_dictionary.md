# DATA DICTIONARY — ML DATA PROJECT (DS102)

Tài liệu mô tả chi tiết từ điển dữ liệu (Data Dictionary), quy cách chuẩn hóa, ý nghĩa đặc trưng và lưu ý phòng chống **Target Leakage** cho cả 4 bộ dữ liệu phục vụ môn **Học máy thống kê (DS102)**.

---

## 1. Nguồn 1: Books to Scrape (Web Scraping Cơ bản)

* **Mục đích**: Rèn luyện kỹ năng Web Scraping căn bản: HTTP GET, DOM traversal, CSS Selectors, Pagination tĩnh và tiền xử lý dữ liệu bảng.
* **Nguồn**: `https://books.toscrape.com`
* **Quy cách bảng**: Một dòng = Một cuốn sách (`books_1000_clean.csv`).
* **Bảng SQLite**: `books_1000.db` (Table: `books`).

| Tên trường | Kiểu dữ liệu | Ý nghĩa | Miền giá trị / Đơn vị | Ghi chú & Xử lý |
| :--- | :--- | :--- | :--- | :--- |
| `title` | Text | Tên đầy đủ cuốn sách | Chuỗi ký tự UTF-8 | Trích từ thuộc tính `title` thẻ `<a>` để tránh bị cắt `...` |
| `price_gbp` | Float | Giá bán | £10.00 – £59.99 | Loại bỏ ký tự `£`, chuyển thành số thực |
| `rating_star` | Integer | Đánh giá xếp hạng sao | 1, 2, 3, 4, 5 | Ánh xạ từ CSS class (`One`->1, ..., `Five`->5) |
| `is_in_stock` | Boolean | Trạng thái còn hàng | `True` / `False` | Kiểm tra chuỗi `"In stock"` |
| `product_url` | Text | Đường dẫn chi tiết sản phẩm | URL tuyệt đối | Khóa định danh duy nhất (Deduplication) |
| `thumbnail_url` | Text | Đường dẫn ảnh đại diện | URL tuyệt đối | Chuẩn hóa qua `urljoin` |
| `page_number` | Integer | Trang xuất hiện trên danh mục | 1 – 50 | 20 sách mỗi trang |
| `retrieved_at` | Text (ISO) | Thời điểm thu thập dữ liệu | ISO 8601 UTC | Đảm bảo tính kiểm toán dữ liệu (Auditability) |

### Các đặc trưng dẫn xuất (`books_features.csv`):
* `title_char_length`: Độ dài ký tự tiêu đề.
* `title_word_count`: Số từ trong tiêu đề.
* `price_tier`: Phân khoảng giá (`budget`, `standard`, `premium`).
* `is_high_rated`: Nhãn phân loại sao cao ($\ge 4$ sao).

---

## 2. Nguồn 2: Open Food Facts (Dữ liệu bảng đa thuộc tính & Nhãn dinh dưỡng)

* **Mục đích**: Bộ dữ liệu chính cho bài toán Học máy dạng bảng (Tabular ML): Phân loại đa lớp (Multi-class Classification), Hồi quy dinh dưỡng (Regression), Phân cụm (Clustering).
* **Nguồn**: Open Food Facts Search API v2 (`https://world.openfoodfacts.org`).
* **Quy cách bảng**: Một dòng = Một sản phẩm thực phẩm theo mã vạch barcode (`code`).
* **Bảng SQLite**: `openfoodfacts_1000.db` (Table: `food_products`).

| Tên trường | Kiểu dữ liệu | Ý nghĩa | Đơn vị / Miền giá trị | Ghi chú & Xử lý |
| :--- | :--- | :--- | :--- | :--- |
| `code` | Text | Mã vạch barcode sản phẩm | Chuỗi số (Primary Key) | Dùng để khử trùng lặp (Deduplicate) |
| `product_name` | Text | Tên sản phẩm | Chuỗi ký tự | Làm sạch khoảng trắng thừa |
| `brands` | Text | Thương hiệu sản xuất | Chuỗi ký tự | Đa dạng hóa từ 10 nhóm danh mục |
| `countries` | Text | Quốc gia phân phối | Chuỗi ký tự | Ví dụ: `France`, `Vietnam`, `United States` |
| `categories` | Text | Danh mục sản phẩm | Danh sách phân cấp | Phân loại sản phẩm |
| `energy_kcal_100g` | Float | Năng lượng trên 100g | kcal (0 – 900) | Giữ `NaN` nếu khuyết, không ép thành 0 |
| `fat_100g` | Float | Hàm lượng chất béo | g/100g (0 – 100) | Loại bỏ các giá trị âm hoặc outlier vô lý |
| `saturated_fat_100g` | Float | Chất béo bão hòa | g/100g (0 – 100) | Thành phần tính điểm Nutri-Score |
| `carbohydrates_100g` | Float | Tổng Carbohydrate | g/100g (0 – 100) | Giữ missing là `NaN` |
| `sugars_100g` | Float | Hàm lượng đường | g/100g (0 – 100) | Target cho hồi quy hoặc feature |
| `fiber_100g` | Float | Hàm lượng chất xơ | g/100g (0 – 100) | Thành phần tích cực trong dinh dưỡng |
| `proteins_100g` | Float | Hàm lượng chất đạm | g/100g (0 – 100) | Thành phần dinh dưỡng đa lượng |
| `salt_100g` | Float | Hàm lượng muối | g/100g (0 – 100) | Target hồi quy / Cảnh báo sức khỏe |
| `sodium_100g` | Float | Hàm lượng natri | g/100g | Quan hệ tỷ lệ với salt |
| `ingredients_text` | Text | Văn bản thành phần nguyên liệu | Chuỗi văn bản | Phục vụ NLP / TF-IDF / Embedding |
| `allergens` | Text | Các chất gây dị ứng | Chuỗi nhãn | Bài toán Multi-label classification |
| `additives_n` | Integer | Số lượng phụ gia thực phẩm | $\ge 0$ | Đánh giá mức độ siêu chế biến |
| `nutrition_grade` | Text | Điểm chất lượng Nutri-Score | `A`, `B`, `C`, `D`, `E` | Target phân loại chính (Multi-class) |
| `vegan` | Boolean/None | Sản phẩm thuần chay hay không | `True`/`False`/`None` | Phân tích từ `ingredients_analysis_tags` |
| `vegetarian` | Boolean/None | Sản phẩm ăn chay | `True`/`False`/`None` | Phân tích từ tags |
| `palm_oil_free` | Boolean/None | Không chứa dầu cọ | `True`/`False`/`None` | Phân tích môi trường/sức khỏe |
| `retrieved_at` | Text (ISO) | Thời điểm lấy dữ liệu | ISO 8601 UTC | Audit log |

> [!CAUTION]
> **CẢNH BÁO TARGET LEAKAGE**: Khi xây dựng mô hình dự đoán `nutrition_grade` (Nutri-Score), tuyệt đối **không** đưa công thức tính trực tiếp (như điểm số Nutri-Score có sẵn hoặc các điểm cộng/trừ nội bộ) vào vector đặc trưng. Nếu mô hình học lại chính thuật toán cộng điểm đã biết thì kết quả thực nghiệm sẽ bị rò rỉ nhãn (leakage).

---

## 3. Nguồn 3: Inside Airbnb (Dữ liệu Giá, Không gian và Thời gian)

* **Mục đích**: Bộ dữ liệu cho bài toán Hồi quy giá phòng (Price Regression), Phân tích không gian (Spatial Analytics), Phân cụm vị trí (Spatial Clustering).
* **Nguồn**: Trang [Inside Airbnb "Get the Data"](https://insideairbnb.com/get-the-data/) — Snapshot thành phố Amsterdam.
* **License**: Creative Commons Attribution 4.0 International.
* **Quy cách bảng**: Một dòng = Một listing phòng thuê (`airbnb_1000_clean.csv`).
* **Bảng SQLite**: `airbnb_1000.db` (Table: `listings`).

| Tên trường | Kiểu dữ liệu | Ý nghĩa | Đơn vị / Miền giá trị | Ghi chú & Xử lý |
| :--- | :--- | :--- | :--- | :--- |
| `id` | Integer | ID listing duy nhất | Số nguyên (Primary Key) | Dùng để deduplicate |
| `host_id` | Integer | ID chủ nhà | Số nguyên | Quan hệ host - listing |
| `host_response_rate` | Float | Tỷ lệ phản hồi tin nhắn | 0.0 – 1.0 (95% -> 0.95) | Làm sạch bỏ ký tự `%` |
| `host_acceptance_rate` | Float | Tỷ lệ chấp nhận đặt phòng | 0.0 – 1.0 | Làm sạch bỏ ký tự `%` |
| `host_is_superhost` | Integer | Có phải là Superhost không | `1` (True) / `0` (False) | Ánh xạ từ nhãn `'t'` / `'f'` |
| `neighbourhood_cleansed` | Text | Khu vực / Quận địa lý | Tên quận chính thức | Phân nhóm theo khu vực hành chính |
| `latitude` | Float | Vĩ độ địa lý | ~ 52.3x (Amsterdam) | Tọa độ đã được làm mờ nhẹ theo chính sách |
| `longitude` | Float | Kinh độ địa lý | ~ 4.9x (Amsterdam) | Dùng tính khoảng cách đến trung tâm |
| `room_type` | Text | Loại phòng | Entire home, Private room,... | Biến phân loại chính |
| `accommodates` | Integer | Số lượng khách tối đa | $\ge 1$ | Biến số lượng |
| `bedrooms` | Float | Số phòng ngủ | $\ge 0$ | Giữ `NaN` nếu thiếu |
| `beds` | Float | Số giường | $\ge 1$ | Biến số lượng |
| `amenities` | Text (JSON) | Danh sách tiện nghi đi kèm | JSON Array string | Parse ra `amenities_count`, `has_wifi`,... |
| `price` | Float | Giá thuê mỗi đêm | USD / EUR ($10 – $1500) | Làm sạch ký hiệu `$`, `,` |
| `log_price` | Float | Giá sau khi lấy $\ln(1 + \text{price})$ | Số thực | **Target chuẩn cho bài toán hồi quy** |
| `minimum_nights` | Integer | Số đêm thuê tối thiểu | $\ge 1$ | Quy định lưu trú |
| `availability_365` | Integer | Số ngày còn trống trong năm | 0 – 365 | Đánh giá công suất phòng |
| `number_of_reviews` | Integer | Tổng số lượt đánh giá | $\ge 0$ | Đánh giá độ phổ biến |
| `review_scores_rating` | Float | Điểm đánh giá trung bình | 0.0 – 5.0 | Điểm uy tín của phòng |
| `instant_bookable` | Integer | Có thể đặt phòng tức thì | `1` / `0` | Biến nhị phân chính sách đặt |
| `retrieved_at` | Text (ISO) | Thời điểm thu thập | ISO 8601 UTC | Checksum lưu tại `metadata.txt` |

> [!WARNING]
> **LƯU Ý KHÔNG GIAN & BIẾN TRỄ**: Tọa độ GPS của Inside Airbnb đã được thuật toán của họ làm mờ (khoảng 0–150m) nhằm bảo vệ quyền riêng tư của chủ nhà. Do đó, chỉ sử dụng tọa độ này cho mô hình hóa khu vực/phân cụm, không coi là vị trí đo đạc chính xác tuyệt đối. Không dùng `review_scores_*` để dự đoán chính nó (leakage).

---

## 4. Nguồn 4: Open Library (Dữ liệu Văn bản, Metadata & Hệ gợi ý)

* **Mục đích**: Bộ dữ liệu cho bài toán NLP, Khai phá văn bản (Text Mining), Phân loại đa nhãn (Multi-label Tag Prediction), Hệ gợi ý sách (Recommendation System) và Đồ thị liên kết (Graph ML).
* **Nguồn**: Open Library Search API (`https://openlibrary.org/search.json`).
* **Quy cách bảng**: Một dòng = Một tác phẩm cấp độ Work (`openlibrary_1000_clean.csv`).
* **Bảng quan hệ**:
  - `openlibrary_authors.csv` (Quan hệ Work $\leftrightarrow$ Author)
  - `openlibrary_subjects.csv` (Quan hệ Work $\leftrightarrow$ Subject Tag)
* **Bảng SQLite**: `openlibrary_1000.db` (Tables: `works`, `work_authors`, `work_subjects`).

| Tên trường | Kiểu dữ liệu | Ý nghĩa | Ghi chú & Bài toán ứng dụng |
| :--- | :--- | :--- | :--- |
| `work_key` | Text | Mã định danh tác phẩm (Work Key) | Primary Key (Ví dụ: `/works/OL12345W`) |
| `edition_key` | Text | Mã ấn bản tiêu biểu | Khóa tham chiếu phiên bản xuất bản |
| `title` | Text | Tên tác phẩm | Dữ liệu văn bản phục vụ NLP, TF-IDF, BERT |
| `author_names` | Text | Danh sách các tác giả | Nối chuỗi các tác giả đại diện |
| `author_count` | Integer | Số lượng tác giả | Biến đếm tác giả cộng tác |
| `first_publish_year` | Float/Int | Năm xuất bản đầu tiên | Dùng phân nhóm thập kỷ xuất bản |
| `edition_count` | Integer | Tổng số ấn bản phát hành | **Target hồi quy**: dự đoán mức độ thành công/tái bản |
| `language_count` | Integer | Số ngôn ngữ tác phẩm được dịch | Đánh giá độ phổ biến toàn cầu |
| `languages` | Text | Danh sách ngôn ngữ tiêu biểu | Chuỗi mã ngôn ngữ (`eng`, `fre`,...) |
| `subject_count` | Integer | Số lượng chủ đề gán thẻ | Độ đa dạng đề tài |
| `subjects` | Text | Chuỗi các thẻ chủ đề (Subject tags) | Phục vụ bài toán Multi-label classification & Content-based Recommendation |
| `has_fulltext` | Boolean | Có sách đọc toàn văn hay không | Biến nhị phân tiếp cận |
| `number_of_pages_median` | Float | Số trang trung vị | Biến kích thước sách |
| `retrieved_at` | Text (ISO) | Thời điểm thu thập dữ liệu | Auditability |

> [!TIP]
> **PHÒNG NGỪA TARGET LEAKAGE**: Khi xây dựng bài toán phân loại thập kỷ xuất bản (`publish_decade`), bắt buộc phải loại bỏ trường `first_publish_year`, `publish_year_min`, `publish_year_max` khỏi tập đặc trưng đầu vào. Khi dự đoán `edition_count`, không đưa các trường trực tiếp cộng dồn từ số lượng phiên bản (như danh sách toàn bộ `edition_key`).
