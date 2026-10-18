# NHẬT KÝ SỬ DỤNG TRỢ LÝ AI (AI USAGE LOG)
**Dự án**: Thư viện báo cáo nội bộ KPIMATRIX (Edufit)  
**Quy định tuân thủ**: Bắt buộc khai báo minh bạch theo tài liệu quy định bài thực hành tuyển dụng.

---

## 1. Công Cụ Đã Dùng Và Phạm Vi Sử Dụng

| Công cụ AI | Phiên bản / Môi trường | Phạm vi hỗ trợ cụ thể |
|:---|:---|:---|
| **Antigravity (Gemini)** | Gemini Flash / Claude Sonnet | Đọc hiểu đề bài từ file Excel; gợi ý khung sườn máy chủ Flask; hỗ trợ viết các đoạn mã SVG khối màu; hỗ trợ viết kịch bản unit test tự động. |
| **GitHub Copilot / ChatGPT** | Web / IDE | Gợi ý hoàn thành cú pháp CSS Flexbox/Grid và các hàm thao tác DOM cơ bản. |

---

## 2. Các Lời Nhắc Chính (Prompts)

Dưới đây là tóm tắt các câu lệnh/lời nhắc chính được sử dụng trong quá trình phát triển:

1. *"Đọc file đề bài `De_bai_Xay_dung_trang_Thu_vien_bao_cao.xlsx`, phân tích cấu trúc các sheet và tổng hợp các tiêu chí chấp nhận cho từng mã yêu cầu (FR-01 đến FR-10, EX-01 đến EX-05, DOC-01 đến DOC-04)."*
2. *"Thiết kế một kiến trúc tối giản bằng Flask kết hợp với Single Template HTML (gộp CSS + HTML + JS vào `Home.html`), dữ liệu cấu hình tách riêng ở `data.json` để có thể thêm nhóm mới dưới 1 phút khi live-coding."*
3. *"Viết hàm JavaScript và Python chuẩn hóa chuỗi tiếng Việt: bỏ dấu thanh Unicode NFD, xử lý ký tự đặc biệt đ/Đ và không phân biệt hoa thường để tìm kiếm tức thì."*
4. *"Tạo hàm sinh đồ họa khối màu Procedural bằng mã SVG dựa trên mã màu hex và số seed tương ứng với ảnh tham chiếu của hệ thống."*
5. *"Viết bộ kiểm thử tự động với Python unittest kiểm tra các trường hợp: tìm 'giam sat' ra 3 kết quả, tìm 'doanh thu' ra 2 kết quả, kết hợp lọc SKR và tìm kiếm ra 1 kết quả."*

---

## 3. Các Trường Hợp AI Viết Sai/Thiếu Được Phát Hiện Và Sửa Đổi

Đúng theo tiêu chí đánh giá *"Làm chủ sản phẩm và kiểm soát chất lượng mã nguồn"*, dưới đây là 3 trường hợp AI đưa ra giải pháp chưa hoàn thiện và cách xử lý thực tế:

### Trường hợp 1: Hàm tìm kiếm tiếng Việt ban đầu của AI không xử lý được chữ "đ/Đ"
* **Lỗi phát sinh**: Đoạn mã xử lý regex ban đầu do AI gợi ý chỉ dùng `.normalize('NFD').replace(/[\u0300-\u036f]/g, '')`. Thuật toán này chỉ bóc tách các dấu thanh thông thường (sắc, huyền, hỏi, ngã, nặng), nhưng đối với chữ `đ` và `Đ` trong tiếng Việt thì đây là ký tự riêng biệt (D with stroke) nên không bị tách dấu, dẫn đến gõ `tien do` không thể tìm ra `TIẾN ĐỘ`.
* **Cách phát hiện**: Khi đối chiếu với tiêu chí chấp nhận **FR-06** (*"gõ giam sat vẫn ra GIÁM SÁT; chữ đ cũng phải xử lý"*), tôi phát hiện việc tìm kiếm các báo cáo có chữ "tiến độ" bị bỏ sót.
* **Cách sửa**: Bổ sung hàm chuyển đổi thủ công riêng cho ký tự `đ/Đ` thành `d/D` trong cả mã JavaScript lẫn Python:
  ```javascript
  text.normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .replace(/[đĐ]/g, m => m === 'đ' ? 'd' : 'D')
  ```

### Trường hợp 2: AI đề xuất nhúng trực tiếp thẻ iframe với đường dẫn giả
* **Lỗi phát sinh**: AI ban đầu viết mã chèn thẳng thẻ `<iframe src="${report.embed_url}">` vào trang chi tiết.
* **Cách phát hiện**: Đọc kỹ phần ghi chú dòng 34 tab *Dữ liệu mẫu* trong đề bài: *"địa chỉ nhúng là địa chỉ giả (`bi.example.vn`), chỉ để hiển thị trong khung nhúng"*. Nếu để iframe tải link này, trình duyệt của người chấm sẽ báo lỗi không tìm thấy máy chủ (DNS Error / Blank Page), làm giảm điểm trải nghiệm người dùng.
* **Cách sửa**: Quyết định thiết kế một **Mock BI Dashboard** chuyên nghiệp hiển thị các thẻ KPI và biểu đồ tiến độ sinh động, phía trên thanh công cụ ghi rõ đường dẫn URL giả lập theo đúng yêu cầu đề bài.

### Trường hợp 3: Xung đột mã hóa ký tự (cp1252) trên môi trường Windows Terminal
* **Lỗi phát sinh**: Khi chạy file kiểm thử `test_search.py`, màn hình báo lỗi `UnicodeEncodeError: 'charmap' codec can't encode character` và ngừng chạy bài test.
* **Cách phát hiện**: Quan sát trực tiếp console PowerShell khi chạy lệnh `python test_search.py`.
* **Cách sửa**: Bổ sung cấu hình tự động cấu hình lại chuẩn đầu ra UTF-8 cho `sys.stdout` ngay đầu file `test_search.py` và `start.py`:
  ```python
  if sys.stdout.encoding != 'utf-8':
      sys.stdout.reconfigure(encoding='utf-8')
  ```

---

## 4. Phần Tự Quyết Định & Tự Xây Dựng

1. **Quyết định cấu trúc một template duy nhất (`Home.html`)**: Tránh xa việc cấu hình cồng kềnh với Node.js, Webpack hay React để đảm bảo sản phẩm chạy được ở bất kỳ máy tính nào bằng tối đa 2 lệnh (tiêu chí DOC-01) và dễ dàng giải thích trong 20 phút phỏng vấn.
2. **Tách riêng file `data.json`**: Chuẩn bị trước kịch bản người phỏng vấn yêu cầu thêm nhóm `HR` hoặc thêm báo cáo mới ngay trong buổi kiểm tra trực tiếp (tiêu chí EX-01).
3. **Thiết kế tính năng 🧪 Demo State Bar**: Chủ động thêm cụm chuyển đổi trạng thái (Mô phỏng trễ 1s, Mô phỏng lỗi API) ở góc phải thanh công cụ để người chấm có công cụ kiểm chứng ngay lập tức tiêu chí **FR-09**.
4. **Lựa chọn triển khai Vercel Serverless**: Thay vì chỉ chạy cục bộ, tôi chủ động đưa ứng dụng lên máy chủ đám mây Vercel để người chấm có thể kiểm tra trực tiếp trên mọi thiết bị (tiêu chí BN-01).
