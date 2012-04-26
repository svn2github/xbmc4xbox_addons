#===============================================================================
# Import the default modules
#===============================================================================
import xbmc 
import sys
import string
#===============================================================================
# Make global object available
#===============================================================================
import common
import mediaitem
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

register.RegisterChannel('chn_dumpert', 'dumpert')

#===============================================================================
# main Channel Class
#===============================================================================
class Channel(chn_class.Channel):
    #===============================================================================
    # define class variables
    #===============================================================================
    def InitialiseVariables(self):
        """
        Used for the initialisation of user defined parameters. All should be 
        present, but can be adjusted
        """
        # call base function first to ensure all variables are there
        chn_class.Channel.InitialiseVariables(self)
        
        self.guid = "80726A74-42F3-11DD-BBA6-A1F055D89593"
        self.icon = "dumperticon.png"
        self.iconLarge = "dumperticonlarge.png"
        self.noImage = "dumpertimage.png"
        self.backgroundImage = ""  # if not specified, the one defined in the skin is used
        self.backgroundImage16x9 = ""  # if not specified, the one defined in the skin is used
        self.channelName = "Dumpert.nl"
        self.channelDescription = "Fimpjes van Dumpert.nl"
        self.moduleName = "chn_dumpert.py"
        self.sortOrder = 255 #max 255 channels
        self.buttonID = 0
        self.onUpDownUpdateEnabled = True
        self.language = "nl"
        
        self.mainListUri = "http://www.dumpert.nl/%s/%s/"
        self.baseUrl = "http://www.dumpert.nl/mediabase/flv/%s_YTDL_1.flv.flv"
        self.playerUrl = ""
        
        self.contextMenuItems = []
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Download Item", "CtMnDownloadItem", itemTypes="video", completeStatus=True, plugin=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using Mplayer", "CtMnPlayMplayer", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using DVDPlayer", "CtMnPlayDVDPlayer", itemTypes="video", completeStatus=True))
        
        self.requiresLogon = False
        
        self.asxAsfRegex = '<[^\s]*REF href[^"]+"([^"]+)"' # default regex for parsing ASX/ASF files
        self.episodeSort = True
        self.videoItemRegex = '<a[^>]+href="([^"]+)"[^>]*>\W+<img src="([^"]+)[\W\w]{0,400}<h\d>([^<]+)</h\d>\W+<[^>]*date"{0,1}>(\d+) (\w+) (\d+) (\d+):(\d+)'
        self.folderItemRegex = ''  # used for the CreateFolderItem
        
        # Changed on 2008-04-23 self.mediaUrlRegex = "'(http://www.dumpert.nl/mediabase/flv/[^']+)'"    # used for the UpdateVideoItem
        self.mediaUrlRegex = ('data-vidurl="([^"]+)"',)    # used for the UpdateVideoItem
        
        return True
    
    #==============================================================================
    def ParseMainList(self):
        """ 
        accepts an url and returns an list with items of type CListItem
        Items have a name and url. This is used for the filling of the progwindow
        """
        items = []
        
        for page in range(1,3):
            item = mediaitem.MediaItem("Toppertjes - Pagina %s" % (page), self.mainListUri % ('toppers',page))
            item.icon = self.icon;
            items.append(item)                    
        
        for page in range(1,11):
            item = mediaitem.MediaItem("Filmpjes - Pagina %s" % (page), self.mainListUri % ('filmpjes',page))
            item.icon = self.icon;
            items.append(item)                    
        
        item = mediaitem.MediaItem("Zoeken", "searchSite")
        item.icon = self.icon;
        items.append(item)            
            
        return items
    
    #============================================================================= 
    def CreateVideoItem(self, resultSet):
        """
        Accepts an arraylist of results. It returns an item. 
        """
        #                         0              1             2                             3
        #<a class="item" href="([^"]+)"[^=]+="([^"]+)" alt="([^"]+)[^:]+<div class="date">([^<]+)
        logFile.debug('starting CreateVideoItem for %s', self.channelName)
        logFile.debug(resultSet)
        
        item = mediaitem.MediaItem(resultSet[2],resultSet[0], type='video')
        item.icon = self.icon;
        item.description = resultSet[2]
        item.thumb = self.noImage 
        item.thumbUrl = resultSet[1]   
        
        try:
            month = datehelper.DateHelper.GetMonthFromName(resultSet[4], "en")                            
            item.SetDate(resultSet[5], month, resultSet[3], resultSet[6], resultSet[7], 0)
        except:
            logFile.error("Error matching month: %s", resultSet[4].lower(), exc_info=True)
        
        item.complete = False
        item.downloadable = True
        return item
    
    #==============================================================================
    def UpdateVideoItem(self, item):        
        """
        Updates the item
        """
        item.thumb = self.CacheThumb(item.thumbUrl)
        
        data = uriHandler.Open(item.url, pb=False, proxy=self.proxy)
        
        for regex in self.mediaUrlRegex:
            results = common.DoRegexFindAll(regex, data)
            for result in results:
                if result != "":
                    item.AppendSingleStream(result)
                    break
            item.complete = True
            
        logFile.debug("VideoItem updated: %s", item)
        return item
    
    #==============================================================================
    def SearchSite(self, url=None):
        """
        Creates an list of items by searching the site
        """
        items = []
        
        keyboard = xbmc.Keyboard('')
        keyboard.doModal()
        if (keyboard.isConfirmed()):
            needle = keyboard.getText()
            if len(needle)>0:
                #convert to HTML
                needle = string.replace(needle, " ", "%20")
                searchUrl = "http://www.dumpert.nl/search/V/%s/ " % (needle)
                temp = mediaitem.MediaItem("Search", searchUrl)
                return self.ProcessFolderList(temp)
                
        return items
    
    #==============================================================================
    # ContextMenu functions
    #==============================================================================
    def CtMnDownloadItem(self, item):
        item = self.DownloadVideoItem(item)