#===============================================================================
# Import the default modules
#===============================================================================
import xbmc, xbmcgui
import re, sys, os
import urlparse
#===============================================================================
# Make global object available
#===============================================================================
import common
import mediaitem
import config
import controls
import contextmenu
import chn_class
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

register.RegisterChannel('chn_mtvnl', 'mtvnl')

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
        self.guid = "7C52452A-F2F9-11DD-BE3F-3F7356D89593"
        self.icon = "mtvnlicon.png"
        self.iconLarge = "mtvnllarge.png"
        self.noImage = "mtvnlimage.png"
        self.channelName = "MTV.nl"
        self.channelDescription = "MTV.nl Episodes"
        self.moduleName = "chn_mtvnl.py"
        self.mainListUri = "http://www.mtv.nl/info/kijk-alle-afleveringen/"
        self.baseUrl = "http://intl.esperanto.mtvi.com/www/xml/media/mediaGen.jhtml?uri="
        self.onUpDownUpdateEnabled = True
        self.sortOrder = 9
        self.language = "nl"
        
        self.contextMenuItems = []
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using Mplayer", "CtMnPlayMplayer", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using DVDPlayer", "CtMnPlayDVDPlayer", itemTypes="video", completeStatus=True))
                
        self.requiresLogon = False
        
        self.episodeItemRegex = '<a href="(http://www.mtv.nl/shows/[^"]+)"[^>]*><strong>([^<]+)<' # used for the ParseMainList
        self.videoItemRegex = '<a href="([^"]+)" title="([^"]+)" class="thumblink"[^>]*>\W+<img[^>]*class="[^"]*"[^>]*src="([^"]+)"[^>]+>\W+<span'   # used for the CreateVideoItem 
#        self.folderItemRegex = '<a href="\.([^"]*/)(cat/)(\d+)"( style="color:\s*white;"\s*)*>([^>]+)</a><br'  # used for the CreateFolderItem
        self.mediaUrlRegex = '<param name="src" value="([^"]+)" />'    # used for the UpdateVideoItem
        return True
      
    #==============================================================================
    def CreateEpisodeItem(self, resultSet):
        """
        Accepts an arraylist of results. It returns an item. 
        """
        logFile.debug('starting CreateEpisodeItem for %s', self.channelName)
        
        # <li><a href="(/guide/season/[^"]+)">(\d+)</a></li>
        url = "%safleveringen/" % (resultSet[0],)
        item = mediaitem.MediaItem(resultSet[1], url)
        item.icon = self.icon
        item.complete = True
        return item
    
    #============================================================================= 
    def CreateVideoItem(self, resultSet):
        """
        Accepts an arraylist of results. It returns an item. 
        """
        logFile.debug('starting CreateVideoItem for %s', self.channelName)        
        
        item = mediaitem.MediaItem(resultSet[1], "http://www.mtv.nl%s" % (resultSet[0],))
        item.thumbUrl = resultSet[2]      
        item.icon = self.icon
        item.type = 'video'
        item.complete = False
        return item
    
    #============================================================================= 
    def UpdateVideoItem(self, item):
        """
        Accepts an item. It returns an updated item. Usually retrieves the MediaURL 
        and the Thumb! It should return a completed item. 
        """
        logFile.info('starting UpdateVideoItem for %s (%s)', item.name, self.channelName)
        
        if item.thumbUrl != "":
            item.thumb = self.CacheThumb(item.thumbUrl)
        else:
            item.thumb = self.noImage
        
        url = item.url
        data = uriHandler.Open(url,pb=False)
        
        parts = common.DoRegexFindAll("addToVidArray\('([^']+)'\);", data)
        if len(parts) == 0:
            logFile.debug("Unable to determine the number of videoparts")
            return item
        
        first = True
        for part in parts:
            # first part is already loaded
            if not first:
                url = "http://www.mtv.nl%s" % (part,)
                data = uriHandler.Open(url, pb=False)
            
            first = False
            mgid = common.DoRegexFindAll('<link rel="video_src" href="[^"]+(mgid:[^"]+)" />', data)
            if len(mgid) == 1:
                # mgid was found, load the info file
                id = common.DoRegexFindAll('-(\d+)/$', url)[0]
                mgid = mgid[0]
                logFile.debug("Handling mgid='%s'", mgid)
                firstMgidEncoded = htmlentityhelper.HtmlEntityHelper.UrlEncode("mgid:uma:video:mtv.nl:%s" % (id,))
                mgidEncoded = htmlentityhelper.HtmlEntityHelper.UrlEncode(mgid)
                params = "%s&hcxId=%s" % (firstMgidEncoded, mgidEncoded)
                infoUrl = "%s%s" % (self.baseUrl, params) 
                infoData = uriHandler.Open(infoUrl,pb=False)
                
                rtmpUrls = common.DoRegexFindAll('<rendition[^>]+bitrate="([^"]+)"[^>]*>\W+<src>([^<]+ondemand)/([^<]+).flv</src>', infoData)
                logFile.debug(rtmpUrls)
                rtmpUrls.sort(lambda x, y: int(y[0])-int(x[0]))
                logFile.debug(rtmpUrls)
                item.AppendSingleStream("%s?slist=%s" % (rtmpUrls[0][1], rtmpUrls[0][2]))
            else:
                logFile.debug("Unable to determine the MGID from '%s'", )            
                return item
                    
        # get the RTMP urls
        #<src>rtmp://cp40493.edgefcs.net/ondemand/comedystor/_!/com/sp/acts/Season01/E_0102/compressed/flv/0102_3_DI_640x480_500kbps.flv</src>
        #rtmp://cp40493.edgefcs.net/ondemand?slist=comedystor/_!/com/sp/acts/Season01/E_0106/compressed/flv/0106_4_DI_640x480_700kbps 
               
        item.complete = True         
        logFile.debug("Media url of item: %s", item)
        
        return item    