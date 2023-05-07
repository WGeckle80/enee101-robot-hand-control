#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Wyatt Geckle
# 5/6/23

"""Set the robot hand to be controlled by keyboard or controller input.

   If using a controller, an Xinput controller, such as an Xbox One
   Controller, is required.

   Control instructions are shown on the main Pygame window.

   The robot hand and original testing code was developed by Matthew
   Schuyler.  Development was overseen by Dr. Romel Gomez.

   Language and API versions tested:
     - Python 3.10.6
     - pygame 2.4.0
     - pyserial 3.5
"""


import sys

import serial

import pygame


def main():
    """The main program."""
    
    if len(sys.argv) < 2:
        sys.stderr.write("Missing robot hand serial port.  Exiting.\n")
        sys.exit(1)

    try:
        robot_hand = serial.Serial(sys.argv[1], 9600)
    except FileNotFoundError:
        sys.stderr.write("Invalid robot hand serial port.  Exiting.\n")
        sys.exit(1)
    except serial.SerialException:
        sys.stderr.write("Robot hand not responding.  Exiting.\n")
        sys.exit(1)


    pygame.init()
    screen = pygame.display.set_mode((900, 600))
    pygame.display.set_caption("Robot Hand Control")
    pygame.font.init()
    font = pygame.font.SysFont("Ubuntu", 24)
    clock = pygame.time.Clock()

    weak_text = font.render("Z Key or Left Trigger: Weaken Grab",
                            False, (255, 255, 255))
    stren_text = font.render("X Key or Right Trigger: Strengthen Grab",
                             False, (255, 255, 255))
    turn_text = font.render("Left/Right Keys or Left Stick: Wrist Turn",
                            False, (255, 255, 255))
    flex_text = font.render("Up/Down Keys or Right Stick: Wrist Flex",
                            False, (255, 255, 255))

    grab_serial = 127
    flex_serial = 127
    turn_serial = 127
    
    controller = None  # Controller is None if disconnected.

    # Wait for hand to initialize.
    while robot_hand.in_waiting == 0:
        clock.tick(30)
    
    # Get initialization message from hand.
    hand_text = font.render(robot_hand.read_until().decode()[:-1],
                            False, (255, 255, 255))

    try:
        while True:
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    robot_hand.close()
                    sys.exit()

            # Allow controller to disconnect and reconnect throughout
            # runtime.
            if controller is None and pygame.joystick.get_count() > 0:
                controller = pygame.joystick.Joystick(0)
            elif controller is not None and pygame.joystick.get_count() == 0:
                controller.quit()
                controller = None
            

            send_keyboard_grab = True
            send_keyboard_flex = True
            send_keyboard_turn = True

            if controller is not None:
                # Strengthen grab with right trigger, weaken it with left
                # trigger.
                grab_stren_val = controller.get_axis(5)
                grab_weak_val = controller.get_axis(2)
                
                # Flex the hand with the right stick's vertical axis.
                flex_val = controller.get_axis(4)

                # Turn the hand with the left stick's horizontal axis.
                turn_val = controller.get_axis(0)

                # If right trigger pressed, increase grab up to 255.
                # Else if left trigger pressed, decrease grab down to 0.
                if grab_stren_val > -0.90:
                    grab_serial = min(int(grab_serial
                                          + 3*(grab_stren_val + 1)), 255)
                    send_keyboard_grab = False
                elif grab_weak_val > -0.90:
                    grab_serial = max(0, int(grab_serial
                                             - 3*(grab_weak_val + 1)))
                    send_keyboard_grab = False

                # If right analog down, increase flex up to a max of
                # 255.  Else if right analog up, decrease flex down to
                # a min of 0.
                if abs(flex_val) >= 0.2:
                    flex_serial = max(0, min(int(flex_serial + 6*flex_val),
                                             255))
                    send_keyboard_flex = False
                
                # If left analog right, increase turn up to a max of
                # 255.  Else if left analog left, decrease turn down
                # to a min of 0.
                if abs(turn_val) >= 0.2:
                    turn_serial = max(0, min(int(turn_serial + 6*turn_val),
                                             255))
                    send_keyboard_turn = False

            
            # If not sending controller input (controller is either
            # not connected, or analog inputs are at neutral values),
            # send keyboard input.
            
            # Strengthen grab with X key, weaken it with Z key.
            if send_keyboard_grab:
                grab_serial = max(0, min(grab_serial + 6*(
                    keys[pygame.K_x] - keys[pygame.K_z]), 255))

            # Flex the hand with up and down keys.
            if send_keyboard_flex:
                flex_serial = max(0, min(flex_serial + 6*(
                    keys[pygame.K_DOWN] - keys[pygame.K_UP]), 255))

            # Turn the hand with the left and right keys.
            if send_keyboard_turn:
                turn_serial = max(0, min(turn_serial + 6*(
                    keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]), 255))


            # Write 6 bytes for grab, flex, and turn values of hand.
            robot_hand.write(bytes([0x19, grab_serial,
                                    0x16, flex_serial,
                                    0x17, turn_serial]))

            # Allow robot hand text to display on screen.
            if robot_hand.in_waiting > 0:
                hand_text = font.render(robot_hand.read_until().decode()[:-1],
                                        False, (255, 255, 255))


            # Reset the screen and draw text each tick.
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 0, 900, 600))
            screen.blit(weak_text, (0, 10))
            screen.blit(stren_text, (0, 35))
            screen.blit(turn_text, (0, 60))
            screen.blit(flex_text, (0, 85))
            screen.blit(hand_text, (0, 500))

            pygame.display.update()
            clock.tick(30)  # Update robot every 30th of a second.

    except KeyboardInterrupt:
        robot_hand.close()
        sys.exit()
    except OSError:
        sys.stderr.write("The robot hand disconnected.  Exiting.\n")
        robot_hand.close()
        sys.exit(1)


if __name__ == "__main__":
    main()

