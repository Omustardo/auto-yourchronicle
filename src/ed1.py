# Generally:
# Leave village alone
# Get to level 39 to graduate
# Graduate
# Kill Demon King
# Reincarnate

import sys
import time
import datetime

import ed_all
import navigator

def must(result):
	if not result:
		sys.exit()

#def retry(result):
#	

# TODO: minimize the use of the queue.

# Requirements:
# # Title: ? God's Guidance for destiny regen?
# # Queue:
# ## Loop: craft durable leather, tan pelt, farmwork, pray
# ## Other: Make Firewood
# # Party slot 2:
# ## Immortal Rat (pelt regen), Tree Golem (wood regen), Golden Slime (gold regen), Troll (tanning and durable leather boost),
# ## Optional Party:  Elder Treant (apple regen), Forest Fairy (herb regen), Charity Larva (pray bonus), Rock Bird (stone regen, ), Fire Drake (stat boost),
# # Party slot 3:
# ## Anything that boosts sacred ritual and dark ritual.
#
# # Settings:
# ## Enable "Reverse Dungeon Hotkey"
# ## Disable "Next Action Window"
#
# TODO: disable Dark Ritual confirmation popup?
def ed1():
	init()
	ed1_0_village()
	ed1_1_forest()
	ed1_2_academic()
	must(ed1_3_wait_for_graduation_rank())
	ed1_4_finishup()
	ed_all.spend_sins()
	ed_all.reincarnate_WillingRevenge()

def init():
	navigator.select_party(2)

def ed1_0_village():
	must(navigator.click_MainMenu_Main_Area("Village"))
	for i in range(4):
		found = navigator.click_MainMenu_Main_UpgradeAction("Talk with Father") # "Talk with Father"
	must(navigator.click_MainMenu_Main_DungeonAction("Training Room", find_nth=1)) # "Training Room". note that there are two matches and we want the second. This only just happens to match the right one.
	must(navigator.click_MainMenu_Main_UpgradeAction("Go to the Village")) # "Go to the Village"
	print("Waiting 105 seconds to get money and experience")
	time.sleep(105)
	must(navigator.click_MainMenu_Main_UpgradeAction("Study in Church")) # "Study in Church"
	print("Waiting 15 seconds for Sacred Ritual to trigger, to unlock 'Permission to go out'")
	time.sleep(15)
	must(navigator.click_MainMenu_Main_UpgradeAction("Permission")) # "Permission to go out"
	must(navigator.click_MainMenu_Main_DungeonAction("Riverbank")) # "Riverbank"
	print("Waiting 60 seconds to complete Riverbank")
	time.sleep(60)
	print("Waiting 30 seconds to collect leather") # is this needed?
	time.sleep(30)
	for i in range(5):
		must(navigator.click_MainMenu_Main_UpgradeAction("Talk with Old Lady")) # "Talk with Old Lady" (spend pelt)
	for i in range(3):
		must(navigator.click_MainMenu_Main_UpgradeAction("Talk with Old Lady")) # "Talk with Old Lady" (spend leather)
	must(navigator.click_MainMenu_Main_DungeonAction("Unlock")) # "Unlock"
	must(navigator.click_MainMenu_Main_DungeonAction("Waterfall")) # "Waterfall"
	print("Waiting 60 seconds to complete Waterfall")
	time.sleep(60)
	must(navigator.click_MainMenu_Main_DungeonAction("Unlock")) # "Unlock"
	must(navigator.click_MainMenu_Main_DungeonAction("Dim Cave")) # "Dim Cave"
	time.sleep(5)
	must(navigator.click_MainMenu_Main_UpgradeAction("Dark Magic Circle")) # "Dark Magic Circle"
	if not navigator.click_MainMenu_Main_UpgradeAction("Girl is Crying", enable_recursion=False): # "A Girl is Crying"
		must(navigator.click_MainMenu_Main_UpgradeAction("AGirl is Crying")) # "A Girl is Crying"
	must(navigator.click_MainMenu_Main_UpgradeAction("Punish the Bullies")) # "Punish the Bullies"
	must(navigator.click_MainMenu_Main_DungeonAction("Edge of Town")) # "Edge of Town"
	time.sleep(20)
	print("Waiting 30 seconds to craft durable leather")
	time.sleep(30)
	must(navigator.click_MainMenu_Main_UpgradeAction("Talk with Old Lady")) # "Talk with Old Lady" (spend durable leather)
	must(navigator.click_MainMenu_Main_UpgradeAction("Craft a Tent")) # "Craft a Tent 5/5" (spend durable leather)
	must(navigator.click_MainMenu_Main_NextAction("Warrior School")) # "Warrior School"
	must(navigator.click_MainMenu_Main_UpgradeAction("Remember me")) # "Remember me!"
	must(navigator.click_MainMenu_Main_UpgradeAction("Talk with Girl")) # "Talk with Girl"  
	must(navigator.click_MainMenu_Main_UpgradeAction("don't play")) # "I don't play"
	must(navigator.click_MainMenu_Main_UpgradeAction("Talk with Father")) # "Talk with Father"
	must(navigator.click_MainMenu_Main_NextAction("Leave the Village Alone")) # "Leave the Village  Alone"

def ed1_1_forest():
	must(navigator.click_MainMenu_Main_Area("Forest"))
	must(navigator.click_MainMenu_Main_DungeonAction("Lostlorn Forest", find_nth=1)) # "Lostlorn Forest".
	print("Waiting 60 seconds to complete Lostlorn Forest")
	time.sleep(60) # TODO: do Unlock when available
	must(navigator.click_MainMenu_Main_DungeonAction("Unlock"))
	must(navigator.click_MainMenu_Main_DungeonAction("Deep")) # "Lostlorn Forest  - Deep".
	print("Waiting 60 seconds to complete Lostlorn Forest - Deep")
	time.sleep(60) # TODO: do Unlock when available
	must(navigator.click_MainMenu_Main_DungeonAction("Unlock"))
	must(navigator.click_MainMenu_Main_DungeonAction("Abyss")) # "Lostlorn Forest  - Abyss".
	print("Waiting 5 seconds to complete Lostlorn Forest - Abyss")
	time.sleep(5)
	must(navigator.click_MainMenu_Main_NextAction("through")) # "Go through the Forest"

def ed1_2_academic():
	must(navigator.click_MainMenu_Main_Area("Academic")) # "Academic City
	must(navigator.click_MainMenu_Main_UpgradeAction("Dormitory")) # "Enroll in a  Dormitory"
	must(navigator.click_MainMenu_Main_UpgradeAction("Entrance Ceremony")) # "Entrance Ceremony"
	for i in range(3):
		must(navigator.click_MainMenu_Main_UpgradeAction("Speech by the")) # "Speech by the  Principal 1/3-3/3"
	must(navigator.click_MainMenu_Main_UpgradeAction("Greet the Teacher")) # "Greet the Teacher". Either one works.
	for i in range(2):
		must(navigator.click_MainMenu_Main_UpgradeAction("Talk with Teacher")) # "Talk with Teacher".
	print("Sleeping 5 minutes to build up gold")
	time.sleep(60 * 5) 

	# These next four aren't needed, but it saves having to deal with picking the right "Talk with Teacher" option later.
	for i in range(4):
		must(navigator.click_MainMenu_Main_UpgradeAction("Talk with Teacher")) # "Talk with Teacher".

	# The remainder of this method isn't required, but is worthwhile once Alchemy is unlocked. Making smelly satchets to
	# generate tons of Stench is a great way to generate alchemy points.
	must(navigator.click_MainMenu_Main_UpgradeAction("Adventurers Guild"))
	for i in range(3):
		must(navigator.click_MainMenu_Main_UpgradeAction("Receptionist"))
	must(navigator.click_MainMenu_Main_UpgradeAction("Delivery of Pelt"))
	must(navigator.click_MainMenu_Main_UpgradeAction("House clean up"))
	must(navigator.click_MainMenu_Main_DungeonAction("Hoarder's House"))
	time.sleep(60) # TODO: do Unlock when available
	must(navigator.click_MainMenu_Main_DungeonAction("Unlock"))
	must(navigator.click_MainMenu_Main_DungeonAction("Sewer"))
	time.sleep(60) # TODO: do Unlock when available
	# There are two identically named interactions with Shady Merchant. The first takes dung and has 4 interactions.
	# The second takes stench twice and then smelly satchets twice.
	# We only need to do one of the stench interactions to be able to make smelly satchets, but might as finish off
	# the dung ones too.
	for i in range(4):
		must(navigator.click_MainMenu_Main_UpgradeAction("Talk with Shady")) # "Talk with Shady  Merchant"
	must(navigator.click_MainMenu_Main_UpgradeAction("Talk with Shady")) # "Talk with Shady  Merchant"

def ed1_3_wait_for_graduation_rank():
	delay = 15
	print("Waiting for rank 39 as a Graduation requirement. Will execute Dark Ritual when possible. Looping roughly every %d seconds" % (delay))
	start_time = datetime.datetime.now()
	for i in range(30000):
		end_time = datetime.datetime.now()
		diff = end_time - start_time
		if diff.total_seconds() > 120 * 60: # 2 hours
			print("Too long has elapsed, giving up on Dark Ritual")
			return False
		current_rank = navigator.get_current_rank()
		if i % 10 == 0:
			print("Current rank:", current_rank)
		if not current_rank:
			print("Failed to find current rank")
			return False
		if current_rank >= 39:
			print("Current rank 39 is high enough to graduate")
			return True
		ed_all.try_dark_ritual()
		time.sleep(delay)
	return False

def ed1_4_finishup():
	must(navigator.click_MainMenu_Main_Area("Academic")) # "Academic City
	must(navigator.click_MainMenu_Main_NextAction("Graduate")) # "Graduate"
	must(navigator.click_MainMenu_Main_UpgradeAction("Talk")) # "Talk with Teacher".
	must(navigator.click_MainMenu_Main_UpgradeAction("Talk")) # "Talk with Teacher".
	must(navigator.click_MainMenu_Main_UpgradeAction("Talk")) # "Talk with Teacher".
	must(navigator.click_MainMenu_Main_NextAction("Fly")) # "Fly Away"
	must(navigator.click_MainMenu_Main_UpgradeAction("Clouds")) # "Above the Clouds"
	must(navigator.click_MainMenu_Main_UpgradeAction("Clouds")) # "Above the Clouds"
	must(navigator.click_MainMenu_Main_UpgradeAction("Clouds")) # "Above the Clouds"
	must(navigator.click_MainMenu_Main_NextAction("Demon")) # "To the Demon Kingdom"
	must(navigator.click_MainMenu_Main_Area("Demon")) # "Demon Kingdom
	must(navigator.click_MainMenu_Main_DungeonAction("Fort")) # "Demon Kingdom -  Fort"
	time.sleep(4)
	must(navigator.click_MainMenu_Main_UpgradeAction("Talk")) # "Talk with Demon  King"
	must(navigator.click_MainMenu_Main_NextAction("Revenge")) # "Willing Revenge"

