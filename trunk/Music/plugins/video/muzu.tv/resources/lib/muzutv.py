'''
    muzu.tv XBMC Plugin
    Copyright (C) 2011 t0mm0

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

f    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
import Addon
import cookielib
import os
import re
import urllib, urllib2
import xbmcgui, sys

try:
    from xml.etree import ElementTree as ET
except:
    try:
        import elementtree.ElementTree as ET
    except:
        import ElementTree as ET
        
class MuzuTv:
    __BASE_URL = 'http://www.muzu.tv'
    __API_KEY  = Addon.get_setting('api')
    __GENRES   = [{'id': 'acoustic', 'name': Addon.get_string(30001)},
                  {'id': 'alternative', 'name': Addon.get_string(30002)},
                  {'id': 'blues', 'name': Addon.get_string(30003)},
                  {'id': 'celtic', 'name': Addon.get_string(30004)},
                  {'id': 'country', 'name': Addon.get_string(30005)},
                  {'id': 'dance', 'name': Addon.get_string(30006)},
                  {'id': 'electronic', 'name': Addon.get_string(30007)},
                  {'id': 'emo', 'name': Addon.get_string(30008)},
                  {'id': 'folk', 'name': Addon.get_string(30009)},
                  {'id': 'gospel', 'name': Addon.get_string(30010)},
                  {'id': 'hardcore', 'name': Addon.get_string(30011)},
                  {'id': 'hiphop', 'name': Addon.get_string(30012)},
                  {'id': 'indie', 'name': Addon.get_string(30013)},
                  {'id': 'jazz', 'name': Addon.get_string(30014)},
                  {'id': 'latin', 'name': Addon.get_string(30015)},
                  {'id': 'metal', 'name': Addon.get_string(30016)},
                  {'id': 'pop', 'name': Addon.get_string(30017)},
                  {'id': 'poppunk', 'name': Addon.get_string(30018)},
                  {'id': 'punk', 'name': Addon.get_string(30019)},
                  {'id': 'reggae', 'name': Addon.get_string(30020)},
                  {'id': 'rnb', 'name': Addon.get_string(30021)},
                  {'id': 'rock', 'name': Addon.get_string(30022)},
                  {'id': 'soul', 'name': Addon.get_string(30023)},
                  {'id': 'world', 'name': Addon.get_string(30024)},
                  {'id': 'other', 'name': Addon.get_string(30025)},                
                 ]

    def __init__(self):
          pass

    def check_API(self):

        if self.__API_KEY != '':
           return

        d = xbmcgui.Dialog()
        d.ok(Addon.get_string(30300),Addon.get_string(30303) + '\n' + Addon.get_string(30304),'','')
        Addon.addon.openSettings(sys.argv[ 0 ])

        self.__API_KEY = Addon.get_setting('api')
                            
    def get_genres(self):
        return self.__GENRES

    def get_chart(self, chart):
        videos = []
        html = self.__get_html('browse/charts/chart/%s' % chart, {'country': 'gb'})

        list   = html.split('<li class="chartItemList"')
        nItems = len(list)        

        for i in range(1, nItems):
            item = list[i]
            
            pos      = int(re.compile('.+?<div class="position"><span>(.+?)</span>').findall(item)[0])
            last_pos = '-'          

            try:
                move     = int(re.compile('.+?<div class="down_arrow"><span>(.+?)</span>').findall(item)[0])
                last_pos = pos - move
            except:
                pass

            try:
                move     = int(re.compile('.+?<div class="up_arrow"><span>(.+?)</span>').findall(item)[0])
                last_pos = pos + move
            except:
                pass

            try:
                video_id = re.compile('.+?<a href="/(.+?)/" itemprop="url"').findall(item)[0]                 
                video_id = video_id.rsplit('/', 1)[1]                
            except:
                video_id = ''

            try:
                thumb = re.compile('.+?<img src="(.+?)"  width').findall(item)[0]               
            except:
                thumb = ''

            if not thumb.startswith('http'):
                thumb = self.__BASE_URL + thumb

            try:
                #title = re.compile('.+?<span itemprop="name">(.+?)</span>').findall(item)[0]               
                title = re.compile('.+? itemprop="name">(.+?)</').findall(item)[0]               
            except:
                title = '' 

            try:
                artist = re.compile('.+? itemprop="byArtist">(.+?)</').findall(item)[0]               
            except:
                artist = ''  

            title = artist + ' : ' + title         

            videos.append({'title'   : title,
                           'pos'     : str(pos),
                           'last_pos': str(last_pos),
                           'asset_id': str(video_id),
                           'thumb'   : str(thumb)})

        return videos

    def get_chart_original(self, chart):
        videos = []
        html = self.__get_html('browse/charts/chart/%s' % chart, 
                               {'country': 'gb'})
        for v in re.finditer('mDown">.+?(\d+).+?mDown">.+?([\d*]+).+?<\/div>.+?(?:href=".+?\/(\d+)\/".+?)?src="(.+?)".+?alt="(.+?)"', html, re.DOTALL):
            pos, last_pos, video_id, thumb, title = v.groups()
            if not thumb.startswith('http'):
                thumb = self.__BASE_URL + thumb
            videos.append({'title': title,
                           'pos': pos,
                           'last_pos': last_pos,
                           'asset_id': video_id,
                           'thumb': thumb})
        return videos
        
    def jukebox(self, query, country='gb', jam=False):
        assets = {'artists': [], 'artist_ids': [], 'videos': []}
        if jam:
            json = self.__get_html('jukebox/generateMixTape', {'ai': jam})
        else:
            json = self.__get_html('jukebox/findArtistAssets', {'mySearch': query, 
                                                                'country': country})
        if json.startswith('[{"'):
            for a in re.finditer('\{.+?ArtistName":"(.+?)".+?ArtistIdentity":(\d+).+?\}', json):
                name, artist_id = a.groups()
                assets['artists'].append(name)
                assets['artist_ids'].append(artist_id)
        else:
            artist_id = ''
            for s in re.finditer('src="(.+?)".+?contentTitle-(\d+)" value="(.+?)".+?value="(.+?)".+?value="(.+?)"', json, re.DOTALL):
                thumb, asset_id, title, artist, artist_id = s.groups()
                assets['videos'].append({'asset_id': asset_id,
                                         'title': title,
                                         'artist': artist,
                                         'thumb': thumb})
            assets['artist_ids'].append(artist_id)
        return assets

    def list_playlists(self, category, country='gb'):
        playlists = []
        html = self.__get_html('browse/loadPlaylistsByCategory', 
                               {'ob': category, 'country': country})
        for p in re.finditer('data-id="(\d+)" data-network-id="(\d+)".+?title="(.*?)\|(.*?)".+?src="(.+?)"', html, re.DOTALL):
            playlist_id, network_id, name, network, thumb = p.groups()
            playlists.append({'playlist_id': playlist_id,
                              'network_id': network_id,
                              'name': unicode(name, 'utf8'),
                              'network': unicode(network, 'utf8'),
                              'thumb': thumb})
        return playlists

    def list_playlists_by_network(self, network_id, page = 0):
        playlists    = []
        res_per_page = 30
       
        xml = self.__get_html('%smusic-videos' % network_id, {'vo': str(page*res_per_page) })
        xml = xml.split('MUZU.TV <span>')[1]
        xml = xml.split('<div class="pages">')[0]

        list   = xml.split('<li>')
        nItems = len(list) 

        for i in range(1, nItems):
            item = list[i] 
            
            try:
                name = re.compile('.+?title="(.+?)"').findall(item)[0]
            except:
                name = ''
            
            try:
                pi = re.compile('.+?href="/(.+?)/"').findall(item)[0] 
                pi = pi.rsplit('/', 1)[1]                  
            except:
                pi = ''

            try:
                thumb = re.compile('.+?src="(.+?)"').findall(item)[0]               
            except:
                thumb = ''
          
            playlists.append({'name': name, 'id': pi, 'thumb': thumb})

        return playlists    

    def list_playlists_by_network_original(self, network_id):
        playlists = []
        xml = self.__get_html('player/networkVideos/%s' % network_id)
        for p in re.finditer('<channel name="(.+?)" id="(\d+)".+?thumbnailurl="(.+?)"', xml, re.DOTALL):
            name, pi, thumb = p.groups()
            playlists.append({'name': name, 'id': pi, 'thumb': thumb})
        return playlists
    
    def get_playlist(self, network_id, playlist_id):
        videos = []
        xml = self.__get_html('player/networkVideos/%s' % network_id)
        videos = self.__parse_playlist(xml, playlist_id)
        return videos
    
    def search(self, query):
        self.check_API()

        videos = []
        xml = self.__get_html('api/search', {'muzuid': self.__API_KEY,
                                             'mySearch': query,
                                             })
        return self.__parse_videos(xml)

    def browse_videos(self, genre, sort, page, res_per_page, days=0):
        self.check_API()

        queries = {'muzuid': self.__API_KEY,
                   'of': page * res_per_page,
                   'l': res_per_page,
                   'vd': days,
                   'ob': sort,
                   }
        if genre is not 'all':
            queries['g'] = genre
        xml = self.__get_html('api/browse', queries)
        return self.__parse_videos(xml)
            

    def browse_networks(self, genre, sort, page, days=0, country='gb'):
        networks = []
        queries = {'no': page * 32,
                   'vd': days,
                   'ob': sort,
                   'country': country,
                   }
        html = self.__get_html('channels/%s' % genre, queries)
        
        list   = html.split('<li class="browseThumbs">')
        nItems = len(list) 

        for i in range(1, nItems):
            item = list[i]           
            
            title      = re.compile('.+?title="(.+?)"').findall(item)[0]
            thumb      = re.compile('.+?src="(.+?)"').findall(item)[0]
            network_id = re.compile('.+?<a href="/(.+?)"').findall(item)[0]
            num_vids   = re.compile('.+?>(.+?) video').findall(item)[0]

            networks.append({'title': title, 'thumb': thumb, 'network_id': network_id, 'num_vids': num_vids})

        return networks


    def browse_networks_original(self, genre, sort, page, days=0, country='gb'):
        networks = []
        queries = {'no': page * 36,
                   'vd': days,
                   'ob': sort,
                   'country': country,
                   }
        html = self.__get_html('channels/%s' % genre, queries)
        for n in re.finditer('browseContentItemThumb.+?title="(.+?)".+?src="(.+?)".+?data-target-identity="(\d+)".+?(\d+) videos?<\/div>', html, re.DOTALL): 
            title, thumb, network_id, num_vids = n.groups()
            networks.append({'title': title, 'thumb': thumb, 
                             'network_id': network_id, 'num_vids': num_vids})
        return networks



        
    def resolve_stream(self, asset_id, hq=True):       
        #resolved = False
        vt = 1
        if hq:
            vt = 2

        response = self.__get_html('player/requestVideo', {'viewhash': 'GJirdtz3eCmA4ubE4zoQ1RXNKU', 'qv': '360', 'vt' : 'y', 'ai' : asset_id})
        url      = re.compile('.+?url":"(.+?)"').findall(response)[0]

        return Addon.unescape(url)

        #xml = self.__get_html('player/playAsset', {'assetId': asset_id, 'videoType': vt})
        #s = re.search('src="(.+?)"', xml)
        #if s:
        #    resolved = Addon.unescape(s.group(1))
        #return resolved


    def __parse_videos(self, xml):
        xml = xml.replace('media:',     '')
        xml = xml.replace('muzu:video', 'muzuvideo')
        xml = xml.replace('muzu:info',  'muzuinfo')

        videos  = []
        element = ET.fromstring(xml)

        for video in element.getiterator('item'):
            title       = video.findtext('title').strip()
            description = video.findtext('description').strip()

            thumbnail   = ''
            for t in video.findall('thumbnail'):
                height = int(t.attrib['height'])
                if height >= 100:                    
                    thumbnail = t.attrib['url'].strip()
                    break

            try:
                duration = int(video.find('content').attrib['duration'])
            except:
                duration = 0

            mv    = video.find('muzuvideo')
            mi    = mv.find('muzuinfo')
            id    = int(mi.attrib['id'])
            genre = mi.attrib['genre']

            artist = ''
            for c in video.findall('credit'):
                if c.attrib['role'] == 'artist':
                    artist = c.text.strip()
                    break

            videos.append({'duration'   : duration,
                           'asset_id'   : id,
                           'genre'      : genre,
                           'title'      : title,
                           'artist'     : artist,
                           'description': description,
                           'thumb'      : thumbnail,
                           })
        return videos


    def __parse_videos_original(self, xml):
        videos = []
        element = ET.fromstring(xml)
        for video in element.getiterator('video'):
            for img in video.find('thumbnails').getiterator('image'):
                if img.attrib['type'] =='6':
                    thumb = img.find('url').text
            videos.append({'duration': int(video.attrib['duration']),
                           'asset_id': int(video.attrib['id']),
                           'genre': video.attrib['genre'],
                           'title': video.findtext('title').strip(),
                           'artist': video.findtext('artistname').strip(),
                           'description': video.findtext('description').strip(),
                           'thumb': thumb.strip(),
                           })
        return videos

    def __parse_playlist(self, xml, playlist_id):
        videos = []
        element = ET.fromstring(xml)
        for channel in element.getiterator('channel'):
            if channel.attrib['id'] == playlist_id:
                for video in channel.getiterator('asset'):
                    videos.append({'duration': int(int(video.attrib['duration']) / 1000),
                                   'asset_id': int(video.attrib['id']),
                                   'genre': video.attrib['primarygenre'],
                                   'title': video.attrib['title'],
                                   'artist': video.attrib['artistname'],
                                   'description': video.attrib['description'],
                                   'thumb': video.attrib['thumbnailurl'],
                                   })
        return videos

    def __build_url(self, path, queries={}):
        query = Addon.build_query(queries)
        return '%s/%s?%s' % (self.__BASE_URL, path, query) 

    def __fetch(self, url, form_data=False):
        if form_data:
            Addon.log('posting: %s %s' % (url, str(form_data)))
            req = urllib2.Request(url, form_data)
        else:
            Addon.log('getting: ' + url)
            req = url

        try:
            response = urllib2.urlopen(url)
            return response
        except urllib2.URLError, e:
            Addon.log(str(e), True)
            return False
        
    def __get_html(self, path, queries={}):
        html = False
        url = self.__build_url(path, queries) 

        #print "*******************************"
        #url = 'http://www.muzu.tv/player/requestVideo?ni=200290&country=gb&playlistId=0&cn=6&viewhash=GJirdtz3eCmA4ubE4zoQ1RXNKU&qv=360&device=web%2Eonsite&hostName=http%3A%2F%2Fwww%2Emuzu%2Etv&networkVersion=1334919670&tm=0&vt=y&areaName=channel&ai=1222359'
        #url = 'http://www.muzu.tv/player/requestVideo?viewhash=GJirdtz3eCmA4ubE4zoQ1RXNKU&qv=360&ai=1119519'
        #url = 'http://www.muzu.tv/player/getPlayer/a/200290/vidId=1222359&la=n'
        #print url

        response = self.__fetch(url)
        if response:
            html = response.read()
        else:
            html = False
        
        return html

    def __login(self):
        Addon.log('logging in')
        policy = cookielib.DefaultCookiePolicy(rfc2965=True, strict_rfc2965_unverifiable=False)    
        self.cj = cookielib.MozillaCookieJar(self.cookie_file)
        self.cj.set_policy(policy)

        if os.access(self.cookie_file, os.F_OK):
            self.cj.load(ignore_discard=True)

        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        urllib2.install_opener(opener)
        self.cj.clear_session_cookies()
        
        url = self.__build_url('cgi-bin/oc/manage.cgi')
        form_data = urllib.urlencode({'a': 'do_login', 
                                      'force_direct': '0',
                                      'manage_proper': '1',
                                      'input_username': self.user,
                                      'input_password': self.password
                                      })
        response = self.__fetch(self.__LOGIN_URL, form_data)
        self.cj.save(ignore_discard=True)

