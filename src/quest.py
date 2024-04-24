import time

import navigator

def full_quest_loop():
	if not recover_all():
		return False
	if not try_complete_all():
		return False
	if not try_start_new():
		return False
	return maybe_refresh_quest_list()

def maybe_refresh_quest_list():
	print("Determining whether to refresh quests.")
	if not navigator.click_MainMenu_Party_TopMenu("Quest"):
		return False
	for i in range(len(navigator.MENU_REGIONS__PARTY__QUEST__SELECTION_REGIONS)):
		# There's a quest that's either in progress or available to start.
		if "get" in navigator.getText(navigator.MENU_REGIONS__PARTY__QUEST__SELECTION_REGIONS[i]).lower()
			return True
	# If we're here, there aren't any quests remaining.
	_refresh_quest_list()
	return True

# Hidden version of refreshing the quest list which essentially just does it without safeguards around whether
# quests are active. Just use `maybe_refresh_quest_list`.
def _refresh_quest_list():
	# TODO: need to implement clicking the confirmation button.
	if not navigator.click_MainMenu_Party_TopMenu("Quest"):
		return False
	if not recover_all():
		return False
	if not try_complete_all():
		return False
	navigator.click(806, 123) # Click the "Refresh" button
	return True

# Attempt to press the "Complete" button on any active quests.
# If none are found, it is not a failure.
def try_complete_all():
	if not navigator.click_MainMenu_Party_TopMenu("Quest"):
		return False
	for i in range(len(navigator.MENU_REGIONS__PARTY__QUEST__SQUAD_OPTION_BUTTONS)):
		region = navigator.MENU_REGIONS__PARTY__QUEST__SQUAD_OPTION_BUTTONS[i]
		if navigator.getTextRegion(region, "Complete", enable_recursion=False):
			print("Marking squad slot #" + str(i+1) + " complete")
			navigator.clickRegion(region)
			time.sleep(0.2)
	return True

def recover_all():
	if not navigator.click_MainMenu_Party_TopMenu("Quest"):
		return False
	navigator.click(550,155+80*0)
	navigator.click(550,155+80*1)
	navigator.click(550,155+80*2)
	navigator.click(550,155+80*3)
	navigator.click(550,155+80*4)
	return True

# Returns an array of indices for which quests are available to start.
def get_available_quests():
	print("Checking for available quests to start.")
	if not navigator.click_MainMenu_Party_TopMenu("Quest"):
		return None # TODO: This should be an error?
	available_quests = []
	for i in range(len(navigator.MENU_REGIONS__PARTY__QUEST__SELECTION_REGIONS)):
		# Unavailable quests are either empty slots ("Empty"), or they are already in progress which is indicated by "Set"
		# showing up on the far right.
		# "Get" is there for any quest that isn't Empty, but checking for it ensures that there's actually a quest in the
		# region. Otherwise we could be looking at an entirely blank region.
		if (not navigator.getTextRegion(navigator.MENU_REGIONS__PARTY__QUEST__SELECTION_REGIONS[i], "Empty", enable_recursion=False) and
				"get" in navigator.getText(navigator.MENU_REGIONS__PARTY__QUEST__SELECTION_REGIONS[i]).lower() and
		 		not navigator.getTextRegion(navigator.MENU_REGIONS__PARTY__QUEST__SET_REGIONS[i], "Set", enable_recursion=False)):
		 		available_quests.append(i)
	return available_quests

# Returns an array of indices for which squads are available to do quests.
def get_available_squads():
	print("Checking for available squads.")
	if not navigator.click_MainMenu_Party_TopMenu("Quest"):
		return None # TODO: This should be an error?
	available_squads = []
	for i in range(len(navigator.MENU_REGIONS__PARTY__QUEST__SQUAD_OPTION_BUTTONS)):
		region = navigator.MENU_REGIONS__PARTY__QUEST__SQUAD_OPTION_BUTTONS[i]
		if navigator.getTextRegion(region, "Select", enable_recursion=False):
			available_squads.append(i)
	return available_squads

def try_start_new():
	if not navigator.click_MainMenu_Party_TopMenu("Quest"):
		return False
	available_quests = get_available_quests()
	if not available_quests:
		print("No available quests to start.")
		return True
	else:
		print("Found " + str(len(available_quests)) + " available quests.")

	available_squads = get_available_squads()
	if not available_squads:
		print("No available squads to use.")
		return True
	else:
		print("Found " + str(len(available_squads)) + " available squads.")

	# TODO: Rather than matching up the first squad with the first quest, prioritize quests with permanent rewards
	#       and do shorter quests before longer ones.
	started_count = min(len(available_quests), len(available_squads))
	for i in range(started_count):
		print("Squad #" + str(available_squads[i]+1) + " starting quest #" + str(available_quests[0]+1))
		# Select the squad that's available for questing.
		quest_index = available_quests[i]
		squad_index = available_squads[i]
		navigator.clickRegion(navigator.MENU_REGIONS__PARTY__QUEST__SQUAD_OPTION_BUTTONS[squad_index])
		time.sleep(0.2)
		# Select the quest to start.
		navigator.clickRegion(navigator.MENU_REGIONS__PARTY__QUEST__SELECTION_REGIONS[quest_index])
		time.sleep(0.2)
		# Press "OK" to confirm.
		navigator.clickRegion(navigator.MENU_REGIONS__PARTY__QUEST__SET_REGIONS[quest_index])
		time.sleep(0.2)
		started_count = started_count + 1

	print("Started " + str(started_count) + " quest(s).")
	return True
