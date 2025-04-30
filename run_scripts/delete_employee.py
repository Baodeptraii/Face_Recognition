import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# Xóa nhân viên
class DeleteEmployee:
    def __init__(self, root):
        self.root = root
        self.root.title("Xóa nhân viên cũ")
        self.root.geometry("600x500")
        
        self.setup_ui()
        self.load_data()
        
    def setup_ui(self):
        # Tạo frame chính
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Tạo frame chứa Treeview
        self.tree_frame = ttk.Frame(main_frame)
        self.tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Tạo Treeview với thanh cuộn
        self.tree = ttk.Treeview(self.tree_frame, columns=("Employee ID", "Name"), show="headings")
        
        # Tạo thanh cuộn
        y_scroll = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=y_scroll.set)
        
        # Bố trí Treeview và thanh cuộn
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Cấu hình các cột
        self.tree.heading("Employee ID", text="Mã nhân viên")
        self.tree.heading("Name", text="Tên")
        
        self.tree.column("Employee ID", width=150, anchor="center")
        self.tree.column("Name", width=250, anchor="w")
        
        # Thêm tag để định dạng các dòng
        self.tree.tag_configure('evenrow', background='#f0f0f0')
        self.tree.tag_configure('oddrow', background='white')
        
        # Tạo frame cho các nút hành động
        self.button_frame = ttk.Frame(main_frame)
        self.button_frame.pack(fill=tk.X, pady=10)
        
        # Thêm nút xóa nhân viên được chọn
        self.delete_button = ttk.Button(
            self.button_frame, 
            text="Xóa nhân viên", 
            command=self.delete_employee,
            style='Danger.TButton'
        )
        self.delete_button.pack(side=tk.LEFT, padx=5)
        
        # Thêm nút quay lại 
        self.back_button = ttk.Button(
            self.button_frame, 
            text="Quay lại", 
            command=self.root.destroy,
            style='Secondary.TButton'
        )
        self.back_button.pack(side=tk.RIGHT, padx=5)
        
        # Thêm sự kiện khi người dùng nhấp đúp chuột vào một dòng
        self.tree.bind("<Double-1>", lambda event: self.delete_employee())
        
        # Tạo style cho nút nguy hiểm (xóa)
        style = ttk.Style()
        style.configure('Danger.TButton', background='#dc3545')
        style.configure('Secondary.TButton', background='#6c757d')
    
    def load_data(self):
        try:
            # Kết nối database
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="123456",
                database="python"
            )
            cursor = db.cursor()
            
            # Lấy dữ liệu nhân viên
            cursor.execute("SELECT * FROM employees")
            employee_data = cursor.fetchall()
            
            # Xóa dữ liệu cũ trong Treeview
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Thêm dữ liệu vào Treeview
            for i, record in enumerate(employee_data):
                employee_id = record[1]
                name = record[2]
                
                # Thêm dòng vào Treeview
                tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                self.tree.insert("", tk.END, values=(employee_id, name), tags=(tag,))

        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi", f"Không thể kết nối database: {err}")
        finally:
            if 'db' in locals() and db.is_connected():
                cursor.close()
                db.close()
    
    def delete_employee(self):
        # Lấy item được chọn
        selected_item = self.tree.selection()
        
        if not selected_item:
            messagebox.showinfo("Thông báo", "Vui lòng chọn một nhân viên")
            return
        
        # Lấy thông tin nhân viên
        employee_id, name = self.tree.item(selected_item[0], 'values')
        
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
    app = DeleteEmployee(root)
    root.mainloop()

if __name__ == "__main__":
    main()