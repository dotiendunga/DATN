import tkinter as tk
from tkinter import *
import tkintermapview 
from tkinter import ttk
from PIL import ImageTk, Image
from datetime import datetime
import paho.mqtt.client as paho
from paho import mqtt
from tkinter import filedialog, messagebox
from openpyxl import Workbook
import haversine as hs   
from haversine import Unit
import time 
# import simpleaudio as sa
# from playsound import playsound
import json 

import threading
class MQTTClient():
    def __init__(self, broker, port, username, password, topic):
        self.broker = broker
        self.port = port
        self.username = username
        self.password = password
        self.topic = topic
        # client_id is the given name of the client 
        self.client = paho.Client(paho.CallbackAPIVersion.VERSION2)
        self.client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.username_pw_set(self.username, self.password)
        self.client.connect(self.broker, self.port)
        self.client.loop_start()
        
    def on_connect(self,client, userdata, flags, rc, properties=None):
        print("CONNACK received with code %s." % rc)
        # subscribe 1 topic 
        global status_connect
        status_connect = rc
        self.client.subscribe(mqtt_topic_1)
    # Callback function khi nhận được tin nhắn từ MQTT Broker
    def on_message(self,client, userdata, message):
        print("Received message '" 
            + str(message.payload.decode("utf-8")) 
            + "' on topic '"+ message.topic 
            + "' with QoS " + str(message.qos))
        data = str(message.payload.decode("utf-8"))
    # Publish data to hivemq
    def send_data_to_hivemq(self,time, speed, latitude, longitude, direction):
        # Tạo một dictionary chứa thông số cần gửi
        data = {
            "time": time,
            "speed": speed,
            "latitude": latitude,
            "longitude": longitude,
            "direction": direction
        }
        # Chuyển đổi dictionary thành chuỗi JSON
        json_data = json.dumps(data)
        # Đẩy dữ liệu lên topic MQTT
        self.client.publish(mqtt_topic_1, json_data)
    def start(self):
        self.client.loop_start()
            
        # #------------------------------------------------------ Update data when receive data from cloud ------------------------------------------

class Application(tk.Tk):
    def __init__(self, mqtt_client):
        super().__init__()
        self.mqtt_client = mqtt_client
        self.title("MQTT Tkinter Example")
        self.geometry("400x300")

        self.label = tk.Label(self, text="MQTT Client Interface")
        self.label.pack(pady=10)

        self.send_button = tk.Button(self, text="Send Data", command=self.send_data)
        self.send_button.pack(pady=10)

    def send_data(self):
        # Example of sending data
        self.mqtt_client.send_data_to_hivemq("12:00", 60, 21.028511, 105.804817, "North")
        messagebox.showinfo("Info", "Data sent to HiveMQ")


mqtt_broker = "ae501b5ee3194ca682bd67e257459478.s1.eu.hivemq.cloud"
mqtt_username = "RainWay System"
mqtt_password = "012301230123aA#"
mqtt_port = 8883
mqtt_topic_1 = "esp8266/Location_data"
def main():
    mqtt_client = MQTTClient(mqtt_broker, mqtt_port, mqtt_username, mqtt_password, mqtt_topic_1)
    mqtt_client.start()

    app = Application(mqtt_client)
    app.mainloop()

if __name__ == "__main__":
    main()
