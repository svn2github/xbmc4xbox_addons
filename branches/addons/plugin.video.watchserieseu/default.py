"""
    Watchseries.eu XBMC Video Addon
    Copyright (C) 2011 rogerThis
    Copyright (C) 2012 mscreations

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import urllib, urllib2
import re, string
from t0mm0.common.addon import Addon
from t0mm0.common.net import Net
import urlresolver
import os

addon = Addon('plugin.video.watchserieseu', sys.argv)
xaddon = xbmcaddon.Addon(id='plugin.video.watchserieseu')
net = Net()
profile_path = addon.get_profile()
##### Queries ##########
play = addon.queries.get('play', None)
mode = addon.queries['mode']
section = addon.queries.get('section', None)
url = addon.queries.get('url', None)
imdb_id = addon.queries.get('imdb_id', None)

print 'Mode: ' + str(mode)
print 'Play: ' + str(play)
print 'URL: ' + str(url)
print 'Section: ' + str(section)
print 'IMDB ID: ' + str(imdb_id)

################### Global Constants #################################

main_url = 'http://watchseries.eu'
episode_url = main_url + 'episodes.php?e=%s&c=%s'
addon_path = xaddon.getAddonInfo('path')
icon_path = addon_path + "/icons/"
GENRES = ['action', 'adventure', 'comedy', 'drama', 'family', 'fantasy', 'documentaries', 
          'cooking', 'lifestyle', 'cartoons', 'reality-TV']

######################################################################

if not os.path.isdir(profile_path):
     os.mkdir(profile_path)

### Create A-Z Menu
def AZ_Menu(type, url):
     
    addon.add_directory({'mode': type,
                         'url': main_url + url % '09',
                         'section': section,
                         'letter': '09'},{'title': '09'},
                         img='')
    for l in string.uppercase:
        addon.add_directory({'mode': type,
                             'url': main_url + url % l,
                             'section': section,
                             'letter': l}, {'title': l},
                             img='')

                             
def get_latest(url):
    html = net.http_GET(url).content
    
    match = re.compile('\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<li><a href="(.+?)" title=".+?">(.+?)</a></li>',re.DOTALL).findall(html)
    total = len(match)
    for link, title in match:
        r = re.search('(.+?).html',link,re.DOTALL)#.group(1)
        #print r
        #match = re.compile('(.+?).html',re.DOTALL).findall(link)[0]
        if r:
            addon.add_directory({'mode': 'hosting_sites', 'url': link, 'section': 'tv'}, {'title': title}, total_items=total)
        else:
            addon.add_directory({'mode': 'tvepisodes', 'url': link, 'section': 'tv'}, {'title': title}, total_items=total)

def BrowseByGenreMenu(url): 
    print 'Browse by genres screen'
    for g in GENRES:
        addon.add_directory({'mode': 'genresList', 'url': url+g, 'section': 'tv'}, {'title': g})
        
        
        
def get_video_list(url):
    print 'get_video_list'
    html = net.http_GET(url).content
    match = re.compile('\t <li><a href="(.+?)" title="(.+?)">.+?<span class="epnum">(.+?)</span></a></li>',re.DOTALL).findall(html)
    #print match
    total = len(match)
    for link, title, amount in match:
        addon.add_directory({'mode': 'tvseasons', 'url': link, 'section': 'tv'}, {'title': title + ' (' + amount + ')'}, img='', total_items=total)

def get_genres_list(url):
    print 'get_genres_list'
    html = net.http_GET(url).content
 
    match = re.compile('\t\t\t <li><a href="(.+?)\n" title="Watch .+? Online">(.+?)</a></li>',re.DOTALL).findall(html)
    #print match
    total = len(match)
    for link, title in match:
        addon.add_directory({'mode': 'tvseasons', 'url': link, 'section': 'tv'}, {'title': title}, img='', total_items=total)
        
def get_schedule_date(url):
    print 'get_schedule_list'
    html = net.http_GET(url).content
 
    match = re.compile('<li><a href="http://watchseries.eu/tvschedule/(.+?)">(.+?)</a></li>',re.DOTALL).findall(html)
    #print match
    total = len(match)
    for link, title in match:
        addon.add_directory({'mode': 'schedule_list', 'url': main_url+'/tvschedule/'+link, 'section': 'tv'}, {'title': title}, img='', total_items=total)

def get_schedule_list(url):
    print 'get_schedule_list'
    html = net.http_GET(url).content
 
    match = re.compile('\t \t\t\t\t\t\t\t\t\t\t\t\t\t <a href="(.+?)>(.+?)</a>\r\n',re.DOTALL).findall(html)
    #print match
    total = len(match)
    for link, title in match:
        #print link
        match = re.compile('(.+?)"',re.DOTALL).findall(link)[0]
        if match == '#':
            addon.add_directory({'mode': 'schedule_none', 'url': main_url+'/tvschedule/'+match, 'section': 'tv'}, {'title': title}, img='', total_items=total)
        else:
            addon.add_directory({'mode': 'tvseasons', 'url': match, 'section': 'tv'}, {'title': title}, img='', total_items=total)


if mode == 'main':
    print 'main' 
    addon.add_directory({'mode': 'tvaz', 'section': 'tv'}, {'title':'A-Z'}, img='')
    addon.add_directory({'mode': 'latest', 'url': main_url + '/latest', 'section': 'tv'}, {'title': 'Newest Episodes Added'})
    addon.add_directory({'mode': 'popular', 'url': main_url + '/new', 'section': 'tv'}, {'title': 'This Weeks Popular Episodes'})
    addon.add_directory({'mode': 'schedule', 'url': main_url + '/tvschedule', 'section': 'tv'}, {'title': 'TV Schedule'})
    addon.add_directory({'mode': 'genres', 'url': main_url +'/genres/', 'section': 'tv'}, {'title': 'TV Shows Genres'})

elif mode == 'tvaz':
    AZ_Menu('tvseriesaz','/letters/%s')
elif mode == 'tvseriesaz':
    get_video_list(url)
elif mode == 'latest':
    get_latest(url)
elif mode == 'popular':
    get_latest(url)
elif mode == 'schedule':
    get_schedule_date(url)
elif mode == 'schedule_list':
    get_schedule_list(url)
elif mode == 'genres':
    BrowseByGenreMenu(url)
elif mode == 'genresList':
    get_genres_list(url)

elif mode == 'tvseasons':
    print 'tvseasons'
    html = net.http_GET(url).content
    
    match = re.compile('<h2 class="lists"><a href="(.+?)">(.+?)  (.+?)</a> - ').findall(html)
    seasons = re.compile('<h2 class="lists"><a href=".+?">Season ([0-9]+)  .+?</a> -').findall(html)
    num = 0
    for link, season, episodes in match:
        addon.add_directory({'mode': 'tvepisodes', 'url': link, 'section': 'tvshows', 'imdb_id': imdb_id, 'season': num + 1}, {'title': season + ' ' + episodes}, total_items=len(match))
        num += 1
    

elif mode == 'tvepisodes':
    print 'tvepisodes'
    html = net.http_GET(url).content
    match = re.compile('<li><a href="\..(.+?)"><span class="">.+?. Episode (.+?)&nbsp;(.+?)/span><span class="epnum">(.+?)</span></a>',re.DOTALL).findall(html)
    num = 0
    for url, episode, name, aired in match:
        try:
            name1 = re.compile('&nbsp;&nbsp;(.+?)<',re.DOTALL).findall(name)[0]
        except: 
            name1 = ' '
        #name2 = name1.encode("utf-8")
        #print name2
        addon.add_directory({'mode': 'hosting_sites', 'url': main_url + url, 'section': 'tvshows', 'imdb_id': imdb_id, 'season': num + 1} ,{'title':episode+' '+name1+' ('+aired+')'}, total_items=len(match))

elif mode == 'hosting_sites':
    try:
        addon.log_debug('fetching %s' % url)
        match = re.compile('-(.+?).html').findall(url)[0]
        html = net.http_GET(url).content
        #print 'HTML: ' + html
        net.save_cookies(profile_path+'cookie.txt')
        html = net.http_GET(main_url+'/getlinks.php?q='+match+'&domain=load').content
    except urllib2.URLError, e:
        html = ''
            
    #find all sources and their info
    sources = []
    for s in re.finditer('<div class="site">\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t(.+?)\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</div>\r\n\t\t\t\t\t\t\t\t\t\t\t\t<div class="siteparts">\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<a href="..(.+?)" target="_blank"', 
                         html, re.DOTALL):
        print s.groups()
        title, url = s.groups()
        
        if urlresolver.HostedMediaFile(host=title, media_id='xxx'):
            addon.add_directory({'mode': 'play', 'url': main_url+url, 'section': 'tvshows'} ,{'title':title})
            
elif mode == 'play':
    url = addon.queries['url']
    net.set_cookies(profile_path+'cookie.txt')
    html = net.http_GET(url).content
    match = re.compile('\r\n\t\t\t\t<a href="(.+?)" class="myButton">').findall(html)[0]

    print 'MATCH: ' + match

    post_url = net.http_GET(match).get_url()
    print 'POST URL: ' + post_url
    
    stream_url = urlresolver.HostedMediaFile(post_url).resolve()
    print 'STREAM URL: ' + str(stream_url)
    ok=xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play(stream_url)
    addon.add_directory({'mode': 'play', 'url': url, 'section': 'tv'}, {'title': 'Play Again'})

elif mode == 'resolver_settings':
    urlresolver.display_settings()

if not play:
    addon.end_of_directory()
