#!/usr/bin/env pybricks-micropython
""" linetracker.py

Demo program for using Pixy2 on PyBricks: let your robotrover
follow a line.

Usage: In Pixy2's configuration window set the interface to I2C and 
       I2C address to 0x54. If you choose to use a different I2C address, 
       change the value in the code of this file.

       Build a robot with two motors (port B and C) and Pixy2 camera (port S1).
       If you use different ports, adjust the code in this file.
       
       Start linetracker.py and your robot will follow the oject of sig1.
       Push any button on the EV3-brick to stop the program.

       For performance in following the line it may be necessary to adjust
       the PID constants for your robot.

See https://docs.pixycam.com for more inforamation about Pixy2.
See https://docs.pybricks.com how to run programs on Pybricks.


Author  : Kees Smit
Date    : June 16 2020
Version : 1.01
License : 
"""
from pixy2_pybricks import (Pixy2,
                            MainFeatures,
                            Pixy2ConnectionError,
                            Pixy2DataError)
from rover import Rover


# Rover with Pixy2 camera
rover = Rover()
pixy2 = Pixy2(port=1)

# Reerence point for linefollowing
frame_resolution = pixy2.get_resolution()
X_REF = int(frame_resolution.width/2)

# PID control constants
KP = 0.7     # Proportional constant PID-controller
KI = 0.0     # Integral constant PID-controller
KD = 0.0     # Derivative constant PID-controller

# Initializing PID variables
integral_x = 0
derivative_x = 0
last_dx = 0

start_intersection = False

# Turn lamp on
pixy2.set_lamp(upper=True, lower=False)

# Loop until a button is pressed
while not rover.ev3.buttons.pressed():
    # Get linetracking data from Pixy2
    try:
        data = pixy2.get_linetracking_data()
        # Process data
        if data.number_of_barcodes > 0:
            # Barcode(s) found
            pass
        if data.number_of_intersections > 0:
            # Intersection found
            rover.ev3.speaker.beep()
        if data.number_of_vectors > 0:
            # Check for intersection
            if data.vectors[0].flags == 4:
                # Intersection in sight, sl slow down not to miss it
                rover.move_slow()
                start_intersection = True
            else:
                # No intersection in sight, so full speed ahead
                rover.move_fast()
                if start_intersection:
                    start_intersection = False
            # Calculate speed out of offset in X-coördinate, using PID
            dx = X_REF - data.vectors[0].x1
            integral_x += dx
            derivative_x = dx -last_dx
            speed_x = KP*dx + KI*integral_x + KD*derivative_x
            last_dx = dx
            rover.move(speed_x)
        else:
            # No vector data stop robot
            rover.stop()
        # Clear data for reading next loop
        data.clear()
    except Pixy2ConnectionError:
        # No data, stop program and check connection Pixy2
        print('Check connection Pixy2!')
        break
    except Pixy2DataError:
        # Data error, try reading again
        rover.ev3.speaker.beep()
    except:
        # Unknown error, stop program
        print('Unknown error!')
        break

# Stop robot
rover.stop()

# Turn lamp off
pixy2.set_lamp(upper=False, lower=False)
