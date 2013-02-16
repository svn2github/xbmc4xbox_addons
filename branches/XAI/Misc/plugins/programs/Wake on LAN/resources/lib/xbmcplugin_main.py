#
# Imports
#
import sys
import xbmc
import xbmcgui
import xbmcplugin

#
# Main class
#
class Main:
    def __init__( self ):
        computers = int ( xbmcplugin.getSetting("computers") ) + 1
        
        #
        # List computers...
        #
        for i in range(computers) :
            computer_name = xbmcplugin.getSetting("comp_%u_name" % ( i + 1 ))
            computer_mac  = xbmcplugin.getSetting("comp_%u_mac"  % ( i + 1 ))
            
            listitem = xbmcgui.ListItem( xbmc.getLocalizedString(30901) % computer_name, iconImage="DefaultProgram.png" )
            xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1] ), 
                                         url    = sys.argv[ 0 ] + '?action=wake&name=%s&mac=%s' % ( computer_name, computer_mac ), 
                                         listitem=listitem, 
                                         isFolder=False)

        #
        # Disable sorting...
        #
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

        #
        # End of list...
        #        
        xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )        
