#===============================================================================
# Import the default modules
#===============================================================================
import sys
import urlparse
import datetime
import cgi
#===============================================================================
# Make global object available
#===============================================================================
import common
import mediaitem
import contextmenu
import chn_class
from helpers import datehelper
from helpers import brightcovehelper

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

register.RegisterChannel('chn_sbsbrdcst', 'sbs')
register.RegisterChannel('chn_sbsbrdcst', 'net5')
register.RegisterChannel('chn_sbsbrdcst', 'veronica')

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
        
        if self.channelCode == 'veronica':
            self.guid = "01EE94CE-42F4-11DD-89C3-51FD55D89593"
            self.icon = "veronicaicon.png"
            self.iconLarge = "veronicalarge.png"
            self.noImage = "veronicaimage.png"
            self.channelName = "Veronica"
            self.channelDescription = "Uitzendingen op www.veronicatv.nl"
            self.sortOrder = 8
            self.mainListUri = "http://www.veronicatv.nl/ajax/programFilter/day/0/genre/all/block/gemist/range/%s"
            self.baseUrl = "http://www.veronicatv.nl"
            
        elif self.channelCode == 'sbs':
            self.guid = "0B5163FC-42F4-11DD-84D0-5DFE55D89593"
            self.icon = "sbs6icon.png"
            self.iconLarge = "sbs6large.png"
            self.noImage = "sbs6image.png"
            #self.backgroundImage = "background-sbs6.png"
            #self.backgroundImage16x9 = "background-sbs6-16x9.png"
            self.channelName = "SBS 6"
            self.channelDescription = "Online uitzendingen van www.SBS6.nl"
            self.sortOrder = 7
            self.mainListUri = "http://www.sbs6.nl/ajax/programFilter/day/0/genre/all/block/gemist/range/%s"
            self.baseUrl = "http://www.sbs6.nl"
                        
        elif self.channelCode == 'net5':
            self.guid = "B374230E-42F3-11DD-984E-E2F555D89593"
            self.icon = "net5icon.png"
            self.iconLarge = "net5large.png"
            self.noImage = "net5image.png"
            self.channelName = "Net 5"
            self.channelDescription = "Online uitzendingen van www.net5.nl."
            self.sortOrder = 6
            self.mainListUri = "http://www.net5.nl/ajax/programFilter/day/0/genre/all/block/gemist/range/%s"
            self.baseUrl = "http://www.net5.nl"
            
        self.episodeItemRegex = '<img src="(?P<thumb>[^"]+)"[\W\w]+?<h2><a href="(?P<url>[^"]+)">(?P<title>[^<]+)</a></h2>' # used for the ParseMainList
        self.folderItemRegex = '<li><a  href="(?P<url>[^"]+)">(?P<name>[^<]+)</a></li>'
        #self.videoItemRegex = '<a href="(?P<url>/programmas/[^"]+)"[^>]+>\W+<img src="(?P<thumb>[^"]+)"[\W\w]+?<h2>(?:<a[^>]+>){0,1}(?P<title>[^<]+)(?:[\w\W]+?>)\W*(?P<day>\d+) (?P<month>\w+)'
        self.videoItemRegex = '<a href="(?P<url>/programmas/[^"]+)"[^>]+>\W+<img src="(?P<thumb>[^"]+)"[\W\w]{0,400}<h2>(?:<a[^>]+>){0,1}(?P<title>[^<]+)(?:[\w\W]{0,400}?>)\W*(?P<day>\d+) (?P<month>[^v]\w+)\W*/'
        self.mediaUrlRegex = '<object id=\\\\"myExperience[\w\W]+?playerKey\\\\" value=\\\\"(?P<playerKey>[^\\\\]+)[\w\W]+?videoPlayer\\\\" value=\\\\"(?P<contentId>\d+)'
         
        self.pageNavigationRegex = '<li class=""><a href="(/ajax/VideoClips/[^"]+/page/)(\d+)"' #self.pageNavigationIndicationRegex 
        self.pageNavigationRegexIndex = 1
            
        self.moduleName = "chn_sbsbrdcst.py"            
        self.onUpDownUpdateEnabled = True
        self.requiresLogon = False
        self.language = "nl"
        
        self.contextMenuItems = []
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using Mplayer", "CtMnPlayMplayer", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using DVDPlayer", "CtMnPlayDVDPlayer", itemTypes="video", completeStatus=True))        
        return True
      
    def ParseMainList(self):
        """Parses the mainlist of the channel and returns a list of MediaItems
        
        This method creates a list of MediaItems that represent all the different
        programs that are available in the online source. The list is used to fill
        the ProgWindow. 

        Keyword parameters:
        returnData : [opt] boolean - If set to true, it will return the retrieved
                                     data as well

        Returns a list of MediaItems that were retrieved.
        
        """

        items = []
        #urlParts = ["abc", "def", "ghi", "jkl", "mno", "pqr", "stuv", "wxyz", "0-9"]
        urlParts = ["abcdef", "ghijkl", "mnopqr", "stuvwxyz", "0-9"]
        #urlParts = ["abcdef", "ghijkl"]
        baseUrl = self.mainListUri
        
        if len(self.mainListItems) > 1:
            # if there were already items, let the chn_class.py do it's tricks
            return chn_class.Channel.ParseMainList(self)
        
        try:        
            for urlPart in urlParts:
                self.mainListUri = baseUrl % (urlPart,)
                items.extend(chn_class.Channel.ParseMainList(self))
                # reset the internal list, because we need more items
                self.mainListItems = []
        except:
            logFile.debug("Error getting mainlist items", exc_info=True)

        # restore the default
        self.mainListUri = baseUrl
        
        # let the chn_class do the sorting and stuff, or if no items were found, just return
        self.mainListItems = items
        if len(items) > 0:
            return chn_class.Channel.ParseMainList(self)
        else:
            return []
        
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
        
        #logFile.debug('starting CreateEpisodeItem for %s', self.channelName)
        
        url = "%s%s%s" % (self.baseUrl, resultSet['url'], '/')#"/videos/")
        item = mediaitem.MediaItem(resultSet['title'], url)
        item.icon = self.icon
        item.thumbUrl = urlparse.urljoin(self.baseUrl, resultSet['thumb'])
        item.complete = True
        
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
                
        if not "ajax" in self.parentItem.url:
            # we just add a video folder for video's
            clipRegex = 'href="/ajax/[^/]+/([^"]+/page)/\d+"'
            clipResults = common.DoRegexFindAll(clipRegex, data)
            if len(clipResults) > 0:
                logFile.debug("Adding VideoClip item")
                clipResult = clipResults[0]
                url = "%s/ajax/VideoClips/%s/0" % (self.baseUrl, clipResult)
                logFile.debug(url)
                item = mediaitem.MediaItem("Video Clips", url)
                item.icon = self.folderIcon
                item.thumb = self.noImage
                item.complete = True
                items.append(item)
            
            logFile.debug("No Ajax page, so cleanup some stuff")
            # find where to end.
            end = data.find("<h1>Clips</h1>")
            if (end == -1):
                end = data.find("Reacties")
            data = data[data.index("</nav>"):end]
            # this regex is slow!
            #data = common.DoRegexFindAll('([\w\W]+?)<h1>Reacties</h1>', data)[0]
        
        logFile.debug("Pre-Processing finished")
        return (data, items)
        
        #        <h1>Nieuw bij SBS 6</h1>
    
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
        
        url = "%s%s" % (self.baseUrl, resultSet['url'])
        item = mediaitem.MediaItem(resultSet['name'], url)
        item.icon = self.folderIcon
        item.thumb = self.noImage
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
        
        url = "%s%s" % (self.baseUrl, resultSet['url'])
        title = resultSet['title']
        item = mediaitem.MediaItem(title, url)
        item.type = 'video'
        
        item.thumb = self.noImage
        item.icon = self.icon
        item.thumbUrl = "%s%s" % (self.baseUrl, resultSet['thumb'])
                
        month = datehelper.DateHelper.GetMonthFromName(resultSet['month'], 'nl')
        year = datetime.datetime.now().year
        date = datetime.datetime(year, month, int(resultSet['day']), 23, 59, 0)
        if date > datetime.datetime.now():
            year = year - 1
        item.SetDate(year, month, resultSet['day'])
        
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
        
        # now the mediaurl is derived. First we try WMV
        data = uriHandler.Open(item.url, pb=False)
        objectData = common.DoRegexFindAll(self.mediaUrlRegex, data)[0]
        #logFile.debug(objectData)
        
        seed = "61773bc7479ab4e69a5214f17fd4afd21fe1987a"
        amfHelper = brightcovehelper.BrightCoveHelper(logFile, objectData['playerKey'], objectData['contentId'], item.url, seed)
        item.description = amfHelper.GetDescription()
        
        part = item.CreateNewEmptyMediaPart()
        for stream, bitrate in amfHelper.GetStreamInfo():
            part.AppendMediaStream(stream.replace("&mp4:", ""), bitrate)
        
        item.complete = True
        return item    
