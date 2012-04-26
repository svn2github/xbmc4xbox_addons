import xbmc, xbmcgui
import sys
#===============================================================================
# Make global object available
#===============================================================================
import common
import mediaitem
import contextmenu
import chn_class
import guicontroller
import settings
from helpers import htmlentityhelper
from envcontroller import Environments

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

register.RegisterChannel('chn_nos', 'ned1')
register.RegisterChannel('chn_nos', 'ned2')
register.RegisterChannel('chn_nos', 'ned3')
register.RegisterChannel('chn_nos', 'zappold')
        
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
        
        try:
            # call base function first to ensure all variables are there
            chn_class.Channel.InitialiseVariables(self)
            
            self.noImage = "nosimage.png"
            self.baseUrl = "http://oud.uitzendinggemist.nl"
            self.baseUrl2 = "http://wmc.uitzendinggemist.nl"
            self.requiresLogon = False
            self.playerUrl = "http://player.omroep.nl/xml/metaplayer.xml.php"
            self.language = "nl"
            self.compatiblePlatforms = Environments.Unknown
            
            if self.channelCode == "ned1":
                self.guid = "CD702550-42F3-11DD-80F9-8FF855D89593"
                self.mainListUri = "http://oud.uitzendinggemist.nl/index.php/selectie?searchitem=net_zender&net_zender=1&sort=datum"
                #self.mainListUri = "http://wmc.uitzendinggemist.nl/xmlHTTP/searchZender.php?zenderID=1" 
                self.icon = "1icon.png"
                self.iconLarge = "1large.png"
                self.noImage = "nosimage.png"
                self.channelName = "Nederland 1"
                self.moduleName = "chn_nos.py"
                self.sortOrder = 1
                self.channelDescription = "Uitzendingen van de publieke zender Nederland 1"
                
            elif self.channelCode == "ned2":
                self.guid = "C875C1B8-42F3-11DD-BBC9-E4F755D89593"
                self.mainListUri = "http://oud.uitzendinggemist.nl/index.php/selectie?searchitem=net_zender&net_zender=2&sort=datum"
                #self.mainListUri = "http://wmc.uitzendinggemist.nl/xmlHTTP/searchZender.php?zenderID=2" 
                self.icon = "2icon.png"
                self.iconLarge = "2large.png"
                self.noImage = "nosimage.png"
                self.channelName = "Nederland 2"
                self.channelDescription = "Uitzendingen van de publieke zender Nederland 2"
                self.moduleName = "chn_nos.py"
                self.sortOrder = 2
                
            elif self.channelCode == "ned3":
                self.guid = "D0BDAA2A-42F3-11DD-A8C0-D3F855D89593"
                self.mainListUri = "http://oud.uitzendinggemist.nl/index.php/selectie?searchitem=net_zender&net_zender=3&sort=datum"
                #self.mainListUri = "http://wmc.uitzendinggemist.nl/xmlHTTP/searchZender.php?zenderID=3" 
                self.icon = "3icon.png"
                self.iconLarge = "3large.png"
                self.noImage = "nosimage.png"
                self.channelName = "Nederland 3"
                self.channelDescription = "Uitzendingen van de publieke zender Nederland 3"
                self.moduleName = "chn_nos.py"
                self.sortOrder = 3
            
            else: 
                self.guid = "99fa1469-0a95-413e-b1a7-3f9b0506a67b"                                   
                self.mainListUri = "http://oud.uitzendinggemist.nl/index.php/selectie?searchitem=omroep&omroep=47&sort=datum"
                self.icon = "zappicon.png"
                self.iconLarge = "zapplarge.png"
                self.noImage = "zapimage.png"
                self.channelName = "Z@PP"
                self.channelDescription = "Uitzendingen van Z@PP"
                self.moduleName = "chn_nos.py"
                self.sortOrder = 10
    
            self.contextMenuItems = []
            self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using Mplayer", "CtMnPlayMplayer", itemTypes="video", completeStatus=True))
            self.contextMenuItems.append(contextmenu.ContextMenuItem("Play using DVDPlayer", "CtMnPlayDVDPlayer", itemTypes="video", completeStatus=True))
        
            self.episodeItemRegex = '<a class="title" href="(/index.php/serie\?serID=\d+&amp;md5=[0-9a-f]+)">([^<]+)</a>\W+</div>\W+</td>\W+<td[^>]+>(\d+)-(\d+)-(\d+)'
            #self.episodeItemRegex = '<span[^>]+name="([^"]+)"[^>]+>([^<]+)</span>' 
            self.videoItemRegex = '' 
            self.folderItemRegex = '' #not possible, to complex here. ProcessFolderList is used
            
            """ 
                The ProcessPageNavigation method will parse the current data using the pageNavigationRegex. It will
                create a pageItem using the CreatePageItem method. If no CreatePageItem method is in the channel,
                a default one will be created with the number present in the resultset location specified in the 
                pageNavigationRegexIndex and the url from the combined resultset. If that url does not contain http://
                the self.baseUrl will be added. 
            """
            self.pageNavigationRegex = '<a title="Pagina #\d+" href="(/index.php/serie2\?serID=\d+&)amp;(pgNum=)(\d+)(&)amp;([^"]+)" style="text-decoration:none;">\d+</a>' #self.pageNavigationIndicationRegex 
            self.pageNavigationRegexIndex = 2
        except:
            logFile.debug("Error Initialising Varialbles for NOS", exc_info=True)
        #============================================================================== 
        # non standard items
        self.sortAlphabetically = True
        self.maxNumberOfFrontPages = settings.AddonSettings().GetMaxNumberOfPages()        
        return True

    #============================================================================== 
    def InitPlugin(self):
        self.pluginMode = True
        self.maxNumberOfFrontPages = settings.AddonSettings().GetMaxNumberOfPages()
        
        #check for cookie:
        logFile.info("Checking for %s cookies.", self.channelName)
        if uriHandler.CookieCheck('UGSES') and uriHandler.CookieCheck('CheckUGCookie'): # and uriHandler.CookieCheck('UGWMC'):
            logFile.info("Cookies found. Continuing")
        else:
            logFile.info("No cookies found. Opening main site")
            
            if not uriHandler.CookieCheck('UGSES') and not uriHandler.CookieCheck('CheckUGCookie'):
                logFile.debug("Opening %s for cookie UGSES", self.baseUrl)
                temp = uriHandler.Open("%s/" % (self.baseUrl,))
                
            #if not uriHandler.CookieCheck('UGWMC'):
            #    logFile.debug("Opening %s for cookie UGWMC", self.baseUrl2)
            #    temp = uriHandler.Open(self.baseUrl2)
                 
        return chn_class.Channel.InitPlugin(self)    
            
     
    #==============================================================================
    def ParseMainList(self):
        """ 
        accepts an url and returns an list with items of type CListItem
        Items have a name and url. 
        """
        self.maxNumberOfFrontPages = settings.AddonSettings().GetMaxNumberOfPages()
        
        if len(self.mainListItems)>1:
            return self.mainListItems
        
        items = []
        logFile.info('Mainlist for %s parsing %s', self.channelName, self.mainListUri)
        
        #check for cookie:
        logFile.info("Checking for %s cookies.", self.channelName)
        if uriHandler.CookieCheck('UGSES') and uriHandler.CookieCheck('CheckUGCookie'): # and uriHandler.CookieCheck('UGWMC'):
            logFile.info("Cookies found. Continuing")
        else:
            logFile.info("No cookies found. Opening main site")
            
            if not uriHandler.CookieCheck('UGSES') and not uriHandler.CookieCheck('CheckUGCookie'):            
                logFile.debug("Opening %s for cookie UGSES", self.baseUrl)
                temp = uriHandler.Open("%s/" %(self.baseUrl,))
               
            #if not uriHandler.CookieCheck('UGWMC'):
            #    logFile.debug("Opening %s for cookie UGWMC", self.baseUrl2)
            #    temp = uriHandler.Open(self.baseUrl2)
    
        #now start opening
        if not self.pluginMode:
            pb = xbmcgui.DialogProgress()
            pb.create("Opening %s" % (self.channelName,), "Opening page 1 of ??")
        
        try:
            data = uriHandler.Open(self.mainListUri, pb=False, proxy=self.proxy)
            
            # find number of subpages and load them
            numPages = common.DoRegexFindAll("&amp;pgNum=(\d+)", data);
            numPages.sort()
            
            if len(numPages) > 0:
                numPages = int(numPages[-1])
                if numPages > self.maxNumberOfFrontPages:
                    numPages = self.maxNumberOfFrontPages
            else:
                numPages = 1
            logFile.debug("Loading %s pages from the frontpage of uzg", numPages)
            
            # now loop through the pages
            for page in range(1,numPages+1):
                if page > 1:
                    if not self.pluginMode:
                        pb.update(int((page-1)*100/numPages), "Opening page %s of %s" % (page, numPages))
                    
                    data = uriHandler.Open("%s&pgNum=%s" % (self.mainListUri, page), pb=False, proxy=self.proxy)
            
                # programma's
                resultItems = common.DoRegexFindAll(self.episodeItemRegex, data)
                
                for item in resultItems: 
                    tmp = mediaitem.MediaItem(item[1], self.baseUrl + htmlentityhelper.HtmlEntityHelper.StripAmp(item[0]))
                    if len(item) > 2:
                        tmp.SetDate(item[4], item[3], item[2])
                        
                    tmp.icon = self.icon
                    items.append(tmp)
                if not self.pluginMode:
                    if pb.iscanceled():
                        break
                    
            #because lists are downloaded according to date (else some programs will be missing), a sort on name is performed.
            if not self.pluginMode:
                pb.update(int((page)*100/numPages), "Sorting Items")
            
            if self.sortAlphabetically:
                items.sort()
            
            if not self.pluginMode:
                pb.close()
        except:
            logFile.error("Error parsing mainlist", exc_info=True)
            pb.close()
        
        self.mainListItems = items
        return items
    
    #==============================================================================
    def ProcessFolderList(self, item):
        logFile.info('starting ParseFolder for %s', item.url)
        if len(item.items) > 0:
            logFile.debug("ProcessFolderList :: %s Items already available. returning them.", len(item.items))
            return item.items
        
        self.parentItem = item
               
        url = item.url
        items = []
        # get the data for most current episode
        try:
            # load first page as "pageBase"
            data = uriHandler.Open(url, pb=True, proxy=self.proxy)
            
            # see if it is an extended page or not:
            extended = common.DoRegexFindAll('<u>terug naar programma</u>', data)
            if extended != []:
                items = self.ProcessExtendedPages(data)
            else:
                items = self.ProcessNormalPage(data)
                
                # determine if an extended page item should be added
                pageExtUrl = common.DoRegexFindAll('<a href="(/index.php/serie2\?serID=\d+&amp;md5=[0-9a-f]+)"', data)
                if pageExtUrl != []:
                    # add an folder item  for it to the list
                    folderItem =  mediaitem.MediaItem("Oudere afleveringen", self.baseUrl + htmlentityhelper.HtmlEntityHelper.StripAmp(pageExtUrl[0]), type='folder')
                    folderItem.icon = self.folderIcon
                    folderItem.thumb = self.noImage
                    folderItem.complete = True
                    folderItem.description = "Oudere, gearchiveerde items van '%s'." % items[0].name
                    #items.append(folderItem)
                    items.insert(0,folderItem)
            
            return items
        except:
            logFile.critical("Error Parsing with new methode", exc_info=True)
            return items

    #============================================================================= 
    def ProcessNormalPage(self, data):
        logFile.info('starting ProcessNormalPage')
        items = []
        title = common.DoRegexFindAll('<b class="btitle">([^<]+)</b>', data)
        title = title[-1]
            
        results = common.DoRegexFindAll('<td height="40">((\d+)-(\d+)-(\d+)){0,1}</td>\s+[^/]+/index.php/aflevering(\?aflID=\d+)&amp;md5=[0-9a-f]+', data)
        for result in results:
            item = self.CreateEpisodeItem(result[3], result[2], result[1], result[4], title)
            items.append(item)
        return items    
    
    #============================================================================= 
    def ProcessExtendedPages(self, data):
        try:
            logFile.info('starting ProcessExtendedPages')
            items = []
            
            title = common.DoRegexFindAll('<b class="btitle">([^<]+)</b>', data)
            title = title[-1]
            
            results = common.DoRegexFindAll('<a href="http://player.omroep.nl/(\?aflID=\d+)"[^>]*><[^>]+alt="bekijk uitzending: ([^(]+) \(((\d+)-(\d+)-(\d+)){0,1}\)" /></a>', data)
            for result in results:
                item = self.CreateEpisodeItem(result[5], result[4], result[3], result[0], result[1])
                items.append(item)
                
            items = items + self.ProcessPageNavigation(data)
            
            return items
        except:
            logFile.error("Error parsing extended pages", exc_info=True)
            return items
    
    #============================================================================= 
    def CreateEpisodeItem(self, year, month, day, url, title):
        """
        Accepts an arraylist of results. It returns an item. 
        """
        logFile.debug('starting CreateVideoItem for %s', self.channelName)

        #http://player.omroep.nl/?aflID=6954225&md5=e82938c934f962003ec7c9181ca0439e
        item = mediaitem.MediaItem(title, htmlentityhelper.HtmlEntityHelper.StripAmp(url))
        
        if year != "":            
            item.SetDate(year, month, day)
        
        item.thumb = self.noImage
        item.type = 'video'
        item.icon = self.icon
        return item
    
    #============================================================================= 
    def UpdateVideoItem(self, item):
        """
        Accepts an arraylist of results. It returns an item. 
        """
        if not item.type == 'video':
            return item
        
        # if no MD5 is present, get it
        if not item.url.find('md5') >= 0:
            # we need a new cookie for the episode: that is retrieved from: http://player.omroep.nl/?aflID=6746029
            data = uriHandler.Open("http://player.omroep.nl/%s" % (item.url), pb=False, proxy = self.proxy)
            #uriHandler.CookiePrint()
            
            # then we need to get the securitycode to obtain the info XML (var securityCode = '83f9ce0d14af55b2ce48f1fb3af26462';)
            url = "http://player.omroep.nl/js/initialization.js.php%s" % item.url
            data = uriHandler.Open(url, pb=False, proxy = self.proxy)
            code = common.DoRegexFindAll("var securityCode = '([0-9a-f]+)';", data)
            if len(code) == 1:
                code = code[0]
    
            # now we construct the url: http://player.omroep.nl/xml/metaplayer.xml.php?aflID=6954225&md5=e82938c934f962003ec7c9181ca0439e&md5=6fa9fb656ab15d8fa2a086d1c1ba9e47
            url = "%s%s&md5=%s" % (self.playerUrl, item.url, code)
            item.url = url
        elif item.url.startswith('?'):
            logFile.error("No HTTP found in url, adding URL prefix %s to %s and trying anyways", self.playerUrl, item.url)
            item.url = "%s%s" % (self.playerUrl, item.url)
#===============================================================================
#        should be made more compact in 1 single regex
#===============================================================================
        logFile.info('starting UpdateVideoItem for '+ item.url)
        
        data = uriHandler.Open(item.url, pb=False, proxy = self.proxy)
        
        #get title
        title = common.DoRegexFindAll('<tite>(.*)</tite>', data)
        title = title[0]
        
        #get episode ID
        #aflevering = common.DoRegexFindAll('<aflevering id=\'([^\']*)', data)
        
        # now update item:
        item.name = title
        item.type = "video"
        
        # get rating
        rating = common.DoRegexFindAll("<waardering teller='\d+' [^>]+>(\d[.]*\d*)</waardering>", data)
        if len(rating) > 0:
            item.rating = int(float(rating[0]))
            
        # get data
        datums = common.DoRegexFindAll('<begi>(\d+)-(\d+)-(\d+) (\d+):(\d+):(\d+)', data)
        for datum in datums:        
            item.SetDate(datum[2], datum[1], datum[0], datum[3], datum[4], datum[5])
        
        #description
        description = common.DoRegexFindAll('<gids_tekst>([^/]+)((\n&lt;[^<]+&gt;\W\W)([^<]+)*)*</gids_tekst>', data)
        if description == []:
            info = "Geen Omschrijving"
        else:
            info = description[0][0] + description[0][3]
        item.description = info
        
        # get image
        image = common.DoRegexFindAll('<radio_afbeelding>(http://.*/)([^/]*)</radio_afbeelding>', data)
        if image == []: #no image
            item.thumb = self.noImage
        else: #save image
            item.thumb = self.CacheThumb(htmlentityhelper.HtmlEntityHelper.ConvertHTMLEntities(str(image[0][0]) + str(image[0][1])))
                        
        # get the mediaurl
        mediaurl = common.DoRegexFindAll('<stream[^>]+compressie_kwaliteit=.bb.[^>]+compressie_formaat=.wmv.[^>]*>([^<]*)</stream>', data)[0]
        

        # parse the asx
        data = uriHandler.Open(mediaurl, pb=False)
        newMediaUrl = common.DoRegexFindAll('<Ref href[^"]+"([^"]+)"', data)
        if len(newMediaUrl) > 0:
            item.AppendSingleStream(newMediaUrl[0])            
        else:
            item.AppendSingleStream(mediaurl)
            
        # finish and return
        item.complete = True
        logFile.info('finishing UpdateVideoItem: %s', item)        
        
        return item
    
    #==============================================================================
    # ContextMenu functions
    #==============================================================================
    def CtMnPlayMplayer(self, item):
        if not item.complete:
            item = self.UpdateVideoItem(item)
            # check if the list has not changed during upate:
            #if item.guid == self.listItems[_position].guid:
            if item.Equals(self.listItems[self.getCurrentListPosition()]):
                logFile.info("Updating item (GUIDs match)")                
                self.listItems[self.getCurrentListPosition()] = item
            else:
                logFile.error("Aborting Update because of GUID mismatch")
        logFile.info("Starting playback of %s", item)        

        guiController = guicontroller.GuiController(self)
        guiController.UpdateSelectedItem(item)
        
        self.PlayVideoItem(item, "mplayer")
    
    def CtMnPlayDVDPlayer(self, item):
        if not item.complete:
            item = self.UpdateVideoItem(item)
            # check if the list has not changed during upate:
            #if item.guid == self.listItems[_position].guid:
            if item.Equals(self.listItems[self.getCurrentListPosition()]):
                logFile.info("Updating item (GUIDs match)")                
                self.listItems[self.getCurrentListPosition()] = item
            else:
                logFile.error("Aborting Update because of GUID mismatch")
        logFile.info("Starting playback of %s using dvdplayers", item)
        
        guiController = guicontroller.GuiController(self)
        guiController.UpdateSelectedItem(item)
        
        self.PlayVideoItem(item,"dvdplayer")          
