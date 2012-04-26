#
# Imports
#
import os
import sys
import xbmc
import xbmcgui
import xbmcplugin
import urllib
from BeautifulSoup      import BeautifulSoup
from BeautifulSoup      import SoupStrainer
from gametrailers_utils import HTTPCommunicator

#
# Main class
#
class Main:
	#
	# Init
	#
	def __init__( self ) :
		# Constants
		self.DEBUG         = False
		
		# Parse parameters...
		params                = dict(part.split('=') for part in sys.argv[ 2 ][ 1: ].split('&'))
		self.plugin_category  = urllib.unquote_plus( params[ "plugin_category"  ] )
		self.channel_category = urllib.unquote_plus( params[ "channel_category" ] )

		#
		# Get videos (subcategories)
		#
		self.getVideos()
	
	#
	# Get videos...
	#
	def getVideos( self ) :
		# 
		# Get HTML page...
		#
		httpCommunicator = HTTPCommunicator()
		htmlData = httpCommunicator.get( "http://www.gametrailers.com/screwattack" )
					
		#
		# Debug
		#
		if (self.DEBUG) :
			f = open(os.path.join( xbmc.translatePath( "special://profile" ), "plugin_data", "video", sys.modules[ "__main__" ].__plugin__, "page_screwattack.html" ), "w")
			f.write( htmlData )
			f.close()

		#
		# Parse HTML response...
		#
		soupStrainer = SoupStrainer("div", { "class" : "screw_tab_container", "id" : self.channel_category } )
		beautifulSoup = BeautifulSoup( htmlData, parseOnlyThese=soupStrainer )
		
		#
		# Parse movie entries...
		#
		div_screw_tab_top      = beautifulSoup.find( "div", { "class" : "screw_tab_top" } )
		divs_content_row_super = div_screw_tab_top.findAll( "div", { "class" : "content_row_super" } )
		for div_content_row_super in divs_content_row_super:
			div_gamepage_content_row        = div_content_row_super.find( "div", { "class" : "gamepage_content_row" } ) 
			div_gamepage_content_row_thumb  = div_gamepage_content_row.find( "div", { "class" : "gamepage_content_row_thumb" } )
			div_screw_content_row_info      = div_gamepage_content_row.find( "div", { "class" : "screw_content_row_info"     } )
			div_screw_content_row_info_left = div_screw_content_row_info.find( "div", { "class" : "screw_content_row_info_left"     } )
						
			# Video page URL...
			video_page_url = div_gamepage_content_row_thumb.a[ "href" ]
			
			# Thumbnail...
			thumbnail_url  = div_gamepage_content_row_thumb.a.img[ "src" ]
			
			# Title...
			title = div_screw_content_row_info_left.span.a.string.strip()
			
			# Date...
			span_gamepage_content_row_date = div_screw_content_row_info_left.find( "span", { "class" : "gamepage_content_row_date" } )
			date = span_gamepage_content_row_date.string.strip()
			
			# Plot...
			span_gamepage_content_row_text = div_screw_content_row_info_left.find( "span", { "class" : "gamepage_content_row_text" } )
			plot = span_gamepage_content_row_text.contents[0].strip() 
			
			# Add to list...
			listitem        = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail_url )
			listitem.setInfo( "video", { "Title" : title, "Studio" : "GameTrailers", "Plot" : plot, "Genre" : date } )
			plugin_play_url = '%s?action=play&video_page_url=%s' % ( sys.argv[ 0 ], urllib.quote_plus( video_page_url ) )
			xbmcplugin.addDirectoryItem( handle=int(sys.argv[ 1 ]), url=plugin_play_url, listitem=listitem, isFolder=False)

		# Disable sorting...
		xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
		
		# Label (top-right)...
		xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category="%s" % self.plugin_category )
		
		# End of directory...
		xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
