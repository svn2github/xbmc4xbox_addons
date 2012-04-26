# coding:UTF-8
import sys
#===============================================================================
# Make global object available
#===============================================================================
import common
import mediaitem
import contextmenu
import chn_class
from helpers import subtitlehelper
from helpers import encodinghelper

logFile = sys.modules['__main__'].globalLogFile
uriHandler = sys.modules['__main__'].globalUriHandler
#===============================================================================
# register the channels
#===============================================================================
if (sys.modules.has_key('progwindow')):
    register = sys.modules['progwindow'].channelRegister
elif (sys.modules.has_key('plugin')):
    register = sys.modules['plugin'].channelRegister
#register.channelButtonRegister.append(105)

register.RegisterChannel('chn_tvse', 'se6')
register.RegisterChannel('chn_tvse', 'se3')
register.RegisterChannel('chn_tvse', 'se8')
register.RegisterChannel('chn_tvse', 'se3lv')
register.RegisterChannel('chn_tvse', 'no3')
register.RegisterChannel('chn_tvse', 'no4')
#register.RegisterChannel('chn_tvse', 'sesport')
register.RegisterChannel('chn_tvse', 'tv3lt')

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
        
        self.baseUrl = "http://viastream.player.mtgnewmedia.se/"
        self.requiresLogon = False
        self.moduleName = "chn_tvse.py"
                
        if self.channelCode == "se3":
            self.guid = "9EC8F612-2EA4-11DE-867C-B84656D89593"
            #self.mainListUri = "http://viastream.player.mtgnewmedia.se/xml/xmltoplayer.php?type=siteMapData&channel=2se&country=se&category=0"
            self.mainListUri = "http://www.tv3play.se/program"
            self.icon = "tv3seicon.png"
            self.iconLarge = "tv3selarge.png"
            self.noImage = "tv3seimage.png"
            self.channelName = "TV3"
            self.sortOrder = 103
            self.channelDescription = u'Sändningar från TV3.se'
            self.language = "se"    
        
        elif self.channelCode =="se6":
            self.guid = "FB34E1F0-2930-11DE-A339-255856D89593"
            #self.mainListUri = "http://viastream.player.mtgnewmedia.se/xml/xmltoplayer.php?type=siteMapData&channel=3se&country=se&category=0"
            self.mainListUri = "http://www.tv6play.se/program"
            self.icon = "tv6seicon.png"
            self.iconLarge = "tv6selarge.png"
            self.noImage = "tv6seimage.png"
            self.channelName = "TV6"
            self.sortOrder = 106
            self.channelDescription = u'Sändningar från TV6.se'
            self.language = "se"
        
        elif self.channelCode =="se8":
            self.guid = "BDC1A5C5-2777-4D05-BB5B-742A88B89CC5"
            #self.mainListUri = "http://viastream.player.mtgnewmedia.se/xml/xmltoplayer.php?type=siteMapData&channel=4se&country=se&category=0"
            self.mainListUri = "http://www.tv8play.se/program"
            self.icon = "tv8seicon.png"
            self.iconLarge = "tv8selarge.png"
            self.noImage = "tv8seimage.png"
            self.sortOrder = 108
            self.channelName = "TV8"
            self.channelDescription = u'Sändningar från TV8.se'
            self.language = "se"
        
        elif self.channelCode == "sesport":
            raise NotImplementedError('ViaSat sport is not in this channel anymore.') 
#            self.guid = "87533F2C-B759-11DE-A4E3-146355D89593"
#            self.mainListUri = "http://viastream.player.mtgnewmedia.se/xml/xmltoplayer.php?type=siteMapData&channel=1se&country=se&category=0"
#            self.icon = "sesporticon.png"
#            self.iconLarge = "sesportlarge.png"
#            self.noImage = "sesportimage.png"
#            self.sortOrder = 109
#            self.channelName = "Viasat Sport"
#            self.channelDescription = u'Sändningar från viasatsport.se'
        
        # Lithuanian channels
        elif self.channelCode == "tv3lt":
            self.guid = "7FEDC7EA-2281-11E0-8F30-67B5DFD72085"
            self.mainListUri = "http://www.tv3play.lt/program"
            self.icon = "tv3lticon.png"
            self.iconLarge = "tv3ltlarge.png"
            self.noImage = "tv3ltimage.png"
            self.sortOrder = 110
            self.channelName = "TV3.lt"
            self.channelDescription = u'TV3.lt web.tv'
            self.language = "lt"            
        
        # Letvian Channel
        elif self.channelCode == "se3lv":
            self.guid = "8D9FBD00-2284-11E0-8957-55B8DFD72085"
            #self.mainListUri = "http://viastream.player.mtgnewmedia.se/xml/xmltoplayer.php?type=siteMapData&channel=2se&country=se&category=0"
            self.mainListUri = "http://www.tv3play.lv/program"
            self.icon = "tv3lvicon.png"
            self.iconLarge = "tv3lvlarge.png"
            self.noImage = "tv3lvimage.png"
            self.channelName = "TV3.lv"
            self.sortOrder = 112
            self.channelDescription = u'Sändningar från TV3.lv'
            self.language = "lv"
        
        # Norwegian Channels
        elif self.channelCode =="no3":
            self.guid = "89673FF0-5EF3-11E0-8CC9-494DDFD72085"            
            self.mainListUri = "http://www.tv3play.no/program"
            self.icon = "tv3noicon.png"
            self.iconLarge = "tv3nolarge.png"
            self.noImage = "tv3noimage.png"
            self.channelName = "TV3 - Norge"
            self.sortOrder = 91
            self.channelDescription = u'Sendninger fra TV3.no'
            self.language = "no"

        elif self.channelCode =="no4":
            self.guid = "90DD5C88-5EF3-11E0-93A2-4D4DDFD72085"            
            self.mainListUri = "http://www.viasat4play.no/program"
            self.icon = "viasat4noicon.png"
            self.iconLarge = "viasat4nolarge.png"
            self.noImage = "viasat4noimage.png"
            self.channelName = "Viasat4 - Norge"
            self.sortOrder = 92
            self.channelDescription = u'Sendninger fra Viasat4.no'
            self.language = "no"
        
        self.contextMenuItems = []
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using Mplayer", "CtMnPlayMplayer", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using DVDPlayer", "CtMnPlayDVDPlayer", itemTypes="video", completeStatus=True))
        
        
        self.episodeItemRegex = '<li[^>]*><a href="/program/([^"]+)">([^<]+)</a></li>'
        self.videoItemRegex = '(<td [^>]+class="season-col"><a[^>]*><strong>([^<]+)</strong></a></td>|<a href="/play/(\d+)/[^"]*"[^>]*>([^<]+)</a>\W*</th>\W+<td[^>]+>([^<]*)</td>\W+<td[^>]+>[^>]+>\W+<td[^>]+>((\d+)-(\d+)-(\d+) (\d+):(\d+)){0,1}[^<]*</td>)'
        self.folderItemRegex = '<siteMapNode title="([^"]+)" id="([^"]+)" children="([^"]+)" articles="[123456789]\d*"'
        self.mediaUrlRegex = '<param name="flashvars" value="pathflv\W*=\W*([^"]+)_definst_/([^"]+)\$start'
        
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

        #========================================================================== 
        # non standard items
        self.categoryName = ""
        self.currentUrlPart = ""
        self.swfUrl = "http://flvplayer.viastream.viasat.tv/flvplayer/play/swf/player.swf"  
        # redirects and won't work with RTMPLib. So we find out what URL to use in
        # InitScript/InitPlugin methods.
        
        #self.swfUrl = "http://flvplayer.viastream.viasat.tv/play/swf/player110516.swf"
        #self.swfUrl = "http://flvplayer.viastream.viasat.tv/flvplayer/play/swf/player110303.swf"
        #self.swfUrl = "http://flvplayer.viastream.viasat.tv/flvplayer/play/swf/player110114.swf"
        #self.swfUrl = "http://flvplayer.viastream.viasat.tv/flvplayer/play/swf/player100920.swf"
        
        """
            Test cases:
                No GEO Lock: Extra Extra
                GEO Lock:    
                Multi Bitrate: Glamourama
        """
        
        return True
    
    def InitScript(self):
        """Initializes the channel for script use
        
        Returns: 
        The value of self.InitEpisodeList()
        
        """
        
        self.swfUrl = uriHandler.Header(self.swfUrl, self.proxy)[1]
        
        # call base
        return chn_class.Channel.InitScript(self)
    
    def InitPlugin(self):
        """Initializes the channel for plugin use
        
        Returns:
        List of MediaItems that should be displayed
        
        This method is called for each Plugin call and can be used to do some 
        channel initialisation. Make sure to set the self.pluginMode = True
        in this methode if overridden.
        
        """
        
        self.swfUrl = uriHandler.Header(self.swfUrl, self.proxy)[1]        
        
        # call base
        return chn_class.Channel.InitPlugin(self)
        
    #==============================================================================
    def PreProcessFolderList(self, data):
        """
        Accepts an data from the ProcessFolderList Methode, BEFORE the items are
        processed. Allows setting of parameters (like title etc). No return value!
        """
        _items = []
        self.seasonTitle = ''
        
#        swfUrls = common.DoRegexFindAll('"([^"]+video\.swf)"', data) 
#        if len(swfUrls) > 0:
#            self.swfUrl = swfUrls[0]
#            logFile.debug("Setting SWF url to: %s", swfUrls[0])
#        
        return (data, _items)
    
    #==============================================================================
    def CreateEpisodeItem(self, resultSet):
        """
        Accepts an arraylist of results. It returns an item. 
        """
        # http://www.tv3play.se/program/alltforbyn
        if not self.channelCode == "sesport":
            url = "%s/%s" % (self.mainListUri, resultSet[0])
        elif self.channelCode == "sesport":
            url = "http://viastream.player.mtgnewmedia.se/xml/xmltoplayer.php?type=siteMapData&channel=1se&country=se&category=%s" %(resultSet[1],)
            
        item = mediaitem.MediaItem(resultSet[1], url)
        item.description = resultSet[1]
        item.icon = self.icon
        return item
    
    #==============================================================================
    def CreateFolderItem(self, resultSet):
        if not self.channelCode == "sesport":
            url = "http://viastream.viasat.tv/Products/Category/%s" % (resultSet[1],)
        else:
            if resultSet[2] == "false":
                url = "http://viastream.player.mtgnewmedia.se/xml/xmltoplayer.php?type=Products&category=%s" % (resultSet[1],)
            else:        
                url = "http://viastream.player.mtgnewmedia.se/xml/xmltoplayer.php?type=siteMapData&channel=3se&country=se&category=%s" % (resultSet[1],)
            
        item = mediaitem.MediaItem(resultSet[0], url)
        item.thumb = self.noImage
        item.type = "folder"
        item.complete = True
        item.icon = self.folderIcon
        return item
    
    #============================================================================= 
    def CreateVideoItem(self, resultSet):
        """
        Accepts an arraylist of results. It returns an item. 
        """
        #logFile.debug('starting FormatVideoItem for %s', self.channelName)
        #logFile.debug(resultSet)
        
        if not resultSet[1] == '':
            self.seasonTitle = resultSet[1]
            return None 
        
        if (self.channelCode == "sesport"):
            url = "http://viastream.player.mtgnewmedia.se/xml/xmltoplayer.php?type=Products&clipid=%s" % (resultSet[0],)
        else:
            url = "http://viastream.viasat.tv/PlayProduct/%s" % (resultSet[2],) #223950

        if self.seasonTitle == "":
            name = "%s %s" (resultSet[3], resultSet[4])
        else:
            name = "%s - %s %s" % (self.seasonTitle, resultSet[3], resultSet[4])
        
        item = mediaitem.MediaItem(name, url)
        
        if resultSet[5] != "":
            item.SetDate(resultSet[6], resultSet[7], resultSet[8], resultSet[9], resultSet[10], 0)
        item.type = "video"
        item.complete = False
        item.icon = self.icon
        item.thumb = self.noImage
        return item
    
    #============================================================================= 
    def UpdateVideoItem(self, item):
        """
        Accepts an item. It returns an updated item. 
        """
        logFile.debug('starting UpdateVideoItem for %s (%s)', item.name, self.channelName)
        data = uriHandler.Open(item.url, pb=False)
        
        for description in common.DoRegexFindAll("<LongDescription><!\[CDATA\[([^<]+)\]\]", data):
            item.description = description
        
        for image in common.DoRegexFindAll("<Url>([^<]+)</Url>\W+</ImageMedia>", data):
            item.thumbUrl = image        
        item.thumb = self.CacheThumb(item.thumbUrl)
        
        srt = ''
        for subtitle in common.DoRegexFindAll("<SamiFile>([^<]+)</SamiFile>", data):
            srt = subtitlehelper.SubtitleHelper.DownloadSubtitle(subtitle, format="dcsubtitle")
            
        # there is just one part in this one:
        part = item.CreateNewEmptyMediaPart()
        part.Subtitle = srt
        for url in common.DoRegexFindAll("<BitRate>(\d+)</BitRate>\W+<FormatID>[^<]+</FormatID>\W+<Url><!\[CDATA\[([^<]+)\]\]></Url>\W+</Video>", data):
            #rtmp://mtgfs.fplive.net/mtg/mp4:flash/latvia/tv3/ugunsgreks/UgunsGreks283_73
            # to
            #rtmp://mtgfs.fplive.net/mtg/flash/latvia/tv3/beztabu/2011.01.17.btbu.mp4
            strmUrl = url[1] 
            if strmUrl.find('mp4:flash') > 0:
                strmUrl = strmUrl.replace('mp4:flash', 'flash') + '.mp4'
            part.AppendMediaStream(strmUrl, bitrate=url[0])

        # Check for the geoblock parameter
        geoLocked = common.DoRegexFindAll("<geoblock>true</geoblock>", data)
        if len(geoLocked) > 0:
            logFile.debug("GeoBlock found, fetching real MediaUrls")
            for mediaItemPart in item.MediaItemParts:
                for stream in mediaItemPart.MediaStreams:
                    data = uriHandler.Open(stream.Url, pb=False)
                    for resultUrl in common.DoRegexFindAll("<url>([^<]+)</url>", data):
                        stream.Url = self.GetVerifiableVideoUrl(resultUrl)
        else:
            for mediaItemPart in item.MediaItemParts:
                for stream in mediaItemPart.MediaStreams:
                    stream.Url = self.GetVerifiableVideoUrl(stream.Url)
                
        item.complete = True
        logFile.debug("Found mediaurl: %s", item)
        return item
