import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import subprocess
import os
import platform
import sys

running_processes = []

# Hàm cập nhật thời gian
def update_time(label):
    now = datetime.now().strftime("%H:%M:%S - %d/%m/%Y")
    label.config(text=now)
    label.after(1000, update_time, label)

# Hàm dừng tiến tình hiện tại để chạy tiến trình mới
def stop_process():
    global running_processes
    for process in running_processes:
        try:
            if platform.system() == "Windows":
                subprocess.call(['taskkill', '/F', '/T', '/PID', str(process.pid)])
            else:
                process.terminate()
        except Exception as e:
            print(f"Lỗi khi dừng tiến trình: {e}")
    running_processes = []

# Chạy tiến trình sau khi đã dừng tiến trình hiện tại
def run_script_with_process_management(script_path, root, log_label=None):
    global running_processes
    try:
        stop_process()
        root.configure(bg="#f8fafc")
        if log_label:
            log_label.config(text="⏳ Đang thực thi script...")

        if platform.system() == "Windows":
            process = subprocess.Popen(["python", script_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
        elif platform.system() == "Linux":
            process = subprocess.Popen(["x-terminal-emulator", "-e", f"python3 {script_path}"])
        elif platform.system() == "Darwin":
            process = subprocess.Popen(["open", "-a", "Terminal", script_path])
        else:
            messagebox.showerror("Lỗi", "Hệ điều hành không được hỗ trợ")
            return False

        running_processes.append(process)
        if log_label:
            log_label.config(text="✅ Script đã chạy thành công")
        root.configure(bg="#f8fafc")
        return True

    except Exception as e:
        if log_label:
            log_label.config(text="❌ Lỗi khi chạy script")
        messagebox.showerror("Lỗi", f"Không thể chạy script: {e}")
        return False

# Chụp ảnh nhân viên mới
def capture_new_employee(root, log_label):
    script_path = os.path.join(os.path.dirname(__file__), "../../run_scripts/face_capture.py")
    run_script_with_process_management(script_path, root, log_label)

# Xem danh sách nhân viên
def view_employee_state(log_label):
    stop_process()
    script_path = os.path.join(os.path.dirname(__file__), "../../run_scripts/view_employees.py")
    try:
        subprocess.Popen(["python", script_path])
        if log_label:
            log_label.config(text="📋 Đã mở danh sách nhân viên")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể mở danh sách nhân viên: {e}")
        if log_label:
            log_label.config(text="❌ Không thể mở danh sách nhân viên")

def view_employee_info(log_label):
    stop_process()
    script_path = os.path.join(os.path.dirname(__file__), "../../run_scripts/view_employee_info.py")
    try:
        subprocess.Popen(["python", script_path])
        if log_label:
            log_label.config(text="📋 Đã mở thông tin nhân viên")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể mở thông tin nhân viên: {e}")
        if log_label:
            log_label.config(text="❌ Không thể mở thông tin nhân viên")

# Khôi phục lại trạng thái nhân viên
def restore_employee_state(root, log_label):
    confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn khôi phục trạng thái chấm công không?")
    if not confirm:
        return
    script_path = os.path.join(os.path.dirname(__file__), "../../run_scripts/reset_db.py")
    run_script_with_process_management(script_path, root, log_label)

# Xóa nhân viên cũ
def delete_employee(log_label):
    stop_process()
    script_path = os.path.join(os.path.dirname(__file__), "../../run_scripts/delete_employee.py")
    try:
        subprocess.Popen(["python", script_path])
        if log_label:
            log_label.config(text="📋 Đã mở danh sách nhân viên")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể mở danh sách nhân viên: {e}")
        if log_label:
            log_label.config(text="❌ Không thể mở danh sách nhân viên")

# Nút quay lạ
def back_to_home(current_window):
    stop_process()
    script_path = os.path.join(os.path.dirname(__file__), "../app.py")
    try:
        subprocess.Popen(["python", script_path])
        current_window.destroy()
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể quay lại ứng dụng chính: {e}")

# Tạo nút hover
def on_enter(e):
    e.widget.config(bg="#0ea5e9")

def on_leave(e):
    e.widget.config(bg="#0284c7")

def create_hover_button(parent, text, command):
    btn = tk.Button(parent, text=text, font=("Segoe UI", 13, "bold"), width=40,
                    bg="#0284c7", fg="white", activebackground="#0ea5e9",
                    relief="flat", bd=0, command=command, cursor="hand2",
                    padx=12, pady=12)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    btn.pack(pady=12)
    return btn

def main():
    root = tk.Tk()
    root.title("📊 Quản trị hệ thống chấm công")
    root.geometry("900x750")
    root.configure(bg="#f8fafc")
    
    # Giao diện
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TFrame", background="#f8fafc")
    style.configure("Header.TLabel", font=("Segoe UI", 20, "bold"), background="#f8fafc", foreground="#0f172a")
    style.configure("Status.TLabel", font=("Segoe UI", 11), background="#f8fafc", foreground="#64748b")

    main_container = ttk.Frame(root, padding=24)
    main_container.pack(fill=tk.BOTH, expand=True)

    header_frame = ttk.Frame(main_container)
    header_frame.pack(fill=tk.X, pady=(0, 20))

    logo_placeholder = tk.Canvas(header_frame, width=55, height=55, bg="#0ea5e9", highlightthickness=0)
    logo_placeholder.create_text(28, 28, text="G06", fill="white", font=("Segoe UI", 13, "bold"))
    logo_placeholder.pack(side=tk.LEFT)

    title_frame = ttk.Frame(header_frame)
    title_frame.pack(side=tk.LEFT, padx=16)

    ttk.Label(title_frame, text="Bảng điều khiển chấm công", style="Header.TLabel").pack(anchor=tk.W)

    time_label = ttk.Label(title_frame, text="", style="Status.TLabel")
    time_label.pack(anchor=tk.W)
    update_time(time_label)

    status_frame = ttk.Frame(header_frame)
    status_frame.pack(side=tk.RIGHT, padx=10)

    ttk.Label(status_frame, text="Trạng thái:", style="Status.TLabel").pack(side=tk.LEFT)
    status_indicator = tk.Canvas(status_frame, width=16, height=16, bg="#10b981", highlightthickness=0)
    status_indicator.pack(side=tk.LEFT)
    ttk.Label(status_frame, text="Đang hoạt động", style="Status.TLabel").pack(side=tk.LEFT, padx=6)

    content_frame = ttk.Frame(main_container)
    content_frame.pack(expand=True)

    log_label = ttk.Label(main_container, text="", style="Status.TLabel", foreground="#9ca3af")
    log_label.pack(anchor=tk.W, pady=(0, 10))
    
    # Tạo nút
    create_hover_button(content_frame, "📷 Chụp ảnh nhân viên mới", lambda: capture_new_employee(root, log_label))
    create_hover_button(content_frame, "📋 Xem lịch chấm công nhân viên", lambda: view_employee_state(log_label))
    create_hover_button(content_frame, "📋 Quản lý danh sách nhân viên", lambda: view_employee_info(log_label))
    create_hover_button(content_frame, "🔁 Khôi phục trạng thái nhân viên", lambda: restore_employee_state(root, log_label))
    create_hover_button(content_frame, "⬅️ Quay lại ứng dụng chính", lambda: back_to_home(root))

    footer_frame = ttk.Frame(main_container)
    footer_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=10)
    ttk.Label(footer_frame, text="© 2025 Hệ thống chấm công tự động | Nhóm G06", style="Status.TLabel").pack(side=tk.LEFT)

    root.bind("<Escape>", lambda e: back_to_home(root))
    root.mainloop()

if __name__ == "__main__":
    main()
