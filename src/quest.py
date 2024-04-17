import navigator

def refresh_quest_list():
	# TODO: need to implement clicking the confirmation button.
	if not navigator.click_MainMenu_Party_TopMenu("Quest"):
		return False
	if not complete_or_recover_quests():
		return False
	navigator.click(806, 123) # Click the "Refresh" button
	return True

def complete_or_recover_quests():
	if not navigator.click_MainMenu_Party_TopMenu("Quest"):
		return False
	navigator.click(550,155)
	navigator.click(550,155+80)
	navigator.click(550,155+160)
	navigator.click(550,155+240)

