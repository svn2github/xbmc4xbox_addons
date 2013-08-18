import os
import sys
import urllib
import xbmc
import xbmcgui
import datetime

class GUI( xbmcgui.WindowXMLDialog ):
    ACTION_EXIT_SCRIPT         = ( 9, 10, )
    TITLE_CONTROL_ID           = 30010
    DATE_CONTROL_ID            = 30020
    DESCRIPTION_CONTROL_ID     = 30030
    DOWNLOAD_CONTROL_ID        = 30040
    INSTALL_CONTROL_ID         = 30050

    #
    #
    #
    def __init__( self, *args, **kwargs ):
        # Constants
        self.IMAGES_DIR     = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'images' ) )          
        
        # Parse plugin parameters...
        self.params         = dict(part.split('=', 1) for part in sys.argv[ 2 ][ 1: ].split( '&' ))
        
        # Prepare parameter values...
        self.title           = urllib.unquote_plus( self.params[ "title" ] )
        self.link            = urllib.unquote_plus( self.params[ "link" ] )
        
        # Show dialog window...
        xbmcgui.WindowXML.__init__( self )
        self.doModal()

    #
    #
    #
    def onInit( self ):        
        # Name
        self.getControl( self.TITLE_CONTROL_ID ).setLabel( self.title )
        
        # Description
        self.getControl( self.DESCRIPTION_CONTROL_ID ).setText ( self.link )                                         # Description

        # Install / Cancel
        self.getControl( self.DOWNLOAD_CONTROL_ID ).setLabel( xbmc.getLocalizedString( 30500 ) )                     # Download
        self.getControl( self.INSTALL_CONTROL_ID  ).setLabel( xbmc.getLocalizedString( 30501 ) )                     # Install       

    #
    # onClick handler
    #
    def onClick( self, controlId ):
        # Download
        if ( controlId == self.DOWNLOAD_CONTROL_ID ) :
            self.close()
            
            xbmc.executebuiltin( "XBMC.RunPlugin(%s?action=build-download&title=%s&link=%s)" % \
                ( sys.argv[ 0 ], urllib.quote_plus( self.title ), 
                                 urllib.quote_plus( self.link ) ) )
            
        # Install
        if ( controlId == self.INSTALL_CONTROL_ID ) :
            self.close()

            xbmc.executebuiltin( "XBMC.RunPlugin(%s?action=build-install&title=%s&link=%s)" % \
                ( sys.argv[ 0 ], urllib.quote_plus( self.title ), 
                                 urllib.quote_plus( self.link ) ) )
        

    #
    # onFocus handler
    #
    def onFocus( self, controlId ):
        pass

    #
    # onAction handler
    #
    def onAction( self, action ):
        if ( action in self.ACTION_EXIT_SCRIPT ):
            self.close()
