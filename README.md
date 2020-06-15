# Using Pixy2 for LEGO Mindstorms EV3 on Pybricks

## Introduction

This tutorial will explain how to use the Pixy2 camera when your LEGO
Mindstorms EV3 device is running on Pybricks.

**Pixy2** is the second version of Pixy. It's faster, smaller and more capable
than the original Pixy, adding line tracking/following algorithms as well as
other features. For more information visit the
[Pixy wiki](https://docs.pixycam.com/wiki/doku.php?id=wiki:v2:lego_wiki).

**Pybricks** is Python for smart LEGO hubs, including Mindstorms EV3. It
builds on MicroPython, which is a super-efficient version of Python that can run
on the microcontrollers inside the smart hubs. This means your code really runs on
the hub, which makes it super fast, too. For more information visit the
[Pybricks website](https://pybricks.com/).

**LEGO Minstorms EV3** lets you build and program robots. Visit the
[LEGO Mindstorms website](https://www.lego.com/en-us/themes/mindstorms/about)
for more information.

## What's needed

To add vision to your robot, you'll need the following:

- A robot build with LEGO Mindstorms.
- Add Pixy2 to your robot, connect it to one of the sensor ports.
- Run your EV3-brick on Pybricks. Visit the
[Pybricks website](https://docs.pybricks.com/en/latest/start_ev3.html) to
learn how. Here you'll learn how to install VS Code and use the EV3
MicroPython extension.
- Create a new project and add the file `pixy2_pybrick.py` to your project.
- Read this tutorial how to use Pixy2 in your program.

If you like you can also clone this entire repository to you computer. Open
it in VS Code and run the following files:

- `main.py` - This is an example of a two-motor robot chasing an object. Be sure
to adjust the code to your robot configuration, as explained below.
- `linetracker.py` - This is a line-following robot. Again, adjust the code to
the configuration of your robot.

## How to use Pixy2 on Pybricks

Basicly there are two ways to do this:

1. Use Pybrick's I2C classes to interact with Pixy2
(`class I2CDevice(port, address)`). For this you nead to learn the serial
interface of Pixy2.
2. Use the classes from `pixy2_pybricks.py`. These classes do all the hard work
from method 1 for you. So you don't have to bother about the serial interface,
just execute the methods you need.

Method 1 will be desribed briefly now, followed by a more indepth description
of method 2. But first you need to make ready Pixy for the I2C communication.

## Pixy2 I2C interface

Configure Pixy2 to communicate over I2C. For this you can use the PixyMon tool
that comes with Pixy2. Open the configure dialog and click on the Interface
tab.

> If you don't see the Interface tab, you're probably not running the right
firmware on the Pixy camera. Be sure to run the stock version, instead of the
LEGO version. See
[Pixy documentation](https://docs.pixycam.com/wiki/doku.php?id=wiki:v2:uploading_new_firmware)
on how to install firmware.

![PixyMon configure dialog](/images/PixyMon_configure.png)

Set `Data out port` to `I2C` and `I2C address` to `0x54` (or any other address
you like).

## Pybrick's I2C interface

Pybrick's I2C interface is described
[here](https://docs.pybricks.com/en/latest/iodevices.html#i2c-device).
For creating an instance of object `I2CDevice` you need the portnumber which
the camera is connected to (e.g. `Port.S1`) and the I2C-address which you set
on the Pixy2 (e.g. `0x54`, see previous paragraph).

You can read from and write to the camera with methods
`read(reg=0x00, length=*n*)` and `write(reg=0x00, data)`, with `*n*` the
number of bytes to read and `data` being a `bytes` array.

Read the
[Pixy2 wiki](https://docs.pixycam.com/wiki/doku.php?id=wiki:v2:porting_guide)
for learning the serial interface protocol. With this information and the code
in `pixy2_pybricks.py` as an example it's not hard to find out how to do the
programming by yourself.

## Using pixy_pybricks

To make life more easier for you, you an use the classes from module
`pixy2_pybricks` in your program. Just add the file `pixy2_pybricks.py`
to your project and you're ready to go.

> If you just want to download this file to your computer instead of
the complete repository, open the file on Github and click the
`Raw` button on the top of the file. Then you can save the file in the
projectdirectory on your computer.

With class `Pixy2` you can use hte Pixy2 camera on your robot. Class
`Pixy2` has two parameters: portnumber Pixy2 is connected to (values 1 to 4,
default is 1) and I2C-address of Pixy2 (default `0x54):

```python
from pixy2_pybricks import Pixy2

pixy2 = Pixy2(port=1, i2c_address=0x54)
```

>Below we explain the classes in `pixy2_pybricks`. For a fully understanding
of this information it's adviced to read the
[Pixy2 wiki](https://docs.pixycam.com/wiki/doku.php?id=wiki:v2:pixy2_full_api).

### Methods

**get_version()**<br />
Queries and receives the firmware and hardware version of Pixy2.

*parameters*<br />
none.

*return value*<br />
`Pixy2Version`: hardware and software version (see section Data Types).

**get_resolution()**<br />
Gets the width and height of the frames used by the current program.

*parameters*<br />
none.

*return value*<br />
`PixyResolution`: frame resolution (see section Data Types).

**set_lamp(upper, lower)**<br />
Turn leds on or off.

*parameters*<br />
`upper` (bool): toggle for upper leds (`True` for on, `False` for off).<br />
`lower` (bool): toggle for lower led (`True` for on, `False` for off).

*return value*<br />
none.

**set_mode(mode)**<br />
Set mode for Pixy (linetracking).

*parameters*<br />
`mode`.

*return value*<br />
none.

**get_blocks(sigmap, max_blocks)**<br />
Get data about detected object(s).

*parameters*<br />
`sigmap` (int): signature(s) to detect.<br />
`max_blocks` (int): max number of blocks to return.

`sigmap` is a bitmap of all 7 signatures from which you wish to receive
block data. For example, if you are only interested in block data from
signature 1, you would pass in a value of 1. If you are interested in
block data from both signatures 1 and 2, you would pass in a value of 3.
If you are interested in block data from signatures 1, 2, and 3, you would
pass a value of 7, and so on

*return values*<br />
`nr_detected_blocks` (int): number of detected blocks.<br />
`blocks` (`Block`): array with block data. The blocks in this array are sorted
by area, with the largest blocks appearing first in the blocks array (see
section Data Types).

**get_linetracking_data()**<br />
Get linetracking data from Pixy2. It gets the latest features including the
`Vector`, any `Intersection` that connects to the Vector, and `Barcodes`.

*parameters*<br />
none.

*return value*<br />
`MainFeaturures`: linetracking data (see section Data types)

**set_next_turn(angle)**<br />
This function tells the line tracking algorithm which path it should take
at the next intersection. Pixy2 will remember the turn angle you give it, and
execute it at the next intersection. The line tracking algorithm will then go
back to the default turn angle for subsequent intersections.
Upon encountering an intersection, the line tracking algorithm will find the
path in the intersection that matches the turn angle most closely.

*parameters*<br />
`angle` (int): specified in degrees, with 0 being straight ahead, left being 90
and right being -90 (for example), although any valid angle value can be used.
Valid angles are between -180 and 180.


*return value*<br />
none.

**set_default_turn(angle)**<br />
This function tells the line tracking algorithm which path to choose by
default upon encountering an intersection. The line tracking algorithm will
find the path in the intersection that matches the default turn angle most
closely.

*parameters*<br />
`angle` (int): Turn angles are specified in degrees, with 0 being straight
ahead, left being 90 and right being -90 (for example), although any valid
angle value can be used. Valid angles are between -180 and 180.

*return value*<br />
none.

**set_vector(index)**<br />
Set vector to use at an intersection, use this method when Pixy2 is in mode
`LINE_MODE_MANUAL_SELECT_VECTOR`: the line tracking algorithm will no longer
choose the Vector automatically. Instead, `set_vector()` will set the Vector
by providing the index of the line.

*parameters*<br />
`index` (int): index of the line.

*return value*<br />
none.

### Data types

**Pixy2Version**<br />
Version information of Pixy2:<br />
.hardware (int): hardware version.<br />
.firmware (str): firmware version.<br />
.firmware_type (str): firmware type.<br />

**Pixy2Mode**<br />
Different modes for linetracking:<br />
.LINE_MODE_DEFAULT<br />
.LINE_MODE_TURN_DELAYED<br />
.LINE_MODE_MANUAL_SELECT_VECTOR<br />
.LINE_MODE_WHITE_LINE<br />

In LINE_MODE_DEFAULT the linetracking algorithm will automatically choose the
vector based on the angle set with `set_default_turn(angle)`. In
LINE_MODE_TURN_DELAYED the algortihm wait on `set_next_turn(angle)` to instruct the
robot to follow the vector closest to the given angle. In mode
LINE_MODE_MANUAL_SELECT_VECTOR the algorithm chooses the vector set with
`set_vector(index)`.
Use LINE_MODE_WHITE_LINE when using a light colored line on a dark background.

**PixyResolution**<br />
Resolution of the sensor:<br />
`.width` (int): width.<br />
`.height` (int): height.<br />

**Block**<br />
Data for color connected components:<br />
`.sig` (int): signature of detected object.<br />
`.x_center` (int): x-coordinate of center of the block.<br />
`.y_center` (int): y-coordinate of center of the block.<br />
`.width` (int): width of the block.<br />
`.height` (int): height of the block.<br />
`.angle` (int): angle of color-code in degrees.<br />
`.tracking_index` (int): tracking index of the block.<br />
`.age` (int): the number of frames a given block has been detected.<br />

**Vector**
Vector data for linetracking:<br />
`.x0` (int): x-coordinate of tail of vector.<br />
`.y0` (int): y-coordinate of tail of vector.<br />
`.x1` (int): x-coordinate of head of vector.<br />
`.y1` (int): y-coordinate of head of vector.<br />
`.index` (int): tracking index of the vector or line.<br />
`.flags` (int): contains various flags that might be useful.<br />

**Intersection**<br />
Intersection data for linetracking:<br />
`.x` (int): x-coordinate of intersection.<br />
`.y` (int): y-coordinate of intersection.<br />
`.nr_of_branches` (int): number of branches starting on the intersection.<br />
`.branches` (Branch): branch data.<br />

**Branch**<br />
Branch data:<br />
`.index` (int): index of branch.<br />
`.angle` (int): angle of the branch.<br />
`.angle_byte1` (int): first byte of angle.<br />
`.angle_byte2` (int): second byte of angle.<br />

Calculate the angle by `angle = byte2 << 8 | byte1`.

**Barcode**<br />
Barcode data:<br />
`.x` (int): x-coordinate of barcode.<br />
`.y` (int): y-coordinate of barcode.<br />
`.flags` (int): various flags that might be useful.<br />
`.code` (int): code to identity the barcode.<br />

**MainFeatures**<br />
Linetracking data: <br />
`.length_of_payload` (int): number of bytes containing data.<br />
`.number_of_vectors` (int): number of vectors.<br />
`.number_of_intersections` (int): number of intersections.<br />
`.number_of_barcodes` (int): number of barcodes.<br />
`.vectors` (Vector): array with vector data.<br />
`.intersections` (Intersection): array with intersection data.<br />
`.barcodes` (Barcode): array with barcode data.<br />

### Error handling

`Pixy2ConnectionError`: Pixy2 could not be detetected, check connection.<br />
`Pixy2DataError`: error while reading data, try reading again.
