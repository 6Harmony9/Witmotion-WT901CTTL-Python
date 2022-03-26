# Witmotion-WT901CTTL-Python
This is a Python code for Witmotion's WT901CTTL IMU sensor (Acceleromenter, Gyroscope, and Magnetometer)
Welcome to my very first project. Ever. Feedback is welcomed. Also let me know if there are any problems. 

Some Important Notes:
This code reads in data from Witmotion's WT901CTTL IMU sensor which can read acceleration, angular velocity, tilt angles, and magnetism(?). It has been tested to work on both Linux and Windows 11.

Upon execution, you may find that values from say, for example, tilt angles jump from 0 to 360 very rapidly. Do not panic. This sensor reads positions, and position 0 degrees is very close to, if not on the same place as posistion 360 degrees. This rapid change also affects acceleration, angular velocity, and magnetism as well.

I reccomend that if the code is to be used in you project, the code should be integrated into your source code directly in the while loop and not with a separate function. I have tried to use functions but for some reason when I do that, the code has a tendency to hang on startup and read nothing. This problem was significantly worse on Windows 11, but not much of a problem on Linux.

Be sure to uncomment the print function for specific readouts.


Oh, and if you are on Windos 11, type:

[System.IO.Ports.SerialPort]::getportnames()

to get a list of you COM ports.
