
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
import json





# ===========================================================connect to  MQTT======================================================

## /*MQTT Broker Connection Details*/
mqtt_broker = "ae501b5ee3194ca682bd67e257459478.s1.eu.hivemq.cloud"
mqtt_username = "RainWay System"
mqtt_password = "012301230123aA#"
mqtt_port = 8883
mqtt_topic_1 = "esp8266/Location_data"

#============================================================ CONFIG FOR GPS ======================================================
Real_time=""
Location=""
Latitude_values=0.0
Longitude_values=0.0
direction =""
Speed =0.0
#Using queue to getdata from thread gps 
data_queue = queue.Queue()

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
        self.client.subscribe(self.topic)
    # Callback function khi nhận được tin nhắn từ MQTT Broker
    def on_message(self,client, userdata, message):
        print("Received message '" 
            + str(message.payload.decode("utf-8")) 
            + "' on topic '"+ message.topic 
            + "' with QoS " + str(message.qos))
        global data_queue
        data_queue.put(str(message.payload.decode("utf-8")))
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
    # Publish data to hivemq
    # def send_data_to_hivemq(self,time, speed, latitude, longitude, direction):
    # # Tạo một dictionary chứa thông số cần gửi
    #     data = {
    #         "time": time,
    #         "speed": speed,
    #         "latitude": latitude,
    #         "longitude": longitude,
    #         "direction": direction
    #     }
    #     # Chuyển đổi dictionary thành chuỗi JSON
    #     json_data = json.dumps(data)
    #     # Đẩy dữ liệu lên topic MQTT
    #     self.client.publish(self.topic, json_data)
    def start(self):
        self.client.loop_start()
    def close_hivemq(self):
        self.client.disconnect()

# ================================================================================================================================
def parse_gps(line):
    try:
        if line.startswith('$GPGGA') or line.startswith('$GPRMC') or line.startswith('$GPGSV'):  # Kiểm tra xem dòng dữ liệu là thông điệp GGA, RMC hoặc GSV không
            msg = pynmea2.parse(line)
            #print(msg)
            if isinstance(msg, pynmea2.types.talker.RMC) and msg.latitude !=0.0 and msg.longitude !=0.0:
                data_queue.put(msg)
                
    except pynmea2.ParseError as e:
        print(f"Parse error: {e}")   
    except KeyboardInterrupt:
        print("Dừng đọc dữ liệu GPS.")
        
def read_gps():
    serial_port = serial.Serial('/dev/ttyS0', 9600, timeout=5)  # Mở cổng serial
    # Gửi lệnh cấu hình tần số cập nhật của GPS module thành 5 giây (0.2 Hz)
    ubx_command = b"\xB5\x62\x06\x08\x06\x00\xB8\x0B\x01\x00\x01\x00\xD9\x41"
    serial_port.write(ubx_command)
    while True:
        try:
            line = serial_port.readline().decode('unicode_escape')  # Đọc dòng dữ liệu từ cổng serial
            parse_gps(line)  # Gọi hàm parse dữ liệu GPS
        except Exception as e:
            print("Exception in read_gps:", e)
            
        
class RootApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Train System")
        self.geometry("1280x720")
        self.resizable(False,False)
        self.configure(bg='gray')
        self.title("Điều khiển Tàu Hỏa")
        # Icon 
        # self.iconbitmap('./image/eye.ico')
        img = PhotoImage(file='image/eye.png')
        self.tk.call('wm', 'iconphoto', self._w, img)
        # BackGround:
        self.image = Image.open(r"image/Bground.png")
        self.img = ImageTk.PhotoImage(self.image)
        # image_path = "image/Bground.png"
        # self.img = PhotoImage(file=image_path)
        self.label_Bg=tk.Label(self,image=self.img)
        self.label_Bg.place(x=0,y=0)
        #------------------------- frame_show map in app -------------------------------
        self.frame2 = Frame2(self)
        self.frame2.config(bg="white",width=1180,height=600)
        self.frame2.place(x=50,y=93)

#========================================================= Frame 2:  Show map ==========================================================
        
class Frame2(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        # data gps 
        self.data_queue = data_queue
        self.marker1 =None
        #----------------------------------------------- header location detail -------------------------------------------------
        
        # Header timestamp
        self.header2_0 = Label(self,text="Thời gian",fg='white',bg="#4660ac",width=15,
                              borderwidth=0,border=1,justify=CENTER,font=("arial", 12, "bold"),relief='groove',pady=2)
        self.header2_0.place(x=0,y=140)
        # Header latitude
        self.header2_1= Label(self,text="Kinh Độ",fg='white',bg="#4660ac",width=15,
                              borderwidth=0,border=1,justify=CENTER,font=("arial", 12, "bold"),relief='groove',pady=2)
        self.header2_1.place(x=0,y=210)
        # Header Longitude
        self.header2_2= Label(self,text="Vĩ Độ",fg='white',bg="#4660ac",width=15,
                              borderwidth=0,border=1,justify=CENTER,font=("arial", 12, "bold"),relief='groove',pady=2)
        self.header2_2.place(x=0,y=280)
        # Header speed
        self.header2_3= Label(self,text="Tốc độ",fg='white',bg="#4660ac",width=15,
                              borderwidth=0,border=1,justify=CENTER,font=("arial", 12, "bold"),relief='groove',pady=2)
        self.header2_3.place(x=0,y=350)
        # Header address
        self.header2_4= Label(self,text="Địa chỉ",fg='white',bg="#4660ac",width=15,
                              borderwidth=0,border=1,justify=CENTER,font=("arial", 12, "bold"),relief='groove',pady=2)
        self.header2_4.place(x=1040,y=140)
        # Header distance: 
        self.header2_5= Label(self,text="Khoảng cách",fg='white',bg="#4660ac",width=15,
                              borderwidth=0,border=1,justify=CENTER,font=("arial", 12, "bold"),relief='groove',pady=2)
        self.header2_5.place(x=1040,y=240)
        #Header heading:
        self.header2_6= Label(self,text="Hướng tàu",fg='white',bg="#4660ac",width=15,
                              borderwidth=0,border=1,justify=CENTER,font=("arial", 12, "bold"),relief='groove',pady=2)
        self.header2_6.place(x=1040,y=310)

        #--------------------------------------------------- values  details ---------------------------------------------------
        
        # TIME_VALUES
        self.Time= Label(self,text="Thời gian",fg='Gray',width=19,
                             borderwidth=0,border=1,justify=CENTER,font=("arial", 10, "bold"),relief='groove',pady=2)
        self.Time.place(x=0,y=170)
        # latitude values
        self.latitude= Label(self,text="Kinh Độ",fg='Gray',width=19,
                             borderwidth=0,border=1,justify=CENTER,font=("arial", 10, "bold"),relief='groove',pady=2)
        self.latitude.place(x=0,y=240)
        # Longitude values
        self.Longitude= Label(self,text="vĩ Độ",fg='Gray',width=19,
                              borderwidth=0,border=1,justify=CENTER,font=("arial", 10, "bold"),relief='groove',pady=2)
        self.Longitude.place(x=0,y=310)
        # speed values
        self.Speed = Label(self,text="Tốc Độ",fg='Gray',width=19,
                          borderwidth=0,border=1,justify=CENTER,font=("arial", 10, "bold"),relief='groove',pady=2)
        self.Speed.place(x=0,y=380)
         # address values
        self.Address= Label(self,text="Địa chỉ",fg='Gray',width=19,
                            borderwidth=0,border=1,justify=CENTER,font=("arial", 9, "bold"),relief='groove',pady=2)
        self.Address.place(x=1040,y=170)
         # Distance values
        self.Distance= Label(self,text="Khoảng cách",fg='Gray',width=19,
                             borderwidth=0,border=1,justify=CENTER,font=("arial", 9, "bold"),relief='groove',pady=2)
        self.Distance.place(x=1040,y=270)
        # heading values
        self.Heading= Label(self,text="Hướng tàu",fg='Gray',width=19,
                              borderwidth=0,border=1,justify=CENTER,font=("arial", 10, "bold"),relief='groove',pady=2)
        self.Heading.place(x=1040,y=340)
        #---------------------Map view-------------------------------------------------------

        self.map_widget = tkintermapview.TkinterMapView(self, width=880, height=600, corner_radius=0)
        self.map_widget.place(relx=0.5, rely=0.5, anchor='center')
        self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)  # google normal
        self.update_time()
        self.update_realtime_frame2()
    def update_realtime_frame2(self):
        while not self.data_queue.empty():
            # def update_speed(self):
            self.data = self.data_queue.get()
            global Latitude_values,Longitude_values,Speed,direction,Location,Real_time
            direction = mqtt_client.get_direction(self.data.true_course) if self.data.true_course is not None else "Unknown"
            Speed = self.data.spd_over_grnd
            adr = tkintermapview.convert_coordinates_to_address(self.data.latitude,self.data.longitude)
            Location = str(adr.street)+"\n"+str(adr.city) +"\n"+str(adr.country)
            Latitude_values = self.data.latitude
            Longitude_values= self.data.longitude
            self.Speed.config(text=Speed)
            self.latitude.config(text= Latitude_values)
            self.Longitude.config(text = Longitude_values )
            self.Heading.config(text = direction)
            self.Address.config(text=Location)
            print(Speed,Latitude_values,Longitude_values)
            #push data to hivemq
            mqtt_client.send_data_to_hivemq(str(Real_time), str(Speed), str(Latitude_values), str(Longitude_values), self.data.true_course)
            # Xóa marker cũ nếu tồn tại
            if self.marker1 is not None:
                self.marker1.delete()
            # Hiển thị marker mới
            self.marker1 = self.map_widget.set_position(self.data.latitude, self.data.longitude, text="Điểm mục tiêu", marker=True)
        self.after(500,self.update_realtime_frame2)
    def update_time(self):
        global Real_time
        Real_time = datetime.now().strftime('%H:%M:%S')
        self.Time.config(text= Real_time)
        self.after(1000,self.update_time)
        
if __name__ == "__main__":
    try:
            mqtt_client = MQTTClient(mqtt_broker, mqtt_port, mqtt_username, mqtt_password, mqtt_topic_1)
            mqtt_client.start()
            gps_thread =threading.Thread(target=read_gps)
            gps_thread.start()
            app = RootApplication()
            app.mainloop()
    except KeyboardInterrupt:
            print("Dừng đọc dữ liệu GPS.")
            mqtt_client.close_hivemq()
            gps_thread.join()
            app.destroy()
    
    

