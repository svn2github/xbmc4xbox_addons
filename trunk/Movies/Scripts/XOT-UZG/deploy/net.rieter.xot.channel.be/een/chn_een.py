# coding:Cp1252
#===============================================================================
# Import the default modules
#===============================================================================
import sys
import urlparse
#===============================================================================
# Make global object available
#===============================================================================
import common
import mediaitem
import contextmenu
import chn_class

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

register.RegisterChannel('chn_een', 'een')

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
        
        self.guid = "16A5C86D-52C5-48C1-B894-1CC23EBF1CD8"
        self.icon = "eenicon.png"
        self.iconLarge = "eenlarge.png"
        self.noImage = "eenimage.png"
        self.channelName = "Eén"
        self.channelDescription = "Online uitzendingen van www.een.be."
        self.sortOrder = 120
        self.mainListUri = "http://www.een.be/mediatheek"
        self.baseUrl = "http://www.een.be"
        self.swfUrl = "http://www.een.be/sites/een.be/modules/custom/vrt_video/player/player_4.3.swf"
        
        self.episodeItemRegex = '<option value="(\d+)">([^<]+)</option>' # used for the ParseMainList
        self.videoItemRegex = '<li[^>]*>\W+<a href="([^"]+\/)(\d+)"[^<]+<img src="([^"]+)"[^<]*</a>\W+<h5><a[^>]+>([^<]+)</a>'
        #self.mediaUrlRegex = 'file\W*"([^"]+)"\W+streamer\W+"([^"]*?)(?:/)*"' 
        self.mediaUrlRegex = "(rtmpt*://[^']+)',file:\W*'([^']+)'"
        self.pageNavigationRegex = '<a href="([^"]+\?page=\d+)"[^>]+>(\d+)' 
        self.pageNavigationRegexIndex = 1
            
        self.moduleName = "chn_een.py"            
        self.language = "be"
        
        self.contextMenuItems = []
#        self.contextMenuItems.append(contextmenu.ContextMenuItem("Update Item", "CtMnUpdateItem", itemTypes="video", completeStatus=None))            
#        self.contextMenuItems.append(contextmenu.ContextMenuItem("Download Item", "CtMnDownloadItem", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using Mplayer", "CtMnPlayMplayer", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using DVDPlayer", "CtMnPlayDVDPlayer", itemTypes="video", completeStatus=True))        
        
        """Test cases:
        
        Laura: year is first 2 digits
        Koppen: year is first 2 and last 2
        
        """
        
        return True
      
    def CreateEpisodeItem(self, resultSet):
        """
        Accepts an arraylist of results. It returns an item. 
        """
        #logFile.debug('starting CreateEpisodeItem for %s', self.channelName)
        
        # dummy class
        url = "http://www.een.be/mediatheek/tag/%s"
        item = mediaitem.MediaItem(resultSet[1], url % (resultSet[0],))
        item.icon = self.icon
        item.type = "folder"
        item.complete = True
        return item
    
    def CreatePageItem(self, resultSet):
        """Creates a MediaItem of type 'page' using the resultSet from the regex.
        
        Arguments:
        resultSet : tuple(string) - the resultSet of the self.pageNavigationRegex
        
        Returns:
        A new MediaItem of type 'page'
        
        This method creates a new MediaItem from the Regular Expression 
        results <resultSet>. The method should be implemented by derived classes 
        and are specific to the channel.
         
        """
        #logFile.debug("Starting CreatePageItem")
        # we need to overwrite the page number, as the Een.be pages are zero-based.
        item = chn_class.Channel.CreatePageItem(self, (resultSet[0],''))
        item.name = resultSet[1]
        
        logFile.debug("Created '%s' for url %s", item.name, item.url)
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

        #http://www.een.be/mediatheek/ajax/video/531837

        url = "%sajax/video/%s" % (resultSet[0], resultSet[1])
        item = mediaitem.MediaItem(resultSet[3], urlparse.urljoin(self.baseUrl, url))
        
        item.thumbUrl = resultSet[2]
        item.thumb = self.noImage
        item.icon = self.icon        
        
        dateRegex = common.DoRegexFindAll("/(?:20(\d{2})_[^/]+|[^\/]+)/[^/]*_(\d{2})(\d{2})(\d{2})[_.]", item.thumbUrl)
        #logFile.debug("%s: %s", item.thumbUrl, dateRegex)        
        if (len(dateRegex) == 1):
            dateRegex = dateRegex[0]
            
            # figure out if the year is the first part
            year = dateRegex[0]
            if dateRegex[1] == year or year =="":
                # The year was in the path, so use that one. OR the year was not in the
                # path and we assume that the first part is the year
                item.SetDate(2000+int(dateRegex[1]), dateRegex[2], dateRegex[3])
            else:
                # the year was in the path and tells us the first part is the day.
                item.SetDate(2000+int(dateRegex[3]), dateRegex[2], dateRegex[1])
        item.type = 'video'
        item.complete = False
        return item
    
    #============================================================================= 
    def UpdateVideoItem(self, item):
        """
        Accepts an item. It returns an updated item. Usually retrieves the MediaURL 
        and the Thumb! It should return a completed item. 
        """
        logFile.info('starting UpdateVideoItem for %s (%s)', item.name, self.channelName)
        
        # rtmpt://vrt.flash.streampower.be/een//2011/07/1000_110723_getipt_neefs_wiels_Website_EEN.flv
        # http://www.een.be/sites/een.be/modules/custom/vrt_video/player/player_4.3.swf
        
        item.thumb = self.CacheThumb(item.thumbUrl)        
        
        # now the mediaurl is derived. First we try WMV
        data = uriHandler.Open(item.url, pb=False)
        
        descriptions = common.DoRegexFindAll('<div class="teaserInfo">(?:[\W\w])*?<p><a[^>]+>([^<]+)</a>', data)
        for desc in descriptions:
            item.description = desc
            
        urls = common.DoRegexFindAll(self.mediaUrlRegex, data)
        for url in urls:
            #mediaurl = "%s//%s" % (url[1],url[0])  # the extra slash in the url causes the application name in the RTMP stream to be "een" instead of "een/2011"
            mediaurl = "%s//%s" % (url[0],url[1])  # the extra slash in the url causes the application name in the RTMP stream to be "een" instead of "een/2011"
            mediaurl = mediaurl.replace(" ", "%20")
            mediaurl = self.GetVerifiableVideoUrl(mediaurl)
        
        if mediaurl != "":
            item.AppendSingleStream(mediaurl)
            item.complete = True
            #logFile.debug("Media url was found: %s", item)            
        else:
            logFile.debug("Media url was not found.")

        return item    
