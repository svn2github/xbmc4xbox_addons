import xbmc
import xbmcgui
import xbmcplugin
import urllib
import urllib2
import httplib
import sys
import os
import re

from BeautifulSoup import BeautifulStoneSoup
from BeautifulSoup import BeautifulSoup
import demjson
import pyamf

from pyamf import remoting, amf3, util

import resources.lib._common as common

pluginhandle = int(sys.argv[1])
BASE_URL = 'http://nicktoons.nick.com/ajax/videos/all-videos/?sort=date+desc&start=0&page=1&updateDropdown=true&viewType=collectionAll&type=fullEpisodeItem'
BASE = 'http://nicktoons.nick.com'

def masterlist():
    return rootlist(db=True)

def rootlist(db=False):
    xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
    data = common.getURL(BASE_URL)
    tree=BeautifulSoup(data, convertEntities=BeautifulSoup.HTML_ENTITIES)
    db_shows = []
    shows=tree.find('select',attrs={'id':'dropdown-by-show'}).findAll('option')
    for show in shows:
        name = show.string
        if name <> 'All Shows':
            url = show['value']
            if db==True:
                db_shows.append((name, 'nicktoons', 'episodes', url)  )
            else:
                common.addShow(name, 'nicktoons', 'episodes', url)        
    if db==True:
        return db_shows
    else:
        common.setView('tvshows')

def episodes():
    url = 'http://nicktoons.nick.com/ajax/videos/all-videos/'+common.args.url
    url += '?sort=date+desc&start=0&page=1&viewType=collectionAll&type=fullEpisodeItem'
    data = common.getURL(url)
    tree=BeautifulSoup(data, convertEntities=BeautifulSoup.HTML_ENTITIES)
    episodes=tree.find('ul',attrs={'class':'large-grid-list clearfix'}).findAll('li',recursive=False)
    for episode in episodes:
        h4link=episode.find('h4').find('a')
        name = h4link.string
        url = BASE + h4link['href']
        thumb = episode.find('img')['src'].split('?')[0]
        plot = episode.find('p',attrs={'class':'description text-small color-light'}).string
        u = sys.argv[0]
        u += '?url="'+urllib.quote_plus(url)+'"'
        u += '&mode="nicktoons"'
        u += '&sitemode="playvideo"'
        infoLabels={ "Title":name,
                     #"Duration":duration,
                     #"Season":0,
                     #"Episode":0,
                     "Plot":str(plot),
                     "TVShowTitle":common.args.name
                     }
        common.addVideo(u,name,thumb,infoLabels=infoLabels)
    common.setView('episodes')
def playuri(uri = common.args.url,referer='http://nicktoons.nick.com'):
    mtvn = 'http://media.nick.com/'+uri 
    swfUrl = common.getRedirect(mtvn,referer=referer)
    configurl = urllib.unquote_plus(swfUrl.split('CONFIG_URL=')[1].split('&')[0]).strip()
    configxml = common.getURL(configurl,referer=mtvn)
    tree=BeautifulStoneSoup(configxml, convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
    mrssurl = tree.find('feed').string.replace('{uri}',uri).replace('&amp;','&').replace('{type}','network').replace('mode=episode','mode=clip')
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
                rtmpurl = rtmpdata + " swfurl=" + swfUrl.split('?')[0] +" pageUrl=" + referer + " swfvfy=true"
        stacked_url += rtmpurl.replace(',',',,')+' , '
    stacked_url = stacked_url[:-3]
    item = xbmcgui.ListItem(path=stacked_url)
    xbmcplugin.setResolvedUrl(pluginhandle, True, item)

def playvideo(url = common.args.url):
    data=common.getURL(url)
    try:
        uri = re.compile('<meta content="http://media.nick.com/(.+?)" itemprop="embedURL"/>').findall(data)[0]
    except:
        uri=re.compile("NICK.unlock.uri = '(.+?)';").findall(data)[0]
    playuri(uri,referer=url)