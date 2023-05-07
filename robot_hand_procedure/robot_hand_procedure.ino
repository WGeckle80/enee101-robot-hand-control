/*
 * Wyatt Geckle
 * 5/6/23
 *
 * Define the procedure for the robot hand.
 *
 * The robot hand and original testing code was developed by Matthew
 * Schuyler.  Development was overseen by Dr. Romel Gomez.
 */


#include <Wire.h>

#include "robot_hand.hpp"


RobotHand robotHand;

unsigned char serialBuffer[6];


void setup()
{
    Serial.begin(9600);

    robotHand.setDefault();

    delay(2000);

    pinMode(13, OUTPUT);

    Serial.println("Mr. Hand is ready.");
}

void loop()
{
    // A proper serial command has a byte for the command, and if
    // applicable, a byte for the argument.  Read 6 bytes at a time
    // due to the 3 positions that are required to control the hand.
    if (Serial.available())
    {
        Serial.readBytes(serialBuffer, 6);

        for (int i = 0; i < 6; i += 2)
        {
            unsigned char function = serialBuffer[i];
            unsigned char argument = serialBuffer[i + 1];

            switch (function)
            {
                case 0x10:
                    robotHand.setDefault();
                    break;
                case 0x11:
                    robotHand.setPartPosition(ROBOT_THUMB,
                                              (float)argument / 255.0);
                    break;
                case 0x12:
                    robotHand.setPartPosition(ROBOT_INDEX,
                                              (float)argument / 255.0);
                    break;
                case 0x13:
                    robotHand.setPartPosition(ROBOT_MIDDLE,
                                              (float)argument / 255.0);
                    break;
                case 0x14:
                    robotHand.setPartPosition(ROBOT_RING,
                                              (float)argument / 255.0);
                    break;
                case 0x15:
                    robotHand.setPartPosition(ROBOT_PINKY,
                                              (float)argument / 255.0);
                    break;
                case 0x16:
                    robotHand.setPartPosition(ROBOT_WRISTFLEX,
                                              (float)argument / 255.0);
                    break;
                case 0x17:
                    robotHand.setPartPosition(ROBOT_WRISTTURN,
                                              (float)argument / 255.0);
                    break;
                case 0x18:
                    robotHand.countDecimal(argument);
                    break;
                case 0x19:
                    robotHand.grab((float)argument / 255.0);
                    digitalWrite(13, argument > 127);
                    break;
            }
        }
    }
}

