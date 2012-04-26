#===============================================================================
# LICENSE XOT-Framework - CC BY-NC-ND
#===============================================================================
# This work is licenced under the Creative Commons 
# Attribution-Non-Commercial-No Derivative Works 3.0 Unported License. To view a 
# copy of this licence, visit http://creativecommons.org/licenses/by-nc-nd/3.0/ 
# or send a letter to Creative Commons, 171 Second Street, Suite 300, 
# San Francisco, California 94105, USA.
#===============================================================================

import sys
import re

from helpers import database
from config import Config
from proxyinfo import ProxyInfo 

#===============================================================================
# Make global object available
#===============================================================================
logFile = sys.modules['__main__'].globalLogFile
uriHandler = sys.modules['__main__'].globalUriHandler

def CleanupXml(xmlDoc):
    """Cleans up XML to make it look pretty
    
    Arguments:
    xmlDoc : string - the XML to cleanup
    
    """
    
    #cleanup
    prettyXml = xmlDoc.toprettyxml()
    #remove not needed lines with only whitespaces
    prettyXml = re.sub("(?m)^\s+[\n\r]", "", prettyXml, )
    
    prettyXml = re.sub("[\n\r]+\t+([^<\t]+)[\n\r]+\t+", "\g<1>", prettyXml)
    return prettyXml

def LoadFavorites(channel):
    """Reads the channel favorites into items.
    
    Arguments:
    channel : Channel - The channel for which the favorites need to be loaded.
    
    Returns:
    list of MediaItems that were marked as favorites.
     
    """
    
    try:
        db = database.DatabaseHandler()
        items = db.LoadFavorites(channel)
        for item in items:
            item.icon = channel.icon
    except:
        logFile.error("Settings :: Error loading favorites", exc_info=True)
           
    return items


def AddToFavorites(item, channel):
    """Adds an items to the favorites
    
    Arguments:
    item    : MediaItem - The MediaItem to add as favorite.
    channel : Channel   - The channel for which the favorites need to be loaded.
    
    """
    
    if item.url == "":
        logFile.warning("Settings :: Cannot add favorite without URL")
        return
    
    try:
        db = database.DatabaseHandler()
        db.AddFavorite(item.name, item.url, channel)
    except:
        logFile.error("Settings :: Error adding favorites", exc_info=True)
              

def RemoveFromFavorites(item, channel):
    """Removes an item from the favorites
    
    Arguments:
    item    : MediaItem - The MediaItem to be removed
    channel : Channel   - The channel for which it needs to be removed.
    
    """
    
    try:
        db = database.DatabaseHandler()
        db.DeleteFavorites(item.name, item.url, channel)
    except:
        logFile.error("Settings :: Error removing from favorites", exc_info=True)
    return

class AddonSettings:
    """Class for retrieving XBMC Addon settings"""
    
    # these are static properties that store the settings. Creating them each time is causing major slow-down
    __settings = None
    
    def __init__(self, *args, **kwargs):
        """Initialisation of the AddonSettings class.
        
        Arguments:
        args   : list - List of arguments
        
        Keyword Arguments:
        kwargs : list - List of keyword arguments 
        
        """
        
        #===============================================================================
        # Configuration ID's
        #===============================================================================
        self.STREAM_QUALITY = "stream_quality"
        self.NUMBER_OF_PAGES = "number_of_first_pages"
        self.SORTING_ALGORITHM = "sorting_algorithm"
        self.STREAM_BITRATE = "stream_bitrate"
        self.SUBTITLE_MODE = "subtitle_mode"
        self.PLUGIN_MODE = "plugin_mode"
        self.CACHE_ENABLED = "http_cache"
        self.BACKGROUND_CHANNELS = "background_channels"
        self.BACKGROUND_PROGRAMS = "background_programs"
        
        # the settings object
        #AddonSettings.__settings = xbmcaddon.Addon(id=self.ADDON_ID)
        if AddonSettings.__settings == None:
            logFile.debug("Loading Settings into static object")
            try:
                import xbmcaddon
                try:
                    # first try the version without the ID
                    AddonSettings.__settings = xbmcaddon.Addon()
                except:
                    logFile.warning("Settings :: Cannot use xbmcaddon.Addon() as settings. Falling back to  xbmcaddon.Addon(id)")
                    AddonSettings.__settings = xbmcaddon.Addon(id=Config.addonId)
            except:
                logFile.error("Settings :: Cannot use xbmcaddon.Addon() as settings. Falling back to xbmc.Settings(path)", exc_info=True)
                import xbmc
                AddonSettings.__settings = xbmc.Settings(path=Config.rootDir)
        return    
    
    def CacheHttpResponses(self):
        """ Returns True if the HTTP responses need to be cached """
        
        return self.__GetBooleanSetting(self.CACHE_ENABLED) 
    
    def GetDimPercentage(self):
        """ Returns the colordiffuse setting for the background dimmer""" 
        
        try:
            setting  = self.__GetSetting("dim_background")
            
            decValue = int(setting)
            decValue = int(decValue*1.0/100*254) + 1
            if decValue == 1:
                decValue = 0
        except:
            decValue = 0
        
        hexValue = hex(decValue)
        return "%sffffff" % (hexValue[2:])
        
    def GetMaxStreamBitrate(self):
        """Returns the maximum bitrate (kbps) for streams specified by the user"""
        
        setting = self.__GetSetting(self.STREAM_BITRATE)
        return int(setting)

    def UseSubtitle(self):
        """Returns whether to show subtitles or not"""
        
        setting = self.__GetSetting(self.SUBTITLE_MODE)
        
        if setting == "0":
            return True
        else:
            return False

    def BackgroundImageChannels(self):
        """Returns the filename or path for the background of the 
        program overview.
        """
        
        setting = self.__GetSetting(self.BACKGROUND_CHANNELS)        
        return setting
    
    def BackgroundImageProgram(self):
        """Returns the filename or path for the background of the 
        channel overview
        """
        
        setting = self.__GetSetting(self.BACKGROUND_PROGRAMS)        
        return setting

    def UseAdvancedPlugin(self):
        """Returns whether to use advanced playlist features in the plugin"""
        
        setting = self.__GetSetting(self.PLUGIN_MODE)        
        return setting == "true"

    def GetSortAlgorithm(self):
        """Retrieves the sorting mechanism from the settings
        
        Returns:
         * date - If sorting should be based on timestamps
         * name - If sorting should be based on names
        
        """
        
        setting = self.__GetSetting(self.SORTING_ALGORITHM)
        if setting == "0":
            return "name"
        elif setting == "1":
            return "date"
        else:
            return "none"

    def GetIPlayerProxy(self):
        """Returns the proxy server and port for iPlayer access"""
        
        server = self.__GetSetting("uk_proxy_server")
        if server == "":
            return None
        
        port = self.__GetSetting("uk_proxy_port")
        
        username = self.__GetSetting("uk_proxy_username")
        password = self.__GetSetting("uk_proxy_password")
        return ProxyInfo(server, port, username=username, password=password)
        

    def ShowChannelWithLanguage(self, languageCode):
        """Checks if the channel with a certain languageCode should be loaded.
        
        Arguments:
        languageCode : string - one of these language strings:
                                 * nl    - Dutch
                                 * se    - Swedish
                                 * lt    - Lithuanian
                                 * lv    - Latvian
                                 * ca-fr - French Canadian
                                 * ca-en - English Canadian
                                 * be    - Belgium
                                 * en-gb - British
                                 * None  - Other languages
                                 
        Returns:
        True if the channels should be shown. If the lookup does not match 
        a NotImplementedError is thrown.        
        
        """
        
        if languageCode == "nl":
            return self.__GetSetting("show_dutch") == "true"
        elif languageCode == "se":
            return self.__GetSetting("show_swedish") == "true"
        elif languageCode == "lt":
            return self.__GetSetting("show_lithuanian") == "true"
        elif languageCode == "lv":
            return self.__GetSetting("show_latvian") == "true"
        elif languageCode == "ca-fr":
            return self.__GetSetting("show_cafr") == "true"
        elif languageCode == "ca-en":
            return self.__GetSetting("show_caen") == "true"
        elif languageCode == "en-gb":
            return self.__GetSetting("show_engb") == "true"
        elif languageCode == "no":
            return self.__GetSetting("show_norwegian") == "true"
        elif languageCode == "be":
            return self.__GetSetting("show_belgium") == "true"
        elif languageCode == None:
            return self.__GetSetting("show_other") == "true"
        else:
            raise NotImplementedError("Language code not supported")
        
    def GetMaxNumberOfPages(self):
        """Returns the configured maximum number for pages to parse for 
        the mainlist.
        
        """
        
        return int(self.__GetSetting(self.NUMBER_OF_PAGES))
    
    def ShowSettings(self):
        """Shows the settings dialog"""
        
        #__language__ = __settings__.getLocalizedString
        #__language__(30204)              # this will return localized string from resources/language/<name_of_language>/strings.xml
        #__settings__.getSetting( "foo" ) # this will return "foo" setting value 
        #__settings__.setSetting( "foo" ) # this will set "foo" setting value
        AddonSettings.__settings.openSettings()      # this will open settings window
        self.GetMaxStreamBitrate()
        self.GetMaxNumberOfPages()  
        
        # clear the cache because stuff might have chanced
        logFile.info("Clearing Settings cache because settings dialog was shown.")
        return
    
    def __GetSetting(self, settingId): 
        """Returns the setting for the requested ID, from the cached settings.
        
        Arguments:
        settingId - string - the ID of the settings
        
        Returns:
        The configured XBMC add-on values for that <id>.
        
        """           
        
        value = AddonSettings.__settings.getSetting(settingId)
        
        #logFile.debug("Settings: %s = %s", id, value)
        return value   

    def __GetBooleanSetting(self, settingId):
        """ Arguments:
        id - string - the ID of the settings
        
        Returns:
        The configured XBMC add-on values for that <id>.
        
        """           
        
        setting = self.__GetSetting(settingId)
        return setting == "true"

    def __str__(self):
        """Prints the settings"""
        
        pattern = "%s\n%s: %s"        
        value = "%s: %s" % ("MaxNumberOfPages", self.GetMaxNumberOfPages())
        value = pattern % (value, "MaxStreamBitrate", self.GetMaxStreamBitrate())
        value = pattern % (value, "SortingAlgorithm", self.GetSortAlgorithm())
        value = pattern % (value, "DimPercentage", self.GetDimPercentage())
        value = pattern % (value, "UseSubtitle", self.UseSubtitle())
        value = pattern % (value, "UseAdvancedPlugin", self.UseAdvancedPlugin())
        value = pattern % (value, "CacheHttpResponses", self.CacheHttpResponses())
        value = pattern % (value, "IPlayerProxy", self.GetIPlayerProxy())
        value = pattern % (value, "Show Dutch", self.ShowChannelWithLanguage("nl"))
        value = pattern % (value, "Show Swedish", self.ShowChannelWithLanguage("se"))
        value = pattern % (value, "Show Lithuanian", self.ShowChannelWithLanguage("lt"))
        value = pattern % (value, "Show Latvian", self.ShowChannelWithLanguage("lv"))
        value = pattern % (value, "Show French Canadian", self.ShowChannelWithLanguage("ca-fr"))
        value = pattern % (value, "Show English Canadian", self.ShowChannelWithLanguage("ca-en"))
        value = pattern % (value, "Show British", self.ShowChannelWithLanguage("en-gb"))
        value = pattern % (value, "Show Other languages", self.ShowChannelWithLanguage(None))
        return value