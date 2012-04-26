import sys
import os.path
import datetime

import xbmc
import xbmcgui

import common
import mediaitem
from config import Config
from helpers import htmlentityhelper
from envcontroller import Environments

#===============================================================================
# Make global object available
#===============================================================================
sys.path.append(os.path.join(Config.rootDir, "channels", "nos"))                    
import chn_nos

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

register.RegisterChannel('chn_nossearch','nedsearch')

#===============================================================================
# main Channel Class
#===============================================================================
class Channel(chn_nos.Channel):
    #===============================================================================
    # define class variables
    #===============================================================================
    def InitialiseVariables(self):
        """
        Used for the initialisation of user defined parameters. All should be 
        present, but can be adjusted
        """
        # call base function first to ensure all variables are there
        chn_nos.Channel.InitialiseVariables(self)
        
        self.guid = "DCD0F3BC-42F3-11DD-8860-B6F955D89593"
        self.mainListUri = ""
        self.icon = "nosicon.png"
        self.iconLarge = "noslarge.png"
        self.noImage = "nosimage.png"
        self.channelName = "Uitzendinggemist"
        self.channelCode = "nedsearch"
        self.channelDescription = "Speciale items zoals 'Zoeken', 'Nieuw toegevoegd' en 'Populaire uitzendingen'"
        self.moduleName = "chn_nossearch.py"
        self.sortOrder = 4
        self.language = "nl"
        self.compatiblePlatforms = Environments.Unknown
        
        return True

    #============================================================================== 
    def ParseMainList(self):
        items = []
        
        searchItem = mediaitem.MediaItem("Zoek in oud.uitzendinggemist.nl", "searchSite")
        searchItem.icon = self.icon
        items.append(searchItem)
        
        newItem = mediaitem.MediaItem("Nieuw toegevoegd", "newItems")
        newItem.icon = self.icon
        items.append(newItem)        
        
        popItem = mediaitem.MediaItem("Populaire uitzendingen","popularItems")
        popItem.icon = self.icon
        items.append(popItem)        
        
        tipItem = mediaitem.MediaItem("Eerdere Tips","tipItems")
        tipItem.icon = self.icon
        items.append(tipItem)
        
        topItem = mediaitem.MediaItem("Top 50", "topItems")
        topItem.icon = self.icon
        items.append(topItem)
        
        return items
    
    #==============================================================================
    def ProcessFolderList(self, item):
        url = item.url
        logFile.info('starting ParseFolder for %s', url)
        items = []
        # See what action to undertake
        try:
            # check if we need to search
            if url == "searchSite":
                return self.SearchSite()
            elif url == "newItems":
                return self.NewItems()
            elif url == "popularItems":
                return self.PopularItems()
            elif url == "tipItems":
                return self.TipItems()
            elif url == "topItems":
                return self.TopItems()                            
            else:
                return chn_nos.Channel.ProcessFolderList(self, item)
        except:
            logFile.error("Cannot process folderlist for special NOS links", exc_info=True)
    
    #============================================================================== 
    def TopItems(self):
        """
            Gets the top 50 items
        """
        #check for cookie:
        logFile.info("Checking for NOS cookies.")
        if uriHandler.CookieCheck('UGSES') and uriHandler.CookieCheck('CheckUGCookie'):# and uriHandler.CookieCheck('quuid'):
            logFile.info("Cookies found. Continuing")
        else:
            logFile.info("No cookies found. Opening main site")
            temp = uriHandler.Open(self.baseUrl, proxy=self.proxy)
    
        items = []
        data = uriHandler.Open("http://oud.uitzendinggemist.nl/index.php/top50", proxy=self.proxy)
        results = common.DoRegexFindAll('<td style=[^>]+><a href="/index.php/aflevering(\?aflID=\d+)&amp;md5=[^"]+">([^<]+)</a></td>\W+<td align="right">(\d+)-(\d+)-(\d+)</td>', data)
        logFile.debug("Adding %s top50 items", len(results))
        
        for result in results:
            tmp = mediaitem.MediaItem(result[1], htmlentityhelper.HtmlEntityHelper.StripAmp(result[0]))
            tmp.icon = self.icon
            tmp.SetDate(result[4], result[3], result[2])
            tmp.type = 'video'
            tmp.thumb = self.noImage
            items.append(tmp)
        
        return items
    
    #============================================================================== 
    def TipItems(self):
        """
            Filters the tips from oud.uitzendinggemist.nl
        """
        items = []
        data = uriHandler.Open("http://oud.uitzendinggemist.nl/", proxy=self.proxy)
        selectedData = common.DoRegexFindAll("<!--<h1>Eerdere tips van Uitzendinggemist</h1>([\W\w]+)<!--// eerdere tips van uitzendinggemist -->", data)            
        if len(selectedData) > 0:
            data = selectedData[0]
            results = common.DoRegexFindAll("<a href=\"http://player.omroep.nl/(\?aflID=\d+)\" [^>]+>([^<]+)</a>", data)
            for result in results:
                tmp = mediaitem.MediaItem(result[1], htmlentityhelper.HtmlEntityHelper.StripAmp(result[0]))
                tmp.icon = self.icon
                tmp.thumb = self.noImage
                tmp.type = 'video'
                items.append(tmp)
        return items
    
    #============================================================================== 
    def NewItems(self):
        """ 
            Filters the correct data from oud.uitzendinggemist.nl page and calls
        """
        items = []
        data = uriHandler.Open("http://oud.uitzendinggemist.nl/", proxy=self.proxy)
        logFile.debug(data)
        selectedData = common.DoRegexFindAll("Meer nieuwe([\w\W]+)<!--// options -->", data)
        if len(selectedData) > 0:
            data = selectedData[0]
            logFile.debug(data)
            results = common.DoRegexFindAll("<a href=\"/index.php/aflevering(\?aflID=\d+)&amp;md5=[0-9a-f]+\"[^>]+>([^/]+)</a>\W+<a href=\"[^>]+>\(((\d+):(\d+)|gisteren)\)</a>", data)
            for result in results:
                tmp = mediaitem.MediaItem(result[1], htmlentityhelper.HtmlEntityHelper.StripAmp(result[0]))
                
                now = datetime.date.today()                    
                if result[2] == "gisteren":
                    now = now - datetime.timedelta(1)
                    tmp.SetDate(now.year, now.month, now.day)
                else:
                    tmp.SetDate(now.year, now.month, now.day, result[3], result[4],0)
                
                tmp.thumb = self.noImage
                tmp.icon = self.icon
                tmp.type = 'video'
                items.append(tmp)
        return items
    
    #============================================================================== 
    def PopularItems(self):
        """
            Filters the NewItems from oud.uitzendinggemist.nl
        """
        items = []
        data = uriHandler.Open("http://oud.uitzendinggemist.nl/", proxy=self.proxy)
        selectedData = common.DoRegexFindAll("<thead id=\"tooltip_populair\"([\w\W]+)<script type=\"text/javascript\">", data)            
        if len(selectedData) > 0:
            data = selectedData[0]
            results = common.DoRegexFindAll("<td><a href=\"/index.php/aflevering(\?aflID=\d+)&amp;md5=[0-9a-f]+\">([^<]+)</a></td>\W+<td [^>]+>(\d+)-(\d+)-(\d+)</td>", data)
            for result in results:
                tmp = mediaitem.MediaItem(result[1], htmlentityhelper.HtmlEntityHelper.StripAmp(result[0]))
                tmp.SetDate(result[4], result[3], result[2])
                tmp.icon = self.icon
                tmp.type = 'video'
                items.append(tmp)
        return items        
    
    #============================================================================== 
    def SearchSite(self, url=None):
        """ 
        accepts an url and returns an list with items of type CListItem
        Items have a name and url. 
        """

        items = []
        
        #check for cookie:
        logFile.info("Checking for NOS cookies.")
        if uriHandler.CookieCheck('UGSES') and uriHandler.CookieCheck('CheckUGCookie'):# and uriHandler.CookieCheck('quuid'):
            logFile.info("Cookies found. Continuing")
        else:
            logFile.info("No cookies found. Opening main site")
            temp = uriHandler.Open(self.baseUrl, proxy=self.proxy)
    
        keyboard = xbmc.Keyboard('')
        keyboard.doModal()
        if (keyboard.isConfirmed()):
            needle = keyboard.getText()
            if len(needle)<4:
                dialog = xbmcgui.Dialog()
                dialog.ok("Uitzendinggemist","Geen geldig zoekopdracht. Een zoekopdracht\nheeft minimaal 4 characters.")
                return
            #get only first one
            logFile.info("Searching NOS for needle: "+needle)
            data = uriHandler.Open("http://oud.uitzendinggemist.nl/index.php/search",params="searchitem=&qs_uitzending="+needle+"&titel=&dag=&net_zender=&omroep=&genre=", proxy=self.proxy)
            
            #resultSet = common.DoRegexFindAll('<a class="title" href="/index.php/search\?([^"]+)&sq=[^<]+">([^<]+)(<span[^>]+>)*([^<]+)(</span>)*</a></td>', data)
            resultSet = common.DoRegexFindAll('<a class="title" href="/index.php/search\?([^"]+)&sq=[^<]+">([^<]*)(<span[^>]+>)*([^<]*)(</span>)*([^<]*)</a></td>', data)
            
            for item in resultSet: 
                logFile.debug(item)
                name = ""
                for part in item[1:]:
                    if not part.find(">") > 0:
                        name = "%s%s" % (name, part)
                    
                tmp = mediaitem.MediaItem(name, self.baseUrl + "/index.php/serie?" + htmlentityhelper.HtmlEntityHelper.StripAmp(item[0]))
                tmp.icon = self.folderIcon
                tmp.thumb = self.noImage
                tmp.description = name
                items.append(tmp)
        
            #because lists are downloaded according to date (else some programs will be missing), a sort on name is performed.
            items.sort()
    
        else:
            logFile.info('user canceled search')
                    
        return items