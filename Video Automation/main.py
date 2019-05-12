from Video_Editor import *

# Enter Parameters
newVideo = "Test Video.mp4"
mtsDirectory = "C:/Users/Nick Kane/Dropbox/Work/School Stuff/HTML Job/Senior/Video Automation/Test Videos/mts"
mp4Directory = "C:/Users/Nick Kane/Dropbox/Work/School Stuff/HTML Job/Senior/Video Automation/Test Videos/mp4"
converterEXE = "C:/Program Files (x86)/VideoLAN/VLC/vlc.exe"
editorEXE = "C:/Program Files/Avidemux 2.7 - 64 bits/avidemux.exe"
logFile = "log.txt"

# Setup Log file
log = open(logFile, "a+")
log.write("Program start: " + str(datetime.datetime.now()) + "\n\n")

# Run Video Converter program
mtsList = getVideoList(mtsDirectory)
log.write("Will now convert following files in VLC to mp4: " + ''.join(mtsList) + "\n")
reformatAllVideos(mtsList, mtsDirectory, converterEXE, mp4Directory, newVideo, log)

# Run Video Appender program
mp4List = getVideoList(mp4Directory)
log.write("Will now append mp4 files in Avidemux: " + ''.join(mp4List) + "\n")
appendAllVideos(mp4List, mp4Directory, editorEXE, log)
log.close()


# Common lines
# os.startfile("C:/Program Files/Avidemux 2.7 - 64 bits/avidemux.exe")
# pyautogui.locateOnScreen(checkIcon, region=checkIconRegion)
# pyautogui.locateOnScreen(checkIcon, region=checkIconRegion)

# Test Code
# time.sleep(2)
# img = "Pics/Windows10/enterName2.png"
# x, y = pyautogui.locateCenterOnScreen(img)
# pyautogui.click(x, y)