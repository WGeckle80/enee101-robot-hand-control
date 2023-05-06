/*
 * Wyatt Geckle
 * 5/6/23
 *
 * Define the robot hand movements.
 */


#include <Adafruit_PWMServoDriver.h>

#define MIN_SERVO_VALUE 150
#define MID_SERVO_VALUE 300
#define MAX_SERVO_VALUE 500

enum RobotPart {
    ROBOT_THUMB = 1,
    ROBOT_INDEX = 2,
    ROBOT_MIDDLE = 3,
    ROBOT_RING = 4,
    ROBOT_PINKY = 5,
    ROBOT_WRISTFLEX = 6,
    ROBOT_WRISTTURN = 7
};


class RobotHand
{
    private:
        Adafruit_PWMServoDriver *pwm;

        bool thumbOverlapFingers;

    public:
        RobotHand();

        void countDecimal(int number);

        void grab(float percent);

        void setDefault();

        void setPartPosition(RobotPart part,
                             float percent);
};

