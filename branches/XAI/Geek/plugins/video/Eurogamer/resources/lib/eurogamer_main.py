#
# Imports
#
import os
import sys
import xbmc
import xbmcgui
import xbmcplugin
from eurogamer_const import __language__

#
# Main class
#
class Main:
    def __init__( self ):
        #
        # Latest videos
        #
        #listitem = xbmcgui.ListItem( __language__(30001), iconImage="DefaultFolder.png" )
        #xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1] ), url = '%s?action=list&channel=%s&channel_desc=%s' % ( sys.argv[ 0 ], "all",      __language__(30001) ), listitem=listitem, isFolder=True)

        #
        # Trailers
        #
        #listitem = xbmcgui.ListItem( __language__(30002), iconImage="DefaultFolder.png" )
        #xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1] ), url = '%s?action=list&channel=%s&channel_desc=%s' % ( sys.argv[ 0 ], "trailers", __language__(30002) ), listitem=listitem, isFolder=True)
        
        #
        # Gameplay
        #
        #listitem = xbmcgui.ListItem( __language__(30003), iconImage="DefaultFolder.png" )
        #xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?action=list&channel=%s&channel_desc=%s' % ( sys.argv[ 0 ], "capture", __language__(30003) ), listitem=listitem, isFolder=True)

        #
        # Video
        #
        listitem = xbmcgui.ListItem( __language__(30005), iconImage="DefaultFolder.png" )
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1] ), url = '%s?action=list&channel=%s&channel_desc=%s' % ( sys.argv[ 0 ], "video",      __language__(30005) ), listitem=listitem, isFolder=True)

        #
        # Popular Now
        #
        listitem = xbmcgui.ListItem( __language__(30006), iconImage="DefaultFolder.png" )
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1] ), url = '%s?action=list&channel=%s&channel_desc=%s' % ( sys.argv[ 0 ], "now",      __language__(30006) ), listitem=listitem, isFolder=True)

        #
        # Recently popular
        #
        listitem = xbmcgui.ListItem( __language__(30007), iconImage="DefaultFolder.png" )
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1] ), url = '%s?action=list&channel=%s&channel_desc=%s' % ( sys.argv[ 0 ], "recently",      __language__(30007) ), listitem=listitem, isFolder=True)
        
        #
        # EGVT Show
        #
        listitem = xbmcgui.ListItem( __language__(30004), iconImage="DefaultFolder.png" )
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?action=list&channel=%s&channel_desc=%s' % ( sys.argv[ 0 ], "show",    __language__(30004) ), listitem=listitem, isFolder=True)

        #
        # Search
        #
        listitem = xbmcgui.ListItem( __language__(30008), iconImage="DefaultFolder.png" )
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?action=main-search&channel=%s&channel_desc=%s' % ( sys.argv[ 0 ], "search",    __language__(30008) ), listitem=listitem, isFolder=True)

        # Disable sorting...
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
        
        # End of list...
        xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )