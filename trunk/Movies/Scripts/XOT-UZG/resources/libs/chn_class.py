#==============================================================================
# LICENSE XOT-Framework - CC BY-NC-ND
#===============================================================================
# This work is licenced under the Creative Commons 
# Attribution-Non-Commercial-No Derivative Works 3.0 Unported License. To view a 
# copy of this licence, visit http://creativecommons.org/licenses/by-nc-nd/3.0/ 
# or send a letter to Creative Commons, 171 Second Street, Suite 300, 
# San Francisco, California 94105, USA.
#===============================================================================

#===============================================================================
# Import the default modules
#===============================================================================
import urlparse
import sys
import os
import time

import xbmc
import xbmcgui 

import common
import mediaitem

import settings
import guicontroller
from config import Config
from envcontroller import Environments
from helpers import htmlentityhelper
from helpers import stopwatch
from helpers import encodinghelper

#===============================================================================
# Make global object available
#===============================================================================
logFile = sys.modules['__main__'].globalLogFile
uriHandler = sys.modules['__main__'].globalUriHandler

#===============================================================================
# register the channels
#===============================================================================
# register = sys.modules['progwindow']
# register.channelRegister.append('chn_rtl.Channel()')

#===============================================================================
# main Channel Class
#===============================================================================
class Channel:
    """
    main class from which all channels inherit
    """
    
    #============================================================================== 
    def __init__(self, *args, **kwargs):
        """Initialisation of the class. 
        
        WindowXMLDialog(self, xmlFilename, scriptPath[, defaultSkin, defaultRes]) -- Create a new WindowXMLDialog script.
    
        xmlFilename     : string - the name of the xml file to look for.
        scriptPath      : string - path to script. used to fallback to if the xml doesn't exist in the current skin. (eg os.getcwd())
        defaultSkin     : [opt] string - name of the folder in the skins path to look in for the xml. (default='Default')
        defaultRes      : [opt] string - default skins resolution. (default='720p')
        
        *Note, skin folder structure is eg(resources/skins/Default/720p)
        
        All class variables should be instantiated here and this method should not 
        be overridden by any derived classes.
        
        """
        
        self.mainListItems = []
        self.parentItem = None
        
        # set default icons
        self.folderIcon = "xot_DefaultFolder.png"
        self.folderIconHQ = "xot_DefaultFolderHQ.png"
        self.appendIcon = "xot_DefaultAppend.png"
        
        # detect the channelcode
        if kwargs.has_key("channelCode"):
            self.channelCode = kwargs["channelCode"]
            #logFile.debug("ChannelCode present: %s", self.channelCode)
        else:
            self.channelCode = ""
            #logFile.debug("No channelCode present")
        
        self.initialItem = None #uri that is used for the episodeList. NOT mainListUri
        self.proxy = None
        self.loggedOn = False
        
        # initialise user defined variables
        self.InitialiseVariables()
        
        # update image file names: point to local folder if not present in skin
        self.icon = self.GetImageLocation(self.icon)
        self.iconLarge = self.GetImageLocation(self.iconLarge)
        self.folderIcon = self.GetImageLocation(self.folderIcon)
        self.folderIconHQ = self.GetImageLocation(self.folderIconHQ)
        self.appendIcon = self.GetImageLocation(self.appendIcon)
        self.noImage = self.GetImageLocation(self.noImage)
        self.backgroundImage = self.GetImageLocation(self.backgroundImage)
        self.backgroundImage16x9 = self.GetImageLocation(self.backgroundImage16x9)
        
        # plugin stuff
        self.pluginMode = False        
        #logFile.debug("Initialized: %s", self)
                
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
        
        #logFile.debug("Starting IntialiseVariables from chn_class.py")
        
        self.guid = "00000000-0000-0000-0000-000000000000"
        self.icon = ""
        self.iconLarge = ""
        self.noImage = ""
        self.backgroundImage = ""  # if not specified, the one defined in the skin is used
        self.backgroundImage16x9 = ""  # if not specified, the one defined in the skin is used
        self.channelName = "Channel Class"
        self.channelDescription = "This is the channelclass on which all channels are based"
        self.moduleName = "chn_class.py"
        self.compatiblePlatforms = Environments.Linux | Environments.OSX | Environments.Windows | Environments.Xbox | Environments.ATV2 | Environments.IOS
        
        self.sortOrder = 255 #max 255 channels
        self.buttonID = 0
        self.onUpDownUpdateEnabled = True
        self.contextMenuItems = []
        self.language = None
        
        self.mainListUri = ""
        self.baseUrl = ""
        self.playerUrl = ""
        self.defaultPlayer = 'defaultplayer' #(defaultplayer, dvdplayer, mplayer)
        
        self.passWord = ""
        self.userName = ""
        self.logonUrl = ""
        self.requiresLogon = False
        
        self.asxAsfRegex = '<[^\s]*REF href[^"]+"([^"]+)"' # default regex for parsing ASX/ASF files
        
        self.episodeItemRegex = '' # used for the ParseMainList
        self.videoItemRegex = ''   # used for the CreateVideoItem 
        self.folderItemRegex = ''  # used for the CreateFolderItem
        self.mediaUrlRegex = ''    # used for the UpdateVideoItem
        
        """ 
            The ProcessPageNavigation method will parse the current data using the pageNavigationRegex. It will
            create a pageItem using the CreatePageItem method. If no CreatePageItem method is in the channel,
            a default one will be created with the number present in the resultset location specified in the 
            pageNavigationRegexIndex and the url from the combined resultset. If that url does not contain http://
            the self.baseUrl will be added. 
        """
        self.pageNavigationIndicationRegex = '' 
        self.pageNavigationRegex = '' 
        self.pageNavigationRegexIndex = 0 
       
        self.episodeSort = True
        self.swfUrl = ""
        
        #========================================================================== 
        # non standard items
        
        return True

    #===============================================================================
    #    Init for plugin and script
    #===============================================================================
    def InitPlugin(self):
        """Initializes the channel for plugin use
        
        Returns:
        List of MediaItems that should be displayed
        
        This method is called for each Plugin call and can be used to do some 
        channel initialisation. Make sure to set the self.pluginMode = True
        in this methode if overridden.
        
        """
        
        self.pluginMode = True
        
        self.loggedOn = self.LogOn(self.userName, self.passWord)
    
        if not self.loggedOn:
            logFile.error('Not logged on...exiting')
            return False
        
        # set HQ icons
        self.icon = self.iconLarge
        self.folderIcon = self.folderIconHQ
        
        return self.InitEpisodeList()
    
    #============================================================================== 
    def InitScript(self):
        """Initializes the channel for script use
        
        Returns: 
        The value of self.InitEpisodeList()
        
        """
        
        logFile.debug("LogonCheck")
        
        self.pluginMode = False
        
        self.loggedOn = self.LogOn(self.userName, self.passWord)
    
        if not self.loggedOn:
            logFile.error('Not logged on...exiting')
            return False
        
        return self.InitEpisodeList() 
    
    def InitEpisodeList(self):
        """Init method that can be used to do stuff when the channel opens a new episode list
        
        Returns:
        True if the method completed without errors
        
        """
        return True
    
    #==============================================================================
    # ContextMenu functions
    #==============================================================================
    def CtMnAddToFavorites(self, item):
        """Add to favorites.
        
        Arguments:
        item : MediaItem - the item to add to the favorites.
        
        """
        
        if item.type != 'folder':
            logFile.error("AddToFavorites :: Can only add folder items. Got %s-item", item.type)
            return 
        
        settings.AddToFavorites(item, self)        
        return      
    
    def CtMnSettings(self, item):
        """Shows the Addon settings
        
        Arguments: 
        item : MediaItem - the currently selected item
        
        The <item> argument is not really used here, but is just here for compatibility
        in showing the contextmenu.
        
        """
        
        settings.AddonSettings().ShowSettings()
        pass
    
    def CtMnRefresh(self, item):
        return self.UpdateVideoItem(item)
        pass
    
    #==============================================================================
    # Custom Methodes, in chronological order   
    #==============================================================================
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

        items = []
        if len(self.mainListItems) > 1:
            if self.episodeSort:
                # just resort again
                self.mainListItems.sort()
            
            if returnData:
                return (self.mainListItems, "")
            else:
                return self.mainListItems
            
        data = uriHandler.Open(self.mainListUri, proxy=self.proxy)
        
        # first process folder items.
        episodeItems = common.DoRegexFindAll(self.episodeItemRegex, data)
        for _episode in episodeItems:
            tmpItem = self.CreateEpisodeItem(_episode)
            # catch the return of None
            if tmpItem and items.count(tmpItem) == 0:
                items.append(tmpItem)
        
        # sort by name
        if self.episodeSort:
            watch = stopwatch.StopWatch('Sort Timer', logFile)                
            items.sort() #lambda x, y: cmp(x.name.lower(), y.name.lower()))
            watch.Stop()
                
        self.mainListItems = items
        
        if returnData:
            return (items, data)
        else:
            return items
    
    #==============================================================================
    def SearchSite(self, url=None):
        """Creates an list of items by searching the site
        
        Keyword Arguments:
        url : String - Url to use to search with a %s for the search parameters
        
        Returns:
        A list of MediaItems that should be displayed.
        
        This method is called when the URL of an item is "searchSite". The channel
        calling this should implement the search functionality. This could also include
        showing of an input keyboard and following actions. 
        
        The %s the url will be replaced with an URL encoded representation of the 
        text to search for. 
        
        """
        
        items = []
        if url is None:
            item = mediaitem.MediaItem("Search Not Implented", "", type='video')
            item.icon = self.icon
            items.append(item)
        else:
            items = []        
            keyboard = xbmc.Keyboard('')
            keyboard.doModal()
            if (keyboard.isConfirmed()):
                needle = keyboard.getText()
                logFile.debug("Searching for '%s'", needle)
                if len(needle)>0:
                    #convert to HTML
                    needle = htmlentityhelper.HtmlEntityHelper.UrlEncode(needle)
                    searchUrl = url % (needle)
                    temp = mediaitem.MediaItem("Search", searchUrl)
                    return self.ProcessFolderList(temp)
        
        return items
    
    #==============================================================================
    def SetRootItem(self, item):
        """Sets the intialItem that is used to fill the channel. 
        
        Arguments:
        item : MediaItem - the item to set as the initial item.
        
        The <item> is used to load the URL and then process the first folder list
        to display. 
        
        """ 
        
        self.initialItem = item
        return 
    
    #==============================================================================
    def GetRootItem(self):
        """returns the first item for the selected program
        
        Returns:
        The root MediaItem of the channel.
        
        This methode returns the set self.intialItem and returns that item
        to the caller. 
        
        """
        
        # the root item
        rootItem = self.initialItem
        
        # get the image
        if self.initialItem.thumb == "":
            if self.initialItem.thumbUrl == "":
                rootItem.thumb = self.noImage
            else:
                rootItem.thumb = self.CacheThumb(self.initialItem.thumbUrl)
        
        # get the items
        rootItem.items = self.ProcessFolderList(rootItem)
        return rootItem
                
    #==============================================================================
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
        
        logFile.debug('starting CreateEpisodeItem for %s', self.channelName)
        
        # dummy class
        item = mediaitem.MediaItem("No CreateEpisode Implented!", "")
        item.complete = True
        return item
    
    #==============================================================================
    def PreProcessFolderList(self, data):
        """Performs pre-process actions for data processing/
        
        Arguments:
        data : string - the retrieve data that was loaded for the current item and URL. 
        
        Returns:
        A tuple of the data and a list of MediaItems that were generated.  
        
        
        Accepts an data from the ProcessFolderList method, BEFORE the items are
        processed. Allows setting of parameters (like title etc) for the channel. 
        Inside this method the <data> could be changed and additional items can 
        be created. 
        
        The return values should always be instantiated in at least ("", []).        
        
        """
        
        logFile.info("Performing Pre-Processing")
        items = []
        logFile.debug("Pre-Processing finished")
        return (data, items)
          
    #==============================================================================
    def ProcessFolderList(self, item=None):
        """Process the selected item and get's it's child items.
        
        Arguments:
        item : [opt] MediaItem - the selected item 
        
        Returns:
        A list of MediaItems that form the childeren of the <item>.
        
        Accepts an <item> and returns a list of MediaListems with at least name & url 
        set. The following actions are done:
        
        * loading of the data from the item.url
        * perform pre-processing actions
        * creates a sorted list folder items using self.folderItemRegex and self.CreateFolderItem
        * creates a sorted list of media items using self.videoItemRegex and self.CreateVideoItem
        * create page items using self.ProcessPageNavigation
        
        if item = None then an empty list is returned.
        
        """
        
        if item == None:
            logFile.debug("ProcessFolderList :: No item was specified. Returning an empty list")            
            return []
        
        if len(item.items) > 0 and not item.url == "searchSite":
            logFile.debug("ProcessFolderList :: %s Items already available. returning them.", len(item.items))
            return item.items
        
        self.parentItem = item
       
        try:
            sortWatch = stopwatch.StopWatch("ProcessFolderList", logFile)                
            preItems = []
            folderItems = []
            videoItems = []
            pageItems = []
            
            if (item.url == "searchSite"):
                logFile.debug("Starting to search")
                return self.SearchSite()
            
            data = uriHandler.Open(item.url, proxy=self.proxy)
            
            # first of all do the Pre handler
            (data, preItems) = self.PreProcessFolderList(data)
            
            # then process folder items.
            if not self.folderItemRegex == '':
                folders = common.DoRegexFindAll(self.folderItemRegex, data)
                for folder in folders:
                    fItem = self.CreateFolderItem(folder)
                    if not fItem == None:
                        folderItems.append(fItem)
                
            # sort by name
            sortWatch.Lap("Folders Loaded")
            folderItems.sort()#lambda x, y: cmp(x.name.lower(), y.name.lower()))
            sortWatch.Lap("Folders Sorted")            
            
            # now process video items
            if not self.videoItemRegex == '':
                videos = common.DoRegexFindAll(self.videoItemRegex, data)
                for video in videos:
                    vItem = self.CreateVideoItem(video)
                    if not vItem == None:
                        videoItems.append(vItem)
                sortWatch.Lap("Video's Loaded")
                videoItems.sort()
                sortWatch.Lap("Video's Sorted")
            
            # now process page navigation if a pageNavigationIndication is present
            if not self.pageNavigationRegex == '':
                pageItems = self.ProcessPageNavigation(data)
    
            return preItems + folderItems + videoItems + pageItems
        except:
            logFile.critical("Error processing folder", exc_info=True)
            return []
        
    #============================================================================== 
    def ProcessPageNavigation(self, data):
        """Generates a list of pageNavigation items. 
        
        Arguments:
        data : string - the retrieve data that was loaded for the current item and URL. 
        
        Returns:
        A list of MediaItems of type 'page'
        
        Parses the <data> using the self.pageNavigationRegex and then calls the 
        self.CreatePageItem method for each result to create a page item. The 
        list of those items is returned. 
        
        """
        
        logFile.debug("Starting ProcessPageNavigation")
        
        pageItems = []
          
        # try the regex on the current data
        pages = common.DoRegexFindAll(self.pageNavigationRegex, data)
        if len(pages) == 0:
            logFile.debug("No pages found.")
            return pageItems
        
        pages = common.DoRegexFindAll(self.pageNavigationRegex, data)
        
        for page in pages:
            item = self.CreatePageItem(page)
            if item:
                pageItems.append(item)
        
        # filter double items
        for item in pageItems:
            if pageItems.count(item) > 1:
                logFile.debug("Removing duplicate for '%s'", item.name)
                pageItems.remove(item)
        
        #logFile.debug(pageItems)
        return pageItems
    
    #==============================================================================
    def CreatePageItem(self, resultSet):
        """Creates a MediaItem of type 'page' using the resultSet from the regex.
        
        Arguments:
        resultSet : tuple(string) - the resultSet of the self.pageNavigationRegex
        
        Returns:
        A new MediaItem of type 'page'
        
        This method creates a new MediaItem from the Regular Expression 
        results <resultSet>. The method should be implemented by derived classes 
        and are specific to the channel.
         
        """
        
        logFile.debug("Starting CreatePageItem")
        total = ''
        
        for result in resultSet:
            total = "%s%s" % (total, result)
        
        total = htmlentityhelper.HtmlEntityHelper.StripAmp(total)
        
        if not self.pageNavigationRegexIndex == '':
            item = mediaitem.MediaItem(resultSet[self.pageNavigationRegexIndex], urlparse.urljoin(self.baseUrl, total))
        else:
            item = mediaitem.MediaItem("0", "")            
        
        item.type = "page"
        logFile.debug("Created '%s' for url %s", item.name, item.url)
        return item 
        
    #==============================================================================
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
        
        logFile.debug('starting CreateFolderItem for %s', self.channelName)
        
        item = mediaitem.MediaItem("No CreateFolderItem Implented!", "")
        item.complete = True
        return item
    
    #============================================================================= 
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

        logFile.debug('starting CreateVideoItem for %s', self.channelName)
        
        item = mediaitem.MediaItem("No CreateVideoItem Implented!", "")
        item.thumb = self.noImage
        item.icon = self.icon
        item.complete = True
        return item
    
    #============================================================================= 
    def UpdateVideoItem(self, item):
        """Updates an existing MediaItem with more data.
        
        Arguments:
        item : MediaItem - the MediaItem that needs to be updated
        
        Returns:
        The original item with more data added to it's properties.
        
        Used to update none complete MediaItems (self.complete = False). This
        could include opening the item's URL to fetch more data and then process that 
        data or retrieve it's real media-URL. 
        
        The method should at least:
        * cache the thumbnail to disk (use self.noImage if no thumb is available).
        * set at least one MediaItemPart with a single MediaStream.
        * set self.complete = True.
        
        if the returned item does not have a MediaItemPart then the self.complete flag 
        will automatically be set back to False.
        
        """

        logFile.info('starting UpdateVideoItem for %s (%s)', item.name, self.channelName)
        
        _data = uriHandler.Open(item.url, pb=False, proxy=self.proxy)

        url = common.DoRegexFindAll(self.mediaUrlRegex, _data)[-1]
        part = mediaitem.MediaItemPart(item.name, url)
        item.MediaItemParts.append(part)
        
        logFile.info('finishing UpdateVideoItem. MediaItems are %s', item)
        
        item.thumb = self.noImage
        if not item.HasMediaItemParts():
            item.SetErrorState("Update did not result in streams")
        else:
            item.complete = True
        return item
    
    #==============================================================================
    def DownloadVideoItem(self, item):
        """Downloads an existing MediaItem with more data.
        
        Arguments:
        item : MediaItem - the MediaItem that should be downloaded.
        
        Returns:
        The original item with more data added to it's properties.
        
        Used to download an <item>. If the item is not complete, the self.UpdateVideoItem
        method is called to update the item. The method downloads only the MediaStream 
        with the bitrate that was set in the addon settings.
        
        After downloading the self.downloaded property is set.
        
        """
        
        if not item.IsPlayable():
            logFile.error("Cannot download a folder item.")
            return item
        
        if item.IsPlayable():
            if item.complete == False:
                logFile.info("Fetching MediaUrl for PlayableItem[%s]", item.type)
                item = self.UpdateVideoItem(item)
    
            if item.complete == False or not item.HasMediaItemParts():
                item.SetErrorState("Update did not result in streams")
                logFile.error("Cannot download incomplete item or item without MediaItemParts")
                return item
            
            i = 1
            bitrate = self.GetSettingsQuality()
            for mediaItemPart in item.MediaItemParts:
                logFile.debug("Trying to download %s", mediaItemPart)
                stream = mediaItemPart.GetMediaStreamForBitrate(bitrate)            
                downloadUrl = stream.Url 
                if downloadUrl.find(".divx") > 0:
                    saveFileName = "%s-Part_%s.divx" % (item.name, i)
                elif downloadUrl.find(".flv") > 0:
                    saveFileName = "%s-Part_%s.flv" % (item.name, i)
                elif downloadUrl.find(".avi") > 0:
                    saveFileName = "%s-Part_%s.avi" % (item.name, i)
                else:
                    saveFileName = "%s-Part_%s" % (item.name, i)                    
                logFile.debug(saveFileName)
                
                agent = mediaItemPart.UserAgent                     
                uriHandler.Download(downloadUrl, saveFileName, userAgent=agent)
                i = i + 1
            
            item.downloaded = True               
        
        return item
    #============================================================================== 
    def LogOn(self, *args):
        """Logs on to a website, using an url. 
        
        Arguments:
        userName : string - the username to use to log on
        passWord : string - the password to use to log on
        
        Returns:
        True if successful.
        
        First checks if the channel requires log on. If so and it's not already
        logged on, it should handle the log on. That part should be implemented
        by the specific channel. 
        
        More arguments can be passed on, but must be handled by custom code.
        
        After a successful log on the self.loggedOn property is set to True and
        True is returned. 
        
        """
        
        if not self.requiresLogon:
            logFile.info("No login required of %s", self.channelName)
            return True
        
        if self.loggedOn:
            logFile.info("Already logged in")
            return True
        
        _rtrn = False
        _passWord = args["userName"]
        _userName = args["passWord"]
        return _rtrn
    
    #============================================================================== 
    def PlayVideoItem(self, item, player="", bitrate=None):
        """Starts the playback of the <item> with the specific <bitrate> in the selected <player>.  

        Arguments:
        item    : MediaItem - The item to start playing
        
        Keyword Arguments:
        player  : [opt] string - The requested player ('dvdplayer', 'mplayer' or '' for the default one)
        bitrate : [opt] integer - The requested bitrate in Kbps or None.

        Returns:
        The updated <item>.

        Starts the playback of the selected MediaItem <item>. Before playback is started
        the item is check for completion (item.complete), if not completed, the self.UpdateVideoItem
        method is called to update the item.  
        
        After updating the requested bitrate playlist is selected, if bitrate was set to None
        the bitrate is retrieved from the addon settings. The playlist is then played using the
        requested player.        
         
        """
        
        try:
            playList = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
            playList.clear()
            
            
            if player == "":
                player = self.defaultPlayer
            
            if bitrate == None:
                # use the bitrate from the xbmc settings if bitrate was not specified and the item is MultiBitrate
                bitrate = self.GetSettingsQuality()
            
            # should we download items?
            logFile.debug("Checking for not streamable parts")
            for part in item.MediaItemParts:
                if not part.CanStream:
                    stream = part.GetMediaStreamForBitrate(bitrate)
                    if not stream.Downloaded:
                        logFile.debug("Downloading not streamable part: %s\nDownloading Stream: %s", part, stream)
                        fileName = stream.Url[stream.Url.rfind("/") + 1:]
                        folder = uriHandler.Download(stream.Url, fileName, Config.cacheDir, proxy=self.proxy, userAgent=part.UserAgent)
                        if folder == "":
                            logFile.error("Cannot download stream %s \nFrom: %s", stream, part)
                            return
                        stream.Url = folder
                        stream.Downloaded = True
                                                
            item.downloaded = True
            
            # now we can play
            logFile.info("Starting Video Playback using the %s", player)
              
            # get the playlist
            (playList, srt) = item.GetXBMCPlayList(bitrate)
            
            # determine the player
            if player == "dvdplayer":
                logFile.info("Playing using DVDPlayer")
                xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER)
            elif player == "mplayer":
                logFile.info("Playing using Mplayer")
                xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_MPLAYER)
            else:
                logFile.info("Playing using default player")
                xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
            
            # and play
            xbmcPlayer.play(playList)
            
            # any subtitles availabe
            showSubs = settings.AddonSettings().UseSubtitle()
            if (not srt is None) and (srt != ""):
                if showSubs:
                    logFile.info("Adding subtitle: %s", srt)
                    time.sleep(2)
                    xbmcPlayer.setSubtitles(srt)
                else:
                    logFile.info("Subtitle disabled in settings. Not adding.")                    
            
        except:
            dialog = xbmcgui.Dialog()
            dialog.ok(Config.appName, "Cannot start playback.")
            logFile.critical("Could not playback the url", exc_info=True)
    
    #==============================================================================
    def GetVerifiableVideoUrl(self, url):
        """Creates an RTMP(E) url that can be verified using an SWF URL. 
        
        Arguments:
        url : string - the URL that should be made verifiable.
        
        Returns:
        A new URL that includes the self.swfUrl in the form of "url --swfVfy|-W swfUrl". 
        If self.swfUrl == "", the original URL is returned.
        
        """
        
        if self.swfUrl == "":
            return url
        
        #return "%s --swfVfy -W %s" % (url, self.swfUrl)
        return "%s swfurl=%s swfvfy=true" % (url, self.swfUrl)
        
    #============================================================================== 
    def GetImageLocation(self, image):
        """returns the path for a specific image name.
        
        Arguments:
        image : string - the filename of the requested argument.
        
        Returns:
        The full local path to the requested image.
        
        Calls the guiController.GetImageLocation to get the path.
        
        """
        
        return guicontroller.GuiController.GetImageLocation(image, self)
    
    #============================================================================== 
    def GetSettingsQuality(self):
        """Gets the prefered playback quality from the Addon settings.
        
        Returns:
        Integer indicating the quality of playback that is configured:
        * 0 -- low quality
        * 1 -- medium quality
        * 2 -- high quality 
        
        This could also be done directly using the settings.AddonSettings() but 
        it's here for convenience.
        
        """
        
        return settings.AddonSettings().GetMaxStreamBitrate()
        
    #===============================================================================
    def GetBackgroundImage(self, resolution43=True):
        """Returns the background image for this channel for the requested screensize.
        
        Keyword Arguments:
        resolution43 : boolean - Indicates whether to return the 4x3 background or not (16x9).
        
        Returns:
        The path to the requested background, or an empty string if the channel does not
        have a background configured.
        
        The path also takes into consideration that a possible image is available in the
        XBMC sckin folder. Therefore it uses the GetImageLocation methode in the 
        chn_class.__init__() methode.
          
        """
        
        
        if resolution43:
            background = self.backgroundImage
        else:
            background = self.backgroundImage16x9
        
        if (background == ""):
            background = settings.AddonSettings().BackgroundImageProgram()
        
        return background
    
    #===============================================================================
    def CacheThumb(self, remoteImage):
        """Caches an image to disk.
        
        Arguments:
        remoteImage : string - the URL of the remote thumb.
        
        Returns:
        The local path of the cached image. If not remote image was specified
        it will return the path of the self.noImage image file. Therefore 
        it uses the GetImageLocation methode in the chn_class.__init__() methode. 
        
        In order to make everything appear OK while loading. Set the default thumb
        in the MediaItems to self.noImage file.
        
        """
        
        logFile.debug("Going to cache %s", remoteImage)
        
        if self.pluginMode:
            logFile.debug("For plugin-mode we do not cache thumbs, that's XBMC's work.")
            return remoteImage
            
        if remoteImage == "":
            return self.noImage
        
        if remoteImage.find(":") < 2:
            return remoteImage
        
        logFile.debug("Caching url=%s", remoteImage)
        thumb = ""
        
        # get image
        localImageName = encodinghelper.EncodingHelper.EncodeMD5(remoteImage)
        #localImageName = common.DoRegexFindAll('/([^/]*)$', remoteImage)[-1]
        # correct for fatx
        localImageName = uriHandler.CorrectFileName(localImageName)
        
        localCompletePath = os.path.join(Config.cacheDir, localImageName)
        try:
            if os.path.exists(localCompletePath): #check cache
                    thumb = localCompletePath
            else: #  save them in cache folder
                    logFile.debug("Downloading thumb. Filename=%s", localImageName)
                    thumb = uriHandler.Download(remoteImage, localImageName, folder=Config.cacheDir, pb=False)
                    if thumb == "":
                        return self.noImage
        except:
            logFile.error("Error opening thumbfile!", exc_info=True)
            return self.noImage            
        
        return thumb    
    
    #===============================================================================
    # Default methods
    #===============================================================================
    def __str__(self):
        """Returns a string representation of the current channel."""
        
        if self.channelCode == "":
            return "%s [%s, %s] (Order: %s)" % (self.channelName, self.language, self.guid, self.sortOrder)
        else:
            return "%s (%s) [%s, %s] (Order: %s)" % (self.channelName, self.channelCode, self.language, self.guid, self.sortOrder)
    
    #============================================================================== 
    def __eq__(self, other):
        """Compares to channel objects for equality
        
        Arguments: 
        other : Channel - the other channel to compare to
        
        The comparison is based only on the self.guid of the channels. 
         
        """
        
        if other == None:
            return False
        
        return self.guid == other.guid
    
    def __cmp__(self, other):
        """Compares to channels
        
        Arguments:
        other : Channel - the other channel to compare to
        
        Returns:
        The return value is negative if self < other, zero if self == other and strictly positive if self > other
        
        """
        
        if other == None:
            return 1
        
        compVal = cmp(self.sortOrder, other.sortOrder)
        if compVal == 0:
            compVal = cmp(self.channelName, self.channelName)
        
        return compVal
    
    #==============================================================================
    # Default ContextMenu functions
    #==============================================================================
    def CtMnPlayMplayer(self, item):
        """Default ContextMenuHandling for playback of an MediaItem via "mplayer".
        
        Arguments:
        item : MediaItem - the MediaItem to playback.
        
        Returns the updated MediaItem after calling self.PlayVideoItem. The player 
        it defaults to is "mplayer".
        
        """
        
        return self.PlayVideoItem(item, "mplayer")
    
    def CtMnPlayDVDPlayer(self, item):
        """Default ContextMenuHandling for playback of an MediaItem via "dvdplayer".
        
        Arguments:
        item : MediaItem - the MediaItem to playback.
        
        Returns the updated MediaItem after calling self.PlayVideoItem. The player 
        it defaults to is "dvdplayer".
        
        """
        
        return self.PlayVideoItem(item, "dvdplayer")