#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <espnow.h>
#include <WiFiClientSecure.h>
#include <ArduinoJson.h>

// Config data station :
//  Ga Hà Nội
#define ID 1
#define Latitude 21.02439
#define Longitude 105.84122
// Ga Hải Dương
// #define ID 2
// #define Latitude 20.94663
// #define Longitude 106.33057
// Ga Hải Phòng
// #define ID 3
// #define Latitude 20.85596
// #define Longitude 106.68736

// flag config publish data 
bool flag_publish =false;
// data location publish 
float arr_Latitude[6]={21.02423241,
                      21.04902552,
                      21.04938853,
                      20.99465319,
                      20.98529548,
                      20.94769766
};
float arr_Longitude[6]={105.8409704,
                        105.8731988,
                        105.8919927,
                        105.9724607,
                        106.0382846,
                        106.3281004
};

/* ------------------------Wifi connnection Details-----------------------*/ 
// const char* ssid ="TTCH";
// const char* password = "ase123456";
const char* ssid ="Đồ Gỗ Đàm Dung";
const char* password = "01230123";

/*----------------MQTT Broker Connection Details-------------------------*/
const char* mqtt_server = "ae501b5ee3194ca682bd67e257459478.s1.eu.hivemq.cloud";
const char* mqtt_username = "RainWay System"; 
const char* mqtt_password = "012301230123aA#";
const int mqtt_port = 8883;
#define mqtt_topic_esp "esp8266/Location_esp"
#define mqtt_topic_location "esp8266/Location_data"
//--------------Setup wifi------------------------------------
WiFiClientSecure espClient;
PubSubClient client(espClient);

// PWM Setup: pin 3 
#define PWM_PIN 4
double maxvalue =2.55; 
#define RELAY_PIN 5 
// SENSOR PIN
#define SENSOR_PIN 2


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
      // đăng ký nhận dữ liệu từ topic esp8266/Speed
      client.subscribe("esp8266/speed");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}
/*--------------------Call back Method for Receiving MQTT massage------------------*/

void callback(char* topic, byte* payload, unsigned int length) {
  String incommingMessage = "";
  //-----receive data from MQTT Broker---
  for(int i=0; i<length;i++) incommingMessage += (char)payload[i];
  Serial.println("Massage arived ["+String(topic)+"]:"+incommingMessage);
  // quản lý cấu trúc dữ liệu JSON động 
  DynamicJsonDocument doc(100);
  // Check incomingMessage input doc  
  DeserializationError error = deserializeJson(doc, incommingMessage);
  if (error) {
    Serial.print("deserializeJson() failed: ");
    Serial.println(error.c_str());
    return;
  }
  //Transfer DynamicJsonDocument to JsonObject -> handle doc 
  JsonObject obj = doc.as<JsonObject>();
  // containskey: kiểm tra đối tượng out 1 có tồn tại hay không
  if(obj.containsKey("speed")){
    // receive data from obj 
    uint16_t val = obj["speed"];
    //PWM for pin 3 
    if(val==0){
      analogWrite(PWM_PIN,0*maxvalue);
      digitalWrite(RELAY_PIN,HIGH);
      // flag_status = false;
    }else if(val ==1 ){
      analogWrite(PWM_PIN,50*maxvalue);
      digitalWrite(RELAY_PIN,LOW);
      // flag_status = true;
    }else if(val ==2 ){
      analogWrite(PWM_PIN,75*maxvalue);
      digitalWrite(RELAY_PIN,LOW);
      // flag_status = true;
    }else if(val ==3 ){
      analogWrite(PWM_PIN,100*maxvalue);
      digitalWrite(RELAY_PIN,LOW);
      // flag_status = true;
    };
  }
}
/*------------------------Method for Publishing MQTT Messages----------------------------*/

void publishMessage(const char* topic, String payload, boolean retained) {
  //payload.c_str() được sử dụng để truy cập mảng ký tự (c-string) chứa nội dung của chuỗi payload
  if (client.publish(topic, payload.c_str(), true))
    Serial.println("Message published [" + String(topic) + "]: " + payload);
}
void setup() {
  pinMode(RELAY_PIN,OUTPUT);
  pinMode(SENSOR_PIN, INPUT);
  // put your setup code here, to run once:
  Serial.begin(115200);
  while(!Serial) delay(1);
  setup_wifi();
  espClient.setInsecure(); 
  // connect to server hiveMQ cloud
  client.setServer(mqtt_server, mqtt_port);
  //call while data receive from esp8266/Speed 
  client.setCallback(callback);
}

void loop() {
    // wait until connect done 
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  //---------------------------- publish data to hiveMQ --------------------------------------
  // function display - while receive data from orther esp
  // publishMessage(mqtt_topic,mqtt_message,true);
  // delay(5000);
  flag_publish=false;
  if (digitalRead(SENSOR_PIN) == 0) {
    DynamicJsonDocument doc(1024);
    doc["ID"] = ID;
    doc["Latitude"] = Latitude;
    doc["Longitude"] = Longitude;
    char mqtt_message[128];
    serializeJson(doc, mqtt_message);  // giá trị đại chỉ cho mqtt_message
    // while get data from sensor
    publishMessage(mqtt_topic_esp, mqtt_message, true);
    flag_publish = true; 
    DynamicJsonDocument doc_location(1024);
    doc_location["Latitude"] =Latitude;
    doc_location["Longitude"] =Longitude;
    char mqtt_message_location[128];
    serializeJson(doc_location, mqtt_message_location);  // assignt values for  mqtt_message_locatuon
    publishMessage(mqtt_topic_location, mqtt_message_location, true);
    delay(500);
  }
  if(flag_publish == true){
    for(int i=0;i<=5;i++)
    {
      DynamicJsonDocument doc_location(1024);
      doc_location["Latitude"] =arr_Latitude[i];
      doc_location["Longitude"] =arr_Longitude[i];
      char mqtt_message_location[128];
      serializeJson(doc_location, mqtt_message_location);  // gán giá trị địa chỉ cho  mqtt_message_locatuon
      publishMessage(mqtt_topic_location, mqtt_message_location, true);
      delay(1000);
    }
    flag_publish =false;
  }
}