# Debugging util to detect screen tearing in screenshots.
# I want to see if it's caused by a specific screenshot library, or if it's inherent to my linux system.

import pyautogui

def images_are_equal(image1, image2):
	if image1.size != image2.size:
		return False
	for x in range(image1.width):
		for y in range(image1.height):
			if image1.getpixel((x, y)) != image2.getpixel((x, y)):
				return False
	return True

base_image = pyautogui.screenshot(region=(0,0, 2000, 1000))
base_image.save("debug/screen_tearing/base_image.png")
for i in range(100):
	img = pyautogui.screenshot(region=(0,0, 2000, 1000))
	#if images_are_equal(base_image, img):
	#	print("%d eq" % i)
	#else:
	#	print("iteration %d not equal" % i)
	img.save("debug/screen_tearing/%d.png" % i)
