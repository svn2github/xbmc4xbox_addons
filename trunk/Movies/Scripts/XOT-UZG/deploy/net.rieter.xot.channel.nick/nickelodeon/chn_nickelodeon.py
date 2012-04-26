#===============================================================================
# Import the default modules
#===============================================================================
import sys
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

register.RegisterChannel('chn_nickelodeon', 'nickelodeon')
register.RegisterChannel('chn_nickelodeon', 'nickjr')

#===============================================================================
# main Channel Class
#===============================================================================
class Channel(chn_class.Channel):
    """
    main class from which all channels inherit
    """
    
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
        if self.channelCode == 'nickelodeon':         
            self.guid = "8D4EBAE8-F3C6-11DD-92EE-F2FE55D89593"
            self.icon = "nickelodeonicon.png"
            self.iconLarge = "nickelodeonlarge.png"
            self.noImage = "nickelodeonimage.png"
            self.channelName = "Nickelodeon"
            self.channelDescription = "Afleveringen van Nickelodeon"
            self.mainListUri = "http://www.nickelodeon.nl/shows"            
        elif self.channelCode == "nickjr":
            self.guid = "9AD5766A-BA08-11E0-BBC6-190D4824019B"
            self.icon = "nickelodeonicon.png"
            self.iconLarge = "nickjrlarge.png"
            self.noImage = "nickjrimage.png"
            self.channelName = "Nick Jr."
            self.channelDescription = "Afleveringen van Nickelodeon Junior"
            self.mainListUri = "http://www.nickelodeon.nl/kanalen/18"
        else:
            raise NotImplementedError("Unknown channel code")
        
        self.baseUrl = "http://www.nickelodeon.nl"
        self.onUpDownUpdateEnabled = True
        self.moduleName = "chn_nickelodeon.py"            
        self.sortOrder = 11
        self.language = "nl"            
        #
        
        self.contextMenuItems = []
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using Mplayer", "CtMnPlayMplayer", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using DVDPlayer", "CtMnPlayDVDPlayer", itemTypes="video", completeStatus=True))
                
        self.requiresLogon = False
        self.swfUrl = "http://media.mtvnservices.com/player/prime/mediaplayerprime.1.9.1.swf"
        
        self.episodeItemRegex = '<h3>([^<]+)</h3>\W+<a[\W\w]+?<a href="(/videos[^"]+)"' # used for the ParseMainList
        self.videoItemRegex = '<a href="(/videos/[^"]+)" class="preview">(?:<span[^>]+>[^>]+>\W+){0,1}<img alt="([^"]+)"[^>]+src="([^"]+/)([0-9a-f]+)(\d/[^"]+)"[^>]+/>\W+</a><div class=\'description\'>'   # used for the CreateVideoItem 
        #<a href="(/videos/[^"]+)" class="preview"><img alt="([^"]+)"[^>]+src="([^"]+/)([0-9a-f])(/[^"]+)"[^>]+/>
        #self.folderItemRegex = '<a href="\.([^"]*/)(cat/)(\d+)"( style="color:\s*white;"\s*)*>([^>]+)</a><br'  # used for the CreateFolderItem
        self.mediaUrlRegex = '<param name="src" value="([^"]+)" />'    # used for the UpdateVideoItem
        return True
        
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
        
        item = mediaitem.MediaItem(resultSet[0], "%s%s" % (self.baseUrl, resultSet[1]))
        item.thumb = self.noImage
        item.icon = self.icon
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
        self.UpdateVideoItem method is called if the item is focussed or selected
        for playback.
         
        """
        
        logFile.debug('starting CreateVideoItem for %s', self.channelName)
        
        
        url = "http://riptide.mtvnn.com/mediagen/%s" % (resultSet[3]) 
        item = mediaitem.MediaItem(resultSet[1], url)
        item.thumbUrl = "%s%s%s" % (resultSet[2], resultSet[3], resultSet[4])
        item.thumb = self.noImage
        item.icon = self.icon
        item.type = 'video'
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
        
        logFile.info('starting UpdateVideoItem for %s (%s)', item.name, self.channelName)
        
        item.thumb = self.CacheThumb(item.thumbUrl)
        data = uriHandler.Open(item.url, pb=False)
        
        rtmpUrls = common.DoRegexFindAll('<rendition[^>]+bitrate="(\d+)"[^>]*>\W+<src>([^<]+ondemand)/([^<]+)</src>', data)
        
        part = item.CreateNewEmptyMediaPart()
        for rtmpUrl in rtmpUrls:
            url = "%s/%s" % (rtmpUrl[1], rtmpUrl[2])
            bitrate = rtmpUrl[0]
            #convertedUrl = url.replace("ondemand/","ondemand?slist=")
            convertedUrl = self.GetVerifiableVideoUrl(url)
            part.AppendMediaStream(convertedUrl, bitrate)
        
        item.complete = True
        #logFile.debug("Media url: %s", item)
        return item