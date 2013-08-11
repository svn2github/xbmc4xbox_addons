import urllib,urllib2,re,cookielib,xbmcplugin,xbmcgui,xbmcaddon,socket,os,shutil,string,xbmc,stat,xbmcvfs
import base64
import urlresolver
import time
from t0mm0.common.net import Net as net
from t0mm0.common.addon import Addon
from metahandler import metahandlers
from metahandler import metacontainers
#from zipfile import ZipFile as zip
pluginhandle = int(sys.argv[1])
addon = Addon('plugin.video.videobull', sys.argv)
fanart = "resources/art/fanart.png"
xbmc_skin = xbmc.getSkinDir()
ADDON = xbmcaddon.Addon(id='plugin.video.videobull')

try:
    import StorageServer
except:
    import storageserverdummy as StorageServer
cache = StorageServer.StorageServer('plugin.video.videobull', 28)
_VBL = Addon('plugin.video.videobull', sys.argv)
META_ON = _VBL.get_setting('use-meta') == 'true'
META_OFF = _VBL.get_setting('use-meta') == 'false'
AZ_DIRECTORIES = (ltr for ltr in string.ascii_uppercase)
try:
    DB_NAME = _VBL.get_setting('db_name')
    DB_USER = _VBL.get_setting('db_user')
    DB_PASS = _VBL.get_setting('db_pass')
    DB_ADDR = _VBL.get_setting('db_address')

    if _VBL.get_setting('use_remote_db') == 'true' and \
                    DB_ADDR is not None and \
                    DB_USER is not None and \
                    DB_PASS is not None and \
                    DB_NAME is not None:
        import mysql.connector as orm

        _VBL.log('Loading MySQL as DB engine')
        DB = 'mysql'
    else:
        _VBL.log('MySQL not enabled or not setup correctly')
        raise ValueError('MySQL not enabled or not setup correctly')
except:
    try:
        from sqlite3 import dbapi2 as orm

        _VBL.log('Loading sqlite3 as DB engine')
    except:
        from pysqlite2 import dbapi2 as orm

        _VBL.log('pysqlite2 as DB engine')
    DB = 'sqlite'
    __translated__ = xbmc.translatePath("special://database")
    DB_DIR = os.path.join(__translated__, 'videobullcache.db')

PREPARE_ZIP = False
__metaget__ = metahandlers.MetaData(preparezip=PREPARE_ZIP)
	
if not xbmcvfs.exists(_VBL.get_profile()):
    xbmcvfs.mkdirs(_VBL.get_profile())

def init_database():
    _VBL.log('Building VideoBull Database')
    if DB == 'mysql':
        db = orm.connect(DB_NAME, DB_USER,
                         DB_PASS, DB_ADDR, buffered=True)
        cur = db.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS tmp_tvshow_meta (url VARCHAR(255) UNIQUE, title TEXT, iconImg TEXT, year TEXT, imdbnum TEXT)')
        cur.execute(
            'CREATE TABLE IF NOT EXISTS favorites (type VARCHAR(10), name TEXT, url VARCHAR(255) UNIQUE, year VARCHAR(10))')
        cur.execute(
            'CREATE TABLE IF NOT EXISTS subscriptions (url VARCHAR(255) UNIQUE, title TEXT, iconImg TEXT, year TEXT, imdbnum TEXT)')
        cur.execute(
            'CREATE TABLE IF NOT EXISTS bookmarks (video_type VARCHAR(10), title VARCHAR(255), season INTEGER, episode INTEGER, year VARCHAR(10), bookmark VARCHAR(10))')
        cur.execute('CREATE TABLE IF NOT EXISTS url_cache (url VARCHAR(255), response TEXT, timestamp TEXT)')

        try:
            cur.execute('CREATE UNIQUE INDEX unique_bmk ON bookmarks (video_type, title, season, episode, year)')
        except:
            pass

    else:
        if not xbmcvfs.exists(os.path.dirname(DB_DIR)):
            xbmcvfs.mkdirs(os.path.dirname(DB_DIR))
        db = orm.connect(DB_DIR)
        db.execute('CREATE TABLE IF NOT EXISTS seasons (season UNIQUE, contents)')
        db.execute('CREATE TABLE IF NOT EXISTS favorites (type, name, url, year)')
        db.execute('CREATE TABLE IF NOT EXISTS tmp_tvshow_meta (url, title, iconImg, year, imdbnum)')
        db.execute('CREATE TABLE IF NOT EXISTS subscriptions (url, title, iconImg, year, imdbnum)')
        db.execute('CREATE TABLE IF NOT EXISTS bookmarks (video_type, title, season, episode, year, bookmark)')
        db.execute('CREATE TABLE IF NOT EXISTS url_cache (url UNIQUE, response, timestamp)')
        db.execute('CREATE UNIQUE INDEX IF NOT EXISTS unique_fav ON favorites (name, url)')
        db.execute('CREATE UNIQUE INDEX IF NOT EXISTS unique_sub ON subscriptions (url, title, year)')
        db.execute(
            'CREATE UNIQUE INDEX IF NOT EXISTS unique_bmk ON bookmarks (video_type, title, season, episode, year)')
        db.execute('CREATE UNIQUE INDEX IF NOT EXISTS unique_url ON url_cache (url)')
    db.commit()
    db.close()
dbg = False # Set to false if you don't want debugging
##### Queries ##########
total = addon.queries.get('total','')
play = addon.queries.get('play', '')
mode = addon.queries['mode']
level = addon.queries.get('level', '')
levels = addon.queries.get('levels', '')
video_type = addon.queries.get('video_type', '')
section = addon.queries.get('section', '')
url = addon.queries.get('url', '')
title = addon.queries.get('title', '')
name = addon.queries.get('name', '')
imdb_id = addon.queries.get('imdb_id', '')
season = addon.queries.get('season', '')
episode = addon.queries.get('episode', '')
year = addon.queries.get('year', '')
thumb = addon.queries.get('thumb', '')
iconImg = addon.queries.get('iconImg', '')
metatoggle= addon.queries.get('metatoggle', '')
theletter = addon.queries.get('theletter', '')
print '---------------------------------------------------------------'
print '--- Mode: ' + str(mode)
print '--- Play: ' + str(play)
print '--- URL: ' + str(url)
print '--- Video Type: ' + str(video_type)
print '--- Section: ' + str(section)
print '--- Title: ' + str(title)
print '--- Name: ' + str(name)
print '--- IMDB: ' + str(imdb_id)
print '--- Season: ' + str(season)
print '--- Episode: ' + str(episode)
print '--- Cover URL-Thumb: ' + str(thumb)
print '--- Cover URL-iconImg: ' + str(iconImg)
print '--- Cover MetaOn_Off: ' + str(metatoggle)
print '---------------------------------------------------------------'
################### Global Constants #################################
#URLS
MainUrl = 'http://www.videobull.com/'
SearchUrl = MainUrl + 'search/?q=%s&x=%s'
MovieUrl = MainUrl + "movies/"
TVUrl = MainUrl + "tv-shows/"
#PATHS
AddonPath = _VBL.get_path()
IconPath = AddonPath + "/resources/art/"
#VARIABLES
SearchMovies = 'movies'
SearchTV = 'shows'
SearchAll = 'all'
TheLetter = 'theletter'
VideoType_Movies = 'movie'
VideoType_TV = 'tvshow'
VideoType_Season = 'season'
VideoType_Episode = 'episode'
iconImg = 'tbn'
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
'Accept-Encoding': 'none',
'Accept-Language': 'en-US,en;q=0.8'}
def CATEGORIES():
        addDir('Latest TV Show Feed',MainUrl,7,IconPath +'icons/icon.png')
        addDir('Search for Shows',MainUrl,8,IconPath +'icons/search.png')
        addDir('A-Z TV Shows',MainUrl +'tv-shows/',9,IconPath +'letters/AZ.png')
        addDir('[COLOR blue]Resolver Settings[/COLOR]','RES',45,IconPath +'icons/icon.png')
def INDEX(url,name,iconImg):
        req = urllib2.Request(url, headers=hdr)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('/*/?<li>.+?a href="(.+?)" rel="bookmark" title="(.+?)">.+?img src="(.+?)".+?/>.?/a>.+?/li>', re.DOTALL).findall(link)
        for url,name,thumb in match:
            name=name.replace('&#8211','').replace(';','-').replace('&#8217',"'").replace('&#038','&').replace('&#8230','ss')
            cname=re.sub("([^-]*-[^-]*)(-.*$)", r"\1", name)
            aname=name.replace('Season','').replace('Episode','').replace('0','').replace('1','').replace('2','').replace('3','').replace('4','').replace('5','').replace('6','').replace('7','').replace('8','').replace('9','').replace('-\s.*?','')
            artname= re.sub("([^-]*-[^-]*)(-.*$)", r"\1", aname) 
            title = cname
            if META_ON:
                cover = __metaget__.get_meta('tvshow', artname, overlay=6)
                covers= re.compile("cover_url.+?'(.+?)'").findall(str(cover))
                iconImg=cover['cover_url']
                cache.set('Cover_url', iconImg)
            elif META_OFF:
                iconImg=thumb
            cache.set('Vidname', title)
            addDir(name,url,4,iconImg)          
def pages(url,name,iconImg):
	addDir('Page 1',MainUrl +'page/1/',2,'')
	addDir('Page 2',MainUrl +'page/2/',2,'')
	addDir('Page 3',MainUrl +'page/3/',2,'')
	addDir('Page 4',MainUrl +'page/4/',2,'')
	addDir('Page 5',MainUrl +'page/5/',2,'')
	addDir('Page 6',MainUrl +'page/6/',2,'')
	addDir('Page 7',MainUrl +'page/7/',2,'')
	addDir('Page 8',MainUrl +'page/8/',2,'')
	addDir('Page 9',MainUrl +'page/9/',2,'')
	addDir('Page 10',MainUrl +'page/10/',2,'')
def showEpp(url,name):
    req = urllib2.Request(url, headers=hdr)
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('<div id="contentarchive">.*?<a href="(.+?)" title="(.+?)">.+?</a>', re.DOTALL).findall(link)
    for url,name in match:
#        print "PlainURLMode40:"+url
#        print "showEppURL=====:"+url
        name=name.replace('&#8211','').replace(';','-').replace('&#8217',"'").replace('&#038','&').replace('&#8230','ss')
        cname=re.sub("([^-]*-[^-]*)(-.*$)", r"\1", name)
        aname=name.replace('Season','').replace('Episode','').replace('0','').replace('1','').replace('2','').replace('3','').replace('4','').replace('5','').replace('6','').replace('7','').replace('8','').replace('9','').replace('-\s.*?','')
        artname= re.sub("([^-]*-[^-]*)(-.*$)", r"\1", aname) 
        title = cname       
#        print "THIS IS ARTNAME:"+artname
        if META_ON:
            cover = __metaget__.get_meta('tvshow', artname, overlay=6)
            covers= re.compile("cover_url.+?'(.+?)'").findall(str(cover))
            iconImg=cover['cover_url']
            cache.set('Cover_url', iconImg)
        elif META_OFF:
            iconImg=IconPath +'icons/icon.png'
        cache.set('Vidname', title)
        addDir(title,url,4,iconImg)
def AtoZ(url,theletter,iconImg):
    for character in AZ_DIRECTORIES:
        theletter=character
        addDir(theletter,MainUrl +'tv-shows/',10,os.path.join(IconPath,'letters/',theletter+'.png'))
def AZT(url,theletter,iconImg):
        print str(theletter)
        req = urllib2.Request(url, headers=hdr)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('title="[%s](.*?)" href="(.*?)">.*?</a>' % name).findall(link)
        for title,url in match:
            title=name+title
#            meta = {'title': name, 'year': year, 'imdb_id': '', 'overlay':6, ''}
            if META_ON:
                cover = __metaget__.get_meta('tvshow', title, year, overlay=6)
                title = cover['TVShowTitle']
                iconImg=cover['cover_url']
            elif META_OFF:
                title=name
                iconImg=IconPath +'icons/icon.png'
            addDir(title,url,40,iconImg) 
def TvSearch(url):
    search_entered =search()
    name=str(search_entered).replace('+','')
    url='http://videobull.com/?s=' + search_entered + '&x=-1121&y=-30'
    link = getUrl(url)
    match=re.compile('<div id="contentarchivetitle">\n.*?<a href="(.+?)" title="(.+?)">.+?</a>', re.DOTALL).findall(link)
    for url,name in match:
        print "PlainURLMode40:"+url
        print "showEppURL=====:"+url
        name=name.replace('&#8211','').replace(';','-').replace('&#8217',"'").replace('&#038','&').replace('&#8230','ss')
        cname=re.sub("([^-]*-[^-]*)(-.*$)", r"\1", name)
        aname=name.replace('Season','').replace('Episode','').replace('0','').replace('1','').replace('2','').replace('3','').replace('4','').replace('5','').replace('6','').replace('7','').replace('8','').replace('9','').replace('-\s.*?','')
        artname= re.sub("([^-]*-[^-]*)(-.*$)", r"\1", aname) 
        title = cname
        if META_ON:
            cover = __metaget__.get_meta('tvshow', artname, overlay=6)
#            covers= re.compile("cover_url.+?'(.+?)'").findall(str(cover))
            img=cover['cover_url']
            cache.set('Cover_url', img)
        elif META_OFF:
            img=IconPath +'icons/icon.png'
        cache.set('Vidname', title)
        addDir(title,url,4,img)
def search():
        search_entered = ''
        keyboard = xbmc.Keyboard(search_entered, 'Search for Shows on Videobull.com')
        keyboard.doModal()
        if keyboard.isConfirmed():
            search_entered = keyboard.getText() .replace(' ','+')  # sometimes you need to replace spaces with + or %20
            if search_entered == None:
                return False          
        return search_entered	
def getUrl(url):
    req = urllib2.Request(url, headers=hdr)
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link        
def read(url):
#    _log("read "+url)
    f = urllib2.urlopen(url)
    data = f.read()
    f.close()
    return data
def VIDEOLINKS(url,name):
    req = urllib2.Request(url, headers=hdr)
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('''<a id='.+?' href='.*?title=(.+?)' target='_blank' rel='nofollow'>(.+?)</a>''', re.DOTALL).findall(link)
    print match
    for link,source in match:     
     addDir(source,link,5,iconImg)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
def PLAYLINKS(url,name,iconImg):
        regexlink = url
        url = base64.b64decode(regexlink)
        hostUrl = url
        videoLink = urlresolver.resolve(hostUrl)      
        vName=cache.get('Vidname')
        vName=vName.replace('&#8211','').replace(';','-').replace('&#8217',"'").replace('&#038','&').replace('&#8230','ss')
        cname=re.sub("([^-]*-[^-]*)(-.*$)", r"\1", vName)
        aname=cname.replace('Season','').replace('Episode','').replace('0','').replace('1','').replace('2','').replace('3','').replace('4','').replace('5','').replace('6','').replace('7','').replace('8','').replace('9','').replace('-\s.*?','')
        artname=re.sub("([^-]*-[^-]*)(-.*$)", r"\1", aname) 
        print "ARTNAME:"+artname
        cover = __metaget__.get_meta('tvshow', artname, overlay=6)
        ctitle = cover['TVShowTitle']
        name=cname
        tbn=cover['cover_url']
        iconImg=tbn
        player = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
        listitem = xbmcgui.ListItem(name, iconImg)
        listitem.setInfo('video', {'Title': name})
        listitem.setThumbnailImage(iconImg)
        player.play(videoLink,listitem)
        addLink('Restart Stream',videoLink,iconImg) 

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
def addLink(name,url,iconImg):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconImg)
        liz.setInfo( type="Video", infoLabels={ "Title": name,"url": url, "Icon": iconImg } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok
def addDir(name,url,mode,iconImg):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconImg)
        liz.setInfo( type="Video", infoLabels={ "Title": name,"url": url, "Icon": iconImg } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
def setView(content, viewType):
        # set content type so library shows more views and info
        if content:
                xbmcplugin.setContent(int(sys.argv[1]), content)
        if ADDON.getSetting('auto-view') == 'true':#<<<----see here if auto-view is enabled(true)
                xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )#<<<-----then get the view type
params=get_params()
url=None
name=None
mode=None
iconImg=''
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
try:
        url=urllib.unquote_plus(params["iconImg"])
except:
        pass
print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IconImg:"+str(iconImg)
if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
       
elif mode==2:
        print ""+url
        INDEX(url,name,iconImg)
elif mode==6:
        print ""+url
        INDEX3(url,name,iconImg)

elif mode==3:
        print ""+url
        EPISODES(url,name,iconImg)

elif mode==4:
        print ""+url
        VIDEOLINKS(url,name)

elif mode==5:
#        import urlresolver
        print ""+url
        PLAYLINKS(url,name,iconImg)
elif mode==7:
        print ""+url
        pages(url,name,iconImg)
elif mode==8:
        print ""+url
        TvSearch(url)
elif mode==9:
        print ""+url
        AtoZ(url,theletter,iconImg)
elif mode==10:
        print ""+url
        AZT(url,theletter,iconImg)	
elif mode==40:
        print ""+url
        showEpp(url,name)			
elif mode==45 or url==RES:
#        import urlresolver
        print ""+url
        urlresolver.display_settings()			
xbmcplugin.endOfDirectory(int(sys.argv[1]))