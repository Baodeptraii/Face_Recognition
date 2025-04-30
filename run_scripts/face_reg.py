import cv2
import numpy as np
import face_recognition
import os
import mysql.connector
from datetime import datetime
import pickle

# Kết nối MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="python"
)
cursor = db.cursor()

classNames = []
# Đọc dữ liệu mã hóa khuôn mặt từ file pickle
with open('encodings.pkl', 'rb') as f:
    encodeListKnown, classNames = pickle.load(f)

# Kiểm tra xem đã điểm danh hay chưa
def is_attended(name):
    cursor.execute("SELECT * FROM Attendance WHERE employee_id = %s", (name,))
    return cursor.fetchone() is not None


def attendence(name):
    now = datetime.now()
    dtString = now.strftime('%H:%M:%S')
    today_date = now.date()
    # Kiểm tra xem nhân viên đã điểm danh chưa
    cursor.execute("SELECT * FROM Attendance WHERE employee_id = %s AND date = %s", (name, today_date))
    attendance = cursor.fetchone()

    if not attendance:
        # Chưa điểm danh, tiến hành điểm danh
        status = 'D' if now.hour < 8 else 'M'

        # Chèn dữ liệu điểm danh
        cursor.execute("INSERT INTO Attendance (employee_id, check_in_time, date, state) VALUES (%s, %s, %s, %s)",
                       (name, dtString, today_date, status))
        db.commit()
        print(f"{name} da cham cong vao {dtString}, trang thai : {status}")

    else:
        # Nếu nhân viên đã điểm danh, in ra thông báo
        print(f"{name} da cham cong, vui long khong cham cong lai!")
        # Kiểm tra trạng thái hiện tại của nhân viên
        current_status = attendance[5]  # Trạng thái hiện tại từ cột 'state'

        # Kiểm tra nếu thời gian sau 16h và trạng thái là 'D', chuyển thành 'H' và cập nhật check_out_time
        if now.hour >= 17:
            if current_status == 'D':  # Nếu trạng thái là 'D', chuyển sang 'H'
                cursor.execute(
                    "UPDATE Attendance SET state = %s, check_out_time = %s WHERE employee_id = %s AND date = %s",
                    ('H', dtString, name, today_date))
                db.commit()
                print(f"{name} da duoc cap nhat trang thai sang H va check_out_time: {dtString}")
            elif current_status == 'M':  # Nếu trạng thái là 'M', chỉ cập nhật check_out_time
                cursor.execute("UPDATE Attendance SET check_out_time = %s WHERE employee_id = %s AND date = %s",
                               (dtString, name, today_date))
                db.commit()
                print(f"{name} da cham cong check-out vao {dtString}")


# Khởi động webcam
cap = cv2.VideoCapture(1)
cv2.waitKey(1)

# Nhận diện khuôn mặt
while True:
    ret, frame = cap.read()
    if not ret:
        print("Khong the doc frame tu camera!")
        break

    framS = cv2.resize(frame, (0, 0), None, fx=0.5, fy=0.5)
    framS = cv2.cvtColor(framS, cv2.COLOR_BGR2RGB)
    
    # Nhận diện khuôn mặt trong frame 
    # Sử dụng face_recognition để tìm vị trí và mã hóa khuôn mặt

    facecurFrame = face_recognition.face_locations(framS)
    encodecurFrame = face_recognition.face_encodings(framS, facecurFrame)

    for encodeFace, faceLoc in zip(encodecurFrame, facecurFrame):
        if encodeListKnown:
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

            matchIndex = np.argmin(faceDis)

            if faceDis[matchIndex] < 0.50:
                name = classNames[matchIndex].upper()
                attendence(name)
            else:
                name = 'Unknown'

            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 2, x2 * 2, y2 * 2, x1 * 2
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, name, (x1, y2 + 30), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow('Check', frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# Giải phóng tài nguyên
cap.release()
cursor.close()
db.close()
cv2.destroyAllWindows()