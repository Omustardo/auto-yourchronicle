import time

import navigator

def refresh_quest_list():
	# TODO: need to implement clicking the confirmation button.
	if not navigator.click_MainMenu_Party_TopMenu("Quest"):
		return False
	if not recover_all():
		return False
	# TODO: find all complete quests in one pass, rather than having to process multiple times.
	for i in range(2):
		if not try_complete_all():
			return False
	navigator.click(806, 123) # Click the "Refresh" button
	return True

# Attempt to press the "Complete" button on any active quests.
# If none are found, it is not a failure.
def try_complete_all():
	if not navigator.click_MainMenu_Party_TopMenu("Quest"):
		return False
	complete_button_region = navigator.getTextRegion(navigator.MENU_REGIONS__PARTY__QUEST__CURRENT_QUEST_ACTION_OPTIONS, "Complete", enable_recursion=True)
	# Either no active quests, or no quests are ready to complete.
	if not complete_button_region:
		print("No quests are ready to complete")
		return True
	navigator.clickRegion(complete_button_region, offset_region=navigator.MENU_REGIONS__PARTY__QUEST__CURRENT_QUEST_ACTION_OPTIONS)
	time.sleep(0.2)
	return True

def recover_all():
	if not navigator.click_MainMenu_Party_TopMenu("Quest"):
		return False
	navigator.click(550,155)
	navigator.click(550,155+80)
	navigator.click(550,155+160)
	navigator.click(550,155+240)
	return True

# TODO: Implement this.
# If any quests are available, and there are squads available to do them, start the quests.
# If none are found, it is not a failure.
# TODO: Prioritize quests with permanent rewards, and do shorter quests before longer ones.
def try_start_new():
	print("@@@ try_start_new")
	if not navigator.click_MainMenu_Party_TopMenu("Quest"):
		return False
	select_region = navigator.getTextRegion(navigator.MENU_REGIONS__PARTY__QUEST__CURRENT_QUEST_ACTION_OPTIONS, "Select", enable_recursion=True)
	# Either no active quests, or no quests are ready to complete.
	if not select_region:
		print("No squads are ready")
		return True
	navigator.clickRegion(select_region, offset_region=navigator.MENU_REGIONS__PARTY__QUEST__CURRENT_QUEST_ACTION_OPTIONS)
	time.sleep(0.2)
	# TODO: check whether quests are available.
	return True