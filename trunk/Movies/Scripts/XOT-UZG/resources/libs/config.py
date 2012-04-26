import os
import logging
import xml.dom.minidom

import xbmc

import envcontroller
from version import Version
    
class Config:
    """Class with all the configuration constants"""    
    
    try:
        import xbmcaddon
        # calling xbmcaddon.Addon() only works on newer XBMC's. Should see if it keeps working
        # if not, then the addonId should be hard coded here.
        __addon = xbmcaddon.Addon()
        __path = __addon.getAddonInfo('path')
        pathDetection = "addon.getAddonInfo('path')"
    except:
        print "XOT-Uzg.v3: using os.getcwd()"
        __path = os.getcwd()
        pathDetection = "os.getcwd()"
    
    # the XBMC libs return unicode info, so we need to convert this
    __path =  __path.decode('utf-8').encode('latin-1')
    
    # get rootDir, addonsDir and profileDir
    rootDir = __path.replace(";","")                    #: The root directory where XOT resides.
    addonDir = os.path.split(rootDir)[-1]               #: The add-on directory of XBMC.
    rootDir = os.path.join(rootDir, '')                 #: The root directory where XOT resides.
    
    # determine the profile directory, where user data is stored.
    if envcontroller.EnvController.IsPlatform(envcontroller.Environments.Xbox):
        profileDir = os.path.join(xbmc.translatePath("special://profile/script_data/"), addonDir)
    else:
        profileDir = os.path.join(xbmc.translatePath("special://profile/addon_data/"), addonDir)
    # the XBMC libs return unicode info, so we need to convert this
    profileDir = profileDir.decode('utf-8').encode('latin-1')
    
    cacheDir = os.path.join(profileDir,'cache','')      #: The cache directory.
    
    cacheValidTime = 7*24*3600                          #: Time the cache files are valid in seconds.
    webTimeOut = 30                                     #: Maximum wait time for HTTP requests.
    
    appName = "XOT-Uzg (XOT-Uzg.v3)"                    #: Name of the XOT application.
    appSkin = "uzg-progwindow.xml"                      #: Skin XML file for the channels overview window.
    appChannelSkin = "uzg-channelwindow.xml"            #: Skin XML file for the channel window.
    contextMenuSkin = "uzg-contextmenu.xml"             #: Skin XML file for the contextmenu.
    updaterSkin = "xot-updater.xml"                     #: Skin XML file for the updater window.
    skinFolder = ""                                     #: Current skin folder. This gets set from default.py
    
    logLevel = logging.DEBUG                            #: Minimum log level that is being logged.
    logDual = True                                      #: If True then exceptions are also logged in the XBMC logfile
    logFileName = "uzg.log"                             #: Filename of the log file of the script version
    logFileNamePlugin = "uzgPlugin.log"                 #: Filename of the log file of the plugin version
    
    xotDbFile = os.path.join(profileDir,"xot.db")       #: Filename of the XOT DB file 
    
    # must be single quotes for build script
    __addonXmlPath = os.path.join(rootDir, 'addon.xml')
    __addonXmlcontents = xml.dom.minidom.parse(__addonXmlPath)
    for addonentry in __addonXmlcontents.getElementsByTagName("addon"): 
        addonId = str(addonentry.getAttribute("id"))    #: The ID the addon has in XBMC (from addon.xml)
        __version = addonentry.getAttribute("version")  #: The Version of the addon (from addon.xml)
        Version = Version(version=__version)            #: The Version of the addon (from addon.xml) 
    
    updateUrl = "http://www.rieter.net/uitzendinggemist/index.php?currentversion="  #: The URL that is called to check for updates.     
                                                                                    #: should return "" if no update is available