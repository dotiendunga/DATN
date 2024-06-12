import serial
import pynmea2

# Mở cổng serial UART
ser = serial.Serial('/dev/ttyAMA0)', 9600, timeout=1)

while True:
    try:
        # Đọc dữ liệu từ cổng serial UART
        data = ser.readline()
        
        # Giải mã dữ liệu từ cổng Serial UART với encoding ASCII
        data_decoded = data.decode('ascii', errors='ignore')
        
        # Kiểm tra xem dữ liệu có phải là chuỗi NMEA không
        if data_decoded.startswith('$GPGGA'):
            # Phân tích chuỗi NMEA
            msg = pynmea2.parse(data_decoded)
            
            # Trích xuất thông tin địa chỉ
            if hasattr(msg, 'latitude') and hasattr(msg, 'longitude'):
                print(f'Latitude: {msg.latitude}, Longitude: {msg.longitude}')
        
        elif data_decoded.startswith('$GPRMC'):
            # Phân tích chuỗi NMEA
            msg = pynmea2.parse(data_decoded)
            
            # Trích xuất thông tin tốc độ
            if hasattr(msg, 'spd_over_grnd'):
                print(f'Speed (knots): {msg.spd_over_grnd}')
        
        elif data_decoded.startswith('$GPVTG'):
            # Phân tích chuỗi NMEA
            msg = pynmea2.parse(data_decoded)
            
            # Trích xuất thông tin tốc độ
            if hasattr(msg, 'spd_over_grnd_kmph'):
                print(f'Speed (km/h): {msg.spd_over_grnd_kmph}')

    except UnicodeDecodeError:
        print("Lỗi decoding: Không thể giải mã dữ liệu")
    except pynmea2.ParseError as e:
        print("Lỗi parsing:", e)

# Đóng cổng serial UART
ser.close()
