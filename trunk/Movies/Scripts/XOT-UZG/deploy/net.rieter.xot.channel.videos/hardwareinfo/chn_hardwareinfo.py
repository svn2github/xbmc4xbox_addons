import sys
import urllib

#===============================================================================
# Make global object available
#===============================================================================
import common
import mediaitem
#import contextmenu
import chn_class
from helpers import xmlhelper
from helpers import stopwatch
from helpers import htmlentityhelper

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
register.RegisterChannel('chn_hardwareinfo', '')
        
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
        
        self.guid = "DB6A5104-30B0-11E1-A995-AF324924019B"
        self.mainListUri = "http://gdata.youtube.com/feeds/api/users/hardwareinfovideo/uploads?max-results=1&start-index=1"
        self.baseUrl = "http://www.youtube.com"
        self.icon = "hardwareinfoicon.png"
        self.iconLarge = "hardwareinfolarge.png"
        self.noImage = "hardwareinfoimage.png"
        self.channelName = "Hardware.info"
        self.channelDescription = "Videos van Hardware.info"
        self.moduleName = "chn_hardwareinfo.py"
        
        self.requiresLogon = False
        self.sortOrder = 255
        
        self.episodeItemRegex = '<name>([^-]+) - (\d+)-(\d+)-(\d+)[^<]*</name>'
        self.videoItemRegex = '<entry>([\w\W]+?)</entry>' 
        self.folderItemRegex = ''
        self.mediaUrlRegex = ''
        
        """ 
            The ProcessPageNavigation method will parse the current data using the pageNavigationRegex. It will
            create a pageItem using the CreatePageItem method. If no CreatePageItem method is in the channel,
            a default one will be created with the number present in the resultset location specified in the 
            pageNavigationRegexIndex and the url from the combined resultset. If that url does not contain http://
            the self.baseUrl will be added. 
        """
        self.pageNavigationIndicationRegex = '<page>(\d+)</page>' 
        self.pageNavigationRegex = '<page>(\d+)</page>' 
        self.pageNavigationRegexIndex = 0 
       
        self.contextMenuItems = []
        #self.contextMenuItems.append(contextmenu.ContextMenuItem("Play Low (not available)", "CtMnPlayLow", itemTypes="video", completeStatus=True))            
        #self.contextMenuItems.append(contextmenu.ContextMenuItem("Play High (not available)", "CtMnPlayHigh", itemTypes="video", completeStatus=True))
        #self.contextMenuItems.append(contextmenu.ContextMenuItem("Play in MPlayer", "CtMnPlayMplayer", itemTypes="video", completeStatus=True, plugin=True))
        #self.contextMenuItems.append(contextmenu.ContextMenuItem("Refresh item", "CtMnRefresh", itemTypes="video", completeStatus=None))
        return True

    def ParseMainList(self, returnData=False):
        """Parses the mainlist of the channel and returns a list of MediaItems
        
        This method creates a list of MediaItems that represent all the different
        programs that are available in the online source. The list is used to fill
        the ProgWindow. 

        Keyword parameters:
        returnData : [opt] boolean - If set to true, it will return the retrieved
                                     data as well

        Returns a list of MediaItems that were retrieved.
        
        """
        
        if len(self.mainListItems) > 1:
            if self.episodeSort:
                # just resort again
                self.mainListItems.sort()
            
            if returnData:
                return (self.mainListItems, "")
            else:
                return self.mainListItems
        
        items = []
        
        # we need to create page items. So let's just spoof the paging. Youtube has 
        # a 50 max results per query limit.
        itemsPerPage = 50
        data = uriHandler.Open(self.mainListUri) 
        xml = xmlhelper.XmlHelper(data)
        nrItems = xml.GetSingleNodeContent("openSearch:totalResults")
        
        for index in range(1, int(nrItems), itemsPerPage):
            items.append(self.CreateEpisodeItem([index, itemsPerPage]))
            pass
        # Continue working normal!
        
        # sort by name
        if self.episodeSort:
            watch = stopwatch.StopWatch('Sort Timer', logFile)                
            items.sort() #lambda x, y: cmp(x.name.lower(), y.name.lower()))
            watch.Stop()
                
        self.mainListItems = items
        
        if returnData:
            return (items, data)
        else:
            return items
    
    def CreateEpisodeItem(self, resultSet):
        """
        Accepts an arraylist of results. It returns an item. 
        """
        #logFile.debug('starting CreateEpisodeItem for %s', self.channelName)
        
        url = "http://gdata.youtube.com/feeds/api/users/hardwareinfovideo/uploads?max-results=%s&start-index=%s" % (resultSet[1], resultSet[0])
        title = "Hardware Info TV %04d-%04d" % (resultSet[0], resultSet[0] + resultSet[1])
        item = mediaitem.MediaItem(title, url)
        item.complete = True
        item.icon = self.icon
        item.thumb = self.noImage
        return item
    
    def CreateVideoItem(self, resultSet):
        """
        Accepts an arraylist of results. It returns an item. 
        """
        
        xmlData = xmlhelper.XmlHelper(resultSet)
                
        title = xmlData.GetSingleNodeContent("title")
        url = xmlData.GetTagAttribute("media:player", {'url' : None})
        #url = htmlentityhelper.HtmlEntityHelper.StripAmp(url)
        url = url.replace('&amp;feature=youtube_gdata_player','')
        
        item = mediaitem.MediaItem(title, url)
        item.icon = self.icon
        item.type = 'video'
        
        # date stuff
        date = xmlData.GetSingleNodeContent("published")
        year = date[0:4]
        month = date[5:7]
        day = date[8:10]    
        hour = date[11:13]
        minute = date[14:16]
        #logFile.debug("%s-%s-%s %s:%s", year, month, day, hour, minute)
        item.SetDate(year, month , day, hour, minute, 0)
        
        # description stuff
        description = xmlData.GetSingleNodeContent("media:description")
        item.description = description

        # thumbnail stuff
        thumbUrl = xmlData.GetTagAttribute("media:thumbnail", {'url' : None}, {'height' : '360'})
        # <media:thumbnail url="http://i.ytimg.com/vi/5sTMRR0_Wo8/0.jpg" height="360" width="480" time="00:09:52.500" xmlns:media="http://search.yahoo.com/mrss/" />
        if thumbUrl != "":
            item.thumbUrl = thumbUrl
        item.thumb = self.noImage
        
        # finish up
        item.complete = False
        return item
    
    def UpdateVideoItem(self, item):
        """
        Accepts an arraylist of results. It returns an item. 
        """
        
        data = uriHandler.Open(item.url, pb=False)
        streams = common.DoRegexFindAll('url=(http%3A%2F%2F[^,"]+)(\\\\u0026quality=)(\w+)([^,"]+itag=\d+)', data)
        
        part = None
        for stream in streams:
            # let's create a new part
            if part is None:
                part = item.CreateNewEmptyMediaPart()
            
            #logFile.debug(stream)
            
            if stream[2] == "hd1080":
                bitrate = 3750
            elif stream[2] == "hd720":
                bitrate = 2250
            elif stream[2] == "large":
                bitrate = 1250
            elif stream[2] == "medium":
                bitrate = 768
            elif stream[2] == "small":
                bitrate = 384
            else:
                bitrate = 0
            # See: http://adterrasperaspera.com/blog/2010/05/24/approximate-youtube-bitrates
            
            url = "%s" % (stream[0], )
            # TODO: change after the next XOT release
            #url = htmlentityhelper.HtmlEntityHelper.UrlDecode(url) 
            url = self.__UrlDecode(url)
            
            part.AppendMediaStream(url, bitrate) 
        
        item.thumb = self.CacheThumb(item.thumbUrl)          
        item.complete = True
        return item
                
    def CtMnDownload(self, item):
        """ downloads a video item and returns the updated one
        """
        item = self.DownloadVideoItem(item)
    
    def __UrlDecode(self, url):
        """Converts an URL encoded text in plain text
        
        Arguments: 
        url : string - the URL to decode.
        
        Returns:
        decoded URL like this.
        
        Example: '/%7econnolly/' yields '/~connolly/'.
        
        """
        
        if isinstance(url, unicode):
            return urllib.unquote(url.encode("utf-8")) 
        else:
            return urllib.unquote(url)