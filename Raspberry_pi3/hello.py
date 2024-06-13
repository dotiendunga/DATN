import serial
import pynmea2

def parse_gps(line):
    try:
        msg = pynmea2.parse(line)
        if isinstance(msg, pynmea2.types.talker.RMC):
            direction = get_direction(msg.true_course) if msg.true_course is not None else "Unknown"
            print("RMC:", {
                "timestamp": msg.timestamp,
                "latitude": msg.latitude,
                "longitude": msg.longitude,
                "spd_over_grnd": msg.spd_over_grnd,  # Tốc độ qua mặt đất (knots)
                "true_course": get_direction(msg.true_course),
                "direction": direction,
                "datestamp": msg.datestamp
            })
        else:
            pass
    except pynmea2.ParseError as e:
        print(f"Parse error: {e}")
        
def get_direction(true_course):
    if true_course is None:
        return "Unknown"
    directions = [
        "Bắc", "Bắc Đông Bắc", "Đông Bắc", "Đông Đông Bắc",
        "Đông", "Đông Đông Nam", "Đông Nam", "Nam Đông Nam",
        "Nam", "Nam Tây Nam", "Tây Nam", "Tây Tây Nam",
        "Tây", "Tây Tây Bắc", "Tây Bắc", "Bắc Tây Bắc"
    ]
    idx = int((true_course + 11.25) % 360 / 22.5)
    return directions[idx]

# Mở cổng serial
serial_port = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)

try:
    while True:
        line = serial_port.readline().decode('unicode_escape')  # Đọc dòng dữ liệu từ cổng serial
        if line.startswith('$GPGGA') or line.startswith('$GPRMC') or line.startswith('$GPGSV'):  # Kiểm tra xem dòng dữ liệu là thông điệp GGA, RMC hoặc GSV không
            parse_gps(line)
except KeyboardInterrupt:
    print("Dừng đọc dữ liệu GPS.")
finally:
    serial_port.close()  # Đóng cổng serial khi kết thúc