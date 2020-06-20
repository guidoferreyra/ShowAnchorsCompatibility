# encoding: utf-8

from __future__ import print_function
import objc
import sys, os, re
import math

from GlyphsApp import *
from GlyphsApp.plugins import *

class showAnchorsCompatibility (ReporterPlugin):
	@objc.python_method
	def settings(self):
		self.menuName = "Anchors Compatibility"
	@objc.python_method
	def checkAnchors (self, Layer):

		thisFont = Glyphs.font
		currentLayer = thisFont.selectedLayers[0]
		thisGlyph = currentLayer.parent

		HandleSize = self.getHandleSize()
		scale = self.getScale()
		zoomedHandleSize = HandleSize / scale

		xHeight = thisFont.selectedFontMaster.xHeight
		angle = thisFont.selectedFontMaster.italicAngle
		offset = math.tan(math.radians(angle)) * xHeight/2

		lista = []

		for thisMaster in thisFont.masters: 
			thisMasterId = thisMaster.id
			masterIndex = thisFont.masters.index(thisMaster)
			frontLayers = thisGlyph.layers[thisFont.masters[masterIndex].id]
			
			for thisAnchor in frontLayers.anchors:
				lista.append(str(thisAnchor.name))
			
		fontColor1 = NSColor.colorWithCalibratedRed_green_blue_alpha_(1, 0, 0, 0.7)

		for currentAnchor in currentLayer.anchors:
			if lista.count(currentAnchor.name) != len(thisFont.masters):
				name = currentAnchor.name
				posX = currentAnchor.position.x
				posY = currentAnchor.position.y
				self.drawTextAtPoint(u"%s" % name, (posX+10, posY), 14.0, fontColor1)

				# mark zero handles:
				NSColor.colorWithCalibratedRed_green_blue_alpha_(1, 0, 0, 0.7).set()
				redCircles = NSBezierPath.alloc().init()
				
				redCircles.appendBezierPath_(self.roundDotForPoint(posX, posY, zoomedHandleSize*2.5))
				redCircles.fill()

	@objc.python_method
	def roundDotForPoint(self, posX, posY, markerWidth):
		myRect = NSRect((posX - markerWidth * 0.5, posY - markerWidth * 0.5), (markerWidth, markerWidth))
		return NSBezierPath.bezierPathWithOvalInRect_(myRect)

	@objc.python_method
	def background(self, Layer):
		try:
			NSColor.colorWithCalibratedRed_green_blue_alpha_(0.0, 0.5, 0.3, 0.5).set()
			self.checkAnchors(Layer)
		except Exception as e:
			import traceback
			print(traceback.format_exc())
