import os
import sys
import urllib
import xbmc
import xbmcgui

class GUI( xbmcgui.WindowXMLDialog ):
    ACTION_EXIT_SCRIPT         = ( 9, 10, )
    NAME_CONTROL_ID            = 30010
    RATING_CONTROL_ID          = 30020
    XBOX_LABEL_CONTROL_ID      = 30030
    XBOX_VALUE_CONTROL_ID      = 30040
    DOWNLOADS_LABEL_CONTROL_ID = 30050
    DOWNLOADS_VALUE_CONTROL_ID = 30060
    DESCRIPTION_CONTROL_ID     = 30070
    SCREENSHOT_PREV_CONTROL_ID = 30081
    SCREENSHOT_WAIT_CONTROL_ID = 30082
    SCREENSHOT_IMG_CONTROL_ID  = 30083
    SCREENSHOT_NEXT_CONTROL_ID = 30084
    INSTALL_CONTROL_ID         = 30091
    CANCEL_CONTROL_ID          = 30092

    #
    #
    #
    def __init__( self, *args, **kwargs ):
        # Constants
        self.IMAGES_DIR     = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'images' ) )          
        
        # Parse plugin parameters...
        self.params         = dict(part.split('=', 1) for part in sys.argv[ 2 ][ 1: ].split( '&' ))
        
        # Prepare parameter values...
        self.name            = urllib.unquote_plus( self.params[ "name" ] )
        self.version         = urllib.unquote_plus( self.params[ "version" ] )
        self.downloads       =                      self.params[ "downloads" ]
        self.xbox_compatible =                      self.params[ "xbox_compat" ]
        self.rating          =                      self.params[ "rating" ]
        self.description     =                      self.params[ "description" ]
        self.screenshots     =                eval( self.params[ "screenshots" ] )
        self.download_url    = urllib.unquote_plus( self.params[ "download-url" ] )
        
        # Init
        self.screenshotIndex = 0
        self.screenshotLocal = "special://temp/xbmcsvn_skin_screenshot"

        # Show dialog window...
        xbmcgui.WindowXML.__init__( self )
        self.doModal()

    #
    #
    #
    def onInit( self ):        
        # Name
        self.getControl( self.NAME_CONTROL_ID ).setLabel( self.name + " " + self.version )                           # Name + version
        
        # Rating...
        self.getControl( self.RATING_CONTROL_ID ).setImage( os.path.join( self.IMAGES_DIR, "rating%s.png" % self.rating ) )
        
        # Xbox Compatible
        self.getControl( self.XBOX_LABEL_CONTROL_ID ).setLabel( "%s: " % "Xbox" )                                    # Xbox Compatible (label)
        self.getControl( self.XBOX_VALUE_CONTROL_ID ).setLabel( self.xbox_compatible )                               # Xbox Compatible (value)  
        
        # Downloads
        self.getControl( self.DOWNLOADS_LABEL_CONTROL_ID ).setLabel( "%s: " % xbmc.getLocalizedString(30300) )       # Downloads (label)
        self.getControl( self.DOWNLOADS_VALUE_CONTROL_ID ).setLabel( self.downloads )                                # Downloads (value)
        
        # Description
        self.getControl( self.DESCRIPTION_CONTROL_ID ).setText ( self.description )                                  # Description
        
        # Screenshot prev / next buttons...
        self.getControl( self.SCREENSHOT_PREV_CONTROL_ID ).setVisible( False )
        self.getControl( self.SCREENSHOT_NEXT_CONTROL_ID ).setVisible( len( self.screenshots ) > 1 )
        
        # Screenshot - Loading, please wait...
        self.getControl( self.SCREENSHOT_WAIT_CONTROL_ID ).setLabel( xbmc.getLocalizedString( 30301 ) )
        
        # Install / Cancel
        self.getControl( self.INSTALL_CONTROL_ID ).setLabel( xbmc.getLocalizedString( 30501 ) )                      #  Install
        self.getControl( self.CANCEL_CONTROL_ID  ).setLabel( xbmc.getLocalizedString( 30502 ) )                      # Cancel
        
        # Screenshot
        self.showScreenshot()

    #
    # onClick handler
    #
    def onClick( self, controlId ):
        # Previous screenshot...
        if ( controlId == self.SCREENSHOT_PREV_CONTROL_ID ) :
            self.screenshotIndex = self.screenshotIndex - 1            
            self.getControl( self.SCREENSHOT_PREV_CONTROL_ID ).setVisible( self.screenshotIndex > 0 )
            self.getControl( self.SCREENSHOT_NEXT_CONTROL_ID ).setVisible( self.screenshotIndex < len( self.screenshots ) - 1 )
            self.showScreenshot()

        
        # Previous screenshot...
        elif ( controlId == self.SCREENSHOT_NEXT_CONTROL_ID ) :
            self.screenshotIndex = self.screenshotIndex + 1
            self.getControl( self.SCREENSHOT_PREV_CONTROL_ID ).setVisible( self.screenshotIndex > 0 )
            self.getControl( self.SCREENSHOT_NEXT_CONTROL_ID ).setVisible( self.screenshotIndex < len( self.screenshots ) - 1 )
            self.showScreenshot() 
        
        # Install
        elif ( controlId == self.INSTALL_CONTROL_ID ) :
            self.close()
            self.cleanupExit()
                        
            xbmc.executebuiltin( "XBMC.RunPlugin(%s?action=skin-install&name=%s&version=%s&url=%s)" % \
                ( sys.argv[ 0 ], urllib.quote_plus( self.name ), urllib.quote_plus( self.version ), urllib.quote_plus( self.download_url ) ) )
        
        # Cancel
        elif ( controlId == self.CANCEL_CONTROL_ID ) :
            self.close()
            self.cleanupExit()

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
            self.cleanupExit()            

    #
    # Show screenshot...
    #
    def showScreenshot( self ):
        # Screenshot control...
        screenshotControl = self.getControl( self.SCREENSHOT_IMG_CONTROL_ID )
        screenshotControl.setVisible ( False )
        
        # Download screenshot image...
        localScreenshot = "special://temp/xbmcsvn_skin_screenshot"
        urllib.urlretrieve(self.screenshots[ self.screenshotIndex ], xbmc.translatePath( localScreenshot ) )
        
        # Show screenshot...
        screenshotControl.setImage( xbmc.translatePath( localScreenshot ) )
        screenshotControl.setVisible ( True )
        
    #
    # Cleanup
    #
    def cleanupExit( self ):
        # Cleanup
        os.remove( xbmc.translatePath( self.screenshotLocal ) )

