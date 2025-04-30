import sys
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
from tkinter import font as tkfont
import mysql.connector
from PIL import Image, ImageTk


def main():
    # Lấy ID nhân viên từ trang đăng nhập
    if len(sys.argv) > 1:
        employee_id = sys.argv[1]
    else:
        messagebox.showerror("Lỗi", "Không có ID nhân viên được cung cấp.")
        return

    # Tạo cửa sổ chính
    root = tk.Tk()
    root.title("Hệ Thống Quản Lý Nhân Viên")
    root.geometry("450x350")
    root.configure(bg="#f8f9fa")
    root.resizable(False, False)

    # Style cho ứng dụng
    style = ttk.Style()
    style.configure("TFrame", background="#f8f9fa")
    style.configure("TLabel", background="#f8f9fa", font=("Arial", 10))
    style.configure("TButton", font=("Arial", 10), padding=5)
    style.map("TButton",
              background=[("active", "#0056b3")],
              foreground=[("active", "white")])

    # Font chữ
    title_font = tkfont.Font(family="Helvetica", size=16, weight="bold")
    label_font = tkfont.Font(family="Arial", size=10)
    button_font = tkfont.Font(family="Arial", size=10, weight="bold")

    # Frame chính
    main_frame = ttk.Frame(root, padding=30)
    main_frame.pack(expand=True, fill="both")

    # Header
    header_frame = ttk.Frame(main_frame)
    header_frame.pack(fill="x", pady=(0, 20))

    # Logo (có thể thay bằng logo thực tế)
    logo_label = tk.Label(header_frame, text="🔒", font=("Arial", 24), bg="#f8f9fa")
    logo_label.pack(side="left")

    title_label = tk.Label(header_frame, text=f"NHÂN VIÊN: {employee_id}",
                           font=title_font, bg="#f8f9fa", fg="#343a40")
    title_label.pack(side="left", padx=10)

    # Hàm tạo nút đẹp
    def create_modern_button(parent, text, command, color="#007bff"):
        btn = tk.Button(parent, text=text, font=button_font,
                        bg=color, fg="white", activebackground="#0056b3",
                        relief="flat", bd=0, padx=20, pady=8,
                        command=command)
        btn.bind("<Enter>", lambda e: btn.config(bg="#0056b3"))
        btn.bind("<Leave>", lambda e: btn.config(bg=color))
        return btn

    # Hàm đổi mật khẩu với giao diện đẹp
    def show_change_password():
        # Tạo cửa sổ đổi mật khẩu
        pw_window = tk.Toplevel(root)
        pw_window.title("Đổi Mật Khẩu")
        pw_window.geometry("450x500")
        pw_window.resizable(False, False)
        pw_window.configure(bg="#f8f9fa")
        pw_window.grab_set()

        # Frame chính
        pw_frame = ttk.Frame(pw_window, padding=30)
        pw_frame.pack(expand=True, fill="both")

        # Tiêu đề
        pw_title = tk.Label(pw_frame, text="ĐỔI MẬT KHẨU",
                            font=title_font, bg="#f8f9fa", fg="#343a40")
        pw_title.pack(pady=(0, 30))

        # Ô nhập liệu với style đẹp
        def create_input_field(frame, label_text, placeholder):
            field_frame = ttk.Frame(frame)
            field_frame.pack(fill="x", pady=10)

            tk.Label(field_frame, text=label_text, font=label_font,
                     bg="#f8f9fa").pack(side="top", anchor="w", pady=(0, 5))

            entry = ttk.Entry(field_frame, font=label_font, width=25)
            entry.pack(fill="x", ipady=8)
            entry.insert(0, placeholder)

            # Xử lý placeholder
            def on_focus_in(event):
                if entry.get() == placeholder:
                    entry.delete(0, "end")
                    entry.config(foreground="black")

            def on_focus_out(event):
                if not entry.get():
                    entry.insert(0, placeholder)
                    entry.config(foreground="gray")

            entry.bind("<FocusIn>", on_focus_in)
            entry.bind("<FocusOut>", on_focus_out)

            return entry

        # Tạo các ô nhập liệu
        old_pw_entry = create_input_field(pw_frame, "Mật khẩu hiện tại", "Nhập mật khẩu hiện tại")
        old_pw_entry.config(show="•")

        new_pw_entry = create_input_field(pw_frame, "Mật khẩu mới", "Nhập mật khẩu mới (tối thiểu 8 ký tự)")
        new_pw_entry.config(show="•")

        confirm_pw_entry = create_input_field(pw_frame, "Xác nhận mật khẩu", "Nhập lại mật khẩu mới")
        confirm_pw_entry.config(show="•")

        # Hiển thị/mật khẩu
        def toggle_password_visibility():
            if show_pw_var.get():
                old_pw_entry.config(show="")
                new_pw_entry.config(show="")
                confirm_pw_entry.config(show="")
            else:
                old_pw_entry.config(show="•")
                new_pw_entry.config(show="•")
                confirm_pw_entry.config(show="•")

        show_pw_var = tk.BooleanVar()
        show_pw_check = ttk.Checkbutton(pw_frame, text="Hiển thị mật khẩu",
                                        variable=show_pw_var, command=toggle_password_visibility)
        show_pw_check.pack(pady=10)

        # Frame nút bấm
        button_frame = ttk.Frame(pw_frame)
        button_frame.pack(pady=20)

        # Hàm xử lý đổi mật khẩu
        def process_password_change():
            old_pw = old_pw_entry.get()
            new_pw = new_pw_entry.get()
            confirm_pw = confirm_pw_entry.get()

            # Validate input
            if not old_pw or old_pw == "Nhập mật khẩu hiện tại":
                messagebox.showerror("Lỗi", "Vui lòng nhập mật khẩu hiện tại!")
                return

            if len(new_pw) < 8 or new_pw == "Nhập mật khẩu mới (tối thiểu 8 ký tự)":
                messagebox.showerror("Lỗi", "Mật khẩu mới phải có ít nhất 8 ký tự!")
                return

            if new_pw != confirm_pw:
                messagebox.showerror("Lỗi", "Mật khẩu mới và xác nhận không khớp!")
                return

            try:
                # Kết nối database
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="123456",
                    database="python"
                )
                cursor = conn.cursor()

                # Kiểm tra mật khẩu cũ
                cursor.execute("SELECT password FROM employees WHERE employee_id = %s", (employee_id,))
                result = cursor.fetchone()

                if result and result[0] == old_pw:
                    # Cập nhật mật khẩu mới
                    cursor.execute("UPDATE employees SET password = %s WHERE employee_id = %s",
                                   (new_pw, employee_id))
                    conn.commit()
                    messagebox.showinfo("Thành công", "Đổi mật khẩu thành công!")
                    pw_window.destroy()
                else:
                    messagebox.showerror("Lỗi", "Mật khẩu cũ không chính xác!")

            except mysql.connector.Error as err:
                messagebox.showerror("Lỗi", f"Lỗi kết nối database: {err}")
            finally:
                if 'cursor' in locals():
                    cursor.close()
                if 'conn' in locals() and conn.is_connected():
                    conn.close()

        # Nút xác nhận
        confirm_btn = create_modern_button(button_frame, "Xác nhận",
                                           process_password_change, "#28a745")
        confirm_btn.pack(side="left", padx=10, ipadx=20)

        # Nút hủy
        cancel_btn = create_modern_button(button_frame, "Hủy",
                                          pw_window.destroy, "#dc3545")
        cancel_btn.pack(side="right", padx=10, ipadx=20)

    # Các chức năng chính
    def open_timekeeping():
        subprocess.Popen(["python", "gui/employee/employee_details.py", str(employee_id)])

    # Tạo các nút chức năng
    timekeeping_btn = create_modern_button(main_frame, "📊 Xem chấm công", open_timekeeping)
    timekeeping_btn.pack(pady=10, fill="x")

    change_pw_btn = create_modern_button(main_frame, "🔑 Đổi mật khẩu", show_change_password)
    change_pw_btn.pack(pady=10, fill="x")

    logout_btn = create_modern_button(main_frame, "🚪 Đăng xuất", root.destroy, "red")
    logout_btn.pack(pady=10, fill="x")

    # Footer
    footer_label = tk.Label(root, text="Hệ thống quản lý nhân viên © 2023",
                            font=("Arial", 8), bg="#f8f9fa", fg="#6c757d")
    footer_label.pack(side="bottom", pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()