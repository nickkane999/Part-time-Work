import pyautogui
import time
import sys, os
import datetime
# from genClicker import *
from programPics import *
from reformat import * 
from append import *

# Get list videos in a folder
def getVideoList(directory):
	list = []
	for root, dirs, files in os.walk(directory, topdown=False):
		for name in files:
			list.append(name)
	return list

# Starts up a new program
def startProgram(program, im, log):
	os.startfile(program)
	while pyautogui.locateOnScreen(im) != None:
		time.sleep(2)
	log.write("\nProgram has loaded\n")

# Covert mts videos to mp4 videos
def reformatAllVideos(videoList, directory, converterProgram, destinationDirectory, newVideo, log):
	pics = loadReformatPics()
	startProgram(converterProgram, pics[8], log)
	for video in videoList:
		convertVideo(directory, destinationDirectory, video, pics, log)
	
# Appends all mp4 files into one video
def appendAllVideos(videoList, directory, editorProgram, log):
	pics = loadAppendPics()
	startProgram(editorProgram, pics[0], log)
	changeVideoSettings(pics)
	openEditVideo(videoList[0], directory, pics, log) # Open 1st video
	time.sleep(2)
	for x in range(1, len(videoList)):
		appendVideo(videoList[x], pics[1], log)
	saveEditVideo("Appended video.mp4", log)