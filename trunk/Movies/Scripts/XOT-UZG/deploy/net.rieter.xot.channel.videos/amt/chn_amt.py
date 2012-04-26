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
from helpers import jsonhelper
from helpers import xmlhelper
from helpers import datehelper
from helpers import htmlhelper

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

register.RegisterChannel('chn_amt')

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
        
        self.guid = "887F773F-E4E5-4E80-AD7D-65F627D1CA44"
        self.icon = "amticon.png"
        self.iconLarge = "amtlarge.png"
        self.noImage = "amtimage.png"
        self.channelName = "Apple Movie Trailers"
        self.channelDescription = "Trailers from the AMT site."
        #self.sortOrder = 8        
        self.baseUrl = "http://trailers.apple.com"
                
        self.mainListUri = "http://trailers.apple.com/trailers/home/feeds/just_added.json"
        #self.mainListUri = "http://trailers.apple.com/trailers/home/xml/newest.xml"
        #self.mainListUri = "http://trailers.apple.com/trailers/home/xml/current.xml"
        #self.mainListUri = "http://trailers.apple.com/trailers/home/xml/current_480p.xml"
        #self.mainListUri = "http://trailers.apple.com/trailers/home/xml/current_720p.xml"

        if self.mainListUri.endswith("json"):
            self.episodeItemRegex = '(\{"title":[\w\W]+?}]})'
        else:
            self.episodeItemRegex = '<movieinfo[\w\W]+?</movieinfo>'
        
        self.videoItemRegex = '(=.single-trailer-info[\w\W]+?<!--/trailer-->)|(<div class=.column first[\w\W]+?<!--/trailer-->)' 
        self.pageNavigationRegex = '' 
        self.pageNavigationRegexIndex = 1
            
        self.moduleName = "chn_amt.py"            
        self.onUpDownUpdateEnabled = True
        self.requiresLogon = False
        self.language = None
        
        self.contextMenuItems = []
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Download Item", "CtMnDownloadItem", itemTypes="video", completeStatus=True, plugin=True))  
        
        return True
        
    def CreateEpisodeItem(self, resultSet):
        if self.mainListUri.endswith("json"):
            return self.CreateEpisodeItemJson(resultSet)
        else:
            return self.CreateEpisodeItemXml(resultSet)
    
    def CreateEpisodeItemJson(self, resultSet):
        """
        Accepts an arraylist of results. It returns an item. 
        """
        #logFile.debug(resultSet)
        json = jsonhelper.JsonHelper(resultSet)
        
        title = json.GetNamedValue("title")
        date = json.GetNamedValue("postdate")
        url = json.GetNamedValue("url")
        thumbUrl = json.GetNamedValue("poster")
        # /trailers/independent/grifftheinvisible/ ->
        #http://trailers.apple.com/trailers/independent/grifftheinvisible/ includes/playlists/web.inc
        #http://trailers.apple.com/moviesxml/s/independent/hellolonesome/index.xml
        #url = "%s/moviesxml/s%sindex.xml" % (self.baseUrl, url.replace("/trailers", ""))
        url = "%s%sincludes/playlists/web.inc" % (self.baseUrl, url)
       
        dates = date.split(" ")
        #logFile.debug(dates)
        day = dates[1]
        month = datehelper.DateHelper.GetMonthFromName(dates[2], "en")
        year = dates[3]
        
        # dummy class
        item = mediaitem.MediaItem(title, url)
        item.icon = self.icon
        item.thumb = self.noImage
        item.thumbUrl = thumbUrl.replace("poster.jpg", "poster-xlarge.jpg")
        item.SetDate(year, month, day)
        item.complete = True
        return item
    
    def CreateEpisodeItemXml(self, resultSet):
        """
        Accepts an arraylist of results. It returns an item. 
        """
        #logFile.debug(resultSet)
        xml = xmlhelper.XmlHelper(resultSet)
            
        title = xml.GetSingleNodeContent("title")
        date = xml.GetSingleNodeContent("postdate")
        thumbUrl = xml.GetSingleNodeContent("location")
        description = xml.GetSingleNodeContent("description")
        
        # http://trailers.apple.com/trailers/paramount/footloose/images/poster.jpg ->
        # http://trailers.apple.com/trailers/independent/grifftheinvisible/ includes/playlists/web.inc
        url = thumbUrl.replace("images/poster.jpg","")
        url = "%sincludes/playlists/web.inc" % (url, )
       
        dates = date.split("-")
        day = dates[2]
        month = dates[1]
        year = dates[0]
        
        # dummy class
        item = mediaitem.MediaItem(title, url)
        item.icon = self.icon
        item.thumb = self.noImage
        item.thumbUrl = thumbUrl
        item.SetDate(year, month, day)
        item.description = description
        item.thumbUrl = thumbUrl
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
        #logFile.debug(resultSet)
        if resultSet[0] == "":
            content = resultSet[1]
        else:
            content = resultSet[0]        
        html = htmlhelper.HtmlHelper(content)
        
        # create the item
        title = html.GetTagContent("h3")
        title = "%s - %s" % (self.parentItem.name, title)
        
        # get the ID from the parent
        url = self.parentItem.url.replace("includes/playlists/web.inc", "")
        
        item = mediaitem.MediaItem(title, url)
        item.icon = self.icon
        item.description = self.parentItem.description
        item.type = 'video'
        
        # get the thumburl
        item.thumb = self.noImage
        item.thumbUrl = html.GetTagAttribute("img", {"src":None})
        #logFile.debug("Found Thumb: %s", item.thumbUrl)
        
        #<a href="http://trailers.apple.com/movies/wb/harrypotterandthedeathlyhallowspart2/hp7part2-tlr2_720p.mov" class="target-quicktimeplayer">
        #urls = html.GetTagAttribute("a", firstOnly=False, href=None, cls="target-quicktimeplayer")
        urls = html.GetTagAttribute("a", {"href": None}, {"cls":"target-quicktimeplayer"}, firstOnly=False)
        #{"": ""}, {"ratio":"4:3"}
        part = item.CreateNewEmptyMediaPart()
        
        if len(urls) == 0:
            # could be that there are no URL, then skip
            return None
        
        # all the URL's should have h[version] in the url, but the URL we get
        # here does not always have this, so check.
        for url in urls:
            if "1080p" in url:
                # if the h1080 is already there, it's OK
                if not "h1080p" in url:
                    logFile.debug("Prefixing the URL with h-version.")
                    url = url.replace("1080p", "h1080p")
                part.AppendMediaStream(url, 8000) # actually 9300
                baseUrl = url.replace("1080p", "[version]")
            
            elif "720p" in url:
                # if the h720 is already there, it's OK
                if not "h720p" in url:
                    logFile.debug("Prefixing the URL with h-version.")
                    url = url.replace("720p", "h720p") 
                part.AppendMediaStream(url, 4000) # actually 5300
                baseUrl = url.replace("720p", "[version]")
                
            elif "480p" in url:
                # if the h480 is already there, it's OK
                if not "h480p" in url:
                    logFile.debug("Prefixing the URL with h-version.")
                    url = url.replace("480p", "h480p")
                part.AppendMediaStream(url, 2000) # actually 2200
                baseUrl = url.replace("480p", "[version]")                
            
            else:
                logFile.info("Skipping url: %s", url)
        
        # add low res
        logFile.debug("Using base URL '%s' to calculate others.", baseUrl)
        part.AppendMediaStream(baseUrl.replace("[version]", "640w"), 1200)  # actually 1200
        part.AppendMediaStream(baseUrl.replace("[version]", "480"), 800)    # actually 800
        part.AppendMediaStream(baseUrl.replace("[version]", "320"), 250)    # actually 250
        
        #part.CanStream = False
        part.UserAgent = "QuickTime/7.6 (qtver=7.6;os=Windows NT 6.0Service Pack 2)"
        
        # get the date
        dateResult = common.DoRegexFindAll('<p>Posted: (\d+)/(\d+)/(\d+)', html.data)
        for dates in dateResult: 
            year = "20%s" % (dates[2],)
            day = dates[1]
            month = dates[0]
            item.SetDate(year, month, day)        
        
        item.downloadable = True
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
        
        if self.mainListUri.endswith("json"):
            # get the description
            data = uriHandler.Open(item.url, pb=False)
            description = common.DoRegexFindAll('<meta name="Description" content="([^"]+)"', data)
            item.description = description[-1]
            pass
        else:
            pass        
        
        item.thumb = self.CacheThumb(item.thumbUrl)
        item.complete = True     
        return item