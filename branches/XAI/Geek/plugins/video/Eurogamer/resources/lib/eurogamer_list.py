#
# Imports
#
from BeautifulSoup import BeautifulStoneSoup, SoupStrainer
from eurogamer_const import __settings__, __language__
from eurogamer_utils import HTTPCommunicator
import os
import re
import sys
import urllib
import xbmc
import xbmcgui
import xbmcplugin
import xml.sax.saxutils
import unicodedata

#
# Main class
#
class Main:
	#
	# Init
	#
	def __init__( self ) :
		#
		# Constants
		#
		self.IMAGES_PATH  = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'images' ) )
		self.THUMBNAIL_RE = re.compile( "background-image: url\((.*)\)" ) 
		
		#
		# Parse parameters...
		#
		if sys.argv[ 2 ][ 1: ] != "" :
			params = dict(part.split('=') for part in sys.argv[ 2 ][ 1: ].split('&'))
			self.channel = params[ 'channel' ]
			self.channel_desc = params[ 'channel_desc' ]
		else :
			params = dict()

		#
		# Settings
		#
		self.video_quality    = __settings__.getSetting ("video_quality")

		# Get page...
		self.current_page     = int ( params.get( "page", "1" ) )

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
		url              = "http://www.eurogamer.net/ajax.php?action=frontpage&page=%i&type=video" % (self.current_page )
		if self.channel == "show" :
			url			 = "http://www.eurogamer.net/ajax.php?action=frontpage&page=%i&topic=egtv-show" % (self.current_page )
		httpCommunicator = HTTPCommunicator()
		htmlSource       = httpCommunicator.get( url )
		
		#
		# Tells us if we have items (so we can display/or not the Next Page)
		#
		self.items = False
		
		#
		# Parse HTML page...
		#
		soupStrainer  = SoupStrainer( "ul" )
		beautifulSoup = BeautifulStoneSoup( htmlSource, parseOnlyThese=soupStrainer )

		# Loop through "playlist" divs...
		uls = beautifulSoup.findAll( "ul", recursive = False )
		for ul in uls:
		
			# skip popular now and popular recently as they will be found at they normal (chronological) position
			ul_id = ul.get( "id" )
			if self.channel == "now" :
				if ul_id != "popular-now" :
					continue
			elif self.channel == "recently" :
				if ul_id != "popular-recently" :
					continue
			else:
				if ul_id != None and ( ul_id == "popular-now" or ul_id == "popular-recently" ) :
					continue
			
			lis = ul.findAll( "li", recursive=False )
			for li in lis :
				# Get A link...
				li_a = li.find("a", recursive=False)				

				# Video page URL
				video_page_url = None
				div_a = li.find( "div", recursive=False )
				if div_a != None :
					h2_a = div_a.find ( "h2", recursive=False )
					if h2_a != None :
						a_a = h2_a.find ( "a", recursive=False)
						if a_a != None :
							video_page_url = a_a[ "href" ]
							
				if (video_page_url == None) :
					continue
				
				# Thumbnail...
				thumbnail = "";
				if (li_a != None) :
					a_style   = li_a[ "style" ]
					if (self.THUMBNAIL_RE.match(a_style)) :
						thumbnail = self.THUMBNAIL_RE.search(a_style).group(1)
						thumbnail = thumbnail.replace("/mirroredfloor/1", "") 
				
				# Title
				title = li.div.h2.a.string.strip()
				# Normalize unicode cause we can find funny accents and they are not properly unicode encoded
				# so we just transform into their ascii equivalent
				title = unicodedata.normalize('NFKD', title).encode("ascii", "ignore")
				
				# Plot
				plot = ""
				p_p = div_a.find ( "p", recursive=False )
				if p_p != None :
					p_plot = p_p.contents[0]
					if ( p_plot != None ) :
						plot = p_plot.strip()
						plot = unicodedata.normalize('NFKD', plot).encode("ascii", "ignore")
				
				play_script_url = '%s?action=play&video_page_url=%s' % ( sys.argv[ 0 ], urllib.quote_plus( video_page_url ) )
				
				# Notify to show Next Page
				self.items = True
				# Add directory entry...
				listitem = xbmcgui.ListItem( title, iconImage=thumbnail, thumbnailImage=thumbnail )
				listitem.setInfo( "video", { "Title" : title, "Studio" : "Eurogamer", "Plot" : plot } )
				xbmcplugin.addDirectoryItem( handle=int(sys.argv[ 1 ]), url=play_script_url, listitem=listitem, isFolder=False)
				

		# Next page...
		if self.items and self.channel != "now" and self.channel != "recently" :
			listitem = xbmcgui.ListItem (__language__(30401), iconImage = "DefaultFolder.png", thumbnailImage = os.path.join(self.IMAGES_PATH, 'next-page.png'))
			xbmcplugin.addDirectoryItem( handle = int(sys.argv[1]), url = "%s?action=list&channel=%s&channel_desc=%s&page=%i" % ( sys.argv[0], self.channel, self.channel_desc, self.current_page + 1 ), listitem = listitem, isFolder = True)
			
		# Disable sorting...
		xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
		
		# End of directory...
		xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
		
	#
	# Convert HTML to readable strings...
	#
	def html2text ( self, html ):
		return xml.sax.saxutils.unescape( html, { "&#39;" : "'" } )
