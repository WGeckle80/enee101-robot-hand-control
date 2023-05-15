/*
 * Wyatt Geckle
 * 5/15/23
 *
 * Define the robot hand movements.
 *
 * The robot hand and original testing code was developed by Matthew
 * Schuyler.  Development was overseen by Dr. Romel Gomez.
 */


#include <Arduino.h>
#include <Adafruit_PWMServoDriver.h>

#include "robot_hand.hpp"


/*
 * Initialize object variables.
 */
RobotHand::RobotHand(Adafruit_PWMServoDriver *pwm)
{
    this->pwm = pwm;
    thumbOverlapFingers = false;
}

/*
 * Set the robot hand to display a decimal number in integer range
 * [0, 5].  Counting is done similar to how humans learn to count.
 */
void RobotHand::countDecimal(int number)
{
    // Set wrist flex and wrist turn to natural position.
    setPartPosition(ROBOT_WRISTFLEX, 0.5);
    setPartPosition(ROBOT_WRISTTURN, 0.5);

    if (thumbOverlapFingers)
    {
        setPartPosition(ROBOT_THUMB, 1.0);
        setPartPosition(ROBOT_INDEX, 1.0);
        setPartPosition(ROBOT_MIDDLE, 1.0);
        setPartPosition(ROBOT_RING, 1.0);
        setPartPosition(ROBOT_PINKY, 1.0);
    }
    else
    {
        setPartPosition(ROBOT_INDEX, 1.0);
        setPartPosition(ROBOT_MIDDLE, 1.0);
        setPartPosition(ROBOT_RING, 1.0);
        setPartPosition(ROBOT_PINKY, 1.0);
        setPartPosition(ROBOT_THUMB, 1.0);
    }

    delay(100);

    setPartPosition(ROBOT_INDEX, (float)(number >= 1));
    setPartPosition(ROBOT_MIDDLE, (float)(number >= 2));
    setPartPosition(ROBOT_RING, (float)(number >= 3));
    setPartPosition(ROBOT_PINKY, (float)(number >= 4));

    delay(100);

    setPartPosition(ROBOT_THUMB, (float)(number >= 5));

    thumbOverlapFingers = number < 4;
}

/*
 * Make the hand grab based on a percentage in the range [0, 1].
 * 0 corresponds to a straight hand, and 1 corresponds to a full
 * grab.
 */
void RobotHand::grab(float percent)
{
    setPartPosition(ROBOT_THUMB, 1.0 - percent);
    setPartPosition(ROBOT_INDEX, 1.0 - percent);
    setPartPosition(ROBOT_MIDDLE, 1.0 - percent);
    setPartPosition(ROBOT_RING, 1.0 - percent);
    setPartPosition(ROBOT_PINKY, 1.0 - percent);

    thumbOverlapFingers = false;
}

/*
 * Set robot hand to default position with delays.
 * Total delay time is ~2 seconds.
 *
 * NOTE: Initialize pwm module before calling this method.
 */
void RobotHand::init()
{
    setPartPosition(ROBOT_WRISTFLEX, 0.5);
    delay(500);

    setPartPosition(ROBOT_WRISTTURN, 0.5);
    delay(500);
    
    setPartPosition(ROBOT_THUMB, 0.5);
    setPartPosition(ROBOT_INDEX, 0.5);
    setPartPosition(ROBOT_MIDDLE, 0.5);
    setPartPosition(ROBOT_RING, 0.5);
    setPartPosition(ROBOT_PINKY, 0.5);

    delay(1000);
    
    thumbOverlapFingers = false;
}

/*
 * Set the robot hand to the default position.
 */
void RobotHand::setDefault()
{
    setPartPosition(ROBOT_WRISTFLEX, 0.5);
    setPartPosition(ROBOT_WRISTTURN, 0.5);
    setPartPosition(ROBOT_THUMB, 0.5);
    setPartPosition(ROBOT_INDEX, 0.5);
    setPartPosition(ROBOT_MIDDLE, 0.5);
    setPartPosition(ROBOT_RING, 0.5);
    setPartPosition(ROBOT_PINKY, 0.5);

    thumbOverlapFingers = false;
}

/*
 * Set a robot part to a straightened percentage in the range [0, 1].
 *
 * For a finger or thumb, a percentage of 0 corresponds to full
 * curling, and 1 corresponds to full straightening.
 *
 * For the wrist flex, a percentage of 0 corresponds to a full
 * flex backwards, and a percentage of 1 corresponds to a full
 * flex forwards.
 *
 * For the wrist turn, a percentage of 0 corresponds to the maximum
 * clockwise rotation, and a percentage of 1 corresponds to the
 * maximum counterclockwise rotation.
 *
 * The procedure is based on the testing code developed by Matthew
 * Schuyler.
 */
void RobotHand::setPartPosition(RobotPart part,
                                float percent)
{
    percent = max(0.0, min(percent, 1.0));  // Clip percent to bounds.

    // The index finger requires a +40 offset.
    if (part == ROBOT_INDEX)
    {
        int servoValue = percent >= 0.5
            ? MID_SERVO_VALUE
            + 2*(percent - 0.5)*(MAX_SERVO_VALUE - MID_SERVO_VALUE)
            : MIN_SERVO_VALUE + 2*percent*(MID_SERVO_VALUE - MIN_SERVO_VALUE);

        pwm->setPWM(part, 0, servoValue + 40);

        return;
    }

    // The ring and pinky movements are reversed.
    if (part == ROBOT_RING || part == ROBOT_PINKY)
    {
        int servoValue = percent >= 0.5
            ? MIN_SERVO_VALUE
            + 2*(percent - 0.5)*(MID_SERVO_VALUE - MIN_SERVO_VALUE)
            : MID_SERVO_VALUE + 2*(MAX_SERVO_VALUE - MID_SERVO_VALUE);

        pwm->setPWM(part, 0, servoValue);

        return;
    }

    // If the percentage is 0, set the servo to the minimum pwm value.
    // If the percentage is 1, set the servo to the maximum pwm value.
    // If the percentage is 0.5, set the servo to the middle pwm value.
    //
    // Since the difference between the minimum and middle values is
    // different from the difference between the middle and maximum
    // values, there must be two cases on how a change in percent
    // changes the servo value.
    int servoValue = percent >= 0.5
        ? MID_SERVO_VALUE
        + 2*(percent - 0.5)*(MAX_SERVO_VALUE - MID_SERVO_VALUE)
        : MIN_SERVO_VALUE + 2*percent*(MID_SERVO_VALUE - MIN_SERVO_VALUE);

    pwm->setPWM(part, 0, servoValue);
}

