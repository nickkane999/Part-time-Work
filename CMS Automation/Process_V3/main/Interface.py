from tkinter import *
from Load_CMS import *
from Upload_CMS import *

class MyFirstGUI:
	def __init__(self, master):
		self.master = master
		master.title("CMS Program Loading and Uploading")
		master.geometry("800x430")
		
		self.headLabel = Label(master, text="Type the FSB URL you want load or upload HTML content to")
		self.headLabel.grid(row=0, column=0, columnspan=2, pady=20)

		self.option = StringVar(master)
		self.option.set("page") # default value
		self.optionMenu = OptionMenu(master, self.option, "page", "widget", "image")		
		self.optionMenu.grid(row=0, column=2, pady=20)
		
		self.textField = Entry(master, width=120)
		self.textField.grid(row=1, columnspan=3, padx=10)
		
		self.loadButton = Button(master, text="Load", command=self.onLoad)
		self.loadButton.grid(row=2, column=0, padx=20)

		self.uploadButton = Button(master, text="Upload", command=self.onUpload)
		self.uploadButton.grid(row=2, column=1, pady=20)

		self.close_button = Button(master, text="Close", command=master.quit)
		self.close_button.grid(row=2, column=2)
		
		self.statusArea = Text(master)
		self.statusArea.grid(row=3, columnspan=3, padx=10)
		
	def onLoad(self):
		option = self.option.get()
		url = self.textField.get()
		if option == "widget" or option == "image": 
			string = self.textField.get().split("FSB")
			string = string[1]
		elif option == "page": 
			string = self.textField.get().split("miamioh.edu/fsb")
			string = string[1][:-5]
		self.statusArea.insert(INSERT, string)
		self.master.update()
		loadCMS(string, "log.txt", url, self, option)
		
	def onUpload(self):
		option = self.option.get()
		url = self.textField.get()
		if option == "widget" or option == "image": 
			string = self.textField.get().split("FSB")
			string = string[1]
		elif option == "page": 
			string = self.textField.get().split("miamioh.edu/fsb")
			string = string[1][:-5]
		self.master.update()
		uploadCMS(string, "log.txt", url, self, option)
		
	def __str__(self):
		return "Interface class"		
