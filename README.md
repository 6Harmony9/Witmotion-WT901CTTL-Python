# Witmotion WT901C TTL Python
This is a Python code for Witmotion's WT901CTTL IMU sensor (Acceleromenter, Gyroscope, and Magnetometer)
Welcome to my very first project. Ever. Feedback is welcomed. Also let me know if there are any problems. 

Some Important Notes:

This code reads in data from Witmotion's WT901CTTL IMU sensor which can read acceleration, angular velocity, tilt angles, and magnetism(?). It has been tested to work on both Linux and Windows 11.

Please make sure that you have the pyserial and numpy libraries installed. Also make sure that you install all of Witmotion's necessary drivers, too.

I reccomend that if the code is to be used in you project, the code should be integrated into your source code directly in the while loop and not with a separate function. I have tried to use functions but for some reason when I do that, the code has a tendency to hang on startup and read nothing. This problem was significantly worse on Windows 11, but not much of a problem on Linux.

Make sure that the physical USB TTL connection between your computer and the IMU sensor is not loose, otherwise the application will freeze.

Be sure to uncomment the print function for specific readouts.


Oh, and if you are on Windows 11, type:

'[System.IO.Ports.SerialPort]::getportnames()'

without the quotation marks into Windows Powershell to get a list of your COM ports.


*So far, so good!*
