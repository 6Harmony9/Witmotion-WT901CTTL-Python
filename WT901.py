import threading
import time
import serial
import struct

class IMUState(object):
	def __init__(self):
		self.lock = threading.Lock()
		self.timestamp = time.time()
		
		self.Ax = 0.0
		self.Ay = 0.0
		self.Az = 0.0
		
		self.Wx = 0.0
		self.Wy = 0.0
		self.Wz = 0.0
		
		self.Roll = 0.0
		self.Pitch = 0.0
		self.Yaw = 0.0
		
		self.Hx = 0.0
		self.Hy = 0.0
		self.Hz = 0.0		


# WT901C IMU reader class:
class WT901C(object):
	FRAME_SIZE = 11
	HEADER = 0x55
	
	# Setup requires the port name and baud rate. 9600 is the default baudrate, but it can be changed using Witmotion's MiniIMU Application.
	def __init__(self, port, baudrate=9600):
		self.port = port
		self.ser = serial.Serial(port, baudrate, timeout=0.05)
		self.buffer = bytearray()
		self.state = IMUState()
		
		self.running = True	
		self.thread = threading.Thread(target=self._fill_buffer)
		self.thread.daemon = True
		self.thread.start()
		

	# Read bytes and fill the buffer:
	def _fill_buffer(self):
		while self.running:
			data = self.ser.read(self.ser.in_waiting or 1)
			if data:
				self.buffer.extend(data)
				self._process_buffer()
			else:
				time.sleep(0.001)
		
		
	# Process the buffer and parse frames:
	def _process_buffer(self):
		buf = self.buffer
		while len(buf) >= self.FRAME_SIZE:
			# Find frame header:
			if buf[0] != self.HEADER:
				del buf[0]
				continue
			
			frame = buf[:self.FRAME_SIZE]
			
			# Checksum Validation:
			if (sum(frame[:10]) & 0xFF) != frame[10]:
				del buf[0]  
				continue
			
			# Decode frame:
			self._decode_frame(frame)
			
			# Remove processed frame:
			del buf[:self.FRAME_SIZE]


	# Decoding the frame:
	def _decode_frame(self, frame):
		frame_type = frame[1]
		vals = struct.unpack('<hhhh', frame[2:10])
		
		with self.state.lock:
			# Acceleration:
			if frame_type == 0x51:  
				self.state.Ax = vals[0] / 32768 * 16
				self.state.Ay = vals[1] / 32768 * 16
				self.state.Az = vals[2] / 32768 * 16

			# Gyroscope:
			elif frame_type == 0x52:  
				self.state.Wx = vals[0] / 32768 * 2000
				self.state.Wy = vals[1] / 32768 * 2000
				self.state.Wz = vals[2] / 32768 * 2000

			# Angle:
			elif frame_type == 0x53:  
				self.state.Roll  = vals[0] / 32768 * 180
				self.state.Pitch = vals[1] / 32768 * 180
				self.state.Yaw   = vals[2] / 32768 * 180
				
			# Magnetometer:
			elif frame_type == 0x54:  
				self.state.Hx = vals[0]
				self.state.Hy = vals[1]
				self.state.Hz = vals[2]
			
			self.state.timestamp = time.time()


	# Get the data, essentially:
	def get_state(self):
		with self.state.lock:
			return (
				self.state.Ax,
				self.state.Ay,
				self.state.Az,
				self.state.Wx,
				self.state.Wy,
				self.state.Wz,
				self.state.Roll,
				self.state.Pitch,
				self.state.Yaw,
				self.state.Hx,
				self.state.Hy,
				self.state.Hz,
				self.state.timestamp
			)


	# Cleanup method:
	def close(self):
		self.running = False
		self.thread.join()

		if self.ser.is_open:
			self.ser.close()


# Testing part. This is just a sample use case and should be removed if you want to call WT901C() in another script.
# However, there is some additional data that can prove useful further down a project namely, delta t, and imu_age.
if __name__ == "__main__":
	
	# Create the imu object. Make sure you enter the correct port name.:
	imu = WT901C("COM9", 9600)

	try:
		# previous_time will be updated throughout the loop.
		previous_time = time.time()
		
		# The control loop:
		while True:
			# dt is the control loop timing, or how long the control loop took to complete, delta t.
			# dt is useful for getting correct angle changes. for example, angle_change = gyro_rate * dt
			current_time = time.time()
			dt = current_time - previous_time
			previous_time = current_time
			
			# Retrieve IMU data:
			Ax, Ay, Az, Wx, Wy, Wz, Roll, Pitch, Yaw, Hx, Hy, Hz, timestamp = imu.get_state()
			
			#imu_age is how long ago the IMU updated. It is useful for detecting and filtering out stale sensor data.
			imu_age = current_time - timestamp
			
			# Comment/Uncomment for values.
			print("{:.3f} {:.3f} {:.3f}".format(Roll, Pitch, Yaw))
			#print("IMU Age:", imu_age)
			#print("Loop Frequency", "{:.14f}".format(1.0/dt), "Hz")
			
			# Ideally, this should be kept at 0.01. This makes sure that the loop frequency is around 90-100Hz.
			time.sleep(0.01)
	finally:
		imu.close()
