import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os,time
import simplejson as json
import datetime
import time
icon = xbmc.translatePath(os.path.join('special://home/plugins/music/XBMCHUB Music', 'icon1.png'))
icon2='http://xbmc-hub-repo.googlecode.com/svn/addons/plugin.audio.xbmchubmusic/icon.png'
allmusic='http://www.allmusic.com'
fanart = xbmc.translatePath(os.path.join('special://home/plugins/music/XBMCHUB Music', 'fanart.jpg'))
ADDON = xbmcaddon.Addon(id='plugin.audio.xbmchubmusic')
musicdownloads=ADDON.getSetting('download_path')
datapath = xbmc.translatePath(ADDON.getAddonInfo('profile'))
if ADDON.getSetting('visitor_ga')=='':
    from random import randint
    ADDON.setSetting('visitor_ga',str(randint(0, 0x7fffffff)))
favorites = os.path.join(datapath, 'favorites')
if os.path.exists(favorites)==True:
    FAV = open(favorites).read()
    
VERSION = "1.8e"
PATH = "XBMC_MUSIC"            
UATRACK="UA-35537758-1"


    
def CATEGORIES():
        addDir('Artist Search','url',1,icon,'Search Your Favourite Artist','','')
        addDir('Album Search','url',2,icon,'Search Your Favourite Album','','')
        addDir('Song Search','url',3,icon,'Search Your Favourite Song','','')
        if os.path.exists(favorites)==True:
            addDir('Favorites','url',7,icon,'','','')
        addDir('UK Charts','http://www.officialcharts.com/albums-chart/',17,icon,'','','')
        addDir('BillBoard Album Charts','http://www1.billboard.com/#/charts',8,icon,'','','')
        addDir('What Mood Are You In','http://www.allmusic.com/moods',11,icon,'','','')
        addDir('Genres','http://www.allmusic.com/genres',13,icon,'','','')
        addDir('Themes','http://www.allmusic.com/themes',14,icon,'','','')
        setView('movies', 'default') 
        
def UK_CHARTS(name,url):
        addDir('UK Top 40 Singles','http://www.bigtop40.com/chart/',15,'http://xbmc-hub-repo.googlecode.com/svn/addons/plugin.audio.xbmchubmusic/icon.png','','','')
        addDir("Number Ones",'url',19,'http://xbmc-hub-repo.googlecode.com/svn/addons/plugin.audio.xbmchubmusic/icon.png','','','')
        link=OPEN_URL(url)
        link=link.split('singles-chart/">Singles Chart Top 100')[1]
        link=link.split('@OfficialCharts')[0]
        match = re.compile('href="(.+?)">(.+?)</a>').findall(link)
        for url,name in match:
            iconimage=icon
            addDir(name,url,16,iconimage,'','','')    
        setView('movies', 'default') 
        
def BILLBOARD_MAIN_LIST(url):
        addDir('BillBoard 200','http://www1.billboard.com/charts/billboard-200',9,icon,'','','')
        addDir('Country Albums','http://www1.billboard.com/charts/country-albums',9,icon,'','','')
        addDir('HeatSeeker Albums','http://www1.billboard.com/charts/heatseekers-albums',9,icon,'','','')
        addDir('Independent Albums','http://www1.billboard.com/charts/independent-albums',9,icon,'','','')
        addDir('Catalogue Albums','http://www1.billboard.com/charts/catalog-albums',9,icon,'','','')
        addDir('Folk Albums','http://www1.billboard.com/charts/folk-albums',9,icon,'','','')
        addDir('Digital Albums','http://www1.billboard.com/charts/digital-albums',9,icon,'','','')
        setView('movies', 'default') 
        
def BILLBOARD_ALBUM_LISTS(name,url):
        GA("None",name)
        link=OPEN_URL(url)
        match = re.compile('"title" : "(.+?)"\r\n.+?"artist" : "(.+?)"\r\n.+?image" : "(.+?)"\r\n.+?"entityId" : ".+?"\r\n.+?"entityUrl" : "(.+?)"').findall(link)
        for name, artist, iconimage, url in match:
            artist=artist.replace('&','And')
            url='http://www1.billboard.com'+url+'#'+url
            if re.search('.gif',iconimage):
                iconimage=icon
            addDir(name,url,10,iconimage,'',artist,name)    
        setView('movies', 'album') 
        
def BILLBOARD_SONG_LISTS(url,iconimage,artist,album):
        link=OPEN_URL(url)
        match = re.compile('<span class="song-title">(.+?)</span>').findall(link)
        foricon = re.compile('<link rel="image_src" href="(.+?)" />').findall(link)
        iconimage=foricon[0]
        for name in match:
            addDir(name,url,6,iconimage,'',artist,album)    
        setView('movies', 'default') 
        
def DownloaderClass(url,dest,name,dp,start,range): 
    dp.update(int(start), "Downloading & Copying File",'',name)   
    urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,dp,start,range,url))
 
def _pbhook(numblocks, blocksize, filesize, dp, start, range, url=None):
    try:
        percent = min(start+((numblocks*blocksize*range)/filesize), start+range)
        print 'Downloaded '+str(percent)+'%'
        dp.update(int(percent))
    except:
        percent = 100
        dp.update(int(percent))
    if dp.iscanceled(): 
        print "DOWNLOAD CANCELLED" # need to get this part working        
        raise Exception("Canceled")
        
def select_year():
    dialog = xbmcgui.Dialog()
    start = 1960
    end   = datetime.datetime.today().year
    year  = []
    for yr in range(start, end+1):
        year.append(str(yr))
    return year[xbmcgui.Dialog().select('Please Select A Year !', year)]
    
    	
def which_year(name):
    year=select_year()
    url='http://www.officialcharts.com/all-the-number-ones-singles-list/_/'+str(year)+'/'
    GA("Number Ones",str(year))
    link=OPEN_URL(url).replace('\n','')
    match = re.compile('<td class="artist">(.+?)</td>.+?td class="title">(.+?)</td>').findall(link)
    iconimage=icon2
    for artist,name in match:      
        artist=str(artist).replace('&amp;','&').replace('&#039;','')
        name=str(name).replace('&amp;','&').replace('&#039;','')
        addDir(name,'Number Ones',6,iconimage,'',artist,str(year))    
    setView('movies', 'default') 
        
def which_year_playlist(name,clear):
    dialog = xbmcgui.Dialog()
    dp = xbmcgui.DialogProgress()
    dp.create("XBMCHUB Music",'Creating Your Playlist')
    dp.update(0)
    year=select_year()
    pl = get_XBMCPlaylist(clear)
    url='http://www.officialcharts.com/all-the-number-ones-singles-list/_/'+str(year)+'/'
    GA("Playing Playlist",str(year))
    link=OPEN_URL(url).replace('\n','')
    try:
        match = re.compile('<td class="artist">(.+?)</td>.+?td class="title">(.+?)</td>').findall(link)
        iconimage=icon2
        playlist=[]
        nItem=len(match)
        for artist,name in match:   
            artist=urllib.unquote(artist).replace('&amp;','&').replace('&#039;','').replace('/','')
            name=urllib.unquote(name).replace('&amp;','&').replace('&#039;','').replace('/','')
            liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
            liz.setInfo('music', {'Title':name, 'Artist':artist, 'Album':"Number Ones "+str(year)})
            liz.setProperty('mimetype', 'audio/mpeg')                
            playlist.append((for_download_or_playlist(name,artist),liz))

            progress = len(playlist) / float(nItem) * 100               
            dp.update(int(progress), 'Adding to Your Playlist',name)
            if dp.iscanceled():
                return

        print 'THIS IS PLAYLIST====   '+str(playlist)
    
        for blob ,liz in playlist:
            try:
                if blob:
                    pl.add(blob,liz)
            except:
                pass
        if clear or (not xbmc.Player().isPlayingAudio()):
            xbmc.Player(xbmc.PLAYER_CORE_PAPLAYER).play(pl)
    except:
        raise
        dialog = xbmcgui.Dialog()
        dialog.ok("XBMCHUB Music", "Sorry Cant Find Songs From Album", "Why Not Try A Different Album")
        
def which_year_download(name):
    iconimage=icon2
    if musicdownloads == '':
        dialog = xbmcgui.Dialog()
        dialog.ok("XBMCHUB Music", "You Need To Set Your Download Path", "A Window Will Now Open For You To Set")
        ADDON.openSettings()
    year=select_year()
    url='http://www.officialcharts.com/all-the-number-ones-singles-list/_/'+str(year)+'/'
    link=OPEN_URL(url).replace('\n','')
    match = re.compile('<td class="artist">(.+?)</td>.+?td class="title">(.+?)</td>').findall(link)
    path = xbmc.translatePath(os.path.join(musicdownloads+'Number Ones',str(year)))
    if os.path.exists(path) == False:
        os.makedirs(path)
    jpg=os.path.join(path, 'folder.jpg')

    dp = xbmcgui.DialogProgress()
    dp.create("XBMCHUB Music")

    nItems = len(match) + 1 #+1 for cover
    range  = float(100) / nItems
    start  = 0

    DownloaderClass(iconimage,jpg,'Album Cover', dp, start, range)
    start += range

    GA("Downloading",str(year))
    for artist, name in match:
        artist=urllib.unquote(artist).replace('&amp;','&').replace('&#039;','').replace('/','')
        name=urllib.unquote(name).replace('&amp;','&').replace('&#039;','').replace('/','')
        url=for_download_or_playlist(name,artist)
        mp3=os.path.join(path, str(name)+'.mp3')
        try:
            DownloaderClass(url,mp3,name, dp, start, range)
        except Exception , e:
            if str(e) == "Canceled":
                dp.close()
                return
            pass
        start += range
        
        
def top40(name,url):
        GA("None",name)
        link=OPEN_URL(url)
        match = re.compile('<img src="(.+?)".+?\n.+?<span class="track_title".+?>(.+?)</span>.+?\n.+?class="artist">.+?>(.+?)</a></span>').findall(link)
        for iconimage, name, artist in match:
            artist=str(artist).replace('&amp;','&')
            name=str(name).replace('&amp;','&')
            iconimage=str(iconimage).replace('170x170-75.jpg','600x600-75.jpg')
            addDir(name,url,6,iconimage,'',artist,'UK TOP 40')    
        setView('movies', 'default') 
        
def ukalbumchart(name,url):
        GA("None",name)
        link=OPEN_URL(url).replace('\n','')
        link=link.split('The Official Charts logo')[1]
        match = re.compile('<img src="(.+?)".+?<h3>(.+?)</h3>.+?<h4>(.+?)</h4>.+?<a target="_blank" href="http://clk.tradedoubler.com.+?&url=(.+?)"').findall(link)
        uniques=[]
        for iconimage, name, artist,url in match:
            if name not in uniques:
                uniques.append(name) 
                artist=urllib.unquote(artist).replace('&amp;','&').replace('&#039;','')
                name=urllib.unquote(name).replace('&amp;','&').replace('&#039;','')
                iconimage=str(iconimage).replace('60x60-50.jpg','600x600-75.jpg').replace('_50.jpg','_350.jpg')  
                url=urllib.unquote(url)
                addDir(name,url,18,iconimage,'',artist,name)    
        setView('movies', 'album') 
        
        
def UK_CHARTS_SONG_LIST(url,iconimage,artist,album): 
        link=OPEN_URL(url)
        link=link.split('"tracklist-footer"')[0]
        match = re.compile('preview-title="(.+?)"').findall(link)
        for name in match:
            name=str(name).replace('&amp;','&')    
            addDir(name,url,6,iconimage,'',artist,album)    
        setView('movies', 'default') 
        
        

                
def song_links(name,url,iconimage,artist,album):
    GA("Song List",album)
    if url=='Number Ones':
        _artist = 'Number Ones'
    else:
        _artist = artist
    name_url=str(name).replace(' ','_').replace("'",'_').replace(',','').replace('(','').replace(')','')
    artist_url=str(artist).replace(' ','_').replace("'",'_').replace(',','').replace('(','').replace(')','')
    url='http://www.soundcat.ch/browse.php?q='+urllib.quote(name_url).replace('_','+')+'+'+urllib.quote(artist_url).replace('_','+')
    link = OPEN_URL(url).replace("\n",'')
    match=re.compile('div class="listing_song_text">(.+?)</div>.+?"listing_bitrate">(.+?)kbps</div>.+?" href="(.+?)">').findall(link)
    if len(match)< 1:
	    url='http://www.soundcat.ch/browse.php?q='+urllib.quote(name_url).replace('_','+')
	    link = OPEN_URL(url).replace("\n",'')
	    match=re.compile('div class="listing_song_text">(.+?)</div>.+?"listing_bitrate">(.+?)kbps</div>.+?" href="(.+?)">').findall(link)
    print 'SOUNDCAT ========================================='+str(match)
    for name,bitrate,url in match:
        addLink(name+'-('+bitrate+' Kbps)',url,iconimage,'',_artist,album,'true')    
    url='http://mp3skull.com/mp3/'+str(name_url)+'_'+str(artist_url)+'.html'
    link = OPEN_URL(url).replace('\n','')
    match=re.compile('-->.+?([0-9]*?) kbps<br.+?<div style="font-size:15px;"><b>(.+?)</b></div>.+?div style="float:left;"><a href="(.+?)"').findall(link)
    if len(match)< 1:
	    url='http://mp3skull.com/mp3/'+str(name_url)+'.html'
	    link = OPEN_URL(url).replace('\n','')
	    match=re.compile('-->.+?([0-9]*?) kbps<br.+?<div style="font-size:15px;"><b>(.+?)</b></div>.+?div style="float:left;"><a href="(.+?)"').findall(link)
    print 'MP3 Skull========================================='+str(match)
    for bitrate,name,url in match:
        addLink(name+'-('+bitrate+' Kbps)',url,iconimage,'',_artist,album,'true')    
    url='http://www.emp3world.com/search/'+str(name_url)+'_'+str(artist_url)+'_mp3_download.html'
    print url
    link = OPEN_URL(url)
    match=re.compile('<span id="song_title">(.+?) mp3</span>\n.+?input type="hidden" id=".+?" value="(.+?),.+?">').findall(link)
    if len(match)< 1:
	    url='http://www.emp3world.com/search/'+str(name_url)+'_mp3_download.html'
	    print url
	    link = OPEN_URL(url)
	    match=re.compile('<span id="song_title">(.+?) mp3</span>\n.+?input type="hidden" id=".+?" value="(.+?),.+?">').findall(link)
    print 'EMP3WORLD========================================='+str(match)
    for name,url in match:
        addLink(name,url,iconimage,'',_artist,album,'true')    
        
        
def artist_search(url):
    search_entered =SEARCH()
    name=str(search_entered).replace('+','')
    GA("Artist Search",name)
    link = OPEN_URL('http://www.allmusic.com/search/artists/'+search_entered)
    match=re.compile('<a href="(.+?)" data-tooltip=".+?">\n.+?div class="cropped-image" style=".+?" ><img src="(.+?).jpg.+?".+?alt="(.+?)"').findall(link)
    for url,iconimage,artist in match:
        url=allmusic+url
        iconimage=iconimage.replace('JPG_170','JPG_400')+'.jpg'
        addDir(artist,url,4,iconimage,'',artist,'')
        setView('movies', 'default') 
        
        
def artist_album_index(name,url,iconimage,artist):
    GA("None","Album Index")
    link = OPEN_URL(url)
    link = link.split('<table class="album-table condensed-view">')[1]
    link = str(link).replace('\n','')
    match=re.compile('<img src="(.+?).jpg.+?".+?alt="(.+?)".+?<td class="title primary_link" data-sort-value=".+?">.+?<a href="http://www.allmusic.com/album(.+?)"').findall(link)
    uniques=[]
    for iconimage,name,url in match:
        if name not in uniques:
            uniques.append(name)
            url=allmusic+'/album'+url
            iconimage=iconimage.replace('JPG_250','JPG_400').replace('JPG_75','JPG_400')+'.jpg'
            name=str(name).replace("'",'').replace(',','') .replace(":",'').replace('&amp;','And').replace('.','')
            addDir(name,url,5,iconimage,'',artist,name)
            setView('movies', 'album') 
            
def album_index(name,url,iconimage,artist,album):
    link = OPEN_URL(url)
    match=re.compile('class="primary_link">(.+?)</a>').findall(link)
    if len(match)<1:
        match=re.compile('<div class="title primary_link">\n.+?<a href=".+?">(.+?)</a>').findall(link)
    match_artist=re.compile('<div class="album-artist"><a href=".+?">(.+?)</a></div>').findall(link)
    artist=match_artist[0]
    for name in match:
        addDir(name,url,6,iconimage,'',artist,album)
        setView('movies', 'default') 
        
        
def moods(url,iconimage):
    GA("None","Moods")
    link=OPEN_URL(url)
    link=link.split('<div class="mood-container">')[1]
    match=re.compile('<a href="http://www.allmusic.com/mood(.+?)">(.+?)</a>').findall(link)
    for url ,name in match:
        url='http://www.allmusic.com/mood'+url
        addDir(name,url,12,iconimage,'','','')
        setView('movies', 'default') 
        
        
def themes(url,iconimage):
    GA("None","Themes")
    link=OPEN_URL(url)
    match=re.compile('<a href="http://www.allmusic.com/theme(.+?)">(.+?)</a>').findall(link)
    for url ,name in match:
        url='http://www.allmusic.com/theme'+url
        addDir(name,url,12,iconimage,'','','')
        setView('movies', 'default') 
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)
            
def moods_extended_list(url,iconimage):
    link = OPEN_URL(url)
    link = str(link).replace('\n','')
    match=re.compile('<a href="/album/(.+?)-mw(.+?)".+?img src="(.+?).jpg.+?"').findall(link)
    for name,url,iconimage in match:
        url=allmusic+'/album/'+name+'-mw'+url
        name=urllib.unquote(name).upper().replace('-',' ')
        iconimage=iconimage.replace('JPG_170','JPG_400').replace('JPG_250','JPG_400').replace('JPG_75','JPG_400')+'.jpg'
        addDir(name,url,5,iconimage,'','',name)
        setView('movies', 'album')
        
def genre(url,iconimage):
    GA("None","Genre")
    link=OPEN_URL(url)
    match=re.compile('<a href="/genre(.+?)">\n.+?span>(.+?)</span>').findall(link)
    for url, name in match:
        url=allmusic+'/genre'+url
        addDir(name,url,12,iconimage,'','','')
        setView('movies', 'default') 
       
        
def album_search(url):
    search_entered =SEARCH()
    name=str(search_entered).replace('+','')
    GA("Album Search",name)
    link = OPEN_URL('http://www.allmusic.com/search/albums/'+search_entered)
    match=re.compile('<a title="(.+?)" href="/album(.+?)" data-tooltip=".+?">\n.+?<div class="cropped-image".+?><img src="(.+?).jpg.+?"').findall(link)
    for artist,url,iconimage in match:
        url=allmusic+'/album'+url
        iconimage=iconimage.replace('JPG_170','JPG_250')+'.jpg'
        addDir(artist,url,5,iconimage,'',artist,artist)
        setView('movies', 'album') 
                        
        
def song_search(url,iconimage):
    search_entered = SEARCH()
    url='http://www.soundcat.ch/browse.php?q='+str(search_entered)
    link = OPEN_URL(url).replace("\n",'')
    match=re.compile('div class="listing_song_text">(.+?)</div>.+?"listing_bitrate">(.+?)kbps</div>.+?" href="(.+?)">').findall(link)
    for name,bitrate,url in match:
        addLink(name+'-('+bitrate+' Kbps)',url,icon2,'','','','true') 
    search_entered=str(search_entered).replace('+','_')
    url='http://mp3skull.com/mp3/'+str(search_entered)+'.html'
    link = OPEN_URL(url).replace('\n','')
    match=re.compile('-->.+?([0-9]*?) kbps<br.+?<div style="font-size:15px;"><b>(.+?)</b></div>.+?div style="float:left;"><a href="(.+?)"').findall(link)
    print 'MP3 Skull========================================='+str(match)
    for bitrate,name,url in match:
        addLink(name+'-('+bitrate+' Kbps)',url,icon2,'','','','true')    
    search_entered=str(search_entered).replace('+','_')
    url='http://www.emp3world.com/search/'+str(search_entered)+'_mp3_download.html'
    link = OPEN_URL(url)
    match=re.compile('<span id="song_title">(.+?) mp3</span>\n.+?input type="hidden" id=".+?" value="(.+?),.+?">').findall(link)
    print 'EMP3WORLD========================================='+str(match)
    for name,url in match:
        addLink(name,url,icon2,'','','','true')    
    GA("Song Search",str(search_entered).replace('+',' '))
    
 
def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
    
def ENTER_ALBUM_OR_ARTIST(name):
        search_entered = ''
        keyboard = xbmc.Keyboard(search_entered, 'Please Enter '+str(name)+' Name')
        keyboard.doModal()
        if keyboard.isConfirmed():
            search_entered = keyboard.getText()
            if search_entered == None:
                return False          
        return search_entered    
    
def SEARCH():
        search_entered = ''
        keyboard = xbmc.Keyboard(search_entered, 'Search Music...XBMCHUB.COM')
        keyboard.doModal()
        if keyboard.isConfirmed():
            search_entered = keyboard.getText() .replace(' ','+')  # sometimes you need to replace spaces with + or %20
            if search_entered == None:
                return False          
        return search_entered    
    
        
def for_download_or_playlist(name,artist):
    hello = None
    name=str(name).replace(' ','_').replace("'",'_').replace(',','').replace('(','').replace(')','')
    artist=str(artist).replace(' ','_').replace("'",'_').replace(',','').replace('(','').replace(')','')
    url='http://www.soundcat.ch/browse.php?q='+urllib.quote(name).replace('_','+')+'+'+urllib.quote(artist).replace('_','+')
    link = OPEN_URL(url).replace("\n",'')
    match=re.compile('div class="listing_song_text">(.+?)</div>.+?" href="(.+?)">').findall(link)
    try:
        url=match[0][1]
        hello= 'SOUNDCAT  ========================================='+str(url)
    except:
        pass
    if len(match)< 1:
        url='http://www.soundcat.ch/browse.php?q='+urllib.quote(name).replace('_','+')
        link = OPEN_URL(url).replace("\n",'')
        match=re.compile('div class="listing_song_text">(.+?)</div>.+?" href="(.+?)">').findall(link)
        try:
            url=match[0][1]
            hello= 'SOUNDCAT WITHOUT ARTIST ========================================='+str(url)
        except:
            pass
    if len(match)< 1:
        url='http://musicspace.in/mp3/'+str(name).replace('_','-')+'-'+str(artist).replace('_','-')
        link = OPEN_URL(url)
        link = str(link).replace('\x00','')
        match=re.compile('<h4>(.+?).mp3</h4>\n.+?p>\n.+?\n.+?a href="(.+?)"').findall(link)
        try:
            url=match[0][1]
            hello= 'MUSIC SPACE 1 ========================================='+str(url)
        except:
            pass
    if len(match)< 1:
        url='http://www.emp3world.com/search/'+str(name)+'_'+str(artist)+'_mp3_download.html'
        link = OPEN_URL(url)
        match=re.compile('<span id="song_title">(.+?) mp3</span>\n.+?input type="hidden" id=".+?" value="(.+?),.+?">').findall(link)
        try:
            url=match[0][1]
            hello= 'emp3 world ====='+str(url)
        except:
            pass
    if len(match)< 1:
        if len(match)<1:
            url = url='http://musicspace.in/mp3/'+str(name).replace('_','-')
            link = OPEN_URL(url)
            link = str(link).replace('\x00','')
            match=re.compile('<h4>(.+?).mp3</h4>\n.+?p>\n.+?\n.+?a href="(.+?)"').findall(link)
            try:
                url=match[0][1]
                hello= 'MUSIC SPACE 2 ========================================='+str(url)
            except:
                pass
        if len(match)<1:
            url='http://mp3skull.com/mp3/'+str(name)+'_'+str(artist)+'.html'
            link = OPEN_URL(url)
            match=re.compile('<div style="float:left;"><a href="(.+?)"').findall(link)
        try:
            url=match[0]
            hello= 'MP3 Skull========================================='+str(url)
        except:
            pass

    if not hello:
        print "NOT FOUND========================================="
        return None
    print hello   
    return url
    
    
def download_single_song(name,url,iconimage,artist,album):
    name=str(name)
    if re.search('Kbps',name,re.IGNORECASE):
        regex=re.compile('(.+?)-\((.+?) Kbps\)')
        match = regex.search(name)
        name = match.group(1)
    if artist=="None":
        artist=ENTER_ALBUM_OR_ARTIST("Artists")
    if album=="None":
        album=ENTER_ALBUM_OR_ARTIST("Album")
    if artist=="":
        artist=ENTER_ALBUM_OR_ARTIST("Artists")
    if album=="":
        album=ENTER_ALBUM_OR_ARTIST("Album")
    path = xbmc.translatePath(os.path.join(musicdownloads+artist,album))
    GA("Downloading",artist)
    if os.path.exists(path) == False:
        os.makedirs(path)
    jpg=os.path.join(path, 'folder.jpg')

    dp = xbmcgui.DialogProgress()
    dp.create("XBMCHUB Music")
    if os.path.exists(jpg) == False:
        nItems = 1 + 1 #+1 for cover
    else:
        nItems = 1
    range  = int(100) / nItems
    start  = 0
    if os.path.exists(jpg) == False:
        try:
            DownloaderClass(iconimage,jpg,'Album Cover', dp, start, range)
            start += range
        except:
            pass
    name=str(name).replace("'",'').replace(".",'').replace(",",'')
    mp3=os.path.join(path, str(name)+'.mp3')
    try:
        DownloaderClass(url,mp3,name, dp, start, range)            
    except Exception , e:
        if str(e) == "Canceled":
            dp.close()
            return
        pass
    start += range


    
def download_album(name,url,iconimage,artist,album):
    iconimage=str(iconimage)
    if musicdownloads == '':
        dialog = xbmcgui.Dialog()
        dialog.ok("XBMCHUB Music", "You Need To Set Your Download Path", "A Window Will Now Open For You To Set")
        ADDON.openSettings()
    if re.search('allmusic',url,re.IGNORECASE):
        link = OPEN_URL(url)
        match=re.compile('class="primary_link">(.+?)</a>').findall(link)
        if len(match)<1:
            match=re.compile('<div class="title primary_link">\n.+?<a href=".+?">(.+?)</a>').findall(link)
        try:
            match_artist=re.compile('<div class="album-artist"><a href=".+?">(.+?)</a></div>').findall(link)
            artist=match_artist[0]
        except:
            artist=''
        album=str(album).replace("'",'').replace(",",'').replace(":",'')
    else:
        link=OPEN_URL(url)
        match=re.compile('<span class="song-title">(.+?)</span>').findall(link)
        foricon = re.compile('<link rel="image_src" href="(.+?)" />').findall(link)
        iconimage=foricon[0]
    path = xbmc.translatePath(os.path.join(musicdownloads+artist,album))
    if os.path.exists(path) == False:
        os.makedirs(path)
    jpg=os.path.join(path, 'folder.jpg')

    dp = xbmcgui.DialogProgress()
    dp.create("XBMCHUB Music")

    nItems = len(match) + 1 #+1 for cover
    range  = float(100) / nItems
    start  = 0

    DownloaderClass(iconimage,jpg,'Album Cover', dp, start, range)
    start += range

    GA("Downloading",artist)
    for name in match:
        name=str(name).replace("'",'').replace(".",'').replace(",",'')
        url=for_download_or_playlist(name,artist)
        mp3=os.path.join(path, str(name)+'.mp3')
        try:
            DownloaderClass(url,mp3,name, dp, start, range)            
        except Exception , e:
            if str(e) == "Canceled":
                dp.close()
                return
            pass
        start += range
            
def download_uk_album(name,url,iconimage,artist,album):
    iconimage=str(iconimage)
    if musicdownloads == '':
        dialog = xbmcgui.Dialog()
        dialog.ok("XBMCHUB Music", "You Need To Set Your Download Path", "A Window Will Now Open For You To Set")
        ADDON.openSettings()
    link=OPEN_URL(url)
    if re.search('apple.com',url,re.IGNORECASE):
        link=link.split('table class="tracklist-footer"')[0]
        match=re.compile('preview-title="(.+?)"').findall(link)
    else:
        match=re.compile('&#39;(.+?)&#39;').findall(link)
    path = xbmc.translatePath(os.path.join(musicdownloads+artist,album))
    if os.path.exists(path) == False:
        os.makedirs(path)
    jpg=os.path.join(path, 'folder.jpg')

    dp = xbmcgui.DialogProgress()
    dp.create("XBMCHUB Music")

    nItems = len(match) + 1 #+1 for cover
    range  = float(100) / nItems
    start  = 0

    DownloaderClass(iconimage,jpg,'Album Cover', dp, start, range)
    start += range

    GA("Downloading",artist)
    for name in match:
        name=str(name).replace("'",'').replace(".",'').replace(",",'').replace('&amp;','')
        url=for_download_or_playlist(name,artist)
        mp3=os.path.join(path, str(name)+'.mp3')
        try:
            DownloaderClass(url,mp3,name, dp, start, range)
        except Exception , e:
            if str(e) == "Canceled":
                dp.close()
                return
            pass
        start += range
            
def get_XBMCPlaylist(clear):
    pl=xbmc.PlayList(xbmc.PLAYLIST_MUSIC)
    #if not xbmc.Player().isPlayingAudio():
    if clear:
        pl.clear()
    return pl

    dialog = xbmcgui.Dialog()
    if dialog.yesno("XBMCHUB Music", 'Queue album or play now?', '', '', 'Play Now','Queue') == 0:
        pl.clear()
    return pl
            
            
def get_playlist(name,url,iconimage,artist,album,clear):
    iconimage=str(iconimage)
    dp = xbmcgui.DialogProgress()
    dp.create("XBMCHUB Music",'Creating Your Playlist')
    dp.update(0)
    pl = get_XBMCPlaylist(clear)
    link=OPEN_URL(url)
    try:
	    if re.search('allmusic',url,re.IGNORECASE):
	        match=re.compile('class="primary_link">(.+?)</a>').findall(link)
	        if len(match)<1:
	            match=re.compile('<div class="title primary_link">\n.+?<a href=".+?">(.+?)</a>').findall(link)
	        try:
		        match_artist=re.compile('<div class="album-artist"><a href=".+?">(.+?)</a></div>').findall(link)
		        artist=match_artist[0]
	        except:
		        artist=''
	    else:
	        match=re.compile('<span class="song-title">(.+?)</span>').findall(link)
	        foricon = re.compile('<link rel="image_src" href="(.+?)" />').findall(link)
	        iconimage=foricon[0]
	    playlist=[]

            nItem = len(match)           
	    for name in match:                
	        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	        #liz.setInfo( type="Audio", infoLabels={ "Title": name} )
                liz.setInfo('music', {'Title':name, 'Artist':artist, 'Album':album})
	        liz.setProperty('mimetype', 'audio/mpeg')                
	        playlist.append((for_download_or_playlist(name,artist),liz))

                progress = len(playlist) / float(nItem) * 100               
	        dp.update(int(progress), 'Adding to Your Playlist',name)
                if dp.iscanceled():
                    return

	    print 'THIS IS PLAYLIST====   '+str(playlist)
            
	    for blob ,liz in playlist:
	        try:
                    if blob:
	                pl.add(blob,liz)
	        except:
	            pass
            if clear or (not xbmc.Player().isPlayingAudio()):
	        xbmc.Player(xbmc.PLAYER_CORE_PAPLAYER).play(pl)
    except:
        raise
        dialog = xbmcgui.Dialog()
        dialog.ok("XBMCHUB Music", "Sorry Cant Find Songs From Album", "Why Not Try A Different Album")
    GA("Playing Playlist",artist)
    
    
def get_uk_playlist(name,url,iconimage,artist,album,clear):
    iconimage=str(iconimage)
    dp = xbmcgui.DialogProgress()
    dp.create("XBMCHUB Music",'Creating Your Playlist')
    dp.update(0)
    pl = get_XBMCPlaylist(clear)
    link=OPEN_URL(url)
    try:
	    if re.search('apple.com',url,re.IGNORECASE):
	        link=link.split('table class="tracklist-footer"')[0]
	        match=re.compile('preview-title="(.+?)"').findall(link)
	    else:
	        match=re.compile('&#39;(.+?)&#39;').findall(link)
	    playlist=[]

            nItem = len(match)           
	    for name in match:    
	        name=name.replace('&amp;','')
	        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	        #liz.setInfo( type="Audio", infoLabels={ "Title": name} )
                liz.setInfo('music', {'Title':name, 'Artist':artist, 'Album':album})
	        liz.setProperty('mimetype', 'audio/mpeg')                
	        playlist.append((for_download_or_playlist(name,artist),liz))

                progress = len(playlist) / float(nItem) * 100               
	        dp.update(int(progress), 'Adding to Your Playlist',name)
                if dp.iscanceled():
                    return

	    print 'THIS IS PLAYLIST====   '+str(playlist)
            
	    for blob ,liz in playlist:
	        try:
                    if blob:
	                pl.add(blob,liz)
	        except:
	            pass
            if clear or (not xbmc.Player().isPlayingAudio()):
	        xbmc.Player(xbmc.PLAYER_CORE_PAPLAYER).play(pl)
    except:
        raise
        dialog = xbmcgui.Dialog()
        dialog.ok("XBMCHUB Music", "Sorry Cant Find Songs From Album", "Why Not Try A Different Album")
    GA("Playing Playlist",artist)
                  
    
def getFavorites():
        f = open(favorites, 'r')
        a = f.read()
        try:
            for i in json.loads(a):
                name = i[0]
                url = i[1]
                iconimage = i[2]
                artist = i[3]
                album = i[4]
                if re.search('allmusic',url,re.IGNORECASE):
                    addDir(name,url,5,iconimage,'',artist,album)
                else:
                        addDir(name,url,10,iconimage,'',artist,album) 
                setView('movies', 'album')
        except:
            pass

            
def addFavorite(name,url,iconimage,artist,album):
        GA("None","Add Favourite")
        favList = []
        if os.path.exists(favorites)==False:
            print 'Making Favorites File'
            favList.append((name,url,iconimage,artist,album))
            a = open(favorites, "w")
            a.write(json.dumps(favList))
            a.close()
        else:
            print 'Appending Favorites'
            f = open(favorites, 'r')
            a = f.read()
            try:
                data = json.loads(a)
                data.append((name,url,iconimage,artist,album))
                f.close()
                b = open(favorites, "w")
                b.write(json.dumps(data))
                b.close()
            except:
                favList.append((name,url,iconimage,artist,album))
                a = open(favorites, "w")
                a.write(json.dumps(favList))
                a.close()

def rmFavorite(name):
        print 'Remove Favorite'
        f = open(favorites, 'r')
        a = f.read()
        data = json.loads(a)
        for index in range(len(data)):
            try:
                if data[index][0]==name:
                    del data[index]
                    f.close()
                    b = open(favorites, "w")
                    b.write(json.dumps(data))
                    b.close()
            except:
                pass
                    
    
def parseDate(dateString):
    try:
        return datetime.datetime.fromtimestamp(time.mktime(time.strptime(dateString.encode('utf-8', 'replace'), "%Y-%m-%d %H:%M:%S")))
    except:
        return datetime.datetime.today() - datetime.timedelta(days = 1) #force update


def checkGA():

    secsInHour = 60 * 60
    threshold  = 2 * secsInHour

    now   = datetime.datetime.today()
    prev  = parseDate(ADDON.getSetting('ga_time'))
    delta = now - prev
    nDays = delta.days
    nSecs = delta.seconds

    doUpdate = (nDays > 0) or (nSecs > threshold)
    if not doUpdate:
        return

    ADDON.setSetting('ga_time', str(now).split('.')[0])
    APP_LAUNCH()
    
    
    
                    
def send_request_to_google_analytics(utm_url):
    ua='Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
    import urllib2
    try:
        req = urllib2.Request(utm_url, None,
                                    {'User-Agent':ua}
                                     )
        response = urllib2.urlopen(req).read()
    except:
        print ("GA fail: %s" % utm_url)         
    return response
       
def GA(group,name):
        try:
            try:
                from hashlib import md5
            except:
                from md5 import md5
            from random import randint
            import time
            from urllib import unquote, quote
            from os import environ
            from hashlib import sha1
            VISITOR = ADDON.getSetting('visitor_ga')
            utm_gif_location = "http://www.google-analytics.com/__utm.gif"
            if not group=="None":
                    utm_track = utm_gif_location + "?" + \
                            "utmwv=" + VERSION + \
                            "&utmn=" + str(randint(0, 0x7fffffff)) + \
                            "&utmt=" + "event" + \
                            "&utme="+ quote("5("+PATH+"*"+group+"*"+name+")")+\
                            "&utmp=" + quote(PATH) + \
                            "&utmac=" + UATRACK + \
                            "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR,VISITOR,"2"])
                    try:
                        print "============================ POSTING TRACK EVENT ============================"
                        send_request_to_google_analytics(utm_track)
                    except:
                        print "============================  CANNOT POST TRACK EVENT ============================" 
            if name=="None":
                    utm_url = utm_gif_location + "?" + \
                            "utmwv=" + VERSION + \
                            "&utmn=" + str(randint(0, 0x7fffffff)) + \
                            "&utmp=" + quote(PATH) + \
                            "&utmac=" + UATRACK + \
                            "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR, VISITOR,"2"])
            else:
                if group=="None":
                       utm_url = utm_gif_location + "?" + \
                                "utmwv=" + VERSION + \
                                "&utmn=" + str(randint(0, 0x7fffffff)) + \
                                "&utmp=" + quote(PATH+"/"+name) + \
                                "&utmac=" + UATRACK + \
                                "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR, VISITOR,"2"])
                else:
                       utm_url = utm_gif_location + "?" + \
                                "utmwv=" + VERSION + \
                                "&utmn=" + str(randint(0, 0x7fffffff)) + \
                                "&utmp=" + quote(PATH+"/"+group+"/"+name) + \
                                "&utmac=" + UATRACK + \
                                "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR, VISITOR,"2"])
                                
            print "============================ POSTING ANALYTICS ============================"
            send_request_to_google_analytics(utm_url)
            
        except:
            print "================  CANNOT POST TO ANALYTICS  ================" 
            
            
def APP_LAUNCH():
        print '==========================   '+PATH+' '+VERSION+'   =========================='
        try:
            try:
                from hashlib import md5
            except:
                from md5 import md5
            from random import randint
            import time
            from urllib import unquote, quote
            from os import environ
            from hashlib import sha1
            import platform
            VISITOR = ADDON.getSetting('visitor_ga')
            if re.search('12.',xbmc.getInfoLabel( "System.BuildVersion"),re.IGNORECASE): 
                build="Frodo" 
            if re.search('11.',xbmc.getInfoLabel( "System.BuildVersion"),re.IGNORECASE): 
                build="Eden" 
            if re.search('13.',xbmc.getInfoLabel( "System.BuildVersion"),re.IGNORECASE): 
                build="Gotham" 
            try: 
                PLATFORM=platform.system()+' '+platform.release()
            except: 
                PLATFORM=platform.system()
            utm_gif_location = "http://www.google-analytics.com/__utm.gif"
            utm_track = utm_gif_location + "?" + \
                    "utmwv=" + VERSION + \
                    "&utmn=" + str(randint(0, 0x7fffffff)) + \
                    "&utmt=" + "event" + \
                    "&utme="+ quote("5(APP LAUNCH*"+PATH+"-"+build+"*"+PLATFORM+")")+\
                    "&utmp=" + quote(PATH) + \
                    "&utmac=" + UATRACK + \
                    "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR,VISITOR,"2"])
            try:
                print "============================ POSTING APP LAUNCH TRACK EVENT ============================"
                send_request_to_google_analytics(utm_track)
            except:
                print "============================  CANNOT POST APP LAUNCH TRACK EVENT ============================" 
            
        except:
            print "================  CANNOT POST TO ANALYTICS  ================" 
checkGA()
            
            
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
def addDir(name,url,mode,iconimage,description,artist,album):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)+"&artist="+urllib.quote_plus(artist)+"&album="+urllib.quote_plus(album)
        ok=True        
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description} )
        liz.setProperty("Fanart_Image", fanart)
        menu = []
        if mode==5:
            menu.append(('Play Album', 'XBMC.RunPlugin(%s?mode=200&url=%s&name=%s&iconimage=%s&artist=%s&album=%s)'% (sys.argv[0], url,name,iconimage,artist,album)))
            menu.append(('Queue Album', 'XBMC.RunPlugin(%s?mode=202&url=%s&name=%s&iconimage=%s&artist=%s&album=%s)'% (sys.argv[0], url,name,iconimage,artist,album)))
            menu.append(('Download Album', 'XBMC.RunPlugin(%s?mode=201&url=%s&name=%s&iconimage=%s&artist=%s&album=%s)'% (sys.argv[0], url,name,iconimage,artist,album)))
            try:
                if name in FAV:
                    menu.append(('Remove Album Favorites','XBMC.Container.Update(%s?name=%s&mode=205&iconimage=None&artist=None&url=None&album=None)' %(sys.argv[0],name)))
                else:
                    menu.append(('Add to Album Favorites','XBMC.Container.Update(%s?&mode=204&url=%s&album=%s&iconimage=%s&artist=%s&name=%s)'% (sys.argv[0], url,name,iconimage,artist,album)))
            except:
                menu.append(('Add to Album Favorites','XBMC.Container.Update(%s?&mode=204&url=%s&album=%s&iconimage=%s&artist=%s&name=%s)'% (sys.argv[0], url,name,iconimage,artist,album)))
            liz.addContextMenuItems(items=menu, replaceItems=True)
        if mode==12:
            menu.append(('Play Album', 'XBMC.RunPlugin(%s?mode=200&url=%s&name=%s&iconimage=%s&artist=%s&album=%s)'% (sys.argv[0], url,name,iconimage,artist,album)))
            menu.append(('Queue Album', 'XBMC.RunPlugin(%s?mode=202&url=%s&name=%s&iconimage=%s&artist=%s&album=%s)'% (sys.argv[0], url,name,iconimage,artist,album)))
            menu.append(('Download Album', 'XBMC.RunPlugin(%s?mode=201&url=%s&name=%s&iconimage=%s&artist=%s&album=%s)'% (sys.argv[0], url,name,iconimage,artist,album)))
            try:
                if name in FAV:
                    menu.append(('Remove Album Favorites','XBMC.Container.Update(%s?name=%s&mode=205&iconimage=None&artist=None&url=None&album=None)' %(sys.argv[0],name)))
                else:
                    menu.append(('Add to Album Favorites','XBMC.Container.Update(%s?&mode=204&url=%s&album=%s&iconimage=%s&artist=%s&name=%s)'% (sys.argv[0], url,name,iconimage,artist,album)))
            except:
                menu.append(('Add to Album Favorites','XBMC.Container.Update(%s?&mode=204&url=%s&album=%s&iconimage=%s&artist=%s&name=%s)'% (sys.argv[0], url,name,iconimage,artist,album)))
            liz.addContextMenuItems(items=menu, replaceItems=True)
        if mode==10:
            menu.append(('Play Album', 'XBMC.RunPlugin(%s?mode=200&url=%s&name=%s&iconimage=%s&artist=%s&album=%s)'% (sys.argv[0], url,name,iconimage,artist,album)))
            menu.append(('Queue Album', 'XBMC.RunPlugin(%s?mode=202&url=%s&name=%s&iconimage=%s&artist=%s&album=%s)'% (sys.argv[0], url,name,iconimage,artist,album)))
            menu.append(('Download Album', 'XBMC.RunPlugin(%s?mode=201&url=%s&name=%s&iconimage=%s&artist=%s&album=%s)'% (sys.argv[0], url,name,iconimage,artist,album)))
            try:
                if name in FAV:
                    menu.append(('Remove Album Favorites','XBMC.Container.Update(%s?name=%s&mode=205&iconimage=None&artist=None&url=None&album=None)' %(sys.argv[0],name)))
                else:
                    menu.append(('Add to Album Favorites','XBMC.Container.Update(%s?&mode=204&url=%s&album=%s&iconimage=%s&artist=%s&name=%s)'% (sys.argv[0], url,name,iconimage,artist,album)))
            except:
                menu.append(('Add to Album Favorites','XBMC.Container.Update(%s?&mode=204&url=%s&album=%s&iconimage=%s&artist=%s&name=%s)'% (sys.argv[0], url,name,iconimage,artist,album)))
            liz.addContextMenuItems(items=menu, replaceItems=True)
        if mode==18:
            url=urllib.quote(url)        
            menu.append(('Play Album', 'XBMC.RunPlugin(%s?mode=206&url=%s&name=%s&iconimage=%s&artist=%s&album=%s)'% (sys.argv[0], url,name,iconimage,artist,album)))
            menu.append(('Queue Album', 'XBMC.RunPlugin(%s?mode=207&url=%s&name=%s&iconimage=%s&artist=%s&album=%s)'% (sys.argv[0], url,name,iconimage,artist,album)))
            menu.append(('Download Album', 'XBMC.RunPlugin(%s?mode=208&url=%s&name=%s&iconimage=%s&artist=%s&album=%s)'% (sys.argv[0], url,name,iconimage,artist,album)))
            try:
                if name in FAV:
                    menu.append(('Remove Album Favorites','XBMC.Container.Update(%s?name=%s&mode=205&iconimage=None&artist=None&url=None&album=None)' %(sys.argv[0],name)))
                else:
                    menu.append(('Add to Album Favorites','XBMC.Container.Update(%s?&mode=204&url=%s&album=%s&iconimage=%s&artist=%s&name=%s)'% (sys.argv[0], url,name,iconimage,artist,album)))
            except:
                menu.append(('Add to Album Favorites','XBMC.Container.Update(%s?&mode=204&url=%s&album=%s&iconimage=%s&artist=%s&name=%s)'% (sys.argv[0], url,name,iconimage,artist,album)))
            liz.addContextMenuItems(items=menu, replaceItems=True)
        if mode==15:
            menu.append(('Play Album', 'XBMC.RunPlugin(%s?mode=206&url=%s&name=%s&iconimage=%s&artist=%s&album=%s)'% (sys.argv[0], url,name,iconimage,artist,album)))
            menu.append(('Queue Album', 'XBMC.RunPlugin(%s?mode=207&url=%s&name=%s&iconimage=%s&artist=%s&album=%s)'% (sys.argv[0], url,name,iconimage,artist,album)))
            menu.append(('Download Album', 'XBMC.RunPlugin(%s?mode=208&url=%s&name=%s&iconimage=%s&artist=%s&album=%s)'% (sys.argv[0], url,name,iconimage,artist,album)))
            try:
                if name in FAV:
                    menu.append(('Remove Album Favorites','XBMC.Container.Update(%s?name=%s&mode=205&iconimage=None&artist=None&url=None&album=None)' %(sys.argv[0],name)))
                else:
                    menu.append(('Add to Album Favorites','XBMC.Container.Update(%s?&mode=204&url=%s&album=%s&iconimage=%s&artist=%s&name=%s)'% (sys.argv[0], url,name,iconimage,artist,album)))
            except:
                menu.append(('Add to Album Favorites','XBMC.Container.Update(%s?&mode=204&url=%s&album=%s&iconimage=%s&artist=%s&name=%s)'% (sys.argv[0], url,name,iconimage,artist,album)))
            liz.addContextMenuItems(items=menu, replaceItems=True)
        if mode==19:
            menu.append(('Play Album', 'XBMC.RunPlugin(%s?mode=210&name=%s&iconimage=None&artist=None&url=None&album=None)'% (sys.argv[0], name)))
            menu.append(('Queue Album', 'XBMC.RunPlugin(%s?mode=211&name=%s&iconimage=None&artist=None&url=None&album=None)'% (sys.argv[0], name)))
            menu.append(('Download Album', 'XBMC.RunPlugin(%s?mode=212&name=%s&iconimage=None&artist=None&url=None&album=None)'% (sys.argv[0], name)))
            try:
                if name in FAV:
                    menu.append(('Remove Album Favorites','XBMC.Container.Update(%s?name=%s&mode=205&iconimage=None&artist=None&url=None&album=None)' %(sys.argv[0],name)))
                else:
                    menu.append(('Add to Album Favorites','XBMC.Container.Update(%s?&mode=204&url=%s&album=%s&iconimage=%s&artist=%s&name=%s)'% (sys.argv[0], url,name,iconimage,artist,album)))
            except:
                menu.append(('Add to Album Favorites','XBMC.Container.Update(%s?&mode=204&url=%s&album=%s&iconimage=%s&artist=%s&name=%s)'% (sys.argv[0], url,name,iconimage,artist,album)))
            liz.addContextMenuItems(items=menu, replaceItems=True)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        
        
        
def addLink(name,url,iconimage,description,artist,album,download):  
        ok=True       
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo('music', {'Title':name, 'Artist':artist, 'Album':album})
        liz.setProperty("IsPlayable","true")
        liz.setProperty( "Fanart_Image", fanart)
        menu = []
        if download =="true":
            url_for_download=urllib.quote_plus(url)
            menu.append(('Download Song', 'XBMC.RunPlugin(%s?&iconimage=%s&mode=209&url=%s&artist=%s&album=%s&name=%s)'% (sys.argv[0], iconimage,url_for_download,artist,album,name)))
            liz.addContextMenuItems(items=menu, replaceItems=True)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
        return ok 
        
 
        
def setView(content, viewType):
        if content:
                xbmcplugin.setContent(int(sys.argv[1]), content)
        if ADDON.getSetting('auto-view') == 'true':#<<<----see here if auto-view is enabled(true) 
                xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )#<<<-----then get the view type
                      
               
params=get_params()
url=None
name=None
mode=None
iconimage=None
description=None
artist=None
album=None

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
        mode=int(params["mode"])
except:
        pass
try:        
        description=urllib.unquote_plus(params["description"])
except:
        pass
try:        
        artist=urllib.unquote_plus(params["artist"])
except:
        pass
try:        
        album=urllib.unquote_plus(params["album"])
except:
        pass
        
        
        
        

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IconImage: "+str(iconimage)
print "Artist: "+str(artist)
print "Album: "+str(album)
#these are the modes which tells the plugin where to go
if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
       
elif mode==1:
        print ""+url
        artist_search(url)
        
elif mode==2:
        print ""+url
        album_search(url)
        
elif mode==3:
        print ""+url
        song_search(url,iconimage)
        
elif mode==4:
        print ""+url
        artist_album_index(name,url,iconimage,artist)
        
elif mode==5:
        print ""+url
        album_index(name,url,iconimage,artist,album)
        
elif mode==6:
        print ""+url
        song_links(name,url,iconimage,artist,album)
        
elif mode==7:
    print ""
    getFavorites()
        
elif mode==8:
        print ""+url
        BILLBOARD_MAIN_LIST(url)
        
elif mode==9:
        print ""+url
        BILLBOARD_ALBUM_LISTS(name,url) 
        
elif mode==10:
        print ""+url
        BILLBOARD_SONG_LISTS(url,iconimage,artist,album) 
        
elif mode==11:
        print ""+url
        moods(url,iconimage) 
        
elif mode==12:
        print ""+url
        moods_extended_list(url,iconimage) 
        
elif mode==13:
        print ""+url
        genre(url,iconimage) 
        
elif mode==14:
        print ""+url
        themes(url,iconimage) 
        
elif mode==15:
        print ""+url
        top40(name,url)
        
elif mode==16:
        print ""+url
        ukalbumchart(name,url) 
        
elif mode==17:
        print ""+url
        UK_CHARTS(name,url) 
        
elif mode==18:
        print ""+url
        UK_CHARTS_SONG_LIST(url,iconimage,artist,album) 
elif mode==19:
        print ""+url
        which_year(name) 
        
elif mode==200:
        print ""+url
        get_playlist(name,url,iconimage,artist,album,True)

elif mode==202:
        print ""+url
        get_playlist(name,url,iconimage,artist,album,False)
        
elif mode==201:
        print ""+url
        download_album(name,url,iconimage,artist,album)
               
elif mode==204:
    print ""
    addFavorite(name,url,iconimage,artist,album)

elif mode==205:
    print ""
    rmFavorite(name)
    
    
elif mode==206:
        print ""+url
        get_uk_playlist(name,url,iconimage,artist,album,True)
elif mode==207:
        print ""+url
        get_uk_playlist(name,url,iconimage,artist,album,False)
        
elif mode==208:
        print ""+url
        download_uk_album(name,url,iconimage,artist,album)
    
elif mode==209:
        print ""+url
        download_single_song(name,url,iconimage,artist,album)
        
elif mode==210:
        print ""+url
        which_year_playlist(name,True)
    
elif mode==211:
        print ""+url
        which_year_playlist(name,False)
        
elif mode==212:
        print ""+url
        which_year_download(name)
        
xbmcplugin.endOfDirectory(int(sys.argv[1]))
