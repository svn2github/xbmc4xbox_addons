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
import xbmc, xbmcgui
import urllib, urllib2

SITE_IDENTIFIER = 'serienjunkies_org'
SITE_NAME = 'Serienjunkies.org'

URL_MAIN = 'http://serienjunkies.org'

def load():
    __showCharacters(URL_MAIN)
    
def __createMenuEntry(oGui, sFunction, sLabel, sUrl):
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setFunction(sFunction)
    oGuiElement.setTitle(sLabel)
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', sUrl)
    oGui.addFolder(oGuiElement, oOutputParameterHandler)

def showCharacters():
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    __showCharacters(sUrl)    
    
def __showCharacters(sUrl):
    oGui = cGui()    
    
    sHtmlContent = cRequestHandler(sUrl).request();
    sPattern = '<div class="apz_container">(.*?)</div>'
    aResult = cParser().parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        sHtmlContent = aResult[1][0]
        sPattern = '<a class="letter"\s*href="([^"]+)">([^<]+)</a>'
        aResult = cParser().parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
             for aEntry in aResult[1]:
                newUrl = str(aEntry[0]).strip().replace('&amp;','&')
                if not newUrl.startswith('http'):
                    newUrl = URL_MAIN + newUrl
                sTitle = aEntry[1].replace('&amp;','&').replace('&#039;','\'')

                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_IDENTIFIER)
                oGuiElement.setFunction('showSeries')
                oGuiElement.setTitle(sTitle)

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', newUrl)
                
                oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSeries():
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    __showSeries(sUrl)

def __showSeries(sUrl):  
    oGui = cGui()    
    log('neu: ' + sUrl)
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    sPattern = '<ul>(.*?)</ul>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        sHtmlContent = aResult[1][0]
        sPattern = '<li>\s*<a href="([^"]+)">([^<]+)</a>\s*</li>'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
             for aEntry in aResult[1]:
                newUrl = str(aEntry[0]).strip().replace('&amp;','&')
                if not newUrl.startswith('http'):
                    newUrl = URL_MAIN + newUrl

                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_IDENTIFIER)
                oGuiElement.setFunction('showSeasons')
                sTitle = aEntry[1].replace('&amp;','&').replace('&#039;','\'')
                oGuiElement.setTitle(sTitle)

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', newUrl)
                oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSeasons():
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    __showSeasons(sUrl)
    
def __showSeasons(sUrl):
    oGui = cGui()
    oParser = cParser()
    
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addParameters('','')
    sHtmlContent = oRequestHandler.request();
    
    # get Series ID
    #$.getJSON('http://serienjunkies.org/media/ajax/getStreams.php', {s:seasonNum,ids:'0084967'}, function(data){
    sPattern = '{s:seasonNum,ids:\'([^\']+)\'}'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if not aResult[0] == True:
        oGui.showInfo('Info', 'Keine Streams vorhanden',3)
        return
    sSeriesId = aResult[1][0]    
    if sSeriesId.find(',') > -1:
        sSeriesId = sSeriesId.split(',')[1]
    sPattern = '<select id="season_list">(.*?)</select>'
    aResult = cParser().parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        sSeasons = aResult[1][0]
        sPattern = '<option value="([^"]+)"[^>]*>([^<]+)</option>'
        aResult = cParser().parse(sSeasons, sPattern)
        for aEntry in aResult[1]:
            sSeasonId = aEntry[0]
            sTitle = aEntry[1]
            
            sUrl = 'http://serienjunkies.org/media/ajax/getStreams.php?s=' + sSeasonId + '&ids=' + sSeriesId
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setFunction('showEpisodes')
            oGuiElement.setTitle(sTitle)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sSeasonId', sSeasonId)
            oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()
    
    
def showEpisodes():
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    __showEpisodes(sUrl)
    
def __showEpisodes(sUrl):
    oGui = cGui()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    #id     |       title       |       language        |       episode     |       hosters
    sPattern = '\["([^"]+)","([^"]+)","([^"]+)","([^"]+)",{([^}]+)}'
    aResult = cParser().parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
         for aEntry in aResult[1]:
            sEpisodeId = aEntry[0]
            sTitle = aEntry[1].replace('&amp;','&').replace('&#039;','\'')
            sLanguage = aEntry[2]
            sEpisode = aEntry[3]
            sHosters = aEntry[4]
            
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setFunction('showHosters')
            oGuiElement.setTitle(sTitle)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sTitle', sTitle)
            oOutputParameterHandler.addParameter('sHosters', sHosters)
            
            oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()
    
            
def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sTitle = oInputParameterHandler.getValue('sTitle')
    sHosters = oInputParameterHandler.getValue('sHosters')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();    
    
    # hosterName:hosterId
    sPattern = '"([^"]+)":"([^"]+)"'
    oParser = cParser()
    aResult = oParser.parse(sHosters, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sHoster = aEntry[0]
            sHosterId = aEntry[1]
            
            sUrl = 'http://crypt2.be/file/' + sHosterId
            sThumbnail = 'http://serienjunkies.org/media/img/stream/'+sHoster+'.png'
            
            oHoster = cHosterHandler().getHoster2(sHoster.lower())
            if (oHoster != False):
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_IDENTIFIER)
                oGuiElement.setFunction('getHosterUrlandPlay')
                oGuiElement.setTitle(oHoster.getDisplayName())
                oGuiElement.setThumbnail(sThumbnail)

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('hosterName', oHoster.getPluginIdentifier())
                oOutputParameterHandler.addParameter('sTitle', sTitle)
                oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def checkIfCaptchaRequired(htmlContent):
    captchaPattern = 'recaptcha'
    captchaParser = cParser()
    captchaResult = captchaParser.parse(htmlContent, captchaPattern)
    return captchaResult[0]


def getHosterUrlandPlay():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sHoster = oInputParameterHandler.getValue('hosterName')
    sTitle = oInputParameterHandler.getValue('sTitle')
   
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    if (checkIfCaptchaRequired(sHtmlContent)):
        iframePattern = '<iframe [^>]*src=["|\']([^"|\']+)'
        iframeParser = cParser()
        iframeResult = iframeParser.parse(sHtmlContent, iframePattern)

        captchaRequestHandler = cRequestHandler(iframeResult[1][0])
        captchaHtmlContent = captchaRequestHandler.request();
        captchaPattern = '<img [^>]*src=["|\']([^"|\']+)'
        captchaParser = cParser()
        captchaResult = captchaParser.parse(captchaHtmlContent, captchaPattern)
        
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(SITE_IDENTIFIER)
        oGuiElement.setTitle('Captcha code required, press here ...')
        oGuiElement.setFunction('showKeyboardForCaptchaInput')
        oGuiElement.setThumbnail('http://www.google.com/recaptcha/api/' + str(captchaResult[1][0]))
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('hosterName', sHoster)
        oOutputParameterHandler.addParameter('sTitle', sTitle)
        challengeString = str(captchaResult[1][0]).replace('image?c=','')
        oOutputParameterHandler.addParameter('captchaImageChallenge', challengeString)
        oOutputParameterHandler.addParameter('iframeUrl', str(iframeResult[1][0]))
        oGui.addFolder(oGuiElement, oOutputParameterHandler)
        oGui.setEndOfDirectory()
        return
    else:
        sPattern = '<iframe id="iframe" src="([^"]+)"'
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
        else:
            sPattern = '<param name="movie" value="([^"]+)"'
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

def showKeyboardForCaptchaInput():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sHoster = oInputParameterHandler.getValue('hosterName')
    sTitle = oInputParameterHandler.getValue('sTitle')
    captchaImageChallenge = oInputParameterHandler.getValue('captchaImageChallenge')
    iframeUrl = oInputParameterHandler.getValue('iframeUrl')
    kb = xbmc.Keyboard('', 'Type the letters in the captcha image', False)
    kb.doModal()
    if (kb.isConfirmed()):
        userInput = kb.getText()
        url = iframeUrl
        values = {'recaptcha_challenge_field' : captchaImageChallenge, 'recaptcha_response_field' : userInput }
        data = urllib.urlencode(values)
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        the_page = response.read()
        sPattern = '<textarea rows="5" cols="100">([^"]+)</textarea>'
        oParser = cParser()
        aResult = oParser.parse(the_page, sPattern)
        
        if (aResult[0] == True):
            captchaKey = aResult[1][0]
            values = {'recaptcha_challenge_field' : captchaKey, 'recaptcha_response_field' : 'manual_challenge' }
            data = urllib.urlencode(values)
            req = urllib2.Request(sUrl, data)
            response = urllib2.urlopen(req)
            the_page = response.read()
            if (checkIfCaptchaRequired(the_page) == False):
                getHosterUrlandPlay()
        else:
            xbmcgui.Dialog().ok("Text does not match captcha image!", "To try again, close this box and then: \n Press backspace twice, and reselect your video.")
