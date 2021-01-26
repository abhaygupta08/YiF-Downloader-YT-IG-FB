from tkinter import *
import tkinter
from tkinter import Entry
import requests
from pytube import *
import json
from urllib import *
import urllib.request
from tkinter import ttk
import time
import clint
from clint.textui import progress
import os
import validators
import regex as re

downLink = ""

filename=""
filetype = 0
#FileType deciding part 0-none 1-fbpic 2-fbvid 3-igpic 4-igvid 5-yt

#FUNCTIONS Start
class EntryWithPlaceholder(tkinter.Entry):
	def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey'):
		super().__init__(master)

		self.placeholder = placeholder
		self.placeholder_color = color
		self.default_fg_color = self['fg']

		self.bind("<FocusIn>", self.foc_in)
		self.bind("<FocusOut>", self.foc_out)

		self.put_placeholder()
	def put_placeholder(self):
		self.insert(0, self.placeholder)
		self['fg'] = self.placeholder_color

	def foc_in(self, *args):
		if self['fg'] == self.placeholder_color:
			self.delete('0', 'end')
			self['fg'] = self.default_fg_color

	def foc_out(self, *args):
		if not self.get():
			self.put_placeholder()


def chkforInsta(link):
	global downLink
	global filetype
	socialSite.configure(text="✔ Instagram",fg="white")
	if link.endswith("/") :
		link += "?__a=1"
	else :
		link += "/?__a=1"
	r = requests.session()

	d = requests.get(link, headers = {'User-agent': 'your bot 0.1'})
	if json.dumps(d.json())=="{}":
		mediaType.configure(text="❎ Private Content or Invalid URL :( ",fg="orange")
		return()
	isvideo = json.dumps(d.json()['graphql']['shortcode_media']['is_video'])
	if isvideo=="true":
		filetype = 4
		mediaType.configure(text="✔ Video",fg="white")
		downLink = json.dumps(d.json()['graphql']['shortcode_media']['video_url'])[1:][:-1]
		print(downLink)
		downButton.configure(text="   Download   ",bg="Black")
		downButton.pack()
	elif isvideo=="false":
		filetype = 3
		mediaType.configure(text="✔ Photo",fg="white")
		downLink = json.dumps(d.json()['graphql']['shortcode_media']['display_url'])[1:][:-1]
		print(downLink)
		downButton.configure(text="   Download   ",bg="Black")
		downButton.pack()
	else:
		mediaType.configure(text="❎ Invalid URL :(",fg="orange")

def chkforFb(link):
	global filetype
	global downLink
	html=requests.get(link)
	print(link)
	socialSite.configure(text="✔ Facebook",fg="white")
	if "hd_src:" in html.text:
		url=re.search('hd_src:"(.+?)"',html.text)[1]
		if ".mp4" in url:
			mediaType.configure(text="✔ Video",fg="white")
			downLink = url
			filetype = 2
			downButton.configure(text="   Download   ",bg="Black")
			downButton.pack()
		else:
			mediaType.configure(text="❎ Private Content or Invalid URL :( ",fg="orange")
	

	elif "/photos/" in link:
		if link.startswith("https://www."):
			link=link.replace("https://www.","https://mbasic.")
		elif link.startswith("https://m."):
			link=link.replace("https://m.","https://mbasic.")
		html=requests.get(link)
		url=re.findall('<img src="(.+?)"',html.text)[1]
		url=url.replace("&amp;","&")
		if ".jpg" in url:
			mediaType.configure(text="✔ Photo",fg="white")
			downLink = url
			filetype = 1
			downButton.configure(text="   Download   ",bg="Black")
			downButton.pack()
			print(url)
		else:
			mediaType.configure(text="❎ Private Content or Invalid URL :( ",fg="orange")
	else:
		mediaType.configure(text="❎ Private Content or Invalid URL :( ",fg="orange")


def chkforUtube(link):
	global filetype
	global downLink
	socialSite.configure(text="✔ Youtube",fg="white")
	downLink = link
	filetype = 5
	downButton.configure(text="   Download   ",bg="Black")
	downButton.pack()
#    strm.download()

def downloadMedia():
	global downLink
	global filename
	if filetype is 1:
		#fbpic
		## FileName deciding part
		if ".jpg" in downLink:
			filename = re.findall('\/[^\/"]+.jpg',downLink)[0][1:]
		elif ".png" in downLink:
			filename = re.findall('\/[^\/"]+.png',downLink)[0][1:]
		elif ".jpeg" in downLink:
			filename = re.findall('\/[^\/"]+.jpeg',downLink)[0][1:]
## FileName deciding Ends
#		urllib.request.urlretrieve(downLink,filename)

	if filetype is 2:
		#fbpvid
		## FileName deciding part
		if ".mp4" in downLink:
			filename = re.findall('\/[^\/"]+.mp4',downLink)[0][1:]
## FileName deciding Ends
#		urllib.request.urlretrieve(downLink,filename)
	if filetype is 3:
		#igpic
		filename = re.findall("(.+?).jpg",downLink.split('/')[6])[0]
#		urllib.request.urlretrieve(downLink, '{}.jpg'.format(filename))
	if filetype is 4:
		#igvid
		filename = re.findall("(.+?).mp4",downLink.split('/')[5])[0]
#		urllib.request.urlretrieve(downLink,'{}.mp4'.format(filename))
	if filetype is 5:
		#yt
#		downLink.download()
		print("YT")
	downButton.configure(text="   Downloading...   ",bg="White",fg="Black",state="disabled")
	downButton.pack()
	
def progresBarFxn():
	global downLink
	global filename
	if filetype == 5: #yt
		def progress_func(stream, _chunk, bytes_remaining):
			print("2")
			size = stream.filesize
			progresss['value']=int(((size-bytes_remaining)/size)*100)
			root.update_idletasks()
			print(((size-bytes_remaining)/size)*100)
			print("progss"+str(progresss['value']))
		progresss['value']=int(10.0)
		print(progresss['value'])
		print("1")  
		progresss['value']=20.0
		yt = YouTube(downLink, on_progress_callback=progress_func)
		print("3")
		progresss['value']=30.0
		video = yt.streams.first()
		print("4")
		video.download()

	else:
		r = requests.get(downLink, stream=True)
		if filetype is 4:
			media = open('{}.mp4'.format(filename), "wb")
		elif filetype is 2:
			media = open(filename, "wb")
		else:
			media = open('{}.jpg'.format(filename), "wb")
		total_length = int(r.headers.get('content-length'))
		for ch in progress.bar(r.iter_content(chunk_size = int(total_length/30)), expected_size=(total_length/1024) + 1):
			if ch:
				media.write(ch)
				progresss['value']+=100/(total_length/int(total_length/30))
				root.update_idletasks()
				time.sleep(1)
	root.bell()
	downButton.configure(text="   Downloaded   ",bg="Black",disabledforeground="white",state="disabled")
	downButton.pack()


#FUNCTIONSend


root=Tk()
root.geometry("550x500")
root.configure(bg="#5e5e5a")
root.title("YiF Downloader | YT/IG/FB | Abhay and Dhirendra")
root.iconphoto(False,PhotoImage(file="logo.png"))
Label(root,text=" ",bg="#5e5e5a").pack()
#Label(root,text=" ",bg="#5e5e5a").pack()

Label(root,text="YiF Downloader",bg="#5e5e5a",fg="White",font=("Impacted 2.0",32)).pack()
Label(root,text="[YouTube    Instagram    Facebook]",bg="#5e5e5a",fg="White",font=("Helvetica",13)).pack()

Label(root,text=" ",bg="#5e5e5a").pack()
Label(root,text=" ",bg="#5e5e5a").pack()

socialSite = Label(root,text="",bg="#5e5e5a")
mediaType = Label(root,text="",bg="#5e5e5a")
downButton = Button(root, text="", bg="#5e5e5a", fg="White",font=("Helvetica",12),command=lambda:[downloadMedia(), progresBarFxn()],state="normal")
####PROGRESS baR
progresss = ttk.Progressbar(root,orient=HORIZONTAL,length=200,mode="determinate",maximum=100)



##CutCopyPasteMenu
##source - https://gist.github.com/angeloped/91fb1bb00f1d9e0cd7a55307a801995f
def make_textmenu(root):
	global the_menu
	the_menu = tkinter.Menu(root, tearoff=0)
	the_menu.add_command(label="Cut")
	the_menu.add_command(label="Copy")
	the_menu.add_command(label="Paste")
	the_menu.add_separator()
	the_menu.add_command(label="Select all")

def callback_select_all(event):
	# select text after 50ms
	root.after(50, lambda:event.widget.select_range(0, 'end'))

def show_textmenu(event):
	e_widget = event.widget
	the_menu.entryconfigure("Cut",command=lambda: e_widget.event_generate("<<Cut>>"))
	the_menu.entryconfigure("Copy",command=lambda: e_widget.event_generate("<<Copy>>"))
	the_menu.entryconfigure("Paste",command=lambda: e_widget.event_generate("<<Paste>>"))
	the_menu.entryconfigure("Select all",command=lambda: e_widget.select_range(0, 'end'))
	the_menu.tk.call("tk_popup", the_menu, event.x_root, event.y_root)

make_textmenu(root)

# bind the feature to all Entry widget
root.bind_class("Entry", "<Button-3><ButtonRelease-3>", show_textmenu)
root.bind_class("Entry", "<Control-a>", callback_select_all)



#CutCp MEnu ends



if __name__ == "__main__": 
	url = EntryWithPlaceholder(root, "Enter your url")
	url.pack()
url.configure(width=25,font=("Lucida Console",18))

#https://stackoverflow.com/questions/27820178/how-to-add-placeholder-to-an-entry-in-tkinter

print(url.get())

def chkforinput() :
	inputUrl = url.get()
	inputUrl.strip()
	if url.get()=="Enter your url" or url.get()=="":
		socialSite.configure(text="❎ No Url Entered Please Retype ! :/",fg="orange")
		return()
	if not (inputUrl.startswith("http://") or inputUrl.startswith("https://")):
		inputUrl = "https://"+inputUrl
	if not validators.url(inputUrl):
		socialSite.configure(text="❎Invalid URL :(",fg="orange")
		return()	
	b1.configure(state="disabled")
	print("2nd",inputUrl)
	if "instagram.com" in inputUrl :
		socialSite.configure(text="✔ Instagram")
		chkforInsta(inputUrl)
	elif "facebook.com" in inputUrl or "fb.me" in inputUrl or "fb.watch" in inputUrl :
		chkforFb(inputUrl)
	elif "youtube.com" in inputUrl or "youtu.be" in inputUrl :
		chkforUtube(inputUrl)
		socialSite.configure(text="✔ YouTube")
		downButton.configure(text="   Download   ",bg="Black")
		downButton.pack()
	else :
		socialSite.configure(text="❎ Unsupported URL Type ! :/",fg="orange")
		b1.configure(state="active")
		return()

	

Label(root,text=" ",bg="#5e5e5a").pack()
b1=Button(root, text="   Verify   ", bg="Black", fg="White",font=("Helvetica",12),command=chkforinput)
b1.pack()

socialSite.pack()
mediaType.pack()



downButton.pack_forget()

progresss.pack()

footer = PhotoImage(file="footer.png")
w1 = tkinter.Label(root, image=footer,bg="#5e5e5a").pack(side="bottom",pady=20)



root.mainloop()