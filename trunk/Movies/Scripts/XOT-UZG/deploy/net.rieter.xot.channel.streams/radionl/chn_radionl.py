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

register.RegisterChannel('chn_radionl', "radionl")

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
        
        self.guid = "341BFEA0-2312-11DF-B6B1-B7B256D89593"
        self.icon = "veronicaicon.png"
        self.iconLarge = "radionllarge.png"
        self.noImage = "veronicaimage.png"
        self.channelName = "RadionNL"
        self.channelDescription = "Alle Nederlandse radio's using BigFoot87's stream collection"
        self.sortOrder = 9
        self.language = "nl"
        
        self.moduleName = "chn_radionl.py"            
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
        logFile.debug("Radio stations located at: %s", dataPath)
        regionals = os.listdir(os.path.join(dataPath, "Regionale Omroepen"))
        for regional in regionals:
            path = os.path.join(dataPath, "Regionale Omroepen", regional) 
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
        item = mediaitem.MediaItem("Nationale Radiozenders", os.path.join(dataPath))
        item.icon = self.folderIcon
        item.complete = True
        items.insert(0, item)
        
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
            if not station.endswith(".strm"):
                continue
            
            name = station.replace(".strm", "")
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