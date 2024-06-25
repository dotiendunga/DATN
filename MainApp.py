import tkinter as tk
from tkinter import *
import tkintermapview 
from tkinter import ttk
from PIL import ImageTk, Image
from datetime import datetime
from tkinter import filedialog, messagebox
from openpyxl import Workbook
import time 
import queue
import threading
from MQTT_class import*
from Play_audio import playsound
import haversine as hs   
from haversine import Unit
import json 
import tkintermapview

#---------------- initializing the variables    -----------------------
#Using queue to getdata from thread gps 
data_queue = queue.Queue()
# Khai báo một mutex
mutex = threading.Lock()
queue_flag = False
# Realtime data latitude - longitude from cloud
latitude_values=0.0
longitude_values=0.0
speed_values=0.0
distance_2_point=0.0
direction = ""

flag_frame1 =False
flag_frame2 = False
flag_frame3 = False
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


#=========================================   connect to  MQTT   ===========================================

# /*MQTT Broker Connection Details*/
mqtt_broker = "ae501b5ee3194ca682bd67e257459478.s1.eu.hivemq.cloud"
mqtt_username = "RainWay System"
mqtt_password = "012301230123aA#"
mqtt_port = 8883
mqtt_topic_1 = "Train/Location_data"
        
class CustomMQTTClient(MQTTClient):
    def on_message(self, client, userdata, message):
        # Gọi phương thức on_message của lớp cha nếu muốn giữ lại phần xử lý cũ
        try:
            super().on_message(client, userdata, message)
            self.data = json.loads(str(message.payload.decode("utf-8")) )
            global speed_values,longitude_values, latitude_values,direction,Location,Latitude_target,Longitude_target,train_status
            speed_values = float(self.data["speed"])
            longitude_values = float(self.data["longitude"])
            latitude_values = float(self.data["latitude"])
            train_status = "An Toàn" if speed_values < 60 else "Vượt quá tốc độ"
            adr = tkintermapview.convert_coordinates_to_address(latitude_values,longitude_values)
            Location = str(adr.street)+"\n"+str(adr.city) +"\n"+str(adr.country)
            try:
                direction = self.get_direction(float(self.data["direction"]))
            except:
                direction = "Unknown"
                # print("Unknown")
            # Flag
            global flag_frame1,flag_frame2,flag_frame3
            flag_frame1 =True
            flag_frame2 =True
            flag_frame3 =True   
        except Exception as e:
            print(f"An error occurred: {e}")
        # Thêm phần xử lý mới
        print("Custom on_message processing")
        # # Ví dụ: in ra thêm thông tin từ message
        # print(f"Received message with payload: {message.payload.decode('utf-8')}")  
    def get_direction(self, true_course):
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
# ==============================================================================================================

# =================================================== Play sound ==============================================
def playAudio():
    global latitude_values,longitude_values,turn_values
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
# ===============================================================================================================

# =====================================================  Main App  ==============================================

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
        # Khởi tạo và bắt đầu luồng phát âm thanh
        self.sound_thread = threading.Thread(target=playAudio, daemon=True)
        self.sound_thread.start()
        # Khởi tạo MQTT Client
        self.mqtt_client = CustomMQTTClient(mqtt_broker, mqtt_port, mqtt_username, mqtt_password, mqtt_topic_1)
        self.frames = {}  # Dictionary to store frames
        # Initialize frames
        self.create_frames()
        self.label_time = tk.Label(self, font=('Arial', 15, 'bold'), bg="white", fg="#4660ac", borderwidth=0, 
                                   border=0, width=18, relief='groove', justify=CENTER)
        self.label_time.place(x=54, y=102)
        #--------------------------- Func -------------------------------
        self.update_time()
         # Gán hàm xử lý sự kiện khi đóng cửa sổ
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        # Đóng kết nối MQTT
        self.mqtt_client.close_hivemq()

        # Chờ cho luồng phát âm thanh kết thúc
        self.sound_thread.join()

        # Hủy ứng dụng Tkinter
        self.destroy()

    def create_frames(self):
        #------------------------- frame2 -------------------------------
        self.frame2 = Frame2(self)
        self.frames["frame2"] = self.frame2
        self.frame2.config(bg="white", width=1180, height=550)
        self.frame2.place(x=52, y=146)
        self.button_frame2 = tk.Button(self, text="Theo dõi tàu", font=('Arial', 13, 'bold'), bg="white", fg="#4660ac", 
                                       activebackground="white", cursor='hand2', borderwidth=0, border=0, width=15, 
                                       relief='groove', justify=CENTER, command=lambda: self.raise_frame("frame2"))
        self.button_frame2.place(x=881, y=100)

        #------------------------- frame3 -------------------------------
        self.frame3 = Frame3(self)
        self.frames["frame3"] = self.frame3
        self.frame3.config(bg="white", width=1180, height=550)
        self.frame3.place(x=52, y=146)
        self.button_frame3 = tk.Button(self, text="Trang dữ liệu", font=('Arial', 13, 'bold'), bg="white", fg="#4660ac", 
                                       activebackground="white", cursor='hand2', borderwidth=0, border=0, width=15, 
                                       relief='groove', justify=CENTER, command=lambda: self.raise_frame("frame3"))
        self.button_frame3.place(x=1081, y=100)

        #------------------------- Frame1 -------------------------------
        self.frame1 = Frame1(self)
        self.frames["frame1"] = self.frame1
        self.frame1.config(bg="white", width=1180, height=550)
        self.frame1.place(x=52, y=146)
        self.button_frame1 = tk.Button(self, text="Trang thông tin", font=('Arial', 13, 'bold'), bg="white", fg="#4660ac", 
                                       activebackground="white", cursor='hand2', borderwidth=0, border=0, width=15, 
                                       relief='groove', justify=CENTER, command=lambda: self.raise_frame("frame1"))
        self.button_frame1.place(x=680, y=100)

    def raise_frame(self, frame_name):
        frame = self.frames.get(frame_name)
        if frame and frame.winfo_exists():
            frame.tkraise()
        else:
            print(f"{frame_name} does not exist or has been destroyed, recreating...")
            self.recreate_frame(frame_name)
            frame = self.frames[frame_name]
            frame.tkraise()

    def recreate_frame(self, frame_name):
        if frame_name == "frame1":
            self.frame1 = Frame1(self)
            self.frames["frame1"] = self.frame1
            self.frame1.config(bg="white", width=1180, height=550)
            self.frame1.place(x=52, y=146)
        elif frame_name == "frame2":
            self.frame2 = Frame2(self)
            self.frames["frame2"] = self.frame2
            self.frame2.config(bg="white", width=1180, height=550)
            self.frame2.place(x=52, y=146)
        elif frame_name == "frame3":
            self.frame3 = Frame3(self)
            self.frames["frame3"] = self.frame3
            self.frame3.config(bg="white", width=1180, height=550)
            self.frame3.place(x=52, y=146)
        #--------------------------- Func -------------------------------
        self.update_time()
    def update_time(self):
        # Real time """datetime(year, month, day[, hour[, minute[, second[, microsecond[,tzinfo]]]]])\
        global current_time
        current_time = datetime.now().strftime('%Y-%m-%d  %H:%M:%S')
        self.label_time.config(text=current_time)
        self.label_time.after(1000,self.update_time)
        
#==================================================== Frame 1: Trang điều khiển xe ===================================================
        
class Frame1(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        #-------------------------------- Train status -----------------------------------------------------------------------------
        self.label_status=Label(self,text="Trạng thái Tàu",fg='white',bg='#f22f2f',relief='groove',
                        width=20,borderwidth=1,border=1,justify=CENTER,font=("Arial", 15, "bold"),pady=5)
        self.label_status.place(x=29,y=160)
        self.label_Noti=Label(self,text="Trạng thái",fg='white',bg='#777777',relief='groove',pady=4,
                        width=17,borderwidth=1,border=1,justify=CENTER,font=("Arial", 13, "bold"))
        self.label_Noti.place(x=62,y=215)
        #--------------------------------------------------- Direction --------------------------------------------------------------
        self.label_direction=Label(self,text="Hương di chuyển",fg='white',bg='#f22f2f',relief='groove',
                        width=20,borderwidth=1,border=1,justify=CENTER,font=("Arial", 15, "bold"),pady=5)
        self.label_direction.place(x=29,y=270)
        self.label_show=Label(self,text="hướng di chuyển",fg='white',bg='#777777',relief='groove',pady=4,
                        width=17,borderwidth=1,border=1,justify=CENTER,font=("Arial", 12, "bold"))
        self.label_show.place(x=62,y=325)
        #------------------------------------ show Location - Speed ----------------------------------------------------------------
        # Header label
        self.header1= Label(self,text="Địa chỉ hiện tại",fg='white',bg="#4660ac",width=30,borderwidth=0,border=1,justify=CENTER,
                       font=("Arial", 15, "bold"),relief='groove',pady=5)
        self.header1.place(x=400,y=110)
        self.header1.config(justify='center')
        # lable Location
        self.local1= Label(self,text="Địa chỉ",fg="#4660ac",width=30,borderwidth=1,border=1,justify=CENTER,
                           font=("Arial", 15, "bold"),pady=5)
        self.local1.place(x=400,y=165)
        #header speed
        self.header2= Label(self,text="Tốc độ hiện tại",fg='white',bg="#4660ac",width=30,borderwidth=0,border=1,justify=CENTER,
                       font=("Arial", 15, "bold"),relief='groove',pady=5)
        self.header2.place(x=400,y=270)
        # lable Speed
        self.speed1= Label(self,text="Tốc độ",fg="#4660ac",width=30,borderwidth=1,border=1,justify=CENTER,
                           font=("Arial", 15, "bold"),pady=5)
        self.speed1.place(x=400,y=325)
         #-------------------------------------- Target train --------------------------------------------------------------------------
        self.Label_target=Label(self,text="Mục tiêu di chuyển",fg='white',bg="#4660ac",width=30,borderwidth=0,border=1,justify=CENTER,
                       font=("Arial", 15, "bold"),pady=5)
        self.Label_target.place(x=400,y=380)
        self.Entry_Lat_Long_Target=Entry(self,fg="#4660ac",bg="#EDEBEB",relief='flat',width=19,borderwidth=1,border=1,justify=CENTER
                                         ,font=("Arial", 15, "bold"))
        self.Entry_Lat_Long_Target.place(x=550,y=435)        
        self.Label_target=Label(self,text="Kinh độ/ Vĩ độ",fg='white',bg="#4660ac",width=12,borderwidth=0,border=0,justify=CENTER,
                                        font=("Arial", 14, "bold"))
        self.Label_target.place(x=400,y=435)
        # --------------------------------------- Status Speed ---------------------------------------------------------------------------
    
        self.header_speed=Label(self,text="Cảnh báo tốc độ",fg='white',bg='#f22f2f',relief='groove',
                        width=20,borderwidth=1,border=1,justify=CENTER,font=("Arial", 15, "bold"),pady=5)
        self.header_speed.place(x=900,y=160)
        self.header_speed_noti = Label(self,text="Cảnh báo",fg='white',bg='#777777',relief='groove',pady=4,
                        width=17,borderwidth=1,border=1,justify=CENTER,font=("Arial", 12, "bold"))
        self.header_speed_noti.place(x=933,y=215)
        # -------------------------------------------------- TURN ON /OFF notification ----------------------------------------------------
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
            Latitude_target=0.0
            Longitude_target=0.0
            target_id=1
        data_target = self.Entry_Lat_Long_Target.get() 
        if data_target !="" and data_target is not None:
            # data_target = self.Entry_Latitude_Target.get() 
            parts = data_target.split()
            try:  # Kiểm tra xem danh sách có phần tử nào không trước khi truy cập

                Latitude_target=float(parts[0])
                Longitude_target=float(parts[1])
            except Exception as e:
                print(f"An error occurred: {e}")
        self.after(2000,self.update_label_location_target)
        
    def update_frame1_realtime(self):
        global train_status,Location,speed_values,longitude_values,latitude_values,direction,flag_frame1
        # self.update_label_location_target()
        if flag_frame1 is True:
            flag_frame1 = False
            try:    
                self.header_speed_noti.config(text=train_status)
                self.label_Noti.config(text=train_status)
                self.local1.config(text=Location)
                self.label_show.config(text=direction)
                self.speed1.config(text=speed_values)
            except Exception as e:
                print(f"An error occurred in frame1 : {e}")
        self.after(500, self.update_frame1_realtime)

#------------------------- Frame 2:  Show map -----------------------------------------------------------
        
class Frame2(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.marker1 =None
        self.marker2 =None
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
        self.header2_6  =Label(self,text="Hướng di chuyển",fg='white',bg="#4660ac",width=15,borderwidth=0,border=1,justify=CENTER,font=("Arial", 12, "bold"),relief='groove',pady=2)
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
        # self.map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")  # OpenStreetMap (default)
        self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)  # google normal
        # self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)  # google satellite
        #----------------------Show location - Real time------------------------
        self.map_widget.add_right_click_menu_command(label="xóa mục tiêu",command=self.clear_marker_event,
                                                pass_coords=True)
        self.update_location_map()
        self.update_location_target()

    # update location in map
    def update_location_map(self):
        global data_queue,latitude_values,longitude_values,train_status,speed_values,direction,flag_frame2,Location
        if flag_frame2 == True:
            flag_frame2 =False
            # print(latitude_values,longitude_values)
            self.Address.config(text=Location)
            # update_label_direction 
            self.Direction.config(text=direction)
            # update_speed()
            self.speed.config(text=speed_values)
            self.latitude.config(text=latitude_values)
            self.Longitude.config(text=longitude_values)
            try:
                if self.marker1 is not None:
                    self.marker1.delete()
                self.marker1= self.map_widget.set_position(latitude_values, longitude_values,marker=True)
                # self.map_widget.set_path()
            except Exception as e:
                print(e)
        else:
            pass
        # Update the position on the map
        self.after(500,self.update_location_map)
    def update_location_target(self):
        global latitude_values,longitude_values,target_id,Latitude_target,Longitude_target,turn_values,distance_2_point,mutex
        # print(Latitude_target,Longitude_target)
        # address = tkintermapview.convert_address_to_coordinates(Location_target)
        if Latitude_target and Longitude_target is not None:
            try:
                # Khai báo một mutex
                # mutex.acquire()
                self.distance_2_point=hs.haversine((Latitude_target,Longitude_target),(latitude_values,longitude_values),unit=Unit.KILOMETERS)
                self.marker2=self.map_widget.set_marker(Latitude_target,Longitude_target,text="Điểm mục tiêu")
                # update distance values
                self.Distance.config(text=distance_2_point)
                # Load file âm thanh
                if self.distance_2_point <= 1.0 :
                    # self.marker2.delete()
                    self.marker2.delete()
                    # self.map_widget.delete_all_path()
                    if turn_values == 1:
                        playsound('Audio/Audio_MucTieu.wav')
                    target_id=0
                    self.Distance.config(text="Hoàn thành")
                # mutex.release()
            except Exception as e:
                print(e)
                target_id=1
        self.after(2000,self.update_location_target)
    def clear_marker_event(self,event=None):
        global target_id 
        try:
            target_id=0
            self.map_widget.delete_all_marker()
            self.Distance.config(text="")
        except Exception as e:
            print(f"An error occurred in frame2: {e}")
        
#----------------------------------------------------- Frame 3: Data Receive ---------------------------------------------------------------------
        
class Frame3(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        # Tạo Treeview
        self.tree = ttk.Treeview(self, columns=("Time", "Latitude", "Longtitud","Speed","Location","Status"), show="headings")
        self.tree.place(width=1000,height=500,x=0,y=20)
        self.tree.heading("Speed", text="Tốc độ")
        self.tree.heading("Latitude", text="Kinh độ")
        self.tree.heading("Longtitud", text="Vĩ độ")
        self.tree.heading("Location", text="Địa chỉ hiện tại")
        self.tree.heading("Status", text="Trạng thái")
        self.tree.heading("Time", text="Thời gian")
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
        global current_time,Location,latitude_values,longitude_values,train_status,speed_values,flag_frame3
        # Loại bỏ ký tự xuống dòng (\n)
        if flag_frame3 == True :
            flag_frame3 =False
            Location_no_newline = Location.replace("\n", "")
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
            except Exception as e:
                messagebox.showerror("Lỗi", f"Có lỗi xảy ra khi lưu file: {e}")
    def clear_data_received(self):
        for item in self.tree.get_children(): # used self.tree instead
            self.tree.delete(item)
            
if __name__ == "__main__":
    app = RootApplication()
    app.mainloop()