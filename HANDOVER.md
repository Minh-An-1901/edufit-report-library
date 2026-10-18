# TÀI LIỆU BÀN GIAO KỸ THUẬT (HANDOVER DOCUMENT)
**Dự án**: Thư viện báo cáo nội bộ KPIMATRIX (Edufit)  
**Người bàn giao**: Ứng viên Lập trình Web  
**Đối tượng nhận bàn giao**: Kỹ sư phần mềm tiếp quản dự án  
**Trạng thái hệ thống**: Hoàn thành phiên bản MVP 1.0 (Đã chạy thực tế tại [bai-test-so-2-edufit.vercel.app](https://bai-test-so-2-edufit.vercel.app))

---

## 1. Tổng Quan Kiến Trúc & Luồng Dữ Liệu (Architecture & Data Flow)

Hệ thống được thiết kế theo mô hình **Hybrid SPA (Single Page Application trên nền tảng Flask)** nhằm đạt được hai tiêu chí: tốc độ tải trang cực nhanh và khả năng phục vụ trực tiếp các đường dẫn sâu (Deep Linking):

```
[Trình duyệt Client]
   │
   ├── (1) Yêu cầu trang chủ hoặc URL con (/thu-vien-bao-cao/R01) ──► [Flask start.py]
   │                                                                       │
   │                                                             (2) Đọc file cấu hình
   │                                                                       ▼
   ├── (3) Nhận HTML Shell (Home.html) + JSON ban đầu ◄────────── [data.json Service]
   │
   ├── (4) Tương tác trên giao diện:
   │        ├── Lọc nhóm phòng ban (TDS, SKR, ASC, TN) ──► JavaScript Client State
   │        ├── Tìm kiếm không dấu tiếng Việt (NFD)    ──► Cập nhật DOM tức thì
   │        ├── Chuyển đổi Lưới / Danh sách            ──► Lưu trữ vào localStorage
   │        └── Điều hướng URL (/thu-vien-bao-cao/...) ──► History API pushState
```

* **Lớp dữ liệu (`data.json`)**: Đóng vai trò là nguồn dữ liệu duy nhất (Single Source of Truth). Tách rời 100% khỏi giao diện người dùng.
* **Lớp ứng dụng (`start.py`)**: Đảm nhiệm định tuyến web, phục vụ REST API (`/api/data`, `/api/reports`) và cung cấp các hàm logic nghiệp vụ (Data Access Layer) dùng chung cho cả backend lẫn bộ kiểm thử tự động.
* **Lớp giao diện (`templates/Home.html`)**: Chứa toàn bộ CSS chuẩn tham chiếu và logic tương tác JavaScript được chia khối chức năng rõ ràng (State, Utils, Renderers, Event Handlers).

---

## 2. Các Quyết Định Kỹ Thuật Quan Trọng & Lý Do (Key Decisions & Rationale)

1. **Gộp CSS + HTML + JS trong một file template duy nhất (`Home.html`)**:
   * *Lý do*: Loại bỏ hoàn toàn sự phụ thuộc vào chuỗi công cụ build phức tạp (Node/Webpack/Vite), tránh các lỗi xung đột môi trường máy tính khi chuyển giao. Người tiếp quản chỉ cần mở duy nhất file này là nắm bắt được toàn bộ giao diện và luồng điều khiển.
2. **Xử lý tìm kiếm tiếng Việt bằng chuẩn hóa Unicode NFD**:
   * *Lý do*: Tiếng Việt có nhiều cách biểu diễn ký tự (dựng sẵn vs tổ hợp) và ký tự đặc biệt như `đ/Đ`. Thuật toán tách dấu thanh và chuyển `đ -> d` giúp người dùng tìm kiếm tự nhiên không cần gõ dấu (`giam sat` tìm ra `GIÁM SÁT`).
3. **Sinh ảnh khối màu Procedural bằng mã SVG**:
   * *Lý do*: Thay vì lưu trữ hàng loạt ảnh tĩnh dung lượng nặng, hệ thống dùng thuật toán sinh vector SVG nhẹ vài bytes dựa trên `color` và `seed`. Cách làm này đảm bảo tốc độ tải tức thì và độ sắc nét trên mọi độ phân giải màn hình.
4. **Mô phỏng bảng điều khiển BI (Mock BI Dashboard) thay vì gắn iframe trực tiếp**:
   * *Lý do*: Đường dẫn nhúng trong đề bài là địa chỉ giả định (`example.vn`). Nếu nhúng iframe thật sẽ gây lỗi trắng trang hoặc lỗi DNS khi người dùng xem chi tiết. Hệ thống dựng một khung giả lập trực quan với các chỉ số KPI động, đồng thời giữ nguyên cấu trúc URL để sau này thay thế bằng iframe thật một cách liền mạch.

---

## 3. Các Hạn Chế Đã Biết (Known Limitations)

* Đã hỗ trợ chức năng **+ Thêm báo cáo mới** trực tiếp trên giao diện UI (lưu dữ liệu bền vững qua `localStorage` trên Vercel và đồng bộ vào `data.json` qua `POST /api/reports` khi chạy local). Tuy nhiên ở giai đoạn dài hạn, cần kết nối vào hệ quản trị cơ sở dữ liệu quan hệ (PostgreSQL / MySQL) tập trung cho toàn tổ chức.
* Chưa có cơ chế phân quyền người dùng (Role-Based Access Control) thực tế theo tài khoản Google/Azure AD của nhà trường (hiện dùng Mock RBAC giả lập).
* Khung nhúng BI Dashboard hiện tại đang hiển thị giao diện mô phỏng nội bộ cao cấp, chưa nhúng PowerBI Tokenized Iframe trực tiếp từ máy chủ BI thật của Edufit.

---

## 4. Danh Sách 5 Việc Ưu Tiên Cần Làm Tiếp Theo (Top 5 Next Priorities)

Nếu bạn tiếp nhận dự án vào ngày mai, dưới đây là lộ trình 5 bước được khuyến nghị triển khai:

| Thứ tự | Hạng mục công việc | Lý do & Giá trị mang lại |
|:---:|:---|:---|
| **1** | **Chuyển `data.json` sang Cơ sở dữ liệu thật (PostgreSQL / SQLite)** | Đảm bảo tính toàn vẹn dữ liệu khi có nhiều người cùng chỉnh sửa báo cáo; phục vụ các thao tác CRUD từ trang quản trị CMS. |
| **2** | **Tích hợp Đăng nhập tập trung (Edufit SSO / OAuth2)** | Bắt buộc đối với ứng dụng nội bộ: đảm bảo nhân viên khối nào (TDS, SKR, ASC, TN) thì chỉ xem được báo cáo đúng thẩm quyền của khối đó. |
| **3** | **Tích hợp PowerBI Embedded SDK / Metabase Token** | Thay thế khung mô phỏng bằng iframe nhúng báo cáo PowerBI thật với token bảo mật có hạn giờ từ máy chủ backend. |
| **4** | **Phát triển chức năng "Báo cáo yêu thích" (Pin / Favorites)** | Giúp các cấp quản lý lưu lại các báo cáo họ thường xuyên theo dõi hàng ngày lên đầu trang để tiện truy cập nhanh. |
| **5** | **Xây dựng các phân hệ còn lại (`/phan-ra-kpi`, `/giao-kpi`, `/hoc-sinh`)** | Hoàn thiện các trang đang ở trạng thái giữ chỗ "Đang phát triển" để biến ứng dụng thành cổng điều hành KPI toàn diện. |

---

## 5. Hướng Dẫn Nhanh Cho Buổi Đánh Giá

* **Chạy server máy cục bộ**: `python start.py` (cổng 5000).
* **Chạy bộ kiểm thử tự động**: `python test_search.py`.
* **Cập nhật lên link online**: `npx vercel --prod`.
* **Mở rộng báo cáo/nhóm**: Thêm dữ liệu vào `data.json` (chi tiết xem tại `README.md`).
