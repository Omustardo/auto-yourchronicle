# navigator module holds everything related to interactions with the UI.

import subprocess

import pyautogui
import pytesseract
import cv2
import time
import re
from PIL import ImageEnhance, ImageFilter, Image, ImageDraw
from itertools import chain
import hashlib

import common

# Where to put the game window.
WINDOW_TOP_LEFT = (1400, 100)

# Width and height of the game, not including things handled by the OS like the menu bar.
GAME_WIDTH = 1000
GAME_HEIGHT = 1200

# The game and the window it goes in are separate things. The window is managed by the OS may be different on different systems.
# We only want to focus on the game within the window, so we need to know where exactly that is.
# On my system there are no borders around the game except the menu on top. I found the height of that element by:
# 1. Set the window to a known size:
#  $ wmctrl -R YourChronicle -F -e 0,1000,100,1000,1200
# 2. Take a screenshot of the game window. The delay is provided so that you can switch to it:
#  $ gnome-screenshot --file=/tmp/img.png --window --delay=3
# 3. Check the dimensions of the screenshot and then delete it:
#  $ file /tmp/img.png && rm /tmp/img.png
#  For my system, this shows 1000x1237. So the menu height is 37
TOP_MENU_HEIGHT = 37

GAME_TOP_LEFT = (WINDOW_TOP_LEFT[0], WINDOW_TOP_LEFT[1] + TOP_MENU_HEIGHT)
GAME_BOTTOM_RIGHT = (GAME_TOP_LEFT[0] + GAME_WIDTH, GAME_TOP_LEFT[1] + GAME_HEIGHT)
# X Y W H : of the playable game region
GAME_REGION = (GAME_TOP_LEFT[0], GAME_TOP_LEFT[1], GAME_WIDTH, GAME_HEIGHT)

# The current navigation state. This lets us keep track of where we currently are in the UI. 
menu_state = "MainMenu/"

# Your full screen. Only used for taking debug screenshots.
SCREEN_REGION = (0,0,2560,1440)

# Theoretically, limiting the search to certain screen regions isn't needed, but practically it'll make things much faster and more reliable. The downside is that it's prone to breaking if the screen resizes or new UI elements are added.
# X Y W H
MENU_REGIONS = (GAME_REGION[0] + 3, GAME_REGION[1] + 106, 94, 1020)
MENU_REGIONS__MAIN__AREAS = (GAME_REGION[0] + 103, GAME_REGION[1] + 108, 90, 1020)
MENU_REGIONS__MAIN__INSTANT_ACTIONS = (GAME_REGION[0] + 207, GAME_REGION[1] + 108, 110, 1020)
MENU_REGIONS__MAIN__LOOP_ACTIONS = (GAME_REGION[0] + 337, GAME_REGION[1] + 108, 110, 1020)
MENU_REGIONS__MAIN__UPGRADE_ACTIONS = (GAME_REGION[0] + 467, GAME_REGION[1] + 108, 110, 1020)
MENU_REGIONS__MAIN__NEXT_ACTIONS = (GAME_REGION[0] + 597, GAME_REGION[1] + 108, 110, 1020)
MENU_REGIONS__MAIN__DUNGEON_ACTIONS = (GAME_REGION[0] + 727, GAME_REGION[1] + 108, 110, 1020)

MENU_REGIONS__PARTY__TOP_BAR = (GAME_REGION[0] + 201, GAME_REGION[1] + 73, 650, 30)
# The vertical strip containing all "Edit Complete Recover" quest options (and other options depending on quest state).
MENU_REGIONS__PARTY__QUEST__CURRENT_QUEST_OPTIONS = (GAME_REGION[0] + 423, GAME_REGION[1] + 143, 175, 1000)
# The thin vertical strip containing quest buttons "Give Up", "Complete", or "Select" as quest options.
MENU_REGIONS__PARTY__QUEST__CURRENT_QUEST_ACTION_OPTIONS = (GAME_REGION[0] + 476, GAME_REGION[1] + 143, 521 - 476, 500)
# The squad buttons containing either "Give Up", "Complete", or "Select" as quest options.
# TODO: increase if more than 5 squad slots is possible.
MENU_REGIONS__PARTY__QUEST__SQUAD_OPTION_BUTTONS = [
	(GAME_REGION[0] + 476, GAME_REGION[1] + 147 + 82 * 0, 522 - 476, 163 - 147),
	(GAME_REGION[0] + 476, GAME_REGION[1] + 147 + 82 * 1, 522 - 476, 163 - 147),
	(GAME_REGION[0] + 476, GAME_REGION[1] + 147 + 82 * 2, 522 - 476, 163 - 147),
	(GAME_REGION[0] + 476, GAME_REGION[1] + 147 + 82 * 3, 522 - 476, 163 - 147),
	(GAME_REGION[0] + 476, GAME_REGION[1] + 147 + 82 * 4, 522 - 476, 163 - 147),
]
# The list of available quests or "Empty". Includes the "Set" text area to the right.
MENU_REGIONS__PARTY__QUEST__SELECTION = (GAME_REGION[0] + 600, GAME_REGION[1] + 144, 240, 500)
# Roughly the same as MENU_REGIONS__PARTY__QUEST__SELECTION but broken down into individual quests and not including
# "Set" to the right, because that has a different background color so OCR breaks.
MENU_REGIONS__PARTY__QUEST__SELECTION_REGIONS = [
	(GAME_REGION[0] + 602, GAME_REGION[1] + 145 + 24 * 0, 842 - 602 - 42, 165 - 145),
	(GAME_REGION[0] + 602, GAME_REGION[1] + 145 + 24 * 1, 842 - 602 - 42, 165 - 145),
	(GAME_REGION[0] + 602, GAME_REGION[1] + 145 + 24 * 2, 842 - 602 - 42, 165 - 145),
	(GAME_REGION[0] + 602, GAME_REGION[1] + 145 + 24 * 3, 842 - 602 - 42, 165 - 145),
	(GAME_REGION[0] + 602, GAME_REGION[1] + 145 + 24 * 4, 842 - 602 - 42, 165 - 145),
	(GAME_REGION[0] + 602, GAME_REGION[1] + 145 + 24 * 5, 842 - 602 - 42, 165 - 145),
	(GAME_REGION[0] + 602, GAME_REGION[1] + 145 + 24 * 6, 842 - 602 - 42, 165 - 145),
	(GAME_REGION[0] + 602, GAME_REGION[1] + 145 + 24 * 7, 842 - 602 - 42, 165 - 145),
	(GAME_REGION[0] + 602, GAME_REGION[1] + 145 + 24 * 8, 842 - 602 - 42, 165 - 145),
	(GAME_REGION[0] + 602, GAME_REGION[1] + 145 + 24 * 9, 842 - 602 - 42, 165 - 145),
]
MENU_REGIONS__PARTY__QUEST__SET_REGIONS = [
	(GAME_REGION[0] + 800, GAME_REGION[1] + 145 + 24 * 0, 42, 165 - 145),
	(GAME_REGION[0] + 800, GAME_REGION[1] + 145 + 24 * 1, 42, 165 - 145),
	(GAME_REGION[0] + 800, GAME_REGION[1] + 145 + 24 * 2, 42, 165 - 145),
	(GAME_REGION[0] + 800, GAME_REGION[1] + 145 + 24 * 3, 42, 165 - 145),
	(GAME_REGION[0] + 800, GAME_REGION[1] + 145 + 24 * 4, 42, 165 - 145),
	(GAME_REGION[0] + 800, GAME_REGION[1] + 145 + 24 * 5, 42, 165 - 145),
	(GAME_REGION[0] + 800, GAME_REGION[1] + 145 + 24 * 6, 42, 165 - 145),
	(GAME_REGION[0] + 800, GAME_REGION[1] + 145 + 24 * 7, 42, 165 - 145),
	(GAME_REGION[0] + 800, GAME_REGION[1] + 145 + 24 * 8, 42, 165 - 145),
	(GAME_REGION[0] + 800, GAME_REGION[1] + 145 + 24 * 9, 42, 165 - 145),
]

MENU_REGIONS__ROUTINE__SUBMENU = (GAME_REGION[0] + 103, GAME_REGION[1] + 108, 90, 1020)

MENU_REGIONS__RITUAL__DARKRITUAL_BUTTON = (GAME_REGION[0] + 156, GAME_REGION[1] + 923, 120, 23)
MENU_REGIONS__RITUAL__DARKRITUALCONFIRMATION = (GAME_REGION[0] + 309, GAME_REGION[1] + 509, 350, 350)


# TODO: remove requirement on xdotool.
def is_active_window():
	active_window_id = subprocess.check_output(['xdotool', 'getactivewindow']).decode().strip()
	active_window_name = subprocess.check_output(['xdotool', 'getwindowname', active_window_id]).decode().strip()
	found = "YourChronicle" in active_window_name
	if not found:
		print("Active window: ", active_window_name)
	return found


def screen_coords_from_game_coords(x, y):
	return x + GAME_REGION[0], y + GAME_REGION[1]


def screen_region_from_game_region(region):
	return region[0] + GAME_REGION[0], region[1] + GAME_REGION[1], region[2], region[3]


def game_region_from_screen_region(region):
	return (region[0]-GAME_REGION[0], region[1]-GAME_REGION[1], region[2], region[3])

def game_coords_from_screen_coords(click_coord):
	return (click_coord[0] - GAME_REGION[0], click_coord[1] - GAME_REGION[1])

# In order to use pytesseract, the image needs to be cleaned up so that it's black text on a white background.
# More processing is possible and may help.
# https://stackoverflow.com/a/28936254/3184079
def preprocess_image(image):
	# Convert image to grayscale
	image = image.convert('L')

	# Enhance contrast and sharpness if needed
	#image = ImageEnhance.Contrast(image).enhance(1)  # Adjust the enhancement factor as needed

	# Apply Gaussian blur or median blur to further remove noise
	#image = image.filter(ImageFilter.GaussianBlur(radius=0.01))

	# Apply a threshold. Since the image is grayscale, we can modify each point with a single intensity value.
	#image = image.point(lambda p: 0 if p < 140 else 255)
	return image


# TODO: consider per-color filtering. This could be used to
#r,g,b = image.split()
#threshold = 140
#thresholded_r = r.point(lambda p: p > threshold and 255)
#thresholded_g = g.point(lambda p: p > threshold and 255)
#thresholded_b = b.point(lambda p: p > threshold and 255)
# Merge thresholded channels back into color image
#image = Image.merge('RGB', (thresholded_r, thresholded_g, thresholded_b))
#return image

# Returns an array of tuples, where each tuple is a string and a region (tuple of x,y,w,h).
# [ (found_text, (x,y,w,h)) ]
# x,y coordinates are relative to the provided image.
def get_all_text_regions(img):
	data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
	#print(data)
	boxes = len(data['text'])
	out = []
	for i in range(boxes):
		found_text = data['text'][i].strip()
		if not found_text:
			continue
		region = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
		out.append((found_text, region))


def text_close_enough(got, want):
	# TODO: consider implementing off-by-one detection, or levenstein distance.
	if got == want:
		return True


# Returns a region containing the given text, or None.
# If text is a string it will look for the first exact match, searching from the top left of the screen.
# If text is an array of strings, it will try to find a match for all of them, but since it tokenizes on words it will only return the region for the first word. (e.g. "Talk to Old Lady" returns the region for "Talk"). Note that this doesn't respect the text actually being close together, only that it's found sequentially.
# The input region can be any region on the screen. It doesn't need to be within the game window.
# The region returned is relative to the top left corner of the screen.
#
# ignore_case is self explanatory.
# only_a_z strips out non alphabet characters
# bottom_up switches the order that results are found. Rather than searching top down, it searches from the bottom. This should be used if there are multiple instances of the same text and you want the last rather than the first. TODO: maybe return all matching regions and let the caller decide?
# find_nth determines which text match should be used. For example, "Training Room" is both the section title and an action. Assuming the title is shown on top, find_nth should be 1. 
# recursion_depth is for this method to call itself recursively and shouldn't be used.
# enable_recursion determines whether to recursively search subsections of the image. This is much more likely to find the desired text, but is also much slower. It also has a very bad worst case: if the text isn't in the image it'll continue recursively searching for a long time. If you aren't sure if the text will be there then disable this. Recursion is not guaranteed to work with find_nth. TODO: implement support for find_nth with recursion. Basically need to dedupe findings as they come in, and return upon getting the nth.
def get_text_region(screen_region, text, ignore_case=True, only_a_z=True, find_nth=0, recursion_depth=0,
										enable_recursion=True):
	# Standardize the input as an array of strings.
	if isinstance(text, str):
		text = text.strip().split(" ")
	# Ensure that if any words included spaces, they get split up. This results in an array of arrays, so flatten it.
	nested_text = [t.strip().split(" ") for t in text]
	text = list(chain.from_iterable(nested_text))
	if ignore_case:
		text = [t.lower() for t in text]
	if only_a_z:
		text = [re.sub(r'[^a-zA-Z]', '', t) for t in text]
	# Assume text can't be smaller than some arbitrary minimum, so this method can be called recursively.
	if screen_region[2] < 20 or screen_region[3] < 10 or recursion_depth > 10:
		return None
	img = preprocess_image(common.screenshot(region=screen_region))

	found_region = get_text_region_from_image(img, screen_region, text, ignore_case, only_a_z, find_nth)
	if found_region:
		debug_screenshot_of_regions(screen_regions=[found_region], description="found '%s' at %s" % (text, str(found_region)))
		return found_region
	# Fall back to searching subsections of the given region recursively.
	# In order to avoid subsections cutting off parts of text we care about, it's done in both halves and thirds.
	if not enable_recursion:
		return None
	sub_regions = [
		# Top third
		(screen_region[0], screen_region[1], screen_region[2], int(screen_region[3] / 3)),
		# Top half
		(screen_region[0], screen_region[1], screen_region[2], int(screen_region[3] / 2)),
		# Middle third
		(screen_region[0], screen_region[1] + int(screen_region[3] / 3), screen_region[2], int(screen_region[3] / 3)),
		# Bottom half
		(screen_region[0], screen_region[1] + int(screen_region[3] / 2), screen_region[2], int(screen_region[3] / 2)),
		# Bottom third
		(screen_region[0], screen_region[1] + int(2 * screen_region[3] / 3), screen_region[2], int(screen_region[3] / 3)),
	]
	#debug_screenshot_of_regions(screen_regions=sub_regions, description=" searching for '%s' recursion_depth_%d" % (text, recursion_depth))
	# TODO: switch to BFS instead of DFS.
	for r in sub_regions:
		found_region = get_text_region(r, text, ignore_case=ignore_case, recursion_depth=recursion_depth + 1)
		if found_region:
			return found_region
	return None


# Cache results of get_text_region_from_image to avoid running pytesseract on the same image multiple times.
# All of the important input parameters to the method must match, not just the image and text.
# It maps from a string (a SHA256 digest) to a region where text was found, or None if none was found.
# TODO: unbounded cache growth is bad. Add LRU or a time limit.
getTextRegionFromImage_cache = {}


# get_text_region_from_image returns a region containing the given text, or None.
# If text is a string it will look for the first exact match, searching from the top left of the screen.
# If text is an array of strings, it will try to find a match for all of them, but since it tokenizes on words it will only return the region for the first word. (e.g. "Talk to Old Lady" returns the region for "Talk"). Note that this doesn't respect the text actually being close together, only that it's found sequentially.
# The provided region is only used for caching purposes.
# The returned region is in the space of the provided region, so if you provide a screen_space region,
# then the returned region is also screen_space.
def get_text_region_from_image(img, region, text, ignore_case=True, only_a_z=True, find_nth=0):
	# All of the important input parameters to the method must match, not just the image and text. Otherwise the same
	# image from different screen locations would get cached to the same value. Similarly other state like `menu_state`
	# needs to be included.
	params_str = str(region) + str(text) + " " + str(ignore_case) + " " + str(only_a_z) + " " + str(find_nth) + str(
		menu_state)
	invocation_hash = hashlib.sha256(img.tobytes() + params_str.encode()).hexdigest()
	if invocation_hash in getTextRegionFromImage_cache:
		cached_region = getTextRegionFromImage_cache[invocation_hash]
		print("get_text_region_from_image search for " + str(text) + " hit cached region: " + str(cached_region))
		return cached_region

	data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
	boxes = len(data['text'])
	all_found_text = []
	all_found_text_indices = []  # indices in the original data from pytesseract.
	for i in range(boxes):
		found_text = data['text'][i].strip()
		if not found_text:
			continue
		if ignore_case:
			found_text = found_text.lower()
		if only_a_z:
			found_text = re.sub(r'[^a-zA-Z]', '', found_text)
		all_found_text.append(found_text)
		all_found_text_indices.append(i)

	index = find_index(text, all_found_text, find_nth=find_nth)
	print("index %d of %s in %s" % (index, text, all_found_text))
	if index != -1:
		data_index = all_found_text_indices[index]
		out_region = (data['left'][data_index], data['top'][data_index], data['width'][data_index], data['height'][data_index])
		out_region = (out_region[0]+region[0], out_region[1]+region[1], out_region[2], out_region[3])
		print("Found match for '%s': %s" % (text, all_found_text[index:index + len(text)]))
		getTextRegionFromImage_cache[invocation_hash] = out_region
		return out_region
	getTextRegionFromImage_cache[invocation_hash] = None
	return None


# Returns the index of where arr1 array starts within arr2, or -1.
# For example, find_index([1,2], [0,1,2,3]) returns 1.
# find_nth allows skipping up to the nth match. This is useful if the same values are expected to show up multiple times. find_index([1,2], [0,1,2,3,1,2], find_nth=1)) returns 4,
def find_index(arr1, arr2, find_nth=0):
	count = 0
	try:
		index = arr2.index(arr1[0])
		while index != -1:
			if arr2[index:index + len(arr1)] == arr1:
				if find_nth == count:
					return index
				count += 1
			index = arr2.index(arr1[0], index + 1)
	except ValueError:
		pass
	return -1


# Returns a string of text from the given region. This is meant to be used on a small region. Ideally a single line of text.
def get_text(region):
	img = preprocess_image(common.screenshot(region=region))
	return get_text_from_image(img)


# Cache results of get_text_from_image to avoid running pytesseract on the same image multiple times.
# It maps from a string (a SHA256 digest) to a string of text from the given image. The string may be empty.
# TODO: unbounded cache growth is bad. Add LRU or a time limit.
get_text_from_image_cache = {}


# Returns a string of text from the given image. This is meant to be used on a small image. Ideally a single line of text.
def get_text_from_image(img):
	img_hash = hashlib.sha256(img.tobytes()).hexdigest()
	if img_hash in get_text_from_image_cache:
		cached_text = get_text_from_image_cache[img_hash]
		print("get_text_from_image cache hit for text: " + cached_text)
		return cached_text

	#img.save("debug/get_text_region.png") # TODO: useful for debugging
	data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
	boxes = len(data['text'])
	all_found_text = []
	for i in range(boxes):
		found_text = data['text'][i].strip()
		if not found_text:
			continue
		all_found_text.append(found_text)
	if not all_found_text:
		get_text_from_image_cache[img_hash] = ""
		return ""
	#print("get_text found: ", all_found_text)
	output = " ".join(all_found_text)
	get_text_from_image_cache[img_hash] = output
	return output


# region is a tuple of x,y,w,h
# It is based on screen coordinates and can click outside the game region.
# If offset_region is provided, its x and y coordinates will be used to offset the given region.
def click_region(region, clicks=1, interval=0.1, offset_region=None):
	if offset_region:
		region[0] += offset_region[0]
		region[1] += offset_region[1]
	# Add half of the width and height to get the centerpoint.
	click_coord = (region[0] + int(region[2] / 2),
								 region[1] + int(region[3] / 2))
	print("Clicking the center of screen region=" + str(region) + " -> screen_coords=" + str(click_coord) + " -> game_coords=" + str(game_coords_from_screen_coords(click_coord)))
	if (click_coord[0] < GAME_REGION[0] or click_coord[0] > GAME_REGION[0] + GAME_REGION[2] or
		click_coord[1] < GAME_REGION[1] or click_coord[1] > GAME_REGION[1] + GAME_REGION[3]):
		print("WARNING: clicking outside of game region")
	pyautogui.click(x=click_coord[0], y=click_coord[1], clicks=clicks, interval=interval)
	pyautogui.moveTo(GAME_TOP_LEFT[0], GAME_TOP_LEFT[1])  # get mouse out of the way for taking screenshots.


# Click on coordinates relative to the game window.
def click(x, y, clicks=1, interval=0.1):
	pyautogui.click(x=GAME_TOP_LEFT[0] + x, y=GAME_TOP_LEFT[1] + y, clicks=clicks, interval=interval)
	pyautogui.moveTo(GAME_TOP_LEFT[0], GAME_TOP_LEFT[1])  # get mouse out of the way for taking screenshots.


def move(x, y):
	pyautogui.moveTo(GAME_TOP_LEFT[0] + x, GAME_TOP_LEFT[1] + y)


# Look on the entire game window for text.
#def clickText(text):
#	region = get_text_region(GAME_REGION, text)
#	if not region:
#		print("Failed to find text: ", text)
#		return False
#	click_region(region)

# Open one of the MainMenu/ options:
# Main, Party, Ritual, Routine
def click_MainMenu_Option(menu_name):
	global menu_state
	if menu_state.startswith("MainMenu/" + menu_name + "/"):
		return True
	region = get_text_region(MENU_REGIONS, menu_name)
	if not region:
		print("Failed to find MainMenu option: ", menu_name)
		return False
	click_region(region)
	menu_state = "MainMenu/" + menu_name + "/"
	time.sleep(0.5)  # sleep enough to let the next menu screen load.
	return True

# Take and save a screenshot of the game with the given regions outlined with rectangles.
# Only one of game_regions or screen_regions must be set.
def debug_screenshot_of_regions(screen_regions=[], game_regions=[], description=""):
	if game_regions and screen_regions:
		print("only one of game_regions or screen_regions should be set")
		return
	regions = []
	if screen_regions:
		regions = screen_regions
	if game_regions:
		for game_region in game_regions:
			regions.append((game_region[0] + GAME_REGION[0], game_region[1] + GAME_REGION[1], game_region[2], game_region[3]))
	img = common.screenshot(region=SCREEN_REGION)
	draw = ImageDraw.Draw(img)
	for region in regions:
		# Convert xywh to x1y1 x2y2
		draw.rectangle((region[0], region[1], region[0]+region[2], region[1]+region[3]), outline="red", width=1)
	img.save("debug/regions__%s.png" % (description))


# Open one of the MainMenu/Main/ options:
# Village, Forest, Academic City, ...
def click_MainMenu_Main_Area(menu_name):
	global menu_state
	if menu_state.startswith("MainMenu/Main/" + menu_name + "/"):
		return True
	if not click_MainMenu_Option("Main"):
		return False
	region = get_text_region(MENU_REGIONS__MAIN__AREAS, menu_name)
	if not region:
		print("Failed to find MainMenu/Main/ option: %s" % menu_name)
		return False
	click_region(region)
	menu_state = "MainMenu/Main/" + menu_name + "/"
	return True


# Click into the options on the top of the MainMenu/Party/
# Main, Level Up, Quest, Bestiary, Skill, Equipment
def click_MainMenu_Party_TopMenu(menu_name):
	global menu_state
	if menu_state.startswith("MainMenu/Party/" + menu_name + "/"):
		return True
	if not click_MainMenu_Option("Party"):
		return False
	region = get_text_region(MENU_REGIONS__PARTY__TOP_BAR, menu_name)
	if not region:
		print("Failed to find MainMenu/Party/ option: %s" % menu_name)
		return False
	click_region(region)
	menu_state = "MainMenu/Party/" + menu_name + "/"
	return True


# Click into the options under MainMenu/Routine/
# SacredRitual, Energy, Familiar, ... Greed, Envy
def click_MainMenu_Routine_Menu(menu_name):
	global menu_state
	if menu_state.startswith("MainMenu/Routine/" + menu_name + "/"):
		return True
	if not click_MainMenu_Option("Routine"):
		return False
	# TODO: this is bad. recursive searching would be better.
	known_menu_coords = {
		"Gluttony": (150, 306),
		"Greed": (150, 327),
	}
	if menu_name in known_menu_coords:
		menu_state = "MainMenu/Routine/" + menu_name + "/"
		coord = known_menu_coords[menu_name]
		click(coord[0], coord[1])
		return True
	region = get_text_region(MENU_REGIONS__ROUTINE__SUBMENU, menu_name)
	if not region:
		print("Failed to find MainMenu/Routine/ option: %s" % menu_name)
		return False
	click_region(region)
	menu_state = "MainMenu/Routine/" + menu_name + "/"
	return True


def click_MainMenu_Main_InstantAction(action_name, find_nth=0, enable_recursion=True):
	global menu_state
	if not menu_state.startswith("MainMenu/Main/"):
		print("Trying InstantAction while not in a MainMenu/Main/")
		return False

	region = get_text_region(MENU_REGIONS__MAIN__INSTANT_ACTIONS, action_name, find_nth=find_nth,
													 enable_recursion=enable_recursion)
	if not region:
		print("Failed to find InstantAction: %s" % action_name)
		return False
	click_region(region)
	return True


def click_MainMenu_Main_LoopAction(action_name, find_nth=0, enable_recursion=True):
	global menu_state
	if not menu_state.startswith("MainMenu/Main/"):
		print("Trying LoopAction while not in a MainMenu/Main/")
		return False
	region = get_text_region(MENU_REGIONS__MAIN__LOOP_ACTIONS, action_name, find_nth=find_nth,
													 enable_recursion=enable_recursion)
	if not region:
		print("Failed to find LoopAction: %s" % action_name)
		return False
	click_region(region)
	return True


def click_MainMenu_Main_UpgradeAction(action_name, find_nth=0, enable_recursion=True):
	global menu_state
	if not menu_state.startswith("MainMenu/Main/"):
		print("Trying UpgradeAction while not in a MainMenu/Main/")
		return False
	region = get_text_region(MENU_REGIONS__MAIN__UPGRADE_ACTIONS, action_name, find_nth=find_nth, enable_recursion=enable_recursion)
	if not region:
		print("Failed to find UpgradeAction: %s" % action_name)
		return False
	click_region(region)
	return True


def click_MainMenu_Main_NextAction(action_name, find_nth=0, enable_recursion=True):
	global menu_state
	if not menu_state.startswith("MainMenu/Main/"):
		print("Trying NextAction while not in a MainMenu/Main/")
		return False

	region = get_text_region(MENU_REGIONS__MAIN__NEXT_ACTIONS, action_name, find_nth=find_nth, enable_recursion=enable_recursion)
	if not region:
		print("Failed to find NextAction: %s" % action_name)
		return False
	click_region(region)
	return True


def click_MainMenu_Main_DungeonAction(action_name, find_nth=0, enable_recursion=True):
	global menu_state
	if not menu_state.startswith("MainMenu/Main/"):
		print("Trying DungeonAction while not in a MainMenu/Main/")
		return False

	region = get_text_region(MENU_REGIONS__MAIN__DUNGEON_ACTIONS, action_name, find_nth=find_nth,
													 enable_recursion=enable_recursion)
	if not region:
		print("Failed to find DungeonAction: %s" % action_name)
		return False
	click_region(region)
	return True


def click_MainMenu_Ritual_ConfirmDarkRitual():
	global menu_state
	if menu_state != "MainMenu/Ritual/":
		if not click_MainMenu_Option("Ritual"):
			return False
	time.sleep(1)
	region = get_text_region(MENU_REGIONS__RITUAL__DARKRITUALCONFIRMATION, text="OK", ignore_case=False)
	if not region:
		print("Failed to find Dark Ritual confirmation")
		return False
	click_region(region)
	return True


def get_current_rank():
	if not click_MainMenu_Option("Ritual"):
		print("Failed to get into Ritual menu")
		return None
	# Location of the "Rank XX ", cutting off the right side's " => XX"
	found_text = get_text(screen_region_from_game_region((387, 190, 100, 26)))
	# OCR sometimes has trouble with zero vs o. I've only seen this with "Rank O" but it is theoretically possible with
	# "Rank 10" and others.
	found_text = found_text.replace('O', '0')
	found_text = re.sub(r'[^0-9]', '', found_text)
	if len(found_text) > 0:
		return int(found_text)
	return None

# Determines whether the provided image has a gray background. A dark background generally means that a button is not clickable. The provided region must be based on a region of a screen, rather than being relative to the game window.
def is_region_grayed_out(region):
	img = preprocess_image(common.screenshot(region=region))
	return is_image_grayed_out(img)


def is_image_grayed_out(image):
	pix = most_common_pixel(image)
	if isinstance(pix, int):
		#print("is_region_grayed_out got avg pix =", pix, ". returning ", pix < 225)
		return pix < 225
	if isinstance(pix, tuple):
		gray = (pix[0] + pix[1] + pix[2]) / 3
		#print("is_region_grayed_out got avg pix =", gray)
		return gray < 225
	print("unknown pix", pix, type(pix))
	return False


# Finds the most commonly occurring pixel in an image.
# This is intended to be used to find the background color on a small region, with the assumption that the background has the most pixels.
def most_common_pixel(image):
	width, height = image.size
	pixel_counts = {}

	# Iterate through each pixel and count occurrences
	for y in range(height):
		for x in range(width):
			pixel = image.getpixel((x, y))
			if pixel in pixel_counts:
				pixel_counts[pixel] += 1
			else:
				pixel_counts[pixel] = 1

	# Find the pixel with the highest count
	return max(pixel_counts, key=pixel_counts.get)


def select_party(n):
	if n < 1 or n > 3:
		return False
	if not click_MainMenu_Party_TopMenu("Main"):
		return False
	# TODO: look at screen region and find numbers.
	if n == 1:
		click(110, 170)
		return True
	if n == 2:
		click(135, 170)
		return True
	if n == 3:
		click(160, 170)
		return True
