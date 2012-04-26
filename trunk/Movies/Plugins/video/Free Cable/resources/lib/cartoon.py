import urllib, urllib2, re, md5, sys
import string, os, time, datetime
import xbmc, xbmcgui, xbmcplugin
from BeautifulSoup import BeautifulStoneSoup
import resources.lib._common as common

pluginhandle = int(sys.argv[1])

#CONFIGURATION_URL = 'http://www.cartoonnetwork.com/video/staged/CN2.configuration.xml'
#getAllEpisodes = 'http://cnvideosvc2.cartoonnetwork.com/svc/episodeSearch/getAllEpisodes'
getCollectionsFull = 'http://www.cartoonnetwork.com/cntv/mvpd/services/getCollectionsFull.do?id=49766'
getAllEpisodes = 'http://www.cartoonnetwork.com/cntv/mvpd/services/getAllEpisodes.do'
getCollectionByContentId = 'http://www.cartoonnetwork.com/cntv/mvpd/services/getCollectionByContentId.do'
cvpXML = 'http://www.cartoonnetwork.com/cntv/mvpd/services/cvpXML.do?id='
tokenurl = 'http://www.cartoonnetwork.com/cntv/mvpd/processors/services/token.do'



def masterlist():
        return rootlist(db=True)
                
def rootlist(db=False):
        xbmcplugin.setContent(pluginhandle, 'shows')
        xbmcplugin.addSortMethod(pluginhandle, xbmcplugin.SORT_METHOD_LABEL)
        html=common.getURL(getCollectionsFull)
        tree=BeautifulStoneSoup(html, convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
        collections = tree.findAll('collection')
        db_shows = []
        for collection in collections:
                subcollections = collection.findAll('subcollection')
                for subcollection in subcollections:
                        scid = subcollection['id']
                        name = subcollection.find('name').string.replace('- Full Episodes','')
                        if db==True:
                                db_shows.append((name,'cartoon', 'episodes',scid))
                        else:
                                common.addDirectory(name, 'cartoon', 'episodes', scid)
        if db==True:
                return db_shows

def episodes():
        cid = common.args.url
        showname = common.args.name
        xbmcplugin.setContent(pluginhandle, 'episodes')
        xbmcplugin.addSortMethod(pluginhandle, xbmcplugin.SORT_METHOD_NONE)
        url = getCollectionByContentId
        url += '?limit=200'
        url += '&offset=0'
        url += '&id='+cid
        html=common.getURL(url)
        tree=BeautifulStoneSoup(html, convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
        episodes = tree.findAll('episode')
        for episode in episodes:
                episodeId = episode['id']
                name = episode.find('title').string
                thumbnail = episode.find('thumbnailurl').string
                plot = episode.find('description').string
                duration = episode.find('duration').string
                try:
                    seasonNum = int(episode.find('seasonnumber').string)
                    print seasonNum
                except:
                    seasonNum = 0
                try:
                    episodeNum = int(episode.find('episodenumber').string)
                    print episodeNum
                except:
                    episodeNum = 0
                if episodeNum == 0 or seasonNum == 0:
                    print 'bad season or episode value'
                else:
                    name = str(seasonNum)+'x'+str(episodeNum)+' - '+name
                segments = episode.findAll('segment')
                if len(segments) == 0:
                    url = episodeId
                    mode = 'play'
                    addLink(name,url,mode,thumbnail,plot,seasonNum,episodeNum,showname,duration)
                else:
                    url = ''
                    for segment in segments:
                            url += segment['id']+'<segment>'
                    mode = 'playepisode' #PLAYEPISODE
                    addLink(name,url,mode,thumbnail,plot,seasonNum,episodeNum,showname,duration)

def addLink(name,url,mode,iconimage='',plot='',season=0,episode=0,showname='',duration=''):
        u = sys.argv[0]
        u += '?url="'+urllib.quote_plus(url)+'"'
        u += '&mode="cartoon"'
        u += '&sitemode="'+mode+'"'
        item=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        item.setInfo( type="Video", infoLabels={ "Title":name,
                                                 "Plot":plot,
                                                 "Season":season,
                                                 "Episode":episode,
                                                 "Duration":duration,
                                                 "TVShowTitle":showname
                                                 }) 
        item.setProperty('IsPlayable', 'true')
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,isFolder=False)

def getAUTH(aifp,window,tokentype,vid,filename):
        authUrl = 'http://www.tbs.com/processors/cvp/token.jsp'
        parameters = {'aifp' : aifp,
                      'window' : window,
                      'authTokenType' : tokentype,
                      'videoId' : vid,
                      'profile' : 'cartoon',
                      'path' : filename
                      }
        data = urllib.urlencode(parameters)
        request = urllib2.Request(authUrl, data)
        request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1')
        response = urllib2.urlopen(request)
        link = response.read(200000)
        response.close()
        print link
        return re.compile('<token>(.+?)</token>').findall(link)[0]

def GET_RTMP(vid):
        url = cvpXML+vid
        html=common.getURL(url)
        tree=BeautifulStoneSoup(html, convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
        print tree.prettify()
        sbitrate = int(common.settings['quality'])
        hbitrate = -1
        files = tree.findAll('file')
        for filenames in files:
                try: bitrate = int(filenames['bitrate'])
                except: bitrate = 1
                if bitrate > hbitrate and bitrate <= sbitrate:
                        hbitrate = bitrate
                        filename = filenames.string
        if 'http://' in filename:
            filename = filename
            return filename
        else:
            filename = filename[1:len(filename)-4]#.replace('mp4:','')
            serverDetails = tree.find('akamai')
            server = serverDetails.find('src').string.split('://')[1]
            #get auth
            tokentype = serverDetails.find('authtokentype').string
            window = serverDetails.find('window').string
            aifp = serverDetails.find('aifp').string
            
            auth=getAUTH(aifp,window,tokentype,vid,filename.replace('mp4:',''))      
            rtmp = 'rtmpe://'+server+'?'+auth+' playpath='+filename
            return rtmp

def playepisode():
        vids = common.args.url.split('<segment>')
        url = 'stack://'
        for vid in vids:
            if vid <> '':
                url += GET_RTMP(vid).replace(',',',,')+' , '
        url = url[:-3]
        item = xbmcgui.ListItem(path=url)
        return xbmcplugin.setResolvedUrl(pluginhandle, True, item)
    
def play():
        url = GET_RTMP(common.args.url)
        item = xbmcgui.ListItem(path=url)
        return xbmcplugin.setResolvedUrl(pluginhandle, True, item)
