import os
import sys
import xbmc
import xbmcgui
import xbmcplugin
import urllib

HOME_DIR = os.getcwd()
names = xbmc.Language( HOME_DIR ).getLocalizedString

alL = (names (33333))

class Main:
	def __init__( self ) :
		self.getNames()
	def getNames(self):
		gl=[
			("MOTO TV",'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=12&tags=%28Moto_TV%29&rss=1'),
			("PRZEJEZDNA24",'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=12&tags=%28Przejezdna24%29&rss=1'),
			("Operacja Tuning",'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=12&tags=%28Operacja_Tuning%29&rss=1'),
			("Jazda Polska!",'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=12&tags=%28Jazda_Polska%29&rss=1'),
			("UWAGA! Pirat!",'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=12&tags=%28Uwaga!_Pirat%29&rss=1'),
			("Raport TURBO",'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=10&tags=%28Da_Vinci_Learning%29&rss=1'),
			(alL,'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=10&rss=1')
			]
		for name, url in gl:
			li=xbmcgui.ListItem(name)
			u=sys.argv[0]+"?RSS&po_co="+"&url="+urllib.quote_plus(url)
			xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
		xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
		xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
