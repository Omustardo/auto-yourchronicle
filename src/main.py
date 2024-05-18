# Automation for the game YourChronicle

import subprocess
import time
import os
import pyautogui
import threading
import pytesseract
import sys

import common
import navigator
import quest
import ed1
import ed_all
import partial_run

DEBUG_DIR = "debug/"


# TODO: set up logging. https://stackoverflow.com/a/28330410/3184079
#   Logging with indentation based on method calls would be cool.

def initialize():
	# List open windows and ensure that YourChronicle is among them.
	output = subprocess.check_output(["wmctrl", "-l"]).decode()
	if "YourChronicle" not in output:
		print("YourChronicle is not running. It must be started and the game must be loaded.")
		exit()

	print("Moving and Resizing YourChronicle window:")
	# Move the game window to a set location and size. The arguments are:
	# g,x,y,w,h. g is always zero and the rest are straightforward.
	cmd = ["wmctrl", "-F", "-R", "YourChronicle", "-e", ("0,%d,%d,%d,%d" % (
	navigator.WINDOW_TOP_LEFT[0], navigator.WINDOW_TOP_LEFT[1], navigator.GAME_WIDTH, navigator.GAME_HEIGHT))]
	print("$ ", " ".join(cmd))
	subprocess.run(cmd, stdout=subprocess.PIPE)

	print("Setting YourChronicle as the active window")
	# -a means to make the window the active one.
	# -F forces exact and case sensitive matching.
	cmd = ["wmctrl", "-F", "-a", "YourChronicle"]
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

	if not os.path.exists(DEBUG_DIR):
		os.mkdir(DEBUG_DIR)
		print("Created debug directory: ", DEBUG_DIR)


# Save a screenshot to the local "debug/" directory.
def take_screenshot(output_filename):
	img = common.screenshot(region=navigator.GAME_REGION)
	img.save("debug/" + output_filename)


# Save a screenshot based on a region relative to navigator.GAME_REGION
def take_gameregion_screenshot(output_filename, region):
	r = (region[0] + navigator.GAME_REGION[0],
			 region[1] + navigator.GAME_REGION[1],
			 region[2],
			 region[3])
	img = common.screenshot(region=r)
	img.save("debug/" + output_filename)


def must(result):
	if not result:
		sys.exit()


def infinite_dark_ritual():
	for i in range(20000):
		print("try_dark_ritual: ", ed_all.try_dark_ritual())
		print(quest.full_quest_loop())
		time.sleep(30)


def infinite_ed1():
	for i in range(20000):
		ed1.ed1()
		print(quest.full_quest_loop())
		time.sleep(30)


initialize()
take_screenshot("init.png")

#infinite_dark_ritual()

partial_run.partial()
infinite_ed1()

# TODO: take named screenshots at each step to be used for unit testing

# TODO: save a screenshot with regions and their centerpoints highlighted. Very useful for debugging

# TODO: clean text (only alphanumeric? or convert stuff to closest letters, e.g. | to L. 0 vs O is tough.

#TODO: find text, check color of a few pixels. See if it's dark but not black. Or find the average color in a small block?
# Maybe not needed? It seems like tesseract doesn't find text in greyed out areas at all.
#def isButtonGreyedOut(button_text):
#	return False

#TODO: minimize / maximize sub-menus. e.g. the "Sell" menu.
# It seems like tesseract can detect ">Sell" when it's minimized. Not sure if this is consistent enough.

#TODO: Consider making a GUI that allows creating new regions for searching, words to search for, etc.
#  https://stackoverflow.com/a/71946454/3184079 is a good example of the basics
