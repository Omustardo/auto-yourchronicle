import time
import sys
import pyautogui

import navigator

def must(result):
	if not result:
		sys.exit()

def spend_sins():
	must(navigator.click_MainMenu_Main_Area("Akashic")) # "Akashic Records"
	# TODO: mouseover and press 'a' rather than this awkward loop. 
	count = 0
	for i in range(50):
		if navigator.click_MainMenu_Main_InstantAction("Inspiration", enable_recursion=False): # "Inspiration+"
			count = count + 1
		else:
			break
	# best effort click the top "Upgrade Action"
	if count < 42:
		navigator.click(520, 130, clicks=50)
	# best effort click the top "Instant Action"
	if count < 42:
		navigator.click(250, 130, clicks=50)

def reincarnate_WillingRevenge():
	greedAll()
	gluttonyAll()
	astral_kill_all()

	must(navigator.click_MainMenu_Option("Ritual"))
	navigator.click(731,660) # TODO: Reincarnation "Detail"
	navigator.click(155,150) # TODO: Willing Revenge
	navigator.click(605,240) # TODO: Reincarnation
	navigator.click(500,655) # TODO: Reincarnation confirmation. This is dependent on no astral bosses being alive. Not sure how to detect "OK" easily.
	time.sleep(20)
	navigator.click(500,655) # "Click to Start"

# consume a specific amount of specified research.
# clickConfig is a map of the position to the number of clicks. {0:2} means to use the topmost greed option two times.
def greed(clickConfig, default_count=0):
	must(navigator.click_MainMenu_Routine_Menu("Greed"))
	for i in range(0,20):
		num_clicks = default_count
		if i in clickConfig:
			num_clicks = clickConfig[i]
		if num_clicks <= 0:
			continue
		navigator.click(815, 143 + i * 24, clicks=num_clicks)

# Consume a reasonable amount of each research.
def greedAll():
	# Click to consume some of each research. Use the click config to customize the value. Negative to skip.
	clickConfig = {
	  0: 5,
	  1: 10,
	  4: 10,
	  6: -1,
	  7: 3,
	  13: -1,
	}
	greed(clickConfig, default_count=1)

def gluttonyAll():
	must(navigator.click_MainMenu_Routine_Menu("Gluttony"))
	# TODO: press 'e' and then confirm to eat everything.
	for i in range(0,10):
		navigator.click(756, 143 + i * 24, clicks=25)

def astral_kill_all():
	if not navigator.click_MainMenu_Main_Area("Astral"):
		return False
	# "Kill all ...".
	return (
		navigator.click_MainMenu_Main_InstantAction("Destroyer", enable_recursion=False)
		and navigator.click_MainMenu_Main_InstantAction("Hermit", enable_recursion=False)
		and navigator.click_MainMenu_Main_InstantAction("Arbitrator", enable_recursion=False)
		and navigator.click_MainMenu_Main_InstantAction("Creator", enable_recursion=False)
		and navigator.click_MainMenu_Main_InstantAction("Dominator", enable_recursion=False))

def try_dark_ritual():
	if not navigator.click_MainMenu_Option("Ritual"):
		return False
	if not navigator.is_region_grayed_out(navigator.MENU_REGIONS__RITUAL__DARKRITUAL_BUTTON):
		# Note: this method can trigger sys.exit. That's probably fine. If it fails then we'd be in a bad state.
		execute_dark_ritual()
		return True
	return False

def execute_dark_ritual():
	print("Executing Dark Ritual")
	astral_kill_all()
	must(navigator.click_MainMenu_Party_TopMenu("Main"))
	must(navigator.select_party(3))
	must(navigator.click_MainMenu_Option("Ritual"))
	navigator.click(470,174) # TODO: Sacred Ritual
	navigator.click(206,938) # TODO: Dark Ritual
	time.sleep(1)
	must(navigator.click_MainMenu_Ritual_ConfirmDarkRitual())
	time.sleep(5)
	navigator.click(470,174) # TODO: Sacred Ritual
	must(navigator.select_party(2))
	greed({0:1, 1:3}, default_count=0)

def wake_from_low_cpu_mode():
	# TODO: put wakeup code elsewhere?
	navigator.click(10, 10) # wake in case it went into low-CPU mode
	time.sleep(5) # wait low-CPU mode to exit
