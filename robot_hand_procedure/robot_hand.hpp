/*
 * Wyatt Geckle
 * 5/15/23
 *
 * Define the robot hand movements.
 *
 * The robot hand and original testing code was developed by Matthew
 * Schuyler.  Development was overseen by Dr. Romel Gomez.
 */


#include <Adafruit_PWMServoDriver.h>

#define MIN_SERVO_VALUE 150
#define MID_SERVO_VALUE 300
#define MAX_SERVO_VALUE 500

enum RobotPart {
    ROBOT_THUMB = 3,
    ROBOT_INDEX = 4,
    ROBOT_MIDDLE = 2,
    ROBOT_RING = 1,
    ROBOT_PINKY = 0,
    ROBOT_WRISTFLEX = 14,
    ROBOT_WRISTTURN = 15
};


class RobotHand
{
    private:
        Adafruit_PWMServoDriver *pwm;

        bool thumbOverlapFingers;

    public:
        RobotHand(Adafruit_PWMServoDriver *pwm);

        void countDecimal(int number);

        void grab(float percent);

        void init();

        void setDefault();

        void setPartPosition(RobotPart part,
                             float percent);
};

