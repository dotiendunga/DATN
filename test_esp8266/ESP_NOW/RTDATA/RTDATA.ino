#ifdef ESP8266
  #include <ESP8266WiFi.h>
  #include <espnow.h>
#else
  #include <WiFi.h>
  #include <esp_now.h>
#endif
// REPLACE WITH RECEIVER MAC Address: ID SLAVE
uint8_t broadcastAddress[] = {0X34,0X94,0X54,0X95,0XB2,0X3F};

#define SENSOR_PIN 4 
#define WAIT_PIN 5
#define TIME_DELAY 1000
typedef struct struct_message {
 bool signal;
} struct_message;

struct_message myData;
// Callback when data is sent
void OnDataSent(uint8_t *mac_addr, uint8_t sendStatus) {
  Serial.print("Last Packet Send Status: ");
  if (sendStatus == 0){
    Serial.println("Delivery success");
  }
  else{
    Serial.println("Delivery fail");
  }
}

 
void setup() {
  // Init Serial Monitor
  Serial.begin(115200);
  // Set device as a Wi-Fi Station
  WiFi.mode(WIFI_STA);

  // Init ESP-NOW
  if (esp_now_init() != 0) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }
  pinMode(SENSOR_PIN, INPUT);
  pinMode(WAIT_PIN,OUTPUT);
  // Once ESPNow is successfully Init, we will register for Send CB to
  // get the status of Trasnmitted packet
  esp_now_set_self_role(ESP_NOW_ROLE_CONTROLLER);
  // Khi một tin nhắn được gửi đi, hàm sẽ được gọi - hàm này trả về việc gửi có thành công hay không.
  esp_now_register_send_cb(OnDataSent);
  // Register peer
  esp_now_add_peer(broadcastAddress, ESP_NOW_ROLE_SLAVE, 1, NULL, 0);
}
 
void loop() {
   if (digitalRead(SENSOR_PIN) == 0) {
    digitalWrite(WAIT_PIN, LOW);
    myData.signal =true;
    // Send message via ESP-NOW
     esp_now_send(broadcastAddress, (uint8_t *) &myData, sizeof(myData));
  } else if (digitalRead(SENSOR_PIN) == 1) {
    digitalWrite(WAIT_PIN, HIGH);// khi không nhận được tín hiệu trả về
    // myData.signal =false;
    // // Send message via ESP-NOW
    //  esp_now_send(broadcastAddress, (uint8_t *) &myData, sizeof(myData));
  };
}