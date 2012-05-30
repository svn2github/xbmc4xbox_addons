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
import xml.dom.minidom

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
		self.DEBUG                     = False
		self.PLAYER_URL_RE             = re.compile( ".*/player/(\d+).html" )
		self.EPISODE_BONUSROUND_URL_RE = re.compile( ".*/episode/bonusround/.*" )
		self.BONUSROUND_PHP_URL_RE     = re.compile( ".*/bonusround.php\?ep=(\d+)" )
		self.VIDEO_URL_RE              = re.compile( ".*/video/(.+)?/(\d+)" )
		self.GAMETRAILERS_TV_PLAYER_RE = re.compile( ".*/gametrailerstv_player.php?.*" )
		self.EPISODE_GAMETRAILER_TV_RE = re.compile( ".*/episode/gametrailers-tv/.*" )
		self.USER_MOVIES_URL_RE        = re.compile( ".*/usermovies/(\d+).html" )
		self.MOSES_MOVIES_THUMBS       = re.compile(".*/moses/moviesthumbs/(\d+)-.*")
		
		#
		# Parse parameters...
		#
		params = dict(part.split('=') for part in sys.argv[ 2 ][ 1: ].split('&'))
		
		self.video_page_url = urllib.unquote_plus( params[ "video_page_url" ] ) 

		# Settings
		self.video_players = { "0" : xbmc.PLAYER_CORE_AUTO,
							   "1" : xbmc.PLAYER_CORE_DVDPLAYER,
							   "2" : xbmc.PLAYER_CORE_MPLAYER }
		self.video_player  = __settings__.getSetting("video_player")
		
		self.video_format  = __settings__.getSetting("video_format")
		self.video_quality = __settings__.getSetting("video_quality")

		#
		# Play video...
		#
		self.playVideo()
	
	#
	# Play video...
	#
	def playVideo( self ) :
		if (self.DEBUG) :
			print "video_page_url = " + self.video_page_url

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
		dialogWait.create( __language__(30504), title )
		
		#
		# Video page URL = /player/48119.html
		#
		if (self.PLAYER_URL_RE.match( self.video_page_url ) ) :
			video_urls = self._getVideoUrl1( self.video_page_url )
		#
		# Video page URL = /episode/bonusround/303?ch=2&sd=1 
		#
		elif (self.EPISODE_BONUSROUND_URL_RE.match ( self.video_page_url ) ) :
			video_urls = self._getVideoUrl2( self.video_page_url )
		#
		# Video page URL = /video/brutal-b-roll-darksiders/49436
		#
		elif (self.VIDEO_URL_RE.match( self.video_page_url ) ) :
			video_urls = self._getVideoUrl3( self.video_page_url )
		#
		# Video page URL = /gametrailerstv_player.php?ep=60&ch=1&sd=1
		# Video page URL = /episode/gametrailers-tv/64&ch=2&sd=0?ep=64&ch=2&sd=0
		#
		elif (self.GAMETRAILERS_TV_PLAYER_RE.match( self.video_page_url ) or
			  self.EPISODE_GAMETRAILER_TV_RE.match( self.video_page_url ) ) :
			video_urls = self._getVideoUrl4( self.video_page_url )
		#
		# Video page URL = /bonusround.php?ep=15
		#
		elif (self.BONUSROUND_PHP_URL_RE.match( self.video_page_url ) ) :
			video_urls = self._getVideoUrl5( self.video_page_url )
		#
		# Video page URL = player/usermovies/1.html
		#
		elif (self.USER_MOVIES_URL_RE.match( self.video_page_url ) ) :
			video_urls = self._getVideoUrl6( self.video_page_url )

		#
		# Check video URLs...
		#
		httpCommunicator = HTTPCommunicator()
		have_valid_url   = False
		for video_url in video_urls :
			if httpCommunicator.exists( video_url ) :
				have_valid_url = True
				break
		
		#
		# Play video...
		#
		if have_valid_url :
			playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
			playlist.clear()
	
			for video_url  in video_urls :
				listitem = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail )
				listitem.setInfo( "video", { "Title": title, "Studio" : studio, "Plot" : plot, "Genre" : genre } )
				playlist.add( video_url, listitem )
	
			# Close wait dialog...
			dialogWait.close()
			del dialogWait
			
			# Play video...
			xbmcPlayer = xbmc.Player( self.video_players[ self.video_player ] )
			xbmcPlayer.play( playlist )
		#
		# Alert user...
		#
		else :
			xbmcgui.Dialog().ok( __language__(30000), __language__(30505) )
		
	#
	# Video page URL = /player/48119.html
	#
	def _getVideoUrl1( self, video_page_url ):
		movie_id = self.PLAYER_URL_RE.search( video_page_url ).group(1)
		
		# 
		# Get HTML page...
		# 
		usock    = urllib.urlopen( "http://mosii.gametrailers.com/getmediainfo4.php?hd=1&mid=%s" % movie_id )
		htmlData = usock.read()
		usock.close()
				
		# Debug
		if (self.DEBUG) :
			f = open(os.path.join( xbmc.translatePath( "special://profile" ), "plugin_data", "video", sys.modules[ "__main__" ].__plugin__, "video_page.html" ), "w")
			f.write( htmlData )
			f.close()
			
		# Parse HTML response...
		params     = dict(part.split('=') for part in htmlData.split('&'))
		umfilename = urllib.unquote( params[ "umfilename" ] )
		
		# Video URL...
		if (self.video_format == "0") :
			video_url = "http://trailers.gametrailers.com/gt_vault/%s.flv" % umfilename
		elif (self.video_format == "1") :
			 video_url = "http://trailers.gametrailers.com/gt_vault/%s.mov" % umfilename
		elif (self.video_format == "2") :
			 video_url = "http://trailers.gametrailers.com/gt_vault/%s.wmv" % umfilename

		#
		# Return value
		#
		video_urls = []
		video_urls.append( video_url )
		return video_urls

	#
	# Video page URL = /episode/bonusround/303?ch=2&sd=1
	#
	def _getVideoUrl2(self, video_page_url ):		
		# 
		# Get HTML page...
		# 
		httpCommunicator = HTTPCommunicator()
		htmlData         = httpCommunicator.get( video_page_url )

		# Parse HTML page...
		beautifulSoup = BeautifulSoup( htmlData )
		embed         = beautifulSoup.find( "embed" )
		
		if embed == None :
			return []

		filename      = embed[ "flashvars" ][ 9: ]		
		url           = re.compile( "(.+?)&" ).search( filename ).group( 1 )
		
		#
		# Get XML data....
		#
		if not url.startswith( "http" ) :
			wins_xml_url = "http://www.gametrailers.com%s" % url
		else :
			wins_xml_url = url		
		usock        = urllib.urlopen( wins_xml_url )
		xmldoc       = xml.dom.minidom.parse( usock )
		usock.close()

		# Debug
		if (self.DEBUG) :
			f = open(os.path.join( xbmc.translatePath( "special://profile" ), "plugin_data", "video", sys.modules[ "__main__" ].__plugin__, "wins_xml_reply.xml" ), "w")
			f.write(  xmldoc.toxml() )
			f.close()
			
		# Get the movie url...
		fileinfoNode = xmldoc.documentElement.getElementsByTagName( "fileinfo" )[0]
		
		sdNode       = fileinfoNode.getElementsByTagName( "sd" )[0]
		sdFlvNode    = sdNode.getElementsByTagName( "flv" )[0]
		video_url    = sdFlvNode.childNodes[0].nodeValue
		
		if self.video_quality == "1" :
			hdNode    = fileinfoNode.getElementsByTagName( "hd" )[0]
			hdFlvNode = hdNode.getElementsByTagName ( "flv" )[0]
			if hdFlvNode.childNodes[0].nodeValue :
				video_url = hdFlvNode.childNodes[0].nodeValue
		
		#
		# Return value
		#
		video_urls = []
		video_urls.append( video_url )
		return video_urls
	
	#
	# Video page URL = /video/brutal-b-roll-darksiders/49436
	#
	def _getVideoUrl3( self, video_page_url ):
		movie_id = self.VIDEO_URL_RE.search( video_page_url ).group(2)
		
		# 
		# Get video URL (method #1)...
		#
		httpCommunicator = HTTPCommunicator()
		htmlData         = httpCommunicator.get( "http://mosii.gametrailers.com/getmediainfo4.php?hd=1&mid=%s" % movie_id )
				
		# Debug
		if (self.DEBUG) :
			f = open(os.path.join( xbmc.translatePath( "special://profile" ), "plugin_data", "video", sys.modules[ "__main__" ].__plugin__, "video_page.html" ), "w")
			f.write( htmlData )
			f.close()
			
		# Parse HTML response...
		params     = dict(part.split('=', 1) for part in htmlData.split('&'))
		umfilename = urllib.unquote( params[ "umfilename" ] )
		hasHD      = urllib.unquote( params.get("hasHD") )
		
		# SD preferred, but the URL is for HD...
		if self.video_quality == "0" and hasHD == "0":
			umthumbnail = urllib.unquote( params.get("umthumbnail") )
			movie_id_sd = self.MOSES_MOVIES_THUMBS.search( umthumbnail ).group(1)
			
			# Get data...
			usock    = urllib.urlopen( "http://mosii.gametrailers.com/getmediainfo4.php?hd=1&mid=%s" % movie_id_sd )
			htmlData = usock.read()
			usock.close()
			
			# Parse response...
			params     = dict(part.split('=', 1) for part in htmlData.split('&'))
			umfilename = urllib.unquote( params[ "umfilename" ] )
		
		#
		# Video URL...
		#
		if (self.video_format == "0") :
			video_url = "http://trailers.gametrailers.com/gt_vault/%s.flv" % umfilename
		elif (self.video_format == "1") :
			video_url = "http://trailers.gametrailers.com/gt_vault/%s.mov" % umfilename
		elif (self.video_format == "2") :
			video_url = "http://trailers.gametrailers.com/gt_vault/%s.wmv" % umfilename
			
		#
		# Get video URL (method #2)...
		#
		if not httpCommunicator.exists(video_url) :
			neo_xml_url  = "http://www.gametrailers.com/neo/?page=xml.mediaplayer.Mediagen&movieId=%s" % movie_id
			usock        = urllib.urlopen( neo_xml_url )
			xmldoc       = xml.dom.minidom.parse( usock )
			usock.close()
			
			video_nodes = xmldoc.documentElement.getElementsByTagName( "video" )
			if video_nodes != None :
				src_nodes = video_nodes[0].getElementsByTagName( "src" )
				if src_nodes != None :
					video_url = src_nodes[0].childNodes[0].nodeValue

		#
		# Return value
		#
		video_urls = []
		video_urls.append( video_url )
		return video_urls	   

	#
	# Video page URL = /gametrailerstv_player.php?ep=60&ch=1&sd=1
	# Video page URL = /episode/gametrailers-tv/64&ch=2&sd=0?ep=64&ch=2&sd=0
	#
	def _getVideoUrl4(self, video_page_url ):
		#
		# Init
		#
		if not video_page_url.startswith( "http" ) :
			video_page_url = "http://www.gametrailers.com%s" % video_page_url 
		
		# 
		# Get HTML page...
		# 
		usock    = urllib.urlopen( video_page_url )
		htmlData = usock.read()
		usock.close()

		# Debug
		if (self.DEBUG) :
			f = open(os.path.join( xbmc.translatePath( "special://profile" ), "plugin_data", "video", sys.modules[ "__main__" ].__plugin__, "video_page.html" ), "w")
			f.write( htmlData )
			f.close()

		# Parse HTML page...
		soupStrainer  = SoupStrainer ( "div", { "id" : "gttv_player" } )
		beautifulSoup = BeautifulSoup( htmlData, soupStrainer )
		
		div_gttv_player = beautifulSoup.find ( "div", { "id" : "gttv_player" } )
		xml_filename    = re.compile( "myFlash.addVariable\('filename', '(.+)'\);" ).search( div_gttv_player.script.string  ).group( 1 )
		
		#
		# Get XML data....
		#
		gttv_xml_url = "http://moses.gametrailers.com/moses/gttv_xml/%s" % urllib.quote( xml_filename )
		usock        = urllib.urlopen( gttv_xml_url )
		xmlData      = usock.read().strip()
		usock.close()

		# Debug
		if (self.DEBUG) :
			f = open(os.path.join( xbmc.translatePath( "special://profile" ), "plugin_data", "video", sys.modules[ "__main__" ].__plugin__, "gttv.xml" ), "w")
			f.write( xmlData )
			f.close()
		
		#
		# Parse XML...
		#
		xmldoc       = xml.dom.minidom.parseString( xmlData )
		video_urls   = []
		
		#
		# Get the movie url (single FLV for all episodes)...
		#
		if len( xmldoc.documentElement.getElementsByTagName( "fileinfo" ) ) == 1 :
			fileinfoNode = xmldoc.documentElement.getElementsByTagName( "fileinfo" )[ 0 ]
			
			sdNode       = fileinfoNode.getElementsByTagName( "sd" )[0]
			sdFlvNode    = sdNode.getElementsByTagName( "flv" )[0]
			video_url    = sdFlvNode.childNodes[0].nodeValue
			
			if self.video_quality == "1" :
				hdNode    = fileinfoNode.getElementsByTagName( "hd" )[0]
				hdFlvNode = hdNode.getElementsByTagName ( "flv" )[0]
				if hdFlvNode.childNodes[0].nodeValue :
					video_url = hdFlvNode.childNodes[0].nodeValue			
			
			video_urls.append ( video_url )
		
		#
		# Get the movie urls (separate FLV for each episode)...
		#
		else :
			chapterNodes = xmldoc.documentElement.getElementsByTagName( "chapter" )
			for chapterNode in chapterNodes :
				fileinfoNode = chapterNode.getElementsByTagName( "fileinfo" )[0]
				
				sdNode       = fileinfoNode.getElementsByTagName( "sd" )[0]
				video_url    = sdNode.childNodes[0].nodeValue.strip()
				
				if self.video_quality == "1" :
					hdNode   = fileinfoNode.getElementsByTagName( "hd" )[0]
					if hdNode.childNodes[0].nodeValue :
						video_url = hdNode.childNodes[0].nodeValue.strip()
				
				video_urls.append ( video_url )
		
		#
		# Return value
		#
		return video_urls

	#
	# Video page URL = /bonusround.php?ep=15
	#
	def _getVideoUrl5( self, video_page_url ):
		# 
		# Get HTML page...
		# 
		httpCommunicator = HTTPCommunicator()
		htmlData = httpCommunicator.get( video_page_url )

		# Debug
		if (self.DEBUG) :
			f = open(os.path.join( xbmc.translatePath( "special://profile" ), "plugin_data", "video", sys.modules[ "__main__" ].__plugin__, "play_url_5.html" ), "w")
			f.write( htmlData )
			f.close()

		#
		# Parse HTML page (get number of parts)...
		#
		soupStrainer  = SoupStrainer ( "div", { "id" : "media_div" } )
		beautifulSoup = BeautifulSoup( htmlData, parseOnlyThese=soupStrainer )
		
		episode_no =      re.compile( "myFlash.addVariable\('episode', '(.*)'\)" ).search( beautifulSoup.script.string ).group( 1 )
		part_count = int( re.compile( "myFlash.addVariable\('eppartcount', '(.*)'\)" ).search( beautifulSoup.script.string ).group( 1 ) )
		
		#
		# Return value
		#
		video_urls = []
		for part_no in range(1, part_count + 1) :
			hd_part = ""
			
			if self.video_quality == "1" :
				if ( 4 <= int(episode_no) and int(episode_no) <= 21 ) :
					hd_part = "_h264"

			video_url = "http://trailers.gametrailers.com/gt_vault/br_ep%s_pt%s%s.flv" % ( episode_no, part_no, hd_part )
			video_urls.append( video_url )
			
		return video_urls

	#
	# Video page URL = player/usermovies/1.html
	#
	def _getVideoUrl6( self, video_page_url ):
		movie_id = self.USER_MOVIES_URL_RE.search( video_page_url ).group(1)
		
		# 
		# Get HTML page...
		# 
		httpCommunicator = HTTPCommunicator()
		htmlData = httpCommunicator.get( "http://mosii.gametrailers.com/getmediainfo4.php?umid=%s" % movie_id )
				
		# Debug
		if (self.DEBUG) :
			f = open(os.path.join( xbmc.translatePath( "special://profile" ), "plugin_data", "video", sys.modules[ "__main__" ].__plugin__, "video_page.html" ), "w")
			f.write( htmlData )
			f.close()
			
		# Parse HTML response...
		params     = dict(part.split('=') for part in htmlData.split('&'))
		umfilename = urllib.unquote( params[ "umfilename" ] )
		
		# Video URL...
		video_url = "http://umtrailers.gametrailers.com/gt_usermovies/um_%s.flv" % umfilename

		#
		# Return value
		#
		video_urls = []
		video_urls.append( video_url )
		return video_urls

#
# The End
#