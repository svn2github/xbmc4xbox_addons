from resources.lib.handler.hosterHandler import cHosterHandler
from hosters.hoster import iHoster

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Stream2k.com'
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
        return 'stream2k'

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True
    
    def getPattern(self):
        return '<file>(.*?)</file>';

    def getHosterLinkPattern(self):
        return '<param name="flashvars" value="config=(http://.*?stream2k.com/[^"]+)"'
    
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