import pyautogui
import time
import sys, os
import datetime
from genClicker import *

# Converts one mts video
def convertVideo(loadDirectory, saveDirectory, video, pics, log):
	setupConvert(loadDirectory, pics)
	enterInfo(video, pics[7], log)
	processConversion(saveDirectory, video, pics, log)

# Add video to the convert queue
def setupConvert(directory, pics):
	addPic = pics[0]
	removePic = pics[1]	
	addPic2 = pics[6]
	pyautogui.keyDown('ctrl')
	pyautogui.press('r')
	pyautogui.keyUp('ctrl')
	time.sleep(2)
	
	print(addPic2)
	if pyautogui.locateOnScreen(removePic) == None: click(addPic)
	else:
		clickOffset(addPic2, -60, 0)
		click(removePic)
		click(addPic)
	changeDirectory(directory, pics[7][0])
	time.sleep(2)

# Add save location for converted video; start conversion
def enterInfo(video, window10Pics, log):
	clickOffset(window10Pics[1], 50, 0)
	pyautogui.typewrite(video)
	pyautogui.press('enter')
	log.write("Video has been queued to convert: " + video + "\n")
	time.sleep(2)

# Processes and finishes conversion for a video
def processConversion(directory, video, pics, log):
	convertPic1 = pics[2]
	typeDirectory = pics[3]
	convertPic2 = pics[4]
	doneLoadingPic = pics[5]
	
	isFinished = False
	click(convertPic1)
	clickOffset(typeDirectory, 50, 0)
	pyautogui.typewrite(directory + "/" + video[:-3] + "mp4")
	time.sleep(2)
	click(convertPic2)

	time.sleep(3)
	while not isFinished:
		if pyautogui.locateOnScreen(doneLoadingPic) != None:
			log.write("Video has finished being converted: " + video + "\n")
			isFinished = True
		else:
			time.sleep(2)