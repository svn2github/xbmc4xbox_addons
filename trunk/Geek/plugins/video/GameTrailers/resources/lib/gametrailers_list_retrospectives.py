#
# Imports
#
import re
import os
import sys
import xbmc
import xbmcgui
import xbmcplugin
import urllib
from BeautifulSoup      import BeautifulSoup
from BeautifulSoup      import SoupStrainer
from gametrailers_utils import HTTPCommunicator

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
        self.EPISODE_SEGMENTS_RE = re.compile( "^episode_segments_.*" )
        
        # Parse parameters...
        params = dict(part.split('=') for part in sys.argv[ 2 ][ 1: ].split('&'))
        self.plugin_category = params[ "plugin_category" ] 

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
        htmlData = httpCommunicator.get( "http://www.gametrailers.com/retrospective/" )

        #
        # Debug
        #
        if (self.DEBUG) :
            f = open(os.path.join( xbmc.translatePath( "special://profile" ), "plugin_data", "video", sys.modules[ "__main__" ].__plugin__, "page_retrospectives.html" ), "w")
            f.write( htmlData )
            f.close()

        #
        # Parse HTML response...
        #
        soupStrainer = SoupStrainer("div", { "class" : "basic_container_top" } )
        beautifulSoup = BeautifulSoup( htmlData, parseOnlyThese=soupStrainer )
        
        divs_basic_container_content      = beautifulSoup.findAll( "div", { "class" : "basic_container_content" } )
        first_div_basic_container_content = True
        for div_basic_container_content in divs_basic_container_content :
            # Skip first basic_container_content div (header)...
            if first_div_basic_container_content :
                first_div_basic_container_content = False
                continue
            
            #
            div_basic_container_text = div_basic_container_content.find( "div", { "class" : "basic_container_text" } ) 
            
            # Game title
            div_gamepage_content_row_title = div_basic_container_text.find( "div" , { "class" : "gamepage_content_row_title" } )
            game_title                     = div_gamepage_content_row_title.a.string.strip().replace("&nbsp;", " ")

            #
            # Parts...
            #
            div_episode_segments_nn   = div_basic_container_text.find( "div", { "id" : self.EPISODE_SEGMENTS_RE } )
            divs_retro_part_title_bar = div_episode_segments_nn.findAll( "div", { "class" : "retro_part_title_bar" } )
            divs_gamepage_content_row = div_episode_segments_nn.findAll( "div", { "class" : "gamepage_content_row" } )
            
            for i in range(0, len( divs_retro_part_title_bar ) ) :
                div_retro_part_title_bar = divs_retro_part_title_bar[ i ]
                div_gamepage_content_row = divs_gamepage_content_row[ i ]
                
                # Title...
                part_title = div_retro_part_title_bar.div.a.string.strip()
                title      = "%s - %s" % ( game_title, part_title ) 
                
                # Thumbnail...
                div_gamepage_content_row_thumb = div_gamepage_content_row.find( "div", { "class" : "gamepage_content_row_thumb" } )
                thumbnail_url                  = div_gamepage_content_row_thumb.a.img[ "src" ]
                                
                # Video page URL...
                video_page_url = div_gamepage_content_row_thumb.a[ "href" ]
                
                # Date...
                div_gamepage_content_row_info = div_gamepage_content_row.find( "div", { "class" : "gamepage_content_row_info" } )
                div_gamepage_content_row_date = div_gamepage_content_row_info.find( "div", { "class" : "gamepage_content_row_date" } )
                date                          = div_gamepage_content_row_date.string.strip()
                
                # Plot...
                div_gamepage_content_row_text = div_gamepage_content_row_info.find( "div", { "class" : "gamepage_content_row_text" } )
                plot                          = div_gamepage_content_row_text.string.strip()
                
                # Add to list...
                listitem        = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail_url )
                listitem.setInfo( "video", { "Title" : title, "Studio" : "GameTrailers", "Genre" : date, "Plot" : plot } )
                plugin_play_url = '%s?action=play&video_page_url=%s' % ( sys.argv[ 0 ], urllib.quote_plus( video_page_url ) )
                xbmcplugin.addDirectoryItem( handle=int(sys.argv[ 1 ]), url=plugin_play_url, listitem=listitem, isFolder=False)     

        # Disable sorting...
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
        
        # Label (top-right)...
        xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category="%s" % self.plugin_category )
        
        # End of directory...
        xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
