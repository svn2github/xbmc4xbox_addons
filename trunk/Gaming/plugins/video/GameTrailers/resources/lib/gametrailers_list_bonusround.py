#
# Imports
#
from BeautifulSoup      import BeautifulSoup
from gametrailers_const import __settings__, __language__
from gametrailers_utils import HTTPCommunicator
import os
import re
import sys
import urllib
import xbmc
import xbmcgui
import xbmcplugin

#
# Main class
#
class Main:
    #
    # Init
    #
    def __init__( self ) :
        # Constants
        self.DEBUG               = False
        self.BR_EPISODE_TITLE_RE = re.compile( "^br_episode_container.*" )
        self.BR_EPISODE_TN_RE    = re.compile( "^br_episode_tn.*" )
        self.IMAGES_PATH         = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'images' ) )
        
        # Parse parameters...
        params = dict(part.split('=') for part in sys.argv[ 2 ][ 1: ].split('&'))
        self.plugin_category = params[ "plugin_category" ] 
        self.current_page    = int ( params.get( "page", "1" ) )
        
        #
        # Get the videos...
        #
        self.getVideos()
    
    #
    # Get videos...
    #
    def getVideos( self ) :
        #
        # Get HTML page...
        #        
        httpCommunicator = HTTPCommunicator()
        htmlData         = httpCommunicator.post( "www.gametrailers.com", "/br_showpage_ajaxfuncs.php", {'do' : 'get_playlist_page', 'page' : self.current_page } )        
        
        #
        # Debug
        #
        if (self.DEBUG) :
            f = open(os.path.join( xbmc.translatePath( "special://profile" ), "plugin_data", "video", sys.modules[ "__main__" ].__plugin__, "page_bonus_round.html" ), "w")
            f.write( htmlData )
            f.close()

        #
        # Parse HTML response...
        #
        beautifulSoup = BeautifulSoup( htmlData )
        
        divs_br_episode_container = beautifulSoup.findAll( "div", { "class" : self.BR_EPISODE_TITLE_RE } )
        for div_br_episode_container in divs_br_episode_container :
            # Title...
            div_br_episode_title = div_br_episode_container.find( "div", { "class" : "br_episode_title" } )
            title                = div_br_episode_title.string.strip()
            
            # Video page URL...
            div_br_episode_tn    = div_br_episode_container.find( "div", { "class" : self.BR_EPISODE_TN_RE } )
            video_page_url       = div_br_episode_tn.a[ "href" ]
            
            # Thumbnail...
            thumbnail_url        = "http://www.gametrailers.com%s" % div_br_episode_tn.a.img[ "src" ]
            
            # Plot...
            div_br_episode_summary = div_br_episode_container.find( "div", { "class" : "br_episode_summary" } )
            plot                   = div_br_episode_summary.contents[ 0 ].strip()
            
            # Add to list...
            listitem        = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail_url )
            listitem.setInfo( "video", { "Title" : title, "Studio" : "GameTrailers", "Plot" : plot } )
            plugin_play_url = '%s?action=play&video_page_url=%s' % ( sys.argv[ 0 ], urllib.quote_plus( video_page_url ) )
            xbmcplugin.addDirectoryItem( handle=int(sys.argv[ 1 ]), url=plugin_play_url, listitem=listitem, isFolder=False)

        # Next page entry...
        listitem = xbmcgui.ListItem (__language__(30503), iconImage = "DefaultFolder.png", thumbnailImage = os.path.join(self.IMAGES_PATH, 'next-page.png'))
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[1]), url = "%s?action=list-bonusround&plugin_category=%s&page=%i" % ( sys.argv[0], self.plugin_category, self.current_page + 1 ), listitem = listitem, isFolder = True)

        # Disable sorting...
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
        
        # Label (top-right)...
        xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category="%s  (%s)" % (self.plugin_category, __language__(30502) % self.current_page ) )
        
        # End of directory...
        xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
