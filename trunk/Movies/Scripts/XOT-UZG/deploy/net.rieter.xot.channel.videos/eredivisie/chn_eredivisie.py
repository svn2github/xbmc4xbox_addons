#===============================================================================
# Import the default modules
#===============================================================================
import sys
import urlparse
import datetime

#===============================================================================
# Make global object available
#===============================================================================
import mediaitem
import common
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

register.RegisterChannel('chn_eredivisie', 'eredivisie')

#===============================================================================
# main Channel Class
#===============================================================================
class Channel(chn_class.Channel):
    """
    main class from which all channels inherit
    """
    
    def InitialiseVariables(self):
        """
        Used for the initialisation of user defined parameters. All should be 
        present, but can be adjusted
        """
        # call base function first to ensure all variables are there
        chn_class.Channel.InitialiseVariables(self)
        
        self.guid = "CC524DC0-C846-11E0-871B-984F4824019B"
        self.icon = "eredivisieicon.png"
        self.iconLarge = "eredivisielarge.png"
        self.noImage = "eredivisieimage.png"
        self.channelName = "Eredivisie Live"
        self.channelDescription = "Videos van de Eredivisie Live website."
        self.sortOrder = 13        
        self.baseUrl = "http://eredivisielive.nl/"                
        self.mainListUri = "http://eredivisielive.nl/video/"
        self.swfUrl = "http://static.eredivisielive.nl/static/swf/edPlayer-1.6.2.plus.swf"
        
        self.episodeItemRegex = '<a href="(/video/overzicht/competitie[^"]+|/video/overzicht/club/[^"]+)">[\w\W]+?>([^<]+)</span>\W+</a>'
        self.videoItemRegex = '<li class="video-item">\W+<a href="/video/(\d+)[^"]+">[\w\W]+?<img src="([^"]+)" [^>]+title="([^"]+)" />\W+<span class="date">(?:(\d+) (\w+) (\d+)|(vandaag|gisteren)) \w+ (\d+):(\d+)'
        self.mediaUrlRegex = '<media:content url="([^"]+)" bitrate="(\d+)"' 
        
        self.pageNavigationRegex = '<a class="page" href="([^>]+/)(\d+)(/)">' 
        self.pageNavigationRegexIndex = 1
            
        self.moduleName = "chn_eredivisie.py"            
        self.onUpDownUpdateEnabled = True
        self.requiresLogon = False
        self.language = "nl"
        
        self.contextMenuItems = []
        #self.contextMenuItems.append(contextmenu.ContextMenuItem("Download Item", "CtMnDownloadItem", itemTypes="video", completeStatus=True))  
        
        return True
        
    def CreateEpisodeItem(self, resultSet):
        """
        Accepts an arraylist of results. It returns an item. 
        """
        
        title = resultSet[1]
        url = urlparse.urljoin(self.baseUrl, resultSet[0])
        
        item = mediaitem.MediaItem(title, url)
        item.icon = self.icon
        item.thumb = self.noImage
        item.thumbUrl = self.noImage
        item.complete = True
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
        self.UpdateVideoItem method is called if the item is focused or selected
        for playback.
         
        """

        logFile.debug('starting CreateVideoItem for %s', self.channelName)
        
        url = "http://eredivisielive.nl/content/playlist/website/%s_ere_lr.xml" % (resultSet[0],)
        title = resultSet[2]
        img = resultSet[1]
        
        item = mediaitem.MediaItem(title, url)
        item.icon = self.icon
        item.description = title
        item.type = 'video'
        item.thumb = self.noImage
        item.thumbUrl = img
        
        # It could be that it reads: Vandaag (Today) instead of a date. Check that.
        if resultSet[6].lower() == "vandaag":
            # it was Vandaag, so set today 
            now = datetime.datetime.now()
            day = now.day 
            month = now.month
            year = now.year
        elif resultSet[6].lower() == "gisteren":
            yesterday = (datetime.datetime.now() - datetime.timedelta(1,0,0)) 
            day = yesterday.day 
            month = yesterday.month
            year = yesterday.year
        else:
            day = resultSet[3]        
            month = datehelper.DateHelper.GetMonthFromName(resultSet[4], "nl")
            year = resultSet[5]
        hour = resultSet[7]        
        minutes = resultSet[8]        
        item.SetDate(year, month, day, hour, minutes, 0)
        
        item.complete = False
        return item
    
    def CtMnDownloadItem(self, item):
        """ downloads a video item and returns the updated one
        """
        item = self.DownloadVideoItem(item)
    
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
        
        # rtmp://lb.streamgate.nl/vod/_definst_/content1/eredivisie/archief/END_36175_B.mp4 swfurl=http://static.eredivisielive.nl/static/swf/edPlayer-1.6.2.plus.swf swfvfy=true   
        
        data = uriHandler.Open(item.url, pb=False)
        
        mediaUrls = common.DoRegexFindAll(self.mediaUrlRegex, data)
        
        part = item.CreateNewEmptyMediaPart()
        for mediaUrl in mediaUrls:
            rtmp = "rtmp://lb.streamgate.nl/vod/_definst_/%s" % (mediaUrl[0],)
            rtmp = self.GetVerifiableVideoUrl(rtmp)
            part.AppendMediaStream(rtmp, mediaUrl[1])
        
        item.thumb = self.CacheThumb(item.thumbUrl)
        item.complete = True     
        return item