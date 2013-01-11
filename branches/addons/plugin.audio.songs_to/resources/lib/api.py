#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#     Copyright (C) 2012 sphere
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#

import re
import simplejson as json
from urllib import urlencode
from urllib2 import urlopen, Request, HTTPError, URLError


MAIN_URL = 'http://songs.to'
PLAY_URL = MAIN_URL + '/data.php?id=%s'

DEFAULT_LANGUAGE = 'de'


class NetworkError(Exception):
    pass


class SongsApi():

    USER_AGENT = 'XBMC SongsApi v0.1'

    def __init__(self, language=None):
        if language in ('de', 'en'):
            self.language = language
        else:
            self.language = DEFAULT_LANGUAGE

    def get_chart_types(self):
        path = '/json/app.php?f=charts&lang=%s' % self.language
        return self.__api_call(path)

    def get_charts(self, chart_type):
        path = '/json/songlist.php?charts=%s' % chart_type
        return self.__format_charts(self.__api_call(path), chart_type)

    def get_top_songs(self):
        path = '/json/songlist.php?top=all'
        return self.__format_songs(self.__api_call(path))

    def get_new_songs(self):
        path = '/json/songlist.php?g='
        return self.__format_songs(self.__api_call(path))

    def get_similar_songs(self, song_id):
        path = '/json/songlist.php?record=%s' % song_id
        return self.__format_songs(self.__api_call(path))

    def get_songs(self, album=None, artist=None, title=None):
        if not album and not artist and not title:
            raise AttributeError('Need at least one parameter')
        path = '/json/songlist.php?quickplay=1'
        data_dict = {
            'data': [{
                'artist': artist or '',
                'album': album or '',
                'title': title or ''
            }]
        }
        post_data = {'data': json.dumps(data_dict)}
        return self.__format_songs(self.__api_call(path, post_data))

    def search_songs(self, field, keyword):
        if field == 'all' or field not in ('title', 'album', 'artist'):
            field = ''
        qs = {'keyword': keyword, 'col': field}
        path = '/json/songlist.php?%s' % urlencode(qs)
        return self.__format_songs(self.__api_call(path))

    @staticmethod
    def get_song_url(song_id):
        return PLAY_URL % song_id

    @staticmethod
    def __format_songs(songs):

        def __cover(cover):
            if cover:
                return '%s/covers/%s' % (MAIN_URL, cover)

        def __date(date_str):
            if date_str:
                y, m, d = date_str.split()[0].split('-')
                return '%s.%s.%s' % (d, m, y)

        return [{
            'id': song['hash'],
            'title': song['title'],
            'artist': song['artist'],
            'album': song['album'],
            'genre': song['genre'],
            'playtime': song['playtime'],
            'bitrate': song['bitrate'],
            'track_nr': song['track_nr'],
            'disc_nr': song['disc_nr'],
            'thumb': __cover(song['cover']),
            'date': __date(song['entrydate']),
        } for song in songs]

    @staticmethod
    def __format_charts(charts, chart_type):

        def __cover(cover, position):
            if cover:
                return '%s/charts/%s-%03d.%s' % (
                    MAIN_URL, chart_type, int(position), cover
                )

        return [{
            'name1': chart['name1'],
            'name2': chart['name2'],
            'position': chart['position'],
            'thumb': __cover(chart['cover'], chart['position']),
            'info': chart['info'],
        } for chart in charts]

    def __api_call(self, path, post_data=None):
        url = MAIN_URL + path
        if post_data:
            log('Using POST: %s' % repr(post_data))
            req = Request(url, urlencode(post_data))
        else:
            req = Request(url)
        req.add_header('User Agent', self.USER_AGENT)
        log('Opening URL: %s' % url)
        try:
            response = urlopen(req).read()
        except URLError, error:
            log('NetworkError: %s' % error)
            raise NetworkError(error)
        log('got %d bytes' % len(response))
        json_data = json.loads(response)
        if json_data.get('error'):
            err = json_data['error']
            log('Error: %s' % repr(err))
        return json_data.get('data', [])


def log(msg):
    print '[Songs API]: %s' % msg
