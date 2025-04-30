import tkinter as tk
from tkinter import messagebox, ttk
import subprocess
import sys
import os

def dang_nhap():
    username = entry_username.get()
    password = entry_password.get()
    if username == "admin" and password == "123":
        log_label.config(text="✅ Đăng nhập thành công", foreground="green")
        root.after(1000, lambda: open_admin_interface())
    else:
        log_label.config(text="❌ Sai tài khoản hoặc mật khẩu")
        messagebox.showerror("Thất bại", "Sai tên tài khoản hoặc mật khẩu.")

def open_admin_interface():
    root.destroy()
    subprocess.Popen(["python", "gui/user_roles/admin.py"])
    sys.exit()

def back_to_home():
    root.destroy()
    subprocess.Popen(["python", "gui/app.py"])
    sys.exit()

def on_enter(e):
    e.widget.config(background="#2980b9")

def on_leave(e):
    e.widget.config(background="#3498db")

def create_hover_button(parent, text, command):
    btn = tk.Button(parent, text=text, font=("Arial", 12), width=20,
                    bg="#3498db", fg="white", activebackground="#2980b9",
                    relief="raised", bd=2, command=command)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    btn.pack(pady=8)
    return btn

# Tạo cửa sổ
root = tk.Tk()
root.title("Đăng nhập hệ thống")
root.geometry("400x300")
root.configure(bg="#f0f0f0")
root.resizable(False, False)

style = ttk.Style()
style.configure("TLabel", background="#f0f0f0", font=("Arial", 11))
style.configure("Title.TLabel", font=("Arial", 16, "bold"))

# Khung chứa chính
main_frame = ttk.Frame(root, padding=20)
main_frame.pack(expand=True)

# Header
header_frame = ttk.Frame(main_frame)
header_frame.pack(pady=(0, 10))

logo = tk.Canvas(header_frame, width=40, height=40, bg="#3498db", highlightthickness=0)
logo.create_text(20, 20, text="G06", fill="white", font=("Arial", 10, "bold"))
logo.pack(side=tk.LEFT, padx=10)

ttk.Label(header_frame, text="Đăng nhập hệ thống", style="Title.TLabel").pack(side=tk.LEFT)

# Form
form_frame = ttk.Frame(main_frame)
form_frame.pack(pady=10)

ttk.Label(form_frame, text="Tài khoản:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
entry_username = tk.Entry(form_frame, font=("Arial", 11))
entry_username.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(form_frame, text="Mật khẩu:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
entry_password = tk.Entry(form_frame, show="*", font=("Arial", 11))
entry_password.grid(row=1, column=1, padx=5, pady=5)

# Nút
btn_frame = ttk.Frame(main_frame)
btn_frame.pack()

create_hover_button(btn_frame, "🔐 Đăng nhập", dang_nhap)
create_hover_button(btn_frame, "⬅️ Quay lại", back_to_home)

# Label trạng thái
log_label = ttk.Label(main_frame, text="", foreground="gray")
log_label.pack(pady=5)

# ESC thoát nhanh
root.bind("<Escape>", lambda e: back_to_home())

root.mainloop()
