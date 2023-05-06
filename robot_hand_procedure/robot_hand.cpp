/*
 * Wyatt Geckle
 * 5/6/23
 *
 * Define the robot hand movements.
 */


#include <Arduino.h>
#include <Adafruit_PWMServoDriver.h>

#include "robot_hand.hpp"


/*
 * Initialize object variables.
 */
RobotHand::RobotHand()
{
    Adafruit_PWMServoDriver pwm;

    // Initialize pwm; I do not have permission to publicly post
    // the code.

    this->pwm = &pwm;
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
 * Set the robot hand to the default position.  Be sure to do this each
 * time a new mode is engaged.
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
 */
void RobotHand::setPartPosition(RobotPart part,
                                float percent)
{
    // I currently do not have permission to publicly post this code.
    return;
}

