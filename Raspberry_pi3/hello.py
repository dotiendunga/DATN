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
ser = serial.Serial("/dev/ttyAMA0", 9600, timeout=1)

while True:
    try:
        # Đọc dữ liệu từ cổng serial UART
        data = ser.readline()

        # Giải mã dữ liệu từ cổng Serial UART với encoding ASCII
        data_decoded = data.decode('ascii')

        # Kiểm tra xem dữ liệu có phải là chuỗi NMEA không
        if data_decoded.startswith('$GPGGA'):
            # Phân tích chuỗi NMEA
            msg = pynmea2.parse(data_decoded)
            
            # Trích xuất thông tin tốc độ và địa chỉ từ chuỗi NMEA
            # ...
    
    except UnicodeDecodeError:
        print("Lỗi decoding: Không thể giải mã dữ liệu")
    except pynmea2.ParseError as e:
        print("Lỗi parsing:", e)

# Đóng cổng serial UART
ser.close()