# coding:UTF-8
import sys
import urlparse
import types
import string
#===============================================================================
# Make global object available
#===============================================================================
import common
import mediaitem
import contextmenu
import chn_class
from helpers import htmlentityhelper
from helpers import subtitlehelper

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

register.RegisterChannel('chn_svt')

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
        
        self.guid = "06DB83A2-42F4-11DD-AAC1-CEFD55D89593"
        self.mainListUri = "http://svtplay.se/alfabetisk"
        self.baseUrl = "http://svtplay.se/"
        self.icon = "svticon.png"
        self.iconLarge = "svtlarge.png"
        self.noImage = "svtimage.png"
        self.channelName = "Sveriges Television"
        self.channelDescription = u'Sändningar från SVT'
        self.moduleName = "chn_svt.py"
        self.sortOrder = 101
        self.language = "se"
        self.swfUrl = "http://svtplay.se/flash/svtplayer-2012.1.swf"
        self.requiresLogon = False
        
        self.contextMenuItems = []
        #self.contextMenuItems.append(contextmenu.ContextMenuItem("Download Item", "CtMnDownloadItem", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using Mplayer", "CtMnPlayMplayer", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using DVDPlayer", "CtMnPlayDVDPlayer", itemTypes="video", completeStatus=True))
        
        self.episodeItemRegex = '<li>\W+<a href="([^"]+)">([^<]+)</a>\W+</li>'
        self.videoItemRegex = '<li class="[^"]*"\W*>\W+<a href="([^"]+)"[^>]+title="([^"]*)"[^>]+>\W+<img[^>]+src="([^"]+)[^>]+>\W+(<!--[^/]+/span -->\W+){0,1}<span[^>]*>([^<]+)</span>'
        self.folderItemRegex = '<li class="">\W+<a href="\?([^"]+)"[^>]+>([^<]+)</a>\W+|<li class="[^"]+">\W+<a href="\?([^"]+)" title="" class="folder overlay tooltip">\W+<img [^>]+>\W+<img [^>]+>\W+<span>([^<]+)</span>'
        #self.mediaUrlRegex = '<param name="flashvars" value="pathflv\W*=\W*([^&]+)(_definst_){0,1}/([^&]+)&amp;'
        
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
        
        """
            Testcases:
            
            På spåret - dynamic streams, multiple bitrates
            Oddasat - dynamic streams, multiple bitrates
            kvartersdoktorn - multiple bitrates + subtitles
            Undercover Boss - dynamic streams, multiple bitrates, subtitle
            
            artists_in_residence - FLV
        """
        
        return True
    
    #============================================================================== 
    def PreProcessFolderList(self, data):
        """
        Accepts an data from the ProcessFolderList Methode, BEFORE the items are
        processed. Allows setting of parameters (like title etc). No return value!
        """
        logFile.info("Performing Pre-Processing")
        _items = []
        
        if data.startswith('<!--endif ajaxcall-->'):
            logFile.debug('Received a AJAX response')
            
            # generate pages and add them to the items \{pagenum:(\d+)
            regex = '\{pagenum:(\d+)'
            pageNums = common.DoRegexFindAll(regex, data)
            pages = 1
            for num in pageNums:
                pages = num
            
            # this is a dirty fix and should perhaps be fixed by sorting the output of the chn_class.ProcessFolder method.
            if pages > 1:
                logFile.debug("Adding %s dummy page items for this ajax call", pages)
                for page in range(1,int(pages)+1):
                    data = '%s\nlink button--> <li class=""><a href="dummyUrl" >%s' % (data,page)
        else:
            # determine the current base url
            logFile.debug("Non-Ajax Reponse")
            regex = '<h1>\W+<a href="/([^"]+)">'
            result = common.DoRegexFindAll(regex, data)
            if len(result) > 0:
                self.currentUrlPart = "%s%s/" % (self.baseUrl, result[0])
                logFile.debug("Setting CurrentUrl to %s", self.currentUrlPart)
                                   
            #chop not needed part:
            end = string.find(data, 'showBrowserModule.extra')
            data = common.DoRegexFindAll('[\w\W]{%s}' % (end,), data)[0]        
        return (data, _items)
    
    #==============================================================================
    def CreateEpisodeItem(self, resultSet):
        """
        Accepts an arraylist of results. It returns an item. 
        """
        item = mediaitem.MediaItem(resultSet[1], htmlentityhelper.HtmlEntityHelper.StripAmp(urlparse.urljoin(self.baseUrl, resultSet[0])))
        item.description = "%s%s" % (self.categoryName, item.name)
        item.icon = self.icon
        return item
    
    #==============================================================================
    def CreatePageItem(self, resultSet):
        """
        Accepts an resultset
        """
        logFile.debug("Starting CreatePageItem")
        ajaxTag = "?ajax"
        
        # http://svtplay.se/t/140122/sos_ambulans/?ajax,sb/cb,a1364145,1,f,-1/pb,a1364142,1,f,-1/pl,v,,2668095/sb,p174261,1,f,
        # should become:
        # http://svtplay.se/t/140122/sos_ambulans/?ajax,sb/sb,p174261,%s,f,-1 where %s is the page

        if ajaxTag in self.parentItem.url:            
            url = self.parentItem.url
            logFile.debug(url)
            regex = "(http://[^?]+\?ajax,sb/).*(sb,.+)(\d+)(,\D,)(-{0,1}\d*)"
            regex = common.DoRegexFindAll(regex, url)[0]
            logFile.debug(regex)
            if regex[4] == "": 
                end = "-1"
            else:
                end = regex[4]  
            url = "%s%s%s%s%s" % (regex[0], regex[1], resultSet[1], regex[3], regex[4])
        else:
            url = "%s/%s" % (self.parentItem.url, resultSet[0])    
        
        if not self.pageNavigationRegexIndex == '':
            item = mediaitem.MediaItem(resultSet[self.pageNavigationRegexIndex], url)
        else:
            item = mediaitem.MediaItem("0", "")            
        
        item.type = "page"
        logFile.debug("Created '%s' for url %s", item.name, item.url)
        return item 
    
    #==============================================================================
    def CreateFolderItem(self, resultSet):
        
        # TODO: the self.currentUrlPart is not useable in the Plugin version if they 
        # go more than one level deep. For now we stay on 1 level so it works. 
        if resultSet[0] == '':
            item = mediaitem.MediaItem(resultSet[3], htmlentityhelper.HtmlEntityHelper.StripAmp("%s?ajax,sb/%s" % (self.currentUrlPart, resultSet[2])))
        else:
            item = mediaitem.MediaItem(resultSet[1], htmlentityhelper.HtmlEntityHelper.StripAmp("%s?ajax,sb/%s" % (self.currentUrlPart, resultSet[0])))
        
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
        logFile.debug('starting FormatVideoItem for %s', self.channelName)
        
        item = mediaitem.MediaItem(resultSet[4].strip(), htmlentityhelper.HtmlEntityHelper.StripAmp(urlparse.urljoin(self.baseUrl, resultSet[0])))
        item.description = "%s" % (resultSet[1],)
        item.thumb = self.noImage
        item.thumbUrl = resultSet[2]
        item.type = "video"
        item.complete = False
        item.icon = self.icon
        return item
    
    #============================================================================= 
    def UpdateVideoItem(self, item):
        """
        Accepts an item. It returns an updated item. 
        """
        logFile.debug('starting UpdateVideoItem for %s (%s)', item.name, self.channelName)
        
        item.thumb = self.CacheThumb(item.thumbUrl)
        
        # retrieve the mediaurl
        data = uriHandler.Open(item.url, pb=False)
        
        aspxRegex = 'href="([^"]+wmv)"'
        #aspxRegex = 'href="http://[^=]+vurl=([^"]+wmv)"'
        aspxResults = common.DoRegexFindAll(aspxRegex, data)
        asxRegex = '<a href="([^"]+\.asx)"'
        asxResults = common.DoRegexFindAll(asxRegex, data)
        ramRegex = '<a href="([^"]+\.ram)">'
        ramResults = common.DoRegexFindAll(ramRegex, data)
        flvRegex = '<param name="flashvars" value="pathflv\W*=\W*([^=$&]+)'
        flvResults = common.DoRegexFindAll(flvRegex, data)
        flvRegex2 = '(url:(rtmp[^|&]+),bitrate:(\d+)[|&])'
        flvResults2 = common.DoRegexFindAll(flvRegex2, data)
        
        mediaurl = ""
        if len(asxResults) > 0:
            #then ASX
            logFile.debug("Running ASX")
            mediaurl = "%s%s" % ("http://www.svt.se", asxResults[0])        
        
        elif len(ramResults) > 0:
            #then RAM
            logFile.debug("Running RAM")
            mediaurl = "%s%s" % ("http://www.svt.se", ramResults[0])
        
        elif len(flvResults) > 0:
            #then FLV
            logFile.debug("Running FLV")
            mUrl = flvResults[0]
            if mUrl.startswith("rtmp"):
                mUrl = mediaurl.replace("_definst_","?slist=")
            
            part = item.AppendSingleStream(mUrl)
            part.Subtitle = self.GetSubtitlePath(mUrl)
            #rtmp://fl1.c00928.cdn.qbrick.com/00928/?slist=/kluster/20090101/090102PASPARET_J53UJH
            #rtmp://fl1.c00928.cdn.qbrick.com/00928/_definst_/kluster/20090101/090102PASPARET_J53UJH
        
        elif len(flvResults2) > 0:
            logFile.debug("Running FLV Dynamic Streams")
            
            # iterate through the results, but first sort them and only take unique values.
            flvResults2.sort(lambda x, y: int(y[2]) - int(x[2]))
            #logFile.debug(flvResults2)
            
            bitrate = 2000000
            part = item.CreateNewEmptyMediaPart()

            loadSubtitles = True                    
            for flvResult2 in flvResults2:
                if int(flvResult2[2]) < bitrate:
                    #logFile.debug(flvResult2)
                    stream = part.AppendMediaStream(flvResult2[1].replace("_definst_","?slist="), int(flvResult2[2]))
                    bitrate = int(flvResult2[2])
                    stream.Url = self.GetVerifiableVideoUrl(stream.Url)
                    
                    # get the subtitle
                    if part.Subtitle == "" and loadSubtitles:
                        part.Subtitle = self.GetSubtitlePath(stream.Url)
                        if part.Subtitle == "":
                            # no subtitles are available, so don't load more
                            loadSubtitles = False
            
            #rtmp://fl1.c00928.cdn.qbrick.com/00928/?slist=/kluster/20090101/090102PASPARET_J53UJH
            #rtmp://fl1.c00928.cdn.qbrick.com/00928/_definst_/kluster/20090101/090102PASPARET_J53UJH
        elif len(aspxResults) > 0:
            # first check for ASPX
            logFile.debug("Running WMV %s", aspxResults[0])            
            mediaurl = aspxResults[0]
            if not mediaurl.startswith("http://"):
                logFile.debug("Adding http:// to the url")
                mediaurl = "http://%s" % (mediaurl,)
                 
        if mediaurl != "":
            item.AppendSingleStream(mediaurl)            
        
        if item.HasMediaItemParts():
            item.complete = True            
            logFile.debug("Found mediaurl: %s", item)
        
        return item


    #============================================================================== 
    def PlayVideoItem(self, item, player="defaultplayer"):
        """ NOT USER EDITABLE
        Accepts an item with or without MediaUrl and playback the item. If no 
        MediaUrl is present, one will be retrieved.
        """
        
        for mediaPart in item.MediaItemParts:
            for stream in mediaPart.MediaStreams:
                stream.Url = self.ReplaceMediaUrl(stream.Url)
        
        chn_class.Channel.PlayVideoItem(self, item, player)

    #==============================================================================
    def ReplaceMediaUrl(self, mediaurl):
        """
            retrieves the real Mediaurl
        """
        # if it is a list, it was already processed. 
        if type(mediaurl) is types.ListType or type(mediaurl) is types.TupleType:
            return mediaurl
        
        elif mediaurl.find(".asx") > 0:
            logFile.debug("Parsing ASX")
            data = uriHandler.Open(mediaurl)
            results = common.DoRegexFindAll('<REF HREF\W*=\W*"([^"]+)"\W*/>', data)
            if len(results) > 0:
                mediaurl = results[0]
            
        elif mediaurl.find(".ram") > 0:
            logFile.debug("Parsing RAM")
            mediaurl = uriHandler.Open(mediaurl)
            mediaurl = mediaurl.split('\n')

        return mediaurl 
    
    def GetSubtitlePath(self, mediaUrl):
        """ Retrieves a subtitle path from the mediaUrl
        
        
        dynamicStreams : url:rtmpe://fl11.c90909.cdn.qbrick.com/90909/_definst_/kluster/20110703/PG-1160692-006A-MIHIGHSERIEI-01-mp4-e-v1.mp4,bitrate:2400|url:rtmpe://fl11.c90909.cdn.qbrick.com/90909/_definst_/kluster/20110703/PG-1160692-006A-MIHIGHSERIEI-01-mp4-d-v1.mp4,bitrate:1400|url:rtmpe://fl11.c90909.cdn.qbrick.com/90909/_definst_/kluster/20110703/PG-1160692-006A-MIHIGHSERIEI-01-mp4-c-v1.mp4,bitrate:850|url:rtmpe://fl11.c90909.cdn.qbrick.com/90909/_definst_/kluster/20110703/PG-1160692-006A-MIHIGHSERIEI-01-mp4-b-v1,bitrate:320
        subtitle : http://media.svt.se/download/mcc/kluster/20110703/PG-1160692-006A-MIHIGHSERIEI-01_sv.wsrt
        
        Here is another of Trapped:
        dynamicStreams : url:rtmpe://fl11.c90909.cdn.qbrick.com/90909/_definst_/kluster/20110703/PG-1136275-015A-TRAPPEDI-01-mp4-e-v1.mp4,bitrate:2400|url:rtmpe://fl11.c90909.cdn.qbrick.com/90909/_definst_/kluster/20110703/PG-1136275-015A-TRAPPEDI-01-mp4-d-v1.mp4,bitrate:1400|url:rtmpe://fl11.c90909.cdn.qbrick.com/90909/_definst_/kluster/20110703/PG-1136275-015A-TRAPPEDI-01-mp4-c-v1.mp4,bitrate:850|url:rtmpe://fl11.c90909.cdn.qbrick.com/90909/_definst_/kluster/20110703/PG-1136275-015A-TRAPPEDI-01-mp4-b-v1,bitrate:320
        subtitle : http://media.svt.se/download/mcc/kluster/20110703/PG-1136275-015A-TRAPPEDI-01_sv.wsrt

        """
        
        startIndex = mediaUrl.find("/kluster/") 
        endIndex = mediaUrl.find("mp4")
        if startIndex > 0 and endIndex > 0:
            namePart = mediaUrl[startIndex:endIndex-1]
            subUrl = "http://media.svt.se/download/mcc%s_sv.wsrt" % (namePart,)
            fileName = namePart[namePart.rindex("/")+1:] + ".srt"
            return subtitlehelper.SubtitleHelper.DownloadSubtitle(subUrl, fileName, 'srt')
        else:
            return ""        