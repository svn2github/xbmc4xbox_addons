import urllib,urllib2,re,cookielib,xbmcplugin,xbmcgui,xbmcaddon,socket,os,shutil,string,xbmc,stat,xbmcvfs
import base64
from t0mm0.common.net import Net as net
from t0mm0.common.addon import Addon
#XBOX-COMPAT-EXCLUSION from metahandler import metahandlers
from zipfile import ZipFile as zip
from BeautifulSoup import BeautifulSoup as soup
import urlresolver
#SET DIRECTORIES
local = xbmcaddon.Addon(id='plugin.video.videobull')
addon = Addon('plugin.video.videobull', sys.argv)
#XBOX-COMPAT-EXCLUSION grab = metahandlers.MetaData(None,preparezip = False)
fanart = "%s/skins/%s/fanart.jpg"%(local.getAddonInfo("path"),local.getSetting("Current Skin"))
xbmc_skin = xbmc.getSkinDir()
print "CURRENT XBMC SKIN: %s"%xbmc_skin
print "VERSION: %s"%local.getAddonInfo('version')
pluginhandle = int(sys.argv[1])








dbg = False # Set to false if you don't want debugging

#Common Cache
try:
  import StorageServer
except:
  import storageserverdummy as StorageServer
cache = StorageServer.StorageServer('plugin.video.videobull')

##### Queries ##########
total = addon.queries.get('total','')
play = addon.queries.get('play', '')
mode = addon.queries['mode']
level = addon.queries.get('level', '')
levels = addon.queries.get('levels', '')
video_type = addon.queries.get('video_type', '')
section = addon.queries.get('section', '')
url = addon.queries.get('url', '')
Title = addon.queries.get('Title', '')
ptitle = addon.queries.get('name','')
name = addon.queries.get('name', '')
imdb_id = addon.queries.get('imdb_id', '')
season = addon.queries.get('season', '')
episode = addon.queries.get('episode', '')
year = addon.queries.get('year', '')
thumb = addon.queries.get('thumb', '')
playingtitle = addon.queries.get('playingtitle', '')
print '---------------------------------------------------------------'
print '--- Mode: ' + str(mode)
print '--- Play: ' + str(play)
print '--- URL: ' + str(url)
print '--- Video Type: ' + str(video_type)
print '--- Section: ' + str(section)
print '--- Title: ' + str(Title)
print '--- Name: ' + str(name)
print '--- IMDB: ' + str(imdb_id)
print '--- Season: ' + str(season)
print '--- Episode: ' + str(episode)
print '--- Cover URL: ' + str(thumb)
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

VideoType_Movies = 'movie'
VideoType_TV = 'tvshow'
VideoType_Season = 'season'
VideoType_Episode = 'episode'


# def get_metadata(video_type, vidtitle, vidname='', year='', imdb='', season_list=None, season_num=0, episode_num=0):
    
    # if meta_setting:
        # # Get Meta settings
        # movie_covers = addon.get_setting('movie-covers')
        # tv_banners = addon.get_setting('tv-banners')
        # tv_posters = addon.get_setting('tv-posters')
        
        # movie_fanart = addon.get_setting('movie-fanart')
        # tv_fanart = addon.get_setting('tv-fanart')
            
        # metaget=metahandlers.MetaData()
    
        # if video_type in (VideoType_Movies, VideoType_TV):
            # meta = metaget.get_meta(video_type, vidtitle, year=year)
    
        # if video_type == VideoType_Season:
            # returnlist = True
            # if not season_list:
                # season_list = []
                # season_list.append(season_num)
                # returnlist = False
            # meta = metaget.get_seasons(vidtitle, imdb, season_list)
            # if not returnlist:
                # meta = meta[0]
    
        # if video_type == VideoType_Episode:
            # meta=metaget.get_episode_meta(vidname, imdb, season_num, episode_num)
        
        # # Check for and blank out covers if option disabled
        # if video_type==VideoType_Movies and movie_covers == 'false':
            # meta['cover_url'] = ''
        # elif video_type==VideoType_TV and tv_banners == 'false':
            # meta['cover_url'] = ''
    
        # # Check for banners vs posters setting    
        # if video_type == VideoType_TV and tv_banners == 'true' and tv_posters == 'false':
            # meta['cover_url'] = meta['banner_url']
        
        # # Check for and blank out fanart if option disabled
        # if video_type==VideoType_Movies and movie_fanart == 'false':
            # meta['backdrop_url'] = ''
        # elif video_type in (VideoType_TV, VideoType_Episode) and tv_fanart == 'false':
            # meta['backdrop_url'] = ''

    # else:
        # meta = {}
        # meta['title'] = vidname
        # meta['cover_url'] = ''
        # meta['imdb_id'] = imdb
        # meta['backdrop_url'] = ''
        # meta['year'] = year
        # meta['overlay'] = 0
        # if video_type in (VideoType_TV, VideoType_Episode):
            # meta['TVShowTitle'] = vidtitle

    # return meta

def CATEGORIES():
        addDir('Latest TV Show Feed',MainUrl,7,IconPath +'icons/icon.png')
        addDir('Search for Shows',MainUrl,8,IconPath +'icons/search.png')
        addDir('A-Z TV Shows',MainUrl +'tv-shows/',9,IconPath +'letters/AZ.png')
        addDir('[COLOR blue]Resolver Settings[/COLOR]','RES',45,IconPath +'icons/icon.png')
        xbmcplugin.endOfDirectory(pluginhandle)
def INDEX(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        
        response.close()
        match = re.compile('/*/?<item>.+?title>(.+?).?/title>.+?link>(.+?).?/link>.+?/item>', re.DOTALL).findall(link)
        for name,url in match:
                addDir(name,url,4,'')
def INDEX2(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('/*/?<li>.+?a href="(.+?)" rel="bookmark" title="(.+?)">.+?img src="(.+?)".+?/>.?/a>.+?/li>', re.DOTALL).findall(link)
        for url,name,thumb in match:
#		plugintools.add_item( action="play" , title=title , url=url )
         addDir(name,url,4,thumb)
           
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

def showEpp(url,name):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('<div id="contentarchive">.*?<a href="(.+?)" title="(.+?)">.+?</a>', re.DOTALL).findall(link)
    for url,name in match:
        name=name.replace('&#8211','').replace(';','-').replace('&#8217',"'").replace('&#038','&').replace('&#8230','ss')
        # artname=name.replace('Season','').replace('Episode','').replace('0','').replace('1','').replace('2','').replace('3','').replace('4','').replace('5','').replace('6','').replace('7','').replace('8','').replace('9','').replace('-\s.*?','')
        # cover = grab.get_meta('tvshow', artname, overlay=6)
        # covers= re.compile("cover_url.+?'(.+?)'").findall(str(cover))
        # for thumb in covers:
            # thumb = str(thumb)
        
        print 'ShowEpp Name---: '+name
        print 'ShowEpp (name)addonQueries.get---:'+addon.queries.get('Title', '')
        ptitle=name
        print 'PLAYING TITLE---: '+ptitle
        addDir(name,url,4,thumb)
        	
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
def A(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('title="[A](.*?)" href="(.*?)">.*?</a>').findall(link)
    for name,url in match:
        name='A'+name
        addDir(name,url,40,'')
def B(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('title="[B](.*?)" href="(.*?)">.*?</a>').findall(link)
    for name,url in match:
        name='B'+name
        addDir(name,url,40,'')		
def C(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('title="[C](.*?)" href="(.*?)">.*?</a>').findall(link)
    for name,url in match:
        name='C'+name
        addDir(name,url,40,'')   
def D(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('title="[D](.*?)" href="(.*?)">.*?</a>').findall(link)
    for name,url in match:
        name='D'+name
        addDir(name,url,40,'')		
def E(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('title="[E](.*?)" href="(.*?)">.*?</a>').findall(link)
    for name,url in match:
        name='E'+name
        addDir(name,url,40,'')
def F(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('title="[F](.*?)" href="(.*?)">.*?</a>').findall(link)
    for name,url in match:
        name='F'+name
        addDir(name,url,40,'')
def G(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('title="[G](.*?)" href="(.*?)">.*?</a>').findall(link)
    for name,url in match:
        name='G'+name
        addDir(name,url,40,'')		
def H(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('title="[H](.*?)" href="(.*?)">.*?</a>').findall(link)
    for name,url in match:
        name='H'+name
        addDir(name,url,40,'')		
def I(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('title="[I](.*?)" href="(.*?)">.*?</a>').findall(link)
    for name,url in match:
        name='I'+name
        addDir(name,url,40,'')		
def J(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('title="[J](.*?)" href="(.*?)">.*?</a>').findall(link)
    for name,url in match:
        name='J'+name
        addDir(name,url,40,'')		
def K(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('title="[K](.*?)" href="(.*?)">.*?</a>').findall(link)
    for name,url in match:
        name='K'+name
        addDir(name,url,40,'')		
def L(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('title="[L](.*?)" href="(.*?)">.*?</a>').findall(link)
    for name,url in match:
        name='L'+name
        addDir(name,url,40,'')		
def M(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('title="[M](.*?)" href="(.*?)">.*?</a>').findall(link)
    for name,url in match:
        name='M'+name
        addDir(name,url,40,'')		
def N(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('title="[N](.*?)" href="(.*?)">.*?</a>').findall(link)
    for name,url in match:
        name='N'+name
        addDir(name,url,40,'')		
def O(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('title="[O](.*?)" href="(.*?)">.*?</a>').findall(link)
    for name,url in match:
        name='O'+name
        addDir(name,url,40,'')		
def P(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('title="[P](.*?)" href="(.*?)">.*?</a>').findall(link)
    for name,url in match:
        name='P'+name
        addDir(name,url,40,'')		
def Q(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('title="[Q](.*?)" href="(.*?)">.*?</a>').findall(link)
    for name,url in match:
        name='Q'+name
        addDir(name,url,40,'')		
def R(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('title="[R](.*?)" href="(.*?)">.*?</a>').findall(link)
    for name,url in match:
        name='R'+name
        addDir(name,url,40,'')		
def S(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('title="[S](.*?)" href="(.*?)">.*?</a>').findall(link)
    for name,url in match:
        name='S'+name
        addDir(name,url,40,'')		
def T(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('title="[T](.*?)" href="(.*?)">.*?</a>').findall(link)
    for name,url in match:
        name='T'+name
        addDir(name,url,40,'')		
def U(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('title="[U](.*?)" href="(.*?)">.*?</a>').findall(link)
    for name,url in match:
        name='U'+name
        addDir(name,url,40,'')		
def V(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('title="[V](.*?)" href="(.*?)">.*?</a>').findall(link)
    for name,url in match:
        name='V'+name
        addDir(name,url,40,'')		
def W(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('title="[W](.*?)" href="(.*?)">.*?</a>').findall(link)
    for name,url in match:
        name='W'+name
        addDir(name,url,40,'')		
def X(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('title="[X](.*?)" href="(.*?)">.*?</a>').findall(link)
    for name,url in match:
        name='X'+name
        addDir(name,url,40,'')		
def Y(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('title="[Y](.*?)" href="(.*?)">.*?</a>').findall(link)
    for name,url in match:
        name='Y'+name
        addDir(name,url,40,'')		
def Z(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('title="[Z](.*?)" href="(.*?)">.*?</a>').findall(link)
    for name,url in match:
        name='Z'+name
        addDir(name,url,40,'')		
def TvSearch(url):
    search_entered =search()
    name=str(search_entered).replace('+','')
    url='http://videobull.com/?s=' + search_entered + '&x=-1121&y=-30'
    link = getUrl(url)
    match=re.compile('<div id="contentarchivetitle">\n.*?<a href="(.+?)" title="(.+?)">.+?</a>', re.DOTALL).findall(link)
    for url,name in match:
        name=name.replace('&#8211','').replace(';','-').replace('&#8217',"'").replace('&#038','&').replace('&#8230','ss')
        artname=name.replace('Season','').replace('Episode','').replace('0','').replace('1','').replace('2','').replace('3','').replace('4','').replace('5','').replace('6','').replace('7','').replace('8','').replace('9','')
#        cover = grab.get_meta('tvshow', artname, overlay=6)
        covers= re.compile("cover_url.+?'(.+?)'").findall(str(cover))
        for thumb in covers:
            thumb = str(thumb)
            addDir(name,url,40,thumb)
		
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
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:16.0) Gecko/20100101 Firefox/16.0')
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
                
def EPISODES(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('/*/?<li>.+?a href="(.+?)" rel="bookmark" title="(.+?)">.+?img src="(.+?)".+?/>.?/a>.+?/li>').findall(link)
        for url,name,thumb in match:
                if not thumb.find('http://')>0:
                        thumb='http://www.tvdash.com/'+thumb
                        addDir(name,'http://www.videobull.com/'+url,4,thumb)

def VIDEOLINKS(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('''<a id='.+?' href='.*?title=(.+?)' target='_blank' rel='nofollow'>(.+?)</a>''', re.DOTALL).findall(link)
        print match
        for url,name in match:     
         addDir(name,url,5,thumb)
         print 'PLAYING TITLE---: '+ptitle
            
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
                      
def PLAYLINKS(url):
        
        regexlink = url
        url = base64.b64decode(regexlink)
        hostUrl = url
        videoLink = urlresolver.resolve(hostUrl)      
        addLink(ptitle,'videoLink','')
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        playlist.add(videoLink)
        xbmc.Player().play(playlist)
    
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
        liz=xbmcgui.ListItem(label=ptitle, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
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
        VIDEOLINKS(url)

elif mode==5:
    print ""+url
    PLAYLINKS(url)
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
        A(url)
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
        showEpp(url,name)			

elif mode==45 or url==RES:
        print ""
        urlresolver.display_settings()		
xbmcplugin.endOfDirectory(int(sys.argv[1]))



