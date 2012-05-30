# -*- coding: utf-8 -*-
import urllib,urllib2,re,xbmcplugin,xbmcgui
import xbmcaddon


pluginhandle = int(sys.argv[1])

__settings__ = xbmcaddon.Addon(id='plugin.video.putpat')



baseurl = 'http://www.putpat.tv'

mainreq = urllib2.Request(baseurl+'/ws.xml?method=Initializer.putpatPlayer&client=putpatplayer&streamingMethod=rtmp&partnerId=1')
mainreq.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
mainresponse = urllib2.urlopen(mainreq)
mainlink=mainresponse.read()
mainresponse.close()

match_channels=re.compile('<channel>(.+?)</channel>', re.DOTALL).findall(mainlink)


def MAIN():
	for channel in match_channels:

		try:
			match_info=re.compile('<channel-info>(.+?)</channel-info>').findall(channel)
			info = match_info[0]
		except:
			info = 'Scraping Fehler, bitte melden ;)'

		try:
			match_message=re.compile('<channel-message>(.+?)</channel-message>').findall(channel)
			message = match_message[0]
		except:
			message = 'Scraping Fehler, bitte melden ;)'

		try:
			match_artists=re.compile('<played-artists>(.+?)</played-artists>', re.DOTALL).findall(channel)
			artists = match_artists[0]
		except:
			artists = 'Scraping Fehler, bitte melden ;)'

		try:
			match_integer=re.compile('<id type="integer">(.+?)</id>', re.DOTALL).findall(channel)
			integer = match_integer[0]
		except:
			integer = 'Scraping Fehler, bitte melden ;)'

		try:
			match_tags=re.compile('<tags>(.+?)</tags>').findall(channel)
			tags = match_tags[0]
		except:
			tags = 'Scraping Fehler, bitte melden ;)'

		try:
			match_title=re.compile('<title>(.+?)</title>').findall(channel)
			title = match_title[0]
		except:
			title = 'Scraping Fehler, bitte melden ;)'

		try:
			match_urlchannel=re.compile('<url-channel-name>(.+?)</url-channel-name>').findall(channel)
			urlchannel = match_urlchannel[0]
		except:
			urlchannel = 'Scraping Fehler, bitte melden ;)'


		name = title + ' - ' + message
		thumb = 'http://files.putpat.tv/artwork/channelgraphics/'+integer+'/channellogo_invert_500.png'
		addLinkFan(name,'<title>'+title+'</title>',1,thumb,'http://files.putpat.tv/putpat_player/231/assets/putpat_splashscreen.jpg')



def PLAY(url,name):#1
	for channel in match_channels:
		if url in channel:
			match_clips=re.compile('<clip>(.+?)</clip>', re.DOTALL).findall(channel)


	pl=xbmc.PlayList(1)
	pl.clear()

	for entry in match_clips:
		try:
			match_title=re.compile('<title>(.+?)</title>').findall(entry)
			title = match_title[-1]
		except:
			title = 'Scraping Fehler, bitte melden ;)'

		try:
			match_author=re.compile('<display-artist-title>(.+?)</display-artist-title>').findall(entry)
			author = match_author[0]
		except:
			author = 'Scraping Fehler, bitte melden ;)'

		try:



			if (__settings__.getSetting("quality") == '2'):
			#if xbmcplugin.getSetting(pluginhandle,"quality") == '2':
				match_video = match_high=re.compile('<high>(.+?)</high>').findall(entry)

			elif  (__settings__.getSetting("quality") == '1'):
			#xbmcplugin.getSetting(pluginhandle,"quality") == '1':
				match_video = match_high=re.compile('<medium>(.+?)</medium>').findall(entry)

			elif (__settings__.getSetting("quality") == '0'):
			#xbmcplugin.getSetting(pluginhandle,"quality") == '0':
				match_video = match_high=re.compile('<low>(.+?)</low>').findall(entry)

			video = match_video[0]
		except:
			video = 'Scraping Fehler, bitte melden ;)'

		try:
			match_token=re.compile('<token>(.+?)</token>').findall(entry)
			token = match_token[0]
		except:
			token = 'Scraping Fehler, bitte melden ;)'

		try:
			match_duration=re.compile('<duration Value="(.+?)" />').findall(entry)
			duration = match_duration[0]
		except:
			duration = 'Scraping Fehler, bitte melden ;)'


		match_token=re.compile('token=(.+?)=').findall(video)
		token = '?token='+match_token[0]+'='

		match_mp4=re.compile('mp4(.+?)mp4').findall(video)
		mp4 = 'mp4'+match_mp4[0]+'mp4'

		url = 'rtmp://tvrlfs.fplive.net/tvrl/ playpath='+mp4+token+' swfurl=http://files.putpat.tv/putpat_player/231/PutpatPlayer.swf swfvfy=true pageUrl=http://www.putpat.tv/'
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

def addLinkFan(name,url,mode,iconimage,fanart):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	liz.setProperty('IsPlayable', 'true')
	liz.setProperty('fanart_image',fanart)
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
        PLAY(url,name)


xbmcplugin.endOfDirectory(int(sys.argv[1]))
