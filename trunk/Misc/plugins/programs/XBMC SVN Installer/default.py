##############################################################################
#
# XBMC SVN Installer - Program plugin for XBMC
# http://www.xbmcsvn.com/
#
# Version 2.1
# 
# Author(s):
#
#  * Dan Dar3 
#    http://dandar3.blogspot.com
#
# Credits:
#
#  * Team XBMC4Xbox                                  [ http://xbmc4xbox.org ]
#  * The Questor        <thequestor@gmail.com>       [ http://wwww.xbmcsvn.com/ ]
#  * Nuka1195 / BigBellyBilly (T3CH Upgrader Script)
#

# 
# Constants
#
__plugin__  = "XBMC SVN Installer"
__author__  = "Dan Dar3 <dan.dar33@gmail.com>"
__url__     = "http://dandar3.blogspot.com"
__date__    = "15 July 2012"
__version__ = "2.1"

#
# Imports
#
import os
import sys

LIB_DIR = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'lib' ) )
sys.path.append (LIB_DIR) 

#
# Main block
#


# Build - List
if ( "action=build-list" in sys.argv[ 2 ] ):
    import xbmcsvn_build_list as plugin
    plugin.Main()

# Build - View details
elif ( "action=build-view" in sys.argv[ 2 ] ):
    import xbmcsvn_build_info as plugin
    gui = plugin.GUI( "xbmcsvn_build_info.xml", os.getcwd(), "default" )

# Build - Download
elif ( "action=build-download" in sys.argv[ 2 ]):
    import xbmcsvn_build_install as plugin
    plugin.Main()
    
# Build - Install
elif ( "action=build-install" in sys.argv[ 2 ]):
    import xbmcsvn_build_install as plugin
    plugin.Main()

# Build - Update dashboard config
elif ( "action=dash-set" in sys.argv[ 2 ]) :
    import xbmcsvn_dash_set as plugin
    plugin.Main()

# Build - Delete old installations
elif ( "action=build-delete" in sys.argv[ 2 ]) :
    import xbmcsvn_build_delete as plugin
    plugin.Main()

# Main
else:
    xbmc.log( "[PLUGIN] %s v%s (%s)" % ( __plugin__, __version__, __date__ ), xbmc.LOGNOTICE )
    
    import xbmcsvn_build_list as plugin
    plugin.Main()
