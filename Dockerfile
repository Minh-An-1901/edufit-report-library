# Dockerfile đóng gói ứng dụng Thư viện báo cáo KPIMATRIX (Edufit)
FROM python:3.10-slim

WORKDIR /app

# Cài đặt các thư viện cần thiết
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép mã nguồn vào container
COPY . .

# Thiết lập biến môi trường
ENV PYTHONUNBUFFERED=1
ENV PORT=5000

# Mở cổng 5000
EXPOSE 5000

# Khởi chạy ứng dụng
CMD ["python", "start.py"]
