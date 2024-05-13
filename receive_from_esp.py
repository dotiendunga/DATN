import paho.mqtt.client as paho
from paho import mqtt
# from playsound import playsound
import json
# import openpyxl
# import time 
import pygame

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
#---------------------------connect to  MQTT----------------------------------

# /*MQTT Broker Connection Details*/
mqtt_broker = "ae501b5ee3194ca682bd67e257459478.s1.eu.hivemq.cloud"
mqtt_username = "RainWay System"
mqtt_password = "012301230123aA#"
mqtt_port = 8883
mqtt_topic_1 = "esp8266/Location_esp"

# Data receive from esp     
latitude_values_esp = 0.0
longitude_values_esp= 0.0
train_id=0


def get_ID_esp():
    # Some data processing code here
    data = {
        'ID': train_id
    }
    return data

def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)
    # subscribe 1 topic 
    client.subscribe(mqtt_topic_1)
# Callback function khi nhận được tin nhắn từ MQTT Broker
def on_message(client, userdata, message):
    print("Received message '" 
          + str(message.payload.decode("utf-8")) 
          + "' on topic '"+ message.topic 
          + "' with QoS " + str(message.qos))
    data = json.loads(str(message.payload.decode("utf-8")) )
    global train_id
    train_id =  data['ID']
    # latitude_values_esp=data['Latitude']
    # longitude_values_esp=data['Longitude']
    if train_id == 1:
        # Load file âm thanh
        playsound('Audio/Audio_HaNoi.wav')
        train_id =0
    if train_id == 2:
        # Load file âm thanh
        playsound( 'Audio/Audio_HaiDuong.wav')
        train_id=0
    if train_id == 3:
        # Load file âm thanh
        playsound('Audio/Audio_HaiPhong.wav')
        train_id=0
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

# client_id is the given name of the client
# def get_data_esp():
#     # Some data processing code here
#     data = {
#         'latitude_values_esp': latitude_values_esp,
#         'longitude_values_esp': longitude_values_esp,
#         'train_id': train_id
#     }
#     return data
# def set_data_esp():
#     # Some data processing code here
#     global train_id,latitude_values_esp,longitude_values_esp
#     train_id=0
#     latitude_values_esp=0
#     longitude_values_esp=0