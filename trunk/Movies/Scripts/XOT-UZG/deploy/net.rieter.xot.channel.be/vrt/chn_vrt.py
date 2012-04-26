# coding:Cp1252
#===============================================================================
# Import the default modules
#===============================================================================
import sys
import urlparse
#===============================================================================
# Make global object available
#===============================================================================
import common
import mediaitem
import contextmenu
import chn_class
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

register.RegisterChannel('chn_vrt', 'redactie')
register.RegisterChannel('chn_vrt', 'ketnet')
register.RegisterChannel('chn_vrt', 'sporza')
register.RegisterChannel('chn_vrt', 'cobra')

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
        
        if self.channelCode == "redactie":
            self.guid = "79C799AE-B6BA-11E0-87FD-20434824019B"
            self.icon = "redactieicon.png"
            self.iconLarge = "redactielarge.png"
            self.noImage = "redactieimage.png"
            self.channelName = "De Redactie"
            self.channelDescription = "Online uitzendingen van www.deredactie.be."
            self.sortOrder = 122
            self.mainListUri = "http://www.deredactie.be/cm/vrtnieuws/mediatheek"
            self.baseUrl = "http://www.deredactie.be"
        
        elif self.channelCode == "ketnet":
            self.guid = "756FFEC8-B6BA-11E0-898D-1F434824019B"
            self.icon = "ketneticon.png"
            self.iconLarge = "ketnetlarge.png"
            self.noImage = "ketnetimage.png"
            self.channelName = "Ketnet"
            self.channelDescription = "Online uitzendingen van www.ketnet.be."
            self.sortOrder = 123
            self.mainListUri = "http://video.ketnet.be/cm/ketnet/ketnet-mediaplayer"
            self.baseUrl = "http://video.ketnet.be"
        
        elif self.channelCode == "sporza":
            self.guid = "71128378-B6BA-11E0-A68A-1B434824019B"
            self.icon = "sporzaicon.png"
            self.iconLarge = "sporzalarge.png"
            self.noImage = "sporzaimage.png"
            self.channelName = "Sporza"
            self.channelDescription = "Online uitzendingen van www.sporza.be."
            self.sortOrder = 124
            self.mainListUri = "http://www.sporza.be/cm/sporza/videozone"
            self.baseUrl = "http://www.sporza.be"
        
        elif self.channelCode == "cobra":
            self.guid = "6C7374A8-B6BA-11E0-A21E-1A434824019B"
            self.icon = "cobraicon.png"
            self.iconLarge = "cobralarge.png"
            self.noImage = "cobraimage.png"
            self.channelName = "Cobra"
            self.channelDescription = "Online uitzendingen van www.cobra.be."
            self.sortOrder = 125
            self.mainListUri = "http://www.cobra.be/cm/cobra/cobra-mediaplayer"
            self.baseUrl = "http://www.cobra.be"
        
        self.swfUrl = "%s/html/flash/common/player.swf" % (self.baseUrl,)
        self.episodeItemRegex = '<div><a href="(/cm(?:/[^/"]+){3})" [^>]+>(?:([^<]+)|<img [^>]+alt="([^"]+)"/>)</a></div>' # used for the ParseMainList
        self.videoItemRegex = '(?:<h3><[^>]+><strong>([^<]+)</strong></h3>|(<div class="mediaItem"[\W\w]+?</div>))'
        self.mediaUrlRegex = "Server'] = '([^']+)';\W+[^]]+Path'] = '([^']+)';" 
        self.pageNavigationRegex = '<a href="([^"]+\?page=\d+)"[^>]+>(\d+)' 
        self.pageNavigationRegexIndex = 1
            
        self.moduleName = "chn_vrt.py"            
        self.language = "be"
        
        self.contextMenuItems = []
#        self.contextMenuItems.append(contextmenu.ContextMenuItem("Update Item", "CtMnUpdateItem", itemTypes="video", completeStatus=None))            
#        self.contextMenuItems.append(contextmenu.ContextMenuItem("Download Item", "CtMnDownloadItem", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using Mplayer", "CtMnPlayMplayer", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using DVDPlayer", "CtMnPlayDVDPlayer", itemTypes="video", completeStatus=True))        
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
        
        (items, data) = chn_class.Channel.ParseMainList(self, returnData=True)
        
        if not data == "": 
            # if data was retrieved, fetch the child items
            for item in items:
                urlPart = urlparse.urlsplit(item.url)[2]
                #logFile.debug(urlPart)
                subRegex = '<a href="(%s/[^"]+)" title\W+"([^"]+)' % (urlPart)
                results = common.DoRegexFindAll(subRegex, data)
                for resultSet in results:
                    subItem = self.CreateFolderItem(resultSet)
                    subItem.parent = item
                    item.items.append(subItem) 
        
        if returnData:
            return (items, data)
        else:
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
        
        #logFile.debug('starting CreateEpisodeItem for %s', self.channelName)
        
        url = "%s%s" % (self.baseUrl, resultSet[0])
        if resultSet[1] == "":
            name = resultSet[2]
        else:
            name = resultSet[1]
        
        item = mediaitem.MediaItem(name.capitalize(), url)
        item.icon = self.icon
        item.type = "folder"
        item.complete = True
        return item
    
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
        
        #logFile.debug('starting CreateFolderItem for %s', self.channelName)
        name = "%s%s" % (resultSet[1][0].upper(), resultSet[1][1:])                
        item = mediaitem.MediaItem(name, urlparse.urljoin(self.baseUrl, resultSet[0]))
        item.complete = True
        item.icon = self.folderIcon
        item.thumb = self.noImage
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
        
        html = htmlhelper.HtmlHelper(resultSet[1])
        url = html.GetTagAttribute("div", {"class" : "mediaItem"} , {"id" : None})
        name = html.GetTagAttribute("img", {"title" : None})
        
        #logFile.debug(url)
        #logFile.debug(resultSet[1])
        
        thumb = html.GetTagAttribute("img", {"src" : None})
        if not ":" in thumb:
            thumb = "http://www.deredactie.be%s" % (thumb,)
        
        item = mediaitem.MediaItem(name, url)
        item.thumb = self.noImage
        item.thumbUrl = thumb
        item.description = name
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
        
        item.thumb = self.CacheThumb(item.thumbUrl)        
        
        """
        vars267354594['type'] = 'video';
        vars267354594['view'] = 'popupPlayer';
        vars267354594['divId'] = 'div_267354594';
        vars267354594['flashId'] = 'flash_267354594';
        vars267354594['format'] = '';
        vars267354594['wmode'] = 'transparent';
        vars267354594['title'] = encodeURIComponent('De familievete van Marijke Pinoy en Dimitri Verhulst');
        vars267354594['rtmpServer'] = 'rtmp://vrt.flash.streampower.be/sporza';
        vars267354594['rtmpPath'] = '2011/07/121632590GINDSTUSS5088380.urlFLVLong.flv';
        vars267354594['rtmptServer'] = 'rtmpt://vrt.flash.streampower.be/sporza';
        vars267354594['rtmptPath'] = '2011/07/121632590GINDSTUSS5088380.urlFLVLong.flv';
        vars267354594['iphoneServer'] = 'http://iphone.streampower.be/vrtnieuws_nogeo/_definst_';
        vars267354594['iphonePath'] = '2011/07/121632590GINDSTUSS5088380.urlMP4_H.264.m4v';
        vars267354594['mobileServer'] = 'rtsp://mp4.streampower.be/vrt/vrt_mobile/sporza_nogeo';
        vars267354594['mobilePath'] = '2011/07/121632590GINDSTUSS5088380.url3GP_MPEG4.3gp';
        vars267354594['thumb'] = '/polopoly_fs/1.1066851!image/1223351651.png';        
        """
        
        # now the mediaurl is derived. First we try WMV
        data = uriHandler.Open(item.url, pb=False)
        
        descriptions = common.DoRegexFindAll('<div class="longdesc"><p>([^<]+)</', data)
        for desc in descriptions:
            item.description = desc
            
        urls = common.DoRegexFindAll(self.mediaUrlRegex, data)
        part = item.CreateNewEmptyMediaPart()
        for url in urls:
            server = url[0]
            path = url[1]
            
            if server != "":
                if server.startswith("rtmp:") or server.startswith("rtmpt:"):
                    mediaUrl = "%s//%s" % (server,path)
                    mediaUrl = self.GetVerifiableVideoUrl(mediaUrl)
                    part.AppendMediaStream(mediaUrl, 800)
                elif "_definst_" in server:
                    continue
#                    #http://iphone.streampower.be/vrtnieuws_nogeo/_definst_/2011/07/151204967HOORENSVL2123520.urlMP4_H.264.m4v/playlist.m3u8
#                    bitrate = 1200
#                    mediaurl = mediaurl.replace("definst_//", "definst_/")+"/playlist.m3u8"
#                    mobileData = uriHandler.Open(mediaurl, pb=False)
#                    mobileUrls = common.DoRegexFindAll("BANDWIDTH=(\d+)\d{3}\W+(http://[^\n]+)", mobileData)
#                    for mobileUrl in mobileUrls:
#                        logFile.debug(mobileUrl)
#                        part.AppendMediaStream(mobileUrl[1], mobileUrl[0])
                else:
                    mediaUrl = "%s/%s" % (server,path)
                    part.AppendMediaStream(mediaUrl, 100)
                item.complete = True
            #logFile.debug("Media url was found: %s", item)            
        else:
            logFile.debug("Media url was not found.")

        return item    
