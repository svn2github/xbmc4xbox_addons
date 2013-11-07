import xbmcaddon,xbmcplugin,xbmcgui,sys,urllib,urllib2,re,socket
import os
import urlresolver


socket.setdefaulttimeout(30)
pluginhandle = int(sys.argv[1])
addon = xbmcaddon.Addon(id='plugin.video.movie25xbmc4xbox')

home = addon.getAddonInfo('path').decode('utf-8')
imageDir = os.path.join(home, 'thumbnails') + '/'
fanart=imageDir+"fanart.jpg"
base='http://www.movie25.so'

def main():
        addDir('Search','',"Moviesearch",'')
        url='http://www.movie25.so/'
        content = getUrl(url)
        match=re.search(r'<li><a href="/">Home</a></li>(.*?)</ul>', content,re.DOTALL)
        match=re.findall('<li><a href="(.*?)" title=".*?">(.*?)</a></li>', match.group())
        for url,title in match:
          url=base+url
          if 'genres' in url:
            addDir(title,url,"genres",'')
          else:
            addDir(title,url,"index",'')
        addDir('Movies A-Z','http://www.movie25.so/',"Letter",'')

def index(url):
        newurl=url
        content = getUrl(url)
        spl=content.split('<div class="movie_pic">')
        if len(spl)>1:
          for i in range(1,len(spl),1):
            entry=spl[i]
            urlmatch=re.compile('<h1><a href="(.*?)"',re.DOTALL).findall(entry)
            url=base+urlmatch[0]
            thumbmatch=re.compile('<img src="(.*?)"',re.DOTALL).findall(entry)
            thumb=thumbmatch[0]
            titlematch=re.compile('<h1><a.*?target="_self">.*?(\w.*?)</a></h1>',re.DOTALL).findall(entry)
            title=titlematch[0]
            staffel=thumb
            addDir2(title,staffel,url,"hoster",thumb)
        link=urllib2.urlopen(newurl).read().replace('&nbsp;','WX')
        nextmatch = re.compile(r'</font>WX<a href=.(.*?)..>\[\d.*?]</a>',re.DOTALL).findall(link)
        if nextmatch:
          print nextmatch
          nexturl=base+nextmatch[0]
          addDir('Next',nexturl,"index",'')


def genres(url):
        url='http://www.movie25.so/'
        content = getUrl(url)
        spl=content.split('<div class="genres_body">')
        if len(spl)>=1:
          for i in range(1,len(spl),1):
            entry=spl[i]
            match=re.compile('<li><a href="(.*?)">(.*?)</a></li>', re.DOTALL).findall(entry)
            for url,title in match:
              url=base+url
              print url
              print title
              addDir(title,url,"index",'')

def hoster(url,name,staffel):
        content = getUrl(url)
        spl=content.split('<ul onclick="ShowPrompt')
        if len(spl)>1:
          for i in range(1,len(spl),1):
            entry=spl[i]
            titlematch=re.search('<li class="link_name">(.*?)</li>',entry,re.DOTALL)
            title=titlematch.group(1)
            likematch=match=re.search('<div class="said_work">(.*?)</div>',entry,re.DOTALL)
            like=likematch.group(1)
            title=name+'  '+title
            urlmatch=re.search('<a href="(.*?)" target="_blank">',entry,re.DOTALL)
            if urlmatch:
              url=base+urlmatch.group(1)
              print url
              addLink(title,url,"play",staffel)

def play(url):
        content=urllib2.urlopen(url).read().replace('\\', '')
        match=re.search('onclick="location.href=\'(.*?)\'"',content, re.DOTALL)
        #match=re.search(' onclick=\"Javascript:location.href=\'(.*?)\'"',content, re.DOTALL)
        url=match.group(1)
        url=urlresolver.resolve(url)
        listitem = xbmcgui.ListItem(path=url)
        return xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)
        
def Moviesearch():
        search_entered =search()
        name=str(search_entered).replace('+','')
        url='http://www.movie25.so/search.php?key=%s&submit=' % search_entered
        content = getUrl(url)
        spl=content.split('<div class="movie_pic">')
        if len(spl)>1:
          for i in range(1,len(spl),1):
            entry=spl[i]
            urlmatch=re.compile('<h1><a href="(.*?)"',re.DOTALL).findall(entry)
            url=base+urlmatch[0]
            thumbmatch=re.compile('<img src="(.*?)"',re.DOTALL).findall(entry)
            thumb=thumbmatch[0]
            titlematch=re.compile('<h1><a.*?target="_blank">.*?(\w.*?)</a></h1>',re.DOTALL).findall(entry)
            title=titlematch[0]
            viewmatch=re.compile('Views: <span>.*?(\d.*?)</span>',re.DOTALL).findall(entry)
            view=viewmatch[0]
            print title
            print url
            print thumb 
            staffel=thumb
            addDir2(title,staffel,url,"hoster",thumb)

def search():
        search_entered = ''
        keyboard = xbmc.Keyboard(search_entered, 'Search Movies')
        keyboard.doModal()
        if keyboard.isConfirmed():
            search_entered = keyboard.getText() .replace(' ','+')  
            if search_entered == None:
                return False          
        return search_entered 

def Letter(url):
        content = getUrl(url)
        match=re.compile('(/movies/[a-z]/).*?([A-Z])',re.DOTALL).findall(content)
        for url,title in match:
          url=base+url
          addDir(title,url,"index",'')     


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

def addDir2(name,staffel,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&staffel="+urllib.quote_plus(staffel)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
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
name=params.get('name')
staffel=params.get('staffel')
if type(url)==type(str()):
  url=urllib.unquote_plus(url)
if type(name)==type(str()):
  name=urllib.unquote_plus(name)
if type(staffel)==type(str()):
  staffel=urllib.unquote_plus(staffel)


if mode == 'index':
    index(url)

elif mode == 'genres':
    genres(url)

elif mode == 'hoster':
    hoster(url,name,staffel)

elif mode == 'Moviesearch':
    Moviesearch()

elif mode == 'Letter':
    Letter(url)

elif mode == 'play':
    play(url)

else:
    main()

xbmcplugin.endOfDirectory(pluginhandle)    		
