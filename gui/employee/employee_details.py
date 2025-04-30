import tkinter as tk
from tkinter import ttk
import mysql.connector
from tkinter import messagebox
from datetime import datetime
import sys
from BTL.run_scripts.export_excel import export_attendance_to_excel

# Xem chi tiết lịch chấm công, id được truyền từ employee_info.py ( từ trang đăng nhập)
def xem_lich_cham_cong(employee_id):
    root = tk.Tk()
    root.title("Lịch chấm công nhân viên")
    root.geometry("850x550")
    root.configure(bg="#f0f4f7")

    # Cấu hình style tổng thể
    style = ttk.Style()
    style.theme_use("clam")

    style.configure("Treeview",
                    font=("Segoe UI", 11),
                    rowheight=30,
                    
                    borderwidth=0)

    style.configure("Treeview.Heading",
                    font=("Segoe UI", 12, "bold"),
                  )

    # Loại bỏ hiệu ứng hover ở header

    style.configure("TButton", font=("Segoe UI", 11), padding=(10, 4))

    # Tiêu đề
    title = tk.Label(root, text=f"Lịch chấm công: {employee_id}", font=("Segoe UI", 16, "bold"),
                     )
    title.pack(pady=(20, 10))

    # Khung chứa Treeview
    tree_frame = ttk.Frame(root)
    tree_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

    tree = ttk.Treeview(tree_frame, columns=("Date", "Check-in", "Check-out", "Status"), show="headings")
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Scrollbar dọc
    scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Cấu hình tiêu đề cột
    tree.heading("Date", text="📅 Ngày")
    tree.heading("Check-in", text="🕒 Giờ vào")
    tree.heading("Check-out", text="🕞 Giờ ra")
    tree.heading("Status", text="📌 Trạng thái")

    tree.column("Date", width=150, anchor="center")
    tree.column("Check-in", width=180, anchor="center")
    tree.column("Check-out", width=180, anchor="center")
    tree.column("Status", width=150, anchor="center")

    # Kết nối CSDL
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="python"
        )
        cursor = db.cursor()

        # Lấy dữ liệu lịch chấm công từ CSDL
        cursor.execute("SELECT * FROM attendance WHERE employee_id = %s", (employee_id,))
        attendance_data = cursor.fetchall()
        
        status_counts = {"D": 0, "H": 0, "M": 0}

        if attendance_data:
            for record in attendance_data:
                date, check_in, check_out, status = record[2], record[3], record[4], record[5]
                tree.insert("", tk.END, values=(date, check_in, check_out, status))
                if status in status_counts:
                    status_counts[status] += 1
        else:
            messagebox.showinfo("Thông báo", f"Không có dữ liệu chấm công cho nhân viên {employee_id}.")

        # Hiển thị thống kê trạng thái sau khi có dữ liệu
        status_text = f"Đi đúng giờ (D): {status_counts['D']}    Hoàn thành công việc (H): {status_counts['H']}    Đi muộn (M): {status_counts['M']}"
        status_label = tk.Label(root, text=status_text, font=("Segoe UI", 11), bg="#f0f4f7", fg="#1e293b")
        status_label.pack()

    except mysql.connector.Error as err:
        messagebox.showerror("Lỗi CSDL", f"Không thể kết nối: {err}")
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'db' in locals(): db.close()

    # Nút quay lại
    back_button = ttk.Button(root, text="⬅️ Quay lại", command=root.destroy)
    back_button.pack(pady=10)
    
    export_button = ttk.Button(root, text="📥 Xuất Excel", command=lambda: export_attendance_to_excel(employee_id))
    export_button.pack(pady=10)

    root.mainloop()

# Gọi từ dòng lệnh nếu có
if __name__ == "__main__":
    if len(sys.argv) > 1:
        employee_id = sys.argv[1]
        xem_lich_cham_cong(employee_id)
    else:
        messagebox.showerror("Lỗi", "Không có ID nhân viên được cung cấp.")
