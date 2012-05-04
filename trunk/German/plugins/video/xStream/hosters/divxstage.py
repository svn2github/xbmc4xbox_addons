from resources.lib.handler.hosterHandler import cHosterHandler
from hosters.hoster import iHoster

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'DivxStage.net'
        self.__sFileName = self.__sDisplayName

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'divxstage'

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self): 
        return ['type="video/divx" src="([^"]+)"', 'file=([^&]+)&', 'addVariable\("file","([^"]+)"\)']
        
    def getHosterLinkPattern(self):
        return '<a href="(http://(?:www.)?divxstage.(?:eu|net)?/video/[^"]+)"'

    def setUrl(self, sUrl):
        self.__sUrl = sUrl

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        oHosterHandler = cHosterHandler()
        return oHosterHandler.getUrl(self)
