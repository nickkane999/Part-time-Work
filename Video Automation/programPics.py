# All Icons needed for Windows 10 Interface
def loadWindows10Pics():
	directoryArrow1 = "Pics/Windows10/directoryArrowVLC.png"
	directoryArrow2 = "Pics/Windows10/directoryArrowAvi.png"
	enterName = "Pics/Windows10/enterName.png"
	enterName2 = "Pics/Windows10/enterName2.png"
	pics = [directoryArrow1, enterName, enterName2, directoryArrow2]
	return pics

# Gets all pics needed to click on for the "Reformat" Process
def loadReformatPics():
	otherPics = loadWindows10Pics()
	startPic = "Pics/Reformating/startCone.png"
	addPic = "Pics/Reformating/addConvert.png"
	removePic = "Pics/Reformating/removePic.png"
	convertPic1 = "Pics/Reformating/startConvert1.png"
	typeDirectory = "Pics/Reformating/typeDirectory.png"
	convertPic2 = "Pics/Reformating/startConvert2.png"
	doneLoadingPic = "Pics/Reformating/finishedConvert.png"	
	addPic2 = "Pics/Reformating/addConvert2.png"
	pics = [addPic, removePic, convertPic1, typeDirectory, convertPic2, doneLoadingPic, addPic2, otherPics, startPic]
	return pics

def loadAppendPics():
	otherPics = loadWindows10Pics()
	startPic = "Pics/Clipping/noVideos.png"
	mp4Setting = "Pics/Clipping/mp4Settings.png"
	videoSetting = "Pics/Clipping/outputSettings.png"
	mp4Option = "Pics/Clipping/mp4Option.png"
	loadPic = "Pics/Clipping/processingVideo.png"
	pics = [startPic, mp4Setting, videoSetting, mp4Option, loadPic, otherPics]
	return pics
