#
# Imports
#
import re
import sys
import xbmc
import xbmcgui
import xbmcplugin
import traceback
from xbmc4xbox_utils import HTTPCommunicator
from xbmc4xbox_utils import HTMLStripper

#
# Main class
#
class GUI( xbmcgui.WindowXMLDialog ):
    ACTION_EXIT_SCRIPT = ( 9, 10, 216, 257, 61448, )

    #
    #
    #
    def __init__( self, *args, **kwargs ):
        # Show dialog window...
        self.doModal()

    #
    #
    #
    def onInit( self ):
        #
        # Init
        #
        
        #
        # Wait...
        #        
        dialogProgress = xbmcgui.DialogProgress()
        dialogProgress.create( xbmc.getLocalizedString(30000), xbmc.getLocalizedString(30200) )

        try :            
            #
            # Get the news...
            #
            httpCommunicator = HTTPCommunicator()
            htmlData         = httpCommunicator.get( "http://www.xbmcsvn.com/")
    
            #
            # Look for DIV ID="dd3"...
            #
            regex       = re.compile("<div id=\"dd3\" .*?>(.*?)</div>")
            r           = regex.search(htmlData)
            output_text = r.groups()[0]
            
        #
        # Aw :(
        #
        except Exception :
            exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
            output_text = repr(traceback.format_exception(exceptionType, exceptionValue, exceptionTraceback))
        
        #
        # Output text...
        #
        self.getControl( 5 ).setText( output_text )
        
        #
        # Close progress dialog...
        #
        dialogProgress.close()

    #
    # onClick handler
    #
    def onClick( self, controlId ):
        pass

    #
    # onFocus handler
    #
    def onFocus( self, controlId ):
        pass

    #
    # onAction handler
    #
    def onAction( self, action ):
        if action and ( action in self.ACTION_EXIT_SCRIPT ):
            self.close()            
