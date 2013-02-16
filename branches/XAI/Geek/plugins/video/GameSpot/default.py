##############################################################################
#
# GameSpot - XBMC video plugin
# http://www.gamespot.com/videos/
#
# Version 1.3
# 
# Coding by Dan Dar3 
# http://dandar3.blogspot.com
#
#
# Credits:
#   * GameSpot                                                          [http://www.gamespot.com]
#   * Team XBMC @ XBMC.org                                              [http://xbmc.org/]
#   * Leonard Richardson <leonardr@segfault.org> - BeautifulSoup 3.0.7a [http://www.crummy.com/software/BeautifulSoup/]
#   * Bod Redivi    <bob@redivi.com>             - simplejson 2.0.9     [http://undefined.org/python/#simplejson]
#   * Eric Lawrence <e_lawrence@hotmail.com>     - Fiddler Web Debugger [http://www.fiddler2.com]
#

# 
# Constants
#
__plugin__  = "GameSpot Videos"
__author__  = "Dan Dar3"
__url__     = "http://dandar3.blogspot.com"
__date__    = "13 November 2011"
__version__ = "1.3"

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
if ( "action=list" in sys.argv[ 2 ] ):
    import gamespot_videos_list as plugin
elif ( "action=play" in sys.argv[ 2 ] ):
    import gamespot_videos_play as plugin
else :
	import gamespot_videos_main as plugin

plugin.Main()
