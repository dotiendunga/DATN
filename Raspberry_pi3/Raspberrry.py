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
import json 
import serial
import math
import numpy as np
import pynmea2

# #----------------------------config GPS------------------------
 
# # Neo 6M VCC -----> Raspberry pi 5v
# # Neo 6M GND -----> Raspberry pi GND
# # Neo 6M  RX -----> Raspberry pi TX (gpio 14) //Not required in our case
# # Neo 6M  TX -----> Raspberry pi RX (gpio 15)


# global Longitude_target, latitude_values
# connect with serial ESP
# ser_control = serial.Serial('/dev/ttyACM1', 115200, timeout=5)   
# # // Send char start to ESP
# ser_control.write(b'$')                                         
# # // connect with serial GPS 
# ser_gps = serial.Serial('/dev/ttyACM0', 115200, timeout=5)  
# # // Send char start to GPS
# ser_gps.write(b'$')                                         

# #---------------------------connect to  MQTT---------------------------------

## /*MQTT Broker Connection Details*/
mqtt_broker = "ae501b5ee3194ca682bd67e257459478.s1.eu.hivemq.cloud"
mqtt_username = "RainWay System"
mqtt_password = "012301230123aA#"
mqtt_port = 8883
mqtt_topic_1 = "esp8266/Location_data"

def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)
    # subscribe 1 topic 
    global status_connect
    status_connect = rc
    client.subscribe(mqtt_topic_1)
# Callback function khi nhận được tin nhắn từ MQTT Broker
def on_message(client, userdata, message):
    print("Received message '" 
        + str(message.payload.decode("utf-8")) 
        + "' on topic '"+ message.topic 
        + "' with QoS " + str(message.qos))
    data = str(message.payload.decode("utf-8"))
    
    #------------------------------ Update data when receive data from cloud -------------------------------------

# client_id is the given name of the client 
client = paho.Client(paho.CallbackAPIVersion.VERSION2)
# connect to MQTT
client.on_connect = on_connect

# enable TLS for secure connection
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
# set username and password
client.username_pw_set(mqtt_username,mqtt_password)
# connect to HiveMQ Cloud on port 8883 (default for MQTT)
client.connect(mqtt_broker,mqtt_port)
# setting callbacks, use separate functions like above for better visibility
client.on_message = on_message

client.loop_start()
# #--------------------------------------------------------------  Main  -------------------------------------

class RootApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Train System")
        self.geometry("1280x720+150+20")
        self.resizable(False,False)
        self.configure(bg='gray')
        self.title("Điều khiển Tàu Hỏa")
        # Icon 
        # self.iconbitmap('./image/eye.ico')
        img = PhotoImage(file='image/eye.png')
        self.tk.call('wm', 'iconphoto', self._w, img)
        # BackGround:
        self.image = Image.open(r"image/control.png")
        self.img = ImageTk.PhotoImage(self.image)
        # image_path = "image/Bground.png"
        # self.img = PhotoImage(file=image_path)
        self.label_Bg=tk.Label(self,image=self.img)
        self.label_Bg.place(x=0,y=0)
        
        #------------------------- frame2 -------------------------------
        self.frame2 = Frame2(self)
        self.frame2.config(bg="white",width=1180,height=550)
        self.frame2.place(x=52,y=146)
        #------------------------- Time -------------------------------
        self.label_time = tk.Label(self, font=('arial', 12, 'bold'),fg="#4660ac"
                                   ,borderwidth=0,border=0,width=20,relief='groove',justify=CENTER)
        self.label_time.place(x=50,y=125)
        #--------------------------- Func -------------------------------
        self.update_time()
    def update_time(self):
        # Real time """datetime(year, month, day[, hour[, minute[, second[, microsecond[,tzinfo]]]]])\
        global current_time
        current_time = datetime.now().strftime('%Y-%m-%d  %H:%M:%S')
        self.label_time.config(text=current_time)
        self.label_time.after(1000,self.update_time)
#------------------------- Frame 2:  Show map -----------------------------------------------------------
        
class Frame2(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        #------------------- header location detail ---------------------------------------------------
        # Header latitude
        self.header2_1= Label(self,text="Kinh Độ",fg='white',bg="#4660ac",width=12,
                              borderwidth=0,border=1,justify=CENTER,font=("arial", 12, "bold"),relief='groove',pady=2)
        self.header2_1.place(x=0,y=160)
        # Header Longitude
        self.header2_2= Label(self,text="Vĩ Độ",fg='white',bg="#4660ac",width=12,
                              borderwidth=0,border=1,justify=CENTER,font=("arial", 12, "bold"),relief='groove',pady=2)
        self.header2_2.place(x=0,y=230)
        # Header speed
        self.header2_3= Label(self,text="Tốc độ",fg='white',bg="#4660ac",width=12,
                              borderwidth=0,border=1,justify=CENTER,font=("arial", 12, "bold"),relief='groove',pady=2)
        self.header2_3.place(x=0,y=300)
        # Header address
        self.header2_4= Label(self,text="Địa chỉ",fg='white',bg="#4660ac",width=15,
                              borderwidth=0,border=1,justify=CENTER,font=("arial", 12, "bold"),relief='groove',pady=2)
        self.header2_4.place(x=1032,y=160)
        # Header distance: 
        self.header2_5= Label(self,text="Khoảng cách",fg='white',bg="#4660ac",width=15,
                              borderwidth=0,border=1,justify=CENTER,font=("arial", 12, "bold"),relief='groove',pady=2)
        self.header2_5.place(x=1032,y=260)

        #------------------- values location details ---------------------------------------------------

        # latitude values
        self.latitude= Label(self,text="Kinh Độ",fg='Gray',width=17,
                             borderwidth=0,border=1,justify=CENTER,font=("arial", 10, "bold"),relief='groove',pady=2)
        self.latitude.place(x=0,y=190)
        # Longitude values
        self.Longitude= Label(self,text="vĩ Độ",fg='Gray',width=17,
                              borderwidth=0,border=1,justify=CENTER,font=("arial", 10, "bold"),relief='groove',pady=2)
        self.Longitude.place(x=0,y=260)
        # speed values
        self.speed= Label(self,text="Tốc Độ",fg='Gray',width=17,
                          borderwidth=0,border=1,justify=CENTER,font=("arial", 10, "bold"),relief='groove',pady=2)
        self.speed.place(x=0,y=330)
         # address values
        self.Address= Label(self,text="Địa chỉ",fg='Gray',width=21,
                            borderwidth=0,border=1,justify=CENTER,font=("arial", 9, "bold"),relief='groove',pady=2)
        self.Address.place(x=1032,y=190)
         # Distance values
        self.Distance= Label(self,text="Khoảng cách",fg='Gray',width=21,
                             borderwidth=0,border=1,justify=CENTER,font=("arial", 9, "bold"),relief='groove',pady=2)
        self.Distance.place(x=1032,y=290)
        # # Distance values
        # self.button_clear=Button(self,text="Xóa mục tiêu",fg='white',bg='#4660ac',relief='groove',cursor='hand2',command=self.clear_target_on_map,
        #                 width=15,borderwidth=1,border=1,justify=CENTER,font=("Arial", 13, "bold"))
        # self.button_clear.place(x=1032,y=350)
        
        # ----------------------------------------------Button_Control-----------------------------------------------
        
        self.button_speed0=Button(self,text="stop",fg='white',bg='#777777',relief='groove',cursor='hand2',command=self.speed,
                        width=15,borderwidth=1,border=1,justify=CENTER,font=("Arial", 13, "bold"))
        self.button_speed0.place(x=500,y=500)
        self.button_speed2=Button(self,text="T",fg='white',bg='#9b9b9b',relief='groove',cursor='hand2',command=self.speed,
                        width=15,borderwidth=1,border=1,justify=CENTER,font=("Arial", 13, "bold"))
        self.button_speed2.place(x=500,y=400)
        self.button_speed3=Button(self,text="R",fg='white',bg='#bcbbbb',relief='groove',cursor='hand2',command=self.speed,
                        width=15,borderwidth=1,border=1,justify=CENTER,font=("Arial", 13, "bold"))
        self.button_speed3.place(x=600,y=450)
        self.button_speed3=Button(self,text="L",fg='white',bg='#c1bfbf',relief='groove',cursor='hand2',command=self.speed,
                        width=15,borderwidth=1,border=1,justify=CENTER,font=("Arial", 13, "bold"))
        self.button_speed3.place(x=400,y=450)

        #---------------------Map view-------------------------------------------------------

        self.map_widget = tkintermapview.TkinterMapView(self, width=750, height=400, corner_radius=0)
        self.map_widget.place(relx=0.5, rely=0.7, anchor=S)
        self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)  # google normal

        self.marker2=self.map_widget.set_position(20,106,text="Điểm mục tiêu",marker=True)

        # #----------------------Show location - Real time------------------------
        # self.map_widget.add_right_click_menu_command(label="Add Marker",
        #                                         command=self.add_marker_event,
        #                                         pass_coords=True)
        # self.update_location_map()
        # self.update_location_target()
        # self.update_realtime_frame2()
    def speed(self):
        # ser_control.write(b'$') 
        print("Helloooo {level}")
    # def clear_target_on_map(self):
        # self.map_widget.delete_all_marker()

    # def add_marker_event(self,coords):
    #     # self.marker2.set_text("Điểm mục tiêu")
    #     self.marker3=self.map_widget.set_marker(coords[0],coords[1],text="Điểm mục tiêu")
    #     # update distance values
    #     self.distance_2_point=hs.haversine((coords[0],coords[1]),(latitude_values,longitude_values),unit=Unit.KILOMETERS)
    #     self.Distance.config(text=self.distance_2_point)
    #     if self.distance_2_point <= 1.0:
    #         # self.marker2.hide_image(True)
    #         self.marker3.delete()
    #         # playsound('Audio/Audio_MucTieu.wav')
    #         # self.Distance.config(text="Hoàn thành")
            
    # def update_realtime_frame2(self):
    #     # def update_speed(self):
    #     global speed_id,Location
    #     self.speed.config(text=speed_id)
    #     # show địa chỉ dựa trên tọa độ.
    #     self.Address.config(text=Location)
    #     self.after(3000,self.update_realtime_frame2) 
if __name__ == "__main__":
    app = RootApplication()
    app.mainloop()