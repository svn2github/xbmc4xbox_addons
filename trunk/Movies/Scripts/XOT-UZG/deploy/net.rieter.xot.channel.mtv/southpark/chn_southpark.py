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

import helpers
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

register.RegisterChannel('chn_southpark', 'southpark')

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
        self.guid = "3ac3d6d0-5b2a-11dd-ae16-0800200c9a66"
        self.icon = "southparkicon.png"
        self.iconLarge = "southparklarge.png"
        self.noImage = "southparkimage.png"
        self.channelName = "Southpark.NL"
        self.channelDescription = "Southpark Epsides for playback in The Netherlands."
        self.moduleName = "chn_southpark.py"
        self.mainListUri = "http://www.southpark.nl/episodes/"
        self.baseUrl = "http://www.southpark.nl"
        self.onUpDownUpdateEnabled = True
        self.defaultPlayer = 'dvdplayer' #(defaultplayer, dvdplayer, mplayer)
        self.language = "nl"
        #self.swfUrl = "http://media.mtvnservices.com/player/prime/mediaplayerprime.1.6.0.swf"
        #self.swfUrl = "http://media.mtvnservices.com/player/prime/mediaplayerprime.1.8.1.swf"
        self.swfUrl = "http://media.mtvnservices.com/player/prime/mediaplayerprime.1.11.3.swf"
        
        self.contextMenuItems = []
#        self.contextMenuItems.append(contextmenu.ContextMenuItem("Update Item", "CtMnUpdateItem", itemTypes="video", completeStatus=None))            
#        self.contextMenuItems.append(contextmenu.ContextMenuItem("Initialise", "CtMnInit", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using Mplayer", "CtMnPlayMplayer", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using DVDPlayer", "CtMnPlayDVDPlayer", itemTypes="video", completeStatus=True))
                
        self.requiresLogon = False
        
        self.episodeItemRegex = '<li[^>]*>\W*<a[^>]+href="(/guide/episodes/season/[^"]+)">(\d+)</a>' # used for the ParseMainList
        self.videoItemRegex = '<div class="image">\W+<a href="/guide([^"]+)"><img src="([^"]+)" alt="[^"]+" /></a>\W+</div>\W[^:]+<span class="epnumber">Episode: \d(\d+)</span>\W+<span[^>]+>([^<]+)</span>\W+<span class="epdate">(\d+)-(\d+)-(\d+)</span>\W+<span class="epdesc">([^/]+)</span>\W+</a>\W+<div class="more">\W+<a href="/episodes/(\d+)/"'   # used for the CreateVideoItem 
        self.mediaUrlRegex = ''  
        return True
      
    #==============================================================================
    # ContextMenu functions
    #==============================================================================
    def CtMnInit(self, item):
        logFile.debug("Intializing from menu")
        url = "http://www.southparkstudios.com/stats/register.php/videos/147434"
        uriHandler.Open(url)
    
    #==============================================================================
    def CreateEpisodeItem(self, resultSet):
        """
        Accepts an arraylist of results. It returns an item. 
        """
        logFile.debug('starting CreateEpisodeItem for %s', self.channelName)
        
        # <li><a href="(/guide/season/[^"]+)">(\d+)</a></li>
        item = mediaitem.MediaItem("Season %02d" % int(resultSet[1]), urlparse.urljoin(self.baseUrl, resultSet[0]))
        item.icon = self.icon
        item.complete = True
        return item
    
    #============================================================================= 
    def CreateVideoItem(self, resultSet):
        """
        Accepts an arraylist of results. It returns an item. 
        """
        logFile.debug('starting CreateVideoItem for %s', self.channelName)
        
        url = urlparse.urljoin(self.baseUrl, resultSet[0])
        item = mediaitem.MediaItem("%s %s" % (resultSet[2], resultSet[3]), url)
        
        item.thumb = self.noImage
        item.thumbUrl = resultSet[1]
        item.SetDate(resultSet[4], resultSet[6], resultSet[5])
        item.icon = self.icon
        item.description = resultSet[7]                                
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
        
        # download the thumb
        item.thumb = self.CacheThumb(item.thumbUrl)        
        
        # 1 - get the overal config file
        guidRegex = 'http://[^:]+/(mgid:[^"]+:[0-9a-f-]{36})"'
        data = uriHandler.Open(item.url)
        resultSet = common.DoRegexFindAll(guidRegex, data)
        guid = htmlentityhelper.HtmlEntityHelper.UrlEncode(resultSet[0])
        feedPart = "feeds/video-player/mrss"
        infoUrl = "%s/%s" % (urlparse.urljoin(self.baseUrl, feedPart), guid)
        #http://www.southpark.nl/feeds/as3player/config.php?uri=mgid%3Ahcx%3Acontent%3Asouthparkstudios.nl%3A5f4bbfc8-1e22-4aef-bda0-9ee7b993b5bc&group=entertainment&type=network
        #http://www.southpark.nl/feeds/video-player/mrss/mgid%3Ahcx%3Acontent%3Asouthparkstudios.nl%3A7c0e7b51-3da1-4dc6-950a-4e0d9dae96bb

        # 2- Get the GUIDS for the different ACTS
        infoData = uriHandler.Open(infoUrl)
        actGuidRegex = '<guid isPermaLink="false">([^<]+)</guid>' 
        playerGuids = common.DoRegexFindAll(actGuidRegex, infoData)

        # 3 - Load one act and find the RTMP(E) file off all the acts (First the opening act)
        #sp_1401_act1_512x288_450.mp4
        #0303_1_DI_640x480_700kbps.flv
        flvRegex = '(rtmp[^\n]+\d{4}_)(act|)(\d)(_[^.]+_)(\d{3,4})(kbps|)(.flv|.mp4)'
        #                    0           1    2    3        4        5      6
        actUrlPattern = []
        actId = 0;
        for playerGuid in playerGuids:
            # create a new part
            part = item.CreateNewEmptyMediaPart()
                
            if len(actUrlPattern) == 0:
                # first try, we need to determine the URL pattern
                logFile.debug("Trying to determine the URL pattern")
                
                actGuid = htmlentityhelper.HtmlEntityHelper.UrlEncode(playerGuid)
                mediaGenPart = "feeds/as3player/mediagen.php"
                actUrl = "%s?uri=%s" % (urlparse.urljoin(self.baseUrl, mediaGenPart), actGuid) 
                           
                # load the url and get the info for the media urls:
                data = uriHandler.Open(actUrl, pb=False)
                intros = common.DoRegexFindAll('<src>([^<]+_)(\d+)(kbps[^<]+|[^<]+)</src>', data)
                
                # if the URL matches the flvRegex than we can determine the others.
                actParts = common.DoRegexFindAll(flvRegex, data)
                
                if len(actParts) > 0:
                    # handle acts
                    logFile.debug("First act found these possible acts: %s", actParts)
                    flvParts = filter(lambda x: x[6] == ".flv", actParts)                    
                    
                    for actPart in actParts:
                        #logFile.debug(actPart)
                        # store the pattern for determination of other parts
                        bitrate = actPart[4]
                        pattern = "%s%s%s%s%s%s%s" % (actPart[0], actPart[1], "%s", actPart[3], actPart[4], actPart[5], actPart[6])
                        actUrlPattern.append((bitrate, pattern))
                        
                        # append the stream to the part
                        actId = int(actPart[2])
                        url = pattern % (actId,)
                        url = self.GetVerifiableVideoUrl(url)
                        part.AppendMediaStream(url, bitrate)                        
                else:
                    # no act match, so must be intro
                    logFile.debug("Southpark intro matched")
                    for intro in intros:
                        url = "%s%s%s" % (intro[0], intro[1], intro[2])
                        url = self.GetVerifiableVideoUrl(url)
                        part.AppendMediaStream(url, intro[1])                    
            else:
                # Use the previously determined URL's to guess the new ones.
                logFile.debug("Using prevously determined URL pattern to get other parts")                
                actId = actId + 1                    
                for (bitrate,pattern) in actUrlPattern:
                    url = pattern % (actId,)
                    url = self.GetVerifiableVideoUrl(url)
                    part.AppendMediaStream(url, bitrate)
            
            #url = self.GetVerifiableVideoUrl(url)
            #item.AppendSingleStream(url)
                
        item.complete = True
        logFile.debug("Media item updated: %s", item)
        return item    