import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
from datetime import datetime

class AttendanceSystem:
    # Hàm khởi tạo
    def __init__(self, root):
        self.root = root
        self.root.title("Hệ thống chấm công tự động")
        self.root.geometry("800x500")
        self.root.minsize(800,500)
        self.root.configure(bg="#ffffff")

        self.setup_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    # Hàm thiết lập giao diện
    def setup_ui(self):
        self.style = ttk.Style()
        self.style.theme_use("clam") 
        self.style.configure("TFrame", background="#ffffff")
        self.style.configure("TButton", font=("Segoe UI", 12), padding=6)
        self.style.configure("Header.TLabel", font=("Segoe UI", 20, "bold"), background="#ffffff", foreground="#2c3e50")
        self.style.configure("Status.TLabel", font=("Segoe UI", 10), background="#ffffff", foreground="#7f8c8d")

        main_container = ttk.Frame(self.root, padding=20)
        main_container.pack(fill=tk.BOTH, expand=True)

        # Header
        header_frame = ttk.Frame(main_container)
        header_frame.pack(fill=tk.X, pady=(0, 20))

        logo = tk.Canvas(header_frame, width=60, height=60, bg="#2980b9", highlightthickness=0)
        logo.create_text(30, 30, text="G06", fill="white", font=("Segoe UI", 12, "bold"))
        logo.pack(side=tk.LEFT, padx=(0, 20))

        title_time_frame = ttk.Frame(header_frame)
        title_time_frame.pack(side=tk.LEFT, expand=True)

        ttk.Label(title_time_frame, text="📷 Hệ thống chấm công thông minh", style="Header.TLabel").pack(anchor=tk.W)
        self.time_label = ttk.Label(title_time_frame, text="", style="Status.TLabel")
        self.time_label.pack(anchor=tk.W)
        self.update_time()

        # Status
        self.status_frame = ttk.Frame(header_frame)
        self.status_frame.pack(side=tk.RIGHT, anchor=tk.NE)

        ttk.Label(self.status_frame, text="Trạng thái:", style="Status.TLabel").pack(side=tk.LEFT)
        self.status_indicator = tk.Canvas(self.status_frame, width=16, height=16, bg="#e74c3c", highlightthickness=0)
        self.status_indicator.pack(side=tk.LEFT, padx=5)
        self.status_text = ttk.Label(self.status_frame, text="Chưa hoạt động", style="Status.TLabel")
        self.status_text.pack(side=tk.LEFT)

        # Nội dung chính
        content_frame = ttk.Frame(main_container)
        content_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(content_frame, text="Chức năng chính", style="Header.TLabel").pack(pady=(0, 10))

        button_frame = ttk.Frame(content_frame)
        button_frame.pack(expand=True)

        buttons = [
            ("🎥 Camera chấm công", self.open_user_app, "#3498db"),
            ("🔧 Quản trị hệ thống", self.open_admin_app, "#2ecc71"),
            ("❌ Thoát hệ thống", self.on_closing, "#e74c3c"),
        ]

        for text, command, color in buttons:
            frame = ttk.Frame(button_frame, padding=10)
            frame.pack()
            btn = tk.Button(
                frame,
                text=text,
                font=("Segoe UI", 13, "bold"),
                bg=color,
                fg="white",
                height=2,
                width=30,
                bd=0,
                relief=tk.RAISED,
                activebackground="#34495e",
                command=command
            )
            btn.pack()

        # Footer
        footer = ttk.Frame(main_container)
        footer.pack(fill=tk.X, side=tk.BOTTOM, pady=(20, 0))
        ttk.Label(footer, text="© 2025 Hệ thống chấm công G06", style="Status.TLabel").pack()

    # Hàm cập nhật thời gian
    def update_time(self):
        current_time = datetime.now().strftime("%H:%M:%S - %d/%m/%Y")
        self.time_label.config(text=f"🕒 Thời gian: {current_time}")
        self.root.after(1000, self.update_time)

    # Hàm cập nhật trạng thái
    def update_status(self, text, color):
        self.status_indicator.config(bg=color)
        self.status_text.config(text=text)

    # Hàm mở giao diện người dùng
    def open_user_app(self):
        try:
            subprocess.Popen(["python", "gui/user_roles/user.py"])
            self.update_status("Đang chạy camera chấm công", "#27ae60")
            self.root.withdraw()
            self.root.after(1000, self.root.destroy)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể khởi động: {e}")
            self.update_status("Lỗi khi khởi động", "#e74c3c")

    # Hàm mở giao diện quản trị
    def open_admin_app(self):
        try:
            subprocess.Popen(["python", "gui/login_form/admin_login.py"])
            self.update_status("Đang mở quản trị", "#f39c12")
            self.root.withdraw()
            self.root.after(1000, self.root.destroy)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể mở quản trị: {e}")
            self.update_status("Lỗi khi mở quản trị", "#e74c3c")

    # Nút thoát
    def on_closing(self):
        if messagebox.askokcancel("Thoát", "Bạn có chắc muốn thoát hệ thống?"):
            self.root.destroy()


def main():
    root = tk.Tk()
    app = AttendanceSystem(root)
    root.mainloop()


if __name__ == "__main__":
    main()
