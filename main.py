#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-10-02 15:19:24
# @Author  : Salamander	(1906747819@qq.com)
# @Link    : http://51lucy.com

import os, random
import tkinter as tk
from PIL import Image, ImageTk

class MainWindow():
	__gameTitle = "连连看游戏"
	__windowWidth = 700
	__windowHeigth = 500
	__icons = []
	__gameSize = 10 # 游戏尺寸
	__iconKind = __gameSize * __gameSize / 4 # 小图片种类数量
	__iconWidth = 40
	__iconHeight = 40
	__map = [] # 游戏地图
	__delta = 25

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
        
		self.extractSmallIconList()

	def centerWindow(self, width, height):
	    screenwidth = self.root.winfo_screenwidth()  
	    screenheight = self.root.winfo_screenheight()  
	    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width)/2, (screenheight - height)/2)
	    self.root.geometry(size)
	def file_new(self, event=None):
		self.iniMap()
		self.drawMap()

	'''
	提取小头像数组
	'''
	def extractSmallIconList(self):
		imageSouce = Image.open(r'images\NARUTO.png')
		for index in range(0, int(self.__iconKind)):
			region = imageSouce.crop((self.__iconWidth * index, 0, 
					self.__iconWidth * index + self.__iconWidth - 1, self.__iconHeight - 1))
			self.__icons.append(ImageTk.PhotoImage(region))

	'''
	初始化地图 存值为0-24
	'''
	def iniMap(self):
		self.__map = [] # 重置地图
		tmpRecords = []
		records = []
		for i in range(0, int(self.__iconKind)):
			for j in range(0, 5):
				tmpRecords.append(i)

		total = self.__gameSize * self.__gameSize
		for x in range(0, total):
			index = random.randint(0, total - x - 1)
			records.append(tmpRecords[index])
			del tmpRecords[index]

		# 一维数组转为二维，y为高维度
		for y in range(0, self.__gameSize):
			for x in range(0, self.__gameSize):
				if x == 0:
					self.__map.append([])
				self.__map[y].append(records[x + y * self.__gameSize])

	'''
	根据地图绘制图像
	'''
	def drawMap(self):
		self.canvas.delete("all")
		for y in range(0, self.__gameSize):
			for x in range(0, self.__gameSize):
				self.canvas.create_image((x * self.__iconWidth + self.__delta, y * self.__iconHeight + self.__delta), 
					image=self.__icons[self.__map[y][x]], anchor='nw')

MainWindow()


