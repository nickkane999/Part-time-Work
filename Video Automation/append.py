import pyautogui
import time
import sys, os
import datetime
from genClicker import *

# Get correct save settings as an mp4 file
def changeVideoSettings(pics):
	mp4Setting = pics[1]
	videoSetting = pics[2]
	mp4Option = pics[3]
	
	if pyautogui.locateOnScreen(mp4Setting)== None:
		clickOffset(videoSetting, 0, 30)
		time.sleep(1)
		click(mp4Option)

# Open video to edit
def openEditVideo(video, directory, pics, log):
	loadPic = pics[4]
	windows10Pics = pics[5]	
	winOpen()
	time.sleep(2)
	changeDirectory(directory, windows10Pics[3])
	clickOffset(windows10Pics[2], 50, 0)
	pyautogui.typewrite(video)
	pyautogui.press('enter')
	time.sleep(2)
	while pyautogui.locateOnScreen(loadPic) != None: time.sleep(2)
	log.write("Clip has been added: " + video + "\n")

def appendVideo(video, loadPic, log):
	append()
	time.sleep(1)
	pyautogui.typewrite(video)
	pyautogui.press('enter')
	time.sleep(2)
	while pyautogui.locateOnScreen(loadPic) != None: time.sleep(2)
	log.write("Clip has been appended: " + video + "\n")
	
def saveEditVideo(name, log):
	save()
	pyautogui.typewrite(name)
	pyautogui.press('enter')
	log.write("New appended video has been saved: " + video + "\n")
	