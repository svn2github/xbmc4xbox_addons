# coding: utf-8
'''
Created on 10 jan 2011

@author: Emuller
'''
import os,sys
import urllib,urllib2,re
import xbmc,xbmcplugin,xbmcgui,xbmcaddon #@UnresolvedImport
from xml.dom import minidom
from traceback import print_exc

# plugin modes
MODE_SHOW_GENRES = 5
MODE_SHOW_SUBGENRES = 10
MODE_SHOW_STATIONS = 20
MODE_SHOW_STREAMS = 30
MODE_PLAY_STREAM = 40
MODE_SHOW_SEARCH_TAG = 45
MODE_SHOW_SEARCH_STATION = 46

# parameter keys
PARAMETER_KEY_MODE = "mode"

# control id's
CONTROL_MAIN_LIST_START  = 50
CONTROL_MAIN_LIST_END    = 59

# plugin handle
handle = int(sys.argv[1])
__addonname__ = "plugin.audio.shoutcastradio"
__settings__ = xbmcaddon.Addon(id='plugin.audio.shoutcastradio')
__language__ = __settings__.getLocalizedString

import ShoutcastCore as core
shoutcastcore = core.ShoutcastCore();

# utility functions
def parameters_string_to_dict(parameters):
    ''' Convert parameters encoded in a URL to a dict. '''
    paramDict = {}
    if parameters:
        paramPairs = parameters[1:].split("&")
        for paramsPair in paramPairs:
            paramSplits = paramsPair.split('=')
            if (len(paramSplits)) == 2:
                paramDict[paramSplits[0]] = paramSplits[1]
    return paramDict

def addDirectoryItem(name, isFolder=True, parameters={},image="", isVideo=True):
    ''' Add a list item to the XBMC UI.'''
    li = xbmcgui.ListItem(name, iconImage="DefaultAudio.png", thumbnailImage=image)
            
    if isVideo:
        li.setProperty("IsPlayable", "true")
        li.setProperty( "Music", "true" )  
        li.setInfo(type='Music', infoLabels=parameters)    
        
    
    url = sys.argv[0] + '?' + urllib.urlencode(parameters)
    
    xbmcplugin.setContent( handle=int( sys.argv[ 1 ] ), content="files" )    
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=li, isFolder=isFolder)

# UI builder functions
def show_root_menu():
    ''' Show the plugin root menu. '''
    
    ''' Show the search button '''
    addDirectoryItem(name=__language__(30201), isFolder=True, parameters={PARAMETER_KEY_MODE: MODE_SHOW_SEARCH_TAG}, isVideo=False)
    addDirectoryItem(name=__language__(30202), isFolder=True, parameters={PARAMETER_KEY_MODE: MODE_SHOW_SEARCH_STATION}, isVideo=False)
    addDirectoryItem(name=__language__(30203), isFolder=True, parameters={PARAMETER_KEY_MODE: MODE_SHOW_GENRES}, isVideo=False)
    
    xbmcplugin.endOfDirectory(handle=handle, succeeded=True)

def show_genres():
    ''' get genres '''
    genres = shoutcastcore.getShoutcastGenres()
    
    for genre in genres:
        addDirectoryItem(name=genre.get('title').replace('&amp;','&'), isFolder=True, parameters={PARAMETER_KEY_MODE: MODE_SHOW_SUBGENRES, "id" : genre.get('id'), "title": genre.get('title').replace('&amp;','&')}, isVideo=False)
    
    xbmcplugin.endOfDirectory(handle=handle, succeeded=True)


def show_search_tag():
    viewmode = getCurrentViewmode()
    q = getKeyboardInput(title=__language__(30204), default="")
    if q!="":
        show_stations({ "title" : q, "type" : "genre", "index" : 0})
        xbmc.executebuiltin("Container.SetViewMode(%i)" %  viewmode)

def show_search_station():
    viewmode = getCurrentViewmode()
    q = getKeyboardInput(title=__language__(30205), default="")
    if q!="":
        show_stations({ "title" : q, "type" : "search", "index" : 0})
        xbmc.executebuiltin("Container.SetViewMode(%i)" %  viewmode)

def show_subgenres(params):
    subgenres = shoutcastcore.getShoutcastSubGenres( params.get('id'), urllib.unquote_plus( params.get('title') ) )
    
    addDirectoryItem(name=__language__(30206), isFolder=True, parameters={PARAMETER_KEY_MODE: MODE_SHOW_STATIONS, "type" : 'genre', "title": params.get('title'), "index" : 0}, isVideo=False)
    
    for subgenre in subgenres:
        addDirectoryItem(name=subgenre.get('title'), isFolder=True, parameters={PARAMETER_KEY_MODE: MODE_SHOW_STATIONS, "type" : 'genre', "title": subgenre.get('title'), "index" : 0}, isVideo=False)
    
    xbmcplugin.endOfDirectory(handle=handle, succeeded=True)
    
def show_stations(params):
    stations = shoutcastcore.getShoutcastStations(params.get('title'),params.get('type'),params.get('index'))
    
    for station in stations[0]:
        addDirectoryItem(name="[%s kbps] %s (%s listeners)" % (station.get('bitrate'), station.get('title'), station.get('listeners') ), isFolder=True, parameters={PARAMETER_KEY_MODE: MODE_SHOW_STREAMS, "href" : station.get('href'), "title": station.get('title')}, isVideo=False)

    if stations[1]:
        addDirectoryItem(name=__language__(30207), isFolder=True, parameters={PARAMETER_KEY_MODE: MODE_SHOW_STATIONS, "type" : params.get('type'), "title": params.get('title'), "index" : int(params.get('index')) + (20,40,60,80,100)[int(__settings__.getSetting('numresults'))]}, isVideo=False) 

    xbmcplugin.endOfDirectory(handle=handle, succeeded=True)
    
def show_streams(params):
    streams = shoutcastcore.getShoutcastStreams(urllib.unquote(params.get('href')))
    
    player = xbmc.Player()
    '''if player.isPlaying():
        player.stop()'''
    
    playlist = xbmc.PlayList(xbmc.PLAYLIST_MUSIC)
    playlist.clear()
    
    for stream in streams:
        parameters = {PARAMETER_KEY_MODE : MODE_PLAY_STREAM, "url":stream.get('url'), "title":stream.get('title')}
        listitem=xbmcgui.ListItem(label=stream.get('title'))
        listitem.setProperty('IsPlayable', 'true')
        listitem.setProperty( "Music", "true" )  
        listitem.setInfo(type='Music', infoLabels=parameters)
         
        url = sys.argv[0] + '?' + urllib.urlencode(parameters)        
        playlist.add(url=stream.get('url'), listitem=listitem)
        
        if playlist.size()==1:
            player.play(item=stream.get('url'), listitem=listitem)

def play_stream(params):    
    listitem=xbmcgui.ListItem(label=params.get('title'), path=urllib.unquote( params.get('url')) );    
    ''' listitem.setInfo(type='Video', infoLabels=labels) '''

    xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=listitem)

def parseBoolString(theString):
    return theString[0].upper()=='T'

# Log NOTICE
def log_notice(msg):
    xbmc.output("### [%s] - %s" % (__addonname__,msg,),level=xbmc.LOGNOTICE )

def showMessage(heading, message, duration=10):
    xbmc.executebuiltin('XBMC.Notification("%s", "%s", %s)' % ( heading, message, duration) )

def getCurrentViewmode():
    for id in range( CONTROL_MAIN_LIST_START, CONTROL_MAIN_LIST_END + 1 ):
        try:
            if xbmc.getCondVisibility( "Control.IsVisible(%i)" % id ):
                break
        except:
            print_exc()
    return id

def getKeyboardInput(title = "Input", default="", hidden=False):
    result = None
        
    kbd = xbmc.Keyboard(default, title)
    kbd.setHiddenInput(hidden)
    kbd.doModal()
    
    if kbd.isConfirmed():
        result = kbd.getText()
    
    return result

# parameter values
params = parameters_string_to_dict(sys.argv[2])
mode = int(params.get(PARAMETER_KEY_MODE, "0"))

# Depending on the mode, call the appropriate function to build the UI.
if not sys.argv[2]:
    # new start
    ok = show_root_menu()
if mode == MODE_SHOW_GENRES:
	ok = show_genres()
if mode == MODE_SHOW_SUBGENRES:
    ok = show_subgenres(params)
if mode == MODE_SHOW_STATIONS:
    ok = show_stations(params)
if mode == MODE_SHOW_STREAMS:
    ok = show_streams(params)
if mode == MODE_PLAY_STREAM:
    ok = play_stream(params)
if mode == MODE_SHOW_SEARCH_TAG:
	ok = show_search_tag()
if mode == MODE_SHOW_SEARCH_STATION:
	ok = show_search_station()
    
    