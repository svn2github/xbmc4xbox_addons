# coding:Cp1252
#===============================================================================
# Import the default modules
#===============================================================================
import sys

#===============================================================================
# Make global object available
#===============================================================================
import common
import mediaitem
import contextmenu
import chn_class

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

register.RegisterChannel('chn_canvas', 'canvas')

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
        
        self.guid = "DA1992AE-B600-11E0-AC62-B3D74824019B"
        self.icon = "canvasicon.png"
        self.iconLarge = "canvaslarge.png"
        self.noImage = "canvasimage.png"
        self.channelName = "Canvas"
        self.channelDescription = "Online uitzendingen van www.canvas.be."
        self.sortOrder = 121
        self.mainListUri = "http://video.canvas.be/"
        self.baseUrl = "http://www.canvas.be"
        self.swfUrl = "http://video.canvas.be/common2/all/swf/jw-flv-player/4.3.patched/player.swf"
        
        self.episodeItemRegex = '<li>\W*<a href="([^"]+)"[^>]+>([^<]+)</a></li>' # used for the ParseMainList
        self.videoItemRegex = '<div class="videoitem">[\W\w]+?<img id="rating_[^>]+ratings_off\((\d+.\d+|\d+)[\W\w]+?<div style="background-image: url\(([^)]+)\)[\w\W]+?<p class="itemdesc">\W+<a href="([^"]+)" title="([^"]+)"\W+([^<]+)</a>'
        self.mediaUrlRegex = 'file\W*"([^"]+)"\W+streamer\W+"([^"]*?)(?:/)*"' 
        self.pageNavigationRegex = "<a href='([^']+/page/)(\d+)'" 
        self.pageNavigationRegexIndex = 1
            
        self.moduleName = "chn_canvas.py"            
        self.language = "be"
        
        self.contextMenuItems = []
#        self.contextMenuItems.append(contextmenu.ContextMenuItem("Update Item", "CtMnUpdateItem", itemTypes="video", completeStatus=None))            
#        self.contextMenuItems.append(contextmenu.ContextMenuItem("Download Item", "CtMnDownloadItem", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using Mplayer", "CtMnPlayMplayer", itemTypes="video", completeStatus=True))
        self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using DVDPlayer", "CtMnPlayDVDPlayer", itemTypes="video", completeStatus=True))        
        return True
      
    def CreateEpisodeItem(self, resultSet):
        """
        Accepts an arraylist of results. It returns an item. 
        """
        #logFile.debug('starting CreateEpisodeItem for %s', self.channelName)
        
        # dummy class
        item = mediaitem.MediaItem(resultSet[1], resultSet[0])
        item.icon = self.icon
        item.type = "folder"
        item.complete = True
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
        
        rating = int(round(float(resultSet[0])))
        thumbUrl = resultSet[1]
        url = resultSet[2]        
        title = resultSet[3]
        description = "%s..." % (resultSet[4].strip(),)
        
        item = mediaitem.MediaItem(title, url)        
        item.thumbUrl = thumbUrl
        item.thumb = self.noImage
        item.icon = self.icon
        item.description = description
        item.rating = rating
        
        #item.SetDate(2000+int(resultSet[2]), resultSet[3], resultSet[4])            
        item.type = 'video'
        item.complete = False
        return item
    
    #============================================================================= 
    def UpdateVideoItem(self, item):
        """
        Accepts an item. It returns an updated item. Usually retrieves the MediaURL 
        and the Thumb! It should return a completed item. 
        """
        logFile.info('starting UpdateVideoItem for %s', item)
        
        # rtmpt://vrt.flash.streampower.be/een//2011/07/1000_110723_getipt_neefs_wiels_Website_EEN.flv
        # http://www.een.be/sites/een.be/modules/custom/vrt_video/player/player_4.3.swf
        
        item.thumb = self.CacheThumb(item.thumbUrl)        
        
        # now the mediaurl is derived. First we try WMV
        data = uriHandler.Open(item.url, pb=False)
        
        descriptions = common.DoRegexFindAll('<div class="teaserInfo">(?:[\W\w])*?<p><a[^>]+>([^<]+)</a>', data)
        for desc in descriptions:
            item.description = desc
            
        urls = common.DoRegexFindAll(self.mediaUrlRegex, data)
        for url in urls:
            mediaurl = "%s//%s" % (url[1],url[0])  # the extra slash in the url causes the application name in the RTMP stream to be "een" instead of "een/2011"
            mediaurl = self.GetVerifiableVideoUrl(mediaurl)
        
        if mediaurl != "":
            item.AppendSingleStream(mediaurl)
            item.complete = True
            #logFile.debug("Media url was found: %s", item)            
        else:
            logFile.debug("Media url was not found.")

        return item    
