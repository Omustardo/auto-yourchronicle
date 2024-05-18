# Debugging util to detect screen tearing in screenshots.
# I want to see if it's caused by a specific screenshot library, or if it's inherent to my linux system.

from PIL import Image
import datetime
import subprocess
import os

def take_screenshot(region=None):
	tmpFilename = '.screenshot%s.png' % (datetime.datetime.now().strftime('%Y-%m%d_%H-%M-%S-%f'))
	if not region:
		subprocess.call(['scrot', '-z', tmpFilename])
	else:
		assert len(region) == 4, 'region argument must be a tuple of four ints'
		region = [int(x) for x in region]
		subprocess.call(['scrot', '-z', '-a', ("%d,%d,%d,%d" % tuple(region)), tmpFilename])

	im = Image.open(tmpFilename)
	# force loading before file deletion, Image.open() is lazy
	im.load()
	os.remove(tmpFilename)
	return im

base_image = take_screenshot(region=(0,0, 2000, 1000))
base_image.save("debug/screen_tearing/base_image.png")
for i in range(100):
	img = take_screenshot(region=(0,0, 2000, 1000))
	#if images_are_equal(base_image, img):
	#	print("%d eq" % i)
	#else:
	#	print("iteration %d not equal" % i)
	img.save("debug/screen_tearing/%d.png" % i)
