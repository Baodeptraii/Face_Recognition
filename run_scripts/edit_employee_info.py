import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import mysql.connector

class EditEmployeeInfo:
    def __init__(self, employee_id, name, img_path, password):
        self.root = tk.Toplevel()
        self.root.title("Chỉnh sửa thông tin nhân viên")
        self.root.geometry("800x400")
        self.employee_data = (employee_id, name, img_path, password)
        
        self.setup_ui()
        self.load_employee_data()
        
    def setup_ui(self):
        # Frame chính
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Tiêu đề
        ttk.Label(
            main_frame, 
            text="CHỈNH SỬA THÔNG TIN NHÂN VIÊN", 
            font=("Helvetica", 14, "bold")
        ).grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Tạo Treeview để hiển thị thông tin
        self.tree = ttk.Treeview(
            main_frame, 
            columns=("Field", "Old Info", "New Info"), 
            show="headings",
            height=5
        )
        
        # Định nghĩa các cột
        self.tree.heading("Field", text="Trường thông tin")
        self.tree.heading("Old Info", text="Thông tin cũ")
        self.tree.heading("New Info", text="Thông tin mới")
        
        self.tree.column("Field", width=200, anchor="w")
        self.tree.column("Old Info", width=250, anchor="w")
        self.tree.column("New Info", width=250, anchor="w")
        
        self.tree.grid(row=1, column=0, columnspan=3, sticky="nsew", pady=(0, 20))
        
        # Thêm thanh cuộn
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=1, column=3, sticky="ns")
        
        # Thêm nút Chỉnh sửa
        ttk.Button(
            main_frame,
            text="Chỉnh sửa giá trị",
            command=self.edit_selected_value
        ).grid(row=2, column=0, pady=(0, 20))
        
        # Frame cho các nút
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=(10, 0))
        
        # Nút xác nhận
        ttk.Button(
            button_frame, 
            text="Xác nhận", 
            command=self.confirm_changes,
        ).pack(side=tk.LEFT, padx=10)
        
        # Nút hủy
        ttk.Button(
            button_frame, 
            text="Hủy", 
            command=self.root.destroy,
        ).pack(side=tk.RIGHT, padx=10)
        
        
        # Cấu hình grid để co giãn
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Thêm sự kiện double-click vào tree
        self.tree.bind("<Double-1>", lambda event: self.edit_selected_value())
        
    def edit_selected_value(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showinfo("Thông báo", "Vui lòng chọn một trường để chỉnh sửa")
            return
            
        # Lấy thông tin từ item được chọn
        item = selected_item[0]
        field, old_value, _ = self.tree.item(item, 'values')
        
        # Hiển thị dialog để nhập giá trị mới
        new_value = simpledialog.askstring(
            "Chỉnh sửa", 
            f"Nhập giá trị mới cho {field}:",
            initialvalue=old_value
        )
        
        # Cập nhật giá trị mới vào cột "New Info"
        if new_value is not None:  # User didn't cancel
            self.tree.item(item, values=(field, old_value, new_value))
        
    def load_employee_data(self):
        # Xóa dữ liệu cũ nếu có
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Thêm dữ liệu nhân viên vào Treeview
        fields = ["Mã nhân viên", "Tên nhân viên", "Đường dẫn ảnh", "Mật khẩu"]
        old_values = [
            self.employee_data[0],  # employee_id
            self.employee_data[1],  # name
            self.employee_data[2],  # img_path
            self.employee_data[3]   # password
        ]
        
        for field, old_value in zip(fields, old_values):
            self.tree.insert("", tk.END, values=(field, old_value, ""))
    
    def confirm_changes(self):
        # Lấy tất cả các thay đổi từ Treeview
        changes = {}
        for item in self.tree.get_children():
            field, _, new_value = self.tree.item(item, 'values')
            if new_value.strip():  # Chỉ xử lý các trường có thay đổi
                changes[field] = new_value
        
        if not changes:
            messagebox.showinfo("Thông báo", "Không có thay đổi nào được thực hiện")
            return
        
        # Xác nhận thay đổi
        confirm = messagebox.askyesno(
            "Xác nhận", 
            "Bạn có chắc chắn muốn cập nhật thông tin nhân viên này không?"
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
            
            # Tạo câu lệnh SQL cập nhật
            update_query = "UPDATE employees SET "
            update_params = []
            
            # Ánh xạ tên trường hiển thị sang tên cột trong database
            field_mapping = {
                "Mã nhân viên": "employee_id",
                "Tên nhân viên": "name",
                "Đường dẫn ảnh": "img_path",
                "Mật khẩu": "password"
            }
            
            # Xây dựng phần SET của câu lệnh UPDATE
            set_parts = []
            for field, new_value in changes.items():
                db_field = field_mapping.get(field)
                if db_field:
                    set_parts.append(f"{db_field} = %s")
                    update_params.append(new_value)
            
            update_query += ", ".join(set_parts)
            update_query += " WHERE employee_id = %s"
            update_params.append(self.employee_data[0])  # employee_id cũ
            
            # Thực hiện cập nhật
            cursor.execute(update_query, update_params)
            db.commit()
            
            if cursor.rowcount > 0:
                messagebox.showinfo("Thành công", "Cập nhật thông tin nhân viên thành công")
                self.root.destroy()
            else:
                messagebox.showwarning("Cảnh báo", "Không có thông tin nào được cập nhật")
            
        except mysql.connector.Error as err:
            db.rollback()
            messagebox.showerror("Lỗi", f"Không thể cập nhật thông tin: {err}")
        finally:
            if 'db' in locals() and db.is_connected():
                cursor.close()
                db.close()
                
def open_edit_employee_form(employee_id, name, path, passwd):
    EditEmployeeInfo(employee_id, name, path, passwd)


def main():
    root = tk.Tk()
    # Dữ liệu mẫu: (employee_id, name, img_path, password)
    # 4 tham số được truyền gồm : employee_id, name, path, passwd
    root.mainloop()

if __name__ == "__main__":
    main()