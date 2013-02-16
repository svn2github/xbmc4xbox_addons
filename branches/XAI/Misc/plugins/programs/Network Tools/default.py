##############################################################################
#
# Network Tools - Program plugin for XBMC
#
# Version 1.0
#
# Author:
#
#  * Dan Dar3 <dan.dar33@gmail.com> 
#
# Credits :
#
#  * Impacket [ http://oss.coresecurity.com/projects/impacket.html ]

# 
# Constants
#
__plugin__  = "Network Tools"
__author__  = "Dan Dar3"
__url__     = "http://dandar3.blogspot.com"
__date__    = "12 December 2010"
__version__ = "1.0"


#
# Imports
#
import os
import sys
import urllib
import xbmcgui
import xbmcplugin

LIB_DIR = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'lib' ) )
sys.path.append (LIB_DIR) 

#
# Ping
#
if ( "action=ping" in sys.argv[ 2 ] ):
    import xbmcplugin_ping as plugin
    try:
        plugin.Main( "DialogTextViewer.xml", os.getcwd(), "default" )
    except :
        plugin.Main( "DialogScriptInfo.xml", os.getcwd(), "default" )
#
# Main menu
#
else :
    xbmc.log( "[PLUGIN] %s v%s (%s)" % ( __plugin__, __version__, __date__ ), xbmc.LOGNOTICE )
    import xbmcplugin_main as plugin
    plugin.Main()    
