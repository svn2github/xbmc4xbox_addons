#
# Imports
#
from BeautifulSoup      import BeautifulSoup, SoupStrainer
from gametrailers_const import __settings__, __language__
import httplib
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
		self.DEBUG       = False
		self.IMAGES_PATH = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'images' ) )
		self.PAGELIST_RE = re.compile( "(\d+) to (\d+) of \d+" )
		
		# Parse parameters...
		params = dict(part.split('=') for part in sys.argv[ 2 ][ 1: ].split('&'))
		self.plugin_category =       params[ "plugin_category" ] 
		self.current_page    = int ( params.get( "page", "1" ) )
		
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
		# Init
		#
				
		#
		# Get HTML page...
		#
		params  = urllib.urlencode( {'do' : 'get_movie_page', 'type': 'newest', 'page' : self.current_page, 'loading' : 0 } )
		headers = { "Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain" }
		conn    = httplib.HTTPConnection("www.gametrailers.com:80")
		conn.request( "POST", "/index_ajaxfuncs.php", params, headers )
		response = conn.getresponse()
		htmlData = response.read()
		conn.close()
				
		# Debug
		if (self.DEBUG) :
			f = open(os.path.join( xbmc.translatePath( "special://profile" ), "plugin_data", "video", sys.modules[ "__main__" ].__plugin__, "page_%i.html" % self.current_page), 'w')
			f.write( htmlData )
			f.close()

		# Parse response...
		soupStrainer  = SoupStrainer( "div", { "class" : "newestlist_content" } )
		beautifulSoup = BeautifulSoup( htmlData, soupStrainer )
		
		#
		# Parse movie entries...
		#
		div_newestlist = beautifulSoup.find ("div", { "class" : "newestlist_content" } )
		tables = div_newestlist.findAll( "table" )		  		
		for table in tables:			
			div_newlist_thumb = table.find( "div", { "class" : "newestlist_thumb" } )
			thumbnail_src = div_newlist_thumb.a.img[ "src" ]
	
			# Video URL + overlay...
			div_newlist_movie_sd_hd = div_newlist_thumb.find( "div", { "class" : "newestlist_movie_format_SDHD" } )
			if (div_newlist_movie_sd_hd) :
				a_list = div_newlist_movie_sd_hd.findAll( "a" )
				hd_movie_page_url = a_list[0][ "href" ]
				sd_movie_page_url = a_list[1][ "href" ]
				if (self.video_quality == "1" and hd_movie_page_url) :      # HD
					video_page_url = hd_movie_page_url
					overlay        = xbmcgui.ICON_OVERLAY_HD
				else :
					video_page_url = sd_movie_page_url                      # SD
					overlay       = xbmcgui.ICON_OVERLAY_NONE
			else:
				div_newestlist_movie_sd = div_newlist_thumb.find( "div", { "class" : "newestlist_movie_format_SD" } )
				if (div_newestlist_movie_sd) :
					video_page_url      = div_newestlist_movie_sd.a[ "href" ]
					overlay             = xbmcgui.ICON_OVERLAY_NONE				# SD
				else :
					div_newestlist_movie_hd = div_newlist_thumb.find( "div", { "class" : "newestlist_movie_format_HD" } )
					video_page_url          = div_newestlist_movie_hd.a[ "href" ]
					overlay                 = xbmcgui.ICON_OVERLAY_HD				# HD
			
			div_newestlist_info = table.find( "div", { "class" : "newestlist_info" } )
			
		    # Game title...
			div_newestlist_title = div_newestlist_info.find ("h3", { "class" : "newestlist_title" } )
			game_title = div_newestlist_title.string
			
		    # Movie Title + Plot...
			div_newestlist_text      = div_newestlist_info.find( "div", { "class" : "newestlist_text" } )
			span_newestlist_subtitle = div_newestlist_text.span 
			movie_title              = span_newestlist_subtitle.a.string
			plot                     = div_newestlist_text.contents[1].string.strip(" -").replace("\\'", "'") 

		    # Title...
			title = game_title + " - " + movie_title
			title = title.replace( "\\'", "'" )

			# Genre...
			div_newestlist_platimage      = div_newestlist_info.find ("div", { "class" : "newestlist_platimage" } )
			div_newestlist_platimage_imgs = div_newestlist_platimage.findAll( "img" )
			platforms = []
			for div_newestlist_platimage_img in div_newestlist_platimage_imgs:
				platforms.append( self.decodePlatform ( div_newestlist_platimage_img[ "src" ] ) )
			genre = " / ".join(platforms)
			
			# Add to list...
			listitem        = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail_src )
			listitem.setInfo( "video", { "Title" : title, "Studio" : "GameTrailers", "Plot" : plot, "Genre" : genre, "Overlay" : overlay } )
			plugin_play_url = '%s?action=play&video_page_url=%s' % ( sys.argv[ 0 ], urllib.quote_plus( video_page_url ) )
			xbmcplugin.addDirectoryItem( handle=int(sys.argv[ 1 ]), url=plugin_play_url, listitem=listitem, isFolder=False)

		#
		# Get the number of entries...
		#
		div_pagelist    = beautifulSoup.find( "div", { "class" : "pagelist_bartext" } )
		pagelist        = div_pagelist.string.strip()
		pagelist_result = self.PAGELIST_RE.search( pagelist )
		entry_no_start  = pagelist_result.group(1)
		entry_no_end    = pagelist_result.group(2)
		
		# Next page entry...
		listitem = xbmcgui.ListItem (__language__(30503), iconImage = "DefaultFolder.png", thumbnailImage = os.path.join(self.IMAGES_PATH, 'next-page.png'))
		xbmcplugin.addDirectoryItem( handle = int(sys.argv[1]), url = "%s?action=list-all&plugin_category=%s&page=%i" % ( sys.argv[0], self.plugin_category, self.current_page + 1 ), listitem = listitem, isFolder = True)

		# Disable sorting...
		xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
		
		# Label (top-right)...
		xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=( "%s   (" + __language__(30501) + ")" ) % (self.plugin_category, entry_no_start, entry_no_end) )
		
		# End of directory...
		xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

	#
	# Decode Platform
	#
	def decodePlatform( self, imageName ) :
		if (imageName.find("plat_arcade_default") > -1):
			return "Arcade"
		if (imageName.find("plat_pc_default") > -1):
			return "PC"
		if (imageName.find("plat_ps2_default") > -1):
			return "PS2"
		if (imageName.find("plat_ds_default") > -1):
			return "DS"
		if (imageName.find("plat_psp_default") > -1):
			return "PSP"
		if (imageName.find("plat_ps3_default") > -1):
			return "PS3"
		if (imageName.find("plat_ps1_default") > -1):
			return "PS1"
		if (imageName.find("plat_xbla_default") > -1):
			return "Xbox Live Arcade"
		if (imageName.find("plat_xb360_default") > -1):
			return "Xbox 360"
		if (imageName.find("plat_wii_default") > -1):
			return "Wii"
		if (imageName.find("plat_wiiware_default") > -1):
			return "WiiWare"
		if (imageName.find("plat_iphone_default") > -1):
			return "iPhone"
		if (imageName.find("plat_ipod_default") > -1):
			return "iPod"
		if (imageName.find("plat_vcon_default") > -1):
			return "Wii Virtual Console"
		if (imageName.find("plat_na_default") > -1 or imageName.find("plat__default") > -1):
			return "N/A"
		if (imageName.find("plat_psn_default") > -1):
			return "PSN"
		if (imageName.find("plat_xblcg_default") > -1):
			return "Xbox Live Community Games"
		return ""
