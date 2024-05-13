# # # import openpyxl
# # import paho.mqtt.client as paho
# # from paho import mqtt
# # import time 
# # import json
# # # import simpleaudio as sa
# # from playsound import playsound
# # from receive_from_esp import get_ID_esp
# # import threading

# # # data 
# # Location_1_Latitude={21.02423241,
# #                       21.04902552,
# #                       21.04938853,
# #                       20.99465319,
# #                       20.98529548,
# #                       20.94769766}
# # Location_1_Longitude={105.8409704,
# #                         105.8731988,
# #                         105.8919927,
# #                         105.9724607,
# #                         106.0382846,
# #                         106.3281004
# # }

# # Location_2_Latitude={20.946406254,
# #                         20.945239283,
# #                         20.978829420,
# #                         20.851250375,
# #                         20.851073448,
# #                         20.85596
# # }
# # Location_2_Longitude={106.337105086,
# #                         106.361051675,
# #                         106.422718104,
# #                         106.668475010,
# #                         106.670437086,
# #                         106.68736
# # }
# # #---------------------------connect to  MQTT----------------------------------

# # # /*MQTT Broker Connection Details*/
# # mqtt_broker = "ae501b5ee3194ca682bd67e257459478.s1.eu.hivemq.cloud"
# # mqtt_username = "RainWay System1"
# # mqtt_password = "012301230123aA#"
# # mqtt_port = 8883
# # # data speed receive 
# # train_speed =0
# # train_ID = 0 
# # def get_data_status():
# #     # Some data processing code here
# #     data = {
# #         'speed':train_speed
# #     }
# #     return data

# # def on_connect(client, userdata, flags, rc, properties=None):
# #     print("CONNACK received with code %s." % rc)
# #     # subscribe 1 topic 
# #     client.subscribe("esp8266/speed")
# # # Callback function khi nhận được tin nhắn từ MQTT Broker
# # def on_message(client, userdata, message):
# #     print("Received message '" 
# #           + str(message.payload.decode("utf-8")) 
# #           + "' on topic '"+ message.topic 
# #           + "' with QoS " + str(message.qos))
# #     # lable Location
# #     data = json.loads(str(message.payload.decode("utf-8")) )
# #     global train_speed
# #     train_speed =  data['speed']
# # # client_id is the given name of the client
# # client = paho.Client(paho.CallbackAPIVersion.VERSION2)
# # # connect to MQTT
# # client.on_connect = on_connect

# # # enable TLS for secure connection
# # client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
# # # set username and password
# # client.username_pw_set(mqtt_username,mqtt_password)
# # # connect to HiveMQ Cloud on port 8883 (default for MQTT)
# # client.connect(mqtt_broker,mqtt_port)
# # # setting callbacks, use separate functions like above for better visibility
# # client.on_message = on_message

# # client.loop_start()


# # def publish_data():
# #     data =get_ID_esp()
# #     train_ID=data['ID']
# #     while(1):
# #         if train_ID==1:
# #             # Load file âm thanh
# #             playsound('Audio/Audio_HaNoi.wav')
# #             i=0
# #             while i<=5:
# #                 if train_speed!=0:
# #                     default_value = '{"Latitude":%f,"Longitude":%f}'%(Location_1_Latitude[i],Location_1_Longitude[i])
# #                     client.publish("esp8266/Location_data",payload=default_value)
# #                     time.sleep(1)
# #                     i+=1
# #                 else: 
# #                     pass
# #             # time.sleep(0.5)
# #         while train_ID==1 : 
# #             pass
# #         if train_ID ==2:
# #             # Load file âm thanh
# #             playsound( 'Audio/Audio_HaiDuong.wav')    
# #             i=0
# #             while i<=5:
# #                 if train_speed!=0:
# #                     default_value = '{"Latitude":%f,"Longitude":%f}'%(Location_2_Latitude[i],Location_2_Longitude[i])
# #                     client.publish("esp8266/Location_data",payload=default_value)    
# #                     i+=1
# #                     time.sleep(1)
# #                 else: 
# #                     pass
# #                 # time.sleep(0.5)
# #         while train_ID==2 : 
# #             pass
# #     # if train_ID ==3: 
# #     #     # Load file âm thanh
# #     #     # playsound('Audio/Audio_HaiPhong.wav')
# #     #     None
# # thread1 = threading.Thread(target=publish_data)
# # # Bắt đầu các luồng
# # thread1.start()  



# import tkinter as tk
# from tkinter import *
# import tkintermapview 
# from tkinter import ttk
# from PIL import ImageTk, Image
# from datetime import datetime
# import paho.mqtt.client as paho
# from paho import mqtt
# from tkinter import filedialog, messagebox
# from openpyxl import Workbook
# import haversine as hs   
# from haversine import Unit
# import time 
# # import simpleaudio as sa
# # from playsound import playsound
# import json 
# from receive_from_esp import*
# # from data import*
# # from data import get_data_status
# from Receive_status_esp import get_data_status

# #---------------- initializing the variables    -----------------------
# # Realtime data latitude - longitude from cloud
# latitude_values=0.0
# longitude_values=0.0
# #Location after transfer Latitude - Longitude to Addresss
# Location=""
# # Location target
# get_entry=""
# Location_target=""
# # target_id 
# target_id=1
# # Real time 
# current_time=""
# # values get to table
# data=""
# speed_id=""
# #Status connect to Hivemq 
# status=""
# # Train status 
# train_status="An Toàn"
# # Turn ON / OFF notification 
# turn_values=0
# #---------------------------connect to  MQTT---------------------------------

# # /*MQTT Broker Connection Details*/
# mqtt_broker = "ae501b5ee3194ca682bd67e257459478.s1.eu.hivemq.cloud"
# mqtt_username = "RainWay System"
# mqtt_password = "012301230123aA#"
# mqtt_port = 8883
# mqtt_topic_1 = "esp8266/Location_data"

# def on_connect(client, userdata, flags, rc, properties=None):
#     print("CONNACK received with code %s." % rc)
#     # subscribe 1 topic 
#     global status 
#     status = rc
#     client.subscribe(mqtt_topic_1)
# # Callback function khi nhận được tin nhắn từ MQTT Broker
# def on_message(client, userdata, message):
#     print("Received message '" 
#         + str(message.payload.decode("utf-8")) 
#         + "' on topic '"+ message.topic 
#         + "' with QoS " + str(message.qos))
#     data = json.loads(str(message.payload.decode("utf-8")) )
#     global latitude_values,longitude_values,Location,turn_values,train_status
#     latitude_values=data["Latitude"]
#     longitude_values=data["Longitude"]
#     adr = tkintermapview.convert_coordinates_to_address(latitude_values,longitude_values)
#     Location = str(adr.street)+"\n"+str(adr.city) +"\n"+str(adr.country)
#     #------------------------------ Update data when receive data from cloud -------------------------------------
#     # receive data from esp -> notification Distance between Sation and Train :
#     # Ha Noi Station (Id: 1), Hai Duong Staion(Id: 2), Hai Phong Station (Id :3 ) 
#     # distance Train - Station
#     # adr = tkintermapview.convert_coordinates_to_address(latitude_values,longitude_values)
#     # Location = str(adr.street)+"\n"+str(adr.city) +"\n"+str(adr.country)
#     # if (turn_values.get()) == 1:
#     #     if hs.haversine((latitude_values,longitude_values),(21.02439,105.84122),unit=Unit.KILOMETERS) <=1 :
#     #         # Load file âm thanh
#     #         playsound('Audio/Audio_HaNoi.wav')
            
#     #     if hs.haversine((latitude_values,longitude_values),(20.94663,106.33057),unit=Unit.KILOMETERS) <=1 :
#     #         # Load file âm thanh
#     #         playsound( 'Audio/Audio_HaiDuong.wav')
#     #     if hs.haversine((latitude_values,longitude_values),(20.85596,106.68736),unit=Unit.KILOMETERS) <=1 :
#     #         # Load file âm thanh
#     #         playsound('Audio/Audio_HaiPhong.wav')

# # client_id is the given name of the client 
# client = paho.Client(paho.CallbackAPIVersion.VERSION2)
# # connect to MQTT
# client.on_connect = on_connect

# # enable TLS for secure connection
# client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
# # set username and password
# client.username_pw_set(mqtt_username,mqtt_password)
# # connect to HiveMQ Cloud on port 8883 (default for MQTT)
# client.connect(mqtt_broker,mqtt_port)
# # setting callbacks, use separate functions like above for better visibility
# client.on_message = on_message

# client.loop_start()

# #--------------------------------------------------------------  Main  -------------------------------------

# class RootApplication(tk.Tk):
#     def __init__(self):
#         super().__init__()
#         self.title("Train System")
#         self.geometry("1280x720+150+20")
#         self.resizable(False,False)
#         self.configure(bg='gray')
#         self.title("Hệ Thống Tàu Hỏa")
#         # Icon 
#         self.iconbitmap('image\eye.ico')
#         # BackGround:
#         self.image = Image.open(r"C:\Users\dungs\Desktop\DATN\image\Bground-min.png")
#         self.img = ImageTk.PhotoImage(self.image)
#         # image_path = "image/Bground.png"
#         # self.img = PhotoImage(file=image_path)
#         self.label_Bg=tk.Label(self,image=self.img)
#         self.label_Bg.place(x=0,y=0)
#         # Create frame - button frame : 3 frame 
#         #------------------------- frame2 -------------------------------
#         self.frame2 = Frame2(self)
#         self.frame2.config(bg="white",width=1180,height=550)
#         self.frame2.place(x=52,y=146)
#         self.button_frame1=Button(self,text="Theo dõi xe",font=('Arial', 13, 'bold'),bg="white",fg="#4660ac",activebackground="white",cursor='hand2',
#                                   borderwidth=0,border=0,width=15,relief='groove',justify=CENTER,command=lambda: self.show_frame(self.frame2))
#         self.button_frame1.place(x=881,y=100)
#         #------------------------- frame3 -------------------------------
#         self.frame3 = Frame3(self)
#         self.frame3.config(bg="white",width=1180,height=550)
#         self.frame3.place(x=52,y=146)
#         self.button_frame1=Button(self,text="Trang dữ liệu",font=('Arial', 13, 'bold'),bg="white",fg="#4660ac",activebackground="white",cursor='hand2',
#                                   borderwidth=0,border=0,width=15,relief='groove',justify=CENTER,command=lambda: self.show_frame(self.frame3))
#         self.button_frame1.place(x=1081,y=100)
#         #------------------------- Frame1 -------------------------------
#         self.frame1 = Frame1(self)
#         self.frame1.config(bg="white",width=1180,height=550)
#         self.frame1.place(x=52,y=146)
#         self.button_frame1=Button(self,text="Trang thông tin",font=('Arial', 13, 'bold'),bg="white",fg="#4660ac",activebackground="white",cursor='hand2',
#                                   borderwidth=0,border=0,width=15,relief='groove',justify=CENTER,command=lambda: self.show_frame(self.frame1))
#         self.button_frame1.place(x=680,y=100)
#         self.label_time = tk.Label(self, font=('Arial', 15, 'bold'),bg="white",fg="#4660ac"
#                                    ,borderwidth=0,border=0,width=18,relief='groove',justify=CENTER)
#         self.label_time.place(x=54,y=102)
#         #--------------------------- Func -------------------------------
#         self.update_time()
#     def update_time(self):
#         # Real time """datetime(year, month, day[, hour[, minute[, second[, microsecond[,tzinfo]]]]])\
#         global current_time
#         current_time = datetime.now().strftime('%Y-%m-%d  %H:%M:%S')
#         self.label_time.config(text=current_time)
#         self.label_time.after(1000,self.update_time)
#     def show_frame(self,frame_show):
#         frame_show.tkraise()
# #------------------------------------------- Frame 1: Trang điều khiển xe ---------------------------------------------------
        
# class Frame1(tk.Frame):
#     def __init__(self, master):
#         super().__init__(master)

#         #-------------------------------- status connect to hiveMQ --------------------------------------------------------------------------------

#         self.label_status=Label(self,text="Trạng thái kết nối",fg='white',bg='#f22f2f',relief='groove',
#                         width=20,borderwidth=1,border=1,justify=CENTER,font=("Arial", 15, "bold"),pady=5)
#         self.label_status.place(x=29,y=160)
#         self.label_Noti=Label(self,text="kết nối..",fg='white',bg='#777777',relief='groove',pady=4,
#                         width=17,borderwidth=1,border=1,justify=CENTER,font=("Arial", 13, "bold"))
#         self.label_Noti.place(x=62,y=215)
#         #--------------------------------------------------- Train status --------------------------------------------------------------------------------

#         self.label_status=Label(self,text="Trạng thái Tàu",fg='white',bg='#f22f2f',relief='groove',
#                         width=20,borderwidth=1,border=1,justify=CENTER,font=("Arial", 15, "bold"),pady=5)
#         self.label_status.place(x=870,y=160)
#         self.label_show=Label(self,text="Trạng thái..",fg='white',bg='#777777',relief='groove',pady=4,
#                         width=17,borderwidth=1,border=1,justify=CENTER,font=("Arial", 12, "bold"))
#         self.label_show.place(x=910,y=215)
#         # -------------------------------------------------- TURN ON /OFF notification -------------------------------------------------------------------
#         # Change Turn values:
#         global turn_values
#         turn_values = IntVar()
#         turn_values.set(1)
#         self.check_turn =tk.Checkbutton(self,text = "Âm thanh thông báo", variable = turn_values,font=("Arial", 15, "bold"),cursor='hand2') 
#         self.check_turn.place(x=35,y=320)
#         # #------------------------------------ show Location - Speed ---------------------------------------------------------------------------------
         
#         # Header label
#         self.header1= Label(self,text="Địa chỉ hiện tại",fg='white',bg="#4660ac",width=30,borderwidth=0,border=1,justify=CENTER,
#                        font=("Arial", 15, "bold"),relief='groove',pady=5)
#         self.header1.place(x=400,y=110)
#         self.header1.config(justify='center')
#         # lable Location
#         self.local1= Label(self,text="Location",fg="#4660ac",width=30,borderwidth=1,border=1,justify=CENTER,font=("Arial", 15, "bold"),pady=5)
#         self.local1.place(x=400,y=165)
#         #header speed
#         self.header2= Label(self,text="Tốc độ hiện tại",fg='white',bg="#4660ac",width=30,borderwidth=0,border=1,justify=CENTER,
#                        font=("Arial", 15, "bold"),relief='groove',pady=5)
#         self.header2.place(x=400,y=270)
#         # lable Speed
#         self.speed1= Label(self,text="speed",fg="#4660ac",width=30,borderwidth=1,border=1,justify=CENTER,font=("Arial", 15, "bold"),pady=5)
#         self.speed1.place(x=400,y=325)
#          #--------------------------------------------------- Target train --------------------------------------------------------------------------

#         self.Label_target=Label(self,text="Mục tiêu di chuyển",fg='white',bg="#4660ac",width=30,borderwidth=0,border=1,justify=CENTER,
#                        font=("Arial", 15, "bold"),pady=5)
#         self.Label_target.place(x=400,y=380)
#         self.Entry_Target=Entry(self,fg="#4660ac",bg="#EDEBEB",relief='flat',width=33,borderwidth=1,border=1,justify=CENTER,font=("Arial", 15, "bold"))
#         self.Entry_Target.place(x=400,y=435)        
#         # Update frame
#         self.update_frame1_realtime()
#         # # --------------- Control Speed -----------------------
    
#         # self.header_speed=Label(self,text="Điều khiển tốc độ",fg='white',bg='#f22f2f',relief='groove',
#         #                 width=20,borderwidth=1,border=1,justify=CENTER,font=("Arial", 15, "bold"),pady=5)
#         # self.header_speed.place(x=900,y=160)
#         # self.button_speed3=Button(self,text="Mức 3",fg='white',bg='#777777',relief='groove',cursor='hand2',command=self.speed_3,
#         #                 width=15,borderwidth=1,border=1,justify=CENTER,font=("Arial", 13, "bold"))
#         # self.button_speed3.place(x=945,y=215)
#         # self.button_speed2=Button(self,text="Mức 2",fg='white',bg='#9b9b9b',relief='groove',cursor='hand2',command=self.speed_2,
#         #                 width=15,borderwidth=1,border=1,justify=CENTER,font=("Arial", 13, "bold"))
#         # self.button_speed2.place(x=945,y=265)
#         # self.button_speed1=Button(self,text="Mức 1",fg='white',bg='#bcbbbb',relief='groove',cursor='hand2',command=self.speed_1,
#         #                 width=15,borderwidth=1,border=1,justify=CENTER,font=("Arial", 13, "bold"))
#         # self.button_speed1.place(x=945,y=315)
#         # self.button_speed0=Button(self,text="Dừng lại",fg='white',bg='#c1bfbf',relief='groove',cursor='hand2',command=self.speed_0,
#         #                 width=15,borderwidth=1,border=1,justify=CENTER,font=("Arial", 13, "bold"))
#         # self.button_speed0.place(x=945,y=365)

#     #     #--------------------- Update Label Location:---------------------------
        
#     # def speed_3(self):
#     #     global speed_id,train_status
#     #     default_value = '{"speed":%d}'%(3)
#     #     client.publish("esp8266/speed",payload=default_value)
#     #     speed_id="20 m/s"
#     #     self.speed1.config(text=speed_id)
#     #     # update status
#     #     train_status="An toàn"
#     #     self.label_show.config(text=train_status)
#     # def speed_2(self):
#     #     global speed_id,train_status
#     #     default_value = '{"speed":%d}'%(2)
#     #     client.publish("esp8266/speed",payload=default_value)
#     #     speed_id="15 m/s"
#     #     self.speed1.config(text=speed_id)
#     #     # update status
#     #     train_status="An toàn"
#     #     self.label_show.config(text=train_status)
#     # def speed_1(self):
#     #     global speed_id
#     #     default_value = '{"speed":%d}'%(1)
#     #     client.publish("esp8266/speed",payload=default_value)
#     #     speed_id="10 m/s"
#     #     self.speed1.config(text=speed_id)
#     #     # update status
#     #     train_status="An toàn"
#     #     self.label_show.config(text=train_status)
#     # def speed_0(self):
#     #     global speed_id
#     #     default_value = '{"speed":%d}'%(0)
#     #     client.publish("esp8266/speed",payload=default_value)
#     #     speed_id="Stop"
#     #     self.speed1.config(text=speed_id)
#     #     # update status
#     #     train_status="Không an toàn"
#     #     self.label_show.config(text=train_status)
#     # lable Location
#     # def update_label_location(self):
#     #     global Location
#     #     self.local1.config(text=Location)
#     # def update_label_location_target(self):
#     #     global Location_target,target_id
#     #     if target_id==0:
#     #         self.Entry_Target.delete(0,'end')
#     #         target_id=1
#     #     Location_target=self.Entry_Target.get()
#     # def update_label_status(self):
#     #     global train_status,speed_id
#     #     data = get_data_status()
#     #     if data['speed'] ==0:
#     #         train_status="Không an toàn"
#     #         speed_id="Stop"
#     #         self.label_show.config(text=train_status)
#     #         # self.speed1.config(text=speed_id)
#     #     else:
#     #         train_status="An toàn"
#     #         self.label_show.config(text=train_status)
#     # def update_speed(self):
#     #     global speed_id
#     #     self.speed1.config(text=speed_id)
#     def update_frame1_realtime(self):
#         global Location,Location_target,target_id,train_status,speed_id,status
#         # Update label connect to hivemq
#         self.label_Noti.config(text=status)
#         # update_label_location
#         self.local1.config(text=Location)
#         # update_label_location_target
#         if target_id==0:
#             self.Entry_Target.delete(0,'end')
#             target_id=1
#         Location_target=self.Entry_Target.get()
#         print(Location_target)
#         # update_label_status
#         self.label_show.config(text=train_status)
#         # update_speed()
#         self.speed1.config(text=speed_id)
#         self.after(3000,self.update_frame1_realtime)

# #------------------------- Frame 2:  Show map -----------------------------------------------------------
        
# class Frame2(tk.Frame):
#     def __init__(self, master):
#         super().__init__(master)
#         #------------------- header location detail ---------------------------------------------------

#         # Header latitude
#         self.header2_1= Label(self,text="Kinh Độ",fg='white',bg="#4660ac",width=12,borderwidth=0,border=1,justify=CENTER,font=("Arial", 12, "bold"),relief='groove',pady=2)
#         self.header2_1.place(x=0,y=180)
#         # Header Longitude
#         self.header2_2= Label(self,text="Vĩ Độ",fg='white',bg="#4660ac",width=12,borderwidth=0,border=1,justify=CENTER,font=("Arial", 12, "bold"),relief='groove',pady=2)
#         self.header2_2.place(x=0,y=250)
#         # Header speed
#         self.header2_3= Label(self,text="Tốc độ",fg='white',bg="#4660ac",width=12,borderwidth=0,border=1,justify=CENTER,font=("Arial", 12, "bold"),relief='groove',pady=2)
#         self.header2_3.place(x=0,y=320)
#         # Header address
#         self.header2_4= Label(self,text="Địa chỉ",fg='white',bg="#4660ac",width=15,borderwidth=0,border=1,justify=CENTER,font=("Arial", 12, "bold"),relief='groove',pady=2)
#         self.header2_4.place(x=1032,y=180)
#         # Header distance: 
#         self.header2_5= Label(self,text="Khoảng cách",fg='white',bg="#4660ac",width=15,borderwidth=0,border=1,justify=CENTER,font=("Arial", 12, "bold"),relief='groove',pady=2)
#         self.header2_5.place(x=1032,y=280)

#         #------------------- values location details ---------------------------------------------------

#         # latitude values
#         self.latitude= Label(self,text="Kinh Độ",fg='Gray',width=15,borderwidth=0,border=1,justify=CENTER,font=("Arial", 10, "bold"),relief='groove',pady=2)
#         self.latitude.place(x=0,y=210)
#         # Longitude values
#         self.Longitude= Label(self,text="vĩ Độ",fg='Gray',width=15,borderwidth=0,border=1,justify=CENTER,font=("Arial", 10, "bold"),relief='groove',pady=2)
#         self.Longitude.place(x=0,y=280)
#         # speed values
#         self.speed= Label(self,text="Tốc Độ",fg='Gray',width=15,borderwidth=0,border=1,justify=CENTER,font=("Arial", 10, "bold"),relief='groove',pady=2)
#         self.speed.place(x=0,y=350)
#          # address values
#         self.Address= Label(self,text="Địa chỉ",fg='Gray',width=21,borderwidth=0,border=1,justify=CENTER,font=("Arial", 9, "bold"),relief='groove',pady=2)
#         self.Address.place(x=1032,y=210)
#          # Distance values
#         self.Distance= Label(self,text="Khoảng cách",fg='Gray',width=21,borderwidth=0,border=1,justify=CENTER,font=("Arial", 9, "bold"),relief='groove',pady=2)
#         self.Distance.place(x=1032,y=310)

#         #---------------------Map view-------------------------------------------------------

#         self.map_widget = tkintermapview.TkinterMapView(self, width=900, height=550, corner_radius=0)
#         self.map_widget.place(relx=0.49, rely=0.5, anchor=CENTER)
#         # self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)  # google normal
#         #----------------------Show location - Real time------------------------
#         self.update_location_map()
#         self.update_location_target()
#         self.update_realtime_frame2()
#     # Update speed text
#     # update location in map
#     def deledmarker(self):
#         self.marker1.delete()
#     def update_location_map(self):
#         global latitude_values,longitude_values
#         self.latitude.config(text=latitude_values)
#         self.Longitude.config(text=longitude_values)
#         # Update the position on the map
#         self.marker1= self.map_widget.set_position(latitude_values, longitude_values,marker=True)
#         self.marker1.set_text("Vị trí tàu")
#         self.after(1000,self.update_location_map)
#         self.after(2000,self.deledmarker)
#         # print(adr.street, adr.housenumber, adr.postal, adr.city, adr.state, adr.country, adr.latlng)
#     # data get to table
#     # def update_speed(self):
#     #     global speed_id
#     #     self.speed.config(text=speed_id)
#     # def update_location_target(self):
#     #     global Location_target
#     #     address = tkintermapview.convert_address_to_coordinates(Location_target)
#     #     if address is not None:
#     #         global latitude_values,longitude_values,target_id
#     #         latitude_target=address[0]
#     #         Longitude_target=address[1]
#     #         self.marker2=self.map_widget.set_position(latitude_target,Longitude_target,marker=True)
#     #         self.marker2.set_text("Điểm mục tiêu")
#     #         # update distance values
#     #         distance_2_point=hs.haversine((latitude_target,Longitude_target),(latitude_values,longitude_values),unit=Unit.KILOMETERS)
#     #         self.Distance.config(text=distance_2_point)
#     #         # Load file âm thanh
#     #         if distance_2_point <= 1.0:
#     #             self.marker2.delete()
#     #             # for _ in range(3):
#     #             playsound('Audio/Audio_MucTieu.wav')
#     #             # default_value = '{"speed":%d}'%(0)
#     #             # client.publish("esp8266/speed",payload=default_value)
#     #             target_id=0
#     #             self.Distance.config(text="")
#     #     else:
#     #         self.Distance.config(text="")
#     def update_location_target(self):
#         global Location_target,latitude_values,longitude_values,target_id
#         address = tkintermapview.convert_address_to_coordinates(Location_target)
#         print(address)
#         if address is not None:
#             latitude_target=address[0]
#             Longitude_target=address[1]
#             self.marker2=self.map_widget.set_position(latitude_target,Longitude_target,marker=True)
#             self.marker2.set_text("Điểm mục tiêu")
#             # update distance values
#             distance_2_point=hs.haversine((latitude_target,Longitude_target),(latitude_values,longitude_values),unit=Unit.KILOMETERS)
#             self.Distance.config(text=distance_2_point)
#             # Load file âm thanh
#             if distance_2_point <= 1.0:
#                 self.marker2.delete()
#                 # for _ in range(3):
#                 playsound('Audio/Audio_MucTieu.wav')
#                 # default_value = '{"speed":%d}'%(0)
#                 # client.publish("esp8266/speed",payload=default_value)
#                 target_id=0
#                 self.Distance.config(text="")
#         else:
#             self.Distance.config(text="")
#         self.after(3000,self.update_location_target)

#     def update_realtime_frame2(self):
#         # def update_speed(self):
#         global speed_id,Location
#         self.speed.config(text=speed_id)
#         # show địa chỉ dựa trên tọa độ.
#         self.Address.config(text=Location)
#         self.after(3000,self.update_realtime_frame2) 
        
# #----------------------------------------------------- Frame 3: Data Receive ---------------------------------------------------------------------
        
# class Frame3(tk.Frame):
#     def __init__(self, master):
#         super().__init__(master)
#         # Tạo Treeview
#         self.tree = ttk.Treeview(self, columns=("Time", "Latitude", "Longtitud","Speed","Location","Status"), show="headings")
#         self.tree.place(width=1000,height=500,x=0,y=20)
#         self.tree.heading("Speed", text="Speed")
#         self.tree.heading("Latitude", text="Latitude")
#         self.tree.heading("Longtitud", text="Longtitud")
#         self.tree.heading("Location", text="Location")
#         self.tree.heading("Status", text="Status")
#         self.tree.heading("Time", text="Time")
#         # Thiết lập chiều rộng cột
#         self.tree.column("Latitude", width=50)
#         self.tree.column("Longtitud", width=50)
#         self.tree.column("Speed", width=30)
#         self.tree.column("Location", width=250)
#         self.tree.column("Status", width=50)
#         self.tree.column("Time", width=30)
#         # Tạo scrollbar cho treeview
#         self.scrollbar1 = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
#         self.scrollbar2 = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview)
#         self.tree.configure(yscrollcommand=self.scrollbar1.set,xscrollcommand=self.scrollbar2.set)
#         self.scrollbar1.place(height=500,x=1000,y=20)
#         self.scrollbar2.place(width=1000,x=0,y=520)
#         #------------------------- get data to xlsx file ------------------------------------------
#         self.button_save = tk.Button(self,text="xuất dữ liệu",padx=8,pady=3,background="#4660ac",fg="white",font=("Arial", 15, "bold")
#                                      ,border=0,borderwidth=0,justify=CENTER,cursor='hand2',command=self.get_data)
#         self.button_save.place(x=1030,y=250)
#         # self.update_data(current_time, Location,latitude_values,longitude_values)  # Cập nhật thời gian mỗi giây
#         self.update_data()
#     # update data to table:
#     def update_data(self):
#         # Dữ liệu mẫu
#         global current_time,Location,latitude_values,longitude_values,train_status,speed_id
#         # Loại bỏ ký tự xuống dòng (\n)
#         Location_no_newline = Location.replace("\n", "")
#         data = [str(current_time), str(latitude_values), str(longitude_values),speed_id,Location_no_newline,train_status]
#         self.tree.insert("", "end", values=data)
#         self.after(3000,self.update_data)      
#     def get_data(self):
#         # Tạo một workbook mới
#         self.wb = Workbook()
#         # Chọn active worksheet (sheet mặc định)
#         self.ws = self.wb.active
#         # Ghi dữ liệu vào worksheet
#         self.ws.append(["Time", "Latitude", "Longtitude","Speed","Location","Status"])
#         for item in self.tree.get_children():
#             self.values = self.tree.item(item, 'values')
#             self.ws.append(self.values)
#         self.clear_data_received()
#         # Hiển thị hộp thoại để chọn vị trí lưu tệp
#         file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
#         if file_path:
#             # Lưu workbook thành file Excel tại đường dẫn đã chọn
#             try:
#                 self.wb.save(file_path)
#                 messagebox.showinfo("Thông báo", "Dữ liệu đã được lưu vào file Excel thành công!")
#             except Exception as e:
#                 messagebox.showerror("Lỗi", f"Có lỗi xảy ra khi lưu file: {e}")
#     def clear_data_received(self):
#         for item in self.tree.get_children(): # used self.tree instead
#             self.tree.delete(item)


# if __name__ == "__main__":
#     app = RootApplication()
#     app.mainloop()


import math

class Vehicle:
    def __init__(self, current_position):
        self.current_position = current_position

    def move_to_destination(self, destination):
        while not self.at_destination(destination):
            direction = self.calculate_direction(destination)
            self.update_position(direction)
            print(f"Moving to {self.current_position}")

    def at_destination(self, destination):
        return self.current_position == destination

    def calculate_direction(self, destination):
        dx = destination[0] - self.current_position[0]
        dy = destination[1] - self.current_position[1]
        distance = math.sqrt(dx**2 + dy**2)
        direction = (dx/distance, dy/distance) if distance != 0 else (0, 0)
        return direction

    def update_position(self, direction):
        speed = 0.1  # Tốc độ di chuyển của xe
        self.current_position = (self.current_position[0] + speed * direction[0],
                                 self.current_position[1] + speed * direction[1])

# Khởi tạo xe ở vị trí (0, 0)
vehicle = Vehicle((0, 0))
# Điều khiển xe đến điểm đích (10, 10)
vehicle.move_to_destination((10, 10))