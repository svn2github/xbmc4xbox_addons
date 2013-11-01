import urllib,urllib2,re,cookielib,xbmcplugin,xbmcgui,xbmcaddon,socket,os,shutil,string,xbmc,stat,xbmcvfs
import base64

from t0mm0.common.net import Net as net
from t0mm0.common.addon import Addon
from metahandler import metahandlers
from metahandler import metacontainers

pluginhandle = int(sys.argv[1])
addon = Addon('plugin.video.videobull', sys.argv)
fanart = "resources/art/fanart.png"
xbmc_skin = xbmc.getSkinDir()
ADDON = xbmcaddon.Addon(id='plugin.video.videobull')
grab = metahandlers.MetaData(preparezip = False)
try:
    import StorageServer
except:
    import storageserverdummy as StorageServer
cache = StorageServer.StorageServer('plugin.video.videobull', 48)
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
plot = addon.queries.get('plot', '')
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
print '--- PLOT: ' + str(plot)
print '---------------------------------------------------------------'
################### Global Constants #################################
#URLS
MainUrl = 'http://www.videobull.com/'
SearchUrl = MainUrl + 'search/?q=%s&x=%s'
MovieUrl = MainUrl + "movies/"
TVUrl = MainUrl + "tv-shows/"
#PATHS
AddonPath = addon.get_path()
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
meta = {'title': name, 'year': year, 'imdb_id': '', 'plot': plot, 'fanart': fanart, 'overlay':6}
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
'Accept-Encoding': 'none',
'Accept-Language': 'en-US,en;q=0.8'}
def CATEGORIES():
        addMenu('[COLOR blue][B]Latest TV Show Feed[/B][/COLOR]',MainUrl,2,IconPath +'icons/icon.png',None,'')
        addMenu('[COLOR blue][B]A-Z TV Shows[/B][/COLOR]',MainUrl +'tv-shows/',9,IconPath +'letters/AZ.png',None,'')
        addMenu('[COLOR blue][B]Search for TV Shows[/B][/COLOR]',MainUrl,8,IconPath +'icons/search.png',None,'')
        addMenu('Resolver Settings','RES',45,IconPath +'icons/icon.png',None,'')
        setView('movies', 'default')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
def INDEX(url,name,iconImg):
        pDialog = xbmcgui.DialogProgress(3,'')
        ret = pDialog.create('Videobull', 'Requesting Page from internet')
        pDialog.update(2, 'Requesting webpages...')
        req = urllib2.Request(url, headers=hdr)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        pDialog.update(25, 'Reading webpages...')
        digz=re.compile(r""".*<\/span><a href='(.+?)' class=\'nextpostslink\'>></a>""", re.DOTALL).findall(link)
        numurl=str(digz[0])
        curpage=re.compile('''<span class='pages'>Page (.+?) of (.+?)</span>''', re.DOTALL).findall(link)
        for curpg,totpg in curpage:  
            addMenu('[B][I]Viewing Page : [/I][COLOR gold]'+curpg+'[/COLOR][COLOR blue] / [/COLOR][COLOR gold]'+totpg+'[/COLOR] Pages '+'[COLOR blue]| Next Page>> [/B][/COLOR]',numurl,2,'',None,'')
            match=re.compile('/*/?<li>.+?a href="(.+?)" rel="bookmark" title=".+?">.+?img src="(.+?)".+?/>.?/a>.+?/li>', re.DOTALL).findall(link)
            for url,thumb in match:
                name=url.replace('http://videobull.com/','').replace('%e2%80%99','`').replace('-season-',' : Season ').replace('-episode-',' Episode ').replace('/',' |').replace('-',' ')
                cname=name
                name = cname            
                artname=re.sub('\:.*','', cname) 
#                pDialog.update(68, 'Caching Thumbnails')       
                pDialog.update(32, 'Parsing links...')
                if META_OFF==True:
                    pDialog.update(40, 'Checking plugin settings...')
                    iconImg=thumb
                    pDialog.update(42, 'Metadata is turned off, not grabbing extra tvdb art...')
                else:
				    pass
                pDialog.update(53, 'Parsing links...')
                addDir(name,url,4,iconImg,'tvshow',artname)
                cache.set('Vidname', name)
                pDialog.update(87, 'Compiling results into GUI List...')
            xbmcplugin.endOfDirectory(int(sys.argv[1]))
            pDialog.update(2,'Closing Dialog')
            pDialog.close()                      

def showEpp(url,name,types,meta_name):
    req = urllib2.Request(url, headers=hdr)
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('<div id="contentarchive">.*?<a href="(.+?)" title=".+?">.+?</a>', re.DOTALL).findall(link)
    for url in match:
        name=url.replace('http://videobull.com/','').replace('%e2%80%99','`').replace('-season-',' : Season ').replace('-episode-',' Episode ').replace('/',' |').replace('-',' ')
        cname=name
        artname=re.sub('\:.*','', cname)        
        name = cname       
        addDir(name,url,4,iconImg,'tvshow',artname)
        setView('movies', 'default')
        cache.set('Vidname', name)
        xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))        
def AtoZ(url,theletter,iconImg):
    for character in AZ_DIRECTORIES:
        theletter=character
        addMenu(theletter,MainUrl +'tv-shows/',10,os.path.join(IconPath,'letters/',theletter+'.png'),None,'')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
def AZT(url,theletter,iconImg,types,meta_name):
        print str(theletter)
        req = urllib2.Request(url, headers=hdr)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('title="[%s](.*?)" href="(.*?)">.*?</a>' % name).findall(link)
        for title,url in match:
            title=name+title
            addDir(title,url,40,iconImg,'tvshow',title) 
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_TITLE)
        setView('movies', 'default')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))	
def TvSearch(url):
    search_entered =search()
    name=str(search_entered).replace('+','')
    url='http://videobull.com/?s=' + search_entered + '&x=-1121&y=-30'
    link = getUrl(url)
    match=re.compile('<div id="contentarchivetitle">\n.*?<a href="(.+?)" title=".+?">.+?</a>', re.DOTALL).findall(link)
    for url in match:
        print "PlainURLMode40:"+url
        print "showEppURL=====:"+url
        name=url.replace('http://videobull.com/','').replace('%e2%80%99','`').replace('-season-',' : Season ').replace('-episode-',' Episode ').replace('/',' |').replace('-',' ')
        cname=name 
        artname=re.sub('\:.*','', cname)
        title = cname
        cache.set('Vidname', title)
        addDir(title,url,4,iconImg,'tvshow',artname)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
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
def VIDEOLINKS(url,name,types,meta_name):
    req = urllib2.Request(url, headers=hdr)
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('''<a id='.+?' href='.*?title=(.+?)' target='_blank' rel='nofollow'>(.+?)</a>''', re.DOTALL).findall(link)
    cache.set('Vidname', name)
    for url,source in match:    
        addDir(name+' || '+'[COLOR blue][B]'+source+'[/B][/COLOR]',url,5,iconImg,'tvshow',name)    
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_TITLE)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
def PLAYLINKS(url,name,types):
        regexlink = url
        url = base64.b64decode(regexlink)
        hostUrl = url
        videoLink = urlresolver.resolve(hostUrl)      
        artname=re.sub('\:.*','', meta_name) 
        if META_OFF==True:
            infoLabels={ "Title": name, 'cover_url': iconImg }
        else:
            pass
        infoLabels=GRABMETA(artname,'tvshow')
        player = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
        listitem = xbmcgui.ListItem(name, iconImg, iconImg)
        listitem.setInfo('video', infoLabels=infoLabels)
        listitem.setThumbnailImage(infoLabels['cover_url'])
        player.play(videoLink,listitem)
        addLink('Restart Stream '+ name,str(videoLink),iconImg,'tvshow',artname)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))		

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
		
def GRABMETA(meta_name,types):
    type = types
    meta = grab.get_meta('tvshow',meta_name,None,None,None,overlay=6)
    infoLabels = {'backdrop_url': meta['backdrop_url'], 'cover_url': meta['cover_url'],
                  'plot': meta['plot'], 'title': name, 'TVShowTitle': meta['TVShowTitle']}
    if type == None: infoLabels = {'cover_url': '','title': name}    
    return infoLabels	
def addLink(name,url,iconImg,types,meta_name):
        infoLabels=GRABMETA(meta_name,types)        
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconImg)
        liz.setInfo( type="Video", infoLabels=infoLabels)
        liz.setProperty('fanart_image', infoLabels['backdrop_url'])        
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok
def addDir(name,url,mode,iconImg,types,meta_name):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&types="+str(types)+"&meta_name="+str(meta_name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=IconPath +'icons/icon.png', thumbnailImage=iconImg)
        if META_ON==True:
            infoLabels=GRABMETA(meta_name,types) 
            iconImg=infoLabels['cover_url']
            liz=xbmcgui.ListItem(name, iconImage=IconPath +'icons/icon.png', thumbnailImage=iconImg)
            liz.setProperty('fanart_image', infoLabels['backdrop_url'])
            liz.setInfo( type="Video", infoLabels=infoLabels)
        else:
            infoLabels={ "Title": name, 'cover_url': iconImg }
            iconImg=iconImg
            liz=xbmcgui.ListItem(name, iconImage=IconPath +'icons/icon.png', thumbnailImage=iconImg)
            liz.setProperty('fanart_image', '')
            liz.setInfo( type="Video", infoLabels=infoLabels)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
def addMenu(name,url,mode,iconImg,types,meta_name):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconImg)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image', IconPath +'fanart2.png')
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok		
def setView(content, viewType):
        # set content type so library shows more views and info
        if content:
                xbmcplugin.setContent(int(sys.argv[1]), content)
        if addon.get_setting('auto-view') == 'true':#<<<----see here if auto-view is enabled(true)
                xbmc.executebuiltin("Container.SetViewMode(%s)" % addon.get_setting(viewType) )#<<<-----then get the view type
params=get_params()
url=None
name=None
mode=None
iconImg=''
types=None
meta_name=None
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
try:
        types=urllib.unquote_plus(params["types"])
except:
        pass
try:
        meta_name=urllib.unquote_plus(params["meta_name"])
except:
        pass
print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IconImg:"+str(iconImg)
print "TYPEs:"+str(types)
print 'Meta_Name: '+str(meta_name)
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
        VIDEOLINKS(url,name,types,meta_name)

elif mode==5:
        import urlresolver
        print ""+url
        PLAYLINKS(url,name,types)
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
        AZT(url,theletter,iconImg,types,meta_name)	
elif mode==40:
        print ""+url
        showEpp(url,name,types,meta_name)			
elif mode==45: #or url==RES:
        import urlresolver
        print ""+url
        urlresolver.display_settings()			
#elif mode==58:
#        print "Metahandler Settings"
#        import metahandler
#        metahandler.display_settings()
#        callEndOfDirectory = False
xbmcplugin.endOfDirectory(int(sys.argv[1]))