
import serial
import pynmea2

# Mở cổng serial UART
ser = serial.Serial('/dev/serial0', 9600, timeout=1)

while True:
    try:
        # Đọc dữ liệu từ cổng serial UART
        data = ser.readline().decode('utf-8', errors='ignore')
        
        # Kiểm tra xem dữ liệu có phải là chuỗi NMEA không
        if data.startswith('$GPGGA'):
            try:
                # Phân tích chuỗi NMEA
                msg = pynmea2.parse(data)
                
                # Trích xuất và in kinh độ, vĩ độ
                latitude = msg.latitude
                longitude = msg.longitude
                print(f'Latitude: {latitude}, Longitude: {longitude}')
            except pynmea2.ParseError as e:
                print("Lỗi parsing:", e)
    except UnicodeDecodeError:
        print("Lỗi decoding: Không thể giải mã dữ liệu")
    except Exception as e:
        print("Lỗi khác:", e)

# Đóng cổng serial UART
ser.close()
