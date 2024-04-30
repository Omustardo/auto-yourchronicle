
import subprocess
import time
import os
import pyautogui
import pytesseract
import sys

import navigator
import ed1
import ed_all

def must(result):
	if not result:
		sys.exit()

def partial():
	ed1.init()

	#ed1.ed1_0_village()
	#ed1.ed1_1_forest()
	#ed1.ed1_2_academic()
	must(ed1.ed1_3_wait_for_graduation_rank())
	ed1.ed1_4_finishup()
	ed_all.spend_sins()
	ed_all.reincarnate_WillingRevenge()
	pass

# TODO: do Farmwork for the one sandwich. This would speed up leather stuff, and avoid the use of queue slots.

# TODO: implement waiting for an action to be ready. Maybe all of the "navigator.click_" methods need to return a region instead of actually clicking?

