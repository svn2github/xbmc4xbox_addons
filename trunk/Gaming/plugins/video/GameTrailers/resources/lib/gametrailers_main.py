#
# Imports
#
from gametrailers_const import __settings__, __language__
import os
import sys
import xbmc
import xbmcgui
import xbmcplugin

#
# Main class
#
class Main:
    def __init__( self ):
        # Constants
        IMAGES_DIR = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'images' ) )        
        
        #
        # All
        #
        listitem = xbmcgui.ListItem( __language__(30001), iconImage="DefaultFolder.png" )
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1] ), url = '%s?action=list-all&plugin_category=%s' % ( sys.argv[ 0 ], __language__(30001) ), listitem=listitem, isFolder=True)
		
        #
        # Previews
        #
        listitem = xbmcgui.ListItem( __language__(30002), iconImage="DefaultFolder.png" )
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?action=list-previews&plugin_category=%s' % ( sys.argv[ 0 ], __language__(30002) ), listitem=listitem, isFolder=True)
		
        #		
        # Reviews
        #
        listitem = xbmcgui.ListItem( __language__(30003), iconImage="DefaultFolder.png" )
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?action=list-reviews&plugin_category=%s' % ( sys.argv[ 0 ], __language__(30003) ), listitem=listitem, isFolder=True)

        #
        # Top Media
        #
        listitem = xbmcgui.ListItem( __language__(30004), iconImage="DefaultFolder.png" )
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?action=list-top20&plugin_category=%s' % ( sys.argv[ 0 ], __language__(30004) ), listitem=listitem, isFolder=True)

        #
        # Gameplay
        #
        listitem = xbmcgui.ListItem( __language__(30005), iconImage="DefaultFolder.png" )
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?action=list-gameplay&plugin_category=%s' % ( sys.argv[ 0 ], __language__(30005) ), listitem=listitem, isFolder=True)
        
        #
        # Platforms
        #
        listitem = xbmcgui.ListItem( __language__(30006), iconImage="DefaultFolder.png" )
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?action=main-platforms&plugin_category=%s' % ( sys.argv[ 0 ], __language__(30006) ), listitem=listitem, isFolder=True)

        #
        # Channels
        #
        listitem = xbmcgui.ListItem( __language__(30007), iconImage = "DefaultFolder.png" )
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?action=main-channels&plugin_category=%s' % ( sys.argv[ 0 ], __language__(30007) ), listitem=listitem, isFolder=True)
        
        #
        #  Search
        #
        listitem = xbmcgui.ListItem( __language__(30008), iconImage = "DefaultFolder.png", thumbnailImage = os.path.join(IMAGES_DIR, "search.png" ) )
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?action=main-search&plugin_category=%s' % ( sys.argv[ 0 ], __language__(30008) ), listitem=listitem, isFolder=True)

        # Disable sorting...
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
		
        # End of list...
        xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )