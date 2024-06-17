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
import queue
import pygame
import threading


#---------------- initializing the variables    -----------------------
#Using queue to getdata from thread gps 
data_queue = queue.Queue()
# Realtime data latitude - longitude from cloud
latitude_values=0.0
longitude_values=0.0
speed_values=0.0
# Train status  
train_status="An Toàn"
#Location after transfer Latitude - Longitude to Addresss
Location=""
# Location target
Latitude_target=0.0
Longitude_target=0.0
Location_click=""
# target_id 
target_id=1
# Real time 
current_time=""
# values get to table
data=""
speed_id=""
# Train status  
train_status="An Toàn"
# Turn ON / OFF notification 
turn_values=0
#Các điểm mục tiêu 
# Location_array=[] 
#---------------------------connect to  MQTT---------------------------------

# /*MQTT Broker Connection Details*/
mqtt_broker = "ae501b5ee3194ca682bd67e257459478.s1.eu.hivemq.cloud"
mqtt_username = "RainWay System"
mqtt_password = "012301230123aA#"
mqtt_port = 8883
mqtt_topic_1 = "esp8266/Location_data"


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
        self.client.subscribe(mqtt_topic_1)
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
    def send_data_to_hivemq(self,mqtt_topic,json_data):
        self.client.publish(mqtt_topic,json_data)
    def start(self):
        self.client.loop_start()
    def close_hivemq(self):
        self.client.disconnect()
#------------------------------ Update data when receive data from cloud -------------------------------------
# receive data from esp -> notification Distance between Sation and Train :
# Ha Noi Station (Id: 1), Hai Duong Staion(Id: 2), Hai Phong Station (Id :3 ) 
# distance Train - Station
# ======================== Play sound ============================================
def playsound(file_path):
    try:
        # Khởi tạo Pygame
        pygame.init()

        # Tạo một mixer
        pygame.mixer.init()

        # Load file âm thanh
        sound = pygame.mixer.Sound(file_path)

        # Phát lại âm thanh
        sound.play()

        # Đợi cho âm thanh kết thúc
        while pygame.mixer.get_busy():
            pygame.time.Clock().tick(10)
        # Đóng Pygame
       
        pygame.mixer.quit()
        pygame.quit()
    except Exception as e:
        print("Error:", e)
        
def playAudio():
    global latitude_values,longitude_values,turn_values
    # while latitude_values!= 0.0 and longitude_values != 0.0:
    while True:
        if turn_values == 1:
            if hs.haversine((latitude_values,longitude_values),(21.02439,105.84122),unit=Unit.KILOMETERS) <=1 :
                # Load file âm thanh
                playsound('Audio/Audio_HaNoi.wav')
                time.sleep(0.1)
                
            if hs.haversine((latitude_values,longitude_values),(20.94663,106.33057),unit=Unit.KILOMETERS) <=1 :
                # Load file âm thanh
                playsound( 'Audio/Audio_HaiDuong.wav')
                time.sleep(0.1)
            if hs.haversine((latitude_values,longitude_values),(20.85596,106.68736),unit=Unit.KILOMETERS) <=1 :
                # Load file âm thanh
                playsound('Audio/Audio_HaiPhong.wav')
                time.sleep(0.1)
        else:
            pass
    
#--------------------------------------------------------------  Main  -------------------------------------

class RootApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Train System")
        self.geometry("1280x720+150+20")
        self.resizable(False,False)
        self.configure(bg='gray')
        self.title("Hệ Thống Tàu Hỏa")
        # Icon 
        img = PhotoImage(file='image/eye.png')
        self.tk.call('wm', 'iconphoto', self._w, img)
        # BackGround:
        self.image = Image.open(r"image/Bground-min.png")
        self.img = ImageTk.PhotoImage(self.image)
        self.label_Bg=tk.Label(self,image=self.img)
        self.label_Bg.place(x=0,y=0)
        # Create frame - button frame : 3 frame 
        #------------------------- frame2 -------------------------------
        self.frame2 = Frame2(self)
        self.frame2.config(bg="white",width=1180,height=550)
        self.frame2.place(x=52,y=146)
        self.button_frame1=Button(self,text="Theo dõi xe",font=('Arial', 13, 'bold'),bg="white",fg="#4660ac",activebackground="white",cursor='hand2',
                                  borderwidth=0,border=0,width=15,relief='groove',justify=CENTER,command=lambda: self.frame2.tkraise())
        self.button_frame1.place(x=881,y=100)
        #------------------------- frame3 -------------------------------
        self.frame3 = Frame3(self)
        self.frame3.config(bg="white",width=1180,height=550)
        self.frame3.place(x=52,y=146)
        self.button_frame1=Button(self,text="Trang dữ liệu",font=('Arial', 13, 'bold'),bg="white",fg="#4660ac",activebackground="white",cursor='hand2',
                                  borderwidth=0,border=0,width=15,relief='groove',justify=CENTER,command=lambda: self.frame3.tkraise())
        self.button_frame1.place(x=1081,y=100)
        #------------------------- Frame1 -------------------------------
        self.frame1 = Frame1(self)
        self.frame1.config(bg="white",width=1180,height=550)
        self.frame1.place(x=52,y=146)
        self.button_frame1=Button(self,text="Trang thông tin",font=('Arial', 13, 'bold'),bg="white",fg="#4660ac",activebackground="white",cursor='hand2',
                                  borderwidth=0,border=0,width=15,relief='groove',justify=CENTER,command=lambda: self.frame1.tkraise())
        self.button_frame1.place(x=680,y=100)
        self.label_time = tk.Label(self, font=('Arial', 15, 'bold'),bg="white",fg="#4660ac"
                                   ,borderwidth=0,border=0,width=18,relief='groove',justify=CENTER)
        self.label_time.place(x=54,y=102)
        #--------------------------- Func -------------------------------
        self.update_time()
    def update_time(self):
        # Real time """datetime(year, month, day[, hour[, minute[, second[, microsecond[,tzinfo]]]]])\
        global current_time
        current_time = datetime.now().strftime('%Y-%m-%d  %H:%M:%S')
        self.label_time.config(text=current_time)
        self.label_time.after(1000,self.update_time)
        
#------------------------------------------- Frame 1: Trang điều khiển xe ---------------------------------------------------
        
class Frame1(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        #-------------------------------- Train status --------------------------------------------------------------------------------

        self.label_status=Label(self,text="Trạng thái Tàu",fg='white',bg='#f22f2f',relief='groove',
                        width=20,borderwidth=1,border=1,justify=CENTER,font=("Arial", 15, "bold"),pady=5)
        self.label_status.place(x=29,y=160)
        self.label_Noti=Label(self,text="Trạng thái..",fg='white',bg='#777777',relief='groove',pady=4,
                        width=17,borderwidth=1,border=1,justify=CENTER,font=("Arial", 13, "bold"))
        self.label_Noti.place(x=62,y=215)
        #--------------------------------------------------- Direction --------------------------------------------------------------------------------

        self.label_direction=Label(self,text="Hương di chuyển",fg='white',bg='#f22f2f',relief='groove',
                        width=20,borderwidth=1,border=1,justify=CENTER,font=("Arial", 15, "bold"),pady=5)
        self.label_direction.place(x=29,y=270)
        self.label_show=Label(self,text="hướng",fg='white',bg='#777777',relief='groove',pady=4,
                        width=17,borderwidth=1,border=1,justify=CENTER,font=("Arial", 12, "bold"))
        self.label_show.place(x=62,y=325)
        # #------------------------------------ show Location - Speed ---------------------------------------------------------------------------------
         
        # Header label
        self.header1= Label(self,text="Địa chỉ hiện tại",fg='white',bg="#4660ac",width=30,borderwidth=0,border=1,justify=CENTER,
                       font=("Arial", 15, "bold"),relief='groove',pady=5)
        self.header1.place(x=400,y=110)
        self.header1.config(justify='center')
        # lable Location
        self.local1= Label(self,text="Location",fg="#4660ac",width=30,borderwidth=1,border=1,justify=CENTER,font=("Arial", 15, "bold"),pady=5)
        self.local1.place(x=400,y=165)
        #header speed
        self.header2= Label(self,text="Tốc độ hiện tại",fg='white',bg="#4660ac",width=30,borderwidth=0,border=1,justify=CENTER,
                       font=("Arial", 15, "bold"),relief='groove',pady=5)
        self.header2.place(x=400,y=270)
        # lable Speed
        self.speed1= Label(self,text="speed",fg="#4660ac",width=30,borderwidth=1,border=1,justify=CENTER,font=("Arial", 15, "bold"),pady=5)
        self.speed1.place(x=400,y=325)
         #--------------------------------------------------- Target train --------------------------------------------------------------------------
        self.Label_target=Label(self,text="Mục tiêu di chuyển",fg='white',bg="#4660ac",width=30,borderwidth=0,border=1,justify=CENTER,
                       font=("Arial", 15, "bold"),pady=5)
        self.Label_target.place(x=400,y=380)
        self.Entry_Lat_Long_Target=Entry(self,fg="#4660ac",bg="#EDEBEB",relief='flat',width=19,borderwidth=1,border=1,justify=CENTER,font=("Arial", 15, "bold"))
        self.Entry_Lat_Long_Target.place(x=550,y=435)        
        self.Label_target=Label(self,text="Kinh độ/ Vĩ độ",fg='white',bg="#4660ac",width=12,borderwidth=0,border=0,justify=CENTER,
                       font=("Arial", 15, "bold"))
        self.Label_target.place(x=400,y=435)
        # --------------- Control Speed -----------------------
    
        self.header_speed=Label(self,text="Cảnh báo tốc độ",fg='white',bg='#f22f2f',relief='groove',
                        width=20,borderwidth=1,border=1,justify=CENTER,font=("Arial", 15, "bold"),pady=5)
        self.header_speed.place(x=900,y=160)
        self.header_speed_noti = Label(self,text="Cảnh báo",fg='white',bg='#777777',relief='groove',pady=4,
                        width=17,borderwidth=1,border=1,justify=CENTER,font=("Arial", 12, "bold"))
        self.header_speed_noti.place(x=933,y=215)
        # -------------------------------------------------- TURN ON /OFF notification -------------------------------------------------------------------
        # Change Turn values:
        self.turn_values_tk = tk.IntVar()
        self.turn_values_tk.set(1)
        self.check_turn =tk.Checkbutton(self,text = "Âm thanh thông báo", variable = self.turn_values_tk,font=("Arial", 15, "bold"),
                                        fg="black",bg="#f22f2f",cursor='hand2',width=18,justify=CENTER) 
        self.check_turn.place(x=900,y=270)
        self.update_frame1_realtime()
        self.update_label_location_target()

    def update_label_location_target(self):
        global Latitude_target,Longitude_target,target_id,turn_values
        turn_values =self.turn_values_tk.get()
        if target_id==0:
            self.Entry_Lat_Long_Target.delete(0,'end')
            # self.Entry_Longitude_Target.delete(0,'end')
            Latitude_target=""
            Longitude_target=""
            target_id=1
        data_target = self.Entry_Lat_Long_Target.get() 
        if data_target !="" and data_target is not None:
            # data_target = self.Entry_Latitude_Target.get() 
            parts = data_target.split()
            try:  # Kiểm tra xem danh sách có phần tử nào không trước khi truy cập
                Latitude_target=parts[0]
                Longitude_target=parts[1]
            except: 
                pass
        self.after(1000,self.update_label_location_target)

    def update_frame1_realtime(self):
        global data_queue,latitude_values,longitude_values,train_status,speed_values,direction,Location
        while not data_queue.empty():
            self.data = data_queue.get()
            speed_values = self.data['speed']
            longitude_values =self.data['longitude']
            latitude_values  =self.data['latitude']
            direction = mqtt_client.get_direction(self.data['true_course']) if self.data['true_course'] is not None else "Unknown"
            if float(speed_values) is not None:
                train_status ="An Toàn"
                if float(speed_values)>=60:
                    self.header_speed_noti.config(text="Vượt quá tốc độ")
                else:
                    self.header_speed_noti.config(text="An Toàn")
            # Update status 
            self.label_Noti.config(text=train_status)
            # update_label_location
            adr = tkintermapview.convert_coordinates_to_address(self.data.latitude,self.data.longitude)
            Location = str(adr.street)+"\n"+str(adr.city) +"\n"+str(adr.country)
            self.local1.config(text=Location)
            # update_label_direction 
            self.label_show.config(text=direction)
            # update_speed()
            self.speed1.config(text=speed_values)
        self.after(500,self.update_frame1_realtime)

#------------------------- Frame 2:  Show map -----------------------------------------------------------
        
class Frame2(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.marker1 =None
        #------------------- header location detail ---------------------------------------------------
        # Header latitude
        self.header2_1= Label(self,text="Kinh Độ",fg='white',bg="#4660ac",width=12,borderwidth=0,border=1,justify=CENTER,font=("Arial", 12, "bold"),relief='groove',pady=2)
        self.header2_1.place(x=0,y=180)
        # Header Longitude
        self.header2_2= Label(self,text="Vĩ Độ",fg='white',bg="#4660ac",width=12,borderwidth=0,border=1,justify=CENTER,font=("Arial", 12, "bold"),relief='groove',pady=2)
        self.header2_2.place(x=0,y=250)
        # Header speed
        self.header2_3= Label(self,text="Tốc độ",fg='white',bg="#4660ac",width=12,borderwidth=0,border=1,justify=CENTER,font=("Arial", 12, "bold"),relief='groove',pady=2)
        self.header2_3.place(x=0,y=320)
        # Header address
        self.header2_4= Label(self,text="Địa chỉ",fg='white',bg="#4660ac",width=15,borderwidth=0,border=1,justify=CENTER,font=("Arial", 12, "bold"),relief='groove',pady=2)
        self.header2_4.place(x=1032,y=180)
        # Header distance: 
        self.header2_5= Label(self,text="Khoảng cách",fg='white',bg="#4660ac",width=15,borderwidth=0,border=1,justify=CENTER,font=("Arial", 12, "bold"),relief='groove',pady=2)
        self.header2_5.place(x=1032,y=280)
        # Header direction 
        self.header2_6  =Label(self,text="Khoảng cách",fg='white',bg="#4660ac",width=15,borderwidth=0,border=1,justify=CENTER,font=("Arial", 12, "bold"),relief='groove',pady=2)
        self.header2_6.place(x=1032,y=350)
        #------------------- values location details ---------------------------------------------------
        # latitude values
        self.latitude= Label(self,text="Kinh Độ",fg='Gray',width=15,borderwidth=0,border=1,justify=CENTER,font=("Arial", 10, "bold"),relief='groove',pady=2)
        self.latitude.place(x=0,y=210)
        # Longitude values
        self.Longitude= Label(self,text="vĩ Độ",fg='Gray',width=15,borderwidth=0,border=1,justify=CENTER,font=("Arial", 10, "bold"),relief='groove',pady=2)
        self.Longitude.place(x=0,y=280)
        # speed values
        self.speed= Label(self,text="Tốc Độ",fg='Gray',width=15,borderwidth=0,border=1,justify=CENTER,font=("Arial", 10, "bold"),relief='groove',pady=2)
        self.speed.place(x=0,y=350)
         # address values
        self.Address= Label(self,text="Địa chỉ",fg='Gray',width=21,borderwidth=0,border=1,justify=CENTER,font=("Arial", 9, "bold"),relief='groove',pady=2)
        self.Address.place(x=1032,y=210)
         # Distance values
        self.Distance= Label(self,text="Khoảng cách",fg='Gray',width=21,borderwidth=0,border=1,justify=CENTER,font=("Arial", 9, "bold"),relief='groove',pady=2)
        self.Distance.place(x=1032,y=310)
        # direction values
        self.Direction= Label(self,text="Hướng đi",fg='Gray',width=21,borderwidth=0,border=1,justify=CENTER,font=("Arial", 9, "bold"),relief='groove',pady=2)
        self.Direction.place(x=1032,y=380)
        #---------------------Map view-------------------------------------------------------

        self.map_widget = tkintermapview.TkinterMapView(self, width=900, height=550, corner_radius=0)
        self.map_widget.place(relx=0.49, rely=0.5, anchor=CENTER)
        self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)  # google normal
        #----------------------Show location - Real time------------------------
        self.map_widget.add_right_click_menu_command(label="xóa mục tiêu",command=self.clear_marker_event,
                                                pass_coords=True)
        self.update_location_map()
        self.update_location_target()

    # update location in map
    def update_location_map(self):
        global data_queue,latitude_values,longitude_values,train_status,speed_values,direction,Location
        while latitude_values and longitude_values and speed_values and direction and Location is not None:
            self.Address.config(text=Location)
            # update_label_direction 
            self.Direction.config(text=direction)
            # update_speed()
            self.speed.config(text=speed_values)
            self.latitude.config(text=latitude_values)
            self.Longitude.config(text=longitude_values)
            if self.marker1 is not None:
                self.marker1.delete()
            self.marker1= self.map_widget.set_position(latitude_values, longitude_values,text="Vị trí tàu",marker=True)
        # Update the position on the map
        self.after(1000,self.update_location_map)
    def update_location_target(self):
        global latitude_values,longitude_values,target_id,Latitude_target,Longitude_target,turn_values
        # print(Latitude_target,Longitude_target)
        # address = tkintermapview.convert_address_to_coordinates(Location_target)
        if Latitude_target and Longitude_target is not None:
            try:
                # if Latitude_target and Longitude_target is not None:  # Kiểm tra xem chuỗi có giá trị không
                #     try:
                print(Latitude_target,Longitude_target)
                Latitude_target_f = float(Latitude_target)
                Longitude_target_f = float(Longitude_target)
                # self.marker2.set_text("Điểm mục tiêu")
                self.marker2=self.map_widget.set_position(Latitude_target_f,Longitude_target_f,text="Điểm mục tiêu",marker=True)
                # update distance values
                self.distance_2_point=hs.haversine((Latitude_target_f,Longitude_target_f),(latitude_values,longitude_values),unit=Unit.KILOMETERS)
                self.Distance.config(text=self.distance_2_point)
                # Load file âm thanh
                if self.distance_2_point <= 1.0 :
                    # self.marker2.delete()
                    self.marker2.delete()
                    # self.map_widget.delete_all_path()
                    if turn_values == 1:
                        playsound('Audio/Audio_MucTieu.wav')
                    target_id=0
                    self.Distance.config(text="Hoàn thành")
            except:
                print("Wait")
        else:
            target_id=1
            self.Distance.config(text="")
        self.after(2000,self.update_location_target)
    # def clear_path(self):
    #     self.map_widget.delete_all_path()
    def clear_marker_event(self,event=None):
        global target_id 
        try:
            target_id=0
            self.map_widget.delete_all_marker()
            self.Distance.config(text="")
        except Exception as e:
            print(f"An error occurred: {e}")
        
#----------------------------------------------------- Frame 3: Data Receive ---------------------------------------------------------------------
        
class Frame3(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        # Tạo Treeview
        self.tree = ttk.Treeview(self, columns=("Time", "Latitude", "Longtitud","Speed","Location","Status"), show="headings")
        self.tree.place(width=1000,height=500,x=0,y=20)
        self.tree.heading("Speed", text="Speed")
        self.tree.heading("Latitude", text="Latitude")
        self.tree.heading("Longtitud", text="Longtitud")
        self.tree.heading("Location", text="Location")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Time", text="Time")
        # Thiết lập chiều rộng cột
        self.tree.column("Latitude",anchor="center", width=50)
        self.tree.column("Longtitud", anchor="center",width=50)
        self.tree.column("Speed",anchor="center", width=30)
        self.tree.column("Location", anchor="center",width=250)
        self.tree.column("Status", anchor="center",width=50)
        self.tree.column("Time", anchor="center",width=65)
        # Tạo scrollbar cho treeview
        self.scrollbar1 = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.scrollbar2 = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=self.scrollbar1.set,xscrollcommand=self.scrollbar2.set)
        self.scrollbar1.place(height=500,x=1000,y=20)
        self.scrollbar2.place(width=1000,x=0,y=520)
        #------------------------- get data to xlsx file ------------------------------------------
        self.button_save = tk.Button(self,text="xuất dữ liệu",padx=8,pady=3,background="#4660ac",fg="white",font=("Arial", 15, "bold")
                                     ,border=0,borderwidth=0,justify=CENTER,cursor='hand2',command=self.get_data)
        self.button_save.place(x=1030,y=250)
        # self.update_data(current_time, Location,latitude_values,longitude_values)  # Cập nhật thời gian mỗi giây
        self.update_data()
    # update data to table:
    def update_data(self):
        # Dữ liệu mẫu
        global current_time,Location,latitude_values,longitude_values,train_status,speed_values
        # Loại bỏ ký tự xuống dòng (\n)
        Location_no_newline = Location.replace("\n", "")
        if latitude_values and longitude_values is not None:
            data = [str(current_time), str(latitude_values), str(longitude_values),str(speed_values),Location_no_newline,train_status]
            self.tree.insert("", "end", values=data)
        self.after(1000,self.update_data)      
    def get_data(self):
        # Tạo một workbook mới
        self.wb = Workbook()
        # Chọn active worksheet (sheet mặc định)
        self.ws = self.wb.active
        # Ghi dữ liệu vào worksheet
        self.ws.append(["Time", "Latitude", "Longtitude","Speed","Location","Status"])
        for item in self.tree.get_children():
            self.values = self.tree.item(item, 'values')
            self.ws.append(self.values)
        self.clear_data_received()
        # Hiển thị hộp thoại để chọn vị trí lưu tệp
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            # Lưu workbook thành file Excel tại đường dẫn đã chọn
            try:
                self.wb.save(file_path)
                messagebox.showinfo("Thông báo", "Dữ liệu đã được lưu vào file Excel thành công!")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Có lỗi xảy ra khi lưu file: {e}")
    def clear_data_received(self):
        for item in self.tree.get_children(): # used self.tree instead
            self.tree.delete(item)
            
if __name__ == "__main__":
    try:
        sound_thread =threading.Thread(target=playAudio)
        # Khởi tạo và bắt đầu luồng
        sound_thread.start()
        mqtt_client = MQTTClient(mqtt_broker, mqtt_port, mqtt_username, mqtt_password, mqtt_topic_1)
        mqtt_client.start()
        app = RootApplication()
        app.mainloop()
    except KeyboardInterrupt:
        mqtt_client.close_hivemq()
        sound_thread.join()
        app.destroy()
        
        
        