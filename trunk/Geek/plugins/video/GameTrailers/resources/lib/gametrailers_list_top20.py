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
		self.plugin_category =  unicode( params[ "plugin_category" ], "utf-8")
		self.current_page    =      int( params.get( "page", "1" ) )
		
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
		htmlData         = httpCommunicator.get( "http://www.gametrailers.com/top20.php?toplist=media&topsublist=yesterday&plattyfilt=all&page=%u" % ( (self.current_page - 1 ) * 20 ) )
				
		# Debug
		if (self.DEBUG) :
			f = open(os.path.join( xbmc.translatePath( "special://profile" ), "plugin_data", "video", sys.modules[ "__main__" ].__plugin__, "page_%i.html" % self.current_page), "w")
			f.write( htmlData )
			f.close()

		# Parse response...
		soupStrainer  = SoupStrainer ( "div", { "id" : "top_media" } )
		beautifulSoup = BeautifulSoup( htmlData, soupStrainer )
		
		#
		# Parse movie entries...
		#
		div_top_media = beautifulSoup.find ("div", { "id" : "top_media_yesterday" } )
		videos = self.parseMediaDiv( div_top_media )
		
		if len( videos ) == 0 :
			div_top_media = beautifulSoup.find ("div", { "id" : "top_media_week" } )
			videos = self.parseMediaDiv( div_top_media )
		
		for video in videos :
			# Add to list...
			listitem        = xbmcgui.ListItem( video[ "title" ], iconImage="DefaultVideo.png", thumbnailImage=video[ "thumbnail" ] )
			listitem.setInfo( "video", { "Title" : video[ "title" ], "Studio" : "GameTrailers", "Plot" : video[ "plot" ], "Genre" : video[ "date" ], "Overlay" : video[ "overlay" ] } )
			plugin_play_url = '%s?action=play&video_page_url=%s' % ( sys.argv[ 0 ], urllib.quote_plus( video[ "video_page" ] ) )
			xbmcplugin.addDirectoryItem( handle=int(sys.argv[ 1 ]), url=plugin_play_url, listitem=listitem, isFolder=False)

		#
		# Get the number of entries...
		#
		div_reviewlist_barshort2 = div_top_media.find( "div", { "class" : "reviewlist_barshort2" } )
		div_reviewlist_bartext   = div_reviewlist_barshort2.find( "div", { "class" : "reviewlist_bartext" } )
						
		reviewlist        = div_reviewlist_bartext.string.strip()
		reviewlist_result = self.ENTRY_LIST_RE.search( reviewlist )
		entry_no_start    = reviewlist_result.group(1)
		entry_no_end      = reviewlist_result.group(2)

		# Next page entry...
		listitem = xbmcgui.ListItem (__language__(30503), iconImage = "DefaultFolder.png", thumbnailImage = os.path.join(self.IMAGES_PATH, 'next-page.png'))
		xbmcplugin.addDirectoryItem( handle = int(sys.argv[1]), url = "%s?action=list-top20&plugin_category=%s&page=%i" % ( sys.argv[0], self.plugin_category, self.current_page + 1 ), listitem = listitem, isFolder = True)

		# Disable sorting...
		xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
		
		# Label (top-right)...
		xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=( "%s   (" + __language__(30501) + ")" ) % ( self.plugin_category, entry_no_start, entry_no_end ) )
		
		# End of directory...
		xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

		#
	# Get videos...
	#
	def parseMediaDiv( self, div ) :
		videos = []
		
		div_reviewlist_containershort = div.find( "div", { "class" : "reviewlist_containershort" } )
		div_reviewlist_contentshort   = div_reviewlist_containershort.div
		table                         = div_reviewlist_contentshort.table
		table_trs                     = table.findAll( "tr", recursive=False)
		for table_tr in table_trs:
			div_top20_content_row_thumb = table_tr.find( "div", { "class" : "top20_content_row_thumb" } )
						
			# Video page URL....
			video_page_url = div_top20_content_row_thumb.a[ "href" ]
			overlay        = xbmcgui.ICON_OVERLAY_NONE

			div_top20_movie_format_sd_hd = div_top20_content_row_thumb.find( "div", { "class" : "top20_movie_format_SDHD" } )
			if (div_top20_movie_format_sd_hd) :
				a_list = div_top20_movie_format_sd_hd.findAll( "a" )
				hd_movie_page_url = a_list[0][ "href" ]
				sd_movie_page_url = a_list[1][ "href" ]
				if (self.video_quality == "1" and hd_movie_page_url) :      # HD
					video_page_url = hd_movie_page_url
					overlay        = xbmcgui.ICON_OVERLAY_HD
				else :
					video_page_url = sd_movie_page_url                      # SD
					overlay        = xbmcgui.ICON_OVERLAY_NONE
			else:
				div_top20_movie_format_sd = div_top20_content_row_thumb.find( "div", { "class" : "top20_movie_format_SD" } )
				video_page_url            = div_top20_movie_format_sd.a[ "href" ]
				overlay                   = xbmcgui.ICON_OVERLAY_NONE
			
			# Thumbnail URL...
			thumbnail_url  = div_top20_content_row_thumb.a.img[ "src" ]
			
			# Game title...
			a_gamepage_content_row_title = table_tr.find( "a", { "class" : "gamepage_content_row_title" } )
			if a_gamepage_content_row_title.string == None : game_title = ""
			else                                           : game_title = a_gamepage_content_row_title.string.strip()				
			
			# Movie title...
			div_top20_movie_title = table_tr.find( "div", { "class" : "top20_movie_title" } )
			movie_title = div_top20_movie_title.a.string.strip()
			
			# Title
			if game_title != "" : title = "%s - %s" % ( game_title, movie_title )
			else                : title = movie_title
			
			# Date...
			div_gamepage_content_row_date = table_tr.find( "div", { "class" : "gamepage_content_row_date" } )
			date = div_gamepage_content_row_date.string.strip()
			
			# Plot...			
			plot = ""
			div_top20_content_summary_text = table_tr.find( "div", { "class" : "top20_content_summary_text" } )
			if div_top20_content_summary_text :
				plot = div_top20_content_summary_text.string
			else :
				div_top20_at_content_summary_text = table_tr.find( "div", { "class" : "top20_at_content_summary_text" } )
				plot = div_top20_at_content_summary_text.string
			
			# Add entry to the list...
			video = { "title" : title, "plot" : plot, "date" : date, "thumbnail" : thumbnail_url, "video_page" : video_page_url, "overlay" : overlay }
			videos.append( video )
			
		# Return value
		return videos
