#include <Arduino.h>
#include <WiFi.h>
#include <ESP32QRCodeReader.h>
#include <Servo.h>

#ifndef STR_IMP
#include <string.h>
#define STR_IMP
#endif
#include <FS.h>
#include <SD_MMC.h>

int pos;
String command;
char buf[10];
const char *ssid = "EZ";
const char *password = "lgll7056";
const char *server_ip = "192.168.43.36";
const uint16_t command_port = 8080;
WiFiClient wfc;
const int servo_gpio = 12;
Servo drop;
const char *INITIAL_POSITION = "0X0";
char current_position[4];
char current_direction;
char INITIAL_DIRECTION = 'U';
int SERVO_DROP_POSITION = 90;
int SERVO_UNDROP_POSITION = 0;
const char *ack = "R01";
ESP32QRCodeReader reader(CAMERA_MODEL_AI_THINKER);

char classifyReceviedMessage(char *input)
{
  if (input[2] == '1')
  {
    //Move
    return 'm';
  }
  else if (input[2] == '2')
  { //Drop
    return 'd';
  }
  else if (input[2] == '6')
  { //Rotate
    return 'r';
  }
  return 'u';
}

void setup()
{
  pinMode(33, OUTPUT);
  digitalWrite(33, HIGH);
  SD_MMC.begin("/sdcard", true);
  // Configure Wi-Fi information
  //pinMode(33, OUTPUT);
  reader.setup();
  reader.begin();
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(200);
  }
  while (!wfc.connect(server_ip, command_port))
  {
    delay(200);
  }
  //generateConnectMessage(buf, INITIAL_POSITION, INITIAL_DIRECTION);
  wfc.print("R000X0U");
  while (!(wfc.available() > 0))
  {

    delay(500);
  }

  command = wfc.readStringUntil('\n');

  command.toCharArray(buf, 10);
  // now buf contains the ack message

  // Configure UART parameters
  Serial.begin(9600);
  Serial.write("CS2\n");
  delay(1000);
  Serial.write("CT835\n");
  delay(1000);
  Serial.write("CG1450\n");
  delay(1000);
  current_direction = INITIAL_DIRECTION;

  // Camera initialization
  strcpy(current_position, INITIAL_POSITION);
  //reader.setup();

  // SERVO init
  //set the drop mechanism to the initial position
  // Other parts of the setup
}

void loop()
{
  if (!(wfc.available() > 0))
  {
    delay(500);
  }
  else
  {
    command = wfc.readStringUntil('\n');

    // Here we can expect either move,rotate, position or drop

    command.toCharArray(buf, 10);
    char kind = classifyReceviedMessage(buf);
    if (kind == 'm')
    {
      char new_direction = buf[3];
      if (new_direction != current_direction)
      {
        if (new_direction == 'L')
          Serial.write("RL\n");
        else if (new_direction == 'R')
        {
          Serial.write("RR\n");
        }
        else
        {
          Serial.write("RB\n");
        }
      }
      Serial.write("MF\n");
      delay(5000);
      wfc.write(ack);
      struct QRCodeData qrCodeData;
      int flag = 0;

      while (flag == 0)
      {
        //digitalWrite(33, LOW);
        delay(500);
        if (reader.receiveQrCode(&qrCodeData, 100))
        {
          if (qrCodeData.valid)
          {
            const char *new_position = (const char *)qrCodeData.payload;
            if (new_position[0] != current_position[0] || new_position[1] != current_position[1] || new_position[2] != current_position[2])
            {
              digitalWrite(33, LOW);
              delay(500);
              strcpy(current_position, new_position);
              digitalWrite(33, HIGH);
              flag = 1;
            }
          }
          else
          {
            delay(100);
          }
        }
        //digitalWrite(33, HIGH);
      }
      strcpy(buf, "R02");
      strcat(buf, current_position);

      wfc.write(buf);
      command = wfc.readStringUntil('\n');
      //confirm that it is an ack
    }
    else if (kind == 'r')
    {
      char new_direction = buf[3];
      if (new_direction != current_direction)
      {
        if (new_direction == 'L')
          Serial.write("RL\n");
        else if (new_direction == 'R')
        {
          Serial.write("RR\n");
        }
        else
        {
          Serial.write("RB\n");
        }
      }
      wfc.write(ack);
    }
    else if (kind == 'd')
    {
      drop.attach(0);

      pos = SERVO_UNDROP_POSITION;
      for (pos = SERVO_UNDROP_POSITION; pos <= SERVO_DROP_POSITION; pos += 1)
      {
        drop.write(pos);
        delay(15);
      }
      for (pos = SERVO_DROP_POSITION; pos >= SERVO_UNDROP_POSITION; pos -= 1)
      {
        drop.write(pos);
        delay(15);
      }
      drop.detach();
      wfc.write(ack);
    }

    else
    {
      delay(100);
    }
  }
}