#!/usr/bin/python
# -*- coding: utf-8 -*-
import xbmcaddon,xbmcplugin,xbmcgui,sys,urllib,urllib2,re,socket

socket.setdefaulttimeout(30)
pluginhandle = int(sys.argv[1])
xbox = xbmc.getCondVisibility("System.Platform.xbox")
addon = xbmcaddon.Addon(id='plugin.video.kinotrailer.de')




def CATEGORIES():
        addDir('Kinocharts','http://www.kinotrailer.de/',"listVideos",'')
        addDir( 'Vorschau','http://www.kinotrailer.de/vorschau.html',"listVideos1",'')
        addDir( 'Blockbuster','http://www.kinotrailer.de/blockbuster.html',"listVideos1",'')
        xbmcplugin.endOfDirectory(pluginhandle)


def playVideo(id):
        if xbox==True:
          url = "plugin://video/YouTube/?path=/root/video&action=play_video&videoid=" + id
        else:
          url = "plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid=" + id
        listitem = xbmcgui.ListItem(path=url)
        return xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)

def listVideos(url):
        url='http://www.kinotrailer.de/'
        content = getUrl(url)
        match=re.compile('href="(.*)" rel="bookmark" title="">([0-9]+.*)</a>').findall(content)
        for url,title in match:
          url = 'http://www.kinotrailer.de' + url
          content = getUrl(url)
          match1=re.compile('name="movie" value="(.*?)=player_').findall(content)
          ide = str(match1).replace("http://www.youtube.com/v/", "")
          ide1 = str(ide).replace("?version=3&feature", "")
          id = str(ide1)[2:-2].replace("','","")
          thumb="http://img.youtube.com/vi/"+id+"/0.jpg"
          addLink(title,id,"playVideo",thumb)
        xbmcplugin.endOfDirectory(pluginhandle)
		
def listVideos1(url):
        content = getUrl(url)
        match=re.compile('<a href="(.*)">(.*)</a><br>.*\n.*<small class="gallerydate">(.*)</small>').findall(content)
        for url,title,title1 in match:
          title=title+' '+title1
          url='http://www.kinotrailer.de'+url
          print url
          print title
          content = getUrl(url)
          match1=re.compile('name="movie" value="(.*?)=player_').findall(content)
          ide = str(match1).replace("http://www.youtube.com/v/", "")
          ide1 = str(ide).replace("?version=3&feature", "")
          id = str(ide1)[2:-2].replace("','","")
          thumb="http://img.youtube.com/vi/"+id+"/0.jpg"
          addLink(title,id,"playVideo",thumb)
        xbmcplugin.endOfDirectory(pluginhandle)		
        

def getUrl(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/14.0')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        return link


def addLink(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('IsPlayable', 'true')
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok

def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def parameters_string_to_dict(parameters):
    ''' Convert parameters encoded in a URL to a dict. '''
    paramDict = {}
    if parameters:
        paramPairs = parameters[1:].split("&")
        for paramsPair in paramPairs:
            paramSplits = paramsPair.split('=')
            if (len(paramSplits)) == 2:
                paramDict[paramSplits[0]] = paramSplits[1]
    return paramDict

params=parameters_string_to_dict(sys.argv[2])
mode=params.get('mode')
url=params.get('url')
if type(url)==type(str()):
  url=urllib.unquote_plus(url)


if mode == 'playVideo':
    playVideo(url)

elif mode =='listVideos':
    listVideos(url)
	
elif mode =='listVideos1':
    listVideos1(url)	
	
else:
    CATEGORIES()	
