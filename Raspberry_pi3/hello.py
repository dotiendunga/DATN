import serial
import pynmea2

def parse_gps(line):
    msg = pynmea2.parse(line)
    print((msg.timestamp, msg.latitude, msg.longitude))


serial_port = serial.Serial('/dev/ttyAMA0', 9600, timeout=5)
while True:
    line = serial_port.readline().decode('unicode_escape')

    if 'GGA' in line:
        parse_gps(line)