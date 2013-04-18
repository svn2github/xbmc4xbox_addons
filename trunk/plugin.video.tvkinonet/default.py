import xbmcaddon,xbmcplugin,xbmcgui,sys,urllib,urllib2,re,socket
import os

socket.setdefaulttimeout(30)
pluginhandle = int(sys.argv[1])
addon = xbmcaddon.Addon(id='plugin.video.tvkinonet')

rootDir = os.getcwd()
if rootDir[-1] == ';':rootDir = rootDir[0:-1]
imageDir = os.path.join(rootDir, 'thumbnails') + '/'
fanart=imageDir+"fanart.jpg"


def Main():
        url='http://www.tv-kino.net/'
        mainurl='http://www.tv-kino.net'
        content = getUrl(url)
        Sender=re.compile('<img alt=".*?" src="(.*?)">\n\t\t\t\t</a>\n\t\t\t\t<span>\n\t\t\t\t<h3>\n\t\t\t\t\t<a title=".*?" href="(.*?)">(.*?)</a>').findall(content)
        for thumb,url,title in Sender:
          url = mainurl+url 
          addLink(title,url,"VIDEOLINKS",thumb)
        xbmcplugin.endOfDirectory(pluginhandle)
	
def VIDEOLINKS(url):
        content = getUrl(url)
        match=re.compile('flashvars" value="netstreambasepath=(.*?)&amp;file=(.*?)&.*?streamer=(.*?)&').findall(content)
        match1=re.compile('application/x-shockwave-flash" data="(.*?)".*?=').findall(content)
        for base,sender,streamer in match:
          base = urllib.unquote(base)
          for swf in match1:
            print swf
            url= streamer + ' playpath='+sender+' swfUrl='+swf + ' live=true' +' timeout=15 swfVfy=1'+' pageurl='+base
            listitem = xbmcgui.ListItem(path=url)
            return xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)
            

def addLink(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('IsPlayable', 'true')
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok

def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def getUrl(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:16.0) Gecko/20100101 Firefox/16.0')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        return link		
		

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


if mode == 'VIDEOLINKS':
    VIDEOLINKS(url)

else:
    Main()    		