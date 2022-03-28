# Though more tedious and messy, having all the code as part of the main function loop is more reliable. It appears to start up correctly every time. 
import serial
import time
import numpy as np

# Initial conditions
ser = serial.Serial()
ser.port = '/dev/ttyUSB0' #for linux. Also change the USB# to the correct # if necessary.
#ser.port = 'COM7' 
ser.baudrate = 9600
ser.parity = 'N'
ser.bytesize = 8
ser.timeout = 1
ser.open()

readData = ""
dataStartRecording = False

# This part is needed so that the reading can start reliably.
print('Starting...', ser.name)
time.sleep(1)
ser.reset_input_buffer()

# Loop through the string of bytes. If you are planning to use this code in your project, the main loop starts here.
while True:
	rawData = ser.read(size=2).hex()
	
# Make sure that ALL readData starts with 5551 before recording starts. Readings do not always start at bytes 5551 for some reason.	
	if rawData == '5551':
		dataStartRecording = True
	
# Recording and concatenation functions
	if dataStartRecording == True:
		readData = readData + rawData
		
# Processing. Varaible names based on variables on the Witmotion WT901CTTL datasheet.
		if len(readData) == 88:
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
			
# Acceleration output
			Ax = float(np.short((AxH<<8)|AxL)/32768.0*16.0)
			Ay = float(np.short((AyH<<8)|AyL)/32768.0*16.0)
			Az = float(np.short((AzH<<8)|AzL)/32768.0*16.0)
			T_A = float(np.short((TH_A<<8)|TL_A)/100.0)
			
# Angular velocity output		
			Wx = float(np.short((wxH<<8)|wxL)/32768.0*2000.0)
			Wy = float(np.short((wyH<<8)|wyL)/32768.0*2000.0)
			Wz = float(np.short((wzH<<8)|wzL)/32768.0*2000.0)
			T_w = float(np.short((TH_w<<8)|TL_w) /100.0)
			
# Angle output			
			Roll = float(np.short((RollH<<8)|RollL)/32768.0*180.0)
			Pitch = float(np.short((PitchH<<8)|PitchL)/32768.0*180.0)
			Yaw = float(np.short((YawH<<8)|YawL)/32768.0*180.0)
			
# Magnetic output
			Hx = float(np.short(HxH<<8)| HxL)
			Hy = float(np.short(HyH<<8)| HyL)
			Hz = float(np.short(HzH<<8)| HzL)
			T_mag = float(np.short((TH_mag<<8)|TL_mag) /100.0)

# Readable outputs. Uncomment for specific readouts. 
			#print(readData)
			#print("%6.3f" % Ax, "%6.3f" % Ay, "%6.3f" % Az)
			print("%7.3f" % Wx, "%7.3f" % Wy, "%7.3f" % Wz) # This detects any movement on the axes.
			#print("%7.3f" % Roll, "%7.3f" % Pitch, "%7.3f" % Yaw) # This maps out tilt angles of the axes.
			#print("%4.0f" % Hx, "%4.0f" % Hy, "%4.0f" % Hz)
# Cleanup
			readData = ""
			dataStartRecording = False

	
