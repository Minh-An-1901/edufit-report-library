# KPIMATRIX - THƯ VIỆN BÁO CÁO NỘI BỘ (EDUFIT)

Ứng dụng web quản lý và hiển thị Thư viện báo cáo nội bộ cho hệ thống giáo dục Edufit (TDS, SKR, ASC, TN), xây dựng theo kiến trúc tối giản, hiệu năng cao với **Flask (Python) + HTML5/CSS3/JavaScript (Single Template Architecture)**.

* 🌐 **Bản Demo Trực Tuyến (24/7)**: [https://bai-test-so-2-edufit.vercel.app](https://bai-test-so-2-edufit.vercel.app)
* 🧪 **Kiểm thử tự động**: Đạt 6/6 bài test tiêu chuẩn (`Ran 6 tests - OK`).

---

## 1. Hướng Dẫn Cài Đặt Và Chạy (Tối Đa 2 Lệnh)

Yêu cầu máy tính đã cài **Python 3.8+**.

```powershell
# Lệnh 1: Cài đặt thư viện phụ thuộc
pip install -r requirements.txt

# Lệnh 2: Khởi động máy chủ web
python start.py
```

👉 Mở trình duyệt tại: **`http://localhost:5000`** hoặc **`http://127.0.0.1:5000`**.

---

## 2. Chạy Kiểm Thử Tự Động (DOC-04)

Hệ thống có sẵn bộ unit test tự động kiểm thử chức năng chuẩn hóa tiếng Việt, lọc theo nhóm, tìm kiếm không phân biệt hoa thường và dấu tiếng Việt (FR-03, FR-06):

```powershell
python test_search.py
```

---

## 3. Cấu Trúc Thư Mục Dự Án

```
BÀI TEST SỐ 2 EDUFIT/
│── start.py                 # File thực thi Flask, API endpoints, web routing
│── data.json                # EX-01: File cấu hình dữ liệu (Nhóm, Menu, Báo cáo)
│── test_search.py           # DOC-04: Bộ kiểm thử tự động unit test
│── requirements.txt         # Danh sách thư viện Python
│── vercel.json              # Cấu hình triển khai tự động lên Vercel
│── Procfile                 # Cấu hình triển khai Render / Railway
│── Dockerfile               # BN-01: Đóng gói container Docker
│── .gitignore               # Loại bỏ các file tạm, bảo mật tài liệu bài test
│── README.md                # DOC-01: Hướng dẫn cài đặt và mở rộng
│── HANDOVER.md              # DOC-02: Tài liệu bàn giao kỹ thuật 1-2 trang
│── AI_LOG.md                # Khai báo sử dụng AI minh bạch theo quy định
└── templates/
    └── Home.html            # Giao diện duy nhất tích hợp HTML + CSS + JS (SPA)
```

---

## 4. Hướng Dẫn Mở Rộng Hệ Thống (Dành Cho Vòng Phỏng Vấn Live-Coding)

Toàn bộ dữ liệu được quản lý tập trung tại [**`data.json`**](data.json) theo đúng tiêu chí **EX-01**, cho phép chỉnh sửa hoặc mở rộng mà không cần can thiệp vào mã nguồn giao diện.

### 4.1. Cách thêm một nhóm phòng ban mới (Ví dụ: Nhóm `HR` - Dưới 1 phút)
Mở file `data.json`, tìm mục `"groups"` và thêm đối tượng mới:
```json
{
  "id": "HR",
  "name": "HR",
  "color": "#8b5cf6"
}
```
*Giao diện sẽ tự động xuất hiện nút viên thuốc màu tím `HR` trên thanh công cụ và tạo phân nhóm tương ứng.*

### 4.2. Cách thêm một báo cáo mới
Mở file `data.json`, tìm mục `"reports"` và thêm vào danh sách:
```json
{
  "id": "R13",
  "title": "Báo cáo tuyển dụng nhân sự",
  "group": "HR",
  "color": "#8b5cf6",
  "seed": 15.0,
  "updated_at": "18/10/2026",
  "embed_url": "https://bi.example.vn/embed/R13"
}
```
*Thẻ báo cáo mới sẽ tự động sinh ảnh khối màu theo `seed`, tính vào huy hiệu đếm số lượng và hỗ trợ tìm kiếm ngay tức thì.*

### 4.3. Cách thêm một mục menu mới
Mở file `data.json`, tìm mục `"menus"` và bổ sung:
```json
{
  "order": 6,
  "title": "Báo cáo tài chính",
  "icon": "table",
  "path": "/tai-chinh"
}
```
*Menu bên trái sẽ tự cập nhật mục mới, bấm vào sẽ hiển thị trang giữ chỗ chuẩn bị triển khai mà không làm đứt gãy giao diện.*

---

## 5. Các Tính Năng Nổi Bật Đáp Ứng Yêu Cầu Đề Bài

1. **Khung ứng dụng chuẩn tham chiếu (FR-01, UI-01)**: Sidebar xanh navy tối (`#0b1329`), logo `KPIMATRIX`, menu chuyển đổi động không giật lag/reload toàn trang.
2. **Bộ lọc & Tìm kiếm thông minh (FR-03, FR-06)**:
   * Lọc theo nhãn nhóm phòng ban (bấm để chọn, bấm lại để bỏ chọn).
   * Chuẩn hóa Unicode NFD loại bỏ dấu tiếng Việt, xử lý chính xác ký tự `đ/Đ` (ví dụ: gõ `giam sat` ra `GIÁM SÁT`, gõ `tien do` ra `TIẾN ĐỘ`).
3. **Sinh ảnh khối màu tự động Procedural (FR-05)**: Sinh đồ họa khối hình học SVG vector sắc nét trực tiếp từ mã màu và `seed` ngẫu nhiên.
4. **Chuyển đổi Lưới / Danh sách (FR-07)**: Ghi nhớ trạng thái hiển thị vào `localStorage`.
5. **Xem chi tiết & Khung nhúng giả lập (FR-08)**: Đường dẫn riêng biệt `/thu-vien-bao-cao/<id>`, hiển thị bảng điều khiển BI mô phỏng trực quan; nút quay lại bảo toàn trạng thái lọc trước đó.
6. **Bảng điều khiển giả lập trạng thái 🧪 Demo State (FR-09)**: Tích hợp ngay trên thanh công cụ để người chấm kiểm tra trực quan trạng thái **Loading (Trễ 1s)** và **Lỗi API (Kèm nút Thử lại)**.
7. **Đồng bộ tham số URL (BN-01)**: Tự động gắn `?group=...&q=...` lên URL trình duyệt để lưu lại liên kết hoặc chia sẻ.
