import os
import sys
import xbmc
import xbmcgui
import xbmcplugin
import urllib

HOME_DIR = os.getcwd()
names = xbmc.Language( HOME_DIR ).getLocalizedString

RZM = (names (30054))
gtu = (names (30055))
spm = (names (30056))
six = (names (30057))
alL = (names (33333))

class Main:
	#
	# Init
	#
	def __init__( self ) :

		self.getNames()

	def getNames(self):
		gl=[
			(RZM,'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=3&tags=%28Rozmawiamy%29&rss=1'),
			(gtu,'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=3&tags=%28Gotujemy%29&rss=1'),
			(spm,'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=3&tags=%28%C5%9Apiewamy%29&rss=1'),
			(six,'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=3&tags=%286_miliard%C3%B3w_innych%29&rss=1'),
			(alL,'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=3&rss=1')
			]
		for name, url in gl:
			li=xbmcgui.ListItem(name)
			u=sys.argv[0]+"?RSS&po_co="+"&url="+urllib.quote_plus(url)
			xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
		xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
		xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
