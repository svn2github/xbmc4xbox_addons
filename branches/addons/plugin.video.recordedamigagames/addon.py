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

    game_map = get_games()

    for game_name in game_map:
        match=re.compile(query, re.IGNORECASE).findall(game_name)
        if match:
            addDir(game_name, game_map[game_name]['link'], 'game', base_url + '/' + game_map[game_name]['image'], False)

def ALPHA(name):
    game_map = get_games()

    for game_name in sorted(list(game_map)):
        if game_name[0:1].upper() == name:
            addDir(game_name, game_map[game_name]['link'], 'game', base_url + '/' + game_map[game_name]['image'], False)

        if name == '#':
            for i in range(0,9):
                if game_name.startswith(str(i)):
                    addDir(game_name, game_map[game_name]['link'], 'game', base_url + '/' + game_map[game_name]['image'], False)

def get_games():
    game_map = {}

    for i in range(1, 10):
        req = urllib2.Request(base_url+"/video-index"+str(i)+".php")
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        content=response.read()
        response.close()

        content=content.replace('\n', '')
        content=content.replace('\r', '')

        match=re.compile('<a href="(.+?)".+?<img src=(.+?)>.+?>(.+?)<', re.MULTILINE).findall(content)

        for game in match:
            game_map[game[2]] = {}
            game_map[game[2]]['link'] = game[0]
            game_map[game[2]]['image'] = game[1]
            
    return game_map
  
def GAME(link):
        req = urllib2.Request(base_url+"/"+link)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        content=response.read()
        response.close()

        match=re.compile('href="http://(amiga.sh0.org/.+?)"', re.MULTILINE).findall(content)

        if match:
            addLink ('', "http://"+urllib.quote(match[0]), '')

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

def addDir(name,link,mode,iconimage,folder=True):
        u=sys.argv[0]+"?url="+urllib.quote_plus(link)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name} )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=folder)
        return ok

def addLink(name,url,iconimage):
        ok=True

        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Audio", infoLabels={ "Title": name} )
        liz.setProperty("IsPlayable","true")
        #ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
        xbmc.Player().play(url, liz)

        return ok 
                      
def addImageLink(name,url,iconimage):
        ok=True

        liz=xbmcgui.ListItem(name, iconImage="DefaulImage.png", thumbnailImage=iconimage)
        liz.setInfo( type="image", infoLabels={ "Title": name} )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
        return ok 
 
base_url = "http://www.recordedamigagames.org"

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
    print ""
    INDEX()

elif mode=='game':
    GAME(url)

elif mode=='alpha':
    ALPHA(name)
    
elif mode=='search':
    SEARCH()

xbmcplugin.endOfDirectory(int(sys.argv[1]))
