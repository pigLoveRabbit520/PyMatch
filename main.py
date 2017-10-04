#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-10-02 15:19:24
# @Author  : Salamander	(1906747819@qq.com)
# @Link    : http://51lucy.com

import os
import tkinter as tk
from PIL import Image, ImageTk

class MainWindow():
	__gameTitle = "连连看游戏"
	__windowWidth = 700
	__windowHeigth = 500

	def __init__(self):
		self.root = tk.Tk()
		self.root.title(self.__gameTitle)
		self.centerWindow(self.__windowWidth, self.__windowHeigth)

		self.__addComponets()
		self.root.mainloop()

	def __addComponets(self):
		self.menubar = tk.Menu(self.root, bg="lightgrey", fg="black")

		self.file_menu = tk.Menu(self.menubar, tearoff=0, bg="lightgrey", fg="black")
		self.file_menu.add_command(label="新游戏", command=self.file_new, accelerator="Ctrl+N")

		self.menubar.add_cascade(label="游戏", menu=self.file_menu)
		self.root.configure(menu=self.menubar)

		self.canvas = tk.Canvas(self.root, bg = 'white', width = 450, height = 450)
		self.canvas.pack(side=tk.TOP, pady = 5)
        
		#self.canvas.grid(row = 0, padx = 5, pady = 5, sticky='ne')

		x = 0
		y = 0
		w = 40
		h = 40

		im = Image.open(r'images\NARUTO.png')
		region = im.crop((x, y, x+w, y+h))

		photo = ImageTk.PhotoImage(region)
		self.root.photo = photo  # to prevent the image garbage collected.
		self.canvas.create_image((0,0), image=photo, anchor='nw')

	def centerWindow(self, width, height):
	    screenwidth = self.root.winfo_screenwidth()  
	    screenheight = self.root.winfo_screenheight()  
	    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width)/2, (screenheight - height)/2)
	    self.root.geometry(size)
	def file_new(self, event=None):
		i = 10


MainWindow()


