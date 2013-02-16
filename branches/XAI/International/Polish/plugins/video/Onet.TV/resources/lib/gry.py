import os
import sys
import xbmc
import xbmcgui
import xbmcplugin
import urllib

HOME_DIR = os.getcwd()
names = xbmc.Language( HOME_DIR ).getLocalizedString

tra = (names (30034))
gpy = (names (30035))
KPI = (names (30036))
rwo = (names (30037))
imp = (names (30038))
alL = (names (33333))
wyw = (names (30025))

class Main:
	def __init__( self ) :
		self.getNames()
	def getNames(self):
		gl=[
			(tra,'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=9&tags=%28Trailery%29&rss=1'),
			(gpy,'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=9&tags=%28Gameplay%29&rss=1'),
			(KPI,'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=9&tags=%28Kulisy_produkcji%29&rss=1'),
			(rwo,'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=9&tags=%28Recenzja_wideo%29&rss=1'),
			(wyw,'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=9&tags=%28Wywiady%29&rss=1'),
			(imp,'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=9&tags=%28Imprezy%29&rss=1'),
			(alL,'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=9&rss=1')
			]
		for name, url in gl:
			li=xbmcgui.ListItem(name)
			u=sys.argv[0]+"?RSS&po_co="+"&url="+urllib.quote_plus(url)
			xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
		xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
		xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
