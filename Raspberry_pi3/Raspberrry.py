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
import gps
# from gps import gps, WATCH_ENABLE




# ===========================================================connect to  MQTT======================================================

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
    
# #------------------------------------------------------ Update data when receive data from cloud ------------------------------------------


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

#=============================================================================================================================


#======================================================= Đọc Tín hiệu GPS ====================================================

# #----------------------------config GPS------------------------
 
# # Neo 6M VCC -----> Raspberry pi 5v
# # Neo 6M GND -----> Raspberry pi GND
# # Neo 6M  RX -----> Raspberry pi TX (gpio 14) //Not required in our case
# # Neo 6M  TX -----> Raspberry pi RX (gpio 15)

# # // connect with serial GPS 
ser = serial.Serial('/dev/serial0', 9600, timeout=1)    
latitude_values = None
longitude_values = None
speed_values =None
heading =None
Location =""

report = {
                        'class':'TPV',
                        'lat': 20.0,
                        'lon': 106.0,
                        'speed':20,
                        'track':'huong tay'
}
# #--------------------------------------------------------------  Main  -------------------------------------
# latitude_values = self.report.lat
latitude_values = report['lat']
# Lấy thông tin vĩ độ
# longitude_values = self.report.lon
longitude_values = report['lon']
# Lấy thông tin tốc độ
speed = getattr(report, 'speed', None)
# Lấy thông tin hướng
heading = getattr(report, 'track', None)

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
        
        #------------------------- frame_show map in app -------------------------------
        self.frame2 = Frame2(self)
        self.frame2.config(bg="white",width=1180,height=550)
        self.frame2.place(x=52,y=146)
        #------------------------- Time -------------------------------
        self.label_time = tk.Label(self, font=('arial', 12, 'bold'),fg="#4660ac"
                                   ,borderwidth=0,border=0,width=20,relief='groove',justify=CENTER)
        self.label_time.place(x=50,y=125)
        #--------------------------- Func -------------------------------
        self.update_time()
        self.update_data_gps()
    def update_time(self):
        # Real time """datetime(year, month, day[, hour[, minute[, second[, microsecond[,tzinfo]]]]])\
        global current_time
        current_time = datetime.now().strftime('%Y-%m-%d  %H:%M:%S')
        self.label_time.config(text=current_time)
        self.label_time.after(1000,self.update_time)
    def update_data_gps(self):
        # self.report = session.next()
        print("Đang lấy thông tin GPS...")
        global latitude_values,longitude_values,speed,heading,Location
        try:
            # Đọc dữ liệu từ cổng serial UART
            data = ser.readline().decode('utf-8', errors='ignore')
            
            # Kiểm tra xem dữ liệu có phải là chuỗi NMEA không
            if data.startswith('$GPGGA'):
                try:
                    # Phân tích chuỗi NMEA
                    msg = pynmea2.parse(data)
                    
                    # Trích xuất và in kinh độ, vĩ độ
                    latitude_values = msg.latitude
                    longitude_values = msg.longitude
                    adr = tkintermapview.convert_coordinates_to_address(latitude_values,longitude_values)
                    Location = str(adr.street)+"\n"+str(adr.city) +"\n"+str(adr.country)
                    self.frame2.update_realtime_frame2()
                    self.after(3000,self.update_data_gps)
                except pynmea2.ParseError as e:
                    print("Lỗi parsing:", e)
        except UnicodeDecodeError:
            print("Không giải mã được tin.")
        except KeyError:
            pass
        except KeyboardInterrupt:
            print("Đã dừng chương trình.")
        except StopIteration:
            print("GPSD đã dừng.")
        
#========================================================= Frame 2:  Show map ==========================================================
        
class Frame2(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        #----------------------------------------------- header location detail -------------------------------------------------
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
        #Header heading:
        self.header2_6= Label(self,text="Hướng tàu",fg='white',bg="#4660ac",width=15,
                              borderwidth=0,border=1,justify=CENTER,font=("arial", 12, "bold"),relief='groove',pady=2)
        self.header2_6.place(x=1032,y=360)

        #--------------------------------------------------- values  details ---------------------------------------------------

        # latitude values
        self.latitude= Label(self,text="Kinh Độ",fg='Gray',width=17,
                             borderwidth=0,border=1,justify=CENTER,font=("arial", 10, "bold"),relief='groove',pady=2)
        self.latitude.place(x=0,y=190)
        # Longitude values
        self.Longitude= Label(self,text="vĩ Độ",fg='Gray',width=17,
                              borderwidth=0,border=1,justify=CENTER,font=("arial", 10, "bold"),relief='groove',pady=2)
        self.Longitude.place(x=0,y=260)
        # speed values
        self.Speed = Label(self,text="Tốc Độ",fg='Gray',width=17,
                          borderwidth=0,border=1,justify=CENTER,font=("arial", 10, "bold"),relief='groove',pady=2)
        self.Speed.place(x=0,y=330)
         # address values
        self.Address= Label(self,text="Địa chỉ",fg='Gray',width=21,
                            borderwidth=0,border=1,justify=CENTER,font=("arial", 9, "bold"),relief='groove',pady=2)
        self.Address.place(x=1032,y=190)
         # Distance values
        self.Distance= Label(self,text="Khoảng cách",fg='Gray',width=21,
                             borderwidth=0,border=1,justify=CENTER,font=("arial", 9, "bold"),relief='groove',pady=2)
        self.Distance.place(x=1032,y=290)
        # heading values
        self.Heading= Label(self,text="Hướng tàu",fg='Gray',width=17,
                              borderwidth=0,border=1,justify=CENTER,font=("arial", 10, "bold"),relief='groove',pady=2)
        self.Heading.place(x=1032,y=390)
        # # Distance values
        # self.button_clear=Button(self,text="Xóa mục tiêu",fg='white',bg='#4660ac',relief='groove',cursor='hand2',command=self.clear_target_on_map,
        #                 width=15,borderwidth=1,border=1,justify=CENTER,font=("Arial", 13, "bold"))
        # self.button_clear.place(x=1032,y=350)
        #---------------------Map view-------------------------------------------------------

        self.map_widget = tkintermapview.TkinterMapView(self, width=750, height=400, corner_radius=0)
        self.map_widget.place(relx=0.5, rely=0.7, anchor=S)
        self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)  # google normal
        # self.map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png") 

        # self.marker2=self.map_widget.set_position(20,106,text="Điểm mục tiêu",marker=True)

        # #----------------------Show location - Real time------------------------
        # self.map_widget.add_right_click_menu_command(label="Add Marker",
        #                                         command=self.add_marker_event,
        #                                         pass_coords=True)
        # self.update_location_map()
        # self.update_location_target()
        # self.update_realtime_frame2()
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
    def delete_marker1(self):
            self.marker1.delete()
    def update_realtime_frame2(self):
        # def update_speed(self):
        global speed, latitude_values, longitude_values, heading
        self.Speed.config(text=speed)
        self.latitude.config(text= latitude_values)
        self.Longitude.config(text =longitude_values)
        self.Heading.config(text = heading)
        self.Address.config(text=Location)
        # Update the position on the map
        self.marker1= self.map_widget.set_position(latitude_values, longitude_values,text="Điểm mục tiêu",marker=True)
        # self.marker1.(15)
        # self.marker1.set_text("Vị trí tàu")
        latitude_values+=0.1
        longitude_values+=0.1
        # self.after(2000,self.delete_marker1())
if __name__ == "__main__":
    app = RootApplication()
    app.mainloop()