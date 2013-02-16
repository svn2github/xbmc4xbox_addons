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
		self.plugin_category  = params[ "plugin_category" ] 
		self.current_page     = int ( params.get( "page", "1" ) )
		self.entries_par_page = 10

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
		url              = "http://www.gametrailers.com/game-reviews/ajax/getreviews?plat=all&start=%u&limit=%u&sort=newest" % ( (self.current_page - 1 ) * self.entries_par_page , self.entries_par_page )
		htmlData		 = httpCommunicator.get( url )		

		# Debug
		if (self.DEBUG) :
			f = open(os.path.join( xbmc.translatePath( "special://profile" ), "plugin_data", "video", sys.modules[ "__main__" ].__plugin__, "page_%i.html" % self.current_page), "w")
			f.write( htmlData )
			f.close()

		# Parse response...
		soupStrainer  = SoupStrainer ( "table", { "class" : "reviews" } )
		beautifulSoup = BeautifulSoup( htmlData, soupStrainer )
		
		#
		# Parse movie entries...
		#
		trs_review = beautifulSoup.findAll ( "tr", { "class" : "review" } )
		for tr_review in trs_review:
			td_col_1  = tr_review.find( "td", { "class" : "col_1" } )
			div_thumb = td_col_1.find( "div", { "class" : "thumb" } )
						
			# Video page URL (+ overlay)
			div_movie_format = div_thumb.find( "div", { "class" : "newestlist_movie_format_SDHD" })
			if div_movie_format != None :
				if self.video_quality == "1" :
					overlay        = xbmcgui.ICON_OVERLAY_HD
					a_movie_format = div_movie_format.find( "a", { "class" : "hd" } )
				else :
					overlay        = xbmcgui.ICON_OVERLAY_NONE
					a_movie_format = div_movie_format.find( "a", { "class" : "sd" } )
				
				if a_movie_format == None :
					overlay        = xbmcgui.ICON_OVERLAY_NONE
					a_movie_format = div_movie_format.a
					
				video_page_url    = a_movie_format[ "href" ]
							
			# Thumbnail URL...
			thumbnail_url  = div_thumb.a.img[ "src" ]

			# Title...
			td_col_2  = tr_review.find( "td", { "class" : "col_2" } )
			title = td_col_2.h3.a.string.strip()
						
			# Plot...			
			p_game_description = td_col_2.find( "p", { "class" : "game_description" } )
			plot = ''.join(BeautifulSoup(p_game_description.renderContents()).findAll(text=True))
			
			# Add to list...
			listitem        = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail_url )
			listitem.setInfo( "video", { "Title" : title, "Studio" : "GameTrailers", "Plot" : plot, "Overlay" : overlay } )
			plugin_play_url = '%s?action=play&video_page_url=%s' % ( sys.argv[ 0 ], urllib.quote_plus( video_page_url ) )
			xbmcplugin.addDirectoryItem( handle=int(sys.argv[ 1 ]), url=plugin_play_url, listitem=listitem, isFolder=False)

		# Next page entry...
		entry_no_start    =   self.current_page       * self.entries_par_page + 1
		entry_no_end      = ( self.current_page + 1 ) * self.entries_par_page
		title             = __language__(30503) + " (" + __language__(30501) % ( entry_no_start, entry_no_end ) + ")"
		listitem = xbmcgui.ListItem ( title, iconImage = "DefaultFolder.png", thumbnailImage = os.path.join(self.IMAGES_PATH, 'next-page.png'))
		xbmcplugin.addDirectoryItem( handle = int(sys.argv[1]), url = "%s?action=list-reviews&plugin_category=%s&page=%i" % ( sys.argv[0], self.plugin_category, self.current_page + 1 ), listitem = listitem, isFolder = True)

		# Disable sorting...
		xbmcplugin.addSortMethod( handle = int( sys.argv[ 1 ] ), sortMethod = xbmcplugin.SORT_METHOD_NONE )
		
		# Label (top-right)...
		xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category = self.plugin_category )
		
		# End of directory...
		xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded = True )
