#!/usr/bin/env pybricks-micropython
""" main.py

Demo program for using Pixy2 on PyBricks. It is a good place to start if
you're just getting started with Pixy2 and LEGO MINDSTORMS EV3 running
Pybricks.
This program simply prints the detected object blocks.

Usage: Connect Pixy2 to your EV3-brick on port 1. If you use a different port,
       adjust the code in this file.

       In Pixy2's configuration window set the interface to I2C and 
       I2C address to 0x54. If you choose to use a different I2C address, 
       change the value in the code of this file.

       Start main.py from VS Code and it prints information about detected
       objects to the output console. To stop the program, press any button
       on the EV3-brick.

See https://docs.pixycam.com for more inforamation about Pixy2.
See https://docs.pybricks.com how to run programs on Pybricks.


Author  : Kees Smit
Date    : June 16 2020
Version : 1.00
License : 
"""
from time import sleep

from pybricks.hubs import EV3Brick
from pybricks.parameters import Port
from pixy2_pybricks import (Pixy2,
                            Pixy2ConnectionError,
                            Pixy2DataError)


def main():
    # Objects for ev3-brick and Pixy2 camera
    ev3 = EV3Brick()
    pixy2 = Pixy2(port=1, i2c_address=0x54)
    
    # Detect all signatures (set sig to 255)
    sig = 255
    max_blocks = 10

    while not ev3.buttons.pressed():
        # Read data from Pixy2
        try:
            nr_blocks, blocks = pixy2.get_blocks(sig, max_blocks)
            print('{} blocks detected:'.format(nr_blocks))
            # Parse data
            if nr_blocks > 0:
                # Print information about detected blocks
                for block in blocks:
                    print(block, '\n')
        except Pixy2ConnectionError:
            # No data, stop program and check the connection of Pixy2
            print('Check connection Pixy2!')
            break
        except Pixy2DataError:
            # Data error, try reading again
            pass
    

if __name__ == '__main__':
    main()
