import pyautogui
import time
import sys, os
import datetime

# Get list videos in a folder
def getVideoList(directory):
	list = []
	for root, dirs, files in os.walk(directory, topdown=False):
		for name in files:
			list.append(name)
	
	return list

# Covert mts videos to mp4 videos
def reformatAllVideos(videoList, directory, converterProgram, destinationDirectory, newVideo):
	pic = "Pics/Reformating/finishedConvert.png"
	startProgram(converterProgram)
	for x in range(0, len(videoList)):
		convertVideo(directory, destinationDirectory, videoList[x], pic, x+1)


# Appends all mp4 files into one video
def appendAllVideos(videoList, directory, editorProgram):
	loadPic = "Pics/Clipping/processingVideo.png"
	startProgram(editorProgram)
	openEditVideo(videoList[0], directory, loadPic) # Open 1st video
	time.sleep(0.5)
	
	for x in range(1, len(videoList)):
		appendVideo(videoList[x], loadPic)
	
	saveEditVideo("Appended video.mkv")

# Starts up a new program
def startProgram(program):
	im = pyautogui.screenshot()
	os.startfile(program)
	while pyautogui.locateOnScreen(im) != None:
		time.sleep(2)
	print("Program has loaded")



# Easier way to click tab
def tab(times):
	if times == 1: pyautogui.press('tab')
	else:
		for x in range(0, times-1):
			pyautogui.press('tab')
		
def changeDirectory(name):
	pyautogui.keyDown('alt')
	pyautogui.press('d')
	pyautogui.keyUp('alt')
	pyautogui.press('backspace')
	pyautogui.typewrite(name)
	pyautogui.press('enter')

def open():
	pyautogui.keyDown('ctrl')
	pyautogui.press('o')
	pyautogui.keyUp('ctrl')
	
def save():
	pyautogui.keyDown('ctrl')
	pyautogui.press('s')
	pyautogui.keyUp('ctrl')

def append():
	pyautogui.keyDown('ctrl')
	pyautogui.press('a')
	pyautogui.keyUp('ctrl')
	
def setupConverts(directory, count):
	pyautogui.keyDown('ctrl')
	pyautogui.press('r')
	pyautogui.keyUp('ctrl')
	time.sleep(0.5)
	if count <= 1: tab(4)
	else:
		tab(15)
		time.sleep(0.5)
		pyautogui.press('enter')
		tab(5)
	pyautogui.press('enter')
	changeDirectory(directory)
	time.sleep(0.5)	
	
def convertVideo(loadDirectory, saveDirectory, video, pic, count):
	print("Converting video: " + video)
	setupConverts(loadDirectory, count)
	enterInfo(video)	
	startConversion(saveDirectory, video, pic)

def enterInfo(video):
	tab(6)
	pyautogui.typewrite(video)
	tab(2)
	pyautogui.press('enter')

def startConversion(directory, video, pic):
	isFinished = False
	tab(5)
	pyautogui.press('enter')
	time.sleep(0.5)
	tab(1)
	pyautogui.typewrite(directory + "/" + video[:-3] + "mp4")
	tab(10)
	time.sleep(1)
	pyautogui.press('enter')
	time.sleep(3)
	while not isFinished:
		if pyautogui.locateOnScreen(pic) != None:
			print("Found")
			isFinished = True
		else: 
			time.sleep(2)
	
	

# Open video to edit
def openEditVideo(video, directory, loadPic):
	open()
	changeDirectory(directory)
	time.sleep(0.5)
	tab(6)
	pyautogui.typewrite(video)
	tab(2)
	pyautogui.press('enter')
	time.sleep(2)
	while pyautogui.locateOnScreen(loadPic) != None: time.sleep(2)

def appendVideo(video, loadPic):
	append()
	pyautogui.typewrite(video)
	tab(2)
	pyautogui.press('enter')
	time.sleep(2)
	while pyautogui.locateOnScreen(loadPic) != None: time.sleep(2)
	
def saveEditVideo(name):
	save()
	pyautogui.typewrite(name)
	tab(2)
	pyautogui.press('enter')
