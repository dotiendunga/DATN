import serial
import pynmea2
import paho.mqtt.client as paho
from paho import mqtt
import tkinter as tk
from tkinter import *
import tkintermapview 
from tkinter import ttk
from PIL import ImageTk, Image
from datetime import datetime
import threading
import time 
import queue


# Using queue to get data from thread GPS 
data_queue = queue.Queue()

# MQTT Broker Connection Details
mqtt_broker = "ae501b5ee3194ca682bd67e257459478.s1.eu.hivemq.cloud"
mqtt_username = "RainWay System"
mqtt_password = "012301230123aA#"
mqtt_port = 8883
mqtt_topic_1 = "esp8266/Location_data"

def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)
    global status_connect
    status_connect = rc
    client.subscribe(mqtt_topic_1)

def on_message(client, userdata, message):
    print("Received message '" 
        + str(message.payload.decode("utf-8")) 
        + "' on topic '"+ message.topic 
        + "' with QoS " + str(message.qos))
    data = str(message.payload.decode("utf-8"))

client = paho.Client(paho.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
client.username_pw_set(mqtt_username, mqtt_password)
client.connect(mqtt_broker, mqtt_port)
client.on_message = on_message
client.loop_start()

Location = ""
Latitude_values = 0.0
Longitude_values = 0.0
direction = ""
Speed = 0.0

def parse_gps(line):
    try:
        if line.startswith('$GPGGA') or line.startswith('$GPRMC') or line.startswith('$GPGSV'):
            msg = pynmea2.parse(line)
            if isinstance(msg, pynmea2.types.talker.RMC):
                data_queue.put(msg)
    except pynmea2.ParseError as e:
        print(f"Parse error: {e}")   
    except KeyboardInterrupt:
        print("Dừng đọc dữ liệu GPS.")

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

def read_gps():
    serial_port = serial.Serial('/dev/ttyS0', 9600, timeout=5)
    while True:
        try:
            line = serial_port.readline().decode('unicode_escape')
            parse_gps(line)
            time.sleep(1)
        except Exception as e:
            print("Exception in read_gps:", e)
            time.sleep(1)

class RootApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Train System")
        self.geometry("1280x720")
        self.resizable(True, True)
        self.configure(bg='gray')
        self.title("Điều khiển Tàu Hỏa")

        img = PhotoImage(file='image/eye.png')
        self.tk.call('wm', 'iconphoto', self._w, img)

        self.image = Image.open(r"image/control.png")
        self.img = ImageTk.PhotoImage(self.image)
        self.label_Bg = tk.Label(self, image=self.img)
        self.label_Bg.pack(fill='both', expand=True)

        self.frame2 = Frame2(self)
        self.frame2.config(bg="white")
        self.frame2.pack(fill='both', expand=True, padx=10, pady=10)

        self.label_time = tk.Label(self, font=('arial', 12, 'bold'), fg="#4660ac",
                                   borderwidth=0, border=0, relief='groove', justify=CENTER)
        self.label_time.place(relx=0.02, rely=0.02)

        self.update_time()

    def update_time(self):
        global current_time
        current_time = datetime.now().strftime('%Y-%m-%d  %H:%M:%S')
        self.label_time.config(text=current_time)
        self.label_time.after(1000, self.update_time)

class Frame2(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.data_queue = data_queue

        self.header2_1 = Label(self, text="Kinh Độ", fg='white', bg="#4660ac", width=12,
                               borderwidth=0, justify=CENTER, font=("arial", 12, "bold"), relief='groove', pady=2)
        self.header2_1.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        self.header2_2 = Label(self, text="Vĩ Độ", fg='white', bg="#4660ac", width=12,
                               borderwidth=0, justify=CENTER, font=("arial", 12, "bold"), relief='groove', pady=2)
        self.header2_2.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

        self.header2_3 = Label(self, text="Tốc độ", fg='white', bg="#4660ac", width=12,
                               borderwidth=0, justify=CENTER, font=("arial", 12, "bold"), relief='groove', pady=2)
        self.header2_3.grid(row=2, column=0, padx=5, pady=5, sticky='nsew')

        self.header2_4 = Label(self, text="Địa chỉ", fg='white', bg="#4660ac", width=15,
                               borderwidth=0, justify=CENTER, font=("arial", 12, "bold"), relief='groove', pady=2)
        self.header2_4.grid(row=0, column=2, padx=5, pady=5, sticky='nsew')

        self.header2_5 = Label(self, text="Khoảng cách", fg='white', bg="#4660ac", width=15,
                               borderwidth=0, justify=CENTER, font=("arial", 12, "bold"), relief='groove', pady=2)
        self.header2_5.grid(row=1, column=2, padx=5, pady=5, sticky='nsew')

        self.header2_6 = Label(self, text="Hướng tàu", fg='white', bg="#4660ac", width=15,
                               borderwidth=0, justify=CENTER, font=("arial", 12, "bold"), relief='groove', pady=2)
        self.header2_6.grid(row=2, column=2, padx=5, pady=5, sticky='nsew')

        self.latitude = Label(self, text="Kinh Độ", fg='Gray', width=17,
                              borderwidth=0, justify=CENTER, font=("arial", 10, "bold"), relief='groove', pady=2)
        self.latitude.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')

        self.Longitude = Label(self, text="Vĩ Độ", fg='Gray', width=17,
                               borderwidth=0, justify=CENTER, font=("arial", 10, "bold"), relief='groove', pady=2)
        self.Longitude.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')

        self.Speed = Label(self, text="Tốc Độ", fg='Gray', width=17,
                           borderwidth=0, justify=CENTER, font=("arial", 10, "bold"), relief='groove', pady=2)
        self.Speed.grid(row=2, column=1, padx=5, pady=5, sticky='nsew')

        self.Address = Label(self, text="Địa chỉ", fg='Gray', width=21,
                             borderwidth=0, justify=CENTER, font=("arial", 9, "bold"), relief='groove', pady=2)
        self.Address.grid(row=0, column=3, padx=5, pady=5, sticky='nsew')

        self.Distance = Label(self, text="Khoảng cách", fg='Gray', width=21,
                              borderwidth=0, justify=CENTER, font=("arial", 9, "bold"), relief='groove', pady=2)
        self.Distance.grid(row=1, column=3, padx=5, pady=5, sticky='nsew')

        # self.Heading = Label(self, text="Hướng tàu", fg='Gray', width=17,
        self.marker1 = self.map_widget.set_position(self.data.latitude, self.data.longitude, text="Điểm mục tiêu", marker=True)
        self.marker1.deleted()
                                                                  
                                                            
