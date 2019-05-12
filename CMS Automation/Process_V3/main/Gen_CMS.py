import re
import sys
import os
import glob
import datetime
import pyautogui
import tkinter as tk
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def sendMessage(logFile, gui, message):
	logFile.write(message)
	gui.statusArea.insert(tk.INSERT, message)
	gui.master.update()

def startCMS(logFile, gui):
	# Set parameters; aren't changed often
	driver_name = "../Data/chromedriver.exe"						# Installed driver needed to run selenium
	user_filename = "../Data/user_info" 							# File path for user login info
	hide_driver = False												# Driver visibility when program runs
	
	# Sets up driver, and logs into CMS
	driver = getDriver(driver_name, hide_driver, user_filename)		# Creates components of driver object
	driver.get("https://cms.miamioh.edu/customauth")				# Open webpage, which redirects to login menu
	driver = minimizeWindow2(driver)
	loginMiami(driver, user_filename, logFile, gui)					# Completes login process
	return driver

# Moving window out of view during run-processing
def minimizeWindow():
	# Method 1
	pyautogui.keyDown('alt')
	pyautogui.keyDown('space')
	sleep(0.5)
	pyautogui.press('n')
	pyautogui.keyUp('space')
	pyautogui.keyUp('alt')
	sleep(2)

def minimizeWindow2(driver):
	# Method 2
	driver.set_window_position(-2000, 0)
	return driver
	
# Moving window back into view for end (iframe) processing
def maximizeWindow2(driver):
	driver.set_window_position(0, 0)
	sleep(1)
	return driver
	
def getDriver(driver_name, hide_driver, user_filename):
	# Get file path from parent	for user info and driver
	dir = os.path.dirname(__file__)
	user_filename = os.path.join(dir, user_filename)
	driver_name = os.path.join(dir, driver_name)

	# Make web broswer, with display hidden if specified by the user
	if hide_driver:
		chrome_options = Options()
		chrome_options.add_argument("--headless")  
		chrome_options.add_argument("--window-size=1920,1080")
		driver = webdriver.Chrome(executable_path=driver_name, chrome_options=chrome_options)
	else :
		driver = webdriver.Chrome(driver_name)
	return driver

def loginMiami(driver, user_filename, logFile, gui):
	# Get login info from user's text file
	file = open(user_filename + ".txt", "r")
	name = file.readline()
	password = file.readline()
	file.close()

	# Fill login menu
	passInput = driver.find_element_by_name("password")
	passInput.send_keys(password)
	userInput = driver.find_element_by_name("username")
	userInput.send_keys(name)

	sendMessage(logFile, gui, "Log in was successful\n")
	# ----------------------------------------------------------------------------------- #		

def setupCMS(driver, path, logFile, gui):
	driver = getSection(driver, path)						# Finds correct CMS section page	
	sendMessage(logFile, gui, "Found CMS wepage: " + path + "\n")
	return driver
	
def getSection(driver, path):
	# Go to FSB website
	sleep(2)
	step1 = driver.find_element_by_xpath('//a[@title="FSB"]')
	step1.click()

	sleep(2)
	driver.refresh()
	
	# Navegate the CMS menu
	path = path.split("/") # "path" is stored as list variable
	onPage = True
	sleep(2)
	path.pop(0)
	# print(path)
	for item in path:
		step1a = driver.find_elements_by_link_text(item)
		# print(item)
		while len(step1a) <= 1:
			step1b = driver.find_element_by_css_selector(".paginate_button.next")
			step1b.click()
			sleep(3)
			step1a = driver.find_elements_by_link_text(item)
		step1a[len(step1a)-1].click()
		sleep(2)
	return driver