# encoding: utf-8

import objc
import sys, os, re
import math

from GlyphsApp import *
from GlyphsApp.plugins import *

GlyphsReporterProtocol = objc.protocolNamed( "GlyphsReporter" )

class showAnchorsCompatibility ( NSObject, GlyphsReporterProtocol ):
	
	def init( self ):
		try:
			#Bundle = NSBundle.bundleForClass_( NSClassFromString( self.className() ));
			return self
		except Exception as e:
			self.logToConsole( "init: %s" % str(e) )
	
	def interfaceVersion( self ):
		try:
			return 1
		except Exception as e:
			self.logToConsole( "interfaceVersion: %s" % str(e) )
	
	def title( self ):
		try:
			return "Anchors Compatibility"
		except Exception as e:
			self.logToConsole( "title: %s" % str(e) )
	
	def keyEquivalent( self ):
		try:
			return None
		except Exception as e:
			self.logToConsole( "keyEquivalent: %s" % str(e) )
	
	def modifierMask( self ):
		try:
			return 0
		except Exception as e:
			self.logToConsole( "modifierMask: %s" % str(e) )
	
	def drawForegroundForLayer_( self, Layer ):
		try:
			pass
		except Exception as e:
			self.logToConsole( "drawForegroundForLayer_: %s" % str(e) )
	
	
	def checkAnchors ( self, Layer ):

		thisFont = Glyphs.font
		currentLayer = thisFont.selectedLayers[0]
		thisGlyph = currentLayer.parent
		#ID = 0

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
			
			#ID += 1
	

		fontColor1 = NSColor.colorWithCalibratedRed_green_blue_alpha_( 1, 0, 0, 0.7 )

		def check(currentAnchor):
			if lista.count(currentAnchor.name) != len(thisFont.masters):
				name = currentAnchor.name
				posX = currentAnchor.position.x
				posY = currentAnchor.position.y
				self.drawTextAtPoint( u"%s" % name, (posX+10, posY), 14.0, fontColor1 )

				# mark zero handles:
				NSColor.colorWithCalibratedRed_green_blue_alpha_( 1, 0, 0, 0.7 ).set()
				redCircles = NSBezierPath.alloc().init()
				
				redCircles.appendBezierPath_( self.roundDotForPoint( posX, posY, zoomedHandleSize*2.5 ) )
				redCircles.fill()

		for currentAnchor in currentLayer.anchors:
			check(currentAnchor)

	def roundDotForPoint( self, posX, posY, markerWidth ):
		myRect = NSRect( ( posX - markerWidth * 0.5, posY - markerWidth * 0.5 ), ( markerWidth, markerWidth ) )
		return NSBezierPath.bezierPathWithOvalInRect_(myRect)


	def drawBackgroundForLayer_( self, Layer ):
		try:
			NSColor.colorWithCalibratedRed_green_blue_alpha_( 0.0, 0.5, 0.3, 0.5 ).set()
			self.checkAnchors ( Layer )
		except Exception as e:
			self.logToConsole( "drawBackgroundForLayer_: %s" % str(e) )
	
	def drawBackgroundForInactiveLayer_( self, Layer ):
		try:
			#pass
			NSColor.colorWithCalibratedRed_green_blue_alpha_( 0.0, 0.5, 0.3, 0.5 ).set()
		except Exception as e:
			self.logToConsole( "drawBackgroundForInactiveLayer_: %s" % str(e) )
	
	def needsExtraMainOutlineDrawingForInactiveLayer_( self, Layer ):
		return True
	
	def drawTextAtPoint( self, text, textPosition, fontSize, fontColor):
		try:
			glyphEditView = self.controller.graphicView()
			currentZoom = self.getScale()
			fontAttributes = { 
				NSFontAttributeName: NSFont.labelFontOfSize_( fontSize/currentZoom ),
				NSForegroundColorAttributeName: fontColor }
			displayText = NSAttributedString.alloc().initWithString_attributes_( text, fontAttributes )
			textAlignment = 0 # top left: 6, top center: 7, top right: 8, center left: 3, center center: 4, center right: 5, bottom left: 0, bottom center: 1, bottom right: 2
			glyphEditView.drawText_atPoint_alignment_( displayText, textPosition, textAlignment )
		except Exception as e:
			self.logToConsole( "drawTextAtPoint: %s" % str(e) )
	
	def getHandleSize( self ):
		try:
			Selected = NSUserDefaults.standardUserDefaults().integerForKey_( "GSHandleSize" )
			if Selected == 0:
				return 5.0
			elif Selected == 2:
				return 10.0
			else:
				return 7.0 # Regular
		except Exception as e:
			self.logToConsole( "getHandleSize: HandleSize defaulting to 7.0. %s" % str(e) )
			return 7.0

	def getScale( self ):
		try:
			return self.controller.graphicView().scale()
		except:
			self.logToConsole( "Scale defaulting to 1.0" )
			return 1.0
	
	def setController_( self, Controller ):
		try:
			self.controller = Controller
		except Exception as e:
			self.logToConsole( "Could not set controller" )
	
	def logToConsole( self, message ):
		myLog = "Show %s plugin:\n%s" % ( self.title(), message )
		NSLog( myLog )
