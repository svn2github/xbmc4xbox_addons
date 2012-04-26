#===============================================================================
# Import the default modules
#===============================================================================
import sys
import urlparse

import common
import mediaitem
import contextmenu
import chn_class
from helpers import htmlentityhelper
from helpers import datehelper
from helpers import htmlhelper
from helpers import xmlhelper

#===============================================================================
# Make global object available
#===============================================================================
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

register.RegisterChannel('chn_channel9', 'channel9')

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
        
        self.guid = "21D74788-8084-11E0-9A28-39E64824019B"
        self.icon = "channel9icon.png"
        self.iconLarge = "channel9large.png"
        self.noImage = "channel9image.png"
        self.channelName = "MSDN Channel 9"
        self.channelDescription = "Channel 9 videos @ MSDN.com"
        #self.sortOrder = 8
        self.mainListUri = "http://channel9.msdn.com/Browse"
        self.baseUrl = "http://channel9.msdn.com"
        self.defaultPlayer = 'dvdplayer'
   
        self.episodeItemRegex = '<li>\W+<a href="([^"]+Browse[^"]+)">(\D[^<]+)</a>' # used for the ParseMainList        
        #self.videoItemRegex = '<item>\W+<title>([^<]+)</title>\W+<description><!\[CDATA\[\W+p>([^<]+)[^]]+\]\]></description>\W+<comments>[^<]+</comments>\W+(<[^>]+>[^<]+</[^>]+>\W+){0,1}<link>([^<]+)</link>\W+<pubDate>\w+, (\d+) (\w+) (\d+)' 
        self.videoItemRegex = '<item>([\W\w]+?)</item>' 
        
        self.folderItemRegex = '<a href="([^"]+)" class="title">([^<]+)</a>([\w\W]{0,600})</li>'
        self.folderItemRegex = "(?:%s|%s)" % (self.folderItemRegex, '<li>\W+<a href="(/Browse[^"]+)">(\D[^<]+)')
        
        self.pageNavigationRegex = '<a href="([^"]+page[^"]+)">(\d+)</a>' #self.pageNavigationIndicationRegex 
        self.pageNavigationRegexIndex = 1
            
        self.moduleName = "chn_channel9.py"            
        self.onUpDownUpdateEnabled = True
        self.requiresLogon = False
        self.language = None
        
        self.contextMenuItems = []
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using Mplayer", "CtMnPlayMplayer", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using DVDPlayer", "CtMnPlayDVDPlayer", itemTypes="video", completeStatus=True))        

        """
        KeyNote:
        http://media.ch9.ms/ch9/0ee8/30fd8210-58f1-4d61-a006-9ed200a40ee8/Devdays001_220_ch9.jpg
        
        http://media.ch9.ms/ch9/0ee8/30fd8210-58f1-4d61-a006-9ed200a40ee8/Devdays001_2MB_ch9.wmv">High Quality WMV</a> <span class="usage">(PC, XBox, MCE)</span>
        http://media.ch9.ms/ch9/0ee8/30fd8210-58f1-4d61-a006-9ed200a40ee8/Devdays001_ch9.mp3">MP3<em class="ymp-skin"></em></a> <span class="usage">(Audio only)</span>
        http://media.ch9.ms/ch9/0ee8/30fd8210-58f1-4d61-a006-9ed200a40ee8/Devdays001_ch9.wma">WMA<em class="ymp-skin"></em></a> <span class="usage">(Audio only)</span>
        http://media.ch9.ms/ch9/0ee8/30fd8210-58f1-4d61-a006-9ed200a40ee8/Devdays001_ch9.wmv">Medium Quality WMV</a> <span class="usage">(Lo-band, Mobile)</span>
        http://media.ch9.ms/ch9/0ee8/30fd8210-58f1-4d61-a006-9ed200a40ee8/Devdays001_high_ch9.mp4">High Quality MP4</a> <span class="usage">(iPad, WP7)</span>
        http://media.ch9.ms/ch9/0ee8/30fd8210-58f1-4d61-a006-9ed200a40ee8/Devdays001_low_ch9.mp4">MP4</a> <span class="usage">(iPod, Zune HD)</span>
        
        other image:
        http://media.ch9.ms/ch9/10bd/4a762419-63fb-480e-8c18-9ed200a410bd/Devdays002_220_ch9.jpg
        """
        return True
    
    #==============================================================================
    def CreateEpisodeItem(self, resultSet):
        """
        Accepts an arraylist of results. It returns an item. 
        """
        #logFile.debug('starting CreateEpisodeItem for %s', self.channelName)
        url = urlparse.urljoin(self.baseUrl, htmlentityhelper.HtmlEntityHelper.ConvertHTMLEntities(resultSet[0]))
        name = resultSet[1]
         
        if name == "Tags":
            return None
        if name == "Authors":
            return None
        if name == "Most Viewed":
            return None
        if name == "Top Rated":
            name = "Recent"
            url = "http://channel9.msdn.com/Feeds/RSS"
        else:
            url = "%s?sort=atoz" % (url,)
        
        item = mediaitem.MediaItem(name , url)
        item.icon = self.icon
        item.complete = True
        #logFile.debug(item)
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
        data = data.replace("&#160;", " ")
        
        pageNav = data.find('<div class="pageNav">')
        if pageNav > 0:
            data = data[0:pageNav]
           
        logFile.debug("Pre-Processing finished")
        return (data, items)
          
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
        
        logFile.debug("Starting CreatePageItem")
        
        url = urlparse.urljoin(self.baseUrl, htmlentityhelper.HtmlEntityHelper.ConvertHTMLEntities(resultSet[0]))
        item = mediaitem.MediaItem(resultSet[self.pageNavigationRegexIndex], url)
        item.type = "page"
        item.complete = True
        
        logFile.debug("Created '%s' for url %s", item.name, item.url)
        return item 
    
    
    #==============================================================================
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
        logFile.debug(resultSet)
        
        if (len(resultSet) > 3 and resultSet[3] != ""):
            logFile.debug("Sub category folder found.")
            url = urlparse.urljoin(self.baseUrl, htmlentityhelper.HtmlEntityHelper.ConvertHTMLEntities(resultSet[3]))
            name = ":: %s" % (resultSet[4],)
            item = mediaitem.MediaItem(name, url)
            item.thumb = self.noImage;
            item.complete = True;
            item.type = "folder"
            return item
        
        
        url = urlparse.urljoin(self.baseUrl, htmlentityhelper.HtmlEntityHelper.ConvertHTMLEntities(resultSet[0]))
        name = htmlentityhelper.HtmlEntityHelper.ConvertHTMLEntities(resultSet[1])
        
        helper = htmlhelper.HtmlHelper(resultSet[2])
        description = helper.GetTagContent("div", {'class':'description'})
                
        item = mediaitem.MediaItem(name, "%s/RSS" %(url,))
        item.thumb = self.noImage
        item.icon = self.folderIcon
        item.type = 'folder'
        item.description = description.strip()
        
        date = helper.GetTagContent("div", {'class':'date'})
        if (date == ""):
            date = helper.GetTagContent("span", {'class': 'lastPublishedDate'})
            
        if (not date == ""):
            dateParts = common.DoRegexFindAll("(\w+) (\d+)[^<]+, (\d+)", date)
            if len(dateParts) > 0:
                dateParts = dateParts[0]                
                monthPart = dateParts[0].lower()
                dayPart = dateParts[1]
                yearPart = dateParts[2]
                
                try:
                    month = datehelper.DateHelper.GetMonthFromName(monthPart, "en")
                    item.SetDate(yearPart, month, dayPart)
                except:
                    logFile.error("Error matching month: %s", monthPart, exc_info=True)
        
        item.complete = True
        return item
    
    #============================================================================= 
    def CreateVideoItem(self, resultSet):
        """
        Accepts an arraylist of results. It returns an item. 
        """
        #logFile.debug('starting CreateVideoItem for %s', self.channelName)
        #logFile.debug(resultSet)

        xmlData = xmlhelper.XmlHelper(resultSet)
        #logFile.debug(resultSet)
        title = xmlData.GetSingleNodeContent("title")
        url = xmlData.GetSingleNodeContent("link")
        description = xmlData.GetSingleNodeContent("description")
        description = description.replace("<![CDATA[ ", "").replace("]]>", "").replace("<p>","").replace("</p>","\n")
        
        item = mediaitem.MediaItem(title, url)
        item.type = 'video'
        item.complete = False
        item.description = description
        item.thumb = self.noImage
        item.icon = self.icon
        
        date = xmlData.GetSingleNodeContent("pubDate")
        dateResult = common.DoRegexFindAll("\w+, (\d+) (\w+) (\d+)", date)[-1]
        day = dateResult[0]
        monthPart = dateResult[1].lower()
        year = dateResult[2]
        
        try:
            month = 0
            monthLookup=["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]
            month = monthLookup.index(monthPart)+1                            
            item.SetDate(year, month, day)
        except:
            logFile.error("Error matching month: %s", resultSet[4].lower(), exc_info=True)
            
        return item
    
    #============================================================================= 
    def UpdateVideoItem(self, item):
        """
        Accepts an item. It returns an updated item. Usually retrieves the MediaURL 
        and the Thumb! It should return a completed item. 
        """
        logFile.info('starting UpdateVideoItem for %s (%s)', item.name, self.channelName)
        
        # now the mediaurl is derived. First we try WMV
        data = uriHandler.Open(item.url, pb=False)
        
        urls = common.DoRegexFindAll('<a href="([^"]+.wmv)">(High|Medium|Mid|Low)', data)
        mediaPart = mediaitem.MediaItemPart(item.name)
        for url in urls:
            if url[1].lower() == "high":
                bitrate = 2000
            elif url[1].lower() == "medium" or url[1].lower() == "mid" :
                bitrate = 1200
            elif url[1].lower() == "low":
                bitrate = 200
            else:
                bitrate = 0 
            mediaPart.AppendMediaStream(htmlentityhelper.HtmlEntityHelper.ConvertHTMLEntities(url[0]), bitrate)            
        
        item.MediaItemParts.append(mediaPart)
        
        images = common.DoRegexFindAll('<link type="image/jpeg" rel="videothumbnail" href="([^"]+)"/>', data)
        for image in images:
            thumbUrl = htmlentityhelper.HtmlEntityHelper.ConvertHTMLEntities(image)
            break

        item.thumb = self.CacheThumb(thumbUrl)       
        item.complete = True
        return item    
