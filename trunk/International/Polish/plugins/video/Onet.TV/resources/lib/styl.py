import os
import sys
import xbmc
import xbmcgui
import xbmcplugin
import urllib

HOME_DIR = os.getcwd()
names = xbmc.Language( HOME_DIR ).getLocalizedString

MDA = (names (30069))
GWA = (names (30070))
URO = (names (30071))
FTN = (names (30072))
GTO = (names (30006))
DZI = (names (30073))
MAG = (names (30074))
oth = (names (33334))
alL = (names (33333))

class Main:
	def __init__( self ) :
		self.getNames()
	def getNames(self):
		gl=[
			(MDA,'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=4&tags=%28Moda%29&rss=1'),
			(GWA,'hhttp://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=4&tags=%28Gwiazdy%29&rss=1'),
			(URO,'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=4&tags=(Uroda)&rss=1'),
			(FTN,'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=4&tags=%28Fitness%29&rss=1'),
			(GTO,'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=4&tags=%28Gotowanie%29&rss=1'),
			(DZI,'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=4&tags=%28Dziecko%29&rss=1'),
			(MAG,'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=4&tags=%28Magia%29&rss=1'),
			(oth,'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=4&tags=(Inne)&rss=1'),
			(alL,'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=4&rss=1')
			]
		for name, url in gl:
			li=xbmcgui.ListItem(name)
			u=sys.argv[0]+"?RSS&po_co="+"&url="+urllib.quote_plus(url)
			xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
		xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
		xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
