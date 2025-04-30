import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from edit_employee_info import open_edit_employee_form



class EmployeeList:
    # Khởi tạo giao diện nhân viên
    def __init__(self, root):
        self.root = root
        self.root.title("📋 Danh sách nhân viên")
        self.root.geometry("900x700")
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
        # Thêm style cho nút xóa

    def setup_ui(self):
        
        
        main_frame = ttk.Frame(self.root, padding=20, style="TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True)

        #Tìm kiếm
        # Khung tìm kiếm căn giữa, gọn hơn
        search_frame = ttk.LabelFrame(main_frame, text="🔍 Tìm kiếm nhân viên", padding=(10, 5))
        search_frame.pack(fill=tk.X, pady=(0, 15), ipadx=5, ipady=5)

        self.search_var = tk.StringVar()

        ttk.Label(search_frame, text="Nhập ID nhân viên:").grid(row=0, column=0, padx=0, pady=5, sticky="e", )
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30, font=("Segoe UI", 11))
        self.search_entry.grid(row=0, column=1, padx=0, pady=5)

        ttk.Button(search_frame, text="Tìm", command=self.search_employee, width=8).grid(row=0, column=2, padx=5)
        ttk.Button(search_frame, text="Xóa", command=self.clear_search, width=8).grid(row=0, column=3, padx=5)


        # Treeview
        self.tree_frame = ttk.Frame(main_frame)
        self.tree_frame.pack(fill=tk.BOTH, expand=True)
        
        

        self.tree = ttk.Treeview(self.tree_frame, columns=("Employee ID", "Name", "Img_Path", "Password"), show="headings")
        y_scroll = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=y_scroll.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.heading("Employee ID", text="🆔 Mã nhân viên")
        self.tree.heading("Name", text="👤 Tên")
        self.tree.heading("Img_Path", text="👤 Đường dẫn file ảnh")
        self.tree.heading("Password", text="👤 Mật khẩu")

        self.tree.column("Employee ID", width=150, anchor="center")
        self.tree.column("Name", width=200, anchor="center")
        self.tree.column("Img_Path", width=300, anchor="center")
        self.tree.column("Password", width=150, anchor="center")

        self.tree.tag_configure('evenrow', background='#f1f5f9')
        self.tree.tag_configure('oddrow', background='#ffffff')
        
        self.button_frame = ttk.Frame(main_frame)
        self.button_frame.pack(fill=tk.X, pady=(15, 0))
        
        # Thêm nút xóa nhân viên
        ttk.Button(
            self.button_frame, 
            text="🗑️ Xóa nhân viên", 
            command=self.delete_employee,
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            self.button_frame, 
            text="✏️ Sửa thông tin", 
            command=self.edit_employee,
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            self.button_frame,
            text="Tải lại danh sách",
            command=self.loading,
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            self.button_frame, 
            text="⬅️ Quay lại", 
            command=self.root.destroy,
            style='Secondary.TButton'
        ).pack(side=tk.RIGHT, padx=5)
        
    def loading(self):
        # Xóa tất cả các bản ghi trong Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Tải lại dữ liệu từ database
        self.load_data()
        # Hiển thị thông báo
        messagebox.showinfo("Thông báo", "Đã tải lại danh sách nhân viên")
        

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

            self.all_employees = [(record[1], record[2], record[3], record[4]) for record in employee_data]
            self.display_employees(self.all_employees)

        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi", f"Không thể kết nối database: {err}")
        finally:
            if 'db' in locals() and db.is_connected():
                cursor.close()
                db.close()
                
    def edit_employee(self):
        # Lấy item được chọn
        selected_item = self.tree.selection()
        
        if not selected_item:
            messagebox.showinfo("Thông báo", "Vui lòng chọn một nhân viên")
            return
        
        # Lấy thông tin nhân viên
        employee_id, name, path, passwd = self.tree.item(selected_item[0], 'values')
        
        # Mở cửa sổ chỉnh sửa thông tin nhân viên
        open_edit_employee_form(employee_id, name, path, passwd)
        
               

    # Hiển thị danh sách nhân viên trong Treeview
    def display_employees(self, employees):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for i, (emp_id, name, path, passwd) in enumerate(employees):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tree.insert("", tk.END, values=(emp_id, name, path, passwd), tags=(tag,))
            
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
    
    # Hàm xóa nhân viên
    def delete_employee(self):
        # Lấy item được chọn
        selected_item = self.tree.selection()
        
        if not selected_item:
            messagebox.showinfo("Thông báo", "Vui lòng chọn một nhân viên")
            return
        
        # Lấy thông tin nhân viên
        employee_id, name, _, _ = self.tree.item(selected_item[0], 'values')
        
        # Xác nhận trước khi xóa
        confirm = messagebox.askyesno(
            "Xác nhận xóa", 
            f"Bạn có chắc chắn muốn xóa nhân viên {name} (Mã: {employee_id}) không?"
        )
        
        if not confirm:
            return
        
        try:
            # Kết nối database
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="123456",
                database="python"
            )
            cursor = db.cursor()
            
            # Thực hiện xóa nhân viên
            cursor.execute("DELETE FROM employees WHERE employee_id = %s", (employee_id,))
            db.commit()
            
            # Kiểm tra xem có bản ghi nào bị xóa không
            if cursor.rowcount > 0:
                messagebox.showinfo("Thành công", f"Đã xóa nhân viên {name} (Mã: {employee_id})")
                # Cập nhật lại danh sách
                self.load_data()
            else:
                messagebox.showwarning("Cảnh báo", f"Không tìm thấy nhân viên có mã {employee_id}")

        except mysql.connector.Error as err:
            db.rollback()
            messagebox.showerror("Lỗi", f"Không thể xóa nhân viên: {err}")
        finally:
            if 'db' in locals() and db.is_connected():
                cursor.close()
                db.close()


def main():
    root = tk.Tk()
    app = EmployeeList(root)
    root.mainloop()

if __name__ == "__main__":
    main()