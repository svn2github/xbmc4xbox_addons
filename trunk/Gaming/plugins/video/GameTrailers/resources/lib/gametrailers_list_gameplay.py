#
# Imports
#
from BeautifulSoup      import BeautifulSoup, SoupStrainer
from gametrailers_const import __settings__, __language__
import os
import re
import sys
import urllib
import xbmc
import xbmcgui
import xbmcplugin

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
		self.IMAGES_PATH   = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'images' ) )
		self.ENTRY_LIST_RE = re.compile( "(\d+) to (\d+) of \d+" )
		
		# Parse parameters...
		params = dict(part.split('=') for part in sys.argv[ 2 ][ 1: ].split('&'))
		self.plugin_category = params[ "plugin_category" ] 
		self.current_page    = int ( params.get( "page", "1" ) )

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
		usock    = urllib.urlopen( "http://www.gametrailers.com/gameplay?page=%u&rdir=1" % ( (self.current_page - 1 ) * 10 ) )
		htmlData = usock.read()
		usock.close()
				
		# Debug
		if (self.DEBUG) :
			f = open(os.path.join( xbmc.translatePath( "special://profile" ), "plugin_data", "video", sys.modules[ "__main__" ].__plugin__, "page_%i.html" % self.current_page), "w")
			f.write( htmlData )
			f.close()

		# Parse response...
		soupStrainer  = SoupStrainer( "div", { "class" : "centerwide_content" } )
		beautifulSoup = BeautifulSoup( htmlData, soupStrainer )
		
		#
		# Parse movie entries...
		#
		divs_content_row_super = beautifulSoup.findAll ("div", { "class" : "content_row_super" } )
		for div_content_row_super in divs_content_row_super:
			div_gamepage_content_row_thumb = div_content_row_super.find( "div", { "class" : "gamepage_content_row_thumb" } )
						
			# Video page URL....
			video_page_url = div_gamepage_content_row_thumb.a[ "href" ]
			
			# Thumbnail URL...
			thumbnail_url  = div_gamepage_content_row_thumb.a.img[ "src" ]

			# Game title...
			a_gamepage_content_row_title = div_content_row_super.find( "a", { "class" : "gamepage_content_row_title" } )
			game_title = a_gamepage_content_row_title.string.strip()
			
			# Movie title....
			div_preview_movie_title = div_content_row_super.find( "div", { "class" : "preview_movie_title" } )
			movie_title = div_preview_movie_title.a.string.strip()
		
			# Title
			title = "%s - %s" % ( game_title, movie_title )
			
			# Date...
			div_gamepage_content_row_date = div_content_row_super.find( "div", { "class" : "gamepage_content_row_date" } )
			date = div_gamepage_content_row_date.string.strip()
			
			# Plot...			
			div_gamepage_content_row_text = div_content_row_super.find( "div", { "class" : "gamepage_content_row_text" } )
			plot = div_gamepage_content_row_text.string.strip() 
			
			# Add to list...
			listitem        = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail_url )
			listitem.setInfo( "video", { "Title" : title, "Studio" : "GameTrailers", "Plot" : plot, "Genre" : date } )
			plugin_play_url = '%s?action=play&video_page_url=%s' % ( sys.argv[ 0 ], urllib.quote_plus( video_page_url ) )
			xbmcplugin.addDirectoryItem( handle=int(sys.argv[ 1 ]), url=plugin_play_url, listitem=listitem, isFolder=False)

		#
		# Get the number of entries...
		#
		div_reviewlist_bar_bottom_thin = beautifulSoup.find( "div", { "class" : "reviewlist_bar_bottom_thin" } )
		if (div_reviewlist_bar_bottom_thin) :
			div_reviewlist_bartext     = div_reviewlist_bar_bottom_thin.find( "div", { "class" : "reviewlist_bartext" } )
		else:
			div_reviewlist_bar_bottom = beautifulSoup.find( "div", { "class" : "reviewlist_bar_bottom" } )
			div_reviewlist_bartext    = div_reviewlist_bar_bottom.find( "div", { "class" : "reviewlist_bartext" } )
						
		reviewlist        = div_reviewlist_bartext.string.strip()
		reviewlist_result = self.ENTRY_LIST_RE.search( reviewlist )
		entry_no_start    = reviewlist_result.group(1)
		entry_no_end      = reviewlist_result.group(2)		

		# Next page entry...
		listitem = xbmcgui.ListItem (__language__(30503), iconImage = "DefaultFolder.png", thumbnailImage = os.path.join(self.IMAGES_PATH, 'next-page.png'))
		xbmcplugin.addDirectoryItem( handle = int(sys.argv[1]), url = "%s?action=list-gameplay&plugin_category=%s&page=%i" % ( sys.argv[0], self.plugin_category, self.current_page + 1 ), listitem = listitem, isFolder = True)

		# Disable sorting...
		xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
		
		# Label (top-right)...
		xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=( "%s   (" + __language__(30501) + ")" ) % ( self.plugin_category, entry_no_start, entry_no_end ) )
		
		# End of directory...
		xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
