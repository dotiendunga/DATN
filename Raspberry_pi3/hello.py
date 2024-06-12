import tkinter as tk
from serial import Serial

# Tạo cửa sổ tkinter
root = tk.Tk()
root.title("GPS Tracker")

# Tạo một nhãn để hiển thị dữ liệu GPS
gps_label = tk.Label(root, text="Waiting for GPS data...")
gps_label.pack()

# Kết nối với mô-đul GPS qua cổng serial UART
ser = Serial("/dev/ttyS0", 9600, timeout=1)

def read_gps_data():
    while True:
        # Đọc dữ liệu từ mô-đul GPS
        gps_data = ser.readline().decode().strip()
        # Hiển thị dữ liệu trên nhãn
        gps_label.config(text=gps_data)
        root.update()

# Khởi tạo một luồng để đọc dữ liệu GPS mà không làm đóng kịch bản chính
root.after(100, read_gps_data)

# Chạy vòng lặp chính của tkinter
root.mainloop()