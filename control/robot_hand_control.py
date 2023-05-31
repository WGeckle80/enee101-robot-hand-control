# -*- coding: utf-8 -*-

# Wyatt Geckle
# 5/30/23

"""Set the robot hand to be controlled by keyboard or controller input.

   If using a controller, the default configuration uses the Linux
   interpretation of Xinput controllers.  Check config.ini for the
   default controls.

   The robot hand and original testing code was developed by Matthew
   Schuyler.  Development was overseen by Dr. Romel Gomez.

   Language and API versions tested:
     - pygame-ce 2.2.1
     - pyserial 3.5
     - Python 3.10.6
     - SDL 2.26.4
"""


import configparser
import os
import sys

import pygame

import serial


def get_joystick_input(
        joystick: pygame.joystick.Joystick,
        input_num: int, input_mask: int) -> float:
    """Returns joystick input percentage given input number and
    selector.
    
    Args:
        joystick: Initialized pygame joystick object.
        input_num: The number of the desired input type.
        input_mask: A bitmask selection of the desired input.  It
            should have the following properties:
                - 5th bit is 1 if using axis.
                - 4th bit is 1 if using negative axis/hat.
                - 3rd bit is 1 if using positive axis/hat.
                - 2nd bit is 1 if using hat.
                - 1st and 0th bits are binary count of hat combinations:
                    00 -> left
                    01 -> right
                    10 -> down
                    11 -> up

    Returns:
        Joystick input percentage in range [0, 1].
    """

    if joystick is None:
        return 0.0;

    if (input_mask & 0b100000
            and input_num < joystick.get_numaxes()):
        if input_mask & 0b001000:
            # Positive axis: get value when in [0, 1].
            return max(0, joystick.get_axis(input_num))
        elif input_mask & 0b010000:
            # Negative axis: get value when in [-1, 0].
            return -min(joystick.get_axis(input_num), 0)
        else:
            # Entire axis: set value in range [0, 1].
            return 0.5*joystick.get_axis(input_num) + 0.5
    elif (input_mask & 0b000100
            and input_num < joystick.get_numhats()):
        if input_mask == 0b000111:
            # Up: get second hat coordinate.
            return joystick.get_hat(input_num)[1] == 1
        elif input_mask & 0b000010:
            # Down: get negative of second hat coordinate.
            return joystick.get_hat(input_num)[1] == -1
        elif input_mask & 0b000001:
            # Right: get first hat coordinate.
            return joystick.get_hat(input_num)[0] == 1
        else:
            # Left: get negative of first hat coordinate.
            return joystick.get_hat(input_num)[0] == -1
    elif input_num < joystick.get_numbuttons():
        return joystick.get_button(input_num)
    else:
        return 0.0
    

def joystick_input(joy_input: str, input_name: str = "") -> (int, int):
    """Returns joystick input given a config string.
    
    Args:
        joy_input: String from configuration file.
            Example formats: "axis3+", "axis5", "hat0left", "button6".

    Returns:
        Input index.
        Bitmask with the following properties:
            - 5th bit is 1 if using axis.
            - 4th bit is 1 if using negative axis/hat.
            - 3rd bit is 1 if using positive axis/hat.
            - 2nd bit is 1 if using hat.
            - 1st and 0th bits are binary count of hat combinations:
                00 -> left
                01 -> right
                10 -> down
                11 -> up

    Raises:
        ValueError: If the config string input is invalid.
    """

    joy_input = joy_input.lower()  # Allow variable case in config.
    input_num = -1  # input_num remains -1 if not properly set.
    input_mask = 0b000000

    try:
        if joy_input.startswith("axis"):
            if joy_input[-1] == '-':
                input_num = int(joy_input[4:-1])
                input_mask = 0b110000
            elif joy_input[-1] == '+':
                input_num = int(joy_input[4:-1])
                input_mask = 0b101000
            else:
                input_num = int(joy_input[4:])
                input_mask = 0b100000
        elif joy_input.startswith("hat"):
            if joy_input.endswith("left"):
                input_num_str = joy_input[3:-4]
                input_mask = 0b000100
            elif joy_input.endswith("right"):
                input_num_str = joy_input[3:-5]
                input_mask = 0b000101
            elif joy_input.endswith("down"):
                input_num_str = joy_input[3:-4]
                input_mask = 0b000110
            elif joy_input.endswith("up"):
                input_num_str = joy_input[3:-2]
                input_mask = 0b000111
            else:
                input_num_str = "INVALID"
            
            # Most modern controllers only have 1 hat.  If the hat
            # number is not supplied, use hat0.
            if input_num_str:
                input_num = int(input_num_str)
            else:
                input_num = 0
        elif joy_input.startswith("button"):
            input_num = int(joy_input[6:])
    except ValueError:
        if input_name:
            raise ValueError(f"{input_name} controller input invalid.")
        else:
            raise ValueError("Controller input invalid.")

    # input_num was not properly set, so ValueError must be raised.
    if input_num == -1:
        if input_name:
            raise ValueError(f"{input_name} controller input invalid.")
        else:
            raise ValueError("Controller input invalid.")

    return input_num, input_mask


def main():
    """The main program."""

    pygame.init()

    config = configparser.ConfigParser()
    if os.path.isfile("config.ini"):
        config.read("config.ini")

        try:
            key_grab = pygame.key.key_code(
                config.get("Keyboard", "Grab"))
        except ValueError:
            sys.stderr.write("Grab keyboard key invalid.  Exiting.\n")
            pygame.quit()
            sys.exit(1)

        try:
            key_release = pygame.key.key_code(
                config.get("Keyboard", "Release"))
        except ValueError:
            sys.stderr.write("Release keyboard key invalid.  Exiting.\n")
            pygame.quit()
            sys.exit(1)

        try:
            key_forward = pygame.key.key_code(
                config.get("Keyboard", "Flex_Forward"))
        except ValueError:
            sys.stderr.write("Forward keyboard key invalid.  Exiting.\n")
            pygame.quit()
            sys.exit(1)

        try:
            key_backward = pygame.key.key_code(
                config.get("Keyboard", "Flex_Backward"))
        except ValueError:
            sys.stderr.write("Backward keyboard key invalid.  Exiting.\n")
            pygame.quit()
            sys.exit(1)

        try:
            key_left = pygame.key.key_code(
                config.get("Keyboard", "Turn_Left"))
        except ValueError:
            sys.stderr.write("Left keyboard key invalid.  Exiting.\n")
            pygame.quit()
            sys.exit(1)

        try:
            key_right = pygame.key.key_code(
                config.get("Keyboard", "Turn_Right"))
        except ValueError:
            sys.stderr.write("Right keyboard key invalid.  Exiting.\n")
            pygame.quit()
            sys.exit(1)

        try:
            joy_grab, joy_grab_mask= joystick_input(
                config.get("Joystick", "Grab").lower(), "Grab")
            joy_release, joy_release_mask = joystick_input(
                config.get("Joystick", "Release").lower(), "Release")
            joy_forward, joy_forward_mask = joystick_input(
                config.get("Joystick", "Flex_Forward").lower(), "Forward")
            joy_backward, joy_backward_mask = joystick_input(
                config.get("Joystick", "Flex_Backward").lower(), "Backward")
            joy_left, joy_left_mask = joystick_input(
                config.get("Joystick", "Turn_Left").lower(), "Left")
            joy_right, joy_right_mask = joystick_input(
                config.get("Joystick", "Turn_Right").lower(), "Right")
        except ValueError as e:
            sys.stderr.write(f"{str(e)}  Exiting.\n")
            pygame.quit()
            sys.exit(1)
    else:
        config.add_section("Keyboard")
        config.set("Keyboard", "Grab", "x")
        config.set("Keyboard", "Release", "z")
        config.set("Keyboard", "Flex_Forward", "down")
        config.set("Keyboard", "Flex_Backward", "up")
        config.set("Keyboard", "Turn_Left", "left")
        config.set("Keyboard", "Turn_Right", "right")

        config.add_section("Joystick")
        config.set("Joystick", "Grab", "axis5")
        config.set("Joystick", "Release", "axis2")
        config.set("Joystick", "Flex_Forward", "axis4+")
        config.set("Joystick", "Flex_Backward", "axis4-")
        config.set("Joystick", "Turn_Left", "axis0-")
        config.set("Joystick", "Turn_Right", "axis0+")

        with open("config.ini", "w") as file:
            file.write("""; Robot Hand Control Configuration File
;
; For each of the keyboard values, type in the base character of the
; desired key (e.g. return, a, ;).
;
; For each of the joystick values, write it in the following format
; (without quotes): "[input type][input index][input direction]",
; where [input type] is either "axis", "hat", or "button",
; [input index] is the zero-indexed index of the input, and
; [input direction] specifies the direction of an axis or hat if
; applicable.  Some examples of valid joystick values include:
;     - axis0
;     - axis2-
;     - hat0up
;     - button5
;
; The default controls are as follows (using Xbox One controller as
; joystick):
;
;     Action     | Keyboard |     Joystick
; ---------------|----------|------------------
;  Grab          | X        | Right Trigger
;  Release       | Z        | Left Trigger
;  Flex Forward  | Down     | Right Stick Down
;  Flex Backward | Up       | Right Stick Up
;  Turn Left     | Left     | Left Stick Left
;  Turn Right    | Right    | Left Stick Right
;
; * Default joystick inputs are based on the Linux interpretatation
;   of Xinput controllers.


""")
            config.write(file)

        # Set default keyboard keys.
        key_grab = pygame.K_x
        key_release = pygame.K_z
        key_forward = pygame.K_DOWN
        key_backward = pygame.K_UP
        key_left = pygame.K_LEFT
        key_right = pygame.K_RIGHT

        # Set default joystick inputs
        joy_grab, joy_grab_mask = joystick_input("axis5")
        joy_release, joy_release_mask = joystick_input("axis2")
        joy_forward, joy_forward_mask = joystick_input("axis4+")
        joy_backward, joy_backward_mask = joystick_input("axis4-")
        joy_left, joy_left_mask = joystick_input("axis0-")
        joy_right, joy_right_mask = joystick_input("axis0+")


    # If robot hand serial port not provided, program is in simple mode.
    if len(sys.argv) >= 2:
        try:
            robot_hand = serial.Serial(sys.argv[1], 9600, timeout=5)
        except FileNotFoundError:
            sys.stderr.write("Invalid robot hand serial port.  Exiting.\n")
            pygame.quit()
            sys.exit(1)
        except serial.SerialException:
            sys.stderr.write("Incorrect robot hand serial port.  Exiting.\n")
            pygame.quit()
            sys.exit(1)
        
        # Get initialization message from hand.
        init_message = robot_hand.read_until().decode()[:-2]
        if not init_message:
            sys.stderr.write("Robot hand not responding.  Exiting.\n")
            pygame.quit()
            sys.exit(1)
    else:
        print("Missing robot hand serial port.  Entering joystick demo mode.")

        robot_hand = None  # If in simple mode, robot_hand is None.
        init_message = ""

    screen = pygame.display.set_mode((900, 600))
    if robot_hand is None:
        pygame.display.set_caption("Robot Hand Control (Simple Mode)")
    else:
        pygame.display.set_caption("Robot Hand Control")
    pygame.font.init()
    font = pygame.font.SysFont("Ubuntu", 24)
    clock = pygame.time.Clock()

    grab_serial = 127
    flex_serial = 127
    turn_serial = 127
    
    joystick = None  # joystick is None if disconnected.
    
    hand_text = font.render(init_message,
                            False, (255, 255, 255))

    try:
        while True:
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    if robot_hand is not None:
                        robot_hand.close()
                    sys.exit()

            # Allow controller to disconnect and reconnect throughout
            # runtime.
            if joystick is None and pygame.joystick.get_count() > 0:
                joystick = pygame.joystick.Joystick(0)
            elif joystick is not None and pygame.joystick.get_count() == 0:
                joystick.quit()
                joystick = None
            

            send_keyboard_grab = True
            send_keyboard_flex = True
            send_keyboard_turn = True

            if joystick is not None:
                # For each attribute value, set the positive input
                # value and subtract off the negative input value.
                grab_val = (get_joystick_input(joystick,
                                               joy_grab,
                                               joy_grab_mask)
                            - get_joystick_input(joystick,
                                                 joy_release,
                                                 joy_release_mask))
                flex_val = (get_joystick_input(joystick,
                                               joy_forward,
                                               joy_forward_mask)
                            - get_joystick_input(joystick,
                                                 joy_backward,
                                                 joy_backward_mask))
                turn_val = (get_joystick_input(joystick,
                                               joy_right,
                                               joy_right_mask)
                            - get_joystick_input(joystick,
                                                 joy_left,
                                                 joy_left_mask))

                # If grab input pressed, increase grab up to 255.
                # Otherwise, if release input pressed, decrease grab
                # down to 0.
                if abs(grab_val) >= 0.15:
                    grab_serial = max(0, min(int(grab_serial + 6*grab_val),
                                             255))
                    send_keyboard_grab = False

                # If flex forward activated, increase flex up to a max of
                # 255.  Else if flex backward activated, decrease flex down to
                # a min of 0.
                if abs(flex_val) >= 0.15:
                    flex_serial = max(0, min(int(flex_serial + 6*flex_val),
                                             255))
                    send_keyboard_flex = False
                
                # If turn right activated, increase turn up to a max of
                # 255.  Else if turn left activated, decrease turn down
                # to a min of 0.
                if abs(turn_val) >= 0.15:
                    turn_serial = max(0, min(int(turn_serial + 6*turn_val),
                                             255))
                    send_keyboard_turn = False

            
            # If not sending controller input (controller is either
            # not connected, or analog inputs are at neutral values),
            # send keyboard input.
            if send_keyboard_grab:
                grab_serial = max(0, min(grab_serial + 6*(
                    keys[key_grab] - keys[key_release]), 255))
            if send_keyboard_flex:
                flex_serial = max(0, min(flex_serial + 6*(
                    keys[key_forward] - keys[key_backward]), 255))

            # Turn the hand with the left and right keys.
            if send_keyboard_turn:
                turn_serial = max(0, min(turn_serial + 6*(
                    keys[key_right] - keys[key_left]), 255))


            # Write 6 bytes for grab, flex, and turn values of hand.
            if robot_hand is not None:
                robot_hand.write(bytes([0x19, grab_serial,
                                        0x16, flex_serial,
                                        0x17, turn_serial]))

            # Allow robot hand text to display on screen.
            if robot_hand is not None and robot_hand.in_waiting > 0:
                hand_text = font.render(robot_hand.read_until().decode()[:-2],
                                        False, (255, 255, 255))

            # Reset the screen and draw text each tick.
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 0, 900, 600))
            screen.blit(font.render(f"Grab: {100 * grab_serial / 255:.0f}%",
                                    False, (255, 255, 255)),
                        (0, 10))
            screen.blit(font.render(f"Flex: {100 * flex_serial / 255:.0f}%",
                                    False, (255, 255, 255)),
                        (0, 35))
            screen.blit(font.render(f"Turn: {100 * turn_serial / 255:.0f}%",
                                    False, (255, 255, 255)),
                        (0, 60))
            screen.blit(hand_text, (0, 500))

            pygame.display.update()
            clock.tick(30)  # Update robot every 30th of a second.

    except KeyboardInterrupt:
        if robot_hand is not None:
            robot_hand.close()
        sys.exit()
    except OSError:
        sys.stderr.write("The robot hand disconnected.  Exiting.\n")
        if robot_hand is not None:
            robot_hand.close()
        sys.exit(1)


if __name__ == "__main__":
    main()

