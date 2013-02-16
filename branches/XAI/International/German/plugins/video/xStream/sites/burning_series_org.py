import logger
from resources.lib.gui.gui import cGui
from resources.lib.util import cUtil
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from xbmc import log
from xbmc import LOGDEBUG
from xbmc import LOGERROR

SITE_IDENTIFIER = 'burning_series_org'
SITE_NAME = 'Burning-Series.to'

URL_MAIN = 'http://www.burning-series.to'
URL_SERIES = 'http://www.burning-series.to/andere-serien'
URL_ZUFALL = 'http://www.burning-series.to/zufall'
def load():
    log("Load %s" % SITE_NAME)

    sSecurityValue = __getSecurityCookieValue()
    #__initSiteLanguage(sSecurityValue)
  
    oGui = cGui()
    
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setFunction('showAllSeries')
    oGuiElement.setTitle("Alle Serien")

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SERIES)
    oOutputParameterHandler.addParameter("securityCockie", sSecurityValue)
    oGui.addFolder(oGuiElement, oOutputParameterHandler)
    
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setFunction('showHosters')
    oGuiElement.setTitle("Zuf\xe4llige Episode")

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_ZUFALL)
    oGui.addFolder(oGuiElement, oOutputParameterHandler)
    
    oGui.setEndOfDirectory()
 
def __getSecurityCookieValue():
  oRequestHandler = cRequestHandler(URL_MAIN)
  sHtmlContent = oRequestHandler.request()

  sPattern = "<HTML><HEAD><SCRIPT language=\"javascript\" src=\"([^\"]+)\"></SCRIPT></HEAD><BODY onload=\"scf\('(.*?)'\+'(.*?)','/'\);\"></BODY></HTML>"

  log(sPattern)
  oParser = cParser()
  aResult = oParser.parse(sHtmlContent, sPattern)
  log(URL_MAIN + " : " + sHtmlContent)
  if aResult[0] == False:
    log("Can't find script file for cookie", LOGDEBUG)
    return False

  sScriptFile = URL_MAIN + str(aResult[1][0][0])
  sHashSnippet = str(aResult[1][0][1])+str(aResult[1][0][2])

  log("scriptfile: %s" % sScriptFile, LOGDEBUG)

  oRequestHandler = cRequestHandler(sScriptFile)
  oRequestHandler.addHeaderEntry('Referer', 'http://burning-series.to/')
  oRequestHandler.addHeaderEntry('Accept', '*/*')
  oRequestHandler.addHeaderEntry('Host', 'burning-series.to')
  sHtmlContent = oRequestHandler.request()

  sPattern = 'escape\(hsh \+ "(.+?)"\)' #escape(hsh + "57f7a5b06dcfe4b83dbc68db")
  oParser = cParser()
  aResult = oParser.parse(sHtmlContent, sPattern)

  if not aResult[0]:
    log("No hash value found for the cookie", LOGDEBUG)
    return False

  sHash = aResult[1][0]
  
  sHash = sHashSnippet + sHash
  sSecurityCookieValue = "sitechrx=" + str(sHash) + ";Path=/"

  oRequestHandler = cRequestHandler(URL_MAIN + "/")
  oRequestHandler.addHeaderEntry("Cookie", sSecurityCookieValue)
  oRequestHandler.request()

  log("Token: %s" % sSecurityCookieValue, LOGDEBUG)

  return sSecurityCookieValue
  

def __createMenuEntry(oGui, sFunction, sLabel, sUrl):
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setFunction(sFunction)
    oGuiElement.setTitle(sLabel)
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', sUrl)
    oGui.addFolder(oGuiElement, oOutputParameterHandler)
    
    
def showAllSeries():
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    __showAllSeries(sUrl)

def __showAllSeries(sUrl):
    oGui = cGui()    
    
    oInputParameterHandler = cInputParameterHandler()
    sSecurityValue = oInputParameterHandler.getValue('securityCockie')
	
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('Cookie', sSecurityValue)
    oRequestHandler.addHeaderEntry('Referer', 'http://burning-series.to/')
    sHtmlContent = oRequestHandler.request();
	
    sPattern = '<ul id="serSeries">(.*?)</ul>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        sHtmlContent = aResult[1][0]

        sPattern = '<li><a href="([^"]+)">(.*?)</a></li>'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
             for aEntry in aResult[1]:
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_IDENTIFIER)
                oGuiElement.setFunction('showSeasons')
                sTitle = aEntry[1].replace('&amp;','&').replace('&#039;','\'')
                oGuiElement.setTitle(sTitle)

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + '/' + str(aEntry[0]))
                oOutputParameterHandler.addParameter("securityCockie", sSecurityValue)
                oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

    
def showSeasons():
    oGui = cGui()
	
    oInputParameterHandler = cInputParameterHandler()
    sSecurityValue = oInputParameterHandler.getValue('securityCockie')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('Cookie', sSecurityValue)
    oRequestHandler.addHeaderEntry('Referer', 'http://burning-series.to/')
    sHtmlContent = oRequestHandler.request();
	

    sPattern = '<ul class="pages">(.*?)</ul>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)    
    if (aResult[0] == True):
        sHtmlContent = aResult[1][0]

        sPattern = '<a href="([^"]+)">(.*?)</a>'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
             for aEntry in aResult[1]:
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_IDENTIFIER)
                oGuiElement.setFunction('showSeries')
                oGuiElement.setTitle('Staffel ' + str(aEntry[1]))

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + '/' + str(aEntry[0]))
                oOutputParameterHandler.addParameter("securityCockie", sSecurityValue)
                oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSeries():
    oGui = cGui()
	
    oInputParameterHandler = cInputParameterHandler()
    sSecurityValue = oInputParameterHandler.getValue('securityCockie')
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('Cookie', sSecurityValue)
    oRequestHandler.addHeaderEntry('Referer', 'http://burning-series.to/')
    sHtmlContent = oRequestHandler.request();


    sPattern = '<table>(.*?)</table>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        sHtmlContent = aResult[1][0]
        
        sPattern = '<td>([^<]+)</td>\s*<td>\s*<a href="([^"]+)"><strong>(.*?)</strong>.*?<span lang="en">(.*?)</span></a>'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
             for aEntry in aResult[1]:
                sNumber = str(aEntry[0]).strip()
                sTitleGerman = str(aEntry[2])
                sTitleEnglish = str(aEntry[3])
                
                sTitle = sNumber
                if sTitleGerman != '':
                    sTitle = sTitle + ' - ' + sTitleGerman
                elif sTitleEnglish != '':
                    sTitle = sTitle + ' - ' + sTitleEnglish
                
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_IDENTIFIER)
                oGuiElement.setFunction('showHosters')
                oGuiElement.setTitle(sTitle)

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + '/' + str(aEntry[1]))
                oOutputParameterHandler.addParameter("securityCockie", sSecurityValue)
                oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def __createInfo(oGui, sHtmlContent):
    sPattern = '<meta name="description" lang="de" content="([^"]+)"\s*/>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sDescription = aEntry.strip().replace('&quot;','"')
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            sMovieTitle = __getMovieTitle(sHtmlContent)
            oGuiElement.setTitle('info (press Info Button)')
            oGuiElement.setFunction('dummyFolder')
            oGuiElement.setDescription(sDescription)
            oGui.addFolder(oGuiElement)

def dummyFolder():
    oGui = cGui()
    oGui.setEndOfDirectory()
            
def showHosters():
    oGui = cGui()
	
    oInputParameterHandler = cInputParameterHandler()
    sSecurityValue = oInputParameterHandler.getValue('securityCockie')	
    sUrl = oInputParameterHandler.getValue('siteUrl')
    
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('Cookie', sSecurityValue)
    oRequestHandler.addHeaderEntry('Referer', 'http://burning-series.to/')
    sHtmlContent = oRequestHandler.request();    
    
    __createInfo(oGui, sHtmlContent)
    
    sPattern = '<h3>Hoster dieser Episode(.*?)</ul>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        sHtmlContent = aResult[1][0]

        sPattern = '<a href="([^"]+)">.*?<span class=\"icon ([^"]+)"></span> ([^<]+?)</a>'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
             for aEntry in aResult[1]:
                oHoster = cHosterHandler().getHoster2(str(aEntry[1]).lower())
                if (oHoster != False):
                    oGuiElement = cGuiElement()
                    oGuiElement.setSiteName(SITE_IDENTIFIER)
                    oGuiElement.setFunction('getHosterUrlandPlay')
                    oGuiElement.setTitle(str(aEntry[2]))

                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + '/' + str(aEntry[0]))
                    oOutputParameterHandler.addParameter('hosterName', oHoster.getPluginIdentifier())
                    oOutputParameterHandler.addParameter("securityCockie", sSecurityValue)
                    oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def __getMovieTitle(sHtmlContent):
    sPattern = '</ul><h2>(.*?)<small id="titleEnglish" lang="en">(.*?)</small>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
	for aEntry in aResult[1]:
	    return str(aEntry[0]).strip() + ' - ' + str(aEntry[1]).strip()

    return False

def getHosterUrlandPlay():
    oGui = cGui()
	
    oInputParameterHandler = cInputParameterHandler()
    sSecurityValue = oInputParameterHandler.getValue('securityCockie')	
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sHoster = oInputParameterHandler.getValue('hosterName')
   
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('Cookie', sSecurityValue)
    oRequestHandler.addHeaderEntry('Referer', 'http://burning-series.to/')
    sHtmlContent = oRequestHandler.request();
	
    
    sTitle = __getMovieTitle(sHtmlContent)

    sPattern = '<div id="video_actions">.*?<a href="([^"]+)">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        sStreamUrl = aResult[1][0]
        oHoster = cHosterHandler().getHoster(sHoster)
        if (sTitle != False):
            oHoster.setFileName(sTitle)
        cHosterGui().showHosterMenuDirect(oGui, oHoster, sStreamUrl)
        oGui.setEndOfDirectory()
        return

    oGui.setEndOfDirectory()


