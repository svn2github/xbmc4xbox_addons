#===============================================================================
# LICENSE XOT-Framework - CC BY-NC-ND
#===============================================================================
# This work is licenced under the Creative Commons 
# Attribution-Non-Commercial-No Derivative Works 3.0 Unported License. To view a 
# copy of this licence, visit http://creativecommons.org/licenses/by-nc-nd/3.0/ 
# or send a letter to Creative Commons, 171 Second Street, Suite 300, 
# San Francisco, California 94105, USA. 
#===============================================================================
import os
import sys
import string
import pickle
import base64
import inspect

import xbmcplugin
import xbmcgui

#===============================================================================
# Import XOT stuff
#===============================================================================
try:
    import common
    import settings
    import update
    import envcontroller
    import updater
            
    from locker import LockWithDialog
    from config import Config
    from helpers.channelimporter import ChannelImporter
    from helpers import htmlentityhelper
    from helpers import stopwatch
    
    #===========================================================================
    # Make global object available
    #===========================================================================
    logFile = sys.modules['__main__'].globalLogFile
    uriHandler = sys.modules['__main__'].globalUriHandler
    
    #register for channels
    channelRegister = None
except:
    logFile.critical("Error initializing %s", Config.appName, exc_info=True)

#===============================================================================
# Main Plugin Class
#===============================================================================
class XotPlugin:
    """Main Plugin Class
    
    This class makes it possible to access all the XOT channels as a XBMC plugin
    instead of a script. s
    
    """
    
    def __init__(self, pluginName, params, handle = 0):
        """Initialises the plugin with given arguments."""
        
        self.pluginName = pluginName
        self.handle = int(handle)
        self.params = params.strip('?')
        self.settings = settings.AddonSettings()
        
        # channel objects
        self.channelObject = ""
        self.channelFile = ""
        self.channelCode = ""   
        self.channelObject = ""     
        self.splitChar = "[[#]]"
        
        self.actionProcessVideo = "processVideo".lower()            # : Action used to process a video item (not used in advanced mode)
        self.actionDownloadVideo = "downloadVideo".lower()          # : Action used to download a video item
        self.actionFavorites = "favorites".lower()                  # : Action used to show favorites for a channel
        self.actionRemoveFavorite = "removefromfavorites".lower()   # : Action used to remove items from favorites
        self.actionAddFavorite = "addtofavorites".lower()           # : Action used to add items to favorites
        self.actionPlayVideo = "playvideo".lower()                  # : Action used to play a video item
        self.actionUpdateChannels = "updatechannels".lower()        # : Action used to update channels
        
        self.playAsPlaylist = settings.AddonSettings().UseAdvancedPlugin()
        self.contentType = "movies"
        
#        if self.params=='':
#            # truncate the logfile as this is the first run and write start
#            logFile.CleanUpLog()
        
        logFile.info("*********** Starting %s plugin version v%s ***********", Config.appName, Config.Version)
        logFile.debug("Plugin Params: %s [handle=%s, name=%s]", self.params, self.handle, self.pluginName)   
        #===============================================================================
        #        Start the plugin version of progwindow
        #===============================================================================
        if self.params=='':
            # print the folder structure
            envCtrl = envcontroller.EnvController(logFile)
            envCtrl.DirectoryPrinter(Config, settings.AddonSettings())
            
            # check for updates
            update.CheckVersion(Config.Version, Config.updateUrl)
            
            # check if the repository is available
            envCtrl.IsInstallMethodValid(Config)
            
            # check for cache folder
            common.CacheCheck()
            
            # do some cache cleanup
            common.CacheCleanUp()                

            # now show the list
            self.ShowChannelList()
        #===============================================================================
        #        Start the plugin verion of the episode window
        #===============================================================================
        else:
            # check for cache folder
            common.CacheCheck()
        
            try:
                # determine what stage we are in. Therefore we split the
                # params and check the number of different ones.
                #logFile.debug("Parameters from commandline: %s", self.params)
                self.params = self.params.strip().split(self.splitChar)
                #logFile.debug("Parameters after split: %s", self.params)
                
                # Check that there are more than 2 Parameters
                if len(self.params)>1:
                    # retrieve channel characteristics
                    self.channelFile = os.path.splitext(self.params[0])[0]
                    self.channelCode = self.params[1]
                    logFile.debug("Found Channel data in URL: channel='%s', code='%s'", self.channelFile, self.channelCode)
                    
                    # import the channel, using the global channelRegister.
                    global channelRegister
                    if channelRegister is None:
                        channelRegister = ChannelImporter()
                    channel = channelRegister.GetSingleChannel(self.channelFile, self.channelCode)
                    
                    if not channel is None:
                        logFile.info("Only one channel present. Intialising it.")
                        self.channelObject = channel
                    else:
                        logFile.critical("None or more than one channels were found, unable to continue.")
                        return
                    
                    # init the channel as plugin
                    self.channelObject.InitPlugin()
                    logFile.info("Loaded: %s", self.channelObject.channelName)
                else:
                    logFile.critical("Error determining Plugin action")
                    return
                
                #===============================================================================
                # See what needs to be done.    
                #===============================================================================
                logFile.debug("Found %s parameters", len(self.params))
                if len(self.params)==2:
                    # only the channelName and code is present, so ParseMainList is needed
                    self.ParseMainList()

                elif len(self.params)==3 and self.params[-1] == self.actionFavorites:
                    # we should show the favorites
                    self.ParseMainList(showFavorites=True)
                    
                elif len(self.params)==3 and self.params[-1] == self.actionUpdateChannels:
                    self.UpdateChannels() 

                elif len(self.params)==3:
                    # channelName and URL is present, Parse the folder
                    self.ProcessFolderList()

                elif len(self.params)>3 and self.params[2] == self.actionProcessVideo:
                    # a videoitem was given with an additional paramters
                    self.ProcessVideoItem()

#                Should be done using context menu of the channel
#                elif len(self.params)>3 and self.params[2] == self.actionDownloadVideo:
#                    # download the item
#                    self.DownloadVideoItem()
                    
                elif len(self.params)>3 and self.params[2] == self.actionRemoveFavorite:
                    self.RemoveFavorite()
            
                elif len(self.params)>3 and self.params[2] == self.actionAddFavorite:
                    self.AddFavorite()
            
                elif len(self.params)>3 and self.params[2] == self.actionPlayVideo:
                    self.PlayVideoItem()
                    
                elif len(self.params)>3 and not self.params[2] == "":
                    self.OnActionFromContextMenu(self.params[2])
                else:
                    logFile.debug("Number of parameters (%s) or parameter (%s) values not implemented", len(self.params), self.params)
                #if self.handle > -1:
                #    xbmcplugin.endOfDirectory(self.handle)
            except:
                logFile.critical("Error parsing for plugin", exc_info=True)
                #xbmcplugin.endOfDirectory(self.handle)

    def ShowChannelList(self):
        """Displays the channels that are currently available in XOT as a directory
        listing."""
        
        logFile.info("Plugin::ShowChannelList")
        try:
            # import ProgWindow
            ok = False
            
            # first start of plugin! Show channels only!
            if len(self.params)<=2:
                
                # only display channels, use the global channelRegister to get 
                # the channels
                global channelRegister
                if channelRegister is None:
                    channelRegister = ChannelImporter()
                channels = channelRegister.GetChannels()
                
                for channel in channels:
                    item = xbmcgui.ListItem(channel.channelName,channel.channelDescription, channel.icon , channel.iconLarge)
                    item.setInfo("video", {"tracknumber": channel.sortOrder, "Tagline":channel.channelDescription})
                    
                    contextMenuItems = self.__GetContextMenuItems(channel)
                    item.addContextMenuItems(contextMenuItems)
                    
                    url = self.__CreateActionUrl(channel)
                    ok = xbmcplugin.addDirectoryItem(self.handle, url, item, isFolder=True, totalItems=len(channels))
                    if (not ok): break
            
            xbmcplugin.addSortMethod(handle=self.handle, sortMethod=xbmcplugin.SORT_METHOD_TRACKNUM)
            #xbmcplugin.setContent(handle=self.handle, content=self.contentType)
            #xbmcplugin.addSortMethod(handle=self.handle, sortMethod=xbmcplugin.SORT_METHOD_FILE)
            
            xbmcplugin.endOfDirectory(self.handle, ok)
        except:
            xbmcplugin.endOfDirectory(self.handle, False)
            logFile.critical("Error fetching channels for plugin", exc_info=True)
    
    def ParseMainList(self, showFavorites=False, replaceExisting=False):
        """Wraps the channel.ParseMainList
        
        Keyword Arguments:
        showFavorites : boolean - if True it will show the favorites instead of all the items
        
        """
        
        logFile.info("Plugin::ParseMainList")
        try:
            ok = False           
            
            # only the channelName and code is present, so ParseMainList is needed
            if showFavorites:
                logFile.debug("Showing Favorites")
                
                #self.favoriteItems = settings.LoadFavorites(self.activeChannelGUI)
                #self.ShowListItems(self.favoriteItems)
                episodeItems =  settings.LoadFavorites(self.channelObject)
                if len(episodeItems) == 0:
                    logFile.info("No favorites available")
                    dialog = xbmcgui.Dialog()
                    dialog.ok(Config.appName, "No favorites available")
            
                #logFile.debug(episodeItems)
                # nothing to show, set to true
                ok = True
                pass
            else:  
                logFile.debug("Doing ParseMainlist")            
                episodeItems = self.channelObject.ParseMainList()            
            
            for episodeItem in episodeItems:
                item = episodeItem.GetXBMCItem(pluginMode=True)
                
                # add the remove from favorites item:
                if showFavorites:
                    # XBMC.Container.Refresh refreshes the container and replaces the last history 
                    # XBMC.Container.Update updates the container and but appends the new list to the history
                    contextMenuItems = self.__GetContextMenuItems(self.channelObject, item = episodeItem, favoritesList = True)
                else:
                    contextMenuItems = self.__GetContextMenuItems(self.channelObject, item = episodeItem)
                    
                    # add the show favorites here
                    cmdUrl = self.__CreateActionUrl(self.channelObject, action = self.actionFavorites)
                    cmd = "XBMC.Container.Update(%s)" % (cmdUrl,)
                    #logFile.debug("Adding command: %s", cmd[:100])
                    contextMenuItems.append(('XOT: Show Favorites', cmd))
                    
                item.addContextMenuItems(contextMenuItems)
                
                #time.sleep(0.001)
                url = self.__CreateActionUrl(self.channelObject, item = episodeItem) 
                ok = xbmcplugin.addDirectoryItem(self.handle, url, item, isFolder=True, totalItems=len(episodeItems))
                if (not ok): break
            
            self.__AddSortMethodToHandle(self.handle, episodeItems)
            
            # set the content
            xbmcplugin.setContent(handle=self.handle, content=self.contentType)
            
            # close the directory                
            if showFavorites:
                logFile.debug("Plugin::Favorites completed")
                # make sure we do not cache this one to disc!
                xbmcplugin.endOfDirectory(self.handle, succeeded=ok, updateListing=replaceExisting, cacheToDisc = False)
            else:
                logFile.debug("Plugin::Processing Mainlist completed. Returned %s items", len(episodeItems))
                xbmcplugin.endOfDirectory(self.handle, succeeded=ok, updateListing=replaceExisting)
        except:
            logFile.debug("Plugin::Error parsing mainlist", exc_info=True)
            xbmcplugin.endOfDirectory(self.handle, False)            
     
    def __AddSortMethodToHandle(self, handle, items=None):
        """ Add a sort method to the plugin output. It takes the Add-On settings into
        account. But if none of the items have a date, it is forced to sort by name.
        
        Arguments: 
        handle : int        - The handle to add the sortmethod to
        items  : MediaItems - The items that need to be sorted
        
        """
        
        sortAlgorthim = settings.AddonSettings().GetSortAlgorithm() 
        
        if sortAlgorthim == "date":
            # if we had a list, check it for dates. Else assume that there are no dates!
            if items:
                hasDates = len(filter(lambda i : i.HasDate(), items)) > 0
                #for item in items:
                #    logFile.debug(item)
            else:
                hasDates = True
            
            if hasDates:
                logFile.debug("Sorting method default: Dates")
                xbmcplugin.addSortMethod(handle=handle, sortMethod=xbmcplugin.SORT_METHOD_DATE)
                xbmcplugin.addSortMethod(handle=handle, sortMethod=xbmcplugin.SORT_METHOD_LABEL)
                xbmcplugin.addSortMethod(handle=handle, sortMethod=xbmcplugin.SORT_METHOD_UNSORTED)
            else:
                logFile.debug("Sorting method default: Dates, but no dates are available, sorting by name")
                xbmcplugin.addSortMethod(handle=handle, sortMethod=xbmcplugin.SORT_METHOD_LABEL)
                xbmcplugin.addSortMethod(handle=handle, sortMethod=xbmcplugin.SORT_METHOD_DATE)   
                xbmcplugin.addSortMethod(handle=handle, sortMethod=xbmcplugin.SORT_METHOD_UNSORTED)     
                    
        elif sortAlgorthim == "name":
            logFile.debug("Sorting method default: Names")
            xbmcplugin.addSortMethod(handle=handle, sortMethod=xbmcplugin.SORT_METHOD_LABEL)
            xbmcplugin.addSortMethod(handle=handle, sortMethod=xbmcplugin.SORT_METHOD_DATE)   
            xbmcplugin.addSortMethod(handle=handle, sortMethod=xbmcplugin.SORT_METHOD_UNSORTED)     
        
        else: 
            logFile.debug("Sorting method default: None")
            xbmcplugin.addSortMethod(handle=handle, sortMethod=xbmcplugin.SORT_METHOD_UNSORTED)
            xbmcplugin.addSortMethod(handle=handle, sortMethod=xbmcplugin.SORT_METHOD_LABEL)
            xbmcplugin.addSortMethod(handle=handle, sortMethod=xbmcplugin.SORT_METHOD_DATE)
        return
      
    def ProcessFolderList(self):
        """Wraps the channel.ProcessFolderList"""
        
        logFile.info("Plugin::ProcessFolderList Doing ProcessFolderList")
        try:    
            # strip the extra space from the url
            self.params[2] = string.strip(self.params[2])
            ok = False
                        
            selectedItem = self.DePickleMediaItem(self.params[2])
            
            watcher = stopwatch.StopWatch("Plugin ProcessFolderList", logFile)            
            episodeItems = self.channelObject.ProcessFolderList(selectedItem)            
            watcher.Lap("Class ProcessFolderList finished")
            
            logFile.debug("ProcessFolderList returned %s items", len(episodeItems))
            for episodeItem in episodeItems:
                logFile.debug("Adding: %s", episodeItem)
                
                if episodeItem.type == 'folder' or episodeItem.type == 'append' or episodeItem.type == "page":
                    # it's a folder page or append style. Append as an XBMC folder
                    item = episodeItem.GetXBMCItem(True)          
                    
                    contextMenuItems = self.__GetContextMenuItems(self.channelObject, item = episodeItem)
                    item.addContextMenuItems(contextMenuItems)
                        
                    url = self.__CreateActionUrl(self.channelObject, item = episodeItem)                
                    ok = xbmcplugin.addDirectoryItem(self.handle, url, item, isFolder=True, totalItems=len(episodeItems))
                
                elif episodeItem.type=="video":
                    if self.playAsPlaylist:
                        logFile.debug("Using advanced playlists")
                        # we will process the videoitem as a playlist and add contextmenu's
                        item = episodeItem.GetXBMCItem(pluginMode=True) 
                        
                        contextMenuItems = self.__GetContextMenuItems(self.channelObject, item = episodeItem)
                        item.addContextMenuItems(contextMenuItems)
                        
                        url = self.__CreateActionUrl(self.channelObject, action = self.actionPlayVideo, item = episodeItem)
                        ok = xbmcplugin.addDirectoryItem(int(self.handle), url, item, totalItems=len(episodeItems))                        
                        
                    elif len(episodeItem.MediaItemParts) == 1 and episodeItem.complete == True and episodeItem.downloadable == False:
                        # it's a complete item with only 1 url, just add the URL
                        (stream, item) = episodeItem.MediaItemParts[0].GetXBMCPlayListItem(episodeItem, pluginMode=True) 
                        url = "%s " % (stream.Url,)
                        ok = xbmcplugin.addDirectoryItem(int(self.handle), url, item, totalItems=len(episodeItems))
                    else:   
                        # all other options
                        item = episodeItem.GetXBMCItem(True)                
                        # create serialized cListItem 
                        url = self.__CreateActionUrl(self.channelObject, action = self.actionProcessVideo, item = episodeItem)
                        ok = xbmcplugin.addDirectoryItem(self.handle, url, item, isFolder=True, totalItems=len(episodeItems))                    
                else:
                    logFile.critical("Plugin::ProcessFolderList: Cannot determine what to add")
                    
                if (not ok): break
            
            watcher.Stop()
            
            self.__AddSortMethodToHandle(self.handle, episodeItems)
            
            # set the content
            xbmcplugin.setContent(handle=self.handle, content=self.contentType)
            
            xbmcplugin.endOfDirectory(self.handle, ok)
        except:
            xbmcplugin.endOfDirectory(self.handle, False)
            logFile.debug("Plugin::Error Processing FolderList", exc_info=True)
                
    @LockWithDialog(logger = logFile)
    def RemoveFavorite(self):
        """Removes an item from the favorites"""
        
        logFile.debug("Removing favorite")
        
        # remove the item
        item = self.DePickleMediaItem(self.params[3])
        settings.RemoveFromFavorites(item, self.channelObject)
        
        # refresh the list
        self.ParseMainList(showFavorites=True, replaceExisting=True)
        pass
    
    @LockWithDialog(logger = logFile)
    def AddFavorite(self):
        """Adds an item to the favorites"""
        
        logFile.debug("Adding favorite")
        
        # remove the item
        item = self.DePickleMediaItem(self.params[3])
        settings.AddToFavorites(item, self.channelObject)
        
        # we are finished, so just return
        return self.ParseMainList(showFavorites=True)
    
    def ProcessVideoItem(self):
        """Wraps the channel.UpdateVideoItem and adds an folder with videofile options like
        download and play videoitem. 
        
        This method is not used if UseAdvancedPlugin is True.
        
        """
        
        logFile.info("Plugin::ProcessVideoItem starting")
            
        try:            
            # de-serialize
            pickleItem = self.DePickleMediaItem(self.params[3])
            ok = False
            
            episodeItem = pickleItem
            logFile.debug("De-Pickled: %s", episodeItem)

            #update the item is not up to date
            if episodeItem.complete==False:
                logFile.debug("Trying to update a videoItem")
                episodeItem =self.channelObject.UpdateVideoItem(episodeItem)
                if not episodeItem.HasMediaItemParts():
                    episodeItem.complete = False;
                    
                logFile.debug("Updated MediaItem: %s", episodeItem)
            
            if episodeItem.complete==True and episodeItem.HasMediaItemParts():
                #self.channelObject.PlayVideoItem(episodeItem)
                #ok = False                    
                title = "Play Item: %s" % episodeItem.name
                count = 1
                for mediaListPart in episodeItem.MediaItemParts:
                    if len(episodeItem.MediaItemParts) == 1:
                        partName = title
                    else:
                        partName = "%s (#%s)" % (title, count)
                    # should we download?
                    if not mediaListPart.CanStream:
                        bitrate = settings.AddonSettings().GetMaxStreamBitrate()
                        stream = mediaListPart.GetMediaStreamForBitrate(bitrate)
                        if not stream.Downloaded:
                            logFile.debug("Downloading not streamable part: %s\nDownloading Stream: %s", mediaListPart, stream)
                            file = stream.Url[stream.Url.rfind("/")+1:]
                            folder = uriHandler.Download(stream.Url, file, Config.cacheDir, proxy = self.channelObject.proxy, userAgent=mediaListPart.UserAgent)
                            if folder == "":
                                logFile.error("Cannot download stream %s \nFrom: %s", stream, mediaListPart)
                                continue
                            stream.Url = folder
                            stream.Downloaded = True
                    
                    (stream, xbmcListItem) = mediaListPart.GetXBMCPlayListItem(episodeItem, pluginMode=True, name=partName)
                    
                    logFile.debug("Adding item:  %s:\n%s\nStream: %s", partName, mediaListPart, stream)
                    if mediaListPart.UserAgent is None:
                        totalUrl = stream.Url
                    else:
                        totalUrl = "%s|User-Agent=%s" % (stream.Url, htmlentityhelper.HtmlEntityHelper.UrlEncode(mediaListPart.UserAgent))                        
                    ok = xbmcplugin.addDirectoryItem(int(self.handle), url=totalUrl, listitem=xbmcListItem)
                    
                    count = count + 1
                    if not ok:
                        break
                
                    if episodeItem.downloadable == True:
                        title = "Download Item: %s" % partName
                        (stream, xbmcListItem) = mediaListPart.GetXBMCPlayListItem(episodeItem, pluginMode=True, name=title)
                        logFile.debug("Adding download item:  %s:\n%s\nStream: %s", partName, mediaListPart, stream)                    
                        url = self.__CreateActionUrl(self.channelObject, action = self.actionDownloadVideo, item = episodeItem)
                        ok = xbmcplugin.addDirectoryItem(int(self.handle), url, xbmcListItem)                
            else:
                logFile.error("could not update videoItem")
            
           
            self.__AddSortMethodToHandle(self.handle)
            # set the content
            xbmcplugin.setContent(handle=self.handle, content=self.contentType)
            
            xbmcplugin.endOfDirectory(self.handle, ok)        
        except:
            xbmcplugin.endOfDirectory(self.handle, False)   
            logFile.critical("Error Updating VideoItem", exc_info=True)
            pass
        
    @LockWithDialog(logger = logFile)
    def PlayVideoItem(self):
        """Starts the videoitem using a playlist instead of just the URL only
        used in advanced mode.
        
        """
        
        logFile.debug("Playing videoitem using PlayListMethod")
        
        item = self.DePickleMediaItem(self.params[3])
        
        if not item.complete:
            item = self.channelObject.UpdateVideoItem(item)
        
        self.channelObject.PlayVideoItem(item)
        pass
    
    def DownloadVideoItem(self):
        """Warps the DownloadVideoItem method. Downloads the item, show the 
        diffent dialogs. 
        
        This method is not used when UseAdvancedPlugin is True
        
        """
        
        logFile.info("Plugin::DownloadVideoItem starting")
            
        try:
            logFile.debug("Trying to update a videoItem")
            
            # de-serialize
            pickleString = self.params[3];
            pickleItem = self.DePickleMediaItem(pickleString)
            self.channelObject.DownloadVideoItem(pickleItem)            
            xbmcplugin.endOfDirectory(self.handle, True)
        except:
            logFile.critical("Error Downloading VideoItem", exc_info=True)

    def UpdateChannels(self):
        """Shows the XOT Channel update dialog (only for XBMC4Xbox). 
        
        Arguments:
        selectedIndex : integer - the index of the currently selected item this
                                  one is not used here.
        
        """
        
        updaterWindow = updater.Updater(Config.updaterSkin ,Config.rootDir, Config.skinFolder)
        updaterWindow .doModal()
        del updaterWindow

    def OnActionFromContextMenu(self, action):
        """Peforms the action from a custom contextmenu
        
        Arguments:
        action : String - The name of the method to call
        
        """
        logFile.debug("Performing Custom Contextmenu command: %s", action)
        
        item = self.DePickleMediaItem(self.params[3])
        if not item.complete and self.__ContextActionRequiredCompletedItem(action):
            logFile.debug("The contextmenu action requires a completed item. Updating %s", item)
            item = self.channelObject.UpdateVideoItem(item)
        
        # invoke
        functionString = "returnItem = self.channelObject.%s(item)" % (action, )
        logFile.debug("Calling '%s'", functionString)
        try:
            exec(functionString)
        except:
            logFile.error("OnActionFromContextMenu :: Cannot execute '%s'.", functionString, exc_info = True)
        return

    def PickleMediaItem(self, item):
        """Serialises a mediaitem
        
        Arguments:
        item : MediaItem - the item that should be serialized
        
        Returns:
        A pickled and base64 encoded serialization of the <item>.
        
        """
        
        pickleString = pickle.dumps(item)
        #logFile.debug("Pickle: PickleString: %s", pickleString)                        
        hexString = base64.encodestring(pickleString)        
        #logFile.debug("Pickle: HexString: %s", hexString)                                
        return hexString
    
    def DePickleMediaItem(self, hexString):
        """De-serializes a serialized mediaitem
        
        Arguments:
        hexString : string - Base64 encoded string that should be decoded.
        
        Returns:
        The object that was Pickled and Base64 encoded. 
        
        """
        
        #logFile.debug("DePickle: HexString: %s", hexString)                                
        pickleString = base64.decodestring(hexString)
        #logFile.debug("DePickle: PickleString: %s", pickleString)                        
        pickleItem = pickle.loads(pickleString)
        return pickleItem

    def __ContextActionRequiredCompletedItem(self, action):
        """Get the current context menu and returns if it requires
        an complete MediaItem
        
        Arguments:
        action : string - the Action that the contextmenu should perform
        
        """
        
        for menuItem in self.channelObject.contextMenuItems:
            if menuItem.functionName == action:
                if menuItem.completeStatus is None:
                    return False
                else:
                    # if complete status = False, we don't need a completed one
                    # if complete status = True, we do need one
                    return menuItem.completeStatus 
        
        logFile.warning("ContextMenuAction [%s] not found in channel", action)
        return False

    def __CreateActionUrl(self, channel, action = None, item = None):
        """Creates an URL that includes an action
        
        Arguments:
        channel : Channel - The channel object to use for the URL  
        action  : string  - Action to create an url for
        
        Keyword Arguments:
        item : MediaItem - The media item to add  
        
        """
        
        # create item and add an extra space at the end to prevent removal of last /                
        if item is None and action is None:
            url = "%s?%s%s%s "     % (self.pluginName, channel.moduleName, self.splitChar, channel.channelCode)
        elif action is None:
            pickleString = self.PickleMediaItem(item)
            url = "%s?%s%s%s%s%s "     % (self.pluginName, channel.moduleName, self.splitChar, channel.channelCode, self.splitChar, pickleString)
        elif item is None:
            pickleString = self.PickleMediaItem(item)
            url = "%s?%s%s%s%s%s "     % (self.pluginName, channel.moduleName, self.splitChar, channel.channelCode, self.splitChar, action)
        else:
            pickleString = self.PickleMediaItem(item)        
            url = "%s?%s%s%s%s%s%s%s " % (self.pluginName, channel.moduleName, self.splitChar, channel.channelCode, self.splitChar, action, self.splitChar, pickleString)
        
        #logFile.debug("Created url: '%s'", url)
        return url
    
    def __GetContextMenuItems(self, channel, item = None, favoritesList = False):
        """Retrieves the context menu items to display
        
        Arguments:
        channel : Channel - The channel from which to get the context menu items
        
        Keyword Arguments
        item          : MediaItem - The item to which the context menu belongs.
        favoritesList : Boolean   - Indication that the menu is for the favorites
        """
                    
        contextMenuItems = []
        
        if item is None:
            # it's just the channel, so only add the favorites
            cmdUrl = self.__CreateActionUrl(channel, action = self.actionFavorites)
            cmd = "XBMC.Container.Update(%s)" % (cmdUrl,)
            logFile.debug("Adding command: %s...", cmd[:100])
            contextMenuItems.append(("XOT: Show Favorites", cmd))
            
            if envcontroller.EnvController.IsPlatform(envcontroller.Environments.Xbox):
                # we need to run RunPlugin here instead of Refresh as we don't want to refresh any lists 
                # the refreshing results in empty lists in XBMC4Xbox.
                cmdUrl = self.__CreateActionUrl(channel, action = self.actionUpdateChannels)
                cmd = "XBMC.RunPlugin(%s)" % (cmdUrl,)
                #logFile.debug("Adding command: %s...", cmd[:100])
                contextMenuItems.append(("XOT: Update Channels", cmd))
            
            return contextMenuItems
        
        # we have an item
        if favoritesList:
            # we have list of favorites
            cmdUrl = self.__CreateActionUrl(self.channelObject, action = self.actionRemoveFavorite, item = item)
            cmd = "XBMC.Container.Update(%s)" % (cmdUrl,)
            logFile.debug("Adding command: %s...", cmd[:100])
            contextMenuItems.append(("XOT: Remove Favorite", cmd))  
    
        elif item.type == "folder":
            # we need to run RunPlugin here instead of Refresh as we don't want to refresh any lists 
            # the refreshing results in empty lists in XBMC4Xbox.
            cmdUrl = self.__CreateActionUrl(channel, action = self.actionAddFavorite, item = item)
            #cmd = "XBMC.RunPlugin(%s)" % (cmdUrl,)
            cmd = "XBMC.Container.Update(%s)" % (cmdUrl,)
            #logFile.debug("Adding command: %s...", cmd[:100])
            contextMenuItems.append(("XOT: Add to Favorites", cmd))
        
        
        # now we process the other items
        possibleMethods = inspect.getmembers(channel)
        #logFile.debug(possibleMethods)
    
        for menuItem in channel.contextMenuItems:
            #logFile.debug(menuItem)
            if not menuItem.plugin:
                continue
                            
            if menuItem.itemTypes == None or item.type in menuItem.itemTypes:
                # We don't care for complete here!
                #if menuItem.completeStatus == None or menuItem.completeStatus == item.complete:
                
                # see if the method is available
                methodAvailable = False
                
                for method in possibleMethods:
                    if method[0] == menuItem.functionName:
                        methodAvailable = True
                        # break from the method loop
                        break                    
                
                if not methodAvailable:
                    logFile.info("No method for: %s", menuItem)
                    continue

                cmdUrl = self.__CreateActionUrl(channel, action = menuItem.functionName, item = item)
                cmd = "XBMC.RunPlugin(%s)" % (cmdUrl,)
                logFile.debug("Adding command: %s...", cmd[:100])
                title = "XOT: %s" % (menuItem.label,)
                contextMenuItems.append((title, cmd))
            
        return contextMenuItems