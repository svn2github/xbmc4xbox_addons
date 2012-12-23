"""
    Plugin for streaming Apple Movie Trailers
"""

# main imports
import sys

# plugin constants
__plugin__ = "The Trailers"
__author__ = "nuka1195"
__url__ = "http://code.google.com/p/xbmc-addons/"
__svn_url__ = "http://xbmc-addons.googlecode.com/svn/trunk/plugins/video/Apple%20Movie%20Trailers%20Lite"
__useragent__ = "QuickTime/7.6.5 (qtver=7.6.5;os=Windows NT 5.1Service Pack 3)"
#__useragent__ = "iTunes/9.0.2 (Windows; Microsoft Windows XP Professional Service Pack 3 (Build 2600)) AppleWebKit/531.21.8"
__credits__ = "Team XBMC"
__version__ = "1.8.2a"
__svn_revision__ = "$Revision: 1639 $"
__XBMC_Revision__ = "22965"


if ( __name__ == "__main__" ):
    if ( not sys.argv[ 2 ] ):
        # we need check compatible()
        from resources.lib.utils import check_compatible
        # only run if compatible
        if ( check_compatible() ):
            import resources.lib.trailers as plugin
            plugin.Main()
    elif ( sys.argv[ 2 ].startswith( "?category=" ) ):
        import resources.lib.trailers as plugin
        plugin.Main()
    elif ( sys.argv[ 2 ].startswith( "?showtimes=" ) ):
        import os
        import resources.lib.showtimes as showtimes
        s = showtimes.GUI( "plugin-AMTII-showtimes.xml", os.getcwd(), "default" )
        del s
    elif ( sys.argv[ 2 ].startswith( "?couchpotato=" ) ):
        import resources.lib.couchpotato as couchpotato
        couchpotato.Main()
    elif ( sys.argv[ 2 ].startswith( "?download=" ) ):
        import resources.lib.download as download
        download.Main()
    elif ( sys.argv[ 2 ].startswith( "?settings=" ) ):
        import xbmc
        import xbmcplugin
        xbmcplugin.openSettings( sys.argv[ 0 ] )
        # sleep for a few milliseconds, to give dialog time to close.  had issues early, may not be necessary
        #TODO: verify this is necessary
        #xbmc.sleep( 100 )
        # refresh listing in case settings changed
        xbmc.executebuiltin( "Container.Refresh" )
