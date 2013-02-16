
import xbmc, xbmcgui, xbmcplugin, urllib2, urllib, re, sys, os, time
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup
import resources.lib._common as common

BASE = 'http://www.spike.com'
pluginhandle = int(sys.argv[1])

def masterlist():
    return rootlist(db=True)
        
def rootlist(db=False):
    xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
    xbmcplugin.addSortMethod(pluginhandle, xbmcplugin.SORT_METHOD_LABEL)
    url = BASE + '/shows/'
    data = common.getURL(url)
    tree=BeautifulSoup(data, convertEntities=BeautifulSoup.HTML_ENTITIES)
    categories=tree.findAll(attrs={'class' : 'module  primetime_and_originals'})
    db_shows = []
    for category in categories:
        shows = category.findAll('li')
        for show in shows:
            link = show.find('a')
            url = BASE+link['href']
            name = link.string
            if name == 'The Ultimate Fighter':
                continue
            if db==True:
                db_shows.append((name,'spike','episodes',url))
            else:
                common.addDirectory(name, 'spike', 'episodes', url)
    if db==True:
        return db_shows

def episodes(url=common.args.url):
    xbmcplugin.addSortMethod(pluginhandle, xbmcplugin.SORT_METHOD_LABEL)
    data = common.getURL(url)
    tree=BeautifulSoup(data, convertEntities=BeautifulSoup.HTML_ENTITIES)
    #try:
    seeall=tree.find('a', attrs={'class' : 'see_all'})
    categories=tree.findAll('a',attrs={'class' : 'read_full'})
    categories.append(seeall)
    try:
        for category in categories:
            if category is not None:
                url = category['href']
                name = category.string.replace('See all ','')
                if name == 'Video Clips':
                    common.addDirectory(name, 'spike', 'videos', url)
                elif name == 'Full Episodes':
                    common.addDirectory(name, 'spike', 'fullepisodes', url)
    except:
        video=tree.find(attrs={'class' : 'see_all_videos clearfix'}).find('a')
        url = video['href']
        name = video.contents[1].contents[0].replace('See All ','')
        common.addDirectory(name, 'spike', 'videos', url)


def videos(url=common.args.url):
    xbmcplugin.setContent(pluginhandle, 'episodes')
    data = common.getURL(url)
    tree=BeautifulSoup(data, convertEntities=BeautifulSoup.HTML_ENTITIES)
    episodes=tree.find(attrs={'id' : 'show_clips_res'}).findAll(attrs={'class' : 'block'})
    for episode in episodes:
        description = episode.find('p').renderContents()#.encode('utf-8')
        thumb = episode.find('img')['src'].split('?')[0]
        name = episode.find('h3').find('a').string.encode('utf-8')
        url = episode.find('h3').find('a')['href']
        print name, url, thumb, description
        u = sys.argv[0]
        u += '?url="'+urllib.quote_plus(url)+'"'
        u += '&mode="spike"'
        u += '&sitemode="playvideo"'
        item=xbmcgui.ListItem(name, iconImage=thumb, thumbnailImage=thumb)
        item.setInfo( type="Video", infoLabels={ "Title":name,
                                                 #"Season":season,
                                                 #"Episode":episode,
                                                 "Plot":description
                                                 #"premiered":airDate,
                                                 #"Duration":duration,
                                                 #"TVShowTitle":common.args.name
                                                 })
        item.setProperty('IsPlayable', 'true')
        xbmcplugin.addDirectoryItem(pluginhandle,url=u,listitem=item,isFolder=False)

def fullepisodes(url=common.args.url):
    xbmcplugin.setContent(pluginhandle, 'episodes')
    data = common.getURL(url)
    tree=BeautifulSoup(data, convertEntities=BeautifulSoup.HTML_ENTITIES)
    episodes=tree.find(attrs={'class' : 'clips'}).findAll('div',recursive=False)
    for episode in episodes:
        uri = 'mgid:arc:episode:spike.com:'+episode['id'].replace('episode_','')
        name = episode.find('img')['title']
        thumb = episode.find('img')['src'].split('?')[0]
        description = episode.findAll('p')[0].contents[0].strip().encode('utf-8')
        airDate = episode.findAll('p')[1].contents[2].strip().encode('utf-8')
        try:
            seasonepisode = episode.find(attrs={'class' : 'title'}).contents[2].replace('- Episode ','').strip()
            if 3 == len(seasonepisode):
                season = int(seasonepisode[:1])
                episode = int(seasonepisode[-2:])
            elif 4 == len(seasonepisode):
                season = int(seasonepisode[:2])
                episode = int(seasonepisode[-2:])
            if season <> 0 or episode <> 0:
                displayname = '%sx%s - %s' % (str(season),str(episode),name)
        except:
            print 'no season data'
            displayname = name
            season = 0
            episode = 0
        u = sys.argv[0]
        u += '?url="'+urllib.quote_plus(uri)+'"'
        u += '&mode="spike"'
        u += '&sitemode="play"'
        item=xbmcgui.ListItem(displayname, iconImage=thumb, thumbnailImage=thumb)
        item.setInfo( type="Video", infoLabels={ "Title":name,
                                                 "Season":season,
                                                 "Episode":episode,
                                                 "Plot":description,
                                                 "premiered":airDate
                                                 #"Duration":duration,
                                                 #"TVShowTitle":common.args.name
                                                 })
        item.setProperty('IsPlayable', 'true')
        xbmcplugin.addDirectoryItem(pluginhandle,url=u,listitem=item,isFolder=False)

def play(uri = common.args.url):
    configurl = 'http://media.mtvnservices.com/pmt/e1/players/mgid:arc:episode:spike.com:/context1/config.xml'
    configurl += '?uri=%s&type=network&ref=www.spike.com&geo=US&group=entertainment&site=spike.com' % uri
    configxml = common.getURL(configurl)
    tree=BeautifulStoneSoup(configxml, convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
    mrssurl = tree.find('feed').string.replace('{uri}',uri).replace('&amp;','&')
    mrssxml = common.getURL(mrssurl)
    tree=BeautifulStoneSoup(mrssxml, convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
    segmenturls = tree.findAll('media:content')
    stacked_url = 'stack://'
    for segment in segmenturls:
        surl = segment['url']
        videos = common.getURL(surl)
        videos = BeautifulStoneSoup(videos, convertEntities=BeautifulStoneSoup.HTML_ENTITIES).findAll('rendition')
        hbitrate = -1
        sbitrate = int(common.settings['quality'])
        for video in videos:
            bitrate = int(video['bitrate'])
            if bitrate > hbitrate and bitrate <= sbitrate:
                hbitrate = bitrate
                rtmpdata = video.find('src').string
                app = rtmpdata.split('://')[1].split('/')[1]
                rtmpdata = rtmpdata.split(app)
                rtmp = rtmpdata[0]
                playpath = rtmpdata[1]
                if '.mp4' in playpath:
                    playpath = 'mp4:'+playpath.replace('.mp4','')
                else:
                    playpath = playpath.replace('.flv','')
                swfUrl = "http://media.mtvnservices.com/player/prime/mediaplayerprime.1.6.0.swf"
                rtmpurl = rtmp + app +" playpath=" + playpath + " swfurl=" + swfUrl + " swfvfy=true"
        stacked_url += rtmpurl.replace(',',',,')+' , '
    stacked_url = stacked_url[:-3]
    item = xbmcgui.ListItem(path=stacked_url)
    xbmcplugin.setResolvedUrl(pluginhandle, True, item)

def playvideo(url = common.args.url):
    data=common.getURL(url)
    tree=BeautifulSoup(data, convertEntities=BeautifulSoup.HTML_ENTITIES)
    uri = tree.find('meta',attrs={'property':'og:video'})['content'].split('://')[1].split('/')[1]
    play(uri)


