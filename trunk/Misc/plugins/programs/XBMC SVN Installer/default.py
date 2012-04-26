##############################################################################
#
# XBMC SVN Installer - Program plugin for XBMC
# http://www.xbmcsvn.com/
#
# Version 2.0 beta 1
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
__date__    = "08 October 2011"
__version__ = "2.0 beta 1"

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

# News
if ( "action=news" in sys.argv[ 2 ] ) :
    import xbmcsvn_news as plugin
    try:
        gui = plugin.GUI( "DialogTextViewer.xml", os.getcwd(), "default" )
        del gui
    except :
        gui = plugin.GUI( "DialogScriptInfo.xml", os.getcwd(), "default" )
        del gui
    
# Skins - List
elif ( "action=skins-list" in sys.argv[ 2 ] ):
    import xbmcsvn_skin_list as plugin
    plugin.Main()
    
# Skin - View details
elif ( "action=skin-view" in sys.argv[ 2 ] ):
    import xbmcsvn_skin_info as plugin
    gui = plugin.GUI( "xbmcsvn_skin_info.xml", os.getcwd(), "default" )

# Skin - Install
elif ( "action=skin-install" in sys.argv[ 2 ] ):
    import xbmcsvn_skin_install as plugin
    plugin.Main()

# Build - List
elif ( "action=build-list" in sys.argv[ 2 ] ):
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
    
    import xbmcsvn_main as plugin
    plugin.Main()
