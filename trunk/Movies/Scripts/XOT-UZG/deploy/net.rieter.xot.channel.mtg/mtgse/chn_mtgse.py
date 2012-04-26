# coding:UTF-8
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
elif (sys.modules.has_key('plugin')):
    register = sys.modules['plugin'].channelRegister
#register.channelButtonRegister.append(105)

register.RegisterChannel('chn_mtgse', 'sesport')
#register.RegisterChannel('chn_mtgse', 'tv3lt')
register.RegisterChannel('chn_mtgse', 'tv6lt')

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
        
        self.baseUrl = "http://viastream.player.mtgnewmedia.se/"
        self.requiresLogon = False
        self.moduleName = "chn_mtgse.py"
                
        if self.channelCode == "sesport":
            self.guid = "87533F2C-B759-11DE-A4E3-146355D89593"
            self.mainListUri = "http://viastream.player.mtgnewmedia.se/xml/xmltoplayer.php?type=siteMapData&channel=1se&country=se&category=0"
            self.icon = "sesporticon.png"
            self.iconLarge = "sesportlarge.png"
            self.noImage = "sesportimage.png"
            self.sortOrder = 109
            self.channelName = "Viasat Sport"
            self.channelDescription = u'Sändningar från viasatsport.se'
            self.language = "se"
               
        elif self.channelCode == "tv6lt":
            self.guid = "49A02D20-2283-11E0-8771-2AB7DFD72085"
            self.mainListUri = "http://viastream.viasat.tv/siteMapData/lt/19lt/0"
            self.icon = "tv6lticon.png"
            self.iconLarge = "tv6ltlarge.png"
            self.noImage = "tv6ltimage.png"
            self.sortOrder = 111
            self.channelName = "TV6.lt"
            self.channelDescription = u'TV6.lt web.tv'
            self.language = "lt"
        
        self.contextMenuItems = []
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using Mplayer", "CtMnPlayMplayer", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using DVDPlayer", "CtMnPlayDVDPlayer", itemTypes="video", completeStatus=True))
        
        
        self.episodeItemRegex = '<siteMapNode title="([^"]+)" id="([^"]+)" children="true"'
        self.videoItemRegex = '<ProductId>([^<]+)</ProductId>\W+<Title><!\[CDATA\[([^>]+)\]\]></Title>'
        self.folderItemRegex = '<siteMapNode title="([^"]+)" id="([^"]+)" children="([^"]+)" articles="[123456789]\d*"'
        self.mediaUrlRegex = '<param name="flashvars" value="pathflv\W*=\W*([^"]+)_definst_/([^"]+)\$start'
        
        """ 
            The ProcessPageNavigation method will parse the current data using the pageNavigationRegex. It will
            create a pageItem using the CreatePageItem method. If no CreatePageItem method is in the channel,
            a default one will be created with the number present in the resultset location specified in the 
            pageNavigationRegexIndex and the url from the combined resultset. If that url does not contain http://
            the self.baseUrl will be added. 
        """
        # remove the &amp; from the url
        self.pageNavigationRegex = 'link button-->\W+<li class="[^"]*"><a href="([^"]+)"[^>]+>(\d+)'  
        self.pageNavigationRegexIndex = 1

        #========================================================================== 
        # non standard items
        self.categoryName = ""
        self.currentUrlPart = ""
        self.swfUrl = "http://flvplayer.viastream.viasat.tv/flvplayer/play/swf/player.swf"
        
        return True
    
    def InitScript(self):
        """Initializes the channel for script use
        
        Returns: 
        The value of self.InitEpisodeList()
        
        """
        
        self.swfUrl = uriHandler.Header(self.swfUrl, self.proxy)[1]
        
        # call base
        return chn_class.Channel.InitScript(self)
    
    def InitPlugin(self):
        """Initializes the channel for plugin use
        
        Returns:
        List of MediaItems that should be displayed
        
        This method is called for each Plugin call and can be used to do some 
        channel initialisation. Make sure to set the self.pluginMode = True
        in this methode if overridden.
        
        """
        
        self.swfUrl = uriHandler.Header(self.swfUrl, self.proxy)[1]        
        
        # call base
        return chn_class.Channel.InitPlugin(self)
    
    #==============================================================================
    def PreProcessFolderList(self, data):
        """
        Accepts an data from the ProcessFolderList Methode, BEFORE the items are
        processed. Allows setting of parameters (like title etc). No return value!
        """
        _items = []
        
#        swfUrls = common.DoRegexFindAll('"([^"]+video\.swf)"', data) 
#        if len(swfUrls) > 0:
#            self.swfUrl = swfUrls[0]
#            logFile.debug("Setting SWF url to: %s", swfUrls[0])
#        
        return (data, _items)
    
    #==============================================================================
    def CreateEpisodeItem(self, resultSet):
        """
        Accepts an arraylist of results. It returns an item. 
        """
        if not self.channelCode == "sesport":
            url = self.mainListUri[0:len(self.mainListUri)-2] + resultSet[1]
        elif self.channelCode == "sesport":
            url = "http://viastream.player.mtgnewmedia.se/xml/xmltoplayer.php?type=siteMapData&channel=1se&country=se&category=%s" %(resultSet[1],)
            
        item = mediaitem.MediaItem(resultSet[0], url)
        item.description = resultSet[0]
        item.icon = self.icon
        return item
    
    #==============================================================================
    def CreateFolderItem(self, resultSet):
        if not self.channelCode == "sesport":
            url = "http://viastream.viasat.tv/Products/Category/%s" % (resultSet[1],)
        else:
            if resultSet[2] == "false":
                url = "http://viastream.player.mtgnewmedia.se/xml/xmltoplayer.php?type=Products&category=%s" % (resultSet[1],)
            else:        
                url = "http://viastream.player.mtgnewmedia.se/xml/xmltoplayer.php?type=siteMapData&channel=3se&country=se&category=%s" % (resultSet[1],)
            
        item = mediaitem.MediaItem(resultSet[0], url)
        item.thumb = self.noImage
        item.type = "folder"
        item.complete = True
        item.icon = self.folderIcon
        return item
    
    #============================================================================= 
    def CreateVideoItem(self, resultSet):
        """
        Accepts an arraylist of results. It returns an item. 
        """
        logFile.debug('starting FormatVideoItem for %s', self.channelName)
        
        if (self.channelCode == "sesport"):
            url = "http://viastream.player.mtgnewmedia.se/xml/xmltoplayer.php?type=Products&clipid=%s" % (resultSet[0],)
        else:
            url = "http://viastream.viasat.tv/Products/%s" % (resultSet[0],) #223950

        
        item = mediaitem.MediaItem(resultSet[1], url)
        item.type = "video"
        item.complete = False
        item.icon = self.icon
        return item
    
    #============================================================================= 
    def UpdateVideoItem(self, item):
        """
        Accepts an item. It returns an updated item. 
        """
        logFile.debug('starting UpdateVideoItem for %s (%s)', item.name, self.channelName)
        data = uriHandler.Open(item.url, pb=False)
        
        for description in common.DoRegexFindAll("<LongDescription><!\[CDATA\[([^<]+)\]\]", data):
            item.description = description
        
        for image in common.DoRegexFindAll("<Url>([^<]+)</Url>\W+</ImageMedia>", data):
            item.thumbUrl = image        
        item.thumb = self.CacheThumb(item.thumbUrl)
        
        for url in common.DoRegexFindAll("<Url>([^<]+)</Url>\W+</Video>", data):
            item.AppendSingleStream(url)

        # check for the geoblock parameter
        geoLocked = common.DoRegexFindAll("<geoblock>true</geoblock>", data)
        if len(geoLocked) > 0:
            logFile.debug("GeoBlock found, fetching real MediaUrls")
            for mediaItemPart in item.MediaItemParts:
                for stream in mediaItemPart.MediaStreams:
                    data = uriHandler.Open(stream.Url, pb=False)
                    for resultUrl in common.DoRegexFindAll("<url>([^<]+)</url>", data):
                        stream.Url = self.GetVerifiableVideoUrl(resultUrl)
        else:
            for mediaItemPart in item.MediaItemParts:
                for stream in mediaItemPart.MediaStreams:
                    stream.Url = self.GetVerifiableVideoUrl(stream.Url)
                
        item.complete = True
        logFile.debug("Found mediaurl: %s", item)
        return item