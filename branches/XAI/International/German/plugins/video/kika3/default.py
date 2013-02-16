# -*- coding: iso-8859-1 -*-
import urllib,urllib2,re,xbmcplugin,xbmcgui

pluginhandle = int(sys.argv[1])


def CATEGORIES():

        req = urllib2.Request('http://www.kikaninchen.de/kikaninchen/filme/filme100-flashXml.xml')
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match_links=re.compile('<links id="program">(.+?)</links>', re.DOTALL).findall(link)
        links=re.compile('<image>(.+?)</image>.+?<path type="intern" target="flashapp">(.+?)</path>', re.DOTALL).findall(match_links[0])
        #<a href="/tv/162" class="image_link"><img alt="156543_87ac3a65_mp4_640x480_1600" src="http://asset.gameone.de/gameone/assets/video_metas/teaser_images/000/618/246/featured/156543_87ac3a65_mp4_640x480_1600.mp4_cropped.jpg?1300200447" /></a><h5><a href='/tv/162' title='Flirtgewitter, Yakuza 4, Next'>GameOne - Folge 162</a>
        for thumb,url in links:
		name = thumb
		if 'baumhaus' in thumb:
			name = 'Baumhaus'
		if 'bummi' in thumb:
			name = 'Bummi'
		if 'mitmachmuehle' in thumb:
			name = 'Mit-Mach-Mühle'
		if 'zoeszauberschrank' in thumb:
			name = 'Zoes Zauberschrank'
		if 'sandmann' in thumb:
			name = 'Sandmännchen'
		if 'enemenebu' in thumb:
			name = 'Ene Mene Bu'
		if 'sendungmitdemelefanten' in thumb:
			name = 'Sendung mit dem Elefanten'
		if 'singasmusikbox' in thumb:
			name = 'Singas Musikbox'
		if 'tomunddaserdbeermarmeladebrot' in thumb:
			name = 'Tom und das Erdbeermarmeladebrot'
		if not 'http' in name:
	                addDir(name,url,1,thumb)

def VIDEOS(url,name):#1
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        movies=re.compile('<movie>(.+?)</movie>', re.DOTALL).findall(link)
        #<a href="/tv/162" class="image_link"><img alt="156543_87ac3a65_mp4_640x480_1600" src="http://asset.gameone.de/gameone/assets/video_metas/teaser_images/000/618/246/featured/156543_87ac3a65_mp4_640x480_1600.mp4_cropped.jpg?1300200447" /></a><h5><a href='/tv/162' title='Flirtgewitter, Yakuza 4, Next'>GameOne - Folge 162</a>
        for movie in movies:
		title = re.compile('<title>(.+?)</title>').findall(movie)
		thumb = re.compile('<image>(.+?)</image>').findall(movie)
		video = re.compile('<fileName>(.+?)</fileName>').findall(movie)
		rtmp = 'rtmp://85.239.122.166/vod/'+video[1]
                addLinkOld(title[0],rtmp,thumb[0])



                
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
        VIDEOS(url,name)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
