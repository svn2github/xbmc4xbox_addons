# -*- coding: utf-8 -*-
import urllib,urllib2,re,xbmcplugin,xbmcgui


pluginhandle = int(sys.argv[1])

baseurl = 'http://www.yavido.tv'

def MAIN():
	req = urllib2.Request(baseurl)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	
	playlisten=re.compile('Playlisten</a>(.+?)</ul>', re.DOTALL).findall(link)
	match=re.compile('<a href="(.+?)" title="(.+?)">(.+?)</a>', re.DOTALL).findall(playlisten[0])
	
	for url,name2,name1 in match:
		name = name1+' - '+ name2
		name = name.replace('&amp;','&')
		addLink(name,baseurl+url,2,'')
		
	addDir('Verpasste Sendung',baseurl+'/playlisten',1,'')
		

def VERPASSTE_SENDNGEN(url):#1
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	match=re.compile('<a href="sendung-verpasst/\?id=(.+?)".+?<img.+?src="(.+?)".+?<strong>(.+?)</strong>.+?<div.+?>(.+?)</div>.+?<div.+?>(.+?)</div>', re.DOTALL).findall(link)
	for id,thumb,date,name1,name2 in match:
		name = name1
		if not '</div>' in name2:
			name = name + ' - '+ name2
			
		url = baseurl+'/sendung-verpasst/?id='+id
		addLink(name,url,2,baseurl+thumb)
		


def PLAY(url,name):#2     
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	match_programslot=re.compile('programSlot=(.+?)"').findall(link)
	
	
	url ='http://www.yavido.tv/scripts/dispatchFlash.php?call=http://interface.yavido.de/prod/gadget/playlistV2.php?today=1&type=2&pslid='+match_programslot[0]+'&placementID=18'
	"""
	item = xbmcgui.ListItem(path=url)
	return xbmcplugin.setResolvedUrl(pluginhandle, True, item)
	"""
	
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()

	entries=re.compile('<entry>(.+?)</entry>', re.DOTALL).findall(link)
	
	pl=xbmc.PlayList(1)
	pl.clear()
	
	for entry in entries:
		try:
			match_title=re.compile('<param name="yavTitle" value="(.+?)"/>').findall(entry)
			title = match_title[0]	
		except:
			title = 'Scraping Fehler, bitte melden ;)'
			
		try:
			match_author=re.compile('<param name="yavAuthor" value="(.+?)" />').findall(entry)
			author = match_author[0]
		except:
			author = 'Scraping Fehler, bitte melden ;)'
			
		try:
			match_video=re.compile('<ref href="(.+?)" />').findall(entry)
			video = match_video[0]
		except:
			video = 'Scraping Fehler, bitte melden ;)'
			
		try:
			match_duration=re.compile('<duration Value="(.+?)" />').findall(entry)
			duration = match_duration[0]
		except:
			duration = 'Scraping Fehler, bitte melden ;)'
			
		url = 'rtmp://fms.edge.newmedia.nacamar.net/yavido/'+video
		listitem = xbmcgui.ListItem(author + ' - ' + title,thumbnailImage='')
		xbmc.PlayList(1).add(url, listitem)

	
	#xbmc.Player().play(pl)

			

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




def addLinkOld(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok

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
        
def addDirFan(name,url,mode,iconimage,fanart):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
	liz.setProperty('fanart_image',fanart)

        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
              
params=get_params()
url=None
name=None
mode=None
fanart=None

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
        MAIN()

elif mode==1:
        print ""+url
        VERPASSTE_SENDNGEN(url)

elif mode==2:
        print ""+url
        PLAY(url,name)


xbmcplugin.endOfDirectory(int(sys.argv[1]))
