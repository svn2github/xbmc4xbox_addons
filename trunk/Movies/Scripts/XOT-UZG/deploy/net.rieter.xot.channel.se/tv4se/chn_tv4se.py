# coding:UTF-8
import sys
#===============================================================================
# Make global object available 
#===============================================================================
import common
import mediaitem
import contextmenu
import chn_class
import proxyinfo
from helpers import htmlhelper
from helpers import smilhelper
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

register.RegisterChannel('chn_tv4se', 'tv4se')

#===============================================================================
# main Channel Class
#===============================================================================
class Channel(chn_class.Channel):
    #===============================================================================
    # define class variables
    #===============================================================================
    def InitialiseVariables(self):
        """Initialisation of the class. 
        
        WindowXMLDialog(self, xmlFilename, scriptPath[, defaultSkin, defaultRes]) -- Create a new WindowXMLDialog script.
    
        xmlFilename     : string - the name of the xml file to look for.
        scriptPath      : string - path to script. used to fallback to if the xml doesn't exist in the current skin. (eg os.getcwd())
        defaultSkin     : [opt] string - name of the folder in the skins path to look in for the xml. (default='Default')
        defaultRes      : [opt] string - default skins resolution. (default='720p')
        
        *Note, skin folder structure is eg(resources/skins/Default/720p)
        
        All class variables should be instantiated here and this method should not 
        be overridden by any derived classes.
        
        """
        
        # call base function first to ensure all variables are there
        chn_class.Channel.InitialiseVariables(self)
        
        self.guid = "98506F58-CD6F-11DE-99BA-187F55D89593"
        self.mainListUri = "http://www.tv4play.se/alla_program"
        self.baseUrl = "http://www.tv4play.se"
        self.icon = "tv4icon.png"
        self.iconLarge = "tv4large.png"
        self.noImage = "tv4image.png"
        self.channelName = "TV4"
        self.channelDescription = u'Sändningar från TV 4'
        self.moduleName = "chn_tv4se.py"
        self.sortOrder = 104
        self.defaultPlayer = 'dvdplayer' #(defaultplayer, dvdplayer, mplayer)
        self.language = "se"
        
        #self.backgroundImage = ""
        #self.backgroundImage16x9 = ""
        self.requiresLogon = False
        #self.swfUrl = "http://www.tv4play.se/polopoly_fs/1.939636.1281635185!approot/tv4video.swf"
        #self.swfUrl = "http://wwwb.tv4play.se/polopoly_fs/1.939636.1281635185!approot/tv4video.swf"
        #self.swfUrl = "http://www.tv4play.se/flash/tv4video.swf"
        self.swfUrl = "http://www.tv4play.se/flash/tv4playflashlets.swf"

        self.contextMenuItems = []
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using Mplayer", "CtMnPlayMplayer", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using DVDPlayer", "CtMnPlayDVDPlayer", itemTypes="video", completeStatus=True))
        
        
        self.episodeItemRegex = '<p class="video-picture">\W*<a href="([^"]+)">\W*<img alt="([^"]+)" src="([^"]+/)(\d+.\d+)(.\d+![^"]+)"'
        self.videoItemRegex = '<li class="video-panel[^"]*">([\W\w]*?)</div>\W+</li>'
        self.folderItemRegex = '<a href="/(search\?[^"]+;rows=)(\d+)([^"]+)\d+&amp;total_fetched=(\d+)" class="button"><span>([^<]+)'
        
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
        
        """
            Test cases: Wife-Swap - Uses AJAX method + Hela Programma folder
                        Leon - Uses NextButtonID + Hela Programma folder
                        FUSKBYGGARNA - Uses NextButtonID + folders + paging
                        Det okända - Uses new system
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
        
        #http://www.tv4play.se/search/partial?sorttype=date&categoryids=1.1844489&order=desc&rows=100&start=0
        #programId = resultSet[3]
        #url = "http://www.tv4play.se/search/partial?sorttype=date&categoryids=%s&order=desc&rows=200&start=0" % (programId,)
        #url = "http://www.tv4play.se/search/search?rows=200&order=desc&categoryids=%s&sorttype=date&start=0" % (programId,)
        url = "%s%s" % (self.baseUrl, resultSet[0])
        item = mediaitem.MediaItem(resultSet[1], url)
        item.icon = self.icon
        return item
    
    def PreProcessFolderList(self, data):
        """Performs pre-process actions for data processing/
        
        Arguments:
        data : string - the retrieve data that was loaded for the current item and URL. 
        
        Returns:
        A tuple of the data and a list of MediaItems that were generated.  
        
        
        Accepts an data from the ProcessFolderList method, BEFORE the items are
        processed. Allows setting of parameters (like title etc) for the channel. 
        Inside this method the <data> could be changed and additional items can 
        be created. 
        
        The return values should always be instantiated in at least ("", []).        
        
        """
        
        logFile.info("Performing Pre-Processing")
        items = []
        
        needle = '<div class="module-center-wrapper">'
        
        # there are more video sections, just take the first one.
        if (data.count(needle) > 1):
            data = data[0:data.rfind(needle)]
        
        logFile.debug("Pre-Processing finished")
        return (data, items)
    
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
        #logFile.debug("Content = %s", resultSet)
        
        htmlHelper = htmlhelper.HtmlHelper(resultSet)

        # the vmanProgramId (like 1019976) leads to http://anytime.tv4.se/webtv/metafileFlash.smil?p=1019976&bw=1000&emulate=true&sl=true        
        programId = common.DoRegexFindAll('<a href="[^>]+videoid=(\d+)">', resultSet)[0]
        #logFile.debug("ProgId = %s", programId)
        
        url = "http://anytime.tv4.se/webtv/metafileFlash.smil?p=%s&bw=1000&emulate=true&sl=true" % (programId,)
        
        name = htmlHelper.GetTagAttribute("img", {"alt":None})
        item = mediaitem.MediaItem(name, url)
        item.description = htmlHelper.GetTagContent("p",{"class":"video-description"})
        
        date = htmlHelper.GetTagContent("p", {"cls":"date"})
        dateParts = common.DoRegexFindAll("(\d+) (\w+) (\d+)", date)
        if len(dateParts) > 0:
            dateParts = dateParts[0]
            #logFile.debug(dateParts)
            
            try:
                month = datehelper.DateHelper.GetMonthFromName(dateParts[1], "se")
                item.SetDate(dateParts[2], month, dateParts[0])
            except:
                logFile.error("Cannot set date", exc_info = True)
        
        thumbUrl = htmlHelper.GetTagAttribute("img", {"src":None})
        if thumbUrl.find("source=") > 0:
            item.thumbUrl = thumbUrl[thumbUrl.index("source=")+7:]
        else:
            item.thumbUrl = thumbUrl
        
        premium = htmlHelper.GetTagContent("p", {"class":"premium"})
        if not (premium == ""):
            item.name = "%s [%s]" % (item.name, premium)
        elif "requires-authorization" in resultSet:
            item.name = "%s [Premium-innehåll]" % (item.name,)
        
        item.type = "video"
        item.complete = False
        item.icon = self.icon
        item.thumb = self.noImage
        
        return item
    
    def CreateFolderItem(self, resultSet):
        """Creates a MediaItem of type 'folder' using the resultSet from the regex.
        
        Arguments:
        resultSet : tuple(strig) - the resultSet of the self.folderItemRegex
        
        Returns:
        A new MediaItem of type 'folder'
        
        This method creates a new MediaItem from the Regular Expression 
        results <resultSet>. The method should be implemented by derived classes 
        and are specific to the channel.
         
        """
                
        logFile.debug('starting CreateFolderItem for %s', self.channelName)
        
        # http://www.tv4play.se/search?categoryids=1.1854778&amp;order=desc&amp;rows=8&amp;sorttype=date&amp;start=<value>
        
        currentValue = int(resultSet[1])
        newValue = int(resultSet[1]) + currentValue
        url = "%s/%s%s%s%s" % (self.baseUrl, resultSet[0], 24, resultSet[2], newValue)
        
        item = mediaitem.MediaItem(resultSet[4], url)
        item.thumb = self.noImage
        item.type = 'folder'
        item.complete = True
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
        C:\temp\rtmpdump-2.3>rtmpdump.exe -z -o test.flv -n "cp70051.edgefcs.net" -a "tv
        4ondemand" -y "mp4:/mp4root/2010-06-02/pid2780626_1019976_T3MP48_.mp4?token=c3Rh
        cnRfdGltZT0yMDEwMDcyNjE2NDYyNiZlbmRfdGltZT0yMDEwMDcyNjE2NDgyNiZkaWdlc3Q9ZjFjN2U1
        NTRiY2U5ODMxMDMwYWQxZWEwNzNhZmUxNjI=" -l 2
        
        C:\temp\rtmpdump-2.3>rtmpdump.exe -z -o test.flv -r rtmpe://cp70051.edgefcs.net/
        tv4ondemand/mp4root/2010-06-02/pid2780626_1019976_T3MP48_.mp4?token=c3RhcnRfdGlt
        ZT0yMDEwMDcyNjE2NDYyNiZlbmRfdGltZT0yMDEwMDcyNjE2NDgyNiZkaWdlc3Q9ZjFjN2U1NTRiY2U5
        ODMxMDMwYWQxZWEwNzNhZmUxNjI=
        """
        item.thumb = self.CacheThumb(item.thumbUrl)
        
        # retrieve the mediaurl
        data = uriHandler.Open(item.url, pb=False, proxy=self.proxy)
        
        #proxyInfo = proxyinfo.ProxyInfo("81.233.47.109", 8080, "http")
        #data = uriHandler.Open(item.url, pb=False, proxy=proxyInfo)
        
        smilHelper = smilhelper.SmilHelper(data)
        
        host = smilHelper.GetBaseUrl()
        videos = smilHelper.GetVideosAndBitrates()
        try:
            subTitleUrl = smilHelper.GetSubtitle()
        except:
            #TODO: Remove the Except after next release
            subTitleUrl = self.GetSubtitle(data)        
        
        if not videos:
            logFile.error("No Video Items where found. Perhaps this item is not available in the region or not free?")
            return item
        
        part = item.CreateNewEmptyMediaPart()
        
        if not subTitleUrl == "":
            part.Subtitle = subtitlehelper.SubtitleHelper.DownloadSubtitle(subTitleUrl) 
        
        for video in videos:
            url = "%s%s" % (host, smilHelper.StripTypeStart(video[0]))
            url = self.GetVerifiableVideoUrl(url)
            bitrate = int(video[1])/1000
            part.AppendMediaStream(url, bitrate)
            item.complete = True
        
        return item
    
    def GetSubtitle(self, data):
        """ Retrieves the URL of the included subtitle"""
        
        regex = '<param\W*name="subtitle"[^>]*value="([^"]+)'
        urls = common.DoRegexFindAll(regex, data)
        
        for url in urls:
            if "http:" in url:            
                return url
            else:
                return "%s/%s" % (self.GetBaseUrl().rstrip("/"), url.lstrip("/"))
        
        return ""