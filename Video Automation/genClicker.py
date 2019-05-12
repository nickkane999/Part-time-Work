import pyautogui
import time
import sys, os
import datetime

# Clicks center of an image
def	click(img):
	x, y = pyautogui.locateCenterOnScreen(img)
	pyautogui.click(x, y)
	time.sleep(1)
	
# Clicks center of an image, offset by x and y amount
def	clickOffset(img, addX, addY):
	x, y = pyautogui.locateCenterOnScreen(img)
	pyautogui.click(x + addX, y + addY)
	time.sleep(1)

# Easier way to click tab
def tab(times):
	if times == 1: pyautogui.press('tab')
	else:
		for x in range(0, times-1):
			pyautogui.press('tab')

# Simple way to change Windows 10 Directory
def changeDirectory(name, directoryPic):
	# print(directoryPic)
	clickOffset(directoryPic, -20, 0)
	pyautogui.press('backspace')
	pyautogui.typewrite(name)
	pyautogui.press('enter')

# Common shortcut to open file
def winOpen():
	pyautogui.keyDown('ctrl')
	pyautogui.press('o')
	pyautogui.keyUp('ctrl')
	
# Common shortcut to save file
def save():
	pyautogui.keyDown('ctrl')
	pyautogui.press('s')
	pyautogui.keyUp('ctrl')

# Common shortcut to append file
def append():
	pyautogui.keyDown('ctrl')
	pyautogui.press('a')
	pyautogui.keyUp('ctrl')
