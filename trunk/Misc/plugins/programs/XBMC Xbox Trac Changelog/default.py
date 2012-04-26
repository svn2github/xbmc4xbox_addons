##############################################################################
#
# XBMC for Xbox Trac Changelog - Program plugin for XBMC
# http://sourceforge.net/apps/trac/xbmc4xbox/log/trunk
#
# Version 1.6
# 
# Author:
#
#  * Dan Dar3 
#    http://dandar3.blogspot.com
#
# Credits:
#
#  * Team XBMC4Xbox    [ http://xbmc4xbox.org ]
#

# 
# Constants
#
__plugin__  = "XBMC Xbox Trac Changelog"
__author__  = "Dan Dar3 <dan.dar33@gmail.com>"
__url__     = "http://dandar3.blogspot.com"
__date__    = "06 November 2010"
__version__ = "1.6"


#
# Imports
#
import os
import sys
import xbmc

LIB_DIR = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'lib' ) )
sys.path.append (LIB_DIR) 

#
# Main block
#

# Revision info
if ("action=revision-info" in sys.argv[ 2 ] ):
    import xbmcplugin_revision_info as plugin
    gui = plugin.GUI( "xbmcplugin_revision_info.xml", os.getcwd(), "default" )
    del gui
    
# Revision list
else:
    xbmc.log( "[PLUGIN] %s v%s (%s)" % ( __plugin__, __version__, __date__ ), xbmc.LOGNOTICE )
    
    import xbmcplugin_revision_list as plugin
    plugin.Main()

