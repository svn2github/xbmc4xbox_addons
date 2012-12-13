import urllib, urllib2, re, sys, cookielib, os
import xbmc, xbmcgui, xbmcplugin, xbmcaddon, xbmcvfs
import simplejson as json
from xbmcgui import ListItem

# plugin constants
version = "0.0.1"
plugin = "Crackle2 - " + version


__settings__ = xbmcaddon.Addon(id='plugin.video.crackle2')
rootDir = __settings__.getAddonInfo('path')
if rootDir[-1] == ';':
    rootDir = rootDir[0:-1]
rootDir = xbmc.translatePath(rootDir)

programs_thumb = os.path.join(__settings__.getAddonInfo('path'), 'resources', 'media', 'programs.png')
topics_thumb = os.path.join(__settings__.getAddonInfo('path'), 'resources', 'media', 'topics.png')
search_thumb = os.path.join(__settings__.getAddonInfo('path'), 'resources', 'media', 'search.png')
next_thumb = os.path.join(__settings__.getAddonInfo('path'), 'resources', 'media', 'next.png')

pluginhandle = int(sys.argv[1])

########################################################
## URLs
########################################################
API_URL = 'http://api.crackle.com/Service.svc/'
MOVIES = '/movies/all/US/50?format=json'
SHOWS = '/shows/all/US/50?format=json'
FEATURED = 'featured'
POPULAR = 'popular'
RECENT = 'recent'
BROWSE = 'browse/%s/full/all/alpha/US?format=json'
BROWSE2 = 'browse/%s/all/all/alpha/US?format=json'
SEARCHURL = 'search/all/%s/US?format=json'
HOMESLIDE = 'slideShow/home/us?format=json'
ORIGINALS = 'originals'
COLLECTIONS = 'collections'
CHURL = 'channel/%s/folders/US?format=json'
BASE_MEDIA_URL = 'http://media-us-am.crackle.com/%s_480p.mp4'
DETAILS_URL = 'http://api.crackle.com/Service.svc/details/media/%s/US?format=json'

########################################################
## Modes
########################################################
M_DO_NOTHING = 0
M_MOVIES = 10   # FEATURED
M_MOVIES_POPULAR = 11
M_MOVIES_RECENT = 12
M_SHOWS = 20    # FEATURED
M_SHOWS_POPULAR = 21
M_SHOWS_RECENT = 22
M_BROWSE = 30    # MOVIES
M_BROWSE_SHOWS = 31
M_BROWSE_ORIGINALS = 32
M_BROWSE_COLLECTIONS = 33
M_Search = 4
M_GET_VIDEO_LINKS = 5
M_PLAY = 6
M_SINGLE_VIDEO = 50

##################
## Class for items
##################
class MediaItem:
    def __init__(self):
        self.ListItem = ListItem()
        self.Image = ''
        self.Url = ''
        self.Isfolder = False
        self.Mode = ''
        
## Get URL
def getURL( url ):
    print plugin + ' getURL :: url = ' + url
    cj = cookielib.LWPCookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    opener.addheaders = [('User-Agent', 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2;)')]
    usock=opener.open(url)
    response=usock.read()
    usock.close()
    return response

def TestURL( url ):
    print plugin + ' TestURL :: url = ' + url
    cj = cookielib.LWPCookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    opener.addheaders = [('User-Agent', 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2;)')]
    try:
        usock=opener.open(url)    
        usock.close()
        return True
    except:
        return False

# Remove HTML codes
def cleanHtml( dirty ):
    clean = re.sub('&quot;', '\"', dirty)
    clean = re.sub('&#039;', '\'', clean)
    clean = re.sub('&#215;', 'x', clean)
    clean = re.sub('&#038;', '&', clean)
    clean = re.sub('&#8216;', '\'', clean)
    clean = re.sub('&#8217;', '\'', clean)
    clean = re.sub('&#8211;', '-', clean)
    clean = re.sub('&#8220;', '\"', clean)
    clean = re.sub('&#8221;', '\"', clean)
    clean = re.sub('&#8212;', '-', clean)
    clean = re.sub('&amp;', '&', clean)
    clean = re.sub("`", '', clean)
    clean = re.sub('<em>', '[I]', clean)
    clean = re.sub('</em>', '[/I]', clean)
    return clean

########################################################
## Mode = None
## Build the main directory
########################################################
def BuildMainDirectory():
    # set content type so library shows more views and info
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    MediaItems = []
    # Top Title
    Mediaitem = MediaItem()
    Url = ''
    Mode = M_DO_NOTHING
    Title = __settings__.getLocalizedString(30011)
    Thumb = ''
    Mediaitem.Url = sys.argv[0] + "?url=" + urllib.quote_plus(Url) + "&mode=" + str(Mode) + "&name=" + urllib.quote_plus(Title)
    Mediaitem.ListItem.setThumbnailImage(Thumb)
    Mediaitem.ListItem.setLabel(Title)
    MediaItems.append(Mediaitem)
    # Get featured homepage contents
    URL = API_URL + HOMESLIDE
    data = getURL(URL)
    #data = load_local_json('featured.json')
    items = json.loads(data)
    #print items
    slideList = items['slideList']
    slideList = [slide for slide in slideList]
    #print ('slidelist length ') + str(len(slideList))
    for slide in slideList:
        #print 'Debug Msg 1'
        Title = '* ' + slide['title']
        Url = str(slide['appDataID'])
        #print Url
        Image = slide['MobileImage']
        Genre = slide['ParentChannelName']
        if not Genre:
            Genre = ''
        Plot = slide['slideDescription']
        Mpaa = slide['Rating']
        if not Mpaa:
            Mpaa = 'None'
        Mediaitem = MediaItem()
        NextScreen = slide['appNextScreenType']
        if NextScreen == 'VideoDetail':
            Mediaitem.Mode = M_SINGLE_VIDEO
            Url = DETAILS_URL % Url
        else:
            Mediaitem.Mode = M_GET_VIDEO_LINKS
            Url = API_URL + CHURL % Url
        #print 'Debug Msg 2'
        Mediaitem.Image = Image
        Title = Title.encode('utf-8')
        Mediaitem.Url = sys.argv[0] + "?url=" + urllib.quote_plus(Url) + "&mode=" + str(Mediaitem.Mode) + "&name=" + urllib.quote_plus(Title)
        Plot = Plot.encode('utf-8')
        #print 'Debug Msg 3'
        Mediaitem.ListItem.setInfo('video', { 'Title': Title, 'Plot': Plot, 'Mpaa': Mpaa,
                                             'Genre': Genre})
        Mediaitem.ListItem.setThumbnailImage(Mediaitem.Image)
        Mediaitem.ListItem.setLabel(Title)
        Mediaitem.Isfolder = True
        #print 'Debug Msg 4'
        MediaItems.append(Mediaitem)
               
    # Static Links for Browsing and Search
    main = [
        (__settings__.getLocalizedString(30012), topics_thumb, str(M_MOVIES)),
        (__settings__.getLocalizedString(30013), topics_thumb, str(M_SHOWS)),
        (__settings__.getLocalizedString(30010), programs_thumb, str(M_BROWSE)),
        (__settings__.getLocalizedString(30015), search_thumb, str(M_Search))
        ]
    for name, thumbnailImage, mode in main:
        Mediaitem = MediaItem()
        Url = ''
        Mode = mode
        Title = name
        Thumb = thumbnailImage
        Mediaitem.Url = sys.argv[0] + "?url=" + urllib.quote_plus(Url) + "&mode=" + str(Mode) + "&name=" + urllib.quote_plus(Title)
        Mediaitem.ListItem.setThumbnailImage(Thumb)
        Mediaitem.ListItem.setLabel(Title)
        Mediaitem.Isfolder = True
        MediaItems.append(Mediaitem)
        
    addDir(MediaItems)
    # End of Directory
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    ## Set Default View Mode. This might break with different skins. But who cares?
    SetViewMode()
    
###########################################################
## Mode == M_Movies
## Movies Directory
###########################################################
def MoviesDirectory(mode):
    # set content type so library shows more views and info
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    MediaItems = []
    if mode == M_MOVIES:
        menuTitle = __settings__.getLocalizedString(30011)
        #fname = 'moviesf.json'
        btm = [
        (__settings__.getLocalizedString(30014), topics_thumb, str(M_MOVIES_POPULAR)),
        (__settings__.getLocalizedString(30016), topics_thumb, str(M_MOVIES_RECENT))
        ]
        URL = API_URL + FEATURED + MOVIES
    elif mode == M_MOVIES_POPULAR:
        menuTitle = __settings__.getLocalizedString(30014)
        #fname = 'moviesp.json'
        btm = [
        (__settings__.getLocalizedString(30011), topics_thumb, str(M_MOVIES)),
        (__settings__.getLocalizedString(30016), topics_thumb, str(M_MOVIES_RECENT))
        ]
        URL = API_URL + POPULAR + MOVIES
    elif mode == M_MOVIES_RECENT:
        menuTitle = __settings__.getLocalizedString(30016)
        #fname = 'moviesr.json'
        btm = [
        (__settings__.getLocalizedString(30011), topics_thumb, str(M_MOVIES)),
        (__settings__.getLocalizedString(30014), topics_thumb, str(M_MOVIES_POPULAR))
        ]
        URL = API_URL + RECENT + MOVIES
    menuMode = M_DO_NOTHING
    # Top Title
    Mediaitem = MediaItem()
    Url = ''
    Mode = menuMode
    Title = menuTitle
    Thumb = ''
    Mediaitem.Url = sys.argv[0] + "?url=" + urllib.quote_plus(Url) + "&mode=" + str(Mode) + "&name=" + urllib.quote_plus(Title)
    Mediaitem.ListItem.setThumbnailImage(Thumb)
    Mediaitem.ListItem.setLabel(Title)
    MediaItems.append(Mediaitem)
        
    # Get featured movies contents
    data = getURL(URL)
    #data = load_local_json(fname)
    mjson = json.loads(data)
    items = mjson['Items']
    items = [item for item in items]
    for item in items:
        Title = '* ' + item['Title']
        Url = str(item['ID'])
        Url = API_URL + CHURL % Url
        Image = item['ImageUrl2']
        Genre = item['Genre']
        Plot = item['Description']
        Mpaa = item['Rating']
        Mediaitem = MediaItem()
        Mediaitem.Mode = M_GET_VIDEO_LINKS
        Mediaitem.Image = Image
        Mediaitem.Url = sys.argv[0] + "?url=" + urllib.quote_plus(Url) + "&mode=" + str(Mediaitem.Mode) + "&name=" + urllib.quote_plus(Title)
        Mediaitem.ListItem.setInfo('video', { 'Title': Title, 'Plot': Plot, 'Mpaa': Mpaa,
                                             'Genre': Genre})
        Mediaitem.ListItem.setThumbnailImage(Mediaitem.Image)
        Mediaitem.ListItem.setLabel(Title)
        Mediaitem.Isfolder = True
        MediaItems.append(Mediaitem)
                
    for name, thumbnailImage, mode in btm:
        Mediaitem = MediaItem()
        Url = ''
        Mode = mode
        Title = name
        Thumb = thumbnailImage
        Mediaitem.Url = sys.argv[0] + "?url=" + urllib.quote_plus(Url) + "&mode=" + str(Mode) + "&name=" + urllib.quote_plus(Title)
        Mediaitem.ListItem.setThumbnailImage(Thumb)
        Mediaitem.ListItem.setLabel(Title)
        Mediaitem.Isfolder = True
        MediaItems.append(Mediaitem)
        
    # Static Links for Browsing and Search
    main = [
        (__settings__.getLocalizedString(30013), topics_thumb, str(M_SHOWS)),
        (__settings__.getLocalizedString(30010), programs_thumb, str(M_BROWSE)),
        (__settings__.getLocalizedString(30015), search_thumb, str(M_Search))
        ]
    for name, thumbnailImage, mode in main:
        Mediaitem = MediaItem()
        Url = ''
        Mode = mode
        Title = name
        Thumb = thumbnailImage
        Mediaitem.Url = sys.argv[0] + "?url=" + urllib.quote_plus(Url) + "&mode=" + str(Mode) + "&name=" + urllib.quote_plus(Title)
        Mediaitem.ListItem.setThumbnailImage(Thumb)
        Mediaitem.ListItem.setLabel(Title)
        Mediaitem.Isfolder = True
        MediaItems.append(Mediaitem)

    addDir(MediaItems)
    # End of Directory
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    ## Set Default View Mode. This might break with different skins. But who cares?
    SetViewMode()
    
###########################################################
## Mode == M_SHOWS
## SHOWS DIRECTORY
###########################################################   
def ShowsDirectory(mode):
    # set content type so library shows more views and info
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    MediaItems = []
    if mode == M_SHOWS:
        menuTitle = __settings__.getLocalizedString(30011)
        #fname = 'showsf.json'
        btm = [
        (__settings__.getLocalizedString(30014), topics_thumb, str(M_SHOWS_POPULAR)),
        (__settings__.getLocalizedString(30016), topics_thumb, str(M_SHOWS_RECENT))
        ]
        URL = API_URL + FEATURED + SHOWS
    elif mode == M_SHOWS_POPULAR:
        menuTitle = __settings__.getLocalizedString(30014)
        #fname = 'showsp.json'
        btm = [
        (__settings__.getLocalizedString(30011), topics_thumb, str(M_SHOWS)),
        (__settings__.getLocalizedString(30016), topics_thumb, str(M_SHOWS_RECENT))
        ]
        URL = API_URL + POPULAR + SHOWS
    elif mode == M_SHOWS_RECENT:
        menuTitle = __settings__.getLocalizedString(30016)
        #fname = 'showsr.json'
        btm = [
        (__settings__.getLocalizedString(30011), topics_thumb, str(M_SHOWS)),
        (__settings__.getLocalizedString(30014), topics_thumb, str(M_SHOWS_POPULAR))
        ]
        URL = API_URL + RECENT + SHOWS
    menuMode = M_DO_NOTHING
    # Top Title
    Mediaitem = MediaItem()
    Url = ''
    Mode = menuMode
    Title = menuTitle
    Thumb = ''
    Mediaitem.Url = sys.argv[0] + "?url=" + urllib.quote_plus(Url) + "&mode=" + str(Mode) + "&name=" + urllib.quote_plus(Title)
    Mediaitem.ListItem.setThumbnailImage(Thumb)
    Mediaitem.ListItem.setLabel(Title)
    MediaItems.append(Mediaitem)
        
    # Get featured movies contents
    data = getURL(URL)
    #data = load_local_json(fname)
    mjson = json.loads(data)
    items = mjson['Items']
    items = [item for item in items]
    for item in items:
        Title = '* ' + item['Title']
        Url = str(item['ID'])
        Url = API_URL + CHURL % Url
        Image = item['ImageUrl10']
        Genre = item['Genre']
        Plot = item['Description']
        Mpaa = item['Rating']
        Mediaitem = MediaItem()
        Mediaitem.Mode = M_GET_VIDEO_LINKS
        Mediaitem.Image = Image
        Mediaitem.Url = sys.argv[0] + "?url=" + urllib.quote_plus(Url) + "&mode=" + str(Mediaitem.Mode) + "&name=" + urllib.quote_plus(Title)
        Mediaitem.ListItem.setInfo('video', { 'Title': Title, 'Plot': Plot, 'Mpaa': Mpaa,
                                             'Genre': Genre})
        Mediaitem.ListItem.setThumbnailImage(Mediaitem.Image)
        Mediaitem.ListItem.setLabel(Title)
        Mediaitem.Isfolder = True
        MediaItems.append(Mediaitem)
        
    for name, thumbnailImage, mode in btm:
        Mediaitem = MediaItem()
        Url = ''
        Mode = mode
        Title = name
        Thumb = thumbnailImage
        Mediaitem.Url = sys.argv[0] + "?url=" + urllib.quote_plus(Url) + "&mode=" + str(Mode) + "&name=" + urllib.quote_plus(Title)
        Mediaitem.ListItem.setThumbnailImage(Thumb)
        Mediaitem.ListItem.setLabel(Title)
        Mediaitem.Isfolder = True
        MediaItems.append(Mediaitem)
        
    # Static Links for Browsing and Search
    main = [
        (__settings__.getLocalizedString(30012), topics_thumb, str(M_MOVIES)),
        (__settings__.getLocalizedString(30010), programs_thumb, str(M_BROWSE)),
        (__settings__.getLocalizedString(30015), search_thumb, str(M_Search))
        ]
    for name, thumbnailImage, mode in main:
        Mediaitem = MediaItem()
        Url = ''
        Mode = mode
        Title = name
        Thumb = thumbnailImage
        Mediaitem.Url = sys.argv[0] + "?url=" + urllib.quote_plus(Url) + "&mode=" + str(Mode) + "&name=" + urllib.quote_plus(Title)
        Mediaitem.ListItem.setThumbnailImage(Thumb)
        Mediaitem.ListItem.setLabel(Title)
        Mediaitem.Isfolder = True
        MediaItems.append(Mediaitem)

    addDir(MediaItems)

    # End of Directory
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    ## Set Default View Mode. This might break with different skins. But who cares?
    SetViewMode()
    
###########################################################
## Mode == M_BROWSE
## BROWSE DIRECTORY
###########################################################   
def BrowseDirectory(mode):
    # set content type so library shows more views and info
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    MediaItems = []
    if mode == M_BROWSE:
        menuTitle = __settings__.getLocalizedString(30012)
        #fname = 'browsem.json'
        btm = [
        (__settings__.getLocalizedString(30017), topics_thumb, str(M_BROWSE_SHOWS)),
        (__settings__.getLocalizedString(30018), topics_thumb, str(M_BROWSE_ORIGINALS)),
        (__settings__.getLocalizedString(30019), topics_thumb, str(M_BROWSE_COLLECTIONS))
        ]
        URL = API_URL + BROWSE % 'movies'
    elif mode == M_BROWSE_SHOWS:
        menuTitle = __settings__.getLocalizedString(30017)
        #fname = 'browset.json'
        btm = [
        (__settings__.getLocalizedString(30012), topics_thumb, str(M_BROWSE)),
        (__settings__.getLocalizedString(30018), topics_thumb, str(M_BROWSE_ORIGINALS)),
        (__settings__.getLocalizedString(30019), topics_thumb, str(M_BROWSE_COLLECTIONS))
        ]
        URL = API_URL + BROWSE % 'television'
    elif mode == M_BROWSE_ORIGINALS:
        menuTitle = __settings__.getLocalizedString(30018)
        #fname = 'browseo.json'
        btm = [
        (__settings__.getLocalizedString(30012), topics_thumb, str(M_BROWSE)),
        (__settings__.getLocalizedString(30017), topics_thumb, str(M_BROWSE_SHOWS)),
        (__settings__.getLocalizedString(30019), topics_thumb, str(M_BROWSE_COLLECTIONS))
        ]
        URL = API_URL + BROWSE2 % 'originals'
    elif mode == M_BROWSE_COLLECTIONS:
        menuTitle = __settings__.getLocalizedString(30019)
        #fname = 'browsec.json'
        btm = [
        (__settings__.getLocalizedString(30012), topics_thumb, str(M_BROWSE)),
        (__settings__.getLocalizedString(30017), topics_thumb, str(M_BROWSE_SHOWS)),
        (__settings__.getLocalizedString(30018), topics_thumb, str(M_BROWSE_ORIGINALS))
        ]
        URL = API_URL + BROWSE2 % 'collections'
    menuMode = M_DO_NOTHING
    # Top Title
    Mediaitem = MediaItem()
    Url = ''
    Mode = menuMode
    Title = menuTitle
    Thumb = ''
    Mediaitem.Url = sys.argv[0] + "?url=" + urllib.quote_plus(Url) + "&mode=" + str(Mode) + "&name=" + urllib.quote_plus(Title)
    Mediaitem.ListItem.setThumbnailImage(Thumb)
    Mediaitem.ListItem.setLabel(Title)
    MediaItems.append(Mediaitem)
        
    # Get featured movies contents
    data = getURL(URL)
    #print data
    #data = load_local_json(fname)
    mjson = json.loads(data)
    items = mjson['Entries']
    items = [item for item in items]
    for item in items:
        #print item
        Title = '* ' + item['Name']
        #print Title
        Url = str(item['ID'])
        Url = API_URL + CHURL % Url
        #print Url
        Image = item['ChannelArtTileLarge']
        Genre = item['Genre']
        Plot = item['Description']
        Year = item['ReleaseYear']
        Mpaa = item['Rating']
        Mediaitem = MediaItem()
        Mediaitem.Mode = M_GET_VIDEO_LINKS
        Mediaitem.Image = Image
        Mediaitem.Url = sys.argv[0] + "?url=" + urllib.quote_plus(Url) + "&mode=" + str(Mediaitem.Mode) + "&name=" + urllib.quote_plus(Title)
        Mediaitem.ListItem.setInfo('video', { 'Title': Title, 'Plot': Plot, 'Mpaa': Mpaa,
                                             'Genre': Genre, 'Year': Year})
        Mediaitem.ListItem.setThumbnailImage(Mediaitem.Image)
        Mediaitem.ListItem.setLabel(Title)
        Mediaitem.Isfolder = True
        MediaItems.append(Mediaitem)
        
    for name, thumbnailImage, mode in btm:
        Mediaitem = MediaItem()
        Url = ''
        Mode = mode
        Title = name
        Thumb = thumbnailImage
        Mediaitem.Url = sys.argv[0] + "?url=" + urllib.quote_plus(Url) + "&mode=" + str(Mode) + "&name=" + urllib.quote_plus(Title)
        Mediaitem.ListItem.setThumbnailImage(Thumb)
        Mediaitem.ListItem.setLabel(Title)
        Mediaitem.Isfolder = True
        MediaItems.append(Mediaitem)
        
    # Static Links for Browsing and Search
    main = [
        (__settings__.getLocalizedString(30012), topics_thumb, str(M_MOVIES)),
        (__settings__.getLocalizedString(30013), topics_thumb, str(M_SHOWS)),
        (__settings__.getLocalizedString(30015), search_thumb, str(M_Search))
        ]
    for name, thumbnailImage, mode in main:
        Mediaitem = MediaItem()
        Url = ''
        Mode = mode
        Title = name
        Thumb = thumbnailImage
        Mediaitem.Url = sys.argv[0] + "?url=" + urllib.quote_plus(Url) + "&mode=" + str(Mode) + "&name=" + urllib.quote_plus(Title)
        Mediaitem.ListItem.setThumbnailImage(Thumb)
        Mediaitem.ListItem.setLabel(Title)
        Mediaitem.Isfolder = True
        MediaItems.append(Mediaitem)

    addDir(MediaItems)

    # End of Directory
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    ## Set Default View Mode. This might break with different skins. But who cares?
    SetViewMode()
    
###########################################################
## Mode == M_GET_VIDEO_LINKS
## Try to get a list of playable items and play it.
###########################################################
def Playlist(URL):
    # set content type so library shows more views and info
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    MediaItems = []
    #URL = API_URL + CHURL % url
    data = getURL(URL)
    #data = load_local_json('chdet3.json')
    mjson = json.loads(data)
    Count = mjson['Count']
    if Count < 1:
        dialog = xbmcgui.Dialog()
        dialog.ok('No Item', 'The selected item does not exist any more.')
        return
    FolderList = mjson['FolderList']
    FolderList = [folder for folder in FolderList]
    folder = FolderList[0]
    PlaylistList = folder['PlaylistList']
    PlaylistList = [playlist for playlist in PlaylistList]
    playlist = PlaylistList[0]
    MediaList = playlist['MediaList']
    MediaList = [media for media in MediaList]
    count = 0
    for item in MediaList:
        Title = item['Title']
        HackUrl = item['Thumbnail_Wide']
        #print HackUrl
        Path = re.compile('http://.+?\/(.+?)_.+?').findall(HackUrl)[0]
        Url = BASE_MEDIA_URL % Path
        print Url
        Image = item['Thumbnail_Large208x156']
        Genre = item['Genre']
        Plot = item['Description']
        Mpaa = item['Rating']
        Duration = item['Duration']
        Mediaitem = MediaItem()
        Mediaitem.Mode = M_PLAY
        Mediaitem.Image = Image
        Mediaitem.Url = sys.argv[0] + "?url=" + urllib.quote_plus(Url) + "&mode=" + str(Mediaitem.Mode) + "&name=" + urllib.quote_plus(Title)
        Mediaitem.ListItem.setInfo('video', { 'Title': Title, 'Plot': Plot, 'Mpaa': Mpaa,
                                             'Genre': Genre, 'Duration': Duration})
        Mediaitem.ListItem.setThumbnailImage(Mediaitem.Image)
        Mediaitem.ListItem.setLabel(Title)
        #Mediaitem.ListItem.setProperty('IsPlayable', 'true')
        MediaItems.append(Mediaitem)
        count += 1
    
    if count < 1:
        return
    addDir(MediaItems)
    # End of Directory
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    ## Set Default View Mode. This might break with different skins. But who cares?
    SetViewMode()
    
    if count == 1:
        Play(Url, Mediaitem.ListItem)
        
def VideoDetails(URL):
    ###########################################################
    ## Mode == M_SINGLE_VIDEO
    ## Try to get a playable item and play it.
    ###########################################################
    # set content type so library shows more views and info
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    MediaItems = []
    data = getURL(URL)
    #data = load_local_json('chdet3.json')
    mjson = json.loads(data)
    Title = mjson['Title']
    HackUrl = mjson['Thumbnail_Wide']
    #print HackUrl
    Path = re.compile('http://.+?\/(.+?)_.+?').findall(HackUrl)[0]
    Url = BASE_MEDIA_URL % Path
    #print Url
    Image = mjson['Thumbnail_Large208x156']
    Genre = mjson['Genre']
    Plot = mjson['Description']
    Mpaa = mjson['Rating']
    Duration = mjson['Duration']
    Mediaitem = MediaItem()
    Mediaitem.Mode = M_PLAY
    Mediaitem.Image = Image
    Mediaitem.Url = sys.argv[0] + "?url=" + urllib.quote_plus(Url) + "&mode=" + str(Mediaitem.Mode) + "&name=" + urllib.quote_plus(Title)
    Mediaitem.ListItem.setInfo('video', { 'Title': Title, 'Plot': Plot, 'Mpaa': Mpaa,
                                             'Genre': Genre, 'Duration': Duration})
    Mediaitem.ListItem.setThumbnailImage(Mediaitem.Image)
    Mediaitem.ListItem.setLabel(Title)
    #Mediaitem.ListItem.setProperty('IsPlayable', 'true')
    MediaItems.append(Mediaitem)
    #addDir(Title, Url, M_PLAY, Image, Genre, '', Plot)
    addDir(MediaItems)
    # End of Directory
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    ## Set Default View Mode. This might break with different skins. But who cares?
    SetViewMode()
    
    Play(Url, Mediaitem.ListItem)


def Play(url, litem=False):
    if url is not None and url != '':
        #try:
            #url2 = url.replace('480', '360')
            if not TestURL(url):
                url = url.replace('480', '360')
            playList = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
            playList.clear()
            if litem:
                playList.add(url, litem)
                #playList.add(url2, litem)
            else:
                playList.add(url)
                #playList.add(url2)
            xbmcPlayer = xbmc.Player()
            xbmcPlayer.play(playList)
            playList.clear()
            #vid = xbmcgui.ListItem(path=url)
            #xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play(url, vid)
            #xbmc.executebuiltin("xbmc.PlayMedia("+url+")")
        #except:
        #    print 'Exception while trying to play'

# Set View Mode selected in the setting
def SetViewMode():
    try:
        # if (xbmc.getSkinDir() == "skin.confluence"):
        if __settings__.getSetting('view_mode') == "1": # List
            xbmc.executebuiltin('Container.SetViewMode(502)')
        if __settings__.getSetting('view_mode') == "2": # Big List
            xbmc.executebuiltin('Container.SetViewMode(51)')
        if __settings__.getSetting('view_mode') == "3": # Thumbnails
            xbmc.executebuiltin('Container.SetViewMode(500)')
        if __settings__.getSetting('view_mode') == "4": # Poster Wrap
            xbmc.executebuiltin('Container.SetViewMode(501)')
        if __settings__.getSetting('view_mode') == "5": # Fanart
            xbmc.executebuiltin('Container.SetViewMode(508)')
        if __settings__.getSetting('view_mode') == "6":  # Media info
            xbmc.executebuiltin('Container.SetViewMode(504)')
        if __settings__.getSetting('view_mode') == "7": # Media info 2
            xbmc.executebuiltin('Container.SetViewMode(503)')
            
    except:
        print "SetViewMode Failed: " + __settings__.getSetting('view_mode')
        print "Skin: " + xbmc.getSkinDir()

# Search documentaries
def SEARCH(url):
        # set content type so library shows more views and info
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        MediaItems = []
    
        if url is None or url == '':
            keyb = xbmc.Keyboard('', 'Search Crackle')
            keyb.doModal()
            if (keyb.isConfirmed() == False):
                return
            search = keyb.getText()
            if search is None or search == '':
                return
            search = search.replace(" ", "+")
            encSrc = urllib.quote(search)
            url = API_URL + SEARCHURL % encSrc
        
        data = getURL(url)    
        #data = load_local_json('search2.json')
        mjson = json.loads(data)
        count = mjson['Count']
        if count < 1:
            return
        items = mjson['Items']
        items = [item for item in items]
        for item in items:
            Title = item['Title']
            Url = item['ID']
            Image = item['ImageUrl2']
            Genre = item['Genre']
            Plot = item['Description']
            Mpaa = item['Rating']
            Mediaitem = MediaItem()
            Mediaitem.Mode = M_GET_VIDEO_LINKS
            Mediaitem.Image = Image
            Mediaitem.Url = sys.argv[0] + "?url=" + urllib.quote_plus(Url) + "&mode=" + str(Mediaitem.Mode) + "&name=" + urllib.quote_plus(Title)
            Mediaitem.ListItem.setInfo('video', { 'Title': Title, 'Plot': Plot, 'Mpaa': Mpaa,
                                             'Genre': Genre})
            Mediaitem.ListItem.setThumbnailImage(Mediaitem.Image)
            Mediaitem.ListItem.setLabel(Title)
            Mediaitem.Isfolder = True
            MediaItems.append(Mediaitem)
                    
        addDir(MediaItems)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        SetViewMode()

## Get Parameters
def get_params():
        param = []
        paramstring = sys.argv[2]
        if len(paramstring) >= 2:
                params = sys.argv[2]
                cleanedparams = params.replace('?', '')
                if (params[len(params) - 1] == '/'):
                        params = params[0:len(params) - 2]
                pairsofparams = cleanedparams.split('&')
                param = {}
                for i in range(len(pairsofparams)):
                        splitparams = {}
                        splitparams = pairsofparams[i].split('=')
                        if (len(splitparams)) == 2:
                                param[splitparams[0]] = splitparams[1]
        return param

def addDir(Listitems):
    if Listitems is None:
        return
    Items = []
    for Listitem in Listitems:
        Item = Listitem.Url, Listitem.ListItem, Listitem.Isfolder
        Items.append(Item)
    handle = pluginhandle
    xbmcplugin.addDirectoryItems(handle, Items)
                    
params = get_params()
url = None
name = None
mode = None
titles = None
try:
        url = urllib.unquote_plus(params["url"])
except:
        pass
try:
        name = urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode = int(params["mode"])
except:
        pass
try:
        titles = urllib.unquote_plus(params["titles"])
except:
        pass

xbmc.log( "Mode: " + str(mode) )
#print "URL: " + str(url)
#print "Name: " + str(name)
#print "Title: " + str(titles)

if mode == None: #or url == None or len(url) < 1:
        #print "Top Directory"
        BuildMainDirectory()
elif mode == M_DO_NOTHING:
    print 'Doing Nothing'
elif mode == M_Search:
        #print "SEARCH  :" + url
        SEARCH(url)
elif mode == M_MOVIES or mode == M_MOVIES_POPULAR or mode == M_MOVIES_RECENT:
    MoviesDirectory(mode)
elif mode == M_SHOWS or mode == M_SHOWS_POPULAR or mode == M_SHOWS_RECENT:
    ShowsDirectory(mode)
elif mode == M_BROWSE or mode == M_BROWSE_SHOWS or mode == M_BROWSE_ORIGINALS or mode == M_BROWSE_COLLECTIONS:
    BrowseDirectory(mode)
elif mode == M_GET_VIDEO_LINKS:
    Playlist(url)
elif mode == M_SINGLE_VIDEO:
    VideoDetails(url)    
elif mode == M_PLAY:
    Play(url)
