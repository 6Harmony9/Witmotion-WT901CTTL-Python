# This file contains a function to gather data from the connected Witmotion WT901C-TTl IMU sensor.
import serial
import time

# WT901 setup:
print("Setting up WT901...")
ser = serial.Serial()
#ser.port = '/dev/ttyUSB0' #For Linux. Also change the USB# to the correct # if necessary.
ser.port = 'COM3'  # For Windows 11. Also change the USB# to the correct # if necessary.
ser.baudrate = 9600
ser.parity = 'N'
ser.bytesize = 8
ser.timeout = 1
ser.open()
time.sleep(2)

# This function is to be called continuously in a separate function via a while or for loop.
def getIMUData():
	readData = ser.read(size=44).hex()
	# Make sure that ALL readData starts with 5551. Readings do not always start at bytes 5551 for some reason. This block will loop until the data starts at 5551.
	while(readData.startswith("5551") == False):
		print("Resetting  WT901...")
		ser.close()
		ser.open()
		readData = ser.read(size=44).hex()
		if(readData.startswith("5551")):
			break
	
	
	# After getting the IMU to read properly, calculations can begin.
	StartAddress_1 = int(readData[0:2], 16)
	StartAddress_A = int(readData[2:4], 16)
	AxL = int(readData[4:6], 16)
	AxH = int(readData[6:8], 16)
	AyL = int(readData[8:10], 16)
	AyH = int(readData[10:12], 16)
	AzL = int(readData[12:14], 16)
	AzH = int(readData[14:16], 16)
	TL_A = int(readData[16:18], 16)
	TH_A = int(readData[18:20], 16)
	SUM_A = int(readData[20:22], 16)
	
	StartAddress_2 = int(readData[22:24], 16)
	StartAddress_w = int(readData[24:26], 16)
	wxL = int(readData[26:28], 16)
	wxH = int(readData[28:30], 16)
	wyL = int(readData[30:32], 16)
	wyH = int(readData[32:34], 16)
	wzL = int(readData[34:36], 16)
	wzH = int(readData[36:38], 16)
	TL_w = int(readData[38:40], 16)
	TH_w = int(readData[40:42], 16)
	SUM_w = int(readData[42:44], 16)
	
	StartAddress_3 = int(readData[44:46], 16)
	StartAddress_ypr = int(readData[46:48], 16)
	RollL = int(readData[48:50], 16)
	RollH = int(readData[50:52], 16)
	PitchL = int(readData[52:54], 16)
	PitchH = int(readData[54:56], 16)
	YawL = int(readData[56:58], 16)
	YawH = int(readData[58:60], 16)
	VL = int(readData[60:62], 16)
	VH = int(readData[62:64], 16)
	SUM_ypr = int(readData[64:66], 16)
	
	StartAddress_4 = int(readData[66:68], 16)
	StartAddress_mag = int(readData[68:70], 16)
	HxL = int(readData[70:72], 16)
	HxH = int(readData[72:74], 16)
	HyL = int(readData[74:76], 16)
	HyH = int(readData[76:78], 16)
	HzL = int(readData[78:80], 16)
	HzH = int(readData[80:82], 16)
	TL_mag = int(readData[82:84], 16)
	TH_mag = int(readData[84:86], 16)
	SUM_mag = int(readData[86:88], 16)
	
	
# Acceleration output:
	mappedAx = ((AxH<<8)| AxL)
	mappedAy = ((AyH<<8)| AyL)
	mappedAz = ((AzH<<8)| AzL)
	mappedT_A = ((TH_A<<8)| TL_A)
	
	if(mappedAx > 32768):
		mappedAx = mappedAx - 65535
	if(mappedAy > 32768):
		mappedAy = mappedAy - 65535
	if(mappedAz > 32768):
		mappedAz = mappedAz - 65535
	if(mappedT_A > 32768):
		mappedT_A = mappedT_A - 65535
	
	Ax = float(mappedAx/32768.0*16.0)
	Ay = float(mappedAy/32768.0*16.0)
	Az = float(mappedAz/32768.0*16.0)
	T_A = float(mappedT_A/100.0)
	
	
# Angular velocity output:
	mappedWx = ((wxH<<8)| wxL)
	mappedWy = ((wyH<<8)| wyL)
	mappedWz = ((wzH<<8)| wzL)
	mappedT_w = ((TH_w<<8)| TL_w)
	
	if(mappedWx > 32768):
		mappedWx = mappedWx - 65535
	if(mappedWy > 32768):
		mappedWy = mappedWy - 65535
	if(mappedWz > 32768):
		mappedWz = mappedWz - 65535
	if(mappedT_w > 32768):
		mappedT_w = mappedT_w - 65535
	
	Wx = float(mappedWx/32768.0*2000.0)
	Wy = float(mappedWy/32768.0*2000.0)
	Wz = float(mappedWz/32768.0*2000.0)
	T_A = float(mappedT_w/100.0)
	
	
# Angle output:
	mappedRoll = ((RollH<<8)| RollL)
	mappedPitch = ((PitchH<<8)| PitchL)
	mappedYaw = ((YawH<<8)| YawL)
	
	if(mappedRoll > 32768):
		mappedRoll = mappedRoll - 65535
	if(mappedPitch > 32768):
		mappedPitch = mappedPitch - 65535
	if(mappedYaw > 32768):
		mappedYaw = mappedYaw - 65535
	
	Roll = float(mappedRoll/32768.0*180)
	Pitch = float(mappedPitch/32768.0*180)
	Yaw = float(mappedYaw/32768.0*180)
	
	
# Magnetic output:
	mappedHx = ((HxH<<8)| HxL)
	mappedHy = ((HyH<<8)| HyL)
	mappedHz = ((HzH<<8)| HzL)
	mappedT_mag = ((TH_mag<<8)| TL_mag)
	
	if(mappedHx > 32768):
		mappedHx = mappedHx - 65535
	if(mappedHy > 32768):
		mappedHy = mappedHy - 65535
	if(mappedHz > 32768):
		mappedHz = mappedHz - 65535
	if(mappedT_mag > 32768):
		mappedT_mag = mappedT_mag - 65535
	
	Hx = float(mappedHx)
	Hy = float(mappedHy)
	Hz = float(mappedHz)
	T_mag = float(mappedT_mag/100.0)


# Readable outputs. Uncomment for specific readouts.
	#print("%6.3f" % Ax, "%6.3f" % Ay, "%6.3f" % Az)
	#print("%7.3f" % Wx, "%7.3f" % Wy, "%7.3f" % Wz) # This detects any movement on the axes.
	print("%7.3f" % Roll, "%7.3f" % Pitch, "%7.3f" % Yaw) # This maps out tilt angles of the axes.
	#print("%4.0f" % Hx, "%4.0f" % Hy, "%4.0f" % Hz)
	
	
# The data is placed into a dictionary for organization.
	Ax = format(Ax, "6.3f")
	Ay = format(Ay, "6.3f")
	Az = format(Az, "6.3f")
	
	Wx = format(Wx, "7.3f")
	Wy = format(Wy, "7.3f")
	Wz = format(Wz, "7.3f")
	
	Roll = format(Roll, "7.3f")
	Pitch = format(Pitch, "7.3f")
	Yaw = format(Yaw, "7.3f")
	
	Hx = format(Hx, "4.0f")
	Hy = format(Hy, "4.0f")
	Hz = format(Hz, "4.0f")

	IMU_Data = {
		"Ax": Ax, "Ay": Ay, "Az": Az,
		"Wx": Wx, "Wy": Wy, "Wz": Wz,
		"Roll": Roll, "Pitch": Pitch, "Yaw": Yaw,
		"Hx": Hx, "Hy": Hy, "Hz": Hz 
	}
	#print(IMU_Data)
	return IMU_Data

# This is an example loop.
while True:
	getIMUData()
