"""
    Plugin for viewing content from www.blip.tv
"""

# main imports
import sys
import xbmc

# plugin constants
__plugin__ = "Blip.TV"
__author__ = "nuka1195"
__url__ = "http://code.google.com/p/xbmc-addons/"
__svn_url__ = "http://xbmc-addons.googlecode.com/svn/trunk/plugins/video/Blip.TV"
__version__ = "1.1.1"

xbmc.log( "[PLUGIN] '%s: version %s' initialized!" % ( __plugin__, __version__, ), xbmc.LOGNOTICE )


if ( __name__ == "__main__" ):
    if ( not sys.argv[ 2 ] ):
        from BlipTVAPI import xbmcplugin_categories as plugin
    elif ( "category='presets_videos'" in sys.argv[ 2 ] ):
        from BlipTVAPI import xbmcplugin_categories as plugin
    elif ( "category='presets_users'" in sys.argv[ 2 ] ):
        from BlipTVAPI import xbmcplugin_categories as plugin
    else:
        from BlipTVAPI import xbmcplugin_videos as plugin
    plugin.Main()
