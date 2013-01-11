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

from xbmcswift2 import Plugin, listitem
from resources.lib import playlists
from resources.lib.api import SongsApi, NetworkError

CONTEXT_MENU_ENABLED = True

STRINGS = {
    "top_500_songs": 30001,
    "chart_types": 30002,
    "search_all": 30003,
    "search_title": 30004,
    "search_artist": 30005,
    "search_album": 30006,
    "bitrate": 30007,
    "date": 30008,
    "all_songs_from": 30009,
    "all_songs_in_album": 30010,
    "show_info": 30011,
    "add_to_playlist": 30012,
    "my_playlists": 30013,
    "new_songs": 30014,
    "show_similar_songs": 30015,
}

plugin = Plugin(addon_id='plugin.audio.songs_to')
plugin.register_module(playlists.playlists, '/playlists')
api = SongsApi()


@plugin.route('/')
def show_root_menu():
    items = [
        {'label': _('top_500_songs'),
         'path': plugin.url_for('show_top_500_songs')},
        {'label': _('chart_types'),
         'path': plugin.url_for('show_chart_types')},
        {'label': _('my_playlists'),
         'path': plugin.url_for('playlists.show_playlists')},
        {'label': _('search_all'),
         'path': plugin.url_for('search', field='all')},
        {'label': _('search_title'),
         'path': plugin.url_for('search', field='title')},
        {'label': _('search_artist'),
         'path': plugin.url_for('search', field='artist')},
        {'label': _('search_album'),
         'path': plugin.url_for('search', field='album')},
        {'label': _('new_songs'),
         'path': plugin.url_for('show_new_songs')},
    ]
    return plugin.finish(items)


@plugin.route('/charts/')
def show_chart_types():
    items = []
    for chart_type in api.get_chart_types():
        if chart_type['is_album']:
            endpoint = 'show_album_charts'
        else:
            endpoint = 'show_charts'
        items.append({
            'label': chart_type['title'],
            'path': plugin.url_for(
                endpoint=endpoint,
                chart_type=chart_type['type']
            ),
        })
    return plugin.finish(items)


@plugin.route('/charts/albums/<chart_type>/')
def show_album_charts(chart_type):
    items = []
    for chart in api.get_charts(chart_type):
        artist = chart['name1']
        album = chart['name2']
        items.append({
            'label': '%02d. %s - %s' % (
                int(chart['position']), artist, album
            ),
            'thumbnail': chart['thumb'],
            'path': plugin.url_for(
                endpoint='show_songs',
                artist=artist.encode('ascii', 'replace'),
                album=album.encode('ascii', 'replace'),
            )
        })
    return plugin.finish(items)


@plugin.route('/charts/singles/<chart_type>/')
def show_charts(chart_type):
    items = []
    for chart in api.get_charts(chart_type):
        artist = chart['name1']
        title = chart['name2']
        items.append({
            'label': '%02d. %s - %s' % (
                int(chart['position']), artist, title
            ),
            'thumbnail': chart['thumb'],
            'info': {
                'artist': artist,
                'title': title
            },
            'is_playable': True,
            'path': plugin.url_for(
                endpoint='play_single',
                artist=artist.encode('ascii', 'replace'),
                title=title.encode('ascii', 'replace'),
            )
        })
    return plugin.finish(items)


@plugin.route('/songs/top500/')
def show_top_500_songs():
    return __add_songs(api.get_top_songs())


@plugin.route('/songs/new/')
def show_new_songs():
    return __add_songs(api.get_new_songs())


@plugin.route('/songs/search/<field>/')
def search(field):
    query = plugin.keyboard()
    if query and len(query) > 2:
        url = plugin.url_for(
            endpoint='search_result',
            field=field,
            keyword=query
        )
        plugin.redirect(url)


@plugin.route('/songs/search/<field>/<keyword>/')
def search_result(field, keyword):
    return __add_songs(api.search_songs(field, keyword))


@plugin.route('/songs/similar/<song_id>/')
def show_similar_songs(song_id):
    return __add_songs(api.get_similar_songs(song_id))


@plugin.route('/songs/list/<field>/<query>/')
def exact_query_result(field, query):
    return __add_songs(api.get_songs(**{field: query}))


@plugin.route('/songs/<artist>/<album>/')
def show_songs(artist, album):
    return __add_songs(api.get_songs(artist=artist, album=album))


@plugin.route('/song/<song_id>')
def play_song(song_id):
    url = api.get_song_url(song_id)
    log('Using URL: %s' % url)
    return plugin.set_resolved_url(url)


@plugin.route('/single/<artist>/<title>/')
def play_single(artist, title):
    songs = api.get_songs(artist=artist, title=title)
    # This is hacky, because ... its just hacky ;)
    song_id = songs[0]['id']
    url = api.get_song_url(song_id)
    log('Using URL: %s' % url)
    return plugin.set_resolved_url(url)


def __add_songs(songs):
    title_format = '%(artist)s - %(title)s [%(album)s]'
    str_comment = (
        '%s: %%s kbps | %s: %%s' % (_('bitrate'), _('date'))
    )
    str_artist_context = _('all_songs_from')
    str_album_context = _('all_songs_in_album')
    str_similar_songs = _('show_similar_songs')
    str_info = _('show_info')
    str_add_playlist = _('add_to_playlist')
    my_playlists = plugin.get_storage('my_playlists')
    items = []
    for i, song in enumerate(songs):
        path = plugin.url_for(
            endpoint='play_song',
            song_id=song['id']
        )
        context_menu = []
        if CONTEXT_MENU_ENABLED:
            artist_ascii = song['artist'].encode('ascii', 'ignore')
            album_ascii = song['album'].encode('ascii', 'ignore')
            context_menu.append((
                str_info,
                'XBMC.Action(Info)'
            ))
            context_menu.append((
                str_similar_songs,
                _view(
                    endpoint='show_similar_songs',
                    song_id=song['id']
                )
            ))
            for name in my_playlists.keys():
                context_menu.append((
                    str_add_playlist % name,
                    _run(
                        endpoint='playlists.add_to_playlist',
                        playlist=name,
                        url=path
                    )
                ))
            if artist_ascii:
                context_menu.append((
                    str_artist_context % artist_ascii,
                    _view(
                        endpoint='exact_query_result',
                        field='artist',
                        query=artist_ascii
                    )
                ))
            if album_ascii:
                context_menu.append((
                    str_album_context % album_ascii,
                    _view(
                        endpoint='exact_query_result',
                        field='album',
                        query=album_ascii
                    )
                ))
        items.append({
            'label': title_format % song,
            'thumbnail': song['thumb'],
            'info': {
                'title': song['title'],
                'artist': song['artist'],
                'album': song['album'],
                'genre': song['genre'],
                'duration': int(song['playtime']),
                'size': int(song['bitrate']),
                'date': song['date'],
                'year': int(song.get('date', '0.0.0').split('.')[-1]),
                'comment': str_comment % (song['bitrate'], song['date']),
                'count': i,
            },
            'is_playable': True,
            'context_menu': context_menu,
            'path': path,
        })
    temp_items = plugin.get_storage('temp_items')
    temp_items.update((item['path'], item) for item in items)
    finish_kwargs = {
        'sort_methods': ('PLAYLIST_ORDER', ('LABEL', '%X'), 'DATE')
    }
    return plugin.finish(items, **finish_kwargs)


def _(string_id):
    if string_id in STRINGS:
        return plugin.get_string(STRINGS[string_id])
    else:
        plugin.log.warning('String is missing: %s' % string_id)
        return string_id


def _run(*args, **kwargs):
    return 'XBMC.RunPlugin(%s)' % plugin.url_for(*args, **kwargs)


def _view(*args, **kwargs):
    return 'XBMC.Container.Update(%s)' % plugin.url_for(*args, **kwargs)


def monkey_patch_swift():
    # Congrats - you found the second hacky thing ;)
    # Sometimes its useful to replace the existing context menu
    def add_context_menu_items(self, items, replace_items=True):
        self._listitem.addContextMenuItems(items, replace_items)
    listitem.ListItem.add_context_menu_items = add_context_menu_items


def log(text):
    plugin.log.info(text)

if __name__ == '__main__':
    if CONTEXT_MENU_ENABLED:
        monkey_patch_swift()
    try:
        plugin.run()
    except NetworkError, error:
        plugin.notify(msg=error)
