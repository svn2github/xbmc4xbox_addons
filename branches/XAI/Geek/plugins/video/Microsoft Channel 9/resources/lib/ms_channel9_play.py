#
# Imports
#
import os
import sys
import xbmc
import xbmcgui
import xbmcplugin
import xml.dom.minidom
import re
import urllib
from BeautifulSoup     import SoupStrainer 
from BeautifulSoup     import BeautifulSoup
from ms_channel9_utils import HTTPCommunicator

#
# Main class
#
class Main:
    #
    # Init
    #
    def __init__( self ) :
        #
        # Constants
        #
        self.DEBUG = False
        
        #
        # Parse parameters...
        #
        params = dict(part.split('=') for part in sys.argv[ 2 ][ 1: ].split('&'))
        
        self.video_page_url = urllib.unquote_plus( params[ "video_page_url" ] ) 

        #
        # Settings
        #
        self.video_players = { "0" : xbmc.PLAYER_CORE_AUTO,
                               "1" : xbmc.PLAYER_CORE_DVDPLAYER,
                               "2" : xbmc.PLAYER_CORE_MPLAYER }
        self.video_player  = xbmcplugin.getSetting ("video_player")
        
        self.english           = xbmc.Language (os.getcwd(), "English")
        self.video_format      = xbmcplugin.getSetting ("video_format")
        self.pref_video_format = (self.english.getLocalizedString(30301), 
                                  self.english.getLocalizedString(30302), 
                                  self.english.getLocalizedString(30303)) [int(self.video_format)]
        
        #
        # Play video...
        #
        self.playVideo()
    
    #
    # Play video...
    #
    def playVideo( self ) :
        if (self.DEBUG) :
            print "video_page_url = " + self.video_page_url

        #
        # Get current list item details...
        #
        title     = unicode( xbmc.getInfoLabel( "ListItem.Title"  ), "utf-8" )
        thumbnail =          xbmc.getInfoImage( "ListItem.Thumb"  )
        studio    = unicode( xbmc.getInfoLabel( "ListItem.Studio" ), "utf-8" )
        plot      = unicode( xbmc.getInfoLabel( "ListItem.Plot"   ), "utf-8" )
        genre     = unicode( xbmc.getInfoLabel( "ListItem.Genre"  ), "utf-8" )
        
        #
        # Show wait dialog while parsing data...
        #
        dialogWait = xbmcgui.DialogProgress()
        dialogWait.create( xbmc.getLocalizedString(30504), title )
        
        #
        # Get video URL...
        #
        video_url = self.getVideoUrl( self.video_page_url )
        
        if video_url == None :
            # Close wait dialog...
            dialogWait.close()
            del dialogWait
            
            # Message...
            xbmcgui.Dialog().ok( xbmc.getLocalizedString(30000), xbmc.getLocalizedString(30505) )
            return

        #
        # Play video...
        #
        playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
        playlist.clear()

        listitem = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail )
        listitem.setInfo( "video", { "Title": title, "Studio" : studio, "Plot" : plot, "Genre" : genre } )        
        playlist.add( video_url, listitem )

        # Close wait dialog...
        dialogWait.close()
        del dialogWait
        
        # Play video...
        xbmcPlayer = xbmc.Player( self.video_players[ self.video_player ] )
        xbmcPlayer.play( playlist )
        
    #
    # Get video URL
    #
    def getVideoUrl( self, video_page_url ):
        # 
        # Get HTML page...
        # 
        video_page_url   = "http://channel9.msdn.com%s" % video_page_url
        httpCommunicator = HTTPCommunicator()
        htmlData         = httpCommunicator.get( video_page_url )

        #                
        # Parse HTML response...
        #
        soupStrainer  = SoupStrainer( "ul", { "class" : "download" } )
        beautifulSoup = BeautifulSoup( htmlData, soupStrainer )
        
        #
        # Loop through video URLs and pick one...
        #
        video_url  = None
        
        # Preferred format...
        li_entries = beautifulSoup.findAll( "li" )
        for li_entry in li_entries :
            li_entry_a = li_entry.find( "a" )
            if li_entry_a != None :
                if li_entry_a.string == self.pref_video_format :
                    video_url = li_entry_a[ "href" ]
                    break

        # No preferred format found, pick any available...
        if video_url == None :
            for li_entry in li_entries :
                li_entry_a = li_entry.find( "a" )
                if li_entry_a != None :
                    format = li_entry_a.string
                    if format == self.english.getLocalizedString(30303) or \
                       format == self.english.getLocalizedString(30302) or \
                       format == self.english.getLocalizedString(30301) :
                        video_url = li_entry_a[ "href" ]
                        break

        #
        # Return value
        #
        return video_url

#
# The End
#