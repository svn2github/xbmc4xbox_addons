#===============================================================================
# Import the default modules 
#===============================================================================
import sys

#===============================================================================
# Make global object available
#===============================================================================
import mediaitem
import contextmenu
import chn_class
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

register.RegisterChannel('chn_at5', 'at5')

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
        self.guid = "870EAD32-F2F9-11DD-B0E7-747356D89593"
        self.icon = "at5icon.png"
        self.iconLarge = "at5large.png"
        self.noImage = "at5image.png"
        self.channelName = "AT5"
        self.channelDescription = "AT5 Uitzendinggemist"
        self.moduleName = "chn_at5.py"
        self.mainListUri = "http://www.at5.nl/tv/overzicht"
        self.baseUrl = "http://www.at5.nl"
        self.onUpDownUpdateEnabled = True
        self.sortOrder = 12
        self.language = "nl"
        self.swfUrl = "http://www.at5.nl/embed/at5player.swf"
        
        self.contextMenuItems = []
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using Mplayer", "CtMnPlayMplayer", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using DVDPlayer", "CtMnPlayDVDPlayer", itemTypes="video", completeStatus=True))
                
        self.requiresLogon = False
        
        self.episodeItemRegex = '<li><a class="" href="(/tv/[^"]+)">([^<]+)</a></li>' # used for the ParseMainList
        self.videoItemRegex = """(?:<p class="tijd">\w+ (\d+) (\w+) (\d+), [^<]+</p>\W+<h1>([^<]+)</h1>[\w\W]+?swf\?e=(\d+)[\w\W]+?<div class="detail_tekst">(?:<p>([^<]*)</p>){0,1}|<img[^>]+src='([^']+)'[^>]+/></a>\W+<div>\W+<h3>\W+<span[^>]+>(\d+)-(\d+)-(\d+)</span>\W+<a href="([^"]+/)(\d+)">([^<]+)</a>\W+</h3>\W+<p>(?:<p>([^<]+)</p>){0,1})""" 
        self.mediaUrlRegex = '<param\W+name="URL"\W+value="([^"]+)"'
        self.pageNavigationRegex = '<a href="(/[^"]+page/)(\d+)">\d+</a>' #self.pageNavigationIndicationRegex 
        self.pageNavigationRegexIndex = 1
        return True
    
    def CreateEpisodeItem(self, resultSet):
        """
        Accepts an arraylist of results. It returns an item. 
        """
        logFile.debug('starting CreateEpisodeItem for %s', self.channelName)
        
        item = mediaitem.MediaItem(resultSet[1], "%s%s" % (self.baseUrl, resultSet[0]))
        item.icon = self.icon
        item.thumb = self.noImage
        item.complete = True
        return item
    
    def CreateVideoItem(self, resultSet):
        """
        Accepts an arraylist of results. It returns an item. 
        """
        logFile.debug('starting CreateVideoItem for %s', self.channelName)
        #logFile.debug(resultSet)
        
        if resultSet[0] == "":
            # not the main item
            thumbUrl = "%s%s" % (self.baseUrl, resultSet[6])
            day = resultSet[7]
            month = resultSet[8]
            year = resultSet[9]
            #url = "%s%s" % (resultSet[10], resultSet[11])
            id = resultSet[11]
            title = resultSet[12]
            description = resultSet[13]
        else:
            # the main item on the page, only load once
            if "/page/" in self.parentItem.url:
                return None
            
            day = resultSet[0]
            month = resultSet[1]
            month = datehelper.DateHelper.GetMonthFromName(month, "nl", short=False)        
            year = resultSet[2]
            title = resultSet[3]
            id = resultSet[4]
            description = resultSet[5]
            #url = self.parentItem.url
            thumbUrl = ''
        
        url = "http://www.at5.nl/embedder/videodata?e=%s" % (id,)
        
        item = mediaitem.MediaItem(title, url)
        item.description = description
        item.thumbUrl = thumbUrl
        item.thumb = self.noImage
        item.icon = self.icon        
        item.SetDate(year, month, day)
        item.type = 'video'
        item.complete = False
        return item
    
    def UpdateVideoItem(self, item):
        """
        Accepts an item. It returns an updated item. Usually retrieves the MediaURL 
        and the Thumb! It should return a completed item. 
        """
        logFile.info('starting UpdateVideoItem for %s (%s)', item.name, self.channelName)
        
        data = uriHandler.Open(item.url, pb=False)
        xml = xmlhelper.XmlHelper(data)
        
        if item.thumbUrl == '': 
            # if not thumb was present use the one from the XML
            item.thumbUrl = xml.GetSingleNodeContent("videoimage")
        item.thumb = self.CacheThumb(item.thumbUrl)      
        
        server = xml.GetSingleNodeContent("server")
        fileName = xml.GetSingleNodeContent("filename")
        mediaUrl = "%s/_definst_/%s" % (server, fileName)
        mediaUrl = self.GetVerifiableVideoUrl(mediaUrl)
        item.AppendSingleStream(mediaUrl, 0)
        
        item.complete = True                    
        return item    