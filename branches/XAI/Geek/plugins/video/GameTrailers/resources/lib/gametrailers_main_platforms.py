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
        # PC
        #
        listitem = xbmcgui.ListItem( __language__(30061), iconImage="DefaultFolder.png", thumbnailImage=os.path.join( IMAGES_DIR, "pc.png" ) )
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?action=list-platform&platform=pc&plugin_category=%s' % ( sys.argv[ 0 ], __language__(30061) ), listitem=listitem, isFolder=True)
		
        #		
        # PlayStation 3
        #
        listitem = xbmcgui.ListItem( __language__(30062), iconImage="DefaultFolder.png", thumbnailImage=os.path.join( IMAGES_DIR, "ps3.png" ) )
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?action=list-platform&platform=ps3&plugin_category=%s' % ( sys.argv[ 0 ], __language__(30062) ), listitem=listitem, isFolder=True)

        #
        # Xbox 360
        #
        listitem = xbmcgui.ListItem( __language__(30063), iconImage="DefaultFolder.png", thumbnailImage=os.path.join( IMAGES_DIR, "xbox360.png" ) )
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?action=list-platform&platform=xbox360&plugin_category=%s' % ( sys.argv[ 0 ], __language__(30063) ), listitem=listitem, isFolder=True)

        #
        # Nintendo Wii
        #
        listitem = xbmcgui.ListItem( __language__(30064), iconImage="DefaultFolder.png", thumbnailImage=os.path.join( IMAGES_DIR, "wii.png" ) )
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?action=list-platform&platform=wii&plugin_category=%s' % ( sys.argv[ 0 ], __language__(30064) ), listitem=listitem, isFolder=True)

        #
        # PSP
        #
        listitem = xbmcgui.ListItem( __language__(30066), iconImage="DefaultFolder.png", thumbnailImage=os.path.join(IMAGES_DIR, "psp.png" ) )
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?action=list-platform&platform=psp&plugin_category=%s' % ( sys.argv[ 0 ], __language__(30066) ), listitem=listitem, isFolder=True)

        #
        # DS
        #
        listitem = xbmcgui.ListItem( __language__(30067), iconImage="DefaultFolder.png", thumbnailImage=os.path.join(IMAGES_DIR, "ds.png" ) )
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?action=list-platform&platform=ds&plugin_category=%s' % ( sys.argv[ 0 ], __language__(30067) ), listitem=listitem, isFolder=True)

        #
        # Mobile
        #
        listitem = xbmcgui.ListItem( __language__(30068), iconImage="DefaultFolder.png", thumbnailImage=os.path.join(IMAGES_DIR, "mobile.png" ) )
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?action=list-platform&platform=mobile&plugin_category=%s' % ( sys.argv[ 0 ], __language__(30068) ), listitem=listitem, isFolder=True)

        # Label (top-right)...
        xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=( "%s" % __language__(30006) ) )

        # Disable sorting...
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
		
        # End of list...
        xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )