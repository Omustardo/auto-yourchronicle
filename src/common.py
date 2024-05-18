from PIL import Image
import datetime
import subprocess
import os


# Use a custom screenshot function. The one from pyautogui is not reliable.
# https://gist.github.com/Omustardo/25d14d0bcc8acf3c979b6505c2f136c7
def screenshot(region=None):
	tmp_filename = '.screenshot%s.png' % (datetime.datetime.now().strftime('%Y-%m%d_%H-%M-%S-%f'))
	if not region:
		subprocess.call(['scrot', '-z', tmp_filename])
	else:
		assert len(region) == 4, 'region argument must be a tuple of four ints'
		region = [int(x) for x in region]
		subprocess.call(['scrot', '-z', '-a', ("%d,%d,%d,%d" % tuple(region)), tmp_filename])

	im = Image.open(tmp_filename)
	# force loading before file deletion, Image.open() is lazy
	im.load()
	os.remove(tmp_filename)
	return im
