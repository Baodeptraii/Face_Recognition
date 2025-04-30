import mysql.connector
import pandas as pd
from datetime import datetime
import sys
from tkinter import messagebox

# Thông tin kết nối MySQL
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "123456",
    "database": "python"
}

def export_attendance_to_excel(employee_id):
    #Xuất dữ liệu Attendance từ MySQL ra file Excel.
    try:
        # Kết nối MySQL
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()

        # Lấy dữ liệu từ bảng Attendance
        cursor.execute("SELECT * FROM attendance where employee_id = %s", (employee_id,))
        rows = cursor.fetchall()

        if not rows:
            print("Khong co du lieu trong database!")
            return

        # Lấy tên cột từ bảng
        cursor.execute("SHOW COLUMNS FROM attendance")
        columns = [column[0] for column in cursor.fetchall()]

        # Đóng kết nối
        cursor.close()
        db.close()

        # Tạo DataFrame
        df = pd.DataFrame(rows, columns=columns)

        # Chuyển đổi dữ liệu ngày tháng và thời gian
        df['date'] = pd.to_datetime(df['date']).dt.date
        df['check_in_time'] = pd.to_timedelta(df['check_in_time'])
        df['check_out_time'] = pd.to_timedelta(df['check_out_time'])

        # Tính tổng thời gian làm việc
        df['working_duration'] = df['check_out_time'] - df['check_in_time']

        # Chuyển đổi sang định dạng HH:MM để dễ đọc
        df['working_duration'] = df['working_duration'].apply(lambda x: str(x).split('.')[0])  # Loại bỏ phần mili giây
        df['working_duration'] = df['working_duration'].apply(lambda x: str(x).split(' ')[-1])
        # Chuyển lại check_in_time và check_out_time sang dạng giờ
        df['check_in_time'] = df['check_in_time'].apply(lambda x: str(x).split(' ')[-1])
        df['check_out_time'] = df['check_out_time'].apply(lambda x: str(x).split(' ')[-1])
        # Xuất file Excel
        # file_name = f"Attendance_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
        file_name = f"Attendance_{employee_id}_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
        df.to_excel(file_name, index=False, engine="openpyxl")

        print(f"Da xuat ra file : {file_name}")

    except mysql.connector.Error as err:
        print(f"Khong ket noi duoc voi MySQL: {err}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        employee_id = sys.argv[1]
        export_attendance_to_excel(employee_id)
    else:
        messagebox.showerror("Lỗi", "Không có ID nhân viên được cung cấp.")