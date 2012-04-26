#===============================================================================
# LICENSE XOT-Framework - CC BY-NC-ND
#===============================================================================
# This work is licenced under the Creative Commons 
# Attribution-Non-Commercial-No Derivative Works 3.0 Unported License. To view a 
# copy of this licence, visit http://creativecommons.org/licenses/by-nc-nd/3.0/ 
# or send a letter to Creative Commons, 171 Second Street, Suite 300, 
# San Francisco, California 94105, USA.
#===============================================================================
import time
import sys
import os

import common
from config import Config
from helpers import htmlentityhelper
from helpers import encodinghelper

#===============================================================================
# Make global object available
#===============================================================================
logFile = sys.modules['__main__'].globalLogFile
uriHandler = sys.modules['__main__'].globalUriHandler

class SubtitleHelper:
    """Helper class that is used for handling subtitle files."""
    
    def __init__(self):
        """Create a class instance. This is not allowed, due to only static
        methods.
        
        """
        
        raise Exception("Not allowed to create instance of SubtitleHelper")
        pass
    
    @staticmethod
    def DownloadSubtitle(url, fileName="", format='sami'):
        """Downloads a SAMI and stores the SRT in the cache folder
        
        Arguments:
        url      : string - URL location of the SAMI file
        
        Keyword Arguments:
        fileName : string - Filename to use to store the subtitle in SRT format.
                            if not specified, an MD5 hash of the URL with .xml
                            extension will be used
        format : string   - defines the source format. Defaults to Sami. 
        
        Returns:
        The full patch of the cached SRT file.
        
        """
        
        if fileName == "":
            logFile.debug("No filename present, generating filename using MD5 hash of url.")
            fileName = "%s.xml" % (encodinghelper.EncodingHelper.EncodeMD5(url),)
        
        srt = ""
        try:
            #logFile.debug("Opening Subtitle URL")
            raw = uriHandler.Open(url)
            
            if raw == "":
                logFile.warning("Empty Subtitle path found. Not setting subtitles.")
                return ""
            
            if format.lower() == 'sami':
                srt = SubtitleHelper.__ConvertSamiToSrt(raw)
            elif format.lower() == 'srt':
                srt = raw
            elif format.lower() == 'ttml':
                srt = SubtitleHelper.__ConvertTtmlToSrt(raw)
            elif format.lower() == 'dcsubtitle':
                srt = SubtitleHelper.__ConvertDCSubtitleToSrt(raw)
            else:
                error = "Uknown subtitle format: %s" % (format,)
                raise NotImplementedError(error)
                
            localCompletePath = os.path.join(Config.cacheDir, fileName)
            
            if os.path.exists(localCompletePath):
                return localCompletePath
            
            f = open(localCompletePath, 'w')
            f.write(srt)
            f.close()
            logFile.info("Saved SRT as %s", localCompletePath)
            return localCompletePath
        except:
            logFile.error("Error handling Subtitle file: [%s]", srt, exc_info=True)
            return ""                
    
    @staticmethod
    def __ConvertDCSubtitleToSrt(dcSubtitle):
        """Converts DC Subtitle format into SRT format:
        
        Arguments:
        dcSubtitle : string - DC Subtitle subtitle format
        
        Returns:
        SRT formatted subtitle:
        
        Example:
            <Subtitle SpotNumber="1" TimeIn="00:00:01:220" TimeOut="00:00:04:001" FadeUpTime="20" FadeDownTime="20">
              <Text Direction="horizontal" HAlign="center" HPosition="0.0" VAlign="bottom" VPosition="6.0">Line 1</Text>
            </Subtitle>
            <Subtitle SpotNumber="2" TimeIn="00:02:07:180" TimeOut="00:02:10:040" FadeUpTime="20" FadeDownTime="20">
              <Text Direction="horizontal" HAlign="center" HPosition="0.0" VAlign="bottom" VPosition="6.0">Line 1</Text>
            </Subtitle>
            <Subtitle SpotNumber="3" TimeIn="00:02:15:190" TimeOut="00:02:17:190" FadeUpTime="20" FadeDownTime="20">
              <Text Direction="horizontal" HAlign="center" HPosition="0.0" VAlign="bottom" VPosition="14.0">Line 1</Text>
              <Text Direction="horizontal" HAlign="center" HPosition="0.0" VAlign="bottom" VPosition="6.0">Line 2</Text>
            </Subtitle>
            <Subtitle SpotNumber="4" TimeIn="00:03:23:140" TimeOut="00:03:30:120" FadeUpTime="20" FadeDownTime="20">
              <Text Direction="horizontal" HAlign="center" HPosition="0.0" VAlign="bottom" VPosition="14.0">Line 1</Text>
              <Text Direction="horizontal" HAlign="center" HPosition="0.0" VAlign="bottom" VPosition="14.0">Line 2</Text>
            </Subtitle>
        
        Returns
            1
            00:00:20,000 --> 00:00:24,400
            text    
        
        The format of the timecode is Hours:Minutes:Seconds:Ticks where a "Tick"
        is a value of between 0 and 249 and lasts 4 milliseconds. 
        
        """
    
        parseRegex = '<subtitle[^>]+spotnumber="(\d+)" timein="(\d+:\d+:\d+):(\d+)" timeout="(\d+:\d+:\d+):(\d+)"[^>]+>\W+<text[^>]+>([^<]+)</text>\W+(?:<text[^>]+>([^<]+)</text>)*\W+</subtitle>'
        parseRegex = parseRegex.replace('"', '["\']')
        subs = common.DoRegexFindAll(parseRegex, dcSubtitle)
        
        srt = ""
        i = 1
        
        decoder = encodinghelper.EncodingHelper()
        
        for sub in subs:
            try:
                #print sub
                start = "%s,%03d" % (sub[1], int(sub[2])*4)
                end = "%s,%03d" % (sub[3], int(sub[4])*4)
                text = decoder.Decode(sub[5].replace("<br />", "\n"))
                if (not sub[6] == ''):
                    text2 = decoder.Decode(sub[6].replace("<br />", "\n"))
                    text = "%s\N%s" % (text, text2)        
                text = htmlentityhelper.HtmlEntityHelper.ConvertHTMLEntities(text)
                srt = "%s\n%s\n%s --> %s\n%s\n" % (srt, i, start, end, text.strip())
                i += 1
            except:
                logFile.error("Error parsing subtitle: %s", sub, exc_info=True)        
        
        # re-encode to be able to write it
        return decoder.UnicodeEncode(srt)
    
    @staticmethod
    def __ConvertTtmlToSrt(ttml):
        """Converts sami format into SRT format:
        
        Arguments:
        ttml : string - TTML (Timed Text Markup Language) subtitle format
        
        Returns:
        SRT formatted subtitle:
        
        Example:
            1
            00:00:20,000 --> 00:00:24,400
            text        
        
        """
    
        parsRegex = '<p[^>]+begin="([^"]+)\.(\d+)"[^>]+end="([^"]+)\.(\d+)"[^>]*>([\w\W]+?)</p>'
        subs = common.DoRegexFindAll(parsRegex, ttml)
        
        srt = ""
        i = 1
        
        decoder = encodinghelper.EncodingHelper()
        
        for sub in subs:
            try:
                #print sub
                start = "%s,%s0" % (sub[0], sub[1])
                end = "%s,%s0" % (sub[2], sub[3])
                text = decoder.Decode(sub[4].replace("<br />", "\n"))        
                #text = sub[4].replace("<br />", "\n")        
                text = htmlentityhelper.HtmlEntityHelper.ConvertHTMLEntities(text)
                srt = "%s\n%s\n%s --> %s\n%s\n" % (srt, i, start, end, text.strip())
                i += 1
            except:
                logFile.error("Error parsing subtitle: %s", sub[1], exc_info=True)        
        
        # re-encode to be able to write it
        return decoder.UnicodeEncode(srt)
    
    @staticmethod
    def __ConvertSamiToSrt(sami):
        """Converts sami format into SRT format:
        
        Arguments:
        sami : string - SAMI subtitle format
        
        Returns:
        SRT formatted subtitle:
        
        Example:
            1
            00:00:20,000 --> 00:00:24,400
            text        
        
        """
        parsRegex = '<sync start="(\d+)"><p[^>]+>([^<]+)</p></sync>\W+<sync start="(\d+)">'
        subs = common.DoRegexFindAll(parsRegex, sami)
        
        if len(subs) == 0:
            parsRegex2 = '<sync start=(\d+)>\W+<p[^>]+>([^\n]+)\W+<sync start=(\d+)>'
            subs = common.DoRegexFindAll(parsRegex2, sami)
        
        srt = ""
        i = 1
        
        decoder = encodinghelper.EncodingHelper()
        
        for sub in subs:
            try:
                #print sub
                start = SubtitleHelper.__ConvertToTime(sub[0])
                end = SubtitleHelper.__ConvertToTime(sub[2])
                text = decoder.Decode(sub[1])
                text = htmlentityhelper.HtmlEntityHelper.ConvertHTMLEntities(text)
                #text = sub[1]
                srt = "%s\n%s\n%s --> %s\n%s\n" % (srt, i, start, end, text)
                i += 1
            except:
                logFile.error("Error parsing subtitle: %s", sub[1], exc_info=True)        
        
        # re-encode to be able to write it
        return decoder.UnicodeEncode(srt)
            
    @staticmethod
    def __ConvertToTime(timestamp):
        """Converts a SAMI (msecs since start) timestamp into a SRT timestamp
        
        Arguments:
        timestamp : string - SAMI timestamp
        
        Returns:
        SRT timestamp (00:04:53,920)
        
        """
        msecs = timestamp[-3:]
        secs = int(timestamp)/1000
        sync = time.strftime("%H:%M:%S", time.gmtime(secs)) + ',' + msecs
        return sync
    
