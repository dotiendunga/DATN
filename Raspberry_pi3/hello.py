import serial
import pynmea2

# Mở cổng serial UART
ser = serial.Serial('/dev/ttyS0', 9600, timeout=1)

while True:
    try:
        # Đọc dữ liệu từ cổng serial UART
        data = ser.readline()
        
        # Giải mã dữ liệu từ cổng Serial UART với encoding ASCII
        data_decoded = data.decode('ascii', errors='ignore')
        
        # In dữ liệu để kiểm tra
        print(data_decoded)
        
        # Kiểm tra xem dữ liệu có phải là chuỗi NMEA không
        if data_decoded.startswith('$GPGGA'):
            try:
                # Phân tích chuỗi NMEA
                msg = pynmea2.parse(data_decoded)
                print(f'GPGGA: Latitude: {msg.latitude}, Longitude: {msg.longitude}')
            except pynmea2.ParseError as e:
                print("Lỗi parsing GPGGA:", e)
        
        elif data_decoded.startswith('$GPRMC'):
            try:
                # Phân tích chuỗi NMEA
                msg = pynmea2.parse(data_decoded)
                print(f'GPRMC: Speed (knots): {msg.spd_over_grnd}')
            except pynmea2.ParseError as e:
                print("Lỗi parsing GPRMC:", e)
        
        elif data_decoded.startswith('$GPVTG'):
            try:
                # Phân tích chuỗi NMEA
                msg = pynmea2.parse(data_decoded)
                print(f'GPVTG: Speed (km/h): {msg.spd_over_grnd_kmph}')
            except pynmea2.ParseError as e:
                print("Lỗi parsing GPVTG:", e)

    except UnicodeDecodeError:
        print("Lỗi decoding: Không thể giải mã dữ liệu")
    except Exception as e:
        print("Lỗi khác:", e)

# Đóng cổng serial UART
ser.close()
