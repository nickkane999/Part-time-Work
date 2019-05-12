import re
import sys
import os
import datetime
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def loadCMS(cms_path, fileName):
	logFile = open(fileName, "a+")
	
	# Create Selenium Driver; log into CMS system
	driver = startCMS(logFile)	
	logFile.write("Grabbing content\n")
	
	# Goes to correct CMS page and grabs content to upload content 
	driver = setupCMSUpload(driver, cms_path, logFile)
	
	# Uploads and publishes content to CMS
	driver = grabContent(driver, logFile)
	
	# Save content to new file
	writeHTML(cms_path, logFile)
	
	logFile.write("Program Stop: " + str(datetime.datetime.now()) + "\n\n\n")
	logFile.close()
	driver.quit()

def uploadCMS(cms_path, fileName):
	logFile = open(fileName, "a+")
	
	# Create Selenium Driver; log into CMS system
	driver = startCMS(logFile)
	
	logFile.write("Updating new content\n")
	
	# Goes to correct CMS page and grabs content to upload content 
	driver = setupCMSUpload(driver, cms_path, logFile)
	
	# Uploads and publishes content to CMS
	driver = uploadContent(driver, logFile)

	logFile.write("Program Stop: " + str(datetime.datetime.now()) + "\n\n\n")
	logFile.close()
	driver.quit()
# ----------------------------------------------------------------------------------- #

def startCMS(logFile):
	# Set parameters; aren't changed often
	driver_name = "../Data/chromedriver.exe"						# Installed driver needed to run selenium
	user_filename = "../Data/user_info" 							# File path for user login info
	hide_driver = False												# Driver visibility when program runs
	
	# Sets up driver, and logs into CMS
	driver = getDriver(driver_name, hide_driver, user_filename)		# Creates components of driver object
	driver.get("https://cms.miamioh.edu/customauth")				# Open webpage, which redirects to login menu
	loginMiami(driver, user_filename, logFile)						# Completes login process
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

def loginMiami(driver, user_filename, logFile):
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
	logFile.write("Log in was successful\n")

# ----------------------------------------------------------------------------------- #		
	
def setupCMSUpload(driver, cms_path, logFile):
	driver, path_text = getSection(driver, cms_path)						# Finds correct CMS section page
	logFile.write("Setting up update for page: " + cms_path + "\n")
	checkGood = checkSection(driver, path_text, logFile)					# Checks that correct CMS page is displayed; selects the "edit" page
	if checkGood: textContent = getContent(driver, cms_path)				# Gets content for CMS section
	return driver

def setupCMSLoad(driver, cms_path, logFile):
	driver, path_text = getSection(driver, cms_path)						# Finds correct CMS section page
	logFile.write("Setting up update for page: " + cms_path + "\n")
	checkGood = checkSection(driver, path_text, logFile)					# Checks that correct CMS page is displayed; selects the "edit" page
	if checkGood: textContent = getContent(driver, cms_path)				# Gets content for CMS section
	return driver

def getSection(driver, cms_path):
	# Navegate the CMS menu
	path = cms_path.split("_") # "path" is stored as list variable
	path_text = ""
	firstItem = True
	for item in path:
		if firstItem:
			step1a = driver.find_element_by_link_text(item)
			step1a.click()
			firstItem = False
		else:
			step1a = driver.find_elements_by_link_text(item)
			step1a[len(step1a)-1].click()
		path_text += "/" + item
	return driver, path_text
	
def checkSection(driver, path_text, logFile):
	sleep(2)
	src = driver.page_source
	text_found = re.search(r''+path_text, src)
	if text_found:
		logFile.write("Page located in CMS: " + path_text + "\n")
		step1b = driver.find_element_by_link_text("Edit")
		step1b.click()
		return True
	else:
		logFile.write("This is the wrong page: " + text_found + "\nExiting Edit proccess\n")
		return False

def getContent(driver, cms_path):
	# Move all text from file onto 1 line (if not already done)
	# Replace (') with \' to match correct "HTML" format
	count=0
	with open ('../Text Files/HTML/New/' + cms_path + '.txt', 'r', encoding="utf8") as f:
		for line in f:
			textContent = line
			if count > 1:
				break
			count+=1

	with open('../Text Files/HTML/New/' + cms_path + ".txt", encoding="utf8") as file:
		if count > 1:
			textContent =  " ".join(line.strip() for line in file)
		textContent = textContent.replace("'", "\\'")
	
	return textContent

# ----------------------------------------------------------------------------------- #	
	
def uploadContent(driver, logFile):
	editContent(driver, logFile)						# Finds correct CMS editing page
	submitContent(driver, logFile)						# Submits CMS content by going through additional prompted pages
	publishContent(driver, logFile)										# Publishes CMS content
	return driver

def editContent(driver, logFile):
	# Edit content on CMS, submit changes
	sleep(4)
	iframe = driver.find_element_by_xpath('//iframe[@frameborder="0"]')
	driver.switch_to_frame(iframe)
	driver.execute_script("document.body.innerHTML = '%s'" % textContent) # Line may act up due to (quote formatting) issues
	driver.switch_to.default_content()
	step2 = driver.find_element_by_name("formsubmit")
	step2.click()
	logFile.write("Content read into CMS code editor\n")	

def grabContent(driver, logFile):
	sleep(4)
	iframe = driver.find_element_by_xpath('//iframe[@frameborder="0"]')
	driver.switch_to_frame(iframe)
	content = driver.get_attribute("innerHTML")
	logFile.write("Content loaded into python\n")
	
def submitContent(driver, logFile):
	# Spell Check Page
	sleep(2)
	src = driver.page_source
	text_found = re.search(r'Spell Check', src)
	if text_found:
		step3a = driver.find_element_by_name("formsubmit")
		step3a.click()

	# Link Check
	sleep(2)
	src = driver.page_source
	text_found = re.search(r'Link Check', src)
	if text_found:
		step3b = driver.find_element_by_name("formsubmit")
		step3b.click()

	# Accessibility Check
	src = driver.page_source
	text_found = re.search(r'Accessibility Check', src)
	if text_found:
		step3c = driver.find_element_by_name("formsubmit")
		step3c.click()

	logFile.write("Content was successfully edited\n")
	return driver

def publishContent(driver, logFile):
	# Publish Changes
	step4a = driver.find_element_by_class_name("tab-publish")
	step4a.click()
	step4b = driver.find_element_by_name("formsubmit")
	step4b.click()
	logFile.write("Content was successfully published\n\n")
	
def compareHTML(cms_path, logFile, content):
	logFile = open(logFile, "a+")
	fileName = cms_path + ".html"
	if os.path.isfile(fileName):
		with open(fileName, 'r') as file:
			content2 = file.read()
			file.close()
		if content == content2:
			logFile.write("Content in " + fileName + " has not changed.")
		else:
			with open(fileName, 'r') as file:
				content2 = file.write(content)
				file.close()
				logFile.write("New content has been successfully written to new file: " cms_path)
	else:
		file = open(fileName, "w")
		file.write(content)
		file.close()
		logFile.write("New content has been successfully written to new file: " cms_path)