import threading
import paho.mqtt.client as paho
from paho import mqtt
import json
import tkinter as tk
from tkinter import *
import tkintermapview 
from tkinter import ttk
import time 
mqtt_broker = "ae501b5ee3194ca682bd67e257459478.s1.eu.hivemq.cloud"
mqtt_username = "RainWay System"
mqtt_password = "012301230123aA#"
mqtt_port = 8883
mqtt_topic_1 = "esp8266/Location_data"

mqtt_topic_2 = "esp8266/Location_data2"
latitude_values=""
longitude_values=""
class HiveMQTTClient():
    def __init__(self, broker,username,password, port, topic):
        self.topic = topic
        self.client = paho.Client(paho.CallbackAPIVersion.VERSION2)
        self.client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.username_pw_set(username,password)
        self.client.connect(broker,port)
    def on_connect(self,client, userdata, flags, rc, properties=None):
        print("CONNACK received with code %s." % rc)
        # subscribe 1 topic 
        client.subscribe(self.topic)
    # Callback function khi nhận được tin nhắn từ MQTT Broker
    def on_message(self,client, userdata, message):
        print("Received message '" 
            + str(message.payload.decode("utf-8")) 
            + "' on topic '"+ message.topic 
            + "' with QoS " + str(message.qos))
        data = json.loads(str(message.payload.decode("utf-8")) )
        global latitude_values,longitude_values
        # ,latitude_values_esp,longitude_values_esp,train_id
        latitude_values=data["Latitude"]
        longitude_values=data["Longitude"]
        print(latitude_values)
        print(longitude_values)
    def client_loop(self):
        self.client.loop_start()
    def disconnect(self):
        self.client.loop_stop()
class RootApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Train System")
        self.geometry("1280x720+150+20")
        self.resizable(False,False)
        self.configure(bg='gray')
        self.title("Hệ Thống Tàu Hỏa")
        self.mqtt_instance1 = HiveMQTTClient(mqtt_broker,mqtt_username,mqtt_password,mqtt_port,mqtt_topic_1)
        self.mqtt_instance2 = HiveMQTTClient(mqtt_broker,mqtt_username,mqtt_password,mqtt_port,mqtt_topic_2)
        self.combobox = ttk.Combobox(self, values=["Thread 1", "Thread 2"])
        self.combobox.place(x=945,y=410)
        # Khi có sự kiện thay đổi lựa chọn trong Combobox, gọi hàm on_select
        self.combobox.bind("<<ComboboxSelected>>", self.on_select)
        self.t1_data_station= threading.Thread(target=self.mqtt_instance1.client_loop,daemon=True)
        self.t2_data_station= threading.Thread(target=self.mqtt_instance2.client_loop,daemon=True)
        self.t1_data_station.start()
        self.t2_data_station.start()
    def on_select(self,event):
        selected_function = self.combobox.get()
        if selected_function == "Thread 1":
            self.mqtt_instance2.disconnect()
            self.mqtt_instance1.client_loop()
        elif selected_function == "Thread 2":
            self.mqtt_instance1.disconnect()
            self.mqtt_instance2.client_loop()
# Sử dụng lớp MQTT
if __name__ == "__main__":
    app = RootApplication()
    app.mainloop()
