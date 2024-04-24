# Automation for the game YourChronicle
# It was made on Debian 12, but may work for other linux distros. It would some work to run on Windows, but probably not too much.
#
# Required programs:
#  wmctrl for moving and resizing the game window.
#  xdotool for verifying that the YourChronicle window is active.
#
# Setup:
# 1. Create a python virtual environment so we can add python modules without affecting the rest of the computer:
#   Download this github repo and move to the `auto-yourchronicle/src/` dir.
#   python3 -m venv auto-yourchronicle/
# 2. Activate the virtual environment. This will change your shell to look like: "(src) username@/path/to/auto-yourchronicle/src$". If you aren't in an activated virtual environment, then things won't work.
#   source bin/activate
# 3. Install required modules:
#   pip3 install pyautogui pytesseract opencv-python
# 4. Run the program:
#   python3 -u main.py

import subprocess
import time
import os
import pyautogui
import pytesseract
import sys

import navigator
import quest
import ed1
import ed_all
import partial_run

DEBUG_SCREENSHOT_DIR = "screenshots/"

# TODO: set up logging. https://stackoverflow.com/a/28330410/3184079

def initialize():
	# List open windows and ensure that YourChronicle is among them.
	output = subprocess.check_output(["wmctrl", "-l"]).decode()
	if "YourChronicle" not in output:
		print("YourChronicle is not running. It must be started and the game must be loaded.")
		exit()

	print("Moving and Resizing YourChronicle window:")
	# Move the game window to a set location and size. The arguments are:
	# g,x,y,w,h. g is always zero and the rest are straightforward.
	cmd = ["wmctrl", "-F", "-R", "YourChronicle",  "-e", ("0,%d,%d,%d,%d" % (navigator.WINDOW_TOP_LEFT[0], navigator.WINDOW_TOP_LEFT[1], navigator.GAME_WIDTH, navigator.GAME_HEIGHT))]
	print("$ ", " ".join(cmd))
	subprocess.run(cmd, stdout=subprocess.PIPE)

	print("Setting YourChronicle as the active window")
	# -a means to make the window the active one.
	# -F forces exact and case sensitive matching.
	cmd = ["wmctrl",  "-F", "-a", "YourChronicle"]
	print("$ ", " ".join(cmd))
	subprocess.run(cmd, stdout=subprocess.PIPE)
	for i in range(2):
		if navigator.is_active_window():
			break
		time.sleep(1)
	if not navigator.is_active_window():
		print("YourChronicle is not the active window.")
		exit()
	# There seems to be a race condition where the active window isn't actually in the foreground.
	# Sleep to give it a chance.
	time.sleep(0.1)
	print("YourChronicle is the active window.")
	
	if not os.path.exists(DEBUG_SCREENSHOT_DIR):
		os.mkdir(DEBUG_SCREENSHOT_DIR)
		print("Created debug screenshot directory: ", DEBUG_SCREENSHOT_DIR)

# Save a screenshot to the local "screenshots/" directory.
def take_screenshot(output_filename):
	img = pyautogui.screenshot(region=navigator.GAME_REGION)
	img.save("screenshots/" + output_filename)

# Save a screenshot based on a region relative to navigator.GAME_REGION
def take_gameregion_screenshot(output_filename, region):
	r = (region[0] + navigator.GAME_REGION[0],
		region[1] + navigator.GAME_REGION[1],
		region[2],
		region[3])
	img = pyautogui.screenshot(region=r)
	img.save("screenshots/" + output_filename)

def must(result):
	if not result:
		sys.exit()

initialize()
take_screenshot("init.png")
#sys.exit()
#partial_run.partial()
for i in range(20000):
	#ed1.ed1()
	print("try_dark_ritual: ", ed_all.try_dark_ritual())
	print(quest.full_quest_loop())
	time.sleep(30)

# TODO: I'm using pytesseract to identify the same images repeatedly. I could cache results to speed it up, especially
#       for recursive searching. I'd need to save a map from a hash of the image data to the results. Definitely don't
#       save the full screenshot. Often irrelevant parts of the image change (e.g. red progressbar backgrounds on
#       buttons). Should I strip these out?

# TODO: consider keeping a buffer of the N most recent screenshots, and dump them to file if there's an error. Or just a short video clip?

# TODO: take named screenshots at each step to be used for unit testing

# TODO: how to make text recognition more reliable, rather than dealing with fuzziness and fallbacks.

# TODO: save a screenshot with regions and their centerpoints highlighted. Very useful for debugging

# TODO: clean text (only alphanumeric? or convert stuff to closest letters, e.g. | to L

# TODO: "click to the right of". Find text and then search only to the right of it. Useful for something like:
# find "1st squad" and then click the "Complete" button to the right of it.

#TODO: find text, check color of a few pixels. See if it's dark but not black. Or find the average color in a small block?
# Maybe not needed? It seems like tesseract doesn't find text in greyed out areas at all.
#def isButtonGreyedOut(button_text):
#	return False

#TODO: minimize / maximize sub-menus. e.g. the "Sell" menu.
# It seems like tesseract can detect ">Sell" when it's minimized. Not sure if this is consistent enough.
