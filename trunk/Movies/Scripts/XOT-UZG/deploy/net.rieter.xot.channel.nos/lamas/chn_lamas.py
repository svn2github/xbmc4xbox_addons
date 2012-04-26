#===============================================================================
# Import the default modules
#===============================================================================
import re
import sys
import os
import urlparse
import xbmc
import xbmcgui

#===============================================================================
# Make global object available
#===============================================================================
import common
import mediaitem
import config
import controls
import contextmenu
import chn_class
from helpers import datehelper

logFile = sys.modules['__main__'].globalLogFile
uriHandler = sys.modules['__main__'].globalUriHandler

#===============================================================================
# register the channels
#===============================================================================
if (sys.modules.has_key('progwindow')):
    register = sys.modules['progwindow'].channelRegister
    #.channelRegister
elif (sys.modules.has_key('plugin')):
    register = sys.modules['plugin'].channelRegister

register.RegisterChannel('chn_lamas', 'delamas')

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
        
        self.guid = "9B43CA5A-42F3-11DD-9D91-B6F355D89593"
        self.icon = "lamasicon.png"
        self.iconLarge = "lamasiconlarge.png"
        self.noImage = "lamasimage.png"
        self.channelName = "De Lama's"
        self.channelDescription = "Al de clips en bonus materiaal van De Lama's site"
        self.moduleName = "chn_lamas.py"
        self.sortOrder = 255
        self.language = "nl"
        
        self.mainListUri = "http://sites.bnn.nl/page/lamazien/zoek/doemaarwat"
        self.baseUrl = "http://sites.bnn.nl"
        self.onUpDownUpdateEnabled = False
        
        self.contextMenuItems = []
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Update Item", "CtMnUpdateItem", itemTypes="video", completeStatus=False))            
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Download Item", "CtMnDownloadItem", itemTypes="video", completeStatus=True, plugin=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using Mplayer", "CtMnPlayMplayer", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using DVDPlayer", "CtMnPlayDVDPlayer", itemTypes="video", completeStatus=True))
        
        self.requiresLogon = False
        
        self.episodeItemRegex = "(?:<div class=\"button\"[^>]+href='(/page/lamazien/[^']+)';\">([^<]+)</div>|<a href=\"(/page/lamazien/zoek/[^\"]+)\">([^<]+)</a>)" # used for the ParseMainList
        self.videoItemRegex = """<li>\W+<strong>([^<]+)</strong>+[\w\W]+?onclick="location.href='([^']+)';[\W\w]+?<img src="([^"]+)"[\W\w]+?</div>\W+</div>\W+(?:<br /> )*([^<>]+)<br />(?:\W+<small>[^,]+, (\d+) (\w+) (\d+)</small>){0,1}"""   # used for the CreateVideoItem 
        self.folderItemRegex = ''  # used for the CreateFolderItem
        self.mediaUrlRegex = "'file', '([^']+\.flv)'"    # used for the UpdateVideoItem
        
        #========================================================================== 
        # non standard items
        self.topDescription = ""
        
        return True
      
    #==============================================================================
    # ContextMenu functions
    #==============================================================================
    def CtMnDownloadItem(self, item):
        item = self.DownloadVideoItem(item)

    def CreateEpisodeItem(self, resultSet):
        """Creates a new MediaItem for an episode
        
        Arguments:
        resultSet : list[string] - the resultSet of the self.episodeItemRegex
        
        Returns:
        A new MediaItem of type 'folder'
        
        This method creates a new MediaItem from the Regular Expression 
        results <resultSet>. The method should be implemented by derived classes 
        and are specific to the channel.
         
        """
        
        logFile.debug('starting CreateEpisodeItem for %s', self.channelName)
        
        name = resultSet[3]
        url = resultSet[2]
        if name == '':
            name = "-= %s =-" %  (resultSet[1], )
            url = resultSet[0]
        
        # dummy class
        item = mediaitem.MediaItem(name, urlparse.urljoin(self.baseUrl, url))
        item.complete = True
        item.icon = self.folderIcon
        return item
    
    def CreateVideoItem(self, resultSet):
        """
        Accepts an arraylist of results. It returns an item. 
        """
        logFile.debug(resultSet)
        
        item = mediaitem.MediaItem(resultSet[0], urlparse.urljoin(self.baseUrl, resultSet[1].replace(" ", "%20")))
        item.type = 'video'
        item.icon = self.icon
        
        # temp store the thumb for use in UpdateVideoItem
        item.thumbUrl = resultSet[2]
        item.thumb = self.noImage        
        item.description = resultSet[3]
                
        if not resultSet[4] == "":
            day = resultSet[4]
            month = resultSet[5]
            month = datehelper.DateHelper.GetMonthFromName(month, "nl", short=False)
            year = resultSet[6]
            item.SetDate(year, month, day)
        
        # getting the URL is part of the PlayVideo
        item.downloadable = True
        item.complete = False
        return item
    
    #============================================================================= 
    def UpdateVideoItem(self, item):
        """
        Accepts an item. It returns an updated item. Usually retrieves the MediaURL 
        and the Thumb!
        """
        #logFile.info('starting UpdateVideoItem for %s (%s)', item.name, self.channelName)
        
        item = chn_class.Channel.UpdateVideoItem(self, item)
        item.thumb = self.CacheThumb(item.thumbUrl)

        #logFile.info('finishing UpdateVideoItem: %s', item)
        
        #item.complete = True
        return item
        