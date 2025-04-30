import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from BTL.gui.employee.employee_details import xem_lich_cham_cong

class EmployeeList:
    # Khởi tạo giao diện nhân viên
    def __init__(self, root):
        self.root = root
        self.root.title("📋 Danh sách nhân viên")
        self.root.geometry("700x600")
        self.all_employees = []
        self.setup_style()
        self.setup_ui()
        self.load_data()

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Treeview", 
                        font=("Segoe UI", 11),
                        rowheight=32,
                        borderwidth=0)
        style.configure("Treeview.Heading", 
                        font=("Segoe UI", 12, "bold"),
                       )

        style.configure("TButton", font=("Segoe UI", 11), padding=6)
        style.configure("TLabel", font=("Segoe UI", 13))
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding=20, style="TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Khung tìm kiếm căn giữa, gọn hơn
        search_frame = ttk.LabelFrame(main_frame, text="🔍 Tìm kiếm nhân viên", padding=(10, 5))
        search_frame.pack(fill=tk.X, pady=(0, 15), ipadx=5, ipady=5)

        self.search_var = tk.StringVar()

        ttk.Label(search_frame, text="Nhập ID nhân viên:").grid(row=0, column=0, padx=0, pady=5, sticky="e", )
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30, font=("Segoe UI", 11))
        self.search_entry.grid(row=0, column=1, padx=0, pady=5)

        ttk.Button(search_frame, text="Tìm", command=self.search_employee, width=8).grid(row=0, column=2, padx=5)
        ttk.Button(search_frame, text="Xóa", command=self.clear_search, width=8).grid(row=0, column=3, padx=5)

        # Giữ layout đẹp khi mở rộng
        search_frame.columnconfigure(1, weight=1)

        # Treeview
        self.tree_frame = ttk.Frame(main_frame)
        self.tree_frame.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(self.tree_frame, columns=("Employee ID", "Name"), show="headings")
        y_scroll = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=y_scroll.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.heading("Employee ID", text="🆔 Mã nhân viên")
        self.tree.heading("Name", text="👤 Tên")

        self.tree.column("Employee ID", width=180, anchor="center")
        self.tree.column("Name", width=300, anchor="center")

        self.tree.tag_configure('evenrow', background='#f1f5f9')
        self.tree.tag_configure('oddrow', background='#ffffff')

        # Nút hành động
        self.button_frame = ttk.Frame(main_frame)
        self.button_frame.pack(fill=tk.X, pady=(15, 0))

        ttk.Button(self.button_frame, text="📅 Xem lịch chấm công", command=self.view_schedule).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.button_frame, text="⬅️ Quay lại", command=self.root.destroy).pack(side=tk.RIGHT, padx=5)

        self.tree.bind("<Double-1>", lambda event: self.view_schedule())
        self.search_entry.bind("<Return>", lambda event: self.search_employee())

    # Kết nối database và lấy dữ liệu nhân viên
    def load_data(self):
        try:
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="123456",
                database="python"
            )
            cursor = db.cursor()
            cursor.execute("SELECT * FROM employees")
            employee_data = cursor.fetchall()

            self.all_employees = [(record[1], record[2]) for record in employee_data]
            self.display_employees(self.all_employees)

        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi", f"Không thể kết nối database: {err}")
        finally:
            if 'db' in locals() and db.is_connected():
                cursor.close()
                db.close()

    # Hiển thị danh sách nhân viên trong Treeview
    def display_employees(self, employees):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for i, (emp_id, name) in enumerate(employees):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tree.insert("", tk.END, values=(emp_id, name), tags=(tag,))

    # Tìm kiếm nhân viên theo ID
    def search_employee(self):
        search_id = self.search_var.get().strip()
        if not search_id:
            self.display_employees(self.all_employees)
            return

        filtered = [emp for emp in self.all_employees if search_id in str(emp[0])]
        self.display_employees(filtered)

        if not filtered:
            messagebox.showinfo("Không tìm thấy", f"Không có nhân viên nào với ID chứa '{search_id}'.")

    # Xóa ô tìm kiếm và hiển thị lại tất cả nhân viên
    def clear_search(self):
        self.search_var.set("")
        self.display_employees(self.all_employees)

    # Tạo nút xem lịch hoặc nháy đúp vào nhân viên để xem lịch chấm công
    def view_schedule(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Chưa chọn", "Vui lòng chọn một nhân viên.")
            return
        emp_id = self.tree.item(selected[0], 'values')[0]
        xem_lich_cham_cong(emp_id)

def main():
    root = tk.Tk()
    app = EmployeeList(root)
    root.mainloop()

if __name__ == "__main__":
    main()
