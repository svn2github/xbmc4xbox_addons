##############################################################################
#
# GameTrailers - XBMC video plugin
# http://www.gametrailers.com
#
# Version 2.3 beta 3
# 
# Coding by Dan Dar3 
# http://dandar3.blogspot.com
#
#
# Credits:
#   * GameTrailers.com                                                  [http://www.gametrailers.com]
#   * Team XBMC4Xbox @ XBMC4Xbox.org                                    [http://xbmc4xbox.org/]
#   * Leonard Richardson <leonardr@segfault.org> - BeautifulSoup 3.0.7a [http://www.crummy.com/software/BeautifulSoup/]
#   * Eric Lawrence <e_lawrence@hotmail.com>     - Fiddler Web Debugger [http://www.fiddler2.com]
#

# 
# Constants
#
__plugin__  = "GameTrailers"
__author__  = "Dan Dar3"
__url__     = "http://dandar3.blogspot.com"
__date__    = "18 October 2011"
__version__ = "2.3 beta 3"

#
# Imports
#
import os
import sys

LIB_DIR = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'lib' ) )
sys.path.append (LIB_DIR)

#
# All (list)
#
if ( "action=list-all" in sys.argv[ 2 ] ):
    import gametrailers_list_all as plugin
#
# Previews (list)
#
elif ( "action=list-previews" in sys.argv[ 2 ] ):
    import gametrailers_list_previews as plugin
#
# Reviews (list)
#
elif ( "action=list-reviews" in sys.argv[ 2 ] ):
    import gametrailers_list_reviews as plugin
#
# Top Media (list)
#
elif ( "action=list-top20" in sys.argv[ 2 ] ):
    import gametrailers_list_top20 as plugin
#
# Gameplay (list)
#
elif ( "action=list-gameplay" in sys.argv[ 2 ] ):
    import gametrailers_list_gameplay as plugin
#
# Platforms (menu)
#
elif ( "action=main-platforms" in sys.argv[ 2 ] ):
    import gametrailers_main_platforms as plugin
#
# Platform (videos)
#
elif ( "action=list-platform" in sys.argv[ 2 ] ):
    import gametrailers_list_platform as plugin
#
# Channels (menu)
#
elif ( "action=main-channels" in sys.argv[ 2 ] ):
    import gametrailers_main_channels as plugin
#
# Channels - GTTV (list)
#
elif ( "action=list-gttv" in sys.argv[ 2 ] ):
    import gametrailers_list_gttv as plugin
#
# Channels - Bonus Round (list)
#
elif ( "action=list-bonusround" in sys.argv[ 2 ] ):
    import gametrailers_list_bonusround as plugin
#
# Channels - Retrospectives (list)
#
elif ( "action=list-retrospectives" in sys.argv[ 2 ] ):
    import gametrailers_list_retrospectives as plugin
#
# Channels - ScrewAttack (main - subcategories)
#
elif ( "action=main-screwattack" in sys.argv[ 2 ] ):
    import gametrailers_main_screwattack as plugin
#
# Channels - ScrewAttack (list)
#
elif ( "action=list-screwattack" in sys.argv[ 2 ] ):
    import gametrailers_list_screwattack as plugin
#
# Search (menu)
#
elif ( "action=main-search" in sys.argv[ 2 ] ):
    import gametrailers_main_search as plugin
#
# Search (results)
#
elif ( "action=list-search" in sys.argv[ 2 ] ):
   import gametrailers_list_search as plugin
#
# Play
#
elif ( "action=play" in sys.argv[ 2 ] ):
    import gametrailers_play as plugin
#
# Main menu
#
else :
    xbmc.log( "[PLUGIN] %s v%s (%s)" % ( __plugin__, __version__, __date__ ), xbmc.LOGNOTICE )
    import gametrailers_main as plugin

plugin.Main()
