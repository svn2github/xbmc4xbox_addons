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
BASE_URL = 'http://www.thewb.com/shows/full-episodes'
BASE = 'http://www.thewb.com'

def masterlist():
    return rootlist(db=True)

def rootlist(db=False):
    xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
    data = common.getURL(BASE_URL)
    tree=BeautifulSoup(data, convertEntities=BeautifulSoup.HTML_ENTITIES)
    shows=tree.find('div',attrs={'id':'show-directory'}).findAll('li')
    for show in shows:
        link=show.find('a')
        name = link.contents[0].strip()
        url = BASE+link['href']
        common.addDirectory(name, 'thewb', 'fullepisodes', url)
        
def fullepisodes(url=common.args.url):
    xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
    data = common.getURL(url)
    tree=BeautifulSoup(data, convertEntities=BeautifulSoup.HTML_ENTITIES)
    episodes=tree.find('div',attrs={'id':'full_ep_car'}).findAll('div',attrs={'id':True,'class':True})
    for episode in episodes:
        print episode.prettify()
        links=episode.findAll('a')
        url=BASE+links[1]['href']
        showname = links[1].find('strong').string
        name = links[0].find('img')['title'].replace(showname,'').strip().encode('utf-8')
        thumb=links[0].find('img')['src']
        plot=episode.findAll('p')[1].string
        seasonEpisode = episode.find('span',attrs={'class':'type'}).string
        seasonSplit = seasonEpisode.split(': Ep. ')
        season = int(seasonSplit[0].replace('Season','').strip())
        episodeSplit = seasonSplit[1].split(' ')
        episode = int(episodeSplit[0])
        duration = episodeSplit[1].replace('(','').replace(')','').strip()
        displayname = '%sx%s - %s' % (str(season),str(episode),name)
        u = sys.argv[0]
        u += '?url="'+urllib.quote_plus(url)+'"'
        u += '&mode="thewb"'
        u += '&sitemode="play"'
        item=xbmcgui.ListItem(displayname, iconImage=thumb, thumbnailImage=thumb)
        item.setInfo( type="Video", infoLabels={ "Title":name,
                                                 "Duration":duration,
                                                 "Season":season,
                                                 "Episode":episode,
                                                 "Plot":plot,
                                                 "TVShowTitle":showname
                                                 })
        item.setProperty('IsPlayable', 'true')
        xbmcplugin.addDirectoryItem(pluginhandle,url=u,listitem=item,isFolder=False)

def play(url=common.args.url):
    jsonurl = 'http://metaframe.digitalsmiths.tv/v2/WBtv/assets/'+url.split('/')[-1]+'/partner/146?format=json'
    data = common.getURL(jsonurl)
    rtmp = demjson.decode(data)['videos']['limelight700']['uri']
    rtmpsplit = rtmp.split('mp4:')
    rtmp = rtmpsplit[0]+' playpath=mp4:'+rtmpsplit[1]
    item = xbmcgui.ListItem(path=rtmp)
    return xbmcplugin.setResolvedUrl(pluginhandle, True, item)