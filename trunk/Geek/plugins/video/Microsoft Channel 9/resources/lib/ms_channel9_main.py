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
        # All
        #
        listitem = xbmcgui.ListItem( xbmc.getLocalizedString(30401), iconImage="DefaultFolder.png" )
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1] ), url = '%s?action=list-all' % ( sys.argv[ 0 ] ), listitem=listitem, isFolder=True)

        #
        # Tags
        #
        listitem = xbmcgui.ListItem( xbmc.getLocalizedString(30402), iconImage="DefaultFolder.png" )
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1] ), url = '%s?action=browse-tags' % ( sys.argv[ 0 ] ), listitem=listitem, isFolder=True)

        #
        # Shows
        #
        listitem = xbmcgui.ListItem( xbmc.getLocalizedString(30403), iconImage="DefaultFolder.png" )
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1] ), url = '%s?action=browse-shows' % ( sys.argv[ 0 ] ), listitem=listitem, isFolder=True)

        #
        # Series
        #
        listitem = xbmcgui.ListItem( xbmc.getLocalizedString(30404), iconImage="DefaultFolder.png" )
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1] ), url = '%s?action=browse-series' % ( sys.argv[ 0 ] ), listitem=listitem, isFolder=True)

        # Disable sorting...
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
        
        # End of list...
        xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )