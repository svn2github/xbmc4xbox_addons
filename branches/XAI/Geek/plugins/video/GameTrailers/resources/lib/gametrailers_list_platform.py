#
# Imports
#
from BeautifulSoup      import BeautifulSoup, SoupStrainer
from gametrailers_const import __settings__, __language__
from gametrailers_utils import HTTPCommunicator
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
		self.plugin_category =       params[ "plugin_category" ] 
		self.current_page    = int ( params.get( "page", "1" ) )
		self.platform        =       params[ "platform" ]

		# Settings
		self.video_quality   = __settings__.getSetting ("video_quality")

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
		httpCommunicator = HTTPCommunicator()
		htmlData = httpCommunicator.get( "http://%s.gametrailers.com/?show=&page=%u" % ( self.platform, self.current_page ) )

		# Debug
		if (self.DEBUG) :
			f = open(os.path.join( xbmc.translatePath( "special://profile" ), "plugin_data", "video", sys.modules[ "__main__" ].__plugin__, "page_platform_%i.html" % self.current_page), "w")
			f.write( htmlData )
			f.close()

		# Parse response...
		soupStrainer  = SoupStrainer ( "div", { "id" : "AllMedia" } )
		beautifulSoup = BeautifulSoup( htmlData, soupStrainer )
		
		#
		# Parse movie entries...
		#
		table_entries = beautifulSoup.findAll ( "table", { "width" : "100%" } )
		for table_entry in table_entries :
			table_entry_tr     = table_entry.find ("tr" )
			table_entry_tr_tds = table_entry_tr.findAll ( "td" )
			
			table_entry_tr_td_1            = table_entry_tr_tds[0]
			table_entry_tr_td_2            = table_entry_tr_tds[1]
			div_gamepage_content_row_thumb = table_entry_tr_td_1.find( "div", { "class" : "gamepage_content_row_thumb" } )
						
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
			thumbnail_url  = div_gamepage_content_row_thumb.img[ "src" ]
			thumbnail_url = thumbnail_url.replace( " ", "%20" )

			# Game title...
			h3_movie_title = table_entry_tr_td_2.find( "h3", { "class" : "MovieTitle" } )
			game_title = h3_movie_title.a.string.strip()
			
			# Movie title...
			table_entry_tr_td_2_div_2 = table_entry_tr_td_2.findAll ( "div" )[1] 
			movie_title = table_entry_tr_td_2_div_2.a.string.strip() 
			
			title = game_title + " - " + movie_title
			
			# Plot...			
			plot = table_entry_tr_td_2_div_2.contents[2].strip()
			plot = plot.strip("- ") 
			
			# Date...
			div_movie_file_size = table_entry_tr_td_2.find( "div", { "class" : "MovieFileSize" } )
			if len( div_movie_file_size.contents) > 1 :
				date = div_movie_file_size.contents[2].strip()
			else :
				date = div_movie_file_size.string.strip()
			date = date.replace( "ago ago", "ago" )
			date = date.replace( "Posted", "")
			
			# Add to list...
			listitem        = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail_url )
			listitem.setInfo( "video", { "Title" : title, "Studio" : "GameTrailers", "Plot" : plot, "Genre" : date, "Overlay" : overlay } )
			plugin_play_url = '%s?action=play&video_page_url=%s' % ( sys.argv[ 0 ], urllib.quote_plus( video_page_url ) )
			xbmcplugin.addDirectoryItem( handle=int(sys.argv[ 1 ]), url=plugin_play_url, listitem=listitem, isFolder=False)

		# Next page entry...
		listitem = xbmcgui.ListItem (__language__(30503), iconImage = "DefaultFolder.png", thumbnailImage = os.path.join(self.IMAGES_PATH, 'next-page.png'))
		xbmcplugin.addDirectoryItem( handle = int(sys.argv[1]), url = "%s?action=list-platform&platform=%s&plugin_category=%s&page=%i" % ( sys.argv[0], self.platform, self.plugin_category, self.current_page + 1 ), listitem = listitem, isFolder = True)

		# Disable sorting...
		xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
		
		# Label (top-right)...
		xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=( "%s   (" + __language__(30502) + ")" ) % ( self.plugin_category, self.current_page ) )
		
		# End of directory...
		xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
