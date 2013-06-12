import xbmcaddon,xbmcplugin,xbmcgui,sys,urllib,urllib2,re,socket
import os
import urlresolver
import mechanize
import StringIO,gzip

socket.setdefaulttimeout(30)
pluginhandle = int(sys.argv[1])
addon = xbmcaddon.Addon(id='plugin.video.streamallthis')


rootDir = os.getcwd()
if rootDir[-1] == ';':rootDir = rootDir[0:-1]
imageDir = os.path.join(rootDir, 'thumbnails') + '/'
fanart=imageDir+"fanart.jpg"

mainurl='http://streamallthis.ch'


def CATEGORIES():
        addDir('Most Popular Show','http://streamallthis.ch/tv-shows-list.html',"Bestof",imageDir+"streamallthisMost.jpg")
        addDir('Alphabetic Shows','http://streamallthis.ch/tv-shows-list.html',"alphabetic",imageDir+"streamallthisAlphabetic.jpg")
        addDir('Last Episodes','http://streamallthis.ch/',"LastEpisodes",imageDir+"streamthisallLast.jpg")
        xbmcplugin.endOfDirectory(pluginhandle)
		




def Bestof(url):
        content = getUrl(url)
        #match=re.compile('<img src="(.*?)".*?<a href="(.*?)" class="lc"> (.*?)</a>', re.DOTALL).findall(content)
        match=re.compile('MOST POPULAR(.*?)ALPHABETIC',re.DOTALL).findall(content)
        for find in match:
          gg=re.findall('<img src="(.*?)"/>.*?<a href="(.*?)" class="lc"> (.*?)</a>',find , re.DOTALL)
          for thumb,url, title in gg:
            url=mainurl+url
            addDir(title,url,"assessSeasons",thumb)	  
          xbmcplugin.endOfDirectory(pluginhandle)
		  
		  
def alphabetic(url):
        content = getUrl(url)
        match=re.compile('ALPHABETIC(.*?)</table>', re.DOTALL).findall(content)
        for find in match:
          find=str(find)
          gg=re.findall('<a href="(.*)" class="lc"> (.*)</a>', find)
          for url,title in gg:
            url=mainurl+url
            addDir(title,url,"assessSeasons",imageDir+"Tvshows.jpg")	  
        xbmcplugin.endOfDirectory(pluginhandle)

def LastEpisodes(url):
        content = getUrl(url)
        match=re.compile('LAST EPISODES(.*?)</table>',re.DOTALL).findall(content)
        for find in match:
          gg=re.findall('<img src="(.*?)"/>.*?<a href="(.*?)" class="lc"> (.*?)</a>.*?&nbsp;(.*?)\n.*?&nbsp;(.*?)\n.*?</td>',find, re.DOTALL)
          for thumb,url,title,season,episode in gg:
            url=mainurl+url
            title=title+'SEASON'+' ' +season+' '+'EPISODE'+' '+episode
            thumb=str(thumb).replace('" width="110" height="160', '')
            print title
            print url
            print thumb
            addDir(title,url,"assessSeasons",thumb)	  
          xbmcplugin.endOfDirectory(pluginhandle)

          
def assessSeasons(url):
        coverLINK = GETCOVER(url)
        if coverLINK == None:
        		 coverLINK = "http://www.apps4linux.de/images/not_available.png"
        content = getUrl(url)
        match=re.compile('&nbsp;(.*?)\n.*?</td>.*?&nbsp;(.*?)\n.*?</td>.*?<a href="(.*?)" class="la">WATCH</a>', re.DOTALL).findall(content)
        for name1,name2,url in match:
          name1='SEASON'+' '+name1
          name2='Episode'+' ' +name2
          title=name1+' '+name2
          url=mainurl+url
          addLink(title,url,"VIDEOLINKS",coverLINK)	  
        xbmcplugin.endOfDirectory(pluginhandle)		  
	
def VIDEOLINKS(url):
        content = getUrl(url)
        match=re.compile('<iframe src="(.*?)" width="600" height="360" frameborder="0" scrolling="no"></iframe>').findall(content)
        for url in match:
          print url
          url= urlresolver.resolve(url)
          listitem = xbmcgui.ListItem(path=url)
          return xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)
          		  
def GETCOVER(url):
        print "test :"+str(url)
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        req.add_header('Accept-encoding', 'gzip')        
        response = urllib2.urlopen(req)    
        
        if response.info().get('Content-Encoding') == 'gzip':
        		buf = StringIO.StringIO( response.read())
        		f = gzip.GzipFile(fileobj=buf)
        		link = f.read()
        else:          
        		link=response.read()
        		response.close()
        match=re.compile('<img src="(.*?)" alt=".*?"/>',re.DOTALL).findall(link)
        for m in match:
        		cover = str(m)
        		return cover        

		  
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
        req = mechanize.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:16.0) Gecko/20100101 Firefox/16.0')
        response = mechanize.urlopen(req)
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

if  mode == "Bestof":
    Bestof(url)  
  
elif mode == "alphabetic":
    alphabetic(url)
	
elif mode == "LastEpisodes":
    LastEpisodes(url)	
	
elif mode == "assessSeasons":
    assessSeasons(url)
	
elif mode == "VIDEOLINKS":
    VIDEOLINKS(url)	
		

else:
    CATEGORIES()    		
	
	
