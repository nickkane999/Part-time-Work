from Gen_CMS import *

def loadCMS(path, file, url, gui, option):
	logFile = open(file, "a+")

	if option == "image": sendMessage(logFile, gui, "This program cannot load images from CMS\n")
	else:
		# Create Selenium Driver; log into CMS system
		driver = startCMS(logFile, gui)
		sendMessage(logFile, gui, "Loading the following file: " + path + "\n")
		
		# Goes to correct CMS page
		driver = setupCMS(driver, path, logFile, gui)
		
		# Uploads and publishes content to CMS
		sendMessage(logFile, gui, "Grabbing html content from CMS wepage: " + path + "\n")
		driver = processContent(driver, logFile, path, url, gui)

		sendMessage(logFile, gui, "Program Stop: " + str(datetime.datetime.now()) + "\n\n")
		logFile.close()
		# driver.quit()
# ----------------------------------------------------------------------------------- #
	
def processContent(driver, logFile, path, url, gui):
	content = grabContent(driver, logFile, gui)				# Finds correct CMS editing page
	compareHTML(path, url, logFile, content, gui)				# Submits CMS content by going through additional prompted pages

def grabContent(driver, logFile, gui):
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
	sendMessage(logFile, gui, "Content read from CMS code editor\n")
	driver.quit()
	return contentC[0]
	
def compareHTML(path, url, logFile, content, gui):
	dir = os.getcwd()
	time = str(datetime.datetime.now())[:-7]
	time = time.replace(":", "-")
	path = path.replace("/", "_")
	fileText = path + "_" + time + ".html"
	fileDirectory = os.path.join(dir, "../current/")
	fileName = os.path.join(dir, "../current/" + fileText)
	fileNameError = os.path.join(dir, "../error/" + fileText)
	newList = glob.glob(fileDirectory + '*' + path + '*')
	
	if newList:
		fileName = newList[0]
		with open(fileName, 'r') as file:
			content2 = file.read().replace("\n", "").rstrip()
			file.close()
		if content == content2: sendMessage(logFile, gui, "File already pulled into current directory: " + fileText + ".\n")
		else:
			sendMessage(logFile, gui, "Pulled file exists, but content changed since last pull. Content changes may be from another person.\n")
			with open(fileNameError, 'w') as file:
				content = reformatContent(content)
				file.write(content)
				file.close()
				sendMessage(logFile, gui, "Pulled content has been successfully written to error folder: " + fileText + ".\n")
	else:
		file = open(fileName, "w")
		content = reformatContent(content)
		file.write(content)
		sendMessage(logFile, gui, "New file written to current directory from content on webpage: " + url + ".\n")
		file.close()
		
def reformatContent(content):
	search = "</\w+>"
	count = 0
	for m in re.finditer(r''+search, content):
		content = content[:m.end()+count] + "\n" + content[m.end()+count:]
		count+=1															# Keeps track of "new string" position
	return(content)
