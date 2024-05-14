#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <WiFiClientSecure.h>
#include <ArduinoJson.h>

// config pin 
const int trigPin = 12;
const int echoPin = 14;

//define sound velocity in cm/uS
#define SOUND_VELOCITY 0.034

long duration;
float distanceCm;
uint16_t val;

/* ------------------------Wifi connnection Details-----------------------*/ 
// const char* ssid ="TTCH";
// const char* password = "ase123456";
const char* ssid ="TTCH";
const char* password = "ase123456";
/*----------------MQTT Broker Connection Details-------------------------*/

const char* mqtt_server = "ae501b5ee3194ca682bd67e257459478.s1.eu.hivemq.cloud";
const char* mqtt_username = "RainWay System"; 
const char* mqtt_password = "012301230123aA#";
const int mqtt_port = 8883;
#define  mqtt_topic_speed  "esp8266/speed"

//--------------Setup wifi------------------------------------

WiFiClientSecure espClient;
PubSubClient client(espClient);

/*-----------------------Function Connect to wifi-----------------*/

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  randomSeed(micros());
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

/*----------------------Connect to MQTT Broker-----------------------------*/

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    String clientID =  "ESPClient-";
    clientID += String(random(0xffff),HEX);
    if (client.connect(clientID.c_str(), mqtt_username, mqtt_password)) {
      Serial.println("connected");
      // // đăng ký nhận dữ liệu từ topic esp8266/Speed
      // client.subscribe("esp8266/speed");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}
/*------------------------Method for Publishing MQTT Messages----------------------------*/

void publishMessage(const char* topic, String payload, boolean retained){
  //payload.c_str() được sử dụng để truy cập mảng ký tự (c-string) chứa nội dung của chuỗi payload
  if(client.publish(topic,payload.c_str(),true))
    Serial.println("Message published ["+String(topic)+"]: "+payload);
}
 
void setup() {
  Serial.begin(115200); // Starts the serial communication
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT); // Sets the echoPin as an Input
  while(!Serial) delay(1);
  setup_wifi();
  // config hivemq
  espClient.setInsecure();
  // connect to server hiveMQ cloud
  client.setServer(mqtt_server, mqtt_port); 
}
void loop() {
  // wait until connect done 
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  // Clears the trigPin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);
  
  // Calculate the distance
  distanceCm = duration * SOUND_VELOCITY/2;
  Serial.println(distanceCm);
  if (distanceCm <= 3.0)
  {
    //---------------------------- publish data to hiveMQ --------------------------------------
    DynamicJsonDocument doc_speed(1024);
    doc_speed["speed"]=0;
    char mqtt_message_speed[128];
    serializeJson(doc_speed,mqtt_message_speed); // giá chị cho mqtt_message 
    publishMessage(mqtt_topic_speed,mqtt_message_speed,true);
    // delay(5000);
  }
  delay(1000);
}