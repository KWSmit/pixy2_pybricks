#!/usr/bin/env pybricks-micropython
""" chaser.py

Demo program for using Pixy2 on PyBricks: let your robotrover
follow an object.

Usage: On Pixy2 set sig1 for an object. See manual of Pixy2 how to do this.
       In Pixy2's configuration window set the interface to I2C and 
       I2C address to 0x54. If you choose to use a different I2C address, 
       change the value in the code of this file (line 49).

       Build a robot with two motors (port B and C) and Pixy2 camera (port S1).
       If you use different ports, adjust the code in this file 
       (lines 47, 48 and 49).
       
       Start chaser.py and your robot will follow the oject of sig1.
       Push any button on the EV3-brick to stop the program.

See https://docs.pixycam.com for more inforamation about Pixy2.
See https://docs.pybricks.com how to run programs on Pybricks.


Author  : Kees Smit
Date    : June 16 2020
Version : 1.00
License : 
"""
from time import sleep
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port

from pixy2_pybricks import (Pixy2,
                            Pixy2ConnectionError,
                            Pixy2DataError)


def limit_speed(speed):
    """Limit speed in range [-900,900]."""
    if speed > 900:
        speed = 900
    elif speed < -900:
        speed = -900
    return speed

def main():
    # Objects for ev3-brick, motors and Pixy2 camera
    ev3 = EV3Brick()
    rmotor = Motor(Port.B)
    lmotor = Motor(Port.C)
    pixy2 = Pixy2(port=1, i2c_address=0x54)
    
    # Signature we're interesed in (SIG1)
    sig = 1
    
    # Defining constants
    X_REF = 158  # X-coordinate of referencepoint
    Y_REF = 150  # Y-coordinate of referencepoint
    KP = 0.3     # Proportional constant PID-controller
    KI = 0.01    # Integral constant PID-controller
    KD = 0.005   # Derivative constant PID-controller
    GAIN = 10    # Gain for motorspeed
    
    # Initializing PID variables
    integral_x = 0
    derivative_x = 0
    last_dx = 0
    integral_y = 0
    derivative_y = 0
    last_dy = 0
    
    while not ev3.buttons.pressed():
        # Read data from Pixy2 (only largest object)
        try:
            nr_blocks, blocks = pixy2.get_blocks(sig, 1)
            # Parse data
            if nr_blocks > 0:
                if sig == blocks[0].sig:
                    # SIG1 detected, control motors
                    x = blocks[0].x_center         # X-centroid of largest SIG1-object
                    y = blocks[0].y_center         # Y-centroid of largest SIG1-object
                    dx = X_REF - x                 # Error in reference to X_REF
                    integral_x = integral_x + dx   # Calculate integral for PID
                    derivative_x = dx - last_dx    # Calculate derivative for PID
                    speed_x = KP*dx + KI*integral_x + KD*derivative_x  # Speed X-direction
                    dy = Y_REF - y                 # Error in reference to Y_REF
                    integral_y = integral_y + dy   # Calculate integral for PID
                    derivative_y = dy - last_dy    # Calculate derivative for PID
                    speed_y = KP*dy + KI*integral_y + KD*derivative_y  # Speed Y-direction
                    # Calculate motorspeed out of speed_x and speed_y
                    # Use GAIN otherwise speed will be to slow,
                    # but limit in range [-1000,1000]
                    rspeed = limit_speed(GAIN*(speed_y - speed_x))
                    lspeed = limit_speed(GAIN*(speed_y + speed_x))
                    rmotor.run(round(rspeed))
                    lmotor.run(round(lspeed))
                    last_dx = dx                  # Set last error for x
                    last_dy = dy                  # Set last error for y
                else:
                    # SIG1 not detected, stop motors
                    rmotor.stop()
                    lmotor.stop()
                    last_dx = 0
                    last_dy = 0
        except Pixy2ConnectionError:
            # No data, stop program and check the connection of Pixy2
            print('Check connection Pixy2!')
            break
        except Pixy2DataError:
            # Data error, try reading again
            pass
    
    # Button pressed, stop motors, end of program
    rmotor.stop()
    lmotor.stop()


if __name__ == '__main__':
    main()
