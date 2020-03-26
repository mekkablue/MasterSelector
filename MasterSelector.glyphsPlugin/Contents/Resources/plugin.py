# encoding: utf-8

###########################################################################################################
#
#
#	Master Selector Plugin
#
#	With this plugin you can navigate multi-master Glyphs Files more easily.
#	Slider included.
#
#	Benedikt Bramboeck, 2018
#
###########################################################################################################

from __future__ import print_function
from GlyphsApp import *
from GlyphsApp.plugins import *
from AppKit import NSMenuItem
from vanilla import *



class MasterSelectorWindow(GeneralPlugin):
	@objc.python_method
	def settings(self):
		self.name = 'Master Selector'

	@objc.python_method
	def start(self):
		try: 
			targetMenu = WINDOW_MENU
			newMenuItem = NSMenuItem(self.name, self.showWindow)
			Glyphs.menu[targetMenu].append(newMenuItem)
		except:
			mainMenu = Glyphs.mainMenu()
			s = objc.selector(self.showWindow,signature='v@:@')
			newMenuItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(self.name, s, "")
			newMenuItem.setTarget_(self)
			mainMenu.itemWithTag_(5).submenu().addItem_(newMenuItem)

	@objc.python_method
	def showWindow(self, sender):
		if Glyphs.font is None:
			self.helperWindow("Please open a font first.")
		elif len(Glyphs.font.masters) < 2:
			self.helperWindow("Your font has only 1 master.")
		else:
			mastersList = []
			for m in Glyphs.font.masters:
				mastersList.append(m.name)
			currentMasterIndex = Glyphs.font.masterIndex

			self.windowWidth = 250
			self.windowHeight = 25*len(mastersList)+23+30
			self.w = FloatingWindow((self.windowWidth, self.windowHeight), "Master Selector")
			self.w.radiomasters = RadioGroup((10, 10, -10, 25*len(mastersList)),
	                                mastersList,
	                                callback=self.changeMaster)
			self.w.slider = Slider((10, -35, -10, 23),
	                            tickMarkCount=len(mastersList),
	                            stopOnTickMarks=True,
	                            value=currentMasterIndex,
	                            minValue=0,
	                            maxValue=len(mastersList)-1,
	                            sizeStyle="small",
				    continuous=False,
	                            callback=self.changeMasterSlider)
			
			self.w.open()

	@objc.python_method
	def helperWindow(self, message):
		self.w = FloatingWindow((200, 80), "Master Selector")
		self.w.error = TextBox((10,10,-10,20), message, alignment="center")
		self.w.button = Button((10,40,-10,20), "Close", self.closeWindow)
		self.w.open()

	@objc.python_method
	def closeWindow(self,sender):
		self.w.close()

	@objc.python_method
	def changeMaster(self, sender):
		currentChoice = self.w.radiomasters.get()
		try:
			Glyphs.font.parent.windowController().setMasterIndex_(currentChoice)
			self.w.slider.set(currentChoice)
		except:
			print('BROKEN')
			pass

	@objc.python_method
	def changeMasterSlider(self, sender):
		currentChoice = int(self.w.slider.get())
		try:
			Glyphs.font.parent.windowController().setMasterIndex_(currentChoice)
			self.w.radiomasters.set(currentChoice)
		except:
			print('BROKEN')
			pass

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__


