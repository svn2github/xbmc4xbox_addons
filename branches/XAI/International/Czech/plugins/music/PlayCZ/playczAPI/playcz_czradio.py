""" PlayCZ plugin API module for browsing and playing online czech radio
    streams from www.play.cz 
"""

import xbmc
import xbmcgui
import xbmcplugin
import urllib
import urllib2
import re

# Constants 
PLAYCZ_URL = "http://www.play.cz/"
LIST_URL = "http://www.play.cz/radia-online"
LABEL2_TEXT = 'www.play.cz'

# compiled regular expressions 
LIST_RE = re.compile('<h1>Radia online</h1>[^<]*<ul>(.*?)</ul>', re.M | re.S)
ITEM_RE = re.compile('<li>.*?</li>', re.M | re.S)

IFMT_RE = re.compile('''
              <h4><a[ ]+href="/(?P<link_path>.*?)"              # detail page url
                .*?>(?P<title>.*?)</a>                          # radio title
                .*?<img[ ]+src="/(?P<icon_path>.*?)"            # icon image path
                .*?<span[ ]+class="meta">(?P<genre>.*?)</span>  # genre text
            ''', re.M | re.S | re.X)

PLAY_RE = re.compile('''
              'http://www.play.cz/listen/listen.php\?
                    sh=(?P<sh>[^&'"]+)&                         # "sh" argument value in js-function PlayRadio
                .*?href="javascript:PlayRadio\(
                    (?P<bitrate>\d+),\s*                        # "bitrate" argument in PlayRadio call
                    '(?P<stype>\w+)'\)                          # "stype" argument in PlayRadio call
            ''',  re.M | re.S | re.X)

DETAIL_RE = re.compile('''
                <tr><th>Styl:</td>
                    <td>(?P<genre>[^<]*)</td></tr>              # genre text
                .*?<div[ ]+id="contact">
                    .*?<img[ ]+src="/(?P<icon_path>[^"]+)"        # icon path
                    \s*alt="(?P<title>[^"]+)"                   # radio title 
            ''',  re.M | re.S | re.X)

PLAYER_RE = re.compile('''
                <OBJECT[ ]ID="wmpplayer"[^>]*>
                    <PARAM
                        [ ]+NAME="URL"
                        [ ]+VALUE="(?P<url>[^"]+)"          # playlist URL from "wmpplayer" object
            ''',  re.M | re.S | re.X)

ASX_RE = re.compile('''
                <ASX.*?> .*?
                    <Ref \s+ href\s*=\s*"(?P<url>[^"]+)"    # stream URL from ASX file
            ''',  re.M | re.S | re.X | re.I)

M3U_RE = re.compile('^(?P<url>http://.+)$', re.M | re.I)

PLAYWIN_URL_MASK = 'http://www.play.cz/listen/listen.php?sh=%(sh)s&bitrate=%(bitrate)s&stype=%(stype)s'


class List:
    """ PlayCZ plugin class for listing czech radio online items """

    def __init__(self, baseurl, handle):
        """ constructor """
        self.baseurl = baseurl
        self.handle  = int(handle)

        self.all_items()


    def get_czradio_list(self):
        """ Download and parse cz-radio list page """
        response = urllib2.urlopen(LIST_URL)
        content = response.read()
        m = LIST_RE.search(content)
        if not m:
            raise Exception("Cannot parse page: %s" % LIST_URL)

        return ITEM_RE.findall( m.group(1) )
        

    def parse_list_item(self, itemstr):
        """ Parse content of cz-radion list item string 
            it returns (link_path, info)
        """
        m = IFMT_RE.search(itemstr)
        if not m:
            raise Exception("Cannot parse itemstr: %s" % repr(itemstr))
        
        link_path = m.group('link_path')
        icon_url  = PLAYCZ_URL + m.group('icon_path')
        info = {
                'title': m.group('title'),
                'genre': m.group('genre'),
                'thumb': icon_url,
            }
        return (link_path, icon_url, info)


    def add_item(self, link_path, icon_url, info):
        """ Add item to plugin output list """
        label = info['title']
        url = self.baseurl + '?czradio=' + urllib.quote_plus(link_path)
        listitem = xbmcgui.ListItem(label, LABEL2_TEXT, thumbnailImage=icon_url)
        listitem.setInfo(type='music', infoLabels=info)
        xbmcplugin.addDirectoryItem(self.handle, url, listitem, totalItems=self.totalItems)


    def all_items(self):
        """ Add all items to plugin output list """
        items = self.get_czradio_list()
        self.totalItems = len(items)

        for itemstr in items:
            data = self.parse_list_item(itemstr)
            self.add_item( *data )

        xbmcplugin.endOfDirectory(self.handle)




class Play:
    """ PlayCZ plugin class for plaing czech radio online item """

    def __init__(self, baseurl, handle, path):
        """ constructor """
        self.baseurl = baseurl
        self.handle  = int(handle)
        
        self.play_czradio(path)


    def play_czradio(self, path):
        """ Play czech radio station from giver path """
        
        # show progress dialog 
        pd = xbmcgui.DialogProgress()
        pd.create( xbmc.getLocalizedString(30050) )
        pd.update(0, xbmc.getLocalizedString(30051))
        if pd.iscanceled():
            return

        # get details page 
        detail_url = PLAYCZ_URL + path
        xbmc.log('[PlayCZ] get_details(%s)' % repr(detail_url), xbmc.LOGDEBUG)
        (window_url, icon_url, info) = self.get_details(detail_url)

        # update progress dialog 
        pd.update(33, xbmc.getLocalizedString(30052))
        if pd.iscanceled():
            return

        # get player window -> search for playlist url 
        xbmc.log('[PlayCZ] get_playlist_url(%s)' % repr(window_url), xbmc.LOGDEBUG)
        playlist_url = self.get_playlist_url(window_url)

        # update progress dialog 
        pd.update(66, xbmc.getLocalizedString(30053))
        if pd.iscanceled():
            return

        # download playlist and get stream url 
        xbmc.log('[PlayCZ] get_stream_url(%s)' % repr(playlist_url), xbmc.LOGDEBUG)
        stream_url = self.get_stream_url(playlist_url)

        # update progress dialog 
        pd.update(100, xbmc.getLocalizedString(30054))
        if pd.iscanceled():
            return

        # play stream URL 
        xbmc.log('[PlayCZ] play_stream(%s, %s, %s)' 
                    % (repr(stream_url), repr(icon_url), repr(info)), 
                xbmc.LOGDEBUG)
        self.play_stream(stream_url, icon_url, info)
        pd.close()


    def get_details(self, detail_url):
        """ Download and parse cz-radio details page on given url 
            it returns (window_url, icon_url, info)
        """
        response = urllib2.urlopen(detail_url)
        content = response.read()

        m = PLAY_RE.search(content)
        if not m:
            raise "PlayRadio link not found on %s" % detail_url

        window_url = PLAYWIN_URL_MASK % m.groupdict()

        # Search for title / genre / icon url 
        m = DETAIL_RE.search(content)
        if not m:
            raise "Cannot parse detail page on %s" % detail_url

        icon_url = PLAYCZ_URL + m.group('icon_path')
        info = {
            'title': m.group('title'),
            'genre': m.group('genre'),
            'icon':  icon_url
        }
        return (window_url, icon_url, info)


    def get_playlist_url(self, window_url):
        """ Download and parse "play window" page 
            and return playlist file URL 
        """
        response = urllib2.urlopen(window_url)
        content = response.read()

        # search for "wmpplayer" object
        m = PLAYER_RE.search(content)
        if not m:
            raise "OBJECT wmpplayer not found on %s" % window_url

        return m.group('url')


    def get_stream_url(self, playlist_url):
        """ Download and parse playlist file and return
            contained radio stream URL
        """
        response = urllib2.urlopen(playlist_url)
        content = response.read()

        m = ASX_RE.search(content)
        if not m:
            m = M3U_RE.search(content)
        if not m:
            raise "Cannot parse playlist file on %s" % playlist_url
        return m.group('url')


    def play_stream(self, stream_url, icon_url, info):
        """ Play radio stream in  XMBC player """
        listitem = xbmcgui.ListItem(info['title'], LABEL2_TEXT, iconImage=icon_url)
        listitem.setInfo(type='music', infoLabels=info)

        player = xbmc.Player( xbmc.PLAYER_CORE_AUTO )
        player.play(stream_url, listitem)


