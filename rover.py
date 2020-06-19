""" rover.py

The Rover class can be used for a simple rover build with an LEGO EV3-brick
with two motors. This class is used in the sample program linetracker.py,
part of the tutorial how to use Pixy2 on Pybricks.


Author  : Kees Smit
Date    : June 16 2020
Version : 1.00
License : 
"""
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port


SPEED_FAST = 0 # 400
SPEED_SLOW = 150


class Rover:
    def __init__(self):
        """ Initialization of Rover."""
        # Constants
        self._GAIN = 10
        self._speed = SPEED_FAST

        # Initialize the EV3 brick
        self.ev3 = EV3Brick()

        # Initialize the motors
        self.left_motor = Motor(Port.B)
        self.right_motor = Motor(Port.C)

    def move(self, speed):
        speed *= self._GAIN
        speed_left = limit_speed(self._speed - speed)
        speed_right = limit_speed(self._speed + speed)
        self.left_motor.run(speed_left)
        self.right_motor.run(speed_right)

    def move_slow(self):
        """ Set initial speed to SPEED_SLOW."""
        self._speed = SPEED_SLOW

    def move_fast(self):
        """ Set initial speed to SPEED_FAST."""
        self._speed = SPEED_FAST

    def stop(self):
        self.left_motor.stop()
        self.right_motor.stop()


def limit_speed(speed):
    """Limit speed in range [-900,900]."""
    if speed > 900:
        speed = 900
    elif speed < -900:
        speed = -900
    return speed
