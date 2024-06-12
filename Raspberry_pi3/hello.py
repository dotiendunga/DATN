import tkinter as tk
from serial import Serial

# Khởi tạo cửa sổ tkinter
root = tk.Tk()
root.title("GPS Tracker")

# Thiết lập kích thước cho khung hiển thị
root.geometry("400x200")

# Tạo một khung để chứa dữ liệu GPS
gps_frame = tk.Frame(root)
gps_frame.pack(expand=True, padx=10, pady=10)

# Tạo một nhãn để hiển thị dữ liệu GPS
gps_label = tk.Label(gps_frame, text="Waiting for GPS data...", font=("Arial", 14), justify="left")
gps_label.pack(expand=True)

# Kết nối với mô-đul GPS qua cổng serial UART
ser = Serial("/dev/ttyS0", 9600, timeout=1)

def read_gps_data():
    # Đọc dữ liệu từ mô-đul GPS
    gps_data = ser.readline().decode().strip()
    # Cập nhật dữ liệu lên nhãn
    gps_label.config(text=gps_data)
    # Lặp lại sau mỗi 100 ms
    root.after(100, read_gps_data)

# Bắt đầu đọc dữ liệu GPS
read_gps_data()

# Chạy vòng lặp chính của tkinter
root.mainloop()
