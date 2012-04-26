#===============================================================================
# Import the default modules
#===============================================================================
import xbmc, xbmcgui
import re, sys, os
import urlparse
#===============================================================================
# Make global object available
#===============================================================================
import common
import mediaitem
import config
import controls
import contextmenu
import chn_class

logFile = sys.modules['__main__'].globalLogFile
uriHandler = sys.modules['__main__'].globalUriHandler

#===============================================================================
# register the channels
#===============================================================================
if (sys.modules.has_key('progwindow')):
    register = sys.modules['progwindow'].channelRegister
elif (sys.modules.has_key('plugin')):
    register = sys.modules['plugin'].channelRegister

register.RegisterChannel('chn_tvnl', "tvnl")

#===============================================================================
# main Channel Class
#===============================================================================
class Channel(chn_class.Channel):
    """
    main class from which all channels inherit
    """
    
    #===============================================================================
    def InitialiseVariables(self):
        """
        Used for the initialisation of user defined parameters. All should be 
        present, but can be adjusted
        """
        # call base function first to ensure all variables are there
        chn_class.Channel.InitialiseVariables(self)
        
        self.guid = "1D6063B8-4BCF-11E0-AD8F-5533DFD72085"
        self.icon = "tvnlicon.png"
        self.iconLarge = "tvnllarge.png"
        self.noImage = "tvnlimage.png"
        self.channelName = "TV.NL"
        self.channelDescription = "Nederlandse TV streams using NL TV on Navi-X stream collection"
        self.sortOrder = 9
        self.language = "nl"
        
        self.moduleName = "chn_tvnl.py"            
        self.onUpDownUpdateEnabled = True
        self.requiresLogon = False
        
        self.contextMenuItems = []
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using Mplayer", "CtMnPlayMplayer", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using DVDPlayer", "CtMnPlayDVDPlayer", itemTypes="video", completeStatus=True))        
        return True
      
    #==============================================================================
    # Custom Methodes, in chronological order   
    #==============================================================================
    def ParseMainList(self):
        """ 
        accepts an url and returns an list with items of type CListItem
        Items have a name and url. This is used for the filling of the progwindow
        """        
        items = []
        if len(self.mainListItems) > 1:
            return self.mainListItems
        
        # read the regional ones
        dataPath = os.path.abspath(os.path.join(__file__, '..', 'data'))
        logFile.debug("TV streams located at: %s", dataPath)
        regionals = os.listdir(dataPath)
        for regional in regionals:
            path = os.path.join(dataPath, regional) 
            if not os.path.isdir(path):
                continue
            item = mediaitem.MediaItem(regional, path)
            item.complete = True
            item.icon = self.folderIcon
            items.append(item)
            pass
        
        # sort by name
        if self.episodeSort:
            items.sort()
                
        # add the National ones
        self.mainListItems = items
        return items
    
    #==============================================================================
    
    #==============================================================================
    def ProcessFolderList(self, item):
        logFile.debug("trying first items")
        url = item.url
        items = []
        
        stations = os.listdir(url)
        for station in stations:
            if not station.endswith(".m3u"):
                continue
            
            name = station.replace(".m3u", "")
            stream = os.path.join(url, station)
            stationItem = mediaitem.MediaItem(name, stream)
            stationItem.icon = os.path.join(url, "%s%s" % (name, ".tbn"))
            stationItem.complete = True
            stationItem.description = stationItem.name
            stationItem.AppendSingleStream(stream)
            stationItem.type = "video"
            stationItem.thumb = stationItem.icon
            items.append(stationItem)
            pass
        
        return items