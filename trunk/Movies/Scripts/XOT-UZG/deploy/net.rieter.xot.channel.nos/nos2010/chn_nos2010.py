import sys
import time
import datetime
#===============================================================================
# Make global object available
#===============================================================================
import common
import mediaitem
import contextmenu
import chn_class
from helpers import xmlhelper
from helpers import encodinghelper
from helpers import mmshelper 
from helpers import subtitlehelper
from helpers import datehelper
import envcontroller

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

register.RegisterChannel('chn_nos2010', 'uzg')
register.RegisterChannel('chn_nos2010', 'zappelin')
register.RegisterChannel('chn_nos2010', 'zapp')
#register.RegisterChannel('chn_nos2010', 'ned2')
#register.RegisterChannel('chn_nos2010', 'ned3')
#register.RegisterChannel('chn_nos2010', 'zapp')

        
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
                
        try:
            # call base function first to ensure all variables are there
            chn_class.Channel.InitialiseVariables(self)
            
            self.noImage = "nosimage.png"
            self.baseUrl = "http://www.uitzendinggemist.nl"
            self.requiresLogon = False
            self.moduleName = "chn_nos2010.py"
            self.language = "nl"
            self.moduleName = "chn_nos2010.py"
                        
            if self.channelCode == "uzg":
                self.guid = "C2FB7F24-C5B5-11DF-A324-616DDFD72085"
                self.mainListUri = "%s/programmas" % (self.baseUrl,)
                self.icon = "uzgicon.png"
                self.iconLarge = "uzglarge.png"
                self.noImage = "nosimage.png"
                self.sortOrder = 0
                self.channelName = "Uitzendinggemist.nl"
                self.channelDescription = "Uitzendingen van de publieke zenders"
            
            elif self.channelCode == "zapp":
                self.guid = "F56E3AF0-2D9C-11E1-8F76-94484824019B"
                self.mainListUri = "%s/zapp" % (self.baseUrl,)
                self.icon = "zappicon.png"
                self.iconLarge = "zapplarge.png"
                self.noImage = "zapimage.png"
                self.sortOrder = 10
                self.channelName = "Z@pp"
                self.channelDescription = "Uitzendingen van Z@pp"
            
            elif self.channelCode == "zappelin":
                self.guid = "F67D4C1A-2D9C-11E1-8D9C-98484824019B"
                self.mainListUri = "%s/zappelin" % (self.baseUrl, )
                self.icon = "zappelinicon.png"
                self.iconLarge = "zappelinlarge.png"
                self.noImage = "zappelinimage.png"
                self.sortOrder = 10
                self.channelName = "Z@ppelin"
                self.channelDescription = "Uitzendingen van Z@ppelin"    
            
            self.contextMenuItems = []
            if envcontroller.EnvController.IsPlatform(envcontroller.Environments.Xbox):
                self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using Mplayer", "CtMnPlayMplayer", itemTypes="video", completeStatus=True))
                self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using DVDPlayer", "CtMnPlayDVDPlayer", itemTypes="video", completeStatus=True))
                
            self.contextMenuItems.append(contextmenu.ContextMenuItem("Download item", "CtMnDownload", itemTypes='video', completeStatus=True, plugin=True))
            self.contextMenuItems.append(contextmenu.ContextMenuItem("Refresh item", "CtMnRefresh", itemTypes="video", completeStatus=True))
        
            # these REGEXES are a mess, but we just need more to make shure all works.
        
            # used to catch the A-Z urls and latetly URLs
            episodeItemRegex1 = '<li><a href="/((?:programmas|zapp|zappelin)/[^"]+)"[^>]*title="Toon [^"]+">([^<])</a></li>'
            if self.channelCode == "uzg":
                episodeItemRegex2 = '<li><a href="/(weekarchief)/((\d+)-(\d+)-(\d+)|(\w+))">([^<]+)</a></li>'
            else:
                # no exta stuff needed for Z@pp and Z@ppelin
                episodeItemRegex2 = '(w)(w)(w)(w)(w)(w)(w)'                
            self.episodeItemRegex = '(?:%s|%s)' % (episodeItemRegex1, episodeItemRegex2)
            
            # regex for Top 50 and Weekoverview
            videoItemRegex2 = 'class="thumbnail" data-images="\[([^]]*)\]" [^>]+[\w\W]{0,400}?<h2><a[^>]+title="([^"]+)"[^\n]+\W{0,100}<h3><a href="/([^"]+)"[^>]+title="((?:[^"]+\(){0,1}(\w+ \d+ \w+ \d+, \d+:\d+)\){0,1})"'
            # regex for episodes details
            videoItemRegex3 = 'class="thumbnail" data-images="\[([^]]*)\]" [^>]+></a>\W+[\w\W]{0,800}?(?:<h2>\W*<a href="/afleveringen/\d+"[^>]+title="([^"]+)">[\w\W]{0,500}?){0,1}<h3[^>]*>\W*<a href="/([^"]+)"[^>]+title="((?:[^"]+\(){0,1}(\w+ \d+ \w+ \d+, \d+:\d+)\){0,1})">[\w\W]{0,400}</h3>([^<]+)'            
            self.videoItemRegex = '(?:%s|%s)' % (videoItemRegex2, videoItemRegex3)            
            
            # used for the A-Z indexes to parse the programms
            folderItemRegex1 = '<h2>\W*<a href="/programmas/(\d+)([^"]+)"[^>]*>([^<]+)</a>[\w\W]{0,400}?</h2>\W+<div[^>]+>\W+<a href="[^"]+">Bekijk laatste</a> \((?:(Geen)|\w+\W+(\d+) (\w+) (\d+), (\d+):(\d+))\)'
            # used for search results
            folderItemRegex2 = '<div class="wrapper">\W*<div class="img">\W*<a href="/(programma[^"]+)"[^<]+<img alt="([^"]+)" class="thumbnail" data-images="\[([^]]*)\]"[\w\W]{0,1000}?<div class="date">\w+ (\d+) (\w+) (\d+), (\d+):(\d+)'
            self.folderItemRegex = "(?:%s|%s)" % (folderItemRegex1, folderItemRegex2)
            
            """ 
                The ProcessPageNavigation method will parse the current data using the pageNavigationRegex. It will
                create a pageItem using the CreatePageItem method. If no CreatePageItem method is in the channel,
                a default one will be created with the number present in the resultset location specified in the 
                pageNavigationRegexIndex and the url from the combined resultset. If that url does not contain http://
                the self.baseUrl will be added. 
            """
            
            pageNavigatioRegex2 = ""
            self.pageNavigationRegex = '<a[^>]+href="([^"]+\?page=)(\d+)">\d+'             
            self.pageNavigationRegexIndex = 1
        except:
            logFile.debug("Error Initialising Varialbles for NOS", exc_info=True)
        #============================================================================== 
        # non standard items
        self.sortAlphabetically = True
        self.maxNumberOfFrontPages = 0
        self.md5Encoder = encodinghelper.EncodingHelper()
        self.environmentController = envcontroller.EnvController()
        self.securityCodes = None
        return True
    
    def InitPlugin(self):
        """Initializes the channel for plugin use
        
        Returns:
        List of MediaItems that should be displayed
        
        This method is called for each Plugin call and can be used to do some 
        channel initialisation. Make sure to set the self.pluginMode = True
        in this methode if overridden.
        
        """
        
        self.pluginMode = True
        self.__GetSecurityCode()
        return chn_class.Channel.InitPlugin(self)
    
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
        # get the security Codes
        self.__GetSecurityCode()
        
        # first do the basic stuff
        items = chn_class.Channel.ParseMainList(self, returnData=returnData)
        
        # we need to append some stuff
        top50 = mediaitem.MediaItem("Top 50 bekeken", "%s/top50" % (self.baseUrl,))
        top50.complete = True
        top50.icon = self.icon
        top50.thumb = self.noImage
        items.append(top50)
        
        search = mediaitem.MediaItem("Zoeken", "searchSite")
        search.complete = True
        search.icon = self.icon
        search.thumb = self.noImage
        items.append(search)
        
        return items
    
    def CreateEpisodeItem(self, resultSet):
        """
        Accepts an arraylist of results. It returns an item. 
        
        http://www.uitzendinggemist.nl/programmas/2.rss (programmaID)
        """
        #logFile.debug(resultSet)
        
        if (resultSet[0] != ''):
            name = "Alfabetisch's: %s" % (resultSet[1],)
            url = "%s/%s" % (self.baseUrl, resultSet[0])
        elif (resultSet[2] != ''):
            # specific stuff
            name = resultSet[8].capitalize()
            url = "%s/%s/%s?display_mode=list&herhaling=ja" % (self.baseUrl, resultSet[2], resultSet[3])            
        else:
            return None
        #url = "http://www.uitzendinggemist.nl/programmas/%s%s.rss" % (resultSet[0], resultSet[1])
        
        item = mediaitem.MediaItem(name, url)
        item.type = 'folder'
        item.icon = self.icon
        item.complete = True
        item.thumb = self.noImage
        
        if (resultSet[4] != ''):
            # date specified
            item.SetDate(resultSet[4], resultSet[5], resultSet[6])
            pass
        elif (resultSet[7] == 'vandaag'):
            now = datetime.date.today()                    
            item.SetDate(now.year, now.month, now.day)
        elif (resultSet[7] == 'gisteren'):
            now = datetime.date.today()                    
            now = now - datetime.timedelta(1)
            item.SetDate(now.year, now.month, now.day)
        
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
          
        if '<ul class="episodes" id="episode-results">' in data:
            # we need to strip the search results
            startIndex = data.index('<div id="series-slider">')
            data = data[startIndex+20:]
            endIndex = data.index('<div class="tabs_wrapper">')
            data = data[:endIndex]        
        
        logFile.debug("Pre-Processing finished")
        return (data, items)        
    
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
        #logFile.debug(resultSet)
        
        if (resultSet[0] == ""):
            # search results
            name = resultSet[10]
            url = "%s/%s" % (self.baseUrl, resultSet[9],)
            item = mediaitem.MediaItem(name, url)
            item.type = 'folder'
            item.icon = self.icon
            
            year = resultSet[14]
            month = resultSet[13]
            month = datehelper.DateHelper.GetMonthFromName(month, "nl")
            day = resultSet[12]
            hour = resultSet[15]
            minute = resultSet[16]
            item.SetDate(year, month, day, hour, minute, 0)
            
            thumbnails = resultSet[11]
            thumbUrl = self.__GetThumbUrl(thumbnails)
            if thumbUrl != "":
                item.thumbUrl = thumbUrl        
            
            item.thumb = self.noImage
            item.complete = True
            return item
        
        name = resultSet[2]
        #url = "http://www.uitzendinggemist.nl/programmas/%s%s.rss" % (resultSet[0], resultSet[1])
        # Let's not use RSS for now.
        url = "%s/programmas/%s%s" % (self.baseUrl, resultSet[0], resultSet[1])
        
        item = mediaitem.MediaItem(name, url)
        item.type = 'folder'
        item.icon = self.icon
        item.thumb = self.noImage
        item.complete = True
        
        # get the date
        try:
            month = datehelper.DateHelper.GetMonthFromName(resultSet[5], "nl") 
            
            day = resultSet[4]
            year = resultSet[6]
            #hour = resultSet[7]
            #min = resultSet[8]
            item.SetDate(year, month, day) #, hour, min, 0)
        except:
            logFile.error("Error resolving Month: %s", resultSet[4])

        return item
    
    def CreateVideoItem(self, resultSet):
        """
        Accepts an arraylist of results. It returns an item. 
        """
        #logFile.debug('starting CreateVideoItem for %s', self.channelName)        
        
        """
        http://player.omroep.nl/info/security/ geeft volgende item
        MTI4NTAwODUzMHxOUE9VR1NMIDEuMHxoNnJjbXNJZnxnb25laTFBaQ== -> SessionKey (via Convert.FromBase64String & Encoding.UTF8.GetString ) = 1285008530|NPOUGSL 1.0|h6rcmsIf|gonei1Ai -> split on "|"
                                                                                                                                           1285413107|NPOUGSL 1.0|h6rcmsIf|gonei1Ai
        aflid: 11420664
        AEAE45803625654A216FB8DF43BD9ACD = MD5 van aflid|sessionKey[1]
        Denk niet dat SessionKey[1] ooit veranderd? -> lijkt van niet
        
        http://player.omroep.nl/info/metadata/aflevering/11447726/5CE0A8F6DEAA0106C85C5286EA4F89E4
        http://player.omroep.nl/info/stream/aflevering/11447726/5CE0A8F6DEAA0106C85C5286EA4F89E4        
        """
      
        if resultSet[2] != "#" and resultSet[2] != "":
            # regex for Top 50 and Weekoverview
            logFile.debug("regex for Top 50 and Weekoverview")
            return self.__CreateVideoItem(resultSet[0], resultSet[1], resultSet[2], resultSet[3], resultSet[4], "")
        
        elif resultSet[7] != "#" and resultSet[7] != "":
            # regex for Searchresults and episodes
            logFile.debug("regex for Searchresults and episodes")
            return self.__CreateVideoItem(resultSet[5], resultSet[6], resultSet[7], resultSet[8], resultSet[9], resultSet[10])
        else:
            return None        
    
    def UpdateVideoItem(self, item):
        """
        Accepts an arraylist of results. It returns an item. 
        """
        
        if "gemi.st" in item.url:
            episodeId = common.DoRegexFindAll('http://gemi.st/(\d+)', item.url)[0]
        else:
            data = uriHandler.Open(item.url, proxy=self.proxy)
            episodeId = common.DoRegexFindAll('data-episode-id="(\d+)"', data)[0]
        logFile.debug("EpisodeId for %s: %s", item, episodeId)
        
        preHash = "%s|%s" % (episodeId, self.securityCodes[1])
        hash = encodinghelper.EncodingHelper.EncodeMD5(preHash)
        logFile.debug("Session Hash for '%s': %s (%s)", item, preHash, hash)
        
        metaUrl  = "http://pi.omroep.nl/info/metadata/aflevering/%s/%s" % (episodeId, hash)
        streamUrl = "http://pi.omroep.nl/info/stream/aflevering/%s/%s" % (episodeId, hash)
        
        metaData = uriHandler.Open(metaUrl, pb=False, proxy=self.proxy)
        streamData = uriHandler.Open(streamUrl, pb=False, proxy=self.proxy)
        
        # now we need to get extra info from the data
        metaXml = xmlhelper.XmlHelper(metaData)
        
        item.description = metaXml.GetSingleNodeContent('info')
        item.title = metaXml.GetSingleNodeContent('aflevering_titel')
        
        station = metaXml.GetSingleNodeContent('station')
        if station.startswith('nederland_1'):
            item.icon = self.GetImageLocation("1icon.png")
        elif station.startswith('nederland_2'):
            item.icon = self.GetImageLocation("2icon.png")
        elif station.startswith('nederland_3'):
            item.icon = self.GetImageLocation("3icon.png")
        logFile.debug("Icon for station %s = %s", station,  item.icon)
        
        # url
        #isApple = self.environmentController.IsPlatform("os x")
        isApple = True # Let's just always use the apple stream? = self.environmentController.IsPlatform("os x")
        #isApple = False # UZG added GEO checking by accident to the flash movies. So we must use WMV for now.
        if isApple:
            #urls = common.DoRegexFindAll('<stream compressie_formaat="(mov)" compressie_kwaliteit="(sb|bb|std)">\W+<serviceurl>[^>]+</serviceurl>\W+<streamurl>\W+/ceresflash/h264/+(1/[^m]+.m4v)', streamData)
            urls = common.DoRegexFindAll('<stream compressie_formaat="(mov)" compressie_kwaliteit="(sb|bb|std)">(?:\W+<serviceurl>[^>]+</serviceurl>){0,1}\W+<streamurl>\W+([^\n]+)', streamData)
        else:
            urls = common.DoRegexFindAll('<stream compressie_formaat="(wmv|wvc1)" compressie_kwaliteit="(sb|bb|std)">\W+<streamurl>\W+(http:[^?]+\?type=asx)', streamData)

        # get the subtitle
        subTitleUrl = self.__GetSubtitle(episodeId)
        subTitlePath = subtitlehelper.SubtitleHelper.DownloadSubtitle(subTitleUrl, episodeId + ".srt", format='sami')
        
        part = item.CreateNewEmptyMediaPart()
        part.Subtitle = subTitlePath
        
        for url in urls:
            if url[1] == "bb":
                bitrate = 500
            elif url[1] == "sb":
                bitrate = 220
            elif url[1] == "std":
                bitrate =  1000
            else:
                bitrate = None
            
            if isApple:
                #realUrl = realUrl = "rtsp://mp4streams.omroep.nl/ceres/%s" % url[2]
                realUrl = self.__GetAppleUrl(url[2])
            else:
                realUrl = mmshelper.MmsHelper.GetMmsFromAsx(url[2])
            
            part.AppendMediaStream(realUrl, bitrate=bitrate)
        
        #<image size="380x285" ratio="4:3">http://u.omroep.nl/n/a/2010-12/380x285_boerzoektvrouw_yvon.png</image>
        thumbUrl = metaXml.GetSingleNodeContent('original_image')#, {"size": "380x285"}, {"ratio":"4:3"})
        thumbUrl = "http://u.omroep.nl/n/a/%s" % (thumbUrl,) 
        item.thumb = self.CacheThumb(thumbUrl)
        logFile.debug(thumbUrl)
        
        item.complete = True
        return item
                
    def SearchSite(self, url=None):
        """Creates an list of items by searching the site
        
        Returns:
        A list of MediaItems that should be displayed.
        
        This method is called when the URL of an item is "searchSite". The channel
        calling this should implement the search functionality. This could also include
        showing of an input keyboard and following actions. 
        
        """
        
        url = "%s/zoek/programmas?id=%s&series_page=1" % (self.baseUrl, "%s") 
        return chn_class.Channel.SearchSite(self, url)
    
    def CtMnDownload(self, item):
        """ downloads a video item and returns the updated one
        """
        item = self.DownloadVideoItem(item)
 
    def __CreateVideoItem(self, thumbnails, showName, url, episodeName, datestring, description):
        """ Creates a MediaItem for the given values
        
        Arguments:
        thumbnails  : string - a list of thumbnails in the format: 
                               &quot;<URL>&quot;,&quot;<URL>&quote;
        showName    : string - the name of the main show
        episodeName : string - the name of the episode
        datestring  : string - datetime in the format: 'di 20 dec 2011, 12:00'
        description : string - description of the show
        
        Returns a new MediaItem
        
        """
        
        #logFile.debug("thumbnails: %s\nshowName: %s\nurl: %s\nepisodeName: %s\ndatestring: %s\ndescription: %s", thumbnails, showName, url, episodeName, datestring, description)
        
        if showName:
            name = "%s - %s" % (showName, episodeName)
        else:
            name = episodeName
        url = "%s/%s" % (self.baseUrl, url)
        
        item = mediaitem.MediaItem(name, url)
        item.icon = self.icon
        item.type = 'video'
        item.complete = False
        item.description = description.strip()
        item.thumb = self.noImage
        
        # Date format: 'di 20 dec 2011, 12:00'
        #               012345678901234567890
        partList = common.DoRegexFindAll("\w+ (?P<day>\d+) (?P<month>\w+) (?P<year>\d+).+(?P<hour>\d+):(?P<minute>\d+)", datestring)
        for dateParts in partList:
            year = dateParts['year']
            month = dateParts['month']
            month = datehelper.DateHelper.GetMonthFromName(month, "nl")
            day = dateParts['day']
            hour = dateParts['hour']
            minute = dateParts['minute']
        item.SetDate(year, month , day, hour, minute, 0)
        
        thumbUrl = self.__GetThumbUrl(thumbnails)
        if thumbUrl != "":
            item.thumbUrl = thumbUrl
        
        item.complete = False
        return item
    
    def __GetThumbUrl(self, thumbnails):
        """ fetches the thumburl from an coded string
        
        Arguments:
        thumbnails  : string - a list of thumbnails in the format: 
                               &quot;<URL>&quot;,&quot;<URL>&quote;
        
        returns the URL of single thumb
        
        """
        
        # thumb splitting
        if len(thumbnails) > 0:
            thumbnails = thumbnails.split(';')
            #logFile.debug(thumbnails)
            thumbUrl = thumbnails[1].replace('140x79','280x158').replace('60x34','280x158').replace("&quot", "")
            #logFile.debug(thumbUrl)
        else:
            thumbUrl = ""
            
        return thumbUrl
    
    def __GetSecurityCode(self):
        """
        http://player.omroep.nl/info/security/ geeft volgende item
        MTI4NTAwODUzMHxOUE9VR1NMIDEuMHxoNnJjbXNJZnxnb25laTFBaQ== -> SessionKey (via Convert.FromBase64String & Encoding.UTF8.GetString ) = 1285008530|NPOUGSL 1.0|h6rcmsIf|gonei1Ai -> split on "|"
                                                                                                                                           1285413107|NPOUGSL 1.0|h6rcmsIf|gonei1Ai
        aflid: 11420664
        AEAE45803625654A216FB8DF43BD9ACD = MD5 van aflid|sessionKey[1]
        Denk niet dat SessionKey[1] ooit veranderd? -> lijkt van niet
        
        http://player.omroep.nl/info/metadata/aflevering/11447726/5CE0A8F6DEAA0106C85C5286EA4F89E4
        http://player.omroep.nl/info/stream/aflevering/11447726/5CE0A8F6DEAA0106C85C5286EA4F89E4                
        """
        
        data = uriHandler.Open("http://pi.omroep.nl/info/security/", proxy=self.proxy)
        xmlHelper = xmlhelper.XmlHelper(data)
        encryptedCodes = xmlHelper.GetSingleNodeContent("key")
        
        self.securityCodes = self.md5Encoder.DecodeBase64(encryptedCodes).split('|')       
        logFile.debug("NOS Uzg: Found SecurityCodes: %s from %s", self.securityCodes, encryptedCodes)
        return 
    
    def __GetAppleUrl(self, url):
        """
            gets the apple URL
            We replace /ceresflash/h264/1/vara/rest/2011/VARA_101249798/std.20110408.m4v with
            /ceresiphone/h264/1/vara/rest/2011/VARA_101249798/std.20110408.m4v            
        """
        
        if url.startswith("http:"):
            return url
        
        url = url.replace("ceresflash","ceresiphone")
        salt = "LA4DXOfn"
        hexTime = hex(int(time.time()+30))[2:]
        total = "%s%s%s" % (salt, url, hexTime)
        md5 = encodinghelper.EncodingHelper.EncodeMD5(total, toUpper=False)
        return "http://download.omroep.nl%s?md5=%s&t=%s" % (url, md5, hexTime)
    
    def __GetSubtitle(self, streamId):
        # security = 1285413107|NPOUGSL 1.0|h6rcmsIf|gonei1Ai
        #                0            1        2        3
        hexCode = str(hex(int(self.securityCodes[0]))[2:])
        passCode = str(self.securityCodes[3])
        streamPart = "aflevering/%s/format/sami" % (streamId,)
        preMd5 = passCode + streamPart + hexCode + 'embedplayer'
        md5 = encodinghelper.EncodingHelper.EncodeMD5(preMd5)
        url = 'http://ea.omroep.nl/tt888/embedplayer/' + str(md5).lower() + '/' + hexCode + '/' + streamPart        
        return url
        
        
        """
        if (!(subtitleUrlHashMethod == "none"))
                {
                    if ((subtitleUrlHashMethod == "subtitleSilverlightSecurity1") && ((Session.sessionKey != null) && (Session.sessionKey.Length > 3)))
                    {
                        int result = 0;
                        int.TryParse(Session.sessionKey[0], out result);
                        int num2 = result + DataControl.videoController.InitDuration;
                        string str4 = num2.ToString("X").ToLower();
                        string str5 = "aflevering/" + episodeId + "/format/sami";
                        string str7 = MD5Core.GetHashString(Session.sessionKey[3] + str5 + str4 + subtitleApplicationName).ToLower();
                        string str10 = episodeSubtitleUrl;
                        episodeSubtitleUrl = str10 + subtitleApplicationName + "/" + str7 + "/" + str4 + "/" + str5;
                    }
                }
                else
                {
                    episodeSubtitleUrl = episodeSubtitleUrl + episodeId;
                }        
        """
        """
        public static string GetStreamServiceUrlHash(string streamUrl, int timeStampSeconds)
        {
            if ((sessionKey != null) && (sessionKey.Length > 2))
            {
                int result = 0;
                int.TryParse(sessionKey[0], out result);
                string str = (result + timeStampSeconds).ToString("X");
                string hashString = MD5Core.GetHashString(sessionKey[2] + streamUrl + str);
                return (DataControl.episodeCurrent.ServiceUrl + hashString + "/" + str + streamUrl);
            }
            return null;
        }
        """