import tkinter as tk
from tkinter import ttk
from datetime import datetime
import subprocess
import platform
from tkinter import messagebox

# Hàm cập nhật thời gian
def update_time(label):
    now = datetime.now().strftime("%H:%M:%S - %d/%m/%Y")
    label.config(text=now)
    label.after(1000, update_time, label)

# Nút quay lại
def back_to_home(current_root):
    current_root.destroy()
    subprocess.Popen(["python", "gui/app.py"])

# Nút đăng nhập
def open_login(current_root):
    subprocess.Popen(["python", "gui/login_form/user_login.py"])
    # current_root.destroy()

# Khởi động carmera chấm công
def start_camera():
    script_path = "run_scripts/face_reg.py"  # Đường dẫn tới script face recognition
    
    try:
        if platform.system() == "Windows":
            # Trên Windows, tạo cửa sổ console mới
            process = subprocess.Popen(
                ["python", script_path],
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        elif platform.system() == "Linux":
            # Trên Linux, mở terminal mới để chạy script
            process = subprocess.Popen(
                ["x-terminal-emulator", "-e", f"python3 {script_path}"]
            )
        elif platform.system() == "Darwin":  # macOS
            # Trên Mac, mở Terminal app để chạy script
            process = subprocess.Popen(
                ["open", "-a", "Terminal", script_path]
            )
        else:
            messagebox.showerror("Lỗi", "Hệ điều hành không được hỗ trợ")
            return False
        
        return process  # Trả về process để có thể quản lý sau này
        
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể khởi động camera: {str(e)}")
        return False

def main():
    root = tk.Tk()
    root.title("Hệ thống chấm công bằng camera")
    root.geometry("600x400")
    root.configure(bg="#eaf0f6")

    # Giao diện
    style = ttk.Style()
    style.theme_use("clam")  # Modern style
    style.configure("TFrame", background="#eaf0f6")
    style.configure("TButton",
                    font=("Segoe UI", 12),
                    padding=10)
    style.map("TButton",
              background=[("active", "#3498db")],
              foreground=[("active", "white")])
    style.configure("Header.TLabel",
                    font=("Segoe UI", 18, "bold"),
                    background="#eaf0f6",
                    foreground="#2c3e50")
    style.configure("Status.TLabel",
                    font=("Segoe UI", 10),
                    background="#eaf0f6",
                    foreground="#7f8c8d")

    # Main container
    main_container = ttk.Frame(root, padding=20, style="TFrame")
    main_container.pack(fill=tk.BOTH, expand=True)

    # Header
    header_frame = ttk.Frame(main_container, style="TFrame")
    header_frame.pack(fill=tk.X, pady=(0, 20))

    # Logo
    logo_placeholder = tk.Canvas(header_frame, width=50, height=50, bg="#3498db", highlightthickness=0)
    logo_placeholder.create_text(25, 25, text="G06", fill="white", font=("Segoe UI", 12, "bold"))
    logo_placeholder.pack(side=tk.LEFT)

    # Title + time
    title_frame = ttk.Frame(header_frame, style="TFrame")
    title_frame.pack(side=tk.LEFT, padx=15)

    ttk.Label(title_frame, text="Hệ thống chấm công bằng camera", style="Header.TLabel").pack(anchor=tk.W)

    time_label = ttk.Label(title_frame, text="", style="Status.TLabel")
    time_label.pack(anchor=tk.W)
    update_time(time_label)

    # Content
    content_frame = ttk.Frame(main_container, padding=10, style="TFrame")
    content_frame.pack(expand=True)

    ttk.Button(content_frame, text="▶ Khởi động camera chấm công", width=40, command=start_camera).pack(pady=10)
    ttk.Button(content_frame, text="🔄 Quay lại màn hình chính", width=40, command=lambda: back_to_home(root)).pack(pady=10)
    ttk.Button(content_frame, text="🔐 Đăng nhập để xem trạng thái chấm công", width=40, command=lambda: open_login(root)).pack(pady=10)

    # Footer
    footer_frame = ttk.Frame(main_container, style="TFrame")
    footer_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=(20, 0))

    ttk.Label(footer_frame,
              text="© 2025 Hệ thống chấm công tự động | Nhóm G06",
              style="Status.TLabel").pack(side=tk.LEFT)

    root.mainloop()

if __name__ == "__main__":
    main()
