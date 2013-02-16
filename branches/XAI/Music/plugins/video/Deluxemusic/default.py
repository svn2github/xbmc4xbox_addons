import urllib,urllib2,re,random,xbmcplugin,xbmcgui

pluginhandle = int(sys.argv[1])


baseurl = 'http://deluxemusic.tv'

mainreq = urllib2.Request(baseurl+'/programm/')
mainreq.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
mainresponse = urllib2.urlopen(mainreq)
mainlink=mainresponse.read()
mainresponse.close()

def CATEGORIES():
	addLink('Live',baseurl,1,'')
	addDir('Channels',baseurl,2,'')
	addDir('Shows',baseurl,4,'')

						
def PLAY_LIVE(url,name):#1	
	match=re.compile('<script type="text/javascript" src="/modules/mod_dlx_player/embeddedobjects.js\?(.+?)"></script>', re.DOTALL).findall(mainlink)
	
	req = urllib2.Request('http://deluxemusic.tv/modules/mod_dlx_player/embeddedobjects.js?'+match[0])
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	
	match=re.compile('if\(Itemid == 1\) startcontent = (.+?);', re.DOTALL).findall(link)
	
	req = urllib2.Request('http://deluxemusic.tv.staging.ipercast.net/?ContentId='+match[0])
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	
	match=re.compile('file: "(.+?)"', re.DOTALL).findall(link)
	
	req = urllib2.Request(match[0])
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	
	match_location=re.compile('<location>(.+?)</location>', re.DOTALL).findall(link)
	match_rtmp=re.compile('<meta rel="streamer">(.+?)</meta>', re.DOTALL).findall(link)
	
	location = match_location[0]
	rtmp = match_rtmp[0]
	
	item = xbmcgui.ListItem(path=rtmp+location)
	return xbmcplugin.setResolvedUrl(pluginhandle, True, item)
	
def CHANNELS(url):#2
	match=re.compile('<li class="horizontal tv_scroll_item ">.+?href = "(.+?)">.+?img src="(.+?)".+?<span>(.+?)</span>', re.DOTALL).findall(mainlink)
	for url,thumb,name in match:
		if name != 'DELUXE MUSIK':
			name = name.replace('<br>','')
			addLink(name,baseurl+url,3,baseurl+thumb)
		
		
def PLAY_CHANNEL(url,name):#3
	playlistplayer(url)
	


def SHOWS(url):#4
	match_shows=re.compile('<ul id="show_scroll" class="horizontal shows">(.+?)</ul>', re.DOTALL).findall(mainlink)
	for shows in match_shows:
		match_show=re.compile('<div class="show_item smalltext"><a(.+?)</a>', re.DOTALL).findall(shows)
		for show in match_show:

			try:
				match_url=re.compile('href="(.+?)">').findall(show)
				url = match_url[0]	
			except:
				url = 'error'
				
			if url != 'error':
				try:
					match_thumb=re.compile('<img.+?src="(.+?)"').findall(show)
					match_name=re.compile('<img.+?alt="(.+?)"').findall(show)
					thumb = match_thumb[0]	
					name = match_name[0]	
				except:
					name = 'Scraping Fehler, bitte melden ;)'
					thumb = 'Scraping Fehler, bitte melden ;)'
					
				try:
					match_text=re.compile('<p>(.+?)</p>').findall(show)
					text = match_text[0]	
				except:
					text = 'Scraping Fehler, bitte melden ;)'

			
			addLink(name,baseurl+'/'+url,5,baseurl+'/'+thumb)
		
def PLAY_SHOW(url,name):#5
	playlistplayer(url)

                
				
				
				
def playlistplayer(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()

	match=re.compile("changeStationTV\(0,'(.+?)'", re.DOTALL).findall(link)
	
	id = match[0]

	req = urllib2.Request('http://deluxemusic.tv.staging.ipercast.net/live_playlist/getLivePlaylistXml/live_playlist_id/'+id)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	
	match_track=re.compile('<track>(.+?)</track>', re.DOTALL).findall(link)
	
	for track in match_track:
		try:
			match_title=re.compile('<title>(.+?)</title>').findall(track)
			title = match_title[0]	
		except:
			title = 'Scraping Fehler, bitte melden ;)'
			
		try:
			match_location=re.compile('<location>(.+?)</location>').findall(track)
			location = match_location[0]	
		except:
			location = 'Scraping Fehler, bitte melden ;)'
			
		try:
			match_streamer=re.compile('<meta rel="streamer">(.+?)</meta>').findall(track)
			streamer = match_streamer[0]	
		except:
			streamer = 'Scraping Fehler, bitte melden ;)'
			
		try:
			match_thumb=re.compile('<image>(.+?)</image>').findall(track)
			thumb = match_thumb[0]	
		except:
			thumb = 'Scraping Fehler, bitte melden ;)'
			
		url = streamer+'/'+location
		url = url.replace(' ','%20')
		listitem = xbmcgui.ListItem(title,thumbnailImage=thumb)
		xbmc.PlayList(1).add(url, listitem)
				
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
        PLAY_LIVE(url,name)

elif mode==2:
        print ""+url
        CHANNELS(url)
		
elif mode==3:
        print ""+url
        PLAY_CHANNEL(url,name)
		
elif mode==4:
        print ""+url
        SHOWS(url)
		
elif mode==5:
        print ""+url
        PLAY_SHOW(url,name)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
