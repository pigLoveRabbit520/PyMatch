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
	__isFirst = True
	__isGameStart = False
	__formerPoint = None
	EMPTY = -1
	NONE_LINK = 0
	STRAIGHT_LINK = 1
	ONE_CORNER_LINK = 2
	TWO_CORNER_LINK = 3

	def __init__(self):
		self.root = tk.Tk()
		self.root.title(self.__gameTitle)
		self.centerWindow(self.__windowWidth, self.__windowHeigth)
		self.root.minsize(460, 460)

		self.__addComponets()
		self.extractSmallIconList()

		self.root.mainloop()

	def __addComponets(self):
		self.menubar = tk.Menu(self.root, bg="lightgrey", fg="black")

		self.file_menu = tk.Menu(self.menubar, tearoff=0, bg="lightgrey", fg="black")
		self.file_menu.add_command(label="新游戏", command=self.file_new, accelerator="Ctrl+N")

		self.menubar.add_cascade(label="游戏", menu=self.file_menu)
		self.root.configure(menu=self.menubar)

		self.canvas = tk.Canvas(self.root, bg = 'white', width = 450, height = 450)
		self.canvas.pack(side=tk.TOP, pady = 5)
		self.canvas.bind('<Button-1>', self.clickCanvas)
        

	def centerWindow(self, width, height):
	    screenwidth = self.root.winfo_screenwidth()  
	    screenheight = self.root.winfo_screenheight()  
	    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width)/2, (screenheight - height)/2)
	    self.root.geometry(size)


	def file_new(self, event=None):
		self.iniMap()
		self.drawMap()
		self.__isGameStart = True

	def clickCanvas(self, event):
		if self.__isGameStart:
			point = self.getInnerPoint(Point(event.x, event.y))
			# 有效点击坐标
			if point.isUserful() and not self.isEmptyInMap(point):
				if self.__isFirst:
					self.drawSelectedArea(point)
					self.__isFirst= False
					self.__formerPoint = point
				else:
					if self.__formerPoint.isEqual(point):
						self.__isFirst = True
						self.canvas.delete("rectRedOne")
					else:
						linkType = self.getLinkType(self.__formerPoint, point)
						if linkType['type'] != self.NONE_LINK:
							# TODO
							print("连通方式%d" % linkType['type'])
							self.ClearLinkedBlocks(self.__formerPoint, point)
							self.canvas.delete("rectRedOne")
							self.__isFirst = True
						else:
							self.__formerPoint = point
							self.canvas.delete("rectRedOne")
							self.drawSelectedArea(point)

							

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
				point = self.getOuterLeftTopPoint(Point(x, y))
				im = self.canvas.create_image((point.x, point.y), 
					image=self.__icons[self.__map[y][x]], anchor='nw', tags = 'im%d%d' % (x, y))

	'''
	获取内部坐标对应矩形左上角顶点坐标
	'''
	def getOuterLeftTopPoint(self, point):
		return Point(self.getX(point.x), self.getY(point.y))

	'''
	获取内部坐标对应矩形中心坐标
	'''
	def getOuterCenterPoint(self, point):
		return Point(self.getX(point.x) + int(self.__iconWidth / 2), 
				self.getY(point.y) + int(self.__iconHeight / 2))
		
	def getX(self, x):
		return x * self.__iconWidth + self.__delta

	def getY(self, y):
		return y * self.__iconHeight + self.__delta

	'''
	获取内部坐标
	'''
	def getInnerPoint(self, point):
		x = -1
		y = -1

		for i in range(0, self.__gameSize):
			x1 = self.getX(i)
			x2 = self.getX(i + 1)
			if point.x >= x1 and point.x < x2:
				x = i

		for j in range(0, self.__gameSize):
			j1 = self.getY(j)
			j2 = self.getY(j + 1)
			if point.y >= j1 and point.y < j2:
				y = j

		return Point(x, y)

	'''
	选择的区域变红，point为内部坐标
	'''
	def drawSelectedArea(self, point):
		pointLT = self.getOuterLeftTopPoint(point)
		pointRB = self.getOuterLeftTopPoint(Point(point.x + 1, point.y + 1))
		self.canvas.create_rectangle(pointLT.x, pointLT.y, 
				pointRB.x - 1, pointRB.y - 1, outline = 'red', tags = "rectRedOne")


	'''
	消除连通的两个块
	'''
	def ClearLinkedBlocks(self, p1, p2):
		self.__map[p1.y][p1.x] = self.EMPTY
		self.__map[p2.y][p2.x] = self.EMPTY
		self.canvas.delete('im%d%d' % (p1.x, p1.y))
		self.canvas.delete('im%d%d' % (p2.x, p2.y))

	'''
	地图上该点是否为空
	'''
	def isEmptyInMap(self, point):
		if self.__map[point.y][point.x] == self.EMPTY:
			return True
		else:
			return False

	'''
	获取两个点连通类型
	'''
	def getLinkType(self, p1, p2):
		# 首先判断两个方块中图片是否相同
		if self.__map[p1.y][p1.x] != self.__map[p2.y][p2.x]:
			return { 'type': self.NONE_LINK }

		if self.isStraightLink(p1, p2):
			return {
				'type': self.STRAIGHT_LINK
			}
		res = self.isOneCornerLink(p1, p2)
		if not res:
			return {
				'type': self.ONE_CORNER_LINK,
				'p1': res
			}
		res = self.isTwoCornerLink(p1, p2)
		if not res:
			return {
				'type': self.TWO_CORNER_LINK,
				'p1': res['p1'],
				'p2': res['p2']
			}
		return {
			'type': self.NONE_LINK
		}


	'''
	直连
	'''
	def isStraightLink(self, p1, p2):
		start = -1
		end = -1
		# 水平
		if p1.y == p2.y:
			# 大小判断
			if p2.x < p1.x:
				start = p2.x
				end = p1.x
			else:
				start = p1.x
				end = p2.x
			for x in range(start + 1, end):
				if self.__map[p1.y][x] != self.EMPTY:
					return False
			return True
		elif p1.x == p2.x:
			if p1.y > p2.y:
				start = p2.y
				end = p1.y
			else:
				start = p1.y
				end = p2.y
			for y in range(start + 1, end):
				if self.__map[y][p1.x] != self.EMPTY:
					return False
			return True
		return False

	def isOneCornerLink(self, p1, p2):
		pointCorner = Point(p1.x, p2.y)
		if self.isStraightLink(p1, pointCorner) and self.isStraightLink(pointCorner, p2) and self.isEmptyInMap(pointCorner):
			return pointCorner

		pointCorner = Point(p2.x, p1.y)
		if self.isStraightLink(p1, pointCorner) and self.isStraightLink(pointCorner, p2) and self.isEmptyInMap(pointCorner):
			return pointCorner

	def isTwoCornerLink(self, p1, p2):
		for y in range(-1, self.__gameSize + 1):
			pointCorner1 = Point(p1.x, y)
			pointCorner2 = Point(p2.x, y)
			if y == p1.y or y == p2.y:
				continue
			if y == -1 or y == self.__gameSize:
				if self.isStraightLink(p1, pointCorner1) and self.isStraightLink(pointCorner2, p2):
					return {'p1': pointCorner1, 'p2': pointCorner2}
			else:
				if self.isStraightLink(p1, pointCorner1) and self.isStraightLink(pointCorner1, pointCorner2) and self.isStraightLink(pointCorner2, p2):
					return {'p1': pointCorner1, 'p2': pointCorner2}

		# 横向判断
		for x in range(-1, self.__gameSize + 1):
			pointCorner1 = Point(x, p1.y)
			pointCorner2 = Point(x, p2.y)
			if x == p1.x or x == p2.x:
				continue
			if x == -1 or x == self.__gameSize:
				if self.isStraightLink(p1, pointCorner1) and self.isStraightLink(pointCorner2, p2):
					return {'p1': pointCorner1, 'p2': pointCorner2}
			else:
				if self.isStraightLink(p1, pointCorner1) and self.isStraightLink(pointCorner1, pointCorner2) and self.isStraightLink(pointCorner2, p2):
					return {'p1': pointCorner1, 'p2': pointCorner2}


class Point():
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def isUserful(self):
		if self.x >= 0 and self.y >= 0:
			return True
		else:
			return False
					
	'''
	判断两个点是否相同
	'''
	def isEqual(self, point):
		if self.x == point.x and self.y == point.y:
			return True
		else:
			return False

	'''
	克隆一份对象
	'''
	def clone(self):
		return Point(self.x, self.y)


	'''
	改为另一个对象
	'''
	def changeTo(self, point):
		self.x = point.x
		self.y = point.y

MainWindow()


