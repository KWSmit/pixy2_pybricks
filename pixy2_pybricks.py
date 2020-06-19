""" Python module for using Pixy2 for LEGO Mindstorms on PyBricks

Public classes:
Pixy2           -- Common functionality of Pixy2
Pixy2Version    -- Version information
Pixy2Resolution -- Width and height of frame
Block           -- Color Connected Components packet
Vector          -- Vector data
Intersection    -- Intersection data
Branch          -- Branch data
Barcode         -- Barcode data
MainFeatures    -- Common linetracking data


Author  : Kees Smit
Date    : Jun 16 2020
Version : 1.00
License : 
"""
from pybricks.parameters import Port
from pybricks.iodevices import I2CDevice


# Barcode constants
BARCODE_FORWARD = 1
BARCODE_LEFT = 0
BARCODE_RIGHT = 5
BARCODE_DEACTIVATE = 12
BARCODE_ACTIVATE = 13

class Pixy2:
    """ This class contains all general functionalities of Pixy2.
    
    Keyword arguments:
    port        -- portnumber to wich the Pixy2 is connected (INT)
    i2c_address -- i2c address for communicating with Pixy2 (hexa-decimal)

    Public methods:
    get_version           -- Get harware and firmware version of Pixy2
    get_resolution        -- Get resolution of Pixy2 frame
    set_lamp              -- Turn upper and lower leds of Pixys on or off
    get_blocks            -- Get data about detected signatures
    get_linetracking_data -- Get data for linetracking
    """
    def __init__(self, port=1, i2c_address=0x54):
        """ Initialising Pixy2 class.
        
        Keyword arguments:
        port        -- portnumber to wich the Pixy2 is connected
                       (INT in range (1, 4)).
        i2c_address -- i2c address for communicating with Pixy2
                       (hexa-decimal, set in configuration Pixy2).
        """
        if port == 1:
            ev3_port = Port.S1
        elif port == 2:
            ev3_port = Port.S2
        elif port == 3:
            ev3_port = Port.S3
        elif port == 4:
            ev3_port = Port.S4
        else:
            raise ValueError('Portnumber out of range (1, 4)')
        self.pixy2 = I2CDevice(ev3_port, i2c_address)
        self._mode = Pixy2Mode().LINE_MODE_DEFAULT
    
    def get_version(self):
        """ Queries and receives the firmware and hardware version Pixy2."""
        pixy2_version = Pixy2Version()
        # Request data
        data = [174, 193, 14, 0]
        self.pixy2.write(reg=0x00, data=bytes(data))
        # Read header
        header = self.pixy2.read(reg=0x00, length=6)
        check_packet_type(header, 15)
        # Read and parse data
        data = self.pixy2.read(reg=0x00, length=16)
        pixy2_version.hardware = data[1] << 8 | data[0]
        fw = [str(data[2]), str(data[3]), str(data[5] << 8 | data[4])]
        pixy2_version.firmware = '.'.join(fw)
        pixy2_version.firmware_type = data[6:-1].decode()

        return pixy2_version

    def get_resolution(self):
        """ Gets the width and height of the frames."""
        resolution = PixyResolution()
        data = [174, 193, 12, 1, 0]
        self.pixy2.write(reg=0X00, data=bytes(data))
        # Read header
        header = self.pixy2.read(reg=0x00, length=6)
        check_packet_type(header, 13)
        # Read and parse data
        data = self.pixy2.read(reg=0x00, length=4)
        resolution.width = data[1] << 8 | data[0]
        resolution.height = data[3] << 8 | data[2]
        return resolution

    def set_lamp(self, upper, lower):
        """ Turn on/off upper and lower LED's of Pixy2 (False=off, True=on)."""
        data = [174, 193, 22, 2, upper, lower]
        self.pixy2.write(reg=0x00, data=bytes(data))
        # Read header
        header = self.pixy2.read(reg=0x00, length=10)
        check_packet_type(header, 1)

    def set_mode(self, mode):
        """ Set mode for Pixy2."""
        data = [174, 193, 54, 1, mode]
        self.pixy2.write(reg=0x00, data=bytes(data))
        # Read header
        header = self.pixy2.read(reg=0x00, length=10)
        check_packet_type(header, 1)

    def get_blocks(self, sigmap, max_blocks):
        """ Get blockdata for sigmap."""
        blocks = []
        # Request data
        data = [174, 193, 32, 2, sigmap, max_blocks]
        self.pixy2.write(reg=0x00, data=bytes(data))
        # Read header
        header = self.pixy2.read(reg=0x00, length=6)
        check_packet_type(header, 33)
        length_of_payload = header[3]
        nr_detected_blocks = int(length_of_payload/14)
        # Read and parse data
        for b in range(0, nr_detected_blocks):
            data = self.pixy2.read(reg=0x00, length=14)
            blocks.append(Block())
            blocks[b].sig = data[1] << 8 | data[0]
            blocks[b].x_center = data[3] << 8 | data[2]
            blocks[b].y_center = data[5] << 8 | data[4]
            blocks[b].width= data[7] << 8 | data[6]
            blocks[b].height = data[9] << 8 | data[8]
            blocks[b].angle = data[11] << 8 | data[10]
            blocks[b].tracking_index = data[12]
            blocks[b].age = data[13]

        return nr_detected_blocks, blocks


    def get_linetracking_data(self):
        """ Get linetracking data from Pixy2."""

        mainfeatures = MainFeatures()
        vector = Vector()
        intersection = Intersection()
        branch = Branch()
        barcode = Barcode()
        payload_read = 0

        # Request
        data = [174,193, 48, 2, 0, 7]
        self.pixy2.write(reg=0x00, data=bytes(data))

        # Read header info
        header = self.pixy2.read(reg=0x00, length=6)
        # Parse header info
        check_packet_type(header, 49)
        mainfeatures.length_of_payload = header[3]

        # Read payload data
        while payload_read < mainfeatures.length_of_payload:
            # Read feature type and length
            data = self.pixy2.read(reg=0x00, length=2)
            feature_type = data[0]
            feature_length = data[1]
            # Read feature data
            if feature_type == 1:
                # Feature type is 'vector'
                data = self.pixy2.read(reg=0x00, length=feature_length)
                vector.x0 = data[0]
                vector.y0 = data[1]
                vector.x1 = data[2]
                vector.y1 = data[3]
                vector.index = data[4]
                vector.flags = data[5]
                mainfeatures.add_vector(vector)
            elif feature_type == 2:
                # feature type is 'intersection'
                data = self.pixy2.read(reg=0x00, length=feature_length)
                intersection.x = data[0]
                intersection.y = data[1]
                intersection.nr_of_branches = data[2]
                for i in range(0, intersection.nr_of_branches):
                    i4 = i*4
                    branch.index = data[i4+0]
                    branch.angle = data[14+1]
                    branch.angle_byte1 = data[i4+2]
                    branch.angle_byte2 = data[i4+3]
                    intersection.add_branch(branch)
                mainfeatures.add_intersection(intersection)
            elif feature_type == 4:
                # Feature type is 'barcode'
                data = self.pixy2.read(reg=0x00, length=feature_length)
                barcode.x = data[0]
                barcode.y = data[1]
                barcode.flags = data[2]
                barcode.code = data[3]
                mainfeatures.add_barcode(barcode)
            else:
                # Unknown feature type
                mainfeatures.error = True

            payload_read += feature_length + 2

        # Return data
        return mainfeatures

    def set_next_turn(self, angle):
        """ Set direction for turn at next intersection."""
        data = [174, 193, 58, 2]
        data_bytes = bytes(data)
        # Add angle (2 bytes, little endian, signed)
        data_bytes += angle.to_bytes(2, 'little', True)
        self.pixy2.write(reg=0x00, data=data_bytes)
        # Read header
        header = self.pixy2.read(reg=0x00, length=10)
        check_packet_type(header, 1)

    def set_default_turn(self, angle):
        """ Set default direction for turn at an intersection."""
        data = [174, 193, 60, 2]
        data_bytes = bytes(data)
        # Add angle (2 bytes, little endian, signed)
        data_bytes += angle.to_bytes(2, 'little', True)
        self.pixy2.write(reg=0x00, data=data_bytes)
        # Read header
        header = self.pixy2.read(reg=0x00, length=10)
        check_packet_type(header, 1)

    def set_vector(self, index):
        """ Set vector to use at an intersection, use this method when
        Pixy2 is in mode LINE_MODE_MANUAL_SELECT_VECTOR."""
        data = [174, 193, 56, 1, index]
        self.pixy2.write(reg=0x00, data=bytes(data))
        # Read header
        header = self.pixy2.read(reg=0x00, length=10)
        check_packet_type(header, 1)


# Pixy2 specific datatypes

class Pixy2Version:
    """ Version information of Pixy2."""
    def __init__(self):
        self.hardware = None
        self.firmware = None
        self.firmware_type = None
    
    def __str__(self):
        str_version = 'Hardware version: {}\nFirmware version: {} {}\n'.format(
            self.hardware, self.firmware, self.firmware_type)
        return str_version

class Pixy2Mode:
    """ Pixy2 modes for linetracking."""
    def __init__(self):
        self.LINE_MODE_DEFAULT = 0x00
        self.LINE_MODE_TURN_DELAYED = 0x01
        self.LINE_MODE_MANUAL_SELECT_VECTOR = 0x02
        self.LINE_MODE_WHITE_LINE = 0x80


# General datatypes

class PixyResolution:
    """ Frame resolution."""
    def __init__(self):
        self.width = None
        self.height = None

    def __str__(self):
        return 'Resolution: widht={}, height={}\n'.format(
            self.width, self.height)

class Block:
    """ Datablock with detected signature."""
    def __init__(self):
        self.sig = None
        self.x_center = None
        self.y_center = None
        self.width = None
        self.height = None
        self.angle = None
        self.tracking_index = None
        self.age = None

    def __str__(self):
        desc = 'sig: {}\nx: {}\ny: {}\nwidth:  {}\nheight: {}'.format(
            self.sig, self.x_center, self.y_center, self.width, self.height)
        return desc

class Vector:
    """ Vector data for linetracking."""
    def __init__(self):
        self.x0 = 0
        self.y0 = 0
        self.x1 = 0
        self.y1 = 0
        self.index = 0
        self.flags = 0


class Intersection:
    """ Intersection data for linetracking."""
    def __init__(self):
        self.x = 0
        self.y = 0
        self.nr_of_branches = 0
        self.branches = []

    def add_branch(self, branch):
        """ Add branch to intersection."""
        b = Branch()
        b.index = branch.index
        b.angle = branch.angle
        self.branches.append(b)


class Branch:
    """ Data for branch of intersection."""
    def __init__(self):
        self.index = 0
        self.angle = 0
        self.angle_byte1 = 0
        self.angle_byte2 = 0


class Barcode:
    """ Date of detected barcode."""
    def __init__(self):
        self.x = 0
        self.y = 0
        self.flags = 0
        self.code = 0


class MainFeatures:
    """ Data for linetracking."""
    def __init__(self):
        self.length_of_payload = 0
        self.number_of_vectors = 0
        self.number_of_intersections = 0
        self.number_of_barcodes = 0
        self.vectors = []
        self.intersections = []
        self.barcodes = []

    def add_vector(self, vector):
        v = Vector()
        v.x0 = vector.x0
        v.y0 = vector.y0
        v.x1 = vector.x1
        v.y1 = vector.y1
        v.index = vector.index
        v.flags = vector.flags
        self.vectors.append(v)
        self.number_of_vectors += 1

    def add_intersection(self, intersection):
        ints = Intersection()
        b = Branch()
        ints.x = intersection.x
        ints.y = intersection.y
        ints.nr_of_branches = intersection.nr_of_branches
        for branch in intersection.branches:
            b.index = branch.index
            b.angle = branch.angle
            b.angle_byte1 = branch.angle_byte1
            b.angle_byte2 = branch.angle_byte2
            ints.add_branch(b)
        self.intersections.append(ints)
        self.number_of_intersections += 1

    def add_barcode(self, barcode):
        b = Barcode()
        b.x = barcode.x
        b.y = barcode.y
        b.flags = barcode.flags
        b.code = barcode.code
        self.barcodes.append(b)
        self.number_of_barcodes += 1

    def clear(self):
        self.length_of_payload = 0
        self.number_of_vectors = 0
        self.number_of_intersections = 0
        self.number_of_barcodes = 0
        self.vectors.clear()
        self.intersections.clear()
        self.barcodes.clear()


# Pixy2 custom DataError:
class Pixy2DataError(Exception):
    """ Custom error for Pixy data communication."""
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors
        print(errors)

class Pixy2ConnectionError(Exception):
    """ Custom error for Pixy connection fault."""
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors
        print(errors)

def check_packet_type(header, packet_type):
    """ Check if data packet type is correct, raise exception when not."""
    if header[2] == 0:
        # No data at all, Pixy2 connected?
        msg = 'Empty data packet, check if Pixy2 is properly connected!'
        raise Pixy2ConnectionError(msg, 'Pixy2ConnectionError')
    elif header[2] != packet_type:
        # Read wrong type of packet
        msg = "Read wrong type of packet: {} instead of {}".format(
              header[2], packet_type)
        raise Pixy2DataError(msg, 'Pixy2DataError')
