#!/bin/bash

# Chạy lệnh Python để khởi tạo cơ sở dữ liệu (tạo bảng 'sums' nếu chưa có)
# Lệnh này sẽ gọi hàm init_db() trong app.py
python -c "from app import init_db; init_db()"

# Sau khi CSDL được khởi tạo, khởi động ứng dụng Flask bằng Gunicorn
gunicorn app:app