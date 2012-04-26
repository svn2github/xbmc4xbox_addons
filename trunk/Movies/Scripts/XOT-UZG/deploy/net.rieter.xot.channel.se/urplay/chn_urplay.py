# coding:UTF-8
import sys
import urlparse

#===============================================================================
# Make global object available
#===============================================================================
import mediaitem
import contextmenu
import common
import chn_class
from helpers import datehelper
from helpers import subtitlehelper

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

register.RegisterChannel('chn_urplay')

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
        
        self.guid = "9F0F57D6-B897-11E0-AF2E-92314924019B"
        self.mainListUri = "http://urplay.se/series"
        self.baseUrl = "http://urplay.se/"
        self.icon = "urplayicon.png"
        self.iconLarge = "urplaylarge.png"
        self.noImage = "urplayimage.png"
        self.channelName = "Sveriges Utbildningsradio"
        self.channelDescription = u'Sändningar från UR Play'
        self.moduleName = "chn_urplay.py"
        self.sortOrder = 102
        self.language = "se"
        self.swfUrl = "http://urplay.se/jwplayer/player.swf"
        
        #self.backgroundImage = ""
        #self.backgroundImage16x9 = ""
        self.requiresLogon = False
        
        self.contextMenuItems = []
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using Mplayer", "CtMnPlayMplayer", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using DVDPlayer", "CtMnPlayDVDPlayer", itemTypes="video", completeStatus=True))
        
        
        self.episodeItemRegex = '<div class="serieslink"><a href="([^"]+)"[^>]+title="([^"]+)">([^<]+)</a>'
        #self.videoItemRegex = '<a href="([^"]+)"[^>]+title="([^"]+)">[\W\w]{0,200}?<img src="([^"]+)" [\w\W]{0,400}?<span class="productlistitemcontent">[^/]+</span>([^<]+)</span>\W+<span class="productbroadcastinfo">[^<]+ (\d{1,2}) (\w+) (\d{4}){0,1}'
        self.videoItemRegex = 'class="productlistitem[^"]+(tv|radio)">\W+<a href="([^"]+)" id="ctl00_Content_cltRepeaterPrograms[^>]+title="([^"]+)">[\W\w]{0,200}?<img src="([^"]+)" [\w\W]{0,400}?<span class="productlistitemcontent">[^/]+</span>([^<]+)</span>\W+<span class="productbroadcastinfo">'
        self.mediaUrlRegex = 'movieflashvars = "([^"]+)"'
        
        """ 
            The ProcessPageNavigation method will parse the current data using the pageNavigationRegex. It will
            create a pageItem using the CreatePageItem method. If no CreatePageItem method is in the channel,
            a default one will be created with the number present in the resultset location specified in the 
            pageNavigationRegexIndex and the url from the combined resultset. If that url does not contain http://
            the self.baseUrl will be added. 
        """
        # remove the &amp; from the url
        self.pageNavigationRegex = '<a href="([^"]+page=)(\d+)([^"]+relatedpage=1[^"]+)" title="[^"]+" [^>]+>\d+</a>'  
        self.pageNavigationRegexIndex = 1

        #========================================================================== 
        # non standard items
        self.categoryName = ""
        self.currentUrlPart = ""
        self.currentPageUrlPart = ""

        """
            Testcases:
            Anaconda Auf Deutch : RTMP, Subtitles
            Kunskapsdokument�r: folders, pages
            
        """
        
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
        
        item = mediaitem.MediaItem(resultSet[2], urlparse.urljoin(self.baseUrl, resultSet[0]))        
        item.description = resultSet[1]
        item.thumb = self.noImage
        item.icon = self.icon
        return item
    
#    def CreateFolderItem(self, resultSet):
#        """Creates a MediaItem of type 'folder' using the resultSet from the regex.
#        
#        Arguments:
#        resultSet : tuple(strig) - the resultSet of the self.folderItemRegex
#        
#        Returns:
#        A new MediaItem of type 'folder'
#        
#        This method creates a new MediaItem from the Regular Expression 
#        results <resultSet>. The method should be implemented by derived classes 
#        and are specific to the channel.
#         
#        """
#        
#        logFile.debug('starting CreateFolderItem for %s', self.channelName)
#        
#        title = resultSet[-1]
#        url = urlparse.urljoin(self.baseUrl, resultSet[0])
#        
#        item = mediaitem.MediaItem(title, url)
#        item.type = "folder"
#        item.complete = True
#        item.thumb = self.noImage
#        item.thumbUrl = resultSet[2]
#        return item
    
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
        
        logFile.debug('starting FormatVideoItem for %s', self.channelName)
        logFile.debug(resultSet)
        
        title = resultSet[-1]
        type = resultSet[0]
        
        if "radio" in type:
            title = "%s (Audio Only)" % (title, )
            
        url = urlparse.urljoin(self.baseUrl, resultSet[1])
        
        item = mediaitem.MediaItem(title, url)
        item.description = resultSet[2]
        item.thumb = self.noImage
        item.thumbUrl = resultSet[3]
        item.type = "video"
        item.icon = self.icon
        
#        day = resultSet[4]
#        month = resultSet[5]
#        month = datehelper.DateHelper.GetMonthFromName(month, "se", short=True)
#        year = resultSet[6]
#        if year == '':
#            year = datehelper.DateHelper.ThisYear()
#        item.SetDate(year, month, day)
        
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
        
        logFile.debug('starting UpdateVideoItem for %s (%s)', item.name, self.channelName)
        
        """
        <script type="text/javascript">/* <![CDATA[ */ var movieFlashVars = "
        image=http://assets.ur.se/id/147834/images/1_l.jpg
        file=/147000-147999/147834-20.mp4
        plugins=http://urplay.se/jwplayer/plugins/gapro-1.swf,http://urplay.se/jwplayer/plugins/sharing-2.swf,http://urplay.se/jwplayer/plugins/captions/captions.swf
        sharing.link=http://urplay.se/147834
        gapro.accountid=UA-12814852-8
        captions.margin=40
        captions.fontsize=11
        captions.back=false
        captions.file=http://undertexter.ur.se/147000-147999/147834-19.tt
        streamer=rtmp://streaming.ur.se/ondemand
        autostart=False"; var htmlVideoElementSource = "http://streaming.ur.se/ondemand/mp4:147834-23.mp4/playlist.m3u8?location=SE"; /* //]]> */ </script>

        """
        
        captions = ""
        data = uriHandler.Open(item.url, pb=False)
        resultSet = common.DoRegexFindAll(self.mediaUrlRegex, data)
        parts = resultSet[0].split("&")
        for part in parts:
            all = part.split("=")
            value = all[-1]
            key = all[0]
            logFile.debug("%s = %s", key, value)
            if key == "file":
                file = value
            elif key == "captions.file":
                captions = value
            elif key == "streamer":
                server = value    
        
        url = "%s/%s" % (server, file)
        url = self.GetVerifiableVideoUrl(url)
        
        if not captions == "":
            fileName = captions[captions.rindex("/")+1:] + ".srt"
            subtitle = subtitlehelper.SubtitleHelper.DownloadSubtitle(captions, fileName, "ttml")
        else:
            subtitle = None
        
        item.thumb = self.CacheThumb(item.thumbUrl)
        item.AppendSingleStream(url, 0, subtitle)
        item.complete = True
        return item