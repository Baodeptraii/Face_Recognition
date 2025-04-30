import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
import subprocess
import sys


# Cấu hình cơ sở dữ liệu
db_config = {
    "host": "localhost",
    "user": "root",  # Thay đổi nếu cần thiết
    "password": "123456",  # Thay đổi nếu cần thiết
    "database": "python"  # Tên cơ sở dữ liệu của bạn
}

def dang_nhap():
    username = entry_username.get().strip()
    password = entry_password.get().strip()

    if not username or not password:
        log_label.config(text="❗ Vui lòng điền đầy đủ thông tin", foreground="red")
        return

    try:
        # Kết nối tới cơ sở dữ liệu
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Truy vấn cơ sở dữ liệu để lấy mật khẩu của nhân viên với employee_id tương ứng
        cursor.execute("SELECT password FROM employees WHERE employee_id = %s", (username,))
        result = cursor.fetchone()

        if result and result[0] == password:  # Kiểm tra xem mật khẩu có khớp không
            employee_id = username  # Sử dụng username là employee_id
            log_label.config(text="✅ Đăng nhập thành công!", foreground="green")
            root.after(1000, lambda: open_employee_info(employee_id))
        else:
            log_label.config(text="❌ Sai tài khoản hoặc mật khẩu", foreground="red")

    except mysql.connector.Error as err:
        messagebox.showerror("Lỗi cơ sở dữ liệu", f"Không thể kết nối đến cơ sở dữ liệu: {err}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()


# Xem thông tin nhân viên
def open_employee_info(employee_id):
    root.destroy()
    subprocess.Popen(["python", "gui/employee/employee_info.py", str(employee_id)])
    sys.exit()

# Tạo nút hover
def on_enter(e):
    e.widget.config(background="#2c7edb")

def on_leave(e):
    e.widget.config(background="#3498db")

def create_hover_button(parent, text, command):
    btn = tk.Button(parent, text=text, font=("Arial", 12), width=20,
                    bg="#3498db", fg="white", activebackground="#2980b9",
                    relief="raised", bd=2, command=command)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    btn.pack(pady=10)
    return btn

# Tạo cửa sổ
root = tk.Tk()
root.title("Đăng nhập hệ thống chấm công")
root.geometry("360x280")
root.configure(bg="#f0f0f0")
root.resizable(False, False)

# Frame chính
main_frame = tk.Frame(root, bg="#f0f0f0", padx=20, pady=10)
main_frame.pack(expand=True)

# Tiêu đề
title_label = tk.Label(main_frame, text="🔒 Đăng nhập nhân viên", font=("Arial", 16, "bold"), bg="#f0f0f0")
title_label.pack(pady=(0, 10))

# Form đăng nhập
form_frame = tk.Frame(main_frame, bg="#f0f0f0")
form_frame.pack()

tk.Label(form_frame, text="Mã nhân viên:", bg="#f0f0f0", font=("Arial", 11)).grid(row=0, column=0, sticky="e", padx=5, pady=5)
entry_username = tk.Entry(form_frame, font=("Arial", 11))
entry_username.grid(row=0, column=1, padx=5, pady=5)

tk.Label(form_frame, text="Mật khẩu:", bg="#f0f0f0", font=("Arial", 11)).grid(row=1, column=0, sticky="e", padx=5, pady=5)
entry_password = tk.Entry(form_frame, show="*", font=("Arial", 11))
entry_password.grid(row=1, column=1, padx=5, pady=5)

# Nút đăng nhập
btn_login = create_hover_button(main_frame, "Đăng nhập", dang_nhap)

# Hiển thị trạng thái
log_label = tk.Label(main_frame, text="", bg="#f0f0f0", font=("Arial", 10))
log_label.pack()

# ESC = quit nhanh
root.bind("<Escape>", lambda e: root.destroy())

root.mainloop()
