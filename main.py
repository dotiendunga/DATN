# import threading
# import paho.mqtt.client as paho
# from paho import mqtt
# import json
# import tkinter as tk
# from tkinter import *
# import tkintermapview 
# from tkinter import ttk
# import time 
# mqtt_broker = "ae501b5ee3194ca682bd67e257459478.s1.eu.hivemq.cloud"
# mqtt_username = "RainWay System"
# mqtt_password = "012301230123aA#"
# mqtt_port = 8883
# mqtt_topic_1 = "esp8266/Location_data"

# mqtt_topic_2 = "esp8266/Location_data2"
# latitude_values=""
# longitude_values=""
# class HiveMQTTClient():
#     def __init__(self, broker,username,password, port, topic):
#         self.topic = topic
#         self.client = paho.Client(paho.CallbackAPIVersion.VERSION2)
#         self.client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
#         self.client.on_connect = self.on_connect
#         self.client.on_message = self.on_message
#         self.client.username_pw_set(username,password)
#         self.client.connect(broker,port)
#     def on_connect(self,client, userdata, flags, rc, properties=None):
#         print("CONNACK received with code %s." % rc)
#         # subscribe 1 topic 
#         client.subscribe(self.topic)
#     # Callback function khi nhận được tin nhắn từ MQTT Broker
#     def on_message(self,client, userdata, message):
#         print("Received message '" 
#             + str(message.payload.decode("utf-8")) 
#             + "' on topic '"+ message.topic 
#             + "' with QoS " + str(message.qos))
#         data = json.loads(str(message.payload.decode("utf-8")) )
#         global latitude_values,longitude_values
#         # ,latitude_values_esp,longitude_values_esp,train_id
#         latitude_values=data["Latitude"]
#         longitude_values=data["Longitude"]
#         print(latitude_values)
#         print(longitude_values)
#     def client_loop(self):
#         self.client.loop_start()
#     def disconnect(self):
#         self.client.loop_stop()
# class RootApplication(tk.Tk):
#     def __init__(self):
#         super().__init__()
#         self.title("Train System")
#         self.geometry("1280x720+150+20")
#         self.resizable(False,False)
#         self.configure(bg='gray')
#         self.title("Hệ Thống Tàu Hỏa")
#         self.mqtt_instance1 = HiveMQTTClient(mqtt_broker,mqtt_username,mqtt_password,mqtt_port,mqtt_topic_1)
#         self.mqtt_instance2 = HiveMQTTClient(mqtt_broker,mqtt_username,mqtt_password,mqtt_port,mqtt_topic_2)
#         self.combobox = ttk.Combobox(self, values=["Thread 1", "Thread 2"])
#         self.combobox.place(x=945,y=410)
#         # Khi có sự kiện thay đổi lựa chọn trong Combobox, gọi hàm on_select
#         self.combobox.bind("<<ComboboxSelected>>", self.on_select)
#         self.t1_data_station= threading.Thread(target=self.mqtt_instance1.client_loop,daemon=True)
#         self.t2_data_station= threading.Thread(target=self.mqtt_instance2.client_loop,daemon=True)
#         self.t1_data_station.start()
#         self.t2_data_station.start()
#     def on_select(self,event):
#         selected_function = self.combobox.get()
#         if selected_function == "Thread 1":
#             self.mqtt_instance2.disconnect()
#             self.mqtt_instance1.client_loop()
#         elif selected_function == "Thread 2":
#             self.mqtt_instance1.disconnect()
#             self.mqtt_instance2.client_loop()
# # Sử dụng lớp MQTT
# if __name__ == "__main__":
#     app = RootApplication()
#     app.mainloop()

# string = '0.0011694 0.0027680'
# parts = string.split()  # Tách chuỗi thành danh sách các phần

# # In các phần đã tách
# print(ppart1 = parts[0]
# print(type(part1))  # Output: 0.0011694

# # Phần thứ hai
# part2 = parts[1]
# print(part2)  # Output: 0.0027680
# arts)  # Output: ['0.0011694', '0.0027680']

# # Phần thứ nhất

import tkinter as tk
import webbrowser
import folium

def show_map(latitude, longitude):
    # Tạo bản đồ Folium
    m = folium.Map(location=[latitude, longitude], zoom_start=10)
    
    # Thêm đánh dấu vị trí lên bản đồ
    folium.Marker([latitude, longitude], popup='Your Location').add_to(m)
    
    # Lưu bản đồ vào tệp HTML
    m.save('map.html')
    
    # Mở trình duyệt để hiển thị bản đồ
    webbrowser.open('map.html')

def refresh_page():
    # Đóng cửa sổ hiện tại
    root.destroy()
    # Tạo cửa sổ mới
    create_main_window()

def create_main_window():
    global root
    root = tk.Tk()
    root.title("GPS Location Viewer")
    
    # Tạo nút để hiển thị vị trí
    show_location_button = tk.Button(root, text="Show Location", command=lambda: show_map(10.7809, 106.6297))
    show_location_button.pack(pady=10)
    
    # Tạo nút để làm mới trang
    refresh_button = tk.Button(root, text="Refresh Page", command=refresh_page)
    refresh_button.pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    create_main_window()
    