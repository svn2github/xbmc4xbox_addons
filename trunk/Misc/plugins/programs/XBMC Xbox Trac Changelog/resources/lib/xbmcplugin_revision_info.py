import sys
import urllib
import xbmc
import xbmcgui

class GUI( xbmcgui.WindowXMLDialog ):
	ACTION_EXIT_SCRIPT = ( 9, 10, )

	#
	# Init
	#
	def __init__( self, *args, **kwargs ):
		# Parse plugin parameters...
		self.params = dict(part.split('=') for part in sys.argv[ 2 ][ 1: ].split( '&' ))
		
		# Prepare parameter values...
		self.title        = urllib.unquote_plus( self.params[ "title"       ] )
		self.dateTime     = urllib.unquote_plus( self.params[ "date-time"   ] )
		self.developer    = urllib.unquote_plus( self.params[ "developer"   ] )
		self.description  = urllib.unquote_plus( self.params[ "description" ] )
				
		# Show dialog window...
		xbmcgui.WindowXML.__init__( self )
		self.doModal()		


	#
	# onInit handler
	#
	def onInit( self ):
		self.getControl( 10 ).setLabel( self.title )
		self.getControl( 20 ).setLabel( self.dateTime )
		self.getControl( 30 ).setLabel( self.developer )
		self.getControl( 40 ).setText ( self.description )
		self.getControl( 50 ).setLabel( xbmc.getLocalizedString(30101) )								# OK button

	#
	# onClick handler
	#
	def onClick( self, controlId ):
		# OK
		if (controlId == 50) :
			self.close()

	#
	# onFocus handler
	#
	def onFocus( self, controlId ):
		pass

	#
	# onAction handler
	#
	def onAction( self, action ):
		if ( action in self.ACTION_EXIT_SCRIPT ):
			self.close()
