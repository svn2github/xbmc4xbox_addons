"""
    Music plugin for streaming content from http://www.play.cz 

    Currently only list of online czech radio stations 

"""

import sys
import xbmc
import playczAPI

# plugin constants 
__plugin__ = "PlayCZ"
__author__ = "Tomas.Zemres"
__url__ = "http://code.google.com/p/xbmc-czech/"
__svn_url__ = "http://xbmc-czech.googlecode.com/svn/trunk/plugins/music/PlayCZ"
__version__ = "0.1"

xbmc.log( "[PLUGIN] %s version %s initialized!" % ( __plugin__, __version__, ), xbmc.LOGNOTICE )

if __name__ == '__main__':
    playczAPI.main(sys.argv)

