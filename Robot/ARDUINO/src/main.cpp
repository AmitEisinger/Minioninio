#include <Arduino.h>
#define STEP_MOTOR_1_OUTPUT 2
#define STEP_MOTOR_2_OUTPUT 3
#define DIR_MOTOR_1_OUTPUT 5
#define DIR_MOTOR_2_OUTPUT 6

int GO_STEPS = 1973;
//#define GO_STEPS 1973
//1000 gives ~10.25 cm
// our board is 30 on 30 so we need 30 cm which are ~2926
//#define TURN_STEPS 850
int TURN_STEPS = 850;

int STEP_DELAY = 2;
#define FWD HIGH
#define REV LOW
void makeOneStep()
{
  digitalWrite(STEP_MOTOR_2_OUTPUT, HIGH);
  digitalWrite(STEP_MOTOR_1_OUTPUT, HIGH);
  delay(STEP_DELAY);
  digitalWrite(STEP_MOTOR_2_OUTPUT, LOW);
  digitalWrite(STEP_MOTOR_1_OUTPUT, LOW);
  delay(STEP_DELAY);
}

void goForward()
{
  digitalWrite(DIR_MOTOR_2_OUTPUT, FWD); //change direction to "forward"
  digitalWrite(DIR_MOTOR_1_OUTPUT, FWD); //change direction to "forward"
  for (int i = 0; i < GO_STEPS; i++)
    makeOneStep();
}

void goBackwards()
{
  digitalWrite(DIR_MOTOR_2_OUTPUT, REV); //change direction to "reverse"
  digitalWrite(DIR_MOTOR_1_OUTPUT, REV); //change direction to "reverse"
  for (int i = 0; i < GO_STEPS; i++)
    makeOneStep();
}

void turnRight()
{
  digitalWrite(DIR_MOTOR_2_OUTPUT, REV); //change direction to "reverse"
  digitalWrite(DIR_MOTOR_1_OUTPUT, FWD); //change direction to "forward"
  for (int i = 0; i < TURN_STEPS; i++)
    makeOneStep();
}

void turnLeft()
{
  digitalWrite(DIR_MOTOR_2_OUTPUT, FWD); //change direction to "forward"
  digitalWrite(DIR_MOTOR_1_OUTPUT, REV); //change direction to "reverse"
  for (int i = 0; i < TURN_STEPS; i++)
    makeOneStep();
}

void setup()
{
  // put your setup code here, to run once:
  pinMode(STEP_MOTOR_1_OUTPUT, OUTPUT); //STEP motor 1
  pinMode(STEP_MOTOR_2_OUTPUT, OUTPUT); //STEP motor 2
  pinMode(8, OUTPUT);                   //enable pin for all motors -- must be LOW. set to HIGH to release the motors (no power use)

  pinMode(DIR_MOTOR_1_OUTPUT, OUTPUT);
  digitalWrite(DIR_MOTOR_1_OUTPUT, LOW); // DIR motor 1
  pinMode(DIR_MOTOR_2_OUTPUT, OUTPUT);
  digitalWrite(DIR_MOTOR_2_OUTPUT, LOW); // DIR motor 2
  Serial.begin(9600);
}

void loop()
{
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0)
  {
    String command = Serial.readStringUntil('\n');
    char buf[10];
    command.toCharArray(buf, 10);
    digitalWrite(8, LOW); //enable pin for all motors must be LOW
    switch (buf[0])
    {
    case 'R':
      if (buf[1] == 'R')
      {
        turnRight();
      }
      else if (buf[1] == 'L')
      {
        turnLeft();
      }
      else if (buf[1] == 'B')
      {
        turnLeft();
        turnLeft();
      }
      break;
    case 'M':
      if (buf[1] == 'F')
      {
        goForward();
      }
      else if (buf[1] == 'R')
      {
        goBackwards();
      }
      break;
    case 'C':
      if (buf[1] == 'S')
      {
        STEP_DELAY = atoi(&(buf[2]));
      }
      else if (buf[1] == 'T')
      {
        TURN_STEPS = atoi(&(buf[2]));
      }
      else if (buf[1] == 'G')
      {
        GO_STEPS = atoi(&(buf[2]));
      }
      break;
    }
    digitalWrite(8, HIGH);
  }
  else
  {
    delay(500);
  }
}