import sys, string
import xml.dom.minidom
import time

#===============================================================================
# Make global object available
#===============================================================================
import common
import mediaitem
import chn_class
from helpers import mmshelper

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

register.RegisterChannel('chn_rtl')

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
        
        self.guid = "15D92364-42F4-11DD-AF9B-7BFF55D89593"
        self.mainListUri = "http://www.rtl.nl/system/xl/feed/a-z.xml"
        self.baseUrl = "http://www.rtl.nl"
        self.icon = "rtlthumb.png"
        self.iconLarge = "rtllarge.png"
        self.noImage = "rtlimage.png"
        self.channelName = "RTL 4,5&7"
        self.channelDescription = "Uitzendingen van de zenders RTL 4,5,7 & 8."
        self.moduleName = "chn_rtl.py"
        self.language = "nl"
        
        #self.backgroundImage = "background-rtl.png"
        #self.backgroundImage16x9 = "background-rtl-16x9.png"
        self.requiresLogon = False
        self.sortOrder = 5
        
        self.episodeItemRegex = "<abstract key='([^']+)'>\W+<station>([^<]+)</station>\W+<name>([^<]+)</name>"
        self.videoItemRegex = '' 
        self.folderItemRegex = ''
        self.mediaUrlRegex = '<ref href="([^"]+_)(\d+)(K[^"]+.wmv)"[^>]*>'
        
        self.contextMenuItems = []
        #self.contextMenuItems.append(contextmenu.ContextMenuItem("Play lowest bitrate stream", "CtMnPlayLow", itemTypes="video", completeStatus=True))            
        #self.contextMenuItems.append(contextmenu.ContextMenuItem("Play default bitrate stream", "CtMnPlayHigh", itemTypes="video", completeStatus=True))
        
        #============================================================================== 
        # non standard items
        self.PreProcessRegex = '<ul title="([^"]*)" rel="([^"]*)videomenu.xml"'
        self.progTitle = ""
        self.videoMenu = ""
        
        self.seasons = dict()
        self.episodes = dict()
        self.materials = dict()
        #self.parseWvx = True

        return True
        
    #==============================================================================
    def CreateEpisodeItem(self, resultSet):
        """
        Accepts an arraylist of results. It returns an item. 
        """
        # http://www.rtl.nl/system/s4m/xldata/abstract/218927.xml
        item = mediaitem.MediaItem(resultSet[2], "http://www.rtl.nl/system/s4m/xldata/abstract/%s.xml" % (resultSet[0]))
        
        channel = resultSet[1].lower()
        
        if channel in ("rtl4", "rtl5", "rtl7", "rtl8"):
            logo = "%sicon.png" % (channel,)
            fullLogoPath = self.GetImageLocation(logo)
            item.icon = fullLogoPath
        else:
            item.icon = self.folderIcon
        return item
    
    #==============================================================================
    def PreProcessFolderList(self, data):
        """
        Accepts an data from the ProcessFolderList Methode, BEFORE the items are
        processed. Allows setting of parameters (like title etc). No return value!
        """
        items = []
        
        # process the XML file in items and return an empty data string        
        dom = xml.dom.minidom.parseString(data)
        for abstract in dom.getElementsByTagName("abstract"):
            programName = self.GetXmlTextForNode(abstract, "name")
        logFile.debug("Processing: %s", programName)
        
        # Do not just set the name, add the items, basically we already determine al the items 
        # that are available and already parse them here.
        
        for season in dom.getElementsByTagName("season"):
            name = self.GetXmlTextForNode(season, "name")
            key = season.getAttribute('key')
            
            folderItem = mediaitem.MediaItem(name, "", parent=self)
            folderItem.complete = True
            folderItem.thumb = self.noImage
            folderItem.icon = self.folderIcon
            
            self.seasons[key] = folderItem
            items.append(folderItem)
            logFile.debug("Adding: %s", folderItem)
        
        for episode in dom.getElementsByTagName("episode"):
            number = self.GetXmlTextForNode(episode, "item_number")
            name = self.GetXmlTextForNode(episode, "name")
            synopsis = self.GetXmlTextForNode(episode, "synopsis")
            seasonKey = episode.getAttribute('season_key')
            key = episode.getAttribute('key')
            season = episode.getAttribute('season_key')
            
            if name == None:
                name = "Aflevering #%s" % (number,)
            
            # create the episode
            seasonItem = self.seasons[season]
            episodeItem = mediaitem.MediaItem(name, "", parent=seasonItem)
            episodeItem.description = synopsis
            episodeItem.complete = True;
            episodeItem.thumb = self.noImage
            episodeItem.icon = self.folderIcon
            
            # now add them
            seasonItem.items.append(episodeItem)
            self.episodes[key] = episodeItem
            
        for material in dom.getElementsByTagName("material"):
            drm = self.GetXmlTextForNode(material, "audience")
            date = self.GetXmlTextForNode(material, "broadcast_date_display")
            url = self.GetXmlTextForNode(material, "component_uri")
            title = self.GetXmlTextForNode(material, "title")
            if title is None or title == "":
                continue
            
            thumbId = self.GetXmlTextForNode(material, "thumbnail_id")
            thumbUrl = "http://data.rtl.nl/system/img/71v0o4xqq2yihq1tc3gc23c2w/%s" % (thumbId, )
            #seasonKey = material.getAttribute('season_key')
            episodeKey = material.getAttribute('episode_key')
            
            if episodeKey == "" or episodeKey == u'':
                logFile.error("Error matching RTL video: %s, %s", url, seasonKey) 
                continue

            episodeItem = self.episodes[episodeKey]

            if drm.lower() == "drm":
                title = "[DRM] "+ title
 
            url = "http://www.rtl.nl/system/video/wvx" + url + "/1500.wvx?utf8=ok" #or 600.wvx?utf8=ok
            item = mediaitem.MediaItem(title, url, parent=episodeItem)
            description = episodeItem.description
            item.thumbUrl = thumbUrl
            item.thumb = self.noImage
            item.type = "video"
            item.icon = self.icon
            
            dates = None
            if not date=="":                
                dates = time.localtime(float(date))
                item.SetDate(dates[0], dates[1], dates[2])
            episodeItem.items.append(item)
            
            # now we set the dates for the parents
            if dates:
                episodeItem.SetDate(dates[0], dates[1], dates[2], onlyIfNewer=True)
                episodeItem.parent.SetDate(dates[0], dates[1], dates[2], onlyIfNewer=True)
            
        # now sort them
        items.sort()
        for item in items:
            item.items.sort()
            for subitem in item.items:
                subitem.items.sort()
        return (data, items)
    
    #============================================================================= 
    def UpdateVideoItem(self, item):
        """
        Accepts an item. It returns an updated item. 
        """
        logFile.debug('starting UpdateVideoItem for %s (%s)', item.name, self.channelName)
        
        if not item.HasMediaItemParts():
            highResUrl = item.url
            lowResUrl = string.replace(item.url, "1500.wvx", "600.wvx")
            
            data = uriHandler.Open(highResUrl, pb=False, proxy=self.proxy)
            data = data + uriHandler.Open(lowResUrl, pb=False, proxy=self.proxy)
            
            matches = common.DoRegexFindAll(self.mediaUrlRegex, data)
            logFile.debug("Possible Matches for mediaUrl: %s", matches)
    
            if len(matches) > 0:        
                # sort mediaurl -> get highest quality
                #matches.sort(lambda x, y: int(y[1]) - int(x[1]))
                #part = mediaitem.MediaItemPart(item.name)
                part = item.CreateNewEmptyMediaPart()    
                for match in matches:
                    part.AppendMediaStream("%s%s%s" % match, bitrate=match[1])
            else:
                logFile.error("Cannot find media URL")
        
        # now we should try to parse them using the MMS helper
        for mediaItem in item.MediaItemParts:
            for stream in mediaItem.MediaStreams:
                stream.Url = mmshelper.MmsHelper.GetMmsFromHtml(stream.Url)            
                
        if item.thumbUrl != "":
            item.thumb = self.CacheThumb(item.thumbUrl)
        item.complete = True
        
        logFile.info('finishing UpdateVideoItem: %s.', item)
        return item
    
    #============================================================================== 
    def GetXmlTextForNode(self, node, nodeName):
        elements = node.getElementsByTagName(nodeName)
        if len(elements) == 0:
            return ""
        
        element = elements[0]
        for childNode in element.childNodes:
                if childNode.nodeType == childNode.TEXT_NODE:
                    return childNode.data    