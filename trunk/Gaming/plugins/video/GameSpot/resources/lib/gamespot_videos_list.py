#
# Imports
#
import os
import sys
import xbmc
import xbmcgui
import xbmcplugin
import urllib
import datetime
import re
from BeautifulSoup import SoupStrainer
from BeautifulSoup import BeautifulSoup
from gamespot_videos_utils import HTTPCommunicator

#
# Constants
# 
__settings__ = xbmcplugin
__language__ = xbmc.getLocalizedString

#
# Main class
#
class Main:
	#
	# Init
	#
	def __init__( self ) :
		# Constants
		self.DEBUG       = False
		self.IMAGES_PATH = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'images' ) )
		
		# Parse parameters...
		params = dict(part.split('=') for part in sys.argv[ 2 ][ 1: ].split('&'))
		self.plugin_category = params[ "plugin_category" ] 
		self.video_type      = params[ "video_type" ]

		# Settings
		self.page_size       = 20
		self.video_quality   = __settings__.getSetting ("video_quality")

		# Get page...
		self.current_page    = int ( params.get( "page", "0" ) )

		#
		# Get the videos...
		#
		self.getVideos()
	
	#
	# Get plugins...
	#
	def getVideos( self ) :
		#
		# Init
		#
		user_date_format = xbmc.getRegion( "dateshort" ).replace( "MM", "%m" ).replace( "DD", "%d" ).replace( "YYYY", "%Y" ).strip()
		
		#
		# Get HTML page...
		#
		httpCommunicator = HTTPCommunicator()
		url              = "http://www.gamespot.com/videos/index.html?mode=filter&page=%u&type=%s&range=all&view=list&filter=latest" % ( self.current_page, self.video_type )
		htmlSource       = httpCommunicator.get( url )
		
		# Debug
		if (self.DEBUG) :
			print "PAGE URL = " + url
			f = open(os.path.join( xbmc.translatePath( "special://profile" ), "plugin_data", "video", sys.modules[ "__main__" ].__plugin__, "page_%i.html" % self.current_page), 'w')
			f.write( htmlSource )
			f.close()

		# Parse response...
		soupStrainer  = SoupStrainer( "div", { "class" : "body" } )
		beautifulSoup = BeautifulSoup( htmlSource, soupStrainer )
		
		# Parse movie entries...
		ul_video_list = beautifulSoup.find ("ul", { "id" : "video_list" } )  
		lis = ul_video_list.findAll( 'li', { "class" : re.compile( "video|video alt" ) } )		
		for li in lis :
			div_wrap = li.div
			em = div_wrap.em
			a = em.a
			
			# Title
			title = a.string.strip()
			
			# Video page
			href           = a[ "href" ]
			video_page_url = "http://www.gamespot.com%s" % href
			
			# Thumb
			div_details = div_wrap.div
			div_thumb   = div_details.div
			thumb_img   = div_thumb.img 
			thumb_src   = thumb_img[ "src" ]
			
			# Date
			ul_details   = div_details.ul
			li_date      = ul_details.li 
			date_str     = li_date.string.strip()
			date_display = datetime.date ( int( date_str.split( "/" )[ 2 ] ) + 2000, int( date_str.split( "/" )[ 0 ] ), int( date_str.split( "/" )[ 1 ] ) ).strftime( user_date_format )
			
			# HD?
			play_hd      = [ False, True ][ self.video_quality == "1" ]
			if (play_hd) :
				ul_watch = div_details.find( "ul", { "class" : re.compile( "actions watch" ) } )
				li_hd    = ul_watch.find( "li", { "class" : "hd last" } )
				play_hd  = [ False, True ][ li_hd != None ]			

			# Debug info...
			if (self.DEBUG) :
				print "TITLE = " + title
				print "DATE  = " + date_display
				print "HREF  = " + href
				print "THUMB = " + thumb_src
            
			# Add to list...
			listitem        = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumb_src )
			listitem.setInfo( "video", { "Title" : title, "Studio" : "GameSpot", "Plot" : title, "Genre" : date_display } )
			plugin_play_url = '%s?action=play&video_page_url=%s&play_hd=%s' % ( sys.argv[ 0 ], urllib.quote( href ), play_hd )
			xbmcplugin.addDirectoryItem( handle=int(sys.argv[ 1 ]), url=plugin_play_url, listitem=listitem, totalItems=self.page_size, isFolder=False)
			
		# Total pages...
		div_pagination = beautifulSoup.find ("div", { "class" : "pagination" } )
		ol = div_pagination.ol
		last_li = ol.find ("li", { "class" : re.compile( "last |last on") } )
		last_li_a = last_li.a
		if last_li_a != None :
			total_pages = int( last_li_a.string.strip() )
		else :
			total_pages = int( last_li.span.string.strip() )				
		
		# Next page entry...
		if (self.current_page + 1 < total_pages) :
			listitem = xbmcgui.ListItem (__language__(30402), iconImage = "DefaultFolder.png", thumbnailImage = os.path.join(self.IMAGES_PATH, 'next-page.png'))
			xbmcplugin.addDirectoryItem( handle = int(sys.argv[1]), url = "%s?action=list&plugin_category=%s&video_type=%s&page=%i" % ( sys.argv[0], self.plugin_category, self.video_type, self.current_page + 1 ), listitem = listitem, isFolder = True)

		# Disable sorting...
		xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
				
		# End of directory...
		xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
