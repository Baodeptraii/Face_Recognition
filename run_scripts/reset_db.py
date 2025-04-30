import mysql.connector
import pandas as pd
from datetime import datetime

# Thông tin kết nối MySQL
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "123456",
    "database": "python"
}

def reset_attendance_table():
    # Xóa dữ liệu trong bảng Attendance
    try:
        # Kết nối MySQL
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()

        # Xóa dữ liệu trong bảng Attendance
        cursor.execute("DELETE FROM attendance")
        db.commit()

        # Đóng kết nối
        cursor.close()
        db.close()

        print("Da xoa du lieu trong bang attendance!")
    except mysql.connector.Error as err:
        print(f"Khong ket noi duoc voi MySQL: {err}")
        
if __name__ == "__main__":
    reset_attendance_table()
        