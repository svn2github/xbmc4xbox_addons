#
# Imports
#
from BeautifulSoup import SoupStrainer, BeautifulSoup, Tag
from eurogamer_const import __settings__, __language__
from eurogamer_utils import HTTPCommunicator
import os
import re
import sys
import urllib
import xbmc
import xbmcgui
import xbmcplugin
import unicodedata

#
# Main class
#
class Main:
	#
	# Init
	#
	def __init__( self ) :
		# Constants
		self.IMAGES_PATH   = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'images' ) )
		self.ENTRY_LIST_RE = re.compile( "(\d+) to (\d+) of (\d+)" )
		
		# Parse parameters...
		params = dict(part.split('=') for part in sys.argv[ 2 ][ 1: ].split('&'))
		self.plugin_category = params[ "plugin_category" ] 
		self.current_page    = int ( params.get( "page", "1" ) )
		self.query           = urllib.unquote( params[ "query" ] )

		# Settings
		self.video_quality   = __settings__.getSetting ("video_quality")

		# Ask for query if none was passed...
		if self.query == "" :
			# ask for the query string (keyboard)...			
			keyboard = xbmc.Keyboard( "", "", False )
			keyboard.doModal()
			if ( keyboard.isConfirmed() ):
				self.query = unicode( keyboard.getText(), "utf-8" )
			else :
				xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=False )
				return

		#
		# Get the videos...
		#
		self.getVideos()
	
	#
	# Get videos...
	#
	def getVideos( self ) :
		#
		# Get HTML page...
		#
		url				 = "http://www.eurogamer.net/search.php?q=%s&type=videos" % ( urllib.quote( self.query ) )
		if ( self.current_page > 1 ):
			url = url + "&start=%s" % ( (self.current_page - 1) * 20 )
		httpCommunicator = HTTPCommunicator()
		htmlSource       = httpCommunicator.get( url )
		
		#
		# Parse HTML page...
		#
		soupStrainer  = SoupStrainer( "ul", { "class" : "list" } )
		beautifulSoup = BeautifulSoup(htmlSource, soupStrainer)

		#
		# Get all the videos found
		# 
		lis = beautifulSoup.findAll( "li", { "class" : "article video" } )
				# No results found...
		if len(lis) == 0 :
			xbmcgui.Dialog().ok( __language__(30008), __language__(30404), self.query )
			xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=False )
			return	
		
		for li in lis:
			
			# video page url
			video_page_url = None
			h2_a = li.find( "h2", recursive=False )
			if h2_a != None :
				a = h2_a.find ( "a", recursive=False )
				if a != None:
					video_page_url = a[ "href" ]
			
			if video_page_url == None:
				continue
			
			# Title
			title = ""
			
			ss = ""
			for cont in a.contents:
				if (isinstance(cont, Tag)):
					ss = ss + cont.contents[0]
				else:
					ss = ss + cont
				
			if ss != "":
				title = ss.strip()
				title = title.replace("&bull;", ".")
				title = title.replace("&#39;", "'")
				title = unicodedata.normalize('NFKD', title).encode("ascii", "ignore")
			
			# Thumbnail
			thumbnail = ""
			img = li.find("img")
			if img != None:
				thumbnail = img[ "src" ]
				
			# Plot
			plot = ""
			span_p = li.find ("span", {"class":"time"})
			
			plot_p = span_p.nextSibling
			if plot_p != None and plot_p.string != None:
				plot = plot_p.string.strip()
				plot = unicodedata.normalize('NFKD', plot).encode("ascii", "ignore")
				

			play_script_url = '%s?action=play&video_page_url=%s' % ( sys.argv[ 0 ], urllib.quote_plus( video_page_url ) )
			
			# Add directory entry...
			listitem = xbmcgui.ListItem( title, iconImage=thumbnail, thumbnailImage=thumbnail )
			listitem.setInfo( "video", { "Title" : title, "Studio" : "Eurogamer", "Plot" : plot } )
			xbmcplugin.addDirectoryItem( handle=int(sys.argv[ 1 ]), url=play_script_url, listitem=listitem, isFolder=False)
		
		# Check if we should show the next page		
		a_next = beautifulSoup.find("a", {"class":"tool next"})
		if a_next != None:
			self.items = True
		else:
			self.items = False

		# Next page...
		if self.items :
			listitem = xbmcgui.ListItem (__language__(30401), iconImage = "DefaultFolder.png", thumbnailImage = os.path.join(self.IMAGES_PATH, 'next-page.png'))
			xbmcplugin.addDirectoryItem( handle = int(sys.argv[1]), url = '%s?action=search-list&query=%s&plugin_category=%s&page=%i' % ( sys.argv[ 0 ], urllib.quote( self.query ), __language__(30008), self.current_page + 1 ), listitem = listitem, isFolder = True)
			
		# Disable sorting...
		xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
		
		# End of directory...
		xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
		
		#
		# Save the query for future use...
		#
		#
		try :
			saved_queries = eval( __settings__.getSetting( "saved_queries" ) )
		except :
			saved_queries = []
		
		# Add the entry to the list...
		try :
			# ... if not already in the list...
			saved_queries.index( self.query )
		except :
			saved_queries.append( self.query )
			
			# Sort the list...
			saved_queries.sort()
			
			# Save queries...
			__settings__.setSetting( "saved_queries", repr( saved_queries ))
