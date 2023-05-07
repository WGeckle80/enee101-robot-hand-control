## Overview

The ENEE101 Spring 2023 class at the University of Maryland was tasked with
programming the most impressive procedure for a robot hand to follow.
The hand in question is driven by an Arduino Uno, and has the following
movement options:

* Curling of the thumb and each finger
* Flexing of the wrist back and fourth
* Turning of the wrist left and right

The rules were simple: no hardware modifications of the hand were allowed.
Everything else, including serial communication, was fair game.

My goal for this project was simple: control the hand using a game controller.
To accomplish this, I first turned to the Arduino procedures.  In essence,
the Arduino decides what to do, and to what intensity, based on serial input.
Then, I needed something on my computer to both process controller input and
send the associated serial information.  I chose Python along with the pygame
and pyserial APIs.  The Python program brings up a pygame window, processes
controller inputs on said window, and sends the appropriate serial information
to the Arduino.

I won the competition by a unanimous vote from the ENEE101 teaching team.
The code is provided in hopes that it may be useful to someone for their
own serial communication projects, or to encourage further developments
in future robotics competitions in ENEE101.


## Usage

Acquire the robot hand from Dr. Romel Gomez at UMD (with permission of course),
or build your own.  Unfortunately, build instructions are currently not
developed.  If tangible results aren't a requirement, or the Arduino code is
modified to work with your own project, then the minimum requirement is an
Arduino.

Clone the repository using

```sh
git clone https://github.com/WGeckle80/enee101-robot-hand-control.git
```

Upload the `robot_hand_procedure.ino` sketch from the `robot_hand_procedure`
directory to a target Arduino, and take note of its port name.

Install Python 3 and pip (if applicable), and install the required libraries
with the following terminal commands:

```sh
pip install -U pygame
pip install -U pyserial
```

In the terminal, run `robot_hand_control.py` in the `control` directory with
an extra command line parameter of the Arduino serial port name.
For example, on Linux with a serial port of `/dev/ttyACM0`,

```sh
python3 robot_hand_control.py /dev/ttyACM0
```


## Acknowledgements

The robot hand used for this competition was largely developed by Matthew
Schuyler, and overseen by Dr. Romel Gomez.  I would like to thank them
for developing the hand and putting on the competition.  Additionally,
I would like to thank the entire ENEE101 Spring 2023 teaching team,
with a special mention to my UTF, Emma Griffith.

