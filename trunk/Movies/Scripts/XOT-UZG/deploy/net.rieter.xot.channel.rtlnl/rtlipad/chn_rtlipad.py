import sys 
import os

#===============================================================================
# Make global object available
#===============================================================================
import mediaitem
import contextmenu
import chn_class
import common

from config import Config
from helpers import xmlhelper
from envcontroller import Environments

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

register.RegisterChannel('chn_rtlipad')

#===============================================================================
# main Channel Class
#===============================================================================
class Channel(chn_class.Channel):
    #===============================================================================
    # define class variables
    #===============================================================================
    def InitialiseVariables(self):
        """Used for the initialisation of user defined parameters. 
        
        All should be present, but can be adjusted. If overridden by derived class
        first call chn_class.Channel.InitialiseVariables(self) to make sure all
        variables are initialised. 
        
        Returns:
        True if OK
        
        """
        
        # call base function first to ensure all variables are there
        chn_class.Channel.InitialiseVariables(self)
        
        self.guid = "DE960970-70D3-11DF-B47C-FC51DFD72085"
        # get mainListUri from: http://www.rtl.nl/service/feed/ipad/xl/index.xml
        
        # if the self.mainListUriBase is filled, we get the complete list and cache it locally
        self.mainListUriBase = "http://adaptive.rtl.nl/xlFeedv2/m3u8/ipad/xmlm3u8"
        self.mainListUri = "http://adaptive.rtl.nl/xlFeedv2/m3u8/ipad/seriexml"
        
        self.baseUrl = "http://www.rtl.nl/service/gemist/device/ipad/feed/index.xml"
        self.icon = "rtlthumb.png"
        self.iconLarge = "rtllarge.png"
        self.noImage = "rtlimage.png"
        self.channelName = "iRTL 4,5&7"
        self.channelDescription = "Uitzendingen van de zenders RTL 4,5,7 & 8 via de iPad feed (geen DRM)."
        self.moduleName = "chn_rtlipad.py"
        #self.compatiblePlatforms = Environments.Linux | Environments.OSX | Environments.Windows | Environments.ATV2 | Environments.IOS
        self.language = "nl"
        
        self.requiresLogon = False
        self.sortOrder = 5
        self.episodeSort = True       
        self.defaultPlayer = 'dvdplayer'        
        
        self.contextMenuItems = []
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using Mplayer", "CtMnPlayMplayer", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using DVDPlayer", "CtMnPlayDVDPlayer", itemTypes="video", completeStatus=True))
        
        if self.mainListUriBase == "":
            self.episodeItemRegex = '<serieitem>[\w\W]+?<serienaam>([^<]+)</serienaam>\W+<seriescoverurl>([^<]+)</seriescoverurl>\W+<itemsperserie_url>([^<]+)</'
        else:
            self.episodeItemRegex = '<item>([\w\W]+?)</item>'
        
        self.videoItemRegex = '(<item>([\w\W]+?)</item>)' 
        self.folderItemRegex = ''
        self.mediaUrlRegex = 'BANDWIDTH=(\d+)\d{3}[^\n]+\W+([^\n]+.m3u8)'
        
        #============================================================================== 
        # non standard items
        
        return True
    
    def ParseMainList(self):
        """ 
        accepts an url and returns an list with items of type CListItem
        Items have a name and url. This is used for the filling of the progwindow
        """
        
        if not self.mainListUriBase == "":
            logFile.info("Using Cached iRTL URL")
            # get all the items at once instead of using the short list of only series
            items = []
            if len(self.mainListItems) > 1:
                return self.mainListItems
            
            # due to a bug in Python, we can't get all the chuncked data, so we just get the first 1MB
            data = uriHandler.Open(self.mainListUriBase, proxy = self.proxy) #, bytes = 800*1024)   
            
            # store the file in the profile dir:
            xmlPath = os.path.join(Config.cacheDir, "rtlcache.xml")
            logFile.debug("Storing XML to %s", xmlPath)     
            xmlFile = open(xmlPath, "w")
            xmlFile.write(data)
            xmlFile.close()
            
            # set the new path
            self.mainListUri = "file:" + xmlPath.replace('\\', '/')
            logFile.debug("Setting MainListUri to %s", self.mainListUri)     
        
        # call the main method
        items = chn_class.Channel.ParseMainList(self)
        return items
    
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
        #logFile.debug("iRTL :: %s", resultSet)
            
        if self.mainListUriBase == "":            
            item = mediaitem.MediaItem(resultSet[0], resultSet[2])
            item.thumbUrl = resultSet[1]
            item.icon = self.folderIcon
        else:
            xmldata = xmlhelper.XmlHelper(resultSet)
            seriesKey = xmldata.GetSingleNodeContent("serieskey")
            title = xmldata.GetSingleNodeContent("serienaam")
            thumbnail = "http://www.rtl.nl/system/cover/ipad/%s" % (seriesKey, ) #xmldata.GetSingleNodeContent("thumbnail")
            date = xmldata.GetSingleNodeContent("broadcastdatetime")
            year = date[0:4]
            month = date[5:7]
            day = date[8:10]
            
            #logFile.debug("%s: %s-%s-%s", date, day, month, year)
            
            item = mediaitem.MediaItem(title, self.mainListUri + "?" + seriesKey)
            item.thumbUrl = thumbnail
            item.SetDate(year, month, day)
            
            logo = xmldata.GetSingleNodeContent("station")
            
            if logo.lower() in ("rtl4", "rtl5", "rtl7", "rtl8"):
                logo = "%sicon.png" % (logo,)
                fullLogoPath = self.GetImageLocation(logo)
                item.icon = fullLogoPath
            else:
                item.icon = self.folderIconlogo = "%sicon.png" % (logo,)        
            
        return item
    
    def CreateVideoItem(self, resultSet):
        """Creates a MediaItem of type 'video' using the resultSet from the regex.
        
        Arguments:
        resultSet : tuple (string) - the resultSet of the self.videoItemRegex
        
        Returns:
        A new MediaItem of type 'video' or 'audio' (despite the method's name)
        
        This method creates a new MediaItem from the Regular Expression 
        results <resultSet>. The method should be implemented by derived classes 
        and are specific to the channel.
        
        If the item is completely processed an no further data needs to be fetched
        the self.complete property should be set to True. If not set to True, the
        self.UpdateVideoItem method is called if the item is focussed or selected
        for playback.
         
        """

        #logFile.debug('Starting CreateVideoItem for %s', self.channelName)
        
        if not self.mainListUriBase == "": 
            selectedSeries = self.parentItem.url[self.parentItem.url.rfind("?")+1:]
        
        #logFile.debug("Selected Series Key: %s", selectedSeries)
        
        xml = resultSet[0]
        xmlData = xmlhelper.XmlHelper(xml)
        
        if not self.mainListUriBase == "": 
            seriesKey = xmlData.GetSingleNodeContent("serieskey")
            if not seriesKey == selectedSeries:
                return None
        
            logFile.debug("SeriesKey from parent (%s) is matched: %s", self.parentItem.url, selectedSeries)        
       
        name = "%s - %s" % (xmlData.GetSingleNodeContent("episodetitel"), xmlData.GetSingleNodeContent("title"))
        thumb = xmlData.GetSingleNodeContent("thumbnail")
        url = xmlData.GetSingleNodeContent("movie")
        date = xmlData.GetSingleNodeContent("broadcastdatetime")
        
        item = mediaitem.MediaItem(name, url)
        item.description = name
        item.icon = self.icon
        item.thumb = self.noImage
        item.thumbUrl = thumb
        item.type = 'video'
        
        item.SetDate(date[0:4], date[5:7], date[8:10])
        item.complete = False        
        return item
    
    def UpdateVideoItem(self, item):
        """Updates an existing MediaItem with more data.
        
        Arguments:
        item : MediaItem - the MediaItem that needs to be updated
        
        Returns:
        The original item with more data added to it's properties.
        
        Used to update none complete MediaItems (self.complete = False). This
        could include opening the item's URL to fetch more data and then process that 
        data or retrieve it's real media-URL. 
        
        The method should at least:
        * cache the thumbnail to disk (use self.noImage if no thumb is available).
        * set at least one MediaItemPart with a single MediaStream.
        * set self.complete = True.
        
        if the returned item does not have a MediaItemPart then the self.complete flag 
        will automatically be set back to False.
        
        """

        logFile.debug('starting UpdateVideoItem for %s (%s)',item.name, self.channelName)
        item.thumb = self.CacheThumb(item.thumbUrl)
        
        # load the details.
        playlistdata = uriHandler.Open(item.url)
        urls = common.DoRegexFindAll(self.mediaUrlRegex, playlistdata)
        
        # baseUrl from: http://us.rtl.nl/Thu14.RTL_D_110818_143155_190_Britt_Ymke_op_d.MiMe.ssm/Thu14.RTL_D_110818_143155_190_Britt_Ymke_op_d.MiMe.m3u8
        baseUrl = item.url[0:item.url.rfind("/")]
        logFile.debug("Using baseUrl: %s", baseUrl)
        
        part = item.CreateNewEmptyMediaPart()
        for url in urls:
            #logFile.debug(url)
            mediaUrl = "%s/%s" % (baseUrl, url[1])
            part.AppendMediaStream(mediaUrl, url[0])
            
        item.complete = True        
        return item