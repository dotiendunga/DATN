from serial import Serial

# Kết nối với mô-đul GPS qua cổng serial UART
ser = Serial("/dev/ttyS0", 9600, timeout=1)

def read_gps_data():
    while True:
        # Đọc dữ liệu từ mô-đul GPS
        gps_data = ser.readline().decode().strip()
        # In dữ liệu ra terminal
        print("GPS data:", gps_data)

# Bắt đầu đọc dữ liệu GPS
read_gps_data()