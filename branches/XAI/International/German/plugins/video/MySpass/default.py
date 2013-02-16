import urllib,urllib2,re,xbmcplugin,xbmcgui
from operator import itemgetter

pluginhandle = int(sys.argv[1])
baselink = 'http://www.myspass.de'

def CATEGORIES():
        #addDir('Neuste Folgen','http://www.myspass.de/myspass/includes/php/ajax.php?action=getVideoList&sortBy=newest&category=full_episodes&ajax=true&timeSpan=all',1,'')
        #addDir('Meistgesehen','http://www.myspass.de/myspass/includes/php/ajax.php?action=getVideoList&sortBy=views&category=all&ajax=true&tpl=home',1,'')#alle
        #addDir('Bestbewerted','http://www.myspass.de/myspass/includes/php/ajax.php?action=getVideoList&sortBy=votes&category=all&ajax=true&tpl=home',1,'')#alle
        #addDir('TV Shows','http://www.myspass.de/myspass/includes/php/ajax.php?action=getFormatList&showType=tvshow&sortBy=format&ajax=true',2,'')
        #addDir('Webshows','http://www.myspass.de/myspass/includes/php/ajax.php?action=getFormatList&showType=webshow&sortBy=format&ajax=true',2,'')
        #addDir('Ganze Folgen','http://www.myspass.de/myspass/ganze-folgen/',2,'')
		
		
		
		req = urllib2.Request('http://www.myspass.de/myspass/ganze-folgen/')
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		match=re.compile('<div class="threeTWTInnerHeadline">(.+?)</div>.+?<a href="(.+?)".+?<img src="(.+?)"', re.DOTALL).findall(link)
		match_sorted=sorted(match, key=itemgetter(0))
		for name,url,thumb in match_sorted:
			if name != '&nbsp;':
				addDir(name,baselink+url,3,baselink+thumb)
				
				
def INDEX(url):#1 #neuste videos, meisgesehen, usw
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a href="/myspass(.+?)">.+?<img src="(.+?)".+?title="(.+?)"', re.DOTALL).findall(link)
        for url,thumb,name in match:
                addDir(name,'http://www.myspass.de/myspass'+url,5,thumb)

def SERIEN(url):#2 #web und tv
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		match=re.compile('<div class="threeTWTInnerHeadline">(.+?)</div>.+?<a href="(.+?)".+?<img src="(.+?)"', re.DOTALL).findall(link)
		match_sorted=sorted(match, key=itemgetter(0))
		for name,url,thumb in match_sorted:
			if name != '&nbsp;':
				addDir(name,baselink+url,3,baselink+thumb)


def STAFFELN(url):#3 #web und tv #vorerst nur staffel listen, spaeter auch clips
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()

	match=re.compile('<ul class="episodeListSeasonList">(.+?)</ul>', re.DOTALL).findall(link)

	
	for stuff in match:
		print "inhalt gefunden"
        	match_videos=re.compile("onclick=\"ajax\('', 'ajax.php', '(.+?)', '.+?\)\">(.+?)</a></li>").findall(stuff)
	        for url,name in match_videos:
			print "video gefunden"
                	urlpretty = url.replace("&amp;","&")
			lastname = name
			if "clip" in stuff:
				name = name.replace("Bestbewertet","Bestbewertete Clips")
				name = name.replace("Meistgesehen","Meistgesehenen Clips")
				name = name.replace("Staffel","Clips aus Staffel")
			else:
				name = name.replace("Bestbewertet","Bestbewertete Folgen")
				name = name.replace("Meistgesehen","Meistgesehenen Folgen")
	                addDir(name,'http://www.myspass.de/myspass/includes/php/ajax.php?action='+urlpretty,4,'')
		


"""
        for url,name in match_seasons:

#                print urlpretty
                addDir(name,'http://www.myspass.de/myspass/includes/php/ajax.php?action='+urlpretty,4,'')
                #http://www.myspass.de/myspass/includes/php/ajax.php?action=getEpisodeListFromSeason&format=Der+kleine+Mann&season=1&category=full_episode&id=&ajax=true&sortBy=episode_asc

	match_clips_list=re.compile('<ul class="episodeListSeasonList">(.+?)</ul>').findall(link)
        match_clips=re.compile("onclick=\"ajax\('', 'ajax.php', '(.+?)', '.+?\)\">(.+?)</a></li>").findall(match_clips_list[0])
        for url,name in match_clips:
                urlpretty = url.replace("&amp;","&")
#                print urlpretty
                addDir(name,'http://www.myspass.de/myspass/includes/php/ajax.php?action='+urlpretty,4,'')
"""

def VIDEOSELECTION(url):#4 #web und tv #videoauswahl
#        print 'deb url: '+url
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
#        print link
        match=re.compile('<td class="title" onclick="location.href=\'.+?--/(.+?)/\'">.+?<a href=.+?>(.+?)</a>.+?<img src="(.+?)"', re.DOTALL).findall(link)
        #match=re.compile('<td class="title" onclick="location.href=\'(.+?)\'">.+?>(.+?)</a>.+?<img src="(.+?)"', re.DOTALL).findall(link)
        for number,name,thumb in match:
                addLink(name,number,5,'http://www.myspass.de'+thumb)


def PLAY(url,name):#5
        req = urllib2.Request('http://www.myspass.de/myspass/includes/apps/video/getvideometadataxml.php?id='+url)
        #http://www.myspass.de/myspass/includes/apps/video/getvideometadataxml.php?id=3051&0.12656285148114
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
#        print link
        match=re.compile('<url_flv><!\[CDATA\[(.+?)\]\]></url_flv>').findall(link)
        #<url_flv><![CDATA[http://x3583brainc11021.s.o.l.lb.core-cdn.net/secdl/bd7a33ff642e0b2f91c29fd42fb1ad9c/4db92c88/11021brainpool/ondemand/3583brainpool/163840/myspass2009/177/326/5635/3051/3051_39.flv]]></url_flv>
        item = xbmcgui.ListItem(path=match[0])
	return xbmcplugin.setResolvedUrl(pluginhandle, True, item)

                
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param




#def addLink(name,url,iconimage):
#        ok=True
#        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
#        liz.setInfo( type="Video", infoLabels={ "Title": name } )
#        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
#        return ok

def addLink(name,url,mode,iconimage):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	liz.setProperty('IsPlayable', 'true')
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
	return ok

def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        
              
params=get_params()
url=None
name=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
       
elif mode==1:
        print ""+url
        INDEX(url)

elif mode==2:
        print ""+url
        SERIEN(url)
        
elif mode==3:
        print ""+url
        STAFFELN(url)
        
elif mode==4:
        print ""+url
        VIDEOSELECTION(url)
        
elif mode==5:
        print ""+url
        PLAY(url,name)



xbmcplugin.endOfDirectory(int(sys.argv[1]))
