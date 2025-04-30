# Face_Recognition
# HỆ THỐNG CHẤM CÔNG TỰ ĐỘNG BẰNG NHẬN DIỆN KHUÔN MẶT

## Giới thiệu
Hệ thống chấm công tự động sử dụng công nghệ nhận diện khuôn mặt để ghi nhận thời gian làm việc của nhân viên một cách chính xác và hiệu quả. Ứng dụng được phát triển bằng Python, tích hợp các thư viện OpenCV, dlib, và face_recognition để xử lý hình ảnh và nhận diện khuôn mặt, đồng thời sử dụng MySQL để lưu trữ dữ liệu.

## Tính năng chính
- **Nhận diện khuôn mặt**: Xác định danh tính nhân viên thông qua camera.
- **Quản lý thời gian làm việc**: Tự động ghi nhận thời gian vào/ra và tính toán tổng giờ làm.
- **Quản lý nhân viên**: Thêm, sửa, xóa thông tin nhân viên và xem lịch sử chấm công.
- **Báo cáo và thống kê**: Xuất báo cáo dưới dạng file Excel.
- **Giao diện thân thiện**: Hỗ trợ cả người dùng (nhân viên) và quản trị viên.

## Công nghệ sử dụng
- **Ngôn ngữ lập trình**: Python
- **Thư viện**:
  - OpenCV: Xử lý hình ảnh và phát hiện khuôn mặt.
  - dlib và face_recognition: Trích xuất đặc trưng khuôn mặt và nhận diện.
  - Tkinter: Thiết kế giao diện đồ họa.
  - Pandas: Xử lý dữ liệu và xuất báo cáo Excel.
- **Cơ sở dữ liệu**: MySQL
- **Thiết bị**: Webcam hoặc camera kết nối qua giao thức webcam.

## Cài đặt
1. **Yêu cầu hệ thống**:
   - Python 3.6 trở lên.
   - MySQL Server.
   - Webcam hoặc camera.

2. **Cài đặt thư viện**:
   Hãy cài thêm các thư viện cần thiết khác nếu cần thiết. 
   ```bash
   pip install opencv-python dlib face-recognition mysql-connector-python pandas tk
4. **Cấu hình cơ sở dữ liệu**:
   - Tạo database 'employees' và 'attendence' trong MySQL.
   - Cấu hình đăng nhập và mật khẩu tùy chọn.
5. **Chạy ứng dụng**
   ```bash
   python3 app.py

## Hướng dẫn sử dụng
1. Đăng nhập:
  -  Nhân viên: Sử dụng mã nhân viên và mật khẩu.
  - Quản trị viên: Sử dụng tài khoản admin.
2. Chấm công:
  - Nhấn "Khởi động camera" để bắt đầu nhận diện khuôn mặt.
  - Hệ thống tự động ghi nhận thời gian vào/ra.
3. Quản lý nhân viên (Admin):
  - Thêm nhân viên mới: Chụp ảnh và nhập thông tin.
  - Xem/sửa/xóa thông tin nhân viên.
4. Xuất báo cáo Excel.  
  
Updating ... 
Link youtube demo: https://youtu.be/LxZXbJvoadU
