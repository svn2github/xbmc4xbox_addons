#
# Imports
#
from eurogamer_const import __settings__, __language__
import os
import sys
import urllib
import xbmc
import xbmcgui
import xbmcplugin

#
# Main class
#
class Main:
    def __init__( self ):
        # Constants
        self.IMAGES_PATH = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'images' ) )        
        
        #
        # Search...
        #
        listitem = xbmcgui.ListItem( __language__(30009), iconImage="DefaultFolder.png" )
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1] ), url = '%s?action=search-list&query=&plugin_category=%s' % ( sys.argv[ 0 ], __language__(30008) ), listitem=listitem, isFolder=True)
        
        #
        # Previous search queries...
        #
        try :
            saved_queries = eval( __settings__.getSetting( "saved_queries" ) )
        except :
            saved_queries = []
        
        for query in saved_queries :
            listitem = xbmcgui.ListItem( query, iconImage="DefaultFolder.png" )
            xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), 
                                        url = '%s?action=search-list&query=%s&plugin_category=%s' % ( sys.argv[ 0 ], urllib.quote( query ), __language__(30008) ), 
                                        listitem=listitem, 
                                        isFolder=True)		

        # Label (top-right)...
        xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=( "%s" % __language__(30008) ) )

        # Disable sorting...
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
		
        # End of list...
        xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
