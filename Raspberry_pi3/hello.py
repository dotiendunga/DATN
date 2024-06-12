# import serial
# import pynmea2

# def parse_gps(line):
#     msg = pynmea2.parse(line)
#     print((msg.timestamp, msg.latitude, msg.longitude))


# serial_port = serial.Serial('/dev/ttyAMA0', 9600, timeout=5)
# while True:
#     line = serial_port.readline().decode('unicode_escape')

#     if 'GGA' in line:
#         parse_gps(line)
import serial
import pynmea2

# Mở cổng serial UART
ser = serial.Serial("/dev/ttyS0", 9600, timeout=1)

while True:
    # Đọc dữ liệu từ cổng serial UART
    data = ser.readline().decode('utf-8')

    # Kiểm tra xem dữ liệu có phải là chuỗi NMEA không
    if data.startswith('$GPGGA'):
        try:
            # Phân tích chuỗi NMEA
            msg = pynmea2.parse(data)
            
            # Trích xuất tốc độ (nếu có)
            speed = msg.spd_over_grnd_kmph if hasattr(msg, 'spd_over_grnd_kmph') else None
            print('Tốc độ (km/h):', speed)
            
            # Trích xuất địa chỉ (nếu có)
            address = (msg.latitude, msg.longitude) if hasattr(msg, 'latitude') and hasattr(msg, 'longitude') else None
            print('Địa chỉ:', address)
        except pynmea2.ParseError as e:
            print('Lỗi phân tích:', e)

# Đóng cổng serial UART
ser.close()