import sys

import xbmcgui
import xbmc


#===============================================================================
# Make global object available
#===============================================================================
import common
import mediaitem
import contextmenu
import chn_class
from locker import LockWithDialog
from config import Config
from helpers import htmlentityhelper
from helpers import xmlhelper
from helpers import subtitlehelper
import settings

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

register.RegisterChannel('chn_bbc','bbc1')
register.RegisterChannel('chn_bbc','bbc2')
register.RegisterChannel('chn_bbc','bbc3')
register.RegisterChannel('chn_bbc','bbc4')
register.RegisterChannel('chn_bbc','cbbc')
register.RegisterChannel('chn_bbc','cbeebies')
register.RegisterChannel('chn_bbc','bbchd')
register.RegisterChannel('chn_bbc','bbcnews')
register.RegisterChannel('chn_bbc','bbcparliament')
register.RegisterChannel('chn_bbc','bbcalba')
register.RegisterChannel('chn_bbc','bbciplayersearch')

#===============================================================================
# main Channel Class
#===============================================================================
class Channel(chn_class.Channel):
    #===============================================================================
    # define class variables
    #===============================================================================
    def InitialiseVariables(self):
        """Used for the initialisation of user defined parameters. 
        
        All should be present, but can be adjusted. If overridden by derived class
        first call chn_class.Channel.InitialiseVariables(self) to make sure all
        variables are initialised. 
        
        Returns:
        True if OK
        
        """
        
        #http://feeds.bbc.co.uk/iplayer/search/tv/?q=singapore
        
        # call base function first to ensure all variables are there
        chn_class.Channel.InitialiseVariables(self)
        
        if self.channelCode == "bbc1":
            self.guid = "CB6B08F0-DD6A-11E0-B158-FFFB4824019B"
            self.icon = "bbc1thumb.png"
            self.iconLarge = "bbc1large.png"
            self.noImage = "bbc1image.png"
            self.channelName = "BBC One"
            self.channelDescription = "Episodes from BBC One iPlayer"
            self.mainListUri = "http://feeds.bbc.co.uk/iplayer/bbc_one/list"
            self.sortOrder = 151
        
        elif self.channelCode == "bbc2":
            self.guid = "8FF7DE8A-DD6D-11E0-AF1F-A4FF4824019B"
            self.icon = "bbc2thumb.png"
            self.iconLarge = "bbc2large.png"
            self.noImage = "bbc2image.png"
            self.channelName = "BBC Two"
            self.channelDescription = "Episodes from BBC Two iPlayer"
            self.mainListUri = "http://feeds.bbc.co.uk/iplayer/bbc_two/list"
            self.sortOrder = 152
        
        elif self.channelCode == "bbc3":
            self.guid = "C7962E5C-DE33-11E0-A9EE-1D7F4824019B"
            self.icon = "bbc3thumb.png"
            self.iconLarge = "bbc3large.png"
            self.noImage = "bbc3image.png"
            self.channelName = "BBC Three"
            self.channelDescription = "Episodes from BBC Three iPlayer"
            self.mainListUri = "http://feeds.bbc.co.uk/iplayer/bbc_three/list"
            self.sortOrder = 153
         
        elif self.channelCode == "bbc4":
            self.guid = "DEB79882-DE33-11E0-94A4-267F4824019B"
            self.icon = "bbc4thumb.png"
            self.iconLarge = "bbc4large.png"
            self.noImage = "bbc4image.png"
            self.channelName = "BBC Four"
            self.channelDescription = "Episodes from BBC Four iPlayer"
            self.mainListUri = "http://feeds.bbc.co.uk/iplayer/bbc_four/list"           
            self.sortOrder = 154

        elif self.channelCode == "cbbc":
            self.guid = "28198F12-DE34-11E0-8523-C77F4824019B"
            self.icon = "cbbcthumb.png"
            self.iconLarge = "cbbclarge.png"
            self.noImage = "cbbcimage.png"
            self.channelName = "CBBC"
            self.channelDescription = "Episodes from CBBC iPlayer"
            self.mainListUri = "http://feeds.bbc.co.uk/iplayer/cbbc/list"           
            self.sortOrder = 155

        elif self.channelCode == "cbeebies":
            self.guid = "632E7568-DE34-11E0-A644-02804824019B"
            self.icon = "cbeebiesthumb.png"
            self.iconLarge = "cbeebieslarge.png"
            self.noImage = "cbeebiesimage.png"
            self.channelName = "CBeebies"
            self.channelDescription = "Episodes from CBeebies iPlayer"
            self.mainListUri = "http://feeds.bbc.co.uk/iplayer/cbeebies/list"           
            self.sortOrder = 156
        
        elif self.channelCode == "bbchd":
            self.guid = "67794EAE-DE34-11E0-B79B-11804824019B"
            self.icon = "bbchdthumb.png"
            self.iconLarge = "bbchdlarge.png"
            self.noImage = "bbchdimage.png"
            self.channelName = "BBC HD"
            self.channelDescription = "Episodes from BBC HD iPlayer"
            self.mainListUri = "http://feeds.bbc.co.uk/iplayer/bbc_hd/list"           
            self.sortOrder = 157

        elif self.channelCode == "bbcnews":
            self.guid = "6C99A8FC-DE34-11E0-B40A-18804824019B"
            self.icon = "bbcnewsthumb.png"
            self.iconLarge = "bbcnewslarge.png"
            self.noImage = "bbcnewsimage.png"
            self.channelName = "BBC News Channel"
            self.channelDescription = "Episodes from BBC News Channel iPlayer"
            self.mainListUri = "http://feeds.bbc.co.uk/iplayer/bbc_news24/list"           
            self.sortOrder = 157
            
        elif self.channelCode == "bbcparliament":
            self.guid = "724FD12C-DE34-11E0-9795-3B804824019B"
            self.icon = "bbcparliamentthumb.png"
            self.iconLarge = "bbcparliamentlarge.png"
            self.noImage = "bbcparliamentimage.png"
            self.channelName = "BBC Parliament"
            self.channelDescription = "Episodes from BBC Parliament iPlayer"
            self.mainListUri = "http://feeds.bbc.co.uk/iplayer/bbc_parliament/list"           
            self.sortOrder = 157
            
        elif self.channelCode == "bbcalba":
            self.guid = "718219B2-DE34-11E0-94D7-37804824019B"
            self.icon = "bbcalbathumb.png"
            self.iconLarge = "bbcalbalarge.png"
            self.noImage = "bbcalbaimage.png"
            self.channelName = "BBC Alba"
            self.channelDescription = "Episodes from BBC Alba iPlayer"
            self.mainListUri = "http://feeds.bbc.co.uk/iplayer/bbc_alba/list"           
            self.sortOrder = 157
        
        elif self.channelCode == "bbciplayersearch":
            self.guid = "739E4322-E796-11E0-8604-1B2F4924019B"
            self.icon = "bbciplayerthumb.png"
            self.iconLarge = "bbciplayerlarge.png"
            self.noImage = "bbciplayerimage.png"
            self.channelName = "BBC iPlayer Search"
            self.channelDescription = "Search the BBC iPlayer"
            self.mainListUri = ""           
            self.sortOrder = 158
        else:
            raise ValueError("No such channelcode", self.channelCode)
        
        
        self.baseUrl = "http://www.bbc.co.uk/"
        self.moduleName = "chn_bbc.py"
        self.language = "en-gb"
        self.requiresLogon = False
        self.swfUrl = "http://www.bbc.co.uk/emp/10player.swf"
        
        self.episodeItemRegex = "(<entry>([\w\W]*?)</entry>)"
        self.videoItemRegex = '' 
        self.folderItemRegex = ''
        self.mediaUrlRegex = ''
        
        self.searchUrl = "http://feeds.bbc.co.uk/iplayer/search/tv/?q=%s"
        
        self.contextMenuItems = []
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Test Proxy Server", "CtMnTestProxy", plugin=True))
        
        #============================================================================== 
        # non standard items
        self.programs = dict()
        
        return True
    
    @LockWithDialog(logger = logFile)
    def CtMnTestProxy(self, item):
        """ Checks if the proxy is OK"""
        
        proxy = settings.AddonSettings().GetIPlayerProxy()
        
        if not proxy:
             message = "Proxy not configured" % (settings.AddonSettings().GetIPlayerProxy(),)
        else:
            url = Config.updateUrl + "proxy"
            data = uriHandler.Open(url, proxy = proxy)
            #logFile.debug(data)
            if data == "1":
                message = "Proxy '%s' is working" % (settings.AddonSettings().GetIPlayerProxy(),)
            else:
                message = "Proxy '%s' is not working\nas expected" % (settings.AddonSettings().GetIPlayerProxy(),)
                
        logFile.debug(message)
        
        dialog = xbmcgui.Dialog()            
        dialog.ok(Config.appName, message)        
        pass   
    
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

        if self.channelCode == "bbciplayersearch":
            # clear some stuff
            self.mainListItems = []
            self.programs = dict()
            keyboard = xbmc.Keyboard('')
            keyboard.doModal()
            if not keyboard.isConfirmed():
                return None
            
            needle = keyboard.getText()
            logFile.info("Searching BBC for needle: %s", needle)
            self.mainListUri = self.searchUrl % (needle,)
        elif len(self.mainListItems) == 0:
            # in case we refreshed, the mainlistitems are empty, so we should
            # clear the program list
            self.programs = dict() 
        
        items = chn_class.Channel.ParseMainList(self, returnData=returnData)
        return items
    
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
        
        # http://www.rtl.nl/system/s4m/xldata/abstract/218927.xml
        xmlData = xmlhelper.XmlHelper(resultSet[0])
        
        title = xmlData.GetSingleNodeContent("title")  
        
        # now get the program out of the title:
        program = common.DoRegexFindAll("^(.+?)(: .+|)$", title)[-1][0]
        if program in self.programs:
            # attach the episode to the program
            logFile.debug("Existing program found: %s", program)
            episodeItem = self.programs[program]
            # do not return, just append
            returnValue = None             
        else:
            # create the episode item
            episodeItem = mediaitem.MediaItem(program, "")
            episodeItem.icon = self.icon
            episodeItem.complete = True
            episodeItem.thumb = self.noImage
            
            # store it for the next items
            self.programs[program] = episodeItem
            # return value is the new episodeitem
            returnValue = episodeItem
            
        # attach the sub item
        item = self.CreateVideoItem(resultSet)
        
        # update the main item
        date = xmlData.GetSingleNodeContent("updated")
        year = date[0:4]
        month = date[5:7]
        day = date[8:10]
        item.SetDate(year, month, day)
        
        # update the date of the new item:
        episodeItem.SetDate(year, month, day, onlyIfNewer = True)
        episodeItem.thumbUrl = item.thumbUrl
        
        # link them up
        episodeItem.items.append(item)
        item.parent = episodeItem
        
        return returnValue    
    
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

        #logFile.debug('starting CreateVideoItem for %s', self.channelName)
        
        xmlData = xmlhelper.XmlHelper(resultSet[0])
        title = xmlData.GetSingleNodeContent("title")
        
        # http://www.bbc.co.uk/iplayer/images/episode/b014gsgn_512_288.jpg
        thumb = xmlData.GetTagAttribute("media:thumbnail", {'url':None})
        thumb = thumb[0:thumb.index("_")] + "_512_288.jpg"
        if thumb == "":        
            thumb = self.noImage
        
        # description
        #TODO
        description = xmlData.GetSingleNodeContent("content").split("\n")
        description = description[len(description)-3].strip()
        
        # id
        id = xmlData.GetSingleNodeContent("id")[-8:]
        #logFile.debug(id)
        
        url = "http://www.bbc.co.uk/iplayer/playlist/%s" % (id,)
        
        item = mediaitem.MediaItem(title, url)
        item.icon = self.icon
        item.description = description
        item.type = 'video'
        item.thumb = self.noImage
        item.thumbUrl = thumb        
        item.complete = False
        return item
    
    def UpdateVideoItem(self, item):
        """
        Accepts an item. It returns an updated item. 
        """
        logFile.debug('starting UpdateVideoItem for %s (%s)', item.name, self.channelName)
        
        metaData = uriHandler.Open(item.url, pb=False, proxy=self.proxy)
        
        xmlMetaData = xmlhelper.XmlHelper(metaData)
        # <item kind="programme" duration="3600" identifier="b014r5hj" group="b014r5jm" publisher="pips">
        videoIds = xmlMetaData.GetTagAttribute("item", {'kind': 'programme'}, {'identifier':None}, firstOnly = False)
        
        for videoId in videoIds:
            logFile.debug("Found videoId: %s", videoId)
            # foreach ID add a part
            part = item.CreateNewEmptyMediaPart()
            
            streamDataUrl = "http://www.bbc.co.uk/mediaselector/4/mtis/stream/%s" % (videoId)
            proxy = settings.AddonSettings().GetIPlayerProxy()
            streamData = uriHandler.Open(streamDataUrl, pb=False, proxy=proxy)
            #logFile.debug(streamData)
            connectionDatas = common.DoRegexFindAll('<media bitrate="(\d+)"[^>]+>\W*(<connection[^>]+>)\W*(<connection[^>]+>)*\W*</media>', streamData)
            for connectionData in connectionDatas:
                #logFile.debug(connectionData)
                # first the bitrate
                bitrate = connectionData[0]
                
                # the limelight seem to work, so let's just stick with those
                if "limelight" in connectionData[1]:
                    connection = connectionData[1]
                elif connectionData[-1] == '':
                    connection = connectionData[1]
                else:
                    connection = connectionData[-1]
                connectionXml = xmlhelper.XmlHelper(connection)
                
                #port: we take the default one                
                #determine protocol
                protocol = connectionXml.GetTagAttribute("connection", {"protocol" : None})
                if protocol == "http":
                    logFile.debug("Http stream found, skipping for now.")
                    continue
                    
                    url = connectionXml.GetTagAttribute("connection", {"href" : None})
                    part.AppendMediaStream(url, bitrate)
                    # for http is ends here
                    continue;
                elif protocol == "":
                    protocol = "rtmp"
                
                # now for the non-http version, we need application, authentication, server, file and kind
                application = connectionXml.GetTagAttribute("connection", {"application" : None})
                if application == "":
                    application = "ondemand"
                
                authentication = connectionXml.GetTagAttribute("connection", {"authString" : None})
                authentication = htmlentityhelper.HtmlEntityHelper.ConvertHTMLEntities(authentication)
                server = connectionXml.GetTagAttribute("connection", {"server" : None})
                
                file = connectionXml.GetTagAttribute("connection", {"identifier" : None})
                if protocol == "":
                    protocol = "rtmp"
                
                kind = connectionXml.GetTagAttribute("connection", {"kind" : None})
                
                #logFile.debug("XML: %s\nProtocol: %s, Server: %s, Application: %s, Authentication: %s, File: %s , Kind: %s", connection, protocol, server, application, authentication, file, kind)
                if kind == "limelight":
                    logFile.debug("Creating RTMP for LimeLight type")
                    # for limelight we need to be more specific on what to play
                    url = "%s://%s/ app=%s?%s tcurl=%s://%s/%s?%s playpath=%s" % (protocol, server, application, authentication, protocol, server, application, authentication, file)
                else:
                    logFile.debug("Creating RTMP for a None-LimeLight type")
                    # for a none-limelight we just compose a RTMP stream
                    url = "%s://%s/%s?%s playpath=%s" % (protocol, server, application, authentication, file)
                url = self.GetVerifiableVideoUrl(url)
                part.AppendMediaStream(url, bitrate)
                        
            # get the subtitle
            subtitles = common.DoRegexFindAll('<connection href="(http://www.bbc.co.uk/iplayer/subtitles/[^"]+/)([^/]+.xml)"', streamData)
            if len(subtitles) > 0:
                subtitle = subtitles[0]
                subtitleUrl = "%s%s" % (subtitle[0], subtitle[1])
                part.Subtitle = subtitlehelper.SubtitleHelper.DownloadSubtitle(subtitleUrl, subtitle[1], "ttml")
        
        if item.thumbUrl != "":
            item.thumb = self.CacheThumb(item.thumbUrl)
        item.complete = True
        
        logFile.info('finishing UpdateVideoItem: %s.', item)
        return item