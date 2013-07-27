import urllib,urllib2,re,cookielib,xbmcplugin,xbmcgui,xbmcaddon,socket,os,shutil,string,xbmc,stat,xbmcvfs
import base64
from operator import itemgetter
from t0mm0.common.net import Net as net
from t0mm0.common.addon import Addon
from metahandler import metahandlers
from metahandler import metacontainers
from zipfile import ZipFile as zip
#from BeautifulSoup import BeautifulSoup as soup
#import script.common.plugin.cache
pluginhandle = int(sys.argv[1])
#SET DIRECTORIES
local = xbmcaddon.Addon(id='plugin.video.videobull')
addon = Addon('plugin.video.videobull', sys.argv)

#grab = metahandlers.MetaData(None,preparezip = False)
fanart = "resources/art/fanart.png"
xbmc_skin = xbmc.getSkinDir()


try:
    import StorageServer
except:
    import storageserverdummy as StorageServer
cache = StorageServer.StorageServer('plugin.video.videobull', 24)
_VBL = Addon('plugin.video.videobull', sys.argv)
META_ON = _VBL.get_setting('use-meta') == 'true'
META_OFF = _VBL.get_setting('use-meta') == 'false'

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
        cur.execute('CREATE TABLE IF NOT EXISTS tmp_tvshow_meta (season INTEGER UNIQUE, contents TEXT)')
        cur.execute(
            'CREATE TABLE IF NOT EXISTS favorites (type VARCHAR(10), name TEXT, url VARCHAR(255) UNIQUE, year VARCHAR(10))')
        cur.execute(
            'CREATE TABLE IF NOT EXISTS subscriptions (url VARCHAR(255) UNIQUE, title TEXT, img TEXT, year TEXT, imdbnum TEXT)')
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
        db.execute('CREATE TABLE IF NOT EXISTS subscriptions (url, title, img, year, imdbnum)')
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

#Common Cache
#try:
#  import StorageServer
#except:
#  import storageserverdummy as StorageServer
#cache = StorageServer.StorageServer('plugin.video.videobull')

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
img = addon.queries.get('img', '')
metatoggle= addon.queries.get('metatoggle', '')
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
print '--- Cover URL-IMG: ' + str(img)
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

VideoType_Movies = 'movie'
VideoType_TV = 'tvshow'
VideoType_Season = 'season'
VideoType_Episode = 'episode'




def CATEGORIES():
        addDir('Latest TV Show Feed',MainUrl,7,IconPath +'icons/icon.png')
        addDir('Search for Shows',MainUrl,8,IconPath +'icons/search.png')
        addDir('A-Z TV Shows',MainUrl +'tv-shows/',9,IconPath +'letters/AZ.png')
        addDir('[COLOR blue]Resolver Settings[/COLOR]','RES',45,IconPath +'icons/icon.png')

        xbmcplugin.endOfDirectory(pluginhandle)		

		
def INDEX(url):
        
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}
        req = urllib2.Request(url, headers=hdr)	   
        response = urllib2.urlopen(req)
        link=response.read()
        
        response.close()
        match = re.compile('/*/?<item>.+?title>(.+?).?/title>.+?link>(.+?).?/link>.+?/item>', re.DOTALL).findall(link)
        for name,url in match:
                addDir(name,url,4,'')
def INDEX2(url):
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}
        req = urllib2.Request(url, headers=hdr)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('/*/?<li>.+?a href="(.+?)" rel="bookmark" title="(.+?)">.+?img src="(.+?)".+?/>.?/a>.+?/li>', re.DOTALL).findall(link)
        for url,name,thumb in match:
#		plugintools.add_item( action="play" , title=title , url=url )
            name=name.replace('&#8211','').replace(';','-').replace('&#8217',"'").replace('&#038','&').replace('&#8230','ss')
            cname=re.sub("([^-]*-[^-]*)(-.*$)", r"\1", name)
            aname=name.replace('Season','').replace('Episode','').replace('0','').replace('1','').replace('2','').replace('3','').replace('4','').replace('5','').replace('6','').replace('7','').replace('8','').replace('9','').replace('-\s.*?','')
            artname= re.sub("([^-]*-[^-]*)(-.*$)", r"\1", aname) 
            title = cname
            if META_ON:
                cover = __metaget__.get_meta('tvshow', artname, overlay=6)
                covers= re.compile("cover_url.+?'(.+?)'").findall(str(cover))
                img=cover['cover_url']
                cache.set('Cover_url', img)
            elif META_OFF:
                img=thumb
            cache.set('Vidname', title)
            addDir(name,url,4,img)
           
def pages(url):
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

def showEpp(url):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}
    req = urllib2.Request(url, headers=hdr)
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('<div id="contentarchive">.*?<a href="(.+?)" title="(.+?)">.+?</a>', re.DOTALL).findall(link)
    for url,name in match:
        print "PlainURLMode40:"+url
        print "showEppURL=====:"+url
        name=name.replace('&#8211','').replace(';','-').replace('&#8217',"'").replace('&#038','&').replace('&#8230','ss')
        cname=re.sub("([^-]*-[^-]*)(-.*$)", r"\1", name)
        aname=name.replace('Season','').replace('Episode','').replace('0','').replace('1','').replace('2','').replace('3','').replace('4','').replace('5','').replace('6','').replace('7','').replace('8','').replace('9','').replace('-\s.*?','')
        artname= re.sub("([^-]*-[^-]*)(-.*$)", r"\1", aname) 
        title = cname
        
        print "THIS IS ARTNAME:"+artname
        if META_ON:
            cover = __metaget__.get_meta('tvshow', artname, overlay=6)
            covers= re.compile("cover_url.+?'(.+?)'").findall(str(cover))
            img=cover['cover_url']
            cache.set('Cover_url', img)
        elif META_OFF:
            img=IconPath +'icons/icon.png'
        cache.set('Vidname', title)
        addDir(title,url,4,img)
def AtoZ(url):
   addDir('A',MainUrl +'tv-shows/',10,IconPath +'letters/A.png')
   addDir('B',MainUrl +'tv-shows/',11,IconPath +'letters/B.png')
   addDir('C',MainUrl +'tv-shows/',12,IconPath +'letters/C.png')
   addDir('D',MainUrl +'tv-shows/',13,IconPath +'letters/D.png')
   addDir('E',MainUrl +'tv-shows/',14,IconPath +'letters/E.png')
   addDir('F',MainUrl +'tv-shows/',15,IconPath +'letters/F.png')
   addDir('G',MainUrl +'tv-shows/',16,IconPath +'letters/G.png')
   addDir('H',MainUrl +'tv-shows/',17,IconPath +'letters/H.png')
   addDir('I',MainUrl +'tv-shows/',18,IconPath +'letters/I.png')
   addDir('J',MainUrl +'tv-shows/',19,IconPath +'letters/J.png')
   addDir('K',MainUrl +'tv-shows/',20,IconPath +'letters/K.png')
   addDir('L',MainUrl +'tv-shows/',21,IconPath +'letters/L.png')
   addDir('M',MainUrl +'tv-shows/',22,IconPath +'letters/M.png')
   addDir('N',MainUrl +'tv-shows/',23,IconPath +'letters/N.png')
   addDir('O',MainUrl +'tv-shows/',24,IconPath +'letters/O.png')
   addDir('P',MainUrl +'tv-shows/',25,IconPath +'letters/P.png')
   addDir('Q',MainUrl +'tv-shows/',26,IconPath +'letters/Q.png')
   addDir('R',MainUrl +'tv-shows/',27,IconPath +'letters/R.png')
   addDir('S',MainUrl +'tv-shows/',28,IconPath +'letters/S.png')
   addDir('T',MainUrl +'tv-shows/',29,IconPath +'letters/T.png')
   addDir('U',MainUrl +'tv-shows/',30,IconPath +'letters/U.png')
   addDir('V',MainUrl +'tv-shows/',31,IconPath +'letters/V.png')
   addDir('W',MainUrl +'tv-shows/',32,IconPath +'letters/W.png')
   addDir('X',MainUrl +'tv-shows/',33,IconPath +'letters/X.png')
   addDir('Y',MainUrl +'tv-shows/',34,IconPath +'letters/Y.png')
   addDir('Z',MainUrl +'tv-shows/',35,IconPath +'letters/Z.png')
def A(url,name):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}
    req = urllib2.Request(url, headers=hdr)
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('title="[A](.*?)" href="(.*?)">.*?</a>').findall(link)
    meta = {'title': name, 'year': year, 'imdb_id': '', 'overlay': ''}
    for name,url in match:
        name='A'+name       
        if META_ON:
            cover = __metaget__.get_meta('tvshow', name, year, overlay=6)      
            title = cover['TVShowTitle']
            img=cover['cover_url']
        elif META_OFF:
            title=name
            img=IconPath +'icons/icon.png' 			
        addDir(title,url,40,img)

def B(url):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}
    req = urllib2.Request(url, headers=hdr)
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('title="[B](.*?)" href="(.*?)">.*?</a>').findall(link)
    for name,url in match:
        name='B'+name        
        if META_ON:
            cover = __metaget__.get_meta('tvshow', name, year, overlay=6)      
            title = cover['TVShowTitle']
            img=cover['cover_url']
        elif META_OFF:
            title=name
            img=IconPath +'icons/icon.png' 			
        addDir(title,url,40,img)

def C(url):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}
    req = urllib2.Request(url, headers=hdr)
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('title="[C](.*?)" href="(.*?)">.*?</a>').findall(link)
    for name,url in match:
        name='C'+name
        if META_ON:
            cover = __metaget__.get_meta('tvshow', name, year, overlay=6)      
            title = cover['TVShowTitle']
            img=cover['cover_url']
        elif META_OFF:
            title=name
            img=IconPath +'icons/icon.png' 			
        addDir(title,url,40,img)

def D(url):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}
    req = urllib2.Request(url, headers=hdr)
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('title="[D](.*?)" href="(.*?)">.*?</a>').findall(link)
    for name,url in match:
        name='D'+name
        if META_ON:
            cover = __metaget__.get_meta('tvshow', name, year, overlay=6)      
            title = cover['TVShowTitle']
            img=cover['cover_url']
        elif META_OFF:
            title=name
            img=IconPath +'icons/icon.png' 			
        addDir(title,url,40,img)
def E(url):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}
    req = urllib2.Request(url, headers=hdr)
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('title="[E](.*?)" href="(.*?)">.*?</a>').findall(link)
    for name,url in match:
        name='E'+name
        if META_ON:
            cover = __metaget__.get_meta('tvshow', name, year, overlay=6)      
            title = cover['TVShowTitle']
            img=cover['cover_url']
        elif META_OFF:
            title=name
            img=IconPath +'icons/icon.png' 			
        addDir(title,url,40,img)
def F(url):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}
    req = urllib2.Request(url, headers=hdr)
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('title="[F](.*?)" href="(.*?)">.*?</a>').findall(link)
    for name,url in match:
        name='F'+name
        if META_ON:
            cover = __metaget__.get_meta('tvshow', name, year, overlay=6)      
            title = cover['TVShowTitle']
            img=cover['cover_url']
        elif META_OFF:
            title=name
            img=IconPath +'icons/icon.png' 			
        addDir(title,url,40,img)
def G(url):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}
    req = urllib2.Request(url, headers=hdr)
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('title="[G](.*?)" href="(.*?)">.*?</a>').findall(link)
    for name,url in match:
        name='G'+name
        if META_ON:
            cover = __metaget__.get_meta('tvshow', name, year, overlay=6)      
            title = cover['TVShowTitle']
            img=cover['cover_url']
        elif META_OFF:
            title=name
            img=IconPath +'icons/icon.png' 			
        addDir(title,url,40,img)		
def H(url):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}
    req = urllib2.Request(url, headers=hdr)
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('title="[H](.*?)" href="(.*?)">.*?</a>').findall(link)
    for name,url in match:
        name='H'+name
        if META_ON:
            cover = __metaget__.get_meta('tvshow', name, year, overlay=6)      
            title = cover['TVShowTitle']
            img=cover['cover_url']
        elif META_OFF:
            title=name
            img=IconPath +'icons/icon.png' 			
        addDir(title,url,40,img)
def I(url):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}
    req = urllib2.Request(url, headers=hdr)
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('title="[I](.*?)" href="(.*?)">.*?</a>').findall(link)
    for name,url in match:
        name='I'+name
        if META_ON:
            cover = __metaget__.get_meta('tvshow', name, year, overlay=6)      
            title = cover['TVShowTitle']
            img=cover['cover_url']
        elif META_OFF:
            title=name
            img=IconPath +'icons/icon.png' 			
        addDir(title,url,40,img)	
def J(url):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}
    req = urllib2.Request(url, headers=hdr)
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('title="[J](.*?)" href="(.*?)">.*?</a>').findall(link)
    for name,url in match:
        name='J'+name
        if META_ON:
            cover = __metaget__.get_meta('tvshow', name, year, overlay=6)      
            title = cover['TVShowTitle']
            img=cover['cover_url']
        elif META_OFF:
            title=name
            img=IconPath +'icons/icon.png' 			
        addDir(title,url,40,img)	
def K(url):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}
    req = urllib2.Request(url, headers=hdr)
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('title="[K](.*?)" href="(.*?)">.*?</a>').findall(link)
    for name,url in match:
        name='K'+name
        if META_ON:
            cover = __metaget__.get_meta('tvshow', name, year, overlay=6)      
            title = cover['TVShowTitle']
            img=cover['cover_url']
        elif META_OFF:
            title=name
            img=IconPath +'icons/icon.png' 			
        addDir(title,url,40,img)		
def L(url):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}
    req = urllib2.Request(url, headers=hdr)
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('title="[L](.*?)" href="(.*?)">.*?</a>').findall(link)
    for name,url in match:
        name='L'+name
        if META_ON:
            cover = __metaget__.get_meta('tvshow', name, year, overlay=6)      
            title = cover['TVShowTitle']
            img=cover['cover_url']
        elif META_OFF:
            title=name
            img=IconPath +'icons/icon.png' 			
        addDir(title,url,40,img)	
def M(url):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}
    req = urllib2.Request(url, headers=hdr)
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('title="[M](.*?)" href="(.*?)">.*?</a>').findall(link)
    for name,url in match:
        name='M'+name
        if META_ON:
            cover = __metaget__.get_meta('tvshow', name, year, overlay=6)      
            title = cover['TVShowTitle']
            img=cover['cover_url']
        elif META_OFF:
            title=name
            img=IconPath +'icons/icon.png' 			
        addDir(title,url,40,img)
def N(url):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}
    req = urllib2.Request(url, headers=hdr)
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('title="[N](.*?)" href="(.*?)">.*?</a>').findall(link)
    for name,url in match:
        name='N'+name
        if META_ON:
            cover = __metaget__.get_meta('tvshow', name, year, overlay=6)      
            title = cover['TVShowTitle']
            img=cover['cover_url']
        elif META_OFF:
            title=name
            img=IconPath +'icons/icon.png' 			
        addDir(title,url,40,img)		
def O(url):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}
    req = urllib2.Request(url, headers=hdr)
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('title="[O](.*?)" href="(.*?)">.*?</a>').findall(link)
    for name,url in match:
        name='O'+name
        if META_ON:
            cover = __metaget__.get_meta('tvshow', name, year, overlay=6)      
            title = cover['TVShowTitle']
            img=cover['cover_url']
        elif META_OFF:
            title=name
            img=IconPath +'icons/icon.png' 			
        addDir(title,url,40,img)
def P(url):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}
    req = urllib2.Request(url, headers=hdr)
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('title="[P](.*?)" href="(.*?)">.*?</a>').findall(link)
    for name,url in match:
        name='P'+name
        if META_ON:
            cover = __metaget__.get_meta('tvshow', name, year, overlay=6)      
            title = cover['TVShowTitle']
            img=cover['cover_url']
        elif META_OFF:
            title=name
            img=IconPath +'icons/icon.png' 			
        addDir(title,url,40,img)
def Q(url):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}
    req = urllib2.Request(url, headers=hdr)
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('title="[Q](.*?)" href="(.*?)">.*?</a>').findall(link)
    for name,url in match:
        name='Q'+name
        if META_ON:
            cover = __metaget__.get_meta('tvshow', name, year, overlay=6)      
            title = cover['TVShowTitle']
            img=cover['cover_url']
        elif META_OFF:
            title=name
            img=IconPath +'icons/icon.png' 			
        addDir(title,url,40,img)	
def R(url):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}
    req = urllib2.Request(url, headers=hdr)
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('title="[R](.*?)" href="(.*?)">.*?</a>').findall(link)
    for name,url in match:
        name='R'+name
        if META_ON:
            cover = __metaget__.get_meta('tvshow', name, year, overlay=6)      
            title = cover['TVShowTitle']
            img=cover['cover_url']
        elif META_OFF:
            title=name
            img=IconPath +'icons/icon.png' 			
        addDir(title,url,40,img)		
def S(url):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}
    req = urllib2.Request(url, headers=hdr)
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('title="[S](.*?)" href="(.*?)">.*?</a>').findall(link)
    for name,url in match:
        name='S'+name
        if META_ON:
            cover = __metaget__.get_meta('tvshow', name, year, overlay=6)      
            title = cover['TVShowTitle']
            img=cover['cover_url']
        elif META_OFF:
            title=name
            img=IconPath +'icons/icon.png' 			
        addDir(title,url,40,img)		
def T(url):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}
    req = urllib2.Request(url, headers=hdr)
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('title="[T](.*?)" href="(.*?)">.*?</a>').findall(link)
    for name,url in match:
        name='T'+name
        if META_ON:
            cover = __metaget__.get_meta('tvshow', name, year, overlay=6)      
            title = cover['TVShowTitle']
            img=cover['cover_url']
        elif META_OFF:
            title=name
            img=IconPath +'icons/icon.png' 			
        addDir(title,url,40,img)	
def U(url):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}
    req = urllib2.Request(url, headers=hdr)
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('title="[U](.*?)" href="(.*?)">.*?</a>').findall(link)
    for name,url in match:
        name='U'+name
        if META_ON:
            cover = __metaget__.get_meta('tvshow', name, year, overlay=6)      
            title = cover['TVShowTitle']
            img=cover['cover_url']
        elif META_OFF:
            title=name
            img=IconPath +'icons/icon.png' 			
        addDir(title,url,40,img)		
def V(url):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}
    req = urllib2.Request(url, headers=hdr)
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('title="[V](.*?)" href="(.*?)">.*?</a>').findall(link)
    for name,url in match:
        name='V'+name
        if META_ON:
            cover = __metaget__.get_meta('tvshow', name, year, overlay=6)      
            title = cover['TVShowTitle']
            img=cover['cover_url']
        elif META_OFF:
            title=name
            img=IconPath +'icons/icon.png' 			
        addDir(title,url,40,img)		
def W(url):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}
    req = urllib2.Request(url, headers=hdr)
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('title="[W](.*?)" href="(.*?)">.*?</a>').findall(link)
    for name,url in match:
        name='W'+name
        if META_ON:
            cover = __metaget__.get_meta('tvshow', name, year, overlay=6)      
            title = cover['TVShowTitle']
            img=cover['cover_url']
        elif META_OFF:
            title=name
            img=IconPath +'icons/icon.png' 			
        addDir(title,url,40,img)		
def X(url):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}
    req = urllib2.Request(url, headers=hdr)
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('title="[X](.*?)" href="(.*?)">.*?</a>').findall(link)
    for name,url in match:
        name='X'+name
        if META_ON:
            cover = __metaget__.get_meta('tvshow', name, year, overlay=6)      
            title = cover['TVShowTitle']
            img=cover['cover_url']
        elif META_OFF:
            title=name
            img=IconPath +'icons/icon.png' 			
        addDir(title,url,40,img)		
def Y(url):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}
    req = urllib2.Request(url, headers=hdr)
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('title="[Y](.*?)" href="(.*?)">.*?</a>').findall(link)
    for name,url in match:
        name='Y'+name
        if META_ON:
            cover = __metaget__.get_meta('tvshow', name, year, overlay=6)      
            title = cover['TVShowTitle']
            img=cover['cover_url']
        elif META_OFF:
            title=name
            img=IconPath +'icons/icon.png' 			
        addDir(title,url,40,img)	
def Z(url):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}
    req = urllib2.Request(url, headers=hdr)
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('title="[Z](.*?)" href="(.*?)">.*?</a>').findall(link)
    for name,url in match:
        name='Z'+name
        if META_ON:
            cover = __metaget__.get_meta('tvshow', name, year, overlay=6)      
            title = cover['TVShowTitle']
            img=cover['cover_url']
        elif META_OFF:
            title=name
            img=IconPath +'icons/icon.png' 			
        addDir(title,url,40,img)	
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
        
        print "THIS IS ARTNAME:"+artname
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
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}
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
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}
    req = urllib2.Request(url, headers=hdr)
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('''<a id='.+?' href='.*?title=(.+?)' target='_blank' rel='nofollow'>(.+?)</a>''', re.DOTALL).findall(link)
    print match
    for url,name in match:     
     addDir(name,url,5,'')
         
            
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
                      
def PLAYLINKS(url,name):
        regexlink = url
        url = base64.b64decode(regexlink)
        hostUrl = url
        videoLink = urlresolver.resolve(hostUrl)      
        vName=cache.get('Vidname')
        print "VNAME:"+vName
        if META_ON:
            img=cache.get('Cover_url')
            print "THUMBNAILCACHENAME"+img
        elif META_OFF:
            img=IconPath +'icons/icon.png'
        name=vName
        player = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
        listitem = xbmcgui.ListItem(name, img, img)
        listitem.setInfo('video', {'Title': name})
        listitem.setThumbnailImage(img)
        player.play(videoLink,listitem)
        addLink('Restart Stream',videoLink,img) 


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

def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
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
        INDEX(url)
        
elif mode==2:
        print ""+url
        INDEX2(url)
		
elif mode==6:
        print ""+url
        INDEX3(url)

elif mode==3:
        print ""+url
        EPISODES(url)

elif mode==4:
        print ""+url
        VIDEOLINKS(url,name)

elif mode==5:
        import urlresolver
        print ""+url
        PLAYLINKS(url,name)
elif mode==7:
        print ""+url
        pages(url)
elif mode==8:
        print ""+url
        TvSearch(url)
elif mode==9:
        print ""+url
        AtoZ(url)
elif mode==10:
        print ""+url
        A(url,name)
elif mode==11:
        print ""+url
        B(url)		
elif mode==12:
        print ""+url
        C(url)		
elif mode==13:
        print ""+url
        D(url)		
elif mode==14:
        print ""+url
        E(url)		
elif mode==15:
        print ""+url
        F(url)		
elif mode==16:
        print ""+url
        G(url)		
elif mode==17:
        print ""+url
        H(url)		
elif mode==18:
        print ""+url
        I(url)		
elif mode==19:
        print ""+url
        J(url)		
elif mode==20:
        print ""+url
        K(url)		
elif mode==21:
        print ""+url
        L(url)		
elif mode==22:
        print ""+url
        M(url)		
elif mode==23:
        print ""+url
        N(url)		
elif mode==24:
        print ""+url
        O(url)		
elif mode==25:
        print ""+url
        P(url)		
elif mode==26:
        print ""+url
        Q(url)		
elif mode==27:
        print ""+url
        R(url)		
elif mode==28:
        print ""+url
        S(url)
elif mode==29:
        print ""+url
        T(url)
elif mode==30:
        print ""+url
        U(url)
elif mode==31:
        print ""+url
        V(url)		
elif mode==32:
        print ""+url
        W(url)		
elif mode==33:
        print ""+url
        X(url)		
elif mode==34:
        print ""+url
        Y(url)		
elif mode==35:
        print ""+url
        Z(url)	

elif mode==40:
        print ""+url
        showEpp(url)			
elif mode==45 or url==RES:
        import urlresolver
        print ""+url
        urlresolver.display_settings()			



xbmcplugin.endOfDirectory(int(sys.argv[1]))



