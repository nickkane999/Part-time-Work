from Gen_CMS import *

def uploadCMS(path, fileName, url, gui, option):
	logFile = open(fileName, "a+")
	if option == "image":
		sendMessage(logFile, gui, "Functionality for image upload not done yet\n")
		# sendMessage(logFile, gui, "Uploading image into CMS directory: " + path + "\n")
		# uploadImage(driver, logFile, path, url, gui)
	else:
		# Create Selenium Driver; log into CMS system
		driver = startCMS(logFile, gui)
		
		# Goes to correct CMS page
		sendMessage(logFile, gui, "Locating webpage on the following path: " +  path + "\n")
		driver = setupCMS(driver, path, logFile, gui)
		
		# Uploads and publishes content to CMS
		sendMessage(logFile, gui, "Putting updated file into CMS wepage: " + path + "\n")
		uploadContent(driver, logFile, path, url, gui, option)

	sendMessage(logFile, gui, "Program Stop: " + str(datetime.datetime.now()) + "\n\n\n")
	logFile.close()
	# driver.quit()

# def getDriver(driver_name, hide_driver, user_filename):
	# Get file path from parent	for user info and driver
	# dir = os.path.dirname(__file__)
	# user_filename = os.path.join(dir, user_filename)
	# driver_name = os.path.join(dir, driver_name)

	# Make web broswer, with display hidden if specified by the user
	# if hide_driver:
		# chrome_options = Options()
		# chrome_options.add_argument("--headless")  
		# chrome_options.add_argument("--window-size=1920,1080")
		# driver = webdriver.Chrome(executable_path=driver_name, chrome_options=chrome_options)
	# else :
		# driver = webdriver.Chrome(driver_name)
	
	# return driver

# def loginMiami(driver, user_filename, logFile):
	# Get login info from user's text file
	# file = open(user_filename + ".txt", "r")
	# name = file.readline()
	# password = file.readline()
	# file.close()

	# Fill login menu
	# passInput = driver.find_element_by_name("password")
	# passInput.send_keys(password)
	# userInput = driver.find_element_by_name("username")
	# userInput.send_keys(name)
	# logFile.write("Log in was successful\n")
# ----------------------------------------------------------------------------------- #		

def uploadImage(driver, logFile, path, url, gui):
	step1a = driver.find_element_by_xpath('//i[@class="ci ci-add"]')
	step1a.click()
	step1b = driver.find_element_by_xpath('//i[@class="ci ci-folder-o"]')
	step1b.click()
	step1c = driver.find_element_by_xpath('//i[@class="ci ci-file"]')
	step1c.click()

def uploadContent(driver, logFile, path, url, gui, option):
	content = getContent(driver, path, logFile, gui)
	if (content is not None): hasNewContent = editContent(driver, logFile, content, gui)		# Finds correct CMS editing page
	else: hasNewContent = False
	if (hasNewContent):
		submitContent(driver, logFile, gui)														# Submits CMS content by going through additional prompted pages
		publishedContent = publishContent(driver, logFile, gui)									# Publishes CMS content
		if publishedContent: moveContent(logFile, path, url, gui)
		return True
	else: return False

def getContent(driver, path, logFile, gui):
	dir = os.getcwd()
	fileDirectory = os.path.join(dir, "../current/")
	path = path.replace("/", "_")
	newList = glob.glob(fileDirectory + '*' + path + '*')
	
	if newList:
		fileName = newList[0]
		with open(fileName, 'r') as file:
			content = file.read().replace("\n", "").rstrip()
			file.close()
	else:
		sendMessage(logFile, gui, "Content for this CMS wepage could not be located: " + path + "\n")
		content = None
		
	return content
# ----------------------------------------------------------------------------------- #	

def editContent(driver, logFile, newContent, gui):
	# Edit content on CMS, submit changes
	sleep(2)
	edit = driver.find_element_by_xpath('//a[@title="Edit"]')
	edit.click()
	sleep(4)
	iframe = driver.find_element_by_xpath('//iframe[@frameborder="0"]')
	driver.switch_to_frame(iframe)
	content = driver.page_source
	contentA = content.split("<body", 1)
	contentB = contentA[1].split(">", 1)
	contentC = contentB[1].split("</body>", 1)
	# print(contentC[0])
	# print(newContent)
	# print(contentC[0] == newContent)
	if (contentC[0] == newContent):
		sendMessage(logFile, gui, "Content is not new; no upload is necessary\n")
		return False
	newContent = newContent.replace("'", "\\'")
	driver.execute_script("document.getElementById('tinymce').innerHTML = '%s'" % newContent)
		
	driver.switch_to.default_content()
	step2 = driver.find_element_by_id("save-draft-link")
	step2.click()
	sendMessage(logFile, gui, "New content found; upload now starting\n")
	return True

def submitContent(driver, logFile, gui):
	# Spell Check Page
	sleep(2)
	step3a = driver.find_element_by_xpath('//a[@title="Submit"]')
	step3a.click()
	sleep(2)
	step3b = driver.find_element_by_name("submitButtonType")
	step3b.click()

	sendMessage(logFile, gui, "Content was successfully edited\n")
	return driver

def publishContent(driver, logFile, gui):
	# Publish Changes
	# type = "Live"
	type = "Test"
	sleep(4)
	step4 = driver.find_element_by_xpath('//a[@title="Publish"]')
	step4.click()

	# try:
	driver = maximizeWindow2(driver)
	step5 = driver.find_element_by_xpath('//div[@id="publish-settings-header"]//span[@class="title"]')
	if step5.text == 'View Publish Settings':
		step5b = driver.find_element_by_xpath('//div[@id="publish-settings-header"]')
		step5b.click()

	step6 = driver.find_element_by_xpath('//table[@id="destinations-table"]//tr[@data-destination-name="FSB ' + type + '"]')
	if "selected" not in step6.get_attribute('class'):
		step6b = driver.find_element_by_xpath('//table[@id="destinations-table"]//tr[@data-destination-name="FSB ' + type + '"]//td')
		step6b.click()
		
	if type != "Test":
		step6c = driver.find_element_by_xpath('//table[@id="destinations-table"]//tr[@data-destination-name="FSB Test"]')
		if "selected" not in step6c.get_attribute('class'):
			step6d = driver.find_element_by_xpath('//table[@id="destinations-table"]//tr[@data-destination-name="FSB Test"]//td')
			step6d.click()


	sleep(3)
	step7 = driver.find_element_by_id("primary-submit")
	step7.click()
	
	sleep(2)
	step8 = driver.find_element_by_xpath('//a[@title="Dashboard"]')
	step8.click()
	
	sleep(2)
	sendMessage(logFile, gui, "Content was successfully published\n")
	driver = minimizeWindow2(driver)
	return True
	# except:
	# message = "Publish button wasn't found; content was not successfully published\n"
	# sendMessage(logFile, gui, message)
	# return False
	
def moveContent(logFile, path, url, gui):
	dir = os.getcwd()
	time = str(datetime.datetime.now())[:-7]
	time = time.replace(":", "-")
	path = path.replace("/", "_")
	fileText = path + "_" + time + ".html"

	fileDirectory = os.path.join(dir, "../current/")
	newList = glob.glob(fileDirectory + '*' + path + '*')
	fileNamePrev = os.path.join(dir, "../prev/" + fileText)
	
	if newList:
		# print(newList[0])
		fileName = newList[0]
		with open(newList[0], 'r') as file:
			content = file.read()
			file.close()
		file = open(fileNamePrev, "w")
		file.write(content)
		sendMessage(logFile, gui, "New file written to current directory from content on webpage: " + url + "\n\n")
		file.close()
		os.remove(newList[0])