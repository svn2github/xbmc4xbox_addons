import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon

def INDEX():
    addDir('search', 'search', 'search', '')
    addDir('#', '#', 'alpha', '')
    for ascii_number in range(65, 91):
        letter = chr(ascii_number)
        addDir(letter, letter, 'alpha', '')

def SEARCH():
    kb = xbmc.Keyboard('', 'find game', False)
    kb.doModal()
    if not (kb.isConfirmed()):
        return

    query = kb.getText()

    games = get_games()

    for game in games:
        match=re.compile(query, re.IGNORECASE).findall(game[1])
        if match:
            addLink(game[1], game[0], '')

def get_games():
        req = urllib2.Request(base_url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        content=response.read()
        response.close()
        content=content.replace('\n', '')
        content=content.replace('\r', '')

        match=re.compile('<a href="(http://www.archive.+?)">(.+?)</a>', re.MULTILINE).findall(content)

        return match

def ALPHA(name):
        games = get_games()

        map={}
        for game in games:
            if game[1][0:1].upper() == name:
                map[game[1]] = game[0]

            if name == '#':
                for i in range(0,9):
                    if game[1].startswith(str(i)):
                        map[game[1]] = game[0]

        for game_name in sorted(list(map)):
            addLink(game_name, map[game_name], '')  
   
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

def addDir(name,link,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(link)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name} )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addLink(name,url,iconimage):
        ok=True

        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Audio", infoLabels={ "Title": name} )
        liz.setProperty("IsPlayable","true")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
        return ok 
                      
base_url = "http://www.c64-longplays.de/videos.php"

params=get_params()
url=None
name=None
mode=None
iconimage=None



try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        mode=urllib.unquote_plus(params["mode"])
except:
        pass
                   

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IconImage: "+str(iconimage)

       

if mode==None or url==None or len(url)<1:
    INDEX()

elif mode == 'alpha':
    ALPHA(name)
       
elif mode == 'search':
    SEARCH()

xbmcplugin.endOfDirectory(int(sys.argv[1]))
