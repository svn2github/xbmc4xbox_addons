#
# Imports
#
from BeautifulSoup import BeautifulSoup, SoupStrainer
from eurogamer_const import __settings__, __language__
from eurogamer_utils import HTTPCommunicator
import os
import re
import simplejson
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
		# Parse parameters...
		params = dict(part.split('=') for part in sys.argv[ 2 ][ 1: ].split('&'))
		self.video_page_url = urllib.unquote_plus( params[ "video_page_url" ] ) 

		# Settings
		self.video_players = { "0" : xbmc.PLAYER_CORE_AUTO,
							   "1" : xbmc.PLAYER_CORE_DVDPLAYER,
							   "2" : xbmc.PLAYER_CORE_MPLAYER }
		self.video_player  = __settings__.getSetting("video_player")
		self.video_quality = __settings__.getSetting("video_quality")
		
		# Play video...
		self.playVideo()
	
	#
	# Play video...
	#
	def playVideo( self ) :
		#print "video_page_url = " + self.video_page_url
		
		#
		# Init
		#
		video_url = None

		#
		# Get current list item details...
		#
		title     = unicode( xbmc.getInfoLabel( "ListItem.Title"  ), "utf-8" )
		thumbnail =          xbmc.getInfoImage( "ListItem.Thumb"  )
		studio    = unicode( xbmc.getInfoLabel( "ListItem.Studio" ), "utf-8" )
		plot      = unicode( xbmc.getInfoLabel( "ListItem.Plot"   ), "utf-8" )
		genre     = unicode( xbmc.getInfoLabel( "ListItem.Genre"  ), "utf-8" )
		
		#
		# Show wait dialog while parsing data...
		#
		dialogWait = xbmcgui.DialogProgress()
		dialogWait.create( __language__(30402), title )	
		
		# 
		# Parse video HTML page to get the video playlist i... 
		#
		httpCommunicator = HTTPCommunicator()
		htmlSource       = httpCommunicator.post( "www.eurogamer.net", "/" + self.video_page_url, {'version' : 'portable' } )        
		
		#
		playlist_id_re = re.compile( 'Playlist\["id"\]\s*=\s*"(.*)"')
		playlist_id_m    = playlist_id_re.search( htmlSource )
		
		if (playlist_id_m != None) :
			playlist_id = playlist_id_m.group(1)
			print playlist_id
			
			#
			# Parse JSON reply...
			#
			httpCommunicator = HTTPCommunicator()
			jsonReply        = httpCommunicator.get( "http://www.eurogamer.net/tv/playlist/%s" % playlist_id )        
			
			json = simplejson.loads( jsonReply )
			video_url = json[0][ 'file' ]
			if self.video_quality == "1" :
				video_url_hd = json[0].get( 'hd.file' )
				if video_url_hd != None and video_url_hd != "":
					video_url = video_url_hd

		#
		# Close wait dialog...
		#
		dialogWait.close()
		del dialogWait
		
		if (video_url != None) :
			#	
			# Play video...
			#
			playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
			playlist.clear()
	
			# Set video info...
			listitem = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail )
			listitem.setInfo( "video", { "Title": title, "Studio" : studio, "Plot" : plot, "Genre" : genre } )
	
			# Add item to our playlist...
			playlist.add( video_url, listitem )
	
			# Play...
			xbmcPlayer = xbmc.Player( self.video_players[ self.video_player ] ).play( playlist )
		else :
			#
			# Video not found...
			#
			xbmcgui.Dialog().ok( __language__(30000), __language__(30403) )

#
# The End
#