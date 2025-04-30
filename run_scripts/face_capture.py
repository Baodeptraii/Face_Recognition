import cv2
import os
import time
import mysql.connector
import subprocess

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="python"
)

cursor = db.cursor()

# Tạo thư mục lưu ảnh nếu chưa tồn tại
dataset_path = "dataset"
if not os.path.exists(dataset_path):
    os.makedirs(dataset_path)
    
id = input("Nhap ma nhan vien: ").strip()
name = input("Nhap ten nhan vien: ").strip()

person_path = os.path.join(dataset_path, id)

# Hàm thêm nhân viên vào database nếu chưa có
def add_employee(name, id, image_path):
    cursor.execute("SELECT * FROM Employees WHERE name = %s", (name,))
    if not cursor.fetchone():
        cursor.execute("INSERT INTO Employees (name, employee_id, image_path, password) VALUES (%s,%s, %s, %s)", (name,id, image_path, id))
        db.commit()
        print(f" Da them nhan vien: {name}")

if not os.path.exists(person_path):
    os.makedirs(person_path)

# Khởi động webcam
cap = cv2.VideoCapture(1)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

count = 0
total_images = 20  # Số lượng ảnh cần chụp

cv2.namedWindow("Face Capture", cv2.WINDOW_AUTOSIZE)  # Đảm bảo cửa sổ tự động điều chỉnh
cv2.setWindowProperty("Face Capture", cv2.WND_PROP_TOPMOST, 1)  # Đặt cửa sổ lên trên cùng
cv2.waitKey(1)  # Tạo độ trễ nhỏ để đảm bảo cửa sổ được cập nhật


print(f"📸 Dang thu thap {total_images} anh cho {name}...")

while count < total_images:
    ret, frame = cap.read()
    if not ret:
        print("Khong the doc fame tu camera!")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(100, 100))

    for (x, y, w, h) in faces:
        face_img = frame[y:y+h, x:x+w]
        
        # Resize ảnh khuôn mặt để đảm bảo kích thước đồng nhất
        face_resized = cv2.resize(face_img, (200, 200))

        file_path = os.path.join(person_path, f"{name}_{count+1}.jpg")
        # file_path = dataset_path + "'\'" + id
        cv2.imwrite(file_path, face_resized)
        count += 1

        print(f"Da chup {count}/{total_images}")

        # Vẽ hình chữ nhật quanh khuôn mặt và hiển thị số ảnh đã chụp
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, f"{count}/{total_images}", (x, y-10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        time.sleep(0.5)  # Đợi 0.5 giây trước khi chụp ảnh tiếp theo
    
    cv2.putText(frame, "Dang chup anh ... Vui long nhin thang vao camera", (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
    cv2.imshow("Face Capture", frame)
    
    if cv2.waitKey(1) & 0xFF == ord("q"):  # Bấm "q" để thoát sớm
        break

person = name
img_path = "dataset" + "\\"+ id
add_employee(person, id, img_path)

cap.release()
cv2.destroyAllWindows()

# Lưu mã hóa khuôn mặt vào file pickle
subprocess.call(["python", "run_scripts/face_encode.py"])
print("All done!")