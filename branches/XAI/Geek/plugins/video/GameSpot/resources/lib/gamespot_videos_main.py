#
# Imports
#
import os
import sys
import xbmc
import xbmcgui
import xbmcplugin

#
# Constants
# 
__settings__ = xbmcplugin
__language__ = xbmc.getLocalizedString

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
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1] ), url = '%s?action=list&plugin_category=%s&video_type=%s' % ( sys.argv[ 0 ], __language__(30001), "all" ), listitem=listitem, isFolder=True)
		
        #
        # Trailers
        #
        listitem = xbmcgui.ListItem( __language__(30002), iconImage="DefaultFolder.png" )
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?action=list&plugin_category=%s&video_type=%s' % ( sys.argv[ 0 ], __language__(30002), "trailers" ), listitem=listitem, isFolder=True)
		
        #		
        # Gameplay
        #
        listitem = xbmcgui.ListItem( __language__(30003), iconImage="DefaultFolder.png" )
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?action=list&plugin_category=%s&video_type=%s' % ( sys.argv[ 0 ], __language__(30003), "gameplay" ), listitem=listitem, isFolder=True)

        #
        # Reviews
        #
        listitem = xbmcgui.ListItem( __language__(30004), iconImage="DefaultFolder.png" )
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?action=list&plugin_category=%s&video_type=%s' % ( sys.argv[ 0 ], __language__(30004), "reviews" ), listitem=listitem, isFolder=True)

        #
        # Shows
        #
        listitem = xbmcgui.ListItem( __language__(30005), iconImage="DefaultFolder.png" )
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?action=list&plugin_category=%s&video_type=%s' % ( sys.argv[ 0 ], __language__(30005), "shows" ), listitem=listitem, isFolder=True)

        #
        # Interviews
        #
        listitem = xbmcgui.ListItem( __language__(30006), iconImage="DefaultFolder.png" )
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?action=list&plugin_category=%s&video_type=%s' % ( sys.argv[ 0 ], __language__(30006), "interviews" ), listitem=listitem, isFolder=True)

        #
        # User
        #
        listitem = xbmcgui.ListItem( __language__(30007), iconImage="DefaultFolder.png" )
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?action=list&plugin_category=%s&video_type=%s' % ( sys.argv[ 0 ], __language__(30007), "user" ), listitem=listitem, isFolder=True)

        # Disable sorting...
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
		
        # End of list...
        xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )