# coding:UTF-8
import sys
import urlparse
#===============================================================================
# Make global object available
#===============================================================================
import common
import mediaitem 
import contextmenu
import chn_class
from helpers import htmlentityhelper
from helpers import brightcovehelper

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

register.RegisterChannel('chn_sbs', 'tv5')
register.RegisterChannel('chn_sbs', 'tv9')

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
        self.moduleName = "chn_sbs.py"
            
        self.language = "se"
        
        if self.channelCode == "tv5":
            self.guid = "C72D24F6-5FAE-11E0-9935-5F41E0D72085"
            self.baseUrl = "http://www.kanal5play.se"
            self.mainListUri = "http://www.kanal5play.se/program"            
            self.icon = "tv5seicon.png"
            self.iconLarge = "tv5selarge.png"
            self.noImage = "tv5seimage.png"
            self.channelName = "Kanal 5"
            self.channelDescription = u'Sändningar från Kanal 5'
            self.sortOrder = 105
            self.episodeItemRegex = '<img [^>]+src="/themes/kanal5[^<]+/>\W+</td>\W+<td>\W+<div[^>]*>\W+<a title="([^"]+)"[^<]+\W+href="(/program/[^"]+)">[\n\t\r ]+([^<]+)</a>'
        
        elif self.channelCode == "tv9":
            self.guid = "CE108D08-5FAE-11E0-B2D0-6141E0D72085"
            self.baseUrl = "http://www.kanal9play.se"
            self.mainListUri = "http://www.kanal9play.se/program"            
            self.icon = "tv9seicon.png"
            self.iconLarge = "tv9selarge.png"
            self.noImage = "tv9seimage.png"
            self.channelName = "Kanal 9"
            self.channelDescription = u'Sändningar från Kanal 9'
            self.sortOrder = 109
            self.episodeItemRegex = '<img [^>]+src="/themes/kanal9[^<]+/>\W+</td>\W+<td>\W+<div[^>]*>\W+<a title="([^"]+)"[^<]+\W+href="(/program/[^"]+)">[\n\t\r ]+([^<]+)</a>'
        
        #self.backgroundImage = ""
        #self.backgroundImage16x9 = ""
        self.requiresLogon = False
        self.swfUrl = "http://admin.brightcove.com/viewer/us20110929.2031/connection/ExternalConnection_2.swf"
        
        self.contextMenuItems = []
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using Mplayer", "CtMnPlayMplayer", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using DVDPlayer", "CtMnPlayDVDPlayer", itemTypes="video", completeStatus=True))        
        
        self.videoItemRegex = '<a href="([^"]+)" title="([^"]+)">\W+<img src="([^"]+)"[^>]+>\W+<span[^/]+</span>\W+<span class="title">\W+<span[^/]+</span>\W+([^<\n]+)\W+<'
        self.folderItemRegex = '<div class="button([^"]+)">([^<]+)<span[^>]*>([^<]+)</span>'
        self.mediaUrlRegex = '<object id="myExperience[\w\W]+?playerKey" value="(?P<playerKey>[^"]+)[\w\W]+?videoPlayer" value="(?P<contentId>\d+)'
        
        """ 
            The ProcessPageNavigation method will parse the current data using the pageNavigationRegex. It will
            create a pageItem using the CreatePageItem method. If no CreatePageItem method is in the channel,
            a default one will be created with the number present in the resultset location specified in the 
            pageNavigationRegexIndex and the url from the combined resultset. If that url does not contain http://
            the self.baseUrl will be added. 
        """
        # remove the &amp; from the url
        self.pageNavigationRegex = ''  
        self.pageNavigationRegexIndex = 1

        #========================================================================== 
        # non standard items

        """
            Testcases:
            Svenska miljon&auml;rer - avsnitt 4 s&auml;song 1 : RTMPE with /&mp4:media
            Stridspiloterna - avsnitt 1 s&auml;song 1 : RTMPE /&:media
        """
        
        return True
    
    #==============================================================================
    def CreateEpisodeItem(self, resultSet):
        """
        Accepts an arraylist of results. It returns an item. 
        """
        urlend = htmlentityhelper.HtmlEntityHelper.ConvertHTMLEntities(resultSet[1])
        urlend = htmlentityhelper.HtmlEntityHelper.UrlEncode(urlend)
        url = urlparse.urljoin(self.baseUrl, urlend)
        
        item = mediaitem.MediaItem(resultSet[2], url)
        item.description = resultSet[0]
        item.thumb = self.noImage
        item.icon = self.icon
        return item
    
    #==============================================================================
    def PreProcessFolderList(self, data):
        """
        Accepts an data from the ProcessFolderList Methode, BEFORE the items are
        processed. Allows setting of parameters (like title etc). No return value!
        """
        logFile.info("Performing Pre-Processing")
        _items = []
        
        # we should check if the text "Fler klipp" of "Fler avsnitt" exists, if so we should add a new folder item for it to the data,        
        # so it gets picked up
        # same goes for adding the Senaste, Mest sedda and Mest gillade
        if len(common.DoRegexFindAll("fler klipp", data)) > 0:
            data = data + '<div class="button moreclips">Fler klipp<span>none</span>'
            
        if len(common.DoRegexFindAll("fler avsnitt", data)) > 0:
            data = data + '<div class="button moreepisodes">Fler avsnitt<span>none</span>'
        
        if len(common.DoRegexFindAll('<div class="[^"]+">Senaste</div>', data)) > 0:
            data = data + '<div class="button latest">Senaste<span>none</span>'
        
        if len(common.DoRegexFindAll('<div class="[^"]+">Mest sedda</div>', data)) > 0:
            data = data + '<div class="button mostviewed">Mest sedda<span>none</span>'
        
        if len(common.DoRegexFindAll('<div class="[^"]+">Mest gillade</div>', data)) > 0:
            data = data + '<div class="button mostliked">Mest gillade<span>none</span>'
                
        #logFile.debug(data)                
        logFile.debug("Pre-Processing finished")
        return (data, _items)
    
    #==============================================================================
    def CreateFolderItem(self, resultSet):
        # <div class="button([^"]+)">([^<]+)<span[^>]+>([^<]+)</span>
        #                0              1                 2
        logFile.debug(resultSet)
        
        name = ""
        url = ""
        
        if resultSet[0] == " " or resultSet[0] == " selected":
            # seasons
            name = "Season %s" % (resultSet[1], )
            # /ajax/videoSelector?sortBy=PUBLISH_DATE&amp;programsHeader=Avsnitt+fr%C3%A5n+s%C3%A4song+6&amp;clipsHeader=Klipp+fr%C3%A5n+s%C3%A4song+6&amp;programTag=100+h%C3%B6jdare&amp;season=6
            # should be:
            # /ajax/videoSelector?sortBy=PUBLISH_DATE&programsHeader=Avsnitt+fr%C3%A5n+s%C3%A4song+5&clipsHeader=Klipp+fr%C3%A5n+s%C3%A4song+5&programTag=100+h%C3%B6jdare&season=5
            urlend = htmlentityhelper.HtmlEntityHelper.ConvertHTMLEntities(resultSet[2])
            url = "%s%s" % (self.baseUrl, urlend)                        
            
        elif resultSet[0] == " moreclips":
            # Fler klipp
            name = "%s" % (resultSet[1], )
            pass
        elif resultSet[0] == " moreepisodes":
            # Fler avsnitt
            name = "%s" % (resultSet[1], )
            pass
        elif resultSet[0] == " latest":
            # Senaste
            name = "%s" % (resultSet[1], )
            pass
        elif resultSet[0] == " mostviewed":
            # Mest sedda    
            name = "%s" % (resultSet[1], )
            pass
        elif resultSet[0] == " mostliked":
            # Mest gillade
            name = "%s" % (resultSet[1], )
            pass
        else:
            return None
        
        item = mediaitem.MediaItem(name, url)        
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
        # <a href="([^"]+)" title="([^"]+)">\W+<img src="([^"]+)"[^>]+>\W+<span[^/]+</span>\W+<span class="title">\W+<span[^/]+</span>\W+([^<]+)\W+<
        #              0               1                    2                                                                                3
        
        url = htmlentityhelper.HtmlEntityHelper.ConvertHTMLEntities(resultSet[0])
        name = resultSet[1]
        
        if ("/klipp/" in url):
            name = "Klipp: %s" % (name,)
            
        description = resultSet[3]
        thumb = resultSet[2]
        
        item = mediaitem.MediaItem(name, "%s%s" %(self.baseUrl, url))
        item.description = description
        item.thumbUrl = thumb
        item.thumb = self.noImage
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
        
        data = uriHandler.Open(item.url, pb=False)
        objectData = common.DoRegexFindAll(self.mediaUrlRegex, data)[0]
        #logFile.debug(objectData)
                
        seed = "9f79dd85c3703b8674de883265d8c9e606360c2e"
        amfHelper = brightcovehelper.BrightCoveHelper(logFile, objectData['playerKey'], objectData['contentId'], item.url, seed)
        item.description = amfHelper.GetDescription()
        
        part = item.CreateNewEmptyMediaPart()
        for stream, bitrate in amfHelper.GetStreamInfo():
            #url = self.GetVerifiableVideoUrl(stream.replace("/&media", "/media").replace("/&mp4:media", "/media"))
            # strip the /mp4: and make sure that the app is only "10549" by making sure it's: /10549//media/ or/10549//mp4:media/ 
            url = self.GetVerifiableVideoUrl(stream.replace("/&", "//"))
            part.AppendMediaStream(url, bitrate)
        
        item.complete = True
        return item    