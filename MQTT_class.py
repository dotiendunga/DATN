import paho.mqtt.client as paho
from paho import mqtt

class MQTTClient:
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
    # Publish data to hivemq
    def send_data_to_hivemq(self,mqtt_topic,json_data):
        self.client.publish(mqtt_topic,json_data)
    def start(self):
        self.client.loop_start()
    def close_hivemq(self):
        self.client.loop_stop()
        self.client.disconnect()