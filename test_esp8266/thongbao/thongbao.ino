#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <espnow.h>
#include <WiFiClientSecure.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <ArduinoJson.h>


/* ------------------------Wifi connnection Details-----------------------*/ 
const char* ssid ="TTCH";
const char* password = "ase123456";

/*----------------MQTT Broker Connection Details-------------------------*/
const char* mqtt_server = "ae501b5ee3194ca682bd67e257459478.s1.eu.hivemq.cloud";
const char* mqtt_username = "RainWay System"; 
const char* mqtt_password = "012301230123aA#";
const int mqtt_port = 8883;

//--------------Setup wifi------------------------------------
WiFiClientSecure espClient;
PubSubClient client(espClient);

// PWM Setup: pin 3 
#define PWM_PIN 4
double maxvalue =2.55;

// //Display Setup
// #define SCREEN_WIDTH 128  // OLED display width, in pixels
// #define SCREEN_HEIGHT 64  // OLED display height, in pixels
// // Declaration for an SSD1306 display connected to I2C (SDA, SCL pins)
// // The pins for I2C are defined by the Wire-library.
// // On an ESP8266:       D5 - 12(SDA), D6 - 14(SCL)
// #define OLED_RESET -1        // Reset pin # (or -1 if sharing Arduino reset pin)
// #define SCREEN_ADDRESS 0x3D  ///< See datasheet for Address; 0x3D for 128x64, 0x3C for 128x32
// //Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET); 

//Receive data from esp-now 
typedef struct struct_message {
    bool signal;
} struct_message;
static int count = 0;
struct_message myData;

/*---------------Callback function that will be executed when data is received -ESPNOW--------------*/
void OnDataRecv(uint8_t * mac, uint8_t *incomingData, uint8_t len) {
  memcpy(&myData, incomingData, sizeof(myData));
  Serial.print("Bytes received: ");
  Serial.println(len);
  Serial.print("Bool: ");
  Serial.println(myData.signal);
}

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
    }else if(val ==1 ){
      analogWrite(PWM_PIN,50*maxvalue);
    }else if(val ==2 ){
      analogWrite(PWM_PIN,75*maxvalue);
    }else if(val ==3 ){
      analogWrite(PWM_PIN,100*maxvalue);
    };
  }
}
/*------------------------Method for Publishing MQTT Messages----------------------------*/
void publishMessage(const char* topic, String payload, boolean retained){
  //payload.c_str() được sử dụng để truy cập mảng ký tự (c-string) chứa nội dung của chuỗi payload
  if(client.publish(topic,payload.c_str(),true))
    Serial.println("Message published ["+String(topic)+"]: "+payload);
}
void setup() {
  Serial.begin(112500);
  // //SSD1306_SWITCHCAPVCC = generate display voltage from 3.3V internally - config for DISPLAY
  // if (!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
  //    Serial.println(F("SSD1306 allocation failed"));
  //    for (;;); // Don't proceed, loop forever
  // }
  while(!Serial) delay(1);
  setup_wifi();
  espClient.setInsecure();
  // connect to server hiveMQ cloud
  client.setServer(mqtt_server, mqtt_port);
  //call while data receive from esp8266/Speed 
  client.setCallback(callback);
  // Set device as a Wi-Fi Station
  WiFi.mode(WIFI_STA);
  // Init ESP-NOW
  if (esp_now_init() != 0) {
    Serial.println("Error initializing ESP-NOW");
    return;
  };
  // Once ESPNow is successfully Init, we will register for recv CB to
  esp_now_set_self_role(ESP_NOW_ROLE_SLAVE);
  esp_now_register_recv_cb(OnDataRecv);
}

void loop() {

  // wait until connect done 
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  //------ Kết cấu : "Location": location_1------
  // String location_1 = "ga ha noi";
  // DynamicJsonDocument doc(1024);
  // doc["location"]=location_1;
  // char mqtt_message[128];
  // serializeJson(doc,mqtt_message); // giá chị cho mqtt_message 

  // function display - while receive data from orther esp 
  if (myData.signal) {
    count++;
    Display_screen_in_station(count);
    myData.signal =false;
  } else {
    if(count ==3){count =0;}
    Display_screen_in_railWay(count);
  };
}


void Display_screen_in_station(int count) {
  //    display.clearDisplay(); // Clear display buffer
  //    display.setTextSize(1);
  //    display.setCursor(5, 5);
  if (count == 1) {
    //      display.println("Da den ga Ha Noi");
    //      display.display();
    publishMessage("esp8266/location","Đã đến ga Hà Nội", true);
  } else if (count == 2) {
    //      display.println("Da den ga Hai Phong ");
    //      display.display(); 
    publishMessage("esp8266/location","Đã đến ga  Hai Phong", true);
  } else if (count == 3) {
    //      display.println("Da den ga Hai Duong ");
    //      display.display();
    publishMessage("esp8266/location","Đã đến ga  Hai Duong", true);
  };
  delay(2000);
}

void Display_screen_in_railWay(int count) {
  //    display.clearDisplay(); // Clear display buffer
  //    display.setTextSize(1);
  //    display.setCursor(5, 5);
  if (count == 1) {
    //      display.println("Huong Ha Noi - Hai Phong ");
    //      display.display();
    publishMessage("esp8266/location","Hướng Hà Nội - Hải Phòng ", true);
  } else if (count == 2) {
    //      display.println("Huong Hai Phong - Hai duong ");
    //      display.display();
    publishMessage("esp8266/location","Hướng Hải Phòng - Hải dương ", true);
  } else if (count == 0) {
    //      display.println("Huong Hai Duong - Ha Noi ");
    //      display.display();
    publishMessage("esp8266/location","Hướng Hải Dương - Hà Nội ", true);
  };
  delay(2000);
}
