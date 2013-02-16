import os
import sys
import xbmc
import xbmcgui
import xbmcplugin
import urllib

HOME_DIR = os.getcwd()
names = xbmc.Language( HOME_DIR ).getLocalizedString

kra = (names (30078))
swa = (names (30079))
TMY = (names (30080))
pgd = (names (30081))
nau = (names (30082))
biz = (names (30005))
cie = (names (30083))
alL = (names (33333))

class Main:
	def __init__( self ) :

		self.getNames()

	def getNames(self):
		gl=[
			(kra,'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=1&tags=%28Kraj%29&rss=1'),
			(swa,'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=1&tags=%28%C5%9Awiat%29&rss=1'),
			(TMY,'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=1&tags=%28Teraz_MY%29&rss=1'),
			("CNN",'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=1&tags=%28CNN%29&rss=1'),
			(pgd,'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=1&tags=%28Pogoda%29&rss=1'),
			(biz,'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=1&tags=%28Biznes%29&rss=1'),
			(nau,'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=1&tags=%28Nauka%29&rss=1'),
			(cie,'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=1&tags=%28Ciekawostki%29&rss=1'),
			("UWAGA!",'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=1&tags=%28UWAGA!%29&rss=1'),
			(alL,'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=1&rss=1')
			]
		for name, url in gl:
			li=xbmcgui.ListItem(name)
			u=sys.argv[0]+"?RSS&po_co="+"&url="+urllib.quote_plus(url)
			xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
		xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
		xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
