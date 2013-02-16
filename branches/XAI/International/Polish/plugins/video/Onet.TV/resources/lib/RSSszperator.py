import os 
import sys 
import xbmc 
import xbmcgui 
import xbmcplugin 
import urllib,urllib2 
import re 

HOME_DIR = os.getcwd()
names = xbmc.Language( HOME_DIR ).getLocalizedString

NP = (names (33335))
 
class Main: 
	def __init__( self ) :
 
		url = urllib.unquote_plus(sys.argv[2].split('=')[2])
		getData = urllib2.Request(url)
		response = urllib2.urlopen(getData)
		urlContent =response.read()
		response.close()
 
		links = re.compile('<link href="(.+?)" rel="self" />').findall(urlContent)

		numerek=re.compile('.+?15,(.+?),desc.+?rss=1').findall(url)[0]
		nast=str(int(numerek) + 1)
		adresik=re.compile('(.+?)15,.+?,(.+$)').findall(url)[0]
		nastFin=adresik[0] +"15," + nast +"," + adresik[1]

		next=xbmcgui.ListItem(NP)
		u=sys.argv[0]+"?RSS&po_co="+NP+"&url="+urllib.quote_plus(nastFin)
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u, next, isFolder=True)
 
		for link in links:	 
			linkGetData = urllib2.Request(link)
			response = urllib2.urlopen(linkGetData)
			linkContent = response.read()
			response.close()
 
    			video=re.compile('<onettv:bitrate>800(.+?)</onettv:url>').findall(str(linkContent).replace('\t',"").replace('\r',"").replace('\n',""))[0]
    			video=str(video).replace('</onettv:bitrate><onettv:url>','http://www.onet.tv')	
			title = re.compile('<title>(.+?)</title>').findall(linkContent)[0]
			duration = re.compile('<onettv:duration>(.+?)</onettv:duration>').findall(linkContent)[0]
 			image = re.compile('type="image/jpeg" href="(.+?)"').findall(linkContent)[0]
			li = xbmcgui.ListItem(title + ' - ' + '(' + duration + ')', thumbnailImage=image)
			li.setInfo( type="Video", infoLabels={ "Title": title + ' - ' + '(' + duration + ')' } )
			xbmcplugin.addDirectoryItem(int(sys.argv[1]), video, li, isFolder=False)

		xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_NONE)
		xbmcplugin.endOfDirectory(handle=int(sys.argv[1]), succeeded=True)
