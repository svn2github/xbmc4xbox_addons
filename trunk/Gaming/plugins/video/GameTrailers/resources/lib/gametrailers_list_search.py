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
		usock    = urllib.urlopen( "http://www.gametrailers.com/search.php?page=%u&s=%s&str_type=movies&ac=1&orderby=date_added&search_type=advanced" % ( (self.current_page - 1 ) * 10 , urllib.quote( self.query ) ) )
		htmlData = usock.read()
		usock.close()
				
		# Debug
		if (self.DEBUG) :
			f = open(os.path.join( xbmc.translatePath( "special://profile" ), "plugin_data", "video", sys.modules[ "__main__" ].__plugin__, "page_platform_%i.html" % self.current_page), "w")
			f.write( htmlData )
			f.close()

		# Parse response...
		soupStrainer  = SoupStrainer ( "div", { "class" : "centerwide_content" } )
		beautifulSoup = BeautifulSoup( htmlData, soupStrainer )
		
		#
		# Parse movie entries...
		#
		divs_content_row_super  = beautifulSoup.findAll( "div", { "class" : "content_row_super" } )

		# No results found...
		if len(divs_content_row_super) == 0 :
			xbmcgui.Dialog().ok( __language__(30008), __language__(30506), self.query )
			xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=False )
			return			
		
		# Parse results...
		for div_content_row_super in divs_content_row_super:
			div_gamepage_content_row_thumb = div_content_row_super.find( "div", { "class" : "gamepage_content_row_thumb" } )
						
			# Video page URL....
			div_newlist_movie_sd_hd = div_gamepage_content_row_thumb.find( "div", { "class" : "newestlist_movie_format_SDHD" } )
			if (div_newlist_movie_sd_hd) :
				a_list = div_newlist_movie_sd_hd.findAll( "a" )
				hd_movie_page_url = a_list[0][ "href" ]
				sd_movie_page_url = a_list[1][ "href" ]
				if (self.video_quality == "1" and hd_movie_page_url) :      # HD
					video_page_url = hd_movie_page_url
					overlay        = xbmcgui.ICON_OVERLAY_HD
				else :
					video_page_url = sd_movie_page_url                      # SD
					overlay        = xbmcgui.ICON_OVERLAY_NONE
			else:
				div_newestlist_movie_sd = div_gamepage_content_row_thumb.find( "div", { "class" : "newestlist_movie_format_SD" } )
				video_page_url          = div_newestlist_movie_sd.a[ "href" ]
				overlay                 = xbmcgui.ICON_OVERLAY_NONE
			
			# Thumbnail URL...
			thumbnail_url = div_gamepage_content_row_thumb.a.img[ "src" ]
			thumbnail_url = thumbnail_url.replace( " ", "%20" )
			thumbnail_url = "http://www.gametrailers.com%s" % thumbnail_url

			# 
			div_gamepage_content_row_info = div_content_row_super.find( "div", { "class" : "gamepage_content_row_info" } ) 
			
			# Game title...
			a_gamepage_content_row_title = div_gamepage_content_row_info.find( "a", { "class" : "gamepage_content_row_title" } )
			game_title = a_gamepage_content_row_title.string.strip()
			
			# 
			div_gamepage_content_row_text = div_gamepage_content_row_info.find( "div", { "class" : "gamepage_content_row_text" } )
			
			# Movie title...
			div_search_movie_title = div_gamepage_content_row_text.find( "div", { "class" : "search_movie_title" } )
			movie_title = div_search_movie_title.contents[0].string.strip()
			
			title = game_title + " - " + movie_title
			
			# Date...
			div_gamepage_content_row_date = div_gamepage_content_row_text.find( "div", { "class" : "gamepage_content_row_date" } )
			date = div_gamepage_content_row_date.string.strip()
			
			# Plot...
			plot = div_gamepage_content_row_text.contents[ len( div_gamepage_content_row_text.contents ) - 1].string.strip() 
			
			# Add to list...
			listitem        = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail_url )
			listitem.setInfo( "video", { "Title" : title, "Studio" : "GameTrailers", "Plot" : plot, "Genre" : date, "Overlay" : overlay } )
			plugin_play_url = '%s?action=play&video_page_url=%s' % ( sys.argv[ 0 ], urllib.quote_plus( video_page_url ) )
			xbmcplugin.addDirectoryItem( handle=int(sys.argv[ 1 ]), url=plugin_play_url, listitem=listitem, isFolder=False)

		#
		# Get the number of entries...
		#
		div_reviewlist_barleft_topmedia = beautifulSoup.find( "div", { "class" : "reviewlist_barleft_topmedia" } )
		if (div_reviewlist_barleft_topmedia) :
			div_reviewlist_bartext     = div_reviewlist_barleft_topmedia.find( "div", { "class" : "reviewlist_bartext" } )
		#else:
		#	div_reviewlist_bar_bottom = beautifulSoup.find( "div", { "class" : "reviewlist_bar_bottom" } )
		#	div_reviewlist_bartext    = div_reviewlist_bar_bottom.find( "div", { "class" : "reviewlist_bartext" } )

		#
		reviewlist        = div_reviewlist_bartext.string.strip()
		reviewlist_result = self.ENTRY_LIST_RE.search( reviewlist )
		entry_no_start    = reviewlist_result.group(1)
		entry_no_end      = reviewlist_result.group(2)
		entry_no_total    = reviewlist_result.group(3)

		# Next page entry...
		if entry_no_end < entry_no_total :
			listitem = xbmcgui.ListItem (__language__(30503), iconImage = "DefaultFolder.png", thumbnailImage = os.path.join(self.IMAGES_PATH, 'next-page.png'))
			xbmcplugin.addDirectoryItem( handle = int(sys.argv[1]), url = "%s?action=list-search&query=%s&plugin_category=%s&page=%i" % ( sys.argv[0], self.query, self.plugin_category, self.current_page + 1 ), listitem = listitem, isFolder = True)

		# Disable sorting...
		xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
		
		# Label (top-right)...
		xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=( "%s   (" + __language__(30501) + ")" ) % ( self.plugin_category, entry_no_start, entry_no_end ) )
		
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
