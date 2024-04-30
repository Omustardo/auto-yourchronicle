import imageio
import numpy as np
import threading
import time
import pyautogui
import navigator

# Define constants
FRAME_RATE = 15  # Frames per second
BUFFER_DURATION = 30  # Buffer duration in seconds

# Initialize buffer
buffer = []
buffer_lock = threading.Lock()

# Function to continuously capture frames and update buffer. Must only be called once.
def populate_buffer():
	global buffer
	global buffer_lock
	print("Starting debug video buffer. Buffer len=" + str(BUFFER_DURATION) + "s at " + str(FRAME_RATE) + "fps.")

	while True:
		# TODO: Taking screenshots is very slow, which makes the framerate in the output video not match reality.
		#       There must be a better way to grab screen content.
		# img = pyautogui.screenshot(region=(0,0,2560,1440))#navigator.GAME_REGION)
		img = pyautogui.screenshot(region=navigator.GAME_REGION)
		# img.save("debug/buffer %.20f.png" % time.time()) # Don't enable this unless the while-loop is limited. It writes a lot of files...
		frame = np.array(img)
		buffer_lock.acquire()
		buffer.append(frame)
		if len(buffer) > FRAME_RATE * BUFFER_DURATION:
				buffer.pop(0)
		buffer_lock.release()
		time.sleep(1 / FRAME_RATE)

def save_video():
	with buffer_lock:
			if len(buffer) == 0:
				print("Empty debug video buffer, exiting")
				return
			current_datetime = time.strftime("%Y-%m-%d %H-%M-%S")
			video_filename = f"debug/{current_datetime} recording.mp4"
			imageio.mimwrite(video_filename, buffer, fps=FRAME_RATE)
			print("Video saved: ", video_filename)
