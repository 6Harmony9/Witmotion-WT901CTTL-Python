# Witmotion WT901C TTL Python
This is a Python code for Witmotion's WT901CTTL IMU sensor (Acceleromenter, Gyroscope, and Magnetometer)
Welcome to my very first project. Ever. Feedback is welcomed. Also let me know if there are any problems. 

Some Important Notes:

This code reads in data from Witmotion's WT901CTTL IMU sensor which can read acceleration, angular velocity, tilt angles, and magnetism(?). It has been tested to work on both Linux and Windows 11.

Please make sure that you have the pyserial installed. Also make sure that the physical USB TTL connection between your computer and the IMU sensor is not loose, otherwise the application will freeze.

If you are on Windows 11 and do not know which COM port is being used by the IMU, go to the Device Manager and open the tab Ports(COM & LPT). Under that you will find USB-SERIAL CH430 and a COM port that it is using. This is likely going to be the only USB serial device utilizing the CH430 chip you have connected to your Windows 11 computer.

Be sure to comment/uncomment the print functions for specific readouts.
