#
# Imports
#
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
        # News
        #
        listitem = xbmcgui.ListItem( xbmc.getLocalizedString(30001), iconImage="DefaultFolder.png", thumbnailImage = os.path.join(IMAGES_DIR, "news.png" ) )
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1] ), url = '%s?action=news' % ( sys.argv[ 0 ] ), listitem=listitem, isFolder=False)

        #
        # Skins
        #
        listitem = xbmcgui.ListItem( xbmc.getLocalizedString(30002), iconImage="DefaultFolder.png", thumbnailImage = os.path.join(IMAGES_DIR, "skins.png" ) )
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1] ), url = '%s?action=skins-list&category=%s' % ( sys.argv[ 0 ], xbmc.getLocalizedString(30002) ), listitem=listitem, isFolder=True)

        #
        # Builds (Xbox only)
        #
        if os.getenv("OS") == os.getenv("OS") :
            listitem = xbmcgui.ListItem( xbmc.getLocalizedString(30003), iconImage="DefaultFolder.png", thumbnailImage = os.path.join(IMAGES_DIR, "builds.png" ) )
            xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1] ), url = '%s?action=build-list&category=%s' % ( sys.argv[ 0 ], xbmc.getLocalizedString(30003) ), listitem=listitem, isFolder=True)        

        # Disable sorting...
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
        
        # End of list...
        xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )