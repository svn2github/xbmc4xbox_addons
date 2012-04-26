#
# Imports
#
from BeautifulSoup      import BeautifulSoup, SoupStrainer
from gametrailers_const import __settings__, __language__
from gametrailers_utils import HTTPCommunicator
import os
import re
import sys
import urllib
import urllib2
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
        self.DEBUG         = False
        
        # Parse parameters...
        params = dict(part.split('=') for part in sys.argv[ 2 ][ 1: ].split('&'))
        self.plugin_category = params[ "plugin_category" ]

        # Settings
        self.video_quality   = __settings__.getSetting ("video_quality")

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
        htmlData         = httpCommunicator.get( "http://www.gametrailers.com/show/gametrailers-tv" )

        #
        # Parse HTML response...
        #
        soupStrainer  = SoupStrainer( "div", { "class" : "show_left_content" } )
        beautifulSoup = BeautifulSoup( htmlData, parseOnlyThese=soupStrainer )
        
        #
        # Video episodes...        
        #
        div_show_seasons = beautifulSoup.findAll( "div", id=re.compile("show_season_\d") )
        for div_show_season_x in div_show_seasons :
            div_load_ep               = div_show_season_x.find( "div", { "id" : "load_ep" }, recursive=False )
            table_full_ep_display     = div_load_ep.find( "table", { "class" : "full_ep_display" }, recursive=False )
            table_full_ep_display_trs = table_full_ep_display.findAll( "tr", recursive=False )
            for table_full_ep_display_tr in table_full_ep_display_trs :
                table_full_ep_display_tr_tds = table_full_ep_display_tr.findAll( "td", recursive=False )
                
                #
                if len(table_full_ep_display_tr_tds) < 2 :
                    continue                
                else :
                    table_full_ep_display_tr_td2 = table_full_ep_display_tr_tds[ 1 ]
                    table_full_ep_display_tr_td3 = table_full_ep_display_tr_tds[ 2 ]
                    table_full_ep_display_tr_td4 = table_full_ep_display_tr_tds[ 3 ]
                
                # Title...
                title = table_full_ep_display_tr_td2.a.string.strip()
                
                # Video page URL...
                video_page_url = table_full_ep_display_tr_td2.a[ "href" ]
                
                # Parse tooltip area...
                div_tooltip              = table_full_ep_display_tr_td2.find( "div", { "class" : "tooltip" } )
                div_tooltip_table        = div_tooltip.table
                div_tooltip_table_trs    = div_tooltip_table.findAll( "tr" )
                div_tooltip_table_tr3    = div_tooltip_table_trs[ 2 ]
                div_tooltip_table_tr3_td = div_tooltip_table_tr3.td
                
                # Thumbnail...
                thumbnail     = div_tooltip_table_tr3_td.img[ "src" ]
                
                # Date...
                date_display  = table_full_ep_display_tr_td3.string.strip()
                
                # Overlay...
                if self.video_quality == "1" and table_full_ep_display_tr_td4.a.string == "HD" :
                    overlay = xbmcgui.ICON_OVERLAY_HD
                else :
                    overlay = xbmcgui.ICON_OVERLAY_NONE
    
                # Add to list...
                listitem        = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail )
                listitem.setInfo( "video", { "Title" : title, "Studio" : "GameTrailers", "Genre" : date_display, "Overlay" : overlay } )
                plugin_play_url = '%s?action=play&video_page_url=%s' % ( sys.argv[ 0 ], urllib.quote_plus( video_page_url ) )
                xbmcplugin.addDirectoryItem( handle=int(sys.argv[ 1 ]), url=plugin_play_url, listitem=listitem, isFolder=False)        
        
        # Disable sorting...
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
        
        # Label (top-right)...
        xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category="%s" % self.plugin_category )
        
        # End of directory...
        xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
