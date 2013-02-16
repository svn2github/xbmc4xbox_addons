from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from hosters.hoster import iHoster
from base64 import b64decode
from xbmc import log
from xbmc import LOGERROR
from binascii import unhexlify

try:
  from json import loads
except ImportError:
  from simplejson import loads

class cHoster(iHoster):

  SETTINGS_URL = "http://www.videozer.com/player_control/settings.php?v="

  def __init__(self):
    self.__sDisplayName = 'VideoZer.com'
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
    return 'videozer'

  def isDownloadable(self):
    return True

  def isJDownloaderable(self):
    return True

  def getPattern(self):
    return 'flashvars.file=\"([^\"]+)\"';

  def setUrl(self, sUrl):
    self.__sUrl = sUrl

  def checkUrl(self, sUrl):
    return True

  def getUrl(self):
    return self.__sUrl

  def getMediaLink(self):
    return self.__getMediaLinkForGuest()

  def __getMediaLinkForGuest(self):
    log("Generate direct media link from %s" % self.__sUrl)

    # Get the video id from the link
    sPattern = 'http://(?:www.)?videozer.com/(?:embed|video)?/(.*?)$'
    oParser = cParser()
    aResult = oParser.parse(self.__sUrl, sPattern)

    if not aResult[0]:
      log("The link does not contain a video id.", LOGERROR)
      return [False, ""]

    oRequest = cRequestHandler(cHoster.SETTINGS_URL + aResult[1][0])
    sHtmlContent = oRequest.request()

    # Try to load the datas from the sHtmlContent. This data should be json styled.
    aData = loads(sHtmlContent)
	
    # Decode the link from the json data settings.  
    spn_ik = unhexlify(self.__decrypt(aData["cfg"]["login"]["spen"], aData["cfg"]["login"]["salt"], 950569)).split(';')
    spn = spn_ik[0].split('&')
    ik = spn_ik[1]
	
    for item in ik.split('&') :
        temp = item.split('=')
        if temp[0] == 'ik' : 
            key = self.__getKey(temp[1])

    sLink = ""
    for item in spn :
        item = item.split('=')
        if(int(item[1])==1):
            sLink = sLink + item[0]+ '=' + self.__decrypt(aData["cfg"]["info"]["sece2"], aData["cfg"]["environment"]["rkts"], key) + '&'  #decrypt32byte
        elif(int(item[1]==2)):
            sLink = sLink + item[0]+ '=' + self.__decrypt(aData["cfg"]["ads"]["g_ads"]["url"],aData["cfg"]["environment"]["rkts"], key) + '&'	
        elif(int(item[1])==3):
            sLink = sLink + item[0]+ '=' + self.__decrypt(aData["cfg"]["ads"]["g_ads"]["type"],aData["cfg"]["environment"]["rkts"], key,26,25431,56989,93,32589,784152) + '&'	
        elif(int(item[1])==4):
            sLink = sLink + item[0]+ '=' + self.__decrypt(aData["cfg"]["ads"]["g_ads"]["time"],aData["cfg"]["environment"]["rkts"], key,82,84669,48779,32,65598,115498) + '&'
        elif(int(item[1])==5):
            sLink = sLink + item[0]+ '=' + self.__decrypt(aData["cfg"]["login"]["euno"],aData["cfg"]["login"]["pepper"], key,10,12254,95369,39,21544,545555) + '&'
        elif(int(item[1])==6):
            sLink = sLink + item[0]+ '=' + self.__decrypt(aData["cfg"]["login"]["sugar"],aData["cfg"]["ads"]["lightbox2"]["time"], key,22,66595,17447,52,66852,400595) + '&'
    sLink = sLink + "start=0"
	
    sMediaLink = b64decode(aData["cfg"]["quality"][0]["u"]) + '&' + sLink
    log("Generated direct media link %s" % sMediaLink)

    return [True, sMediaLink]
                      
  def __decrypt(self, str, k1, k2, p4 = 11, p5 = 77213, p6 = 81371, p7 = 17, p8 = 92717, p9 = 192811):
        tobin = self.hex2bin(str,len(str)*4)
        tobin_lenght = len(tobin)
        keys = []
        index = 0
		
        while (index < tobin_lenght*3):
            k1 = ((int(k1) * p4) + p5) % p6
            k2 = ((int(k2) * p7) + p8) % p9
            keys.append((int(k1) + int(k2)) % tobin_lenght)
            index += 1

        index = tobin_lenght*2

        while (index >= 0):
            val1 = keys[index]
            mod  = index%tobin_lenght
            val2 = tobin[val1]
            tobin[val1] = tobin[mod]
            tobin[mod] = val2
            index -= 1

        index = 0
        while(index < tobin_lenght):
            tobin[index] = int(tobin[index]) ^ int(keys[index+(tobin_lenght*2)]) & 1
            index += 1
            decrypted = self.bin2hex(tobin)
        return decrypted
	
  def hex2bin(self,val,fill):
        bin_array = []
        string =  self.bin(int(val, 16))[2:].zfill(fill)
        for value in string:
            bin_array.append(value)
        return bin_array

  def bin2hex(self,val):
        string = str("")
        for char in val:
            string+=str(char)
        return "%x" % int(string.replace(' ',''), 2)
		
  def bin(self, x):
		#bin(number) -> string
		#Stringifies an int or long in base 2.
        if x < 0: return '-' + bin(-x)
        out = []
        if x == 0: out.append('0')
        while x > 0:
            out.append('01'[x & 1])
            x >>= 1
            pass
        try: return '0b' + ''.join(reversed(out))
        except NameError, ne2: out.reverse()
        return '0b' + ''.join(out)
  
  
  def __getKey(self, nbr):
        if nbr == '1': return 215678
        elif nbr == '2': return 516929
        elif nbr == '3': return 962043
        elif nbr == '4': return 461752
        elif nbr == '5': return 141994
        else: return False