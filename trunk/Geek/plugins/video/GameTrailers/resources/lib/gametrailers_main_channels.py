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
        # GTTV
        #
        listitem = xbmcgui.ListItem( __language__(30070), iconImage = "DefaultFolder.png", thumbnailImage = os.path.join(IMAGES_DIR, "GTTV.png" ) )
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?action=list-gttv&plugin_category=%s' % ( sys.argv[ 0 ], __language__(30070) ), listitem=listitem, isFolder=True)

        #
        # Bonus Round
        #
        listitem = xbmcgui.ListItem( __language__(30071), iconImage = "DefaultFolder.png", thumbnailImage = os.path.join(IMAGES_DIR, "BonusRound.png" ) )
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?action=list-bonusround&plugin_category=%s' % ( sys.argv[ 0 ], __language__(30071) ), listitem=listitem, isFolder=True)

        #
        # Retrospectives
        #
        listitem = xbmcgui.ListItem( __language__(30072), iconImage = "DefaultFolder.png", thumbnailImage = os.path.join(IMAGES_DIR, "Retrospectives.png" ) )
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?action=list-retrospectives&plugin_category=%s' % ( sys.argv[ 0 ], __language__(30072) ), listitem=listitem, isFolder=True)

        #
        # ScrewAttack
        #
        listitem = xbmcgui.ListItem( __language__(30073), iconImage = "DefaultFolder.png", thumbnailImage = os.path.join(IMAGES_DIR, "ScrewAttack.png" ) )
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?action=main-screwattack&plugin_category=%s' % ( sys.argv[ 0 ], __language__(30073) ), listitem=listitem, isFolder=True)
        
        # Disable sorting...
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

        # Label (top-right)...
        xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=__language__(30007) )

        # End of list...
        xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )