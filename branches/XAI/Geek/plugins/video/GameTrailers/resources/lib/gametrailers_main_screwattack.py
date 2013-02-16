#
# Imports
#
from gametrailers_const import __settings__, __language__
import os
import sys
import urllib
import xbmcgui
import xbmcplugin

#
# Main class
#
class Main:
    def __init__( self ):
        #
        # ScrewAttack - Angry Video Game Nerd
        #
        listitem = xbmcgui.ListItem( __language__(30074), iconImage = "DefaultFolder.png" )
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?action=list-screwattack&plugin_category=%s&channel_category=nerd' % ( sys.argv[ 0 ], urllib.quote_plus("%s - %s" % ( __language__(30073), __language__(30074) ) ) ), listitem=listitem, isFolder=True)

        #
        # ScrewAttack - Angry Video Game Nerd
        #
        listitem = xbmcgui.ListItem( __language__(30075), iconImage = "DefaultFolder.png" )
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?action=list-screwattack&plugin_category=%s&channel_category=top10' % ( sys.argv[ 0 ], urllib.quote_plus("%s - %s" % ( __language__(30073), __language__(30075) ) ) ), listitem=listitem, isFolder=True)
        
        #
        # ScrewAttack - Angry Video Game Nerd
        #
        listitem = xbmcgui.ListItem( __language__(30076), iconImage = "DefaultFolder.png" )
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?action=list-screwattack&plugin_category=%s&channel_category=vault' % ( sys.argv[ 0 ], urllib.quote_plus("%s - %s" % ( __language__(30073), __language__(30076) ) ) ), listitem=listitem, isFolder=True)
        
        # Disable sorting...
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

        # Label (top-right)...
        xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category="%s" % __language__(30073) )

        # End of list...
        xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
