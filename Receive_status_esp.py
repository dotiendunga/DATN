import paho.mqtt.client as paho
from paho import mqtt
import json
#---------------------------connect to  MQTT----------------------------------

# /*MQTT Broker Connection Details*/
mqtt_broker = "ae501b5ee3194ca682bd67e257459478.s1.eu.hivemq.cloud"
mqtt_username = "RainWay System"
mqtt_password = "012301230123aA#"
mqtt_port = 8883
mqtt_topic_1 = "esp8266/speed"
# Data receive from esp     
train_speed=0

def get_data_status():
    # Some data processing code here
    data = {
        'speed': train_speed
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
    global train_speed
    train_speed= data['speed']

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