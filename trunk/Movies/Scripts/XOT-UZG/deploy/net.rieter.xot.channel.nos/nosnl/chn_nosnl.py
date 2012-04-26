import sys
import string
#===============================================================================
# Make global object available 
#===============================================================================
import mediaitem
import contextmenu
import chn_class
import common
from helpers import datehelper
from helpers import xmlhelper

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

register.RegisterChannel('chn_nosnl', 'nosnl')

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
        
        self.guid = "EE33E7EC-FDAB-11E0-AA09-1EED4724019B"
        self.mainListUri = "http://nos.nl/"
        self.baseUrl = "http://nos.nl"
        self.icon = "nosnlicon.png"
        self.iconLarge = "nosnllarge.png"
        self.noImage = "nosnlimage.png"
        self.channelName = "NOS.nl"
        self.channelDescription = u'Video en audio van NOS.nl.'
        self.moduleName = "chn_nosnl.py"
        self.sortOrder = 13
        self.defaultPlayer = 'dvdplayer' #(defaultplayer, dvdplayer, mplayer)
        self.language = "nl"
        
        self.requiresLogon = False
        
        self.contextMenuItems = []
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using Mplayer", "CtMnPlayMplayer", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using DVDPlayer", "CtMnPlayDVDPlayer", itemTypes="video", completeStatus=True))
                
        self.episodeItemRegex = '<li><a href="/(?P<cat>nieuws|sport)/(?P<subcat>[^"]+)/">(?P<name>[^<]+)</a></li>|<li><a href="/">(?P<basename>[^<]+)</a></li>'
        
        # we need specialized video regular expressions
        self.videoItemRegex1 = '<li>\W*<a href="/(?P<url>video/[^"]+)">(?P<name>[^<]+)</a>\W*<span class="[^>]+>\W*<img src="(?P<image>[^"]+)" alt="" />[\W\w]+?</span>(?P<description>[^<]+)<em>(?P<day>\d+) (?P<month>\w+) (?P<year>\d+)'
        self.searchItemRegex = '<li class="search[^"]+">\W*<strong>(?P<name>[^<]+)</strong>\W*<p>\W*<span class="[^>]+>\W*<img src="(?P<image>[^"]+)"[^>]+/>[\W\w]+?<span class="date">(?P<day>\d+) (?P<month>\w+) +(?P<year>\d+)</span>\W*<span class="cat">[^<]+</span>(?P<description>[^<]+)</p>\W*<a href="(?P<url>[^"]+)"'
        
        # and special folder regular expressions
        self.folderItemRegexPattern = '<li[^>]*><a href="/(?P<url>%s/[^/]+)/">(?:<span>){0,1}(?P<name>[^<]+)(?:</span>){0,1}</a></li>'
        self.folderItemsComplete = False
        
        self.pageNavigationRegex = '<li>\W*<a href="([^"]+&p=)(\d+)([^"]+)">' 
        self.pageNavigationRegexIndex = 1
        
        
        """ 
            The ProcessPageNavigation method will parse the current data using the pageNavigationRegex. It will
            create a pageItem using the CreatePageItem method. If no CreatePageItem method is in the channel,
            a default one will be created with the number present in the resultset location specified in the 
            pageNavigationRegexIndex and the url from the combined resultset. If that url does not contain http://
            the self.baseUrl will be added. 
        """
        
        #self.pageNavigationRegex = 'link button-->\W+<li class="[^"]*"><a href="([^"]+)"[^>]+>(\d+)'  
        #self.pageNavigationRegexIndex = 1
        
        """
            Test cases: 
            
            
        """
        
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
        baseItems = chn_class.Channel.ParseMainList(self, returnData=returnData) 
        
        searchItem = mediaitem.MediaItem("Search", "searchSite")
        searchItem.complete = True
        searchItem.icon = self.icon
        searchItem.thumb = self.noImage        
        baseItems.append(searchItem)
        return baseItems

    def SearchSite(self, url=None):
        """Creates an list of items by searching the site
        
        Returns:
        A list of MediaItems that should be displayed.
        
        This method is called when the URL of an item is "searchSite". The channel
        calling this should implement the search functionality. This could also include
        showing of an input keyboard and following actions. 
        
        """
        
        url = "http://nos.nl/zoeken/?sort=2&type[]=video&datumvan=&datumtot=&s=%s" 
        return chn_class.Channel.SearchSite(self, url)
    
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
        
        logFile.debug(resultSet)
        if resultSet['name']:
            url = "%s/%s/%s/video-en-audio/" % (self.baseUrl, resultSet['cat'], resultSet['subcat'])
            name =  "%s - %s" % (string.capitalize(resultSet['cat']), resultSet['name'])
        else:
            url = "%s/video-en-audio/" % (self.baseUrl,)
            name = resultSet['basename']
        item = mediaitem.MediaItem(name, url)
        item.icon = self.icon
        item.thumb = self.noImage
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
        
        # create a specialised folder regex
        urlPart = self.parentItem.url.replace(self.baseUrl, "").replace("/video-en-audio/","")
        self.folderItemRegex = self.folderItemRegexPattern % (urlPart[1:])
        
        # check if we are searching and if so, update the regex
        searchPart = "%s/zoeken" % (self.baseUrl)
        if searchPart in self.parentItem.url:
            logFile.debug("Activating the Search Regex")
            self.videoItemRegex = self.searchItemRegex
        else:
            self.videoItemRegex = self.videoItemRegex1
        
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
        
        url = "%s/%s/video-en-audio/" % (self.baseUrl, resultSet['url'])
        name = resultSet['name']
        
        if self.folderItemsComplete or "archief" in url or "live" in url:
            self.folderItemsComplete = True
            return None 
        
        item = mediaitem.MediaItem(name, url)
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

        logFile.debug('Starting CreateVideoItem for %s', self.channelName)
        #logFile.debug("Content = %s", resultSet)
        
        name = resultSet['name']
        
        url = resultSet['url']
        if not "http:" in url:
            url = "%s/%s" % (self.baseUrl, url)
        
        item = mediaitem.MediaItem(name, url, type="video")
        item.icon = self.icon
        item.thumb = self.noImage
        item.thumbUrl = resultSet['image'].replace("/xs/", "/xl/")
        item.description = resultSet['description']
        
        day = resultSet['day']
        month = resultSet['month']
        month = datehelper.DateHelper.GetMonthFromName(month, "nl")
        year = resultSet['year']
        item.SetDate(year, month, day)
        
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

        logFile.debug('Starting UpdateVideoItem: %s', item.name)
        item.thumb = self.CacheThumb(item.thumbUrl)
        
        # retrieve the mediaurl
        data = uriHandler.Open(item.url, pb=False, proxy=self.proxy)
        urls = common.DoRegexFindAll("file:\W+'([^']+)'", data)
        for url in urls:
            data2 = uriHandler.Open(url, pb=False, proxy=self.proxy)
            xmlData = xmlhelper.XmlHelper(data2)
            mediaUrl = xmlData.GetSingleNodeContent('location', stripCData=True)
            item.AppendSingleStream(mediaUrl, 800)
            
            description = xmlData.GetSingleNodeContent('annotation', stripCData=True)
            item.description = description
            item.complete = True
            
        #logFile.debug(item)
        return item