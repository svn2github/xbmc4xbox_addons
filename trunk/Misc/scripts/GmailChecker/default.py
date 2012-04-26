
import os
import sys

__scriptname__ = "GmailChecker"
__author__ = "Amet"
__url__ = ""
__svn_url__ = "http://xbmc-addons.googlecode.com/svn/trunk/scripts/GmailChecker"
__credits__ = ""
__version__ = "0.5"
__XBMC_Revision__ = "22240"


BASE_RESOURCE_PATH = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'lib' ) )

sys.path.append (BASE_RESOURCE_PATH)

__language__ = xbmc.Language( os.getcwd() ).getLocalizedString


if __name__ == "__main__":
    import gui
    ui = gui.GUI( "script-GmailChecker-main.xml" , os.getcwd(), "Default")
    ui.doModal()
    del ui
    sys.modules.clear()
            
