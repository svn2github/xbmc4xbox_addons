#===============================================================================
# LICENSE XOT-Framework - CC BY-NC-ND
#===============================================================================
# This work is licenced under the Creative Commons 
# Attribution-Non-Commercial-No Derivative Works 3.0 Unported License. To view a 
# copy of this licence, visit http://creativecommons.org/licenses/by-nc-nd/3.0/ 
# or send a letter to Creative Commons, 171 Second Street, Suite 300, 
# San Francisco, California 94105, USA.
#===============================================================================
import sys
import re

import common

#===============================================================================
# Make global object available
#===============================================================================
logFile = sys.modules['__main__'].globalLogFile

class JsonHelper:
    """Class that could help with parsing of simple JSON"""
    
    def __init__(self, data):
        """Creates a class object with HTML <data>
        
        Arguments:
        data : string - JSON data to parse
        
        """
        
        self.data = data

    @staticmethod
    def ConvertSpecialChars(text):
        """ Converts special characters in json to their Unicode equivalents.
        
        Arguments:
        test : string - the text to search for.
        
        Returns text with all the \uXXXX values replaced with their Unicode 
        characters. XXXX is considered a Hexvalue. It returns unichr(int(hex))
        
        """
        
        return re.sub("(\\\u)(\d+)", JsonHelper.__SpecialCharsHandler, text)
    
    @staticmethod   
    def __SpecialCharsHandler(match):
        """ Helper method to replace \uXXXX with unichr(int(hex))
        
        Arguments:
        match : RegexMatch - the matched element in which group(2) holds the 
                             hex value.
                             
        Returns the Unicode character corresponding to the Hex value.
        
        """
        
        hexString = "0x%s" % (match.group(2))
        print hexString
        hexValue = int(hexString, 16)
        return unichr(hexValue)        

    def GetNamedValue(self, name):
        """Returns the value of the named tag with <name>
        
        Arguments:
        name : string - name of the element which value should be returned.
        
        Returns:
        the value corresponding to the name. If no match is found an empty
        string is returned.
        
        """
        
        nodeRegex = '"%s":"([^"]+)"' % (name,)
        result = common.DoRegexFindAll(nodeRegex, self.data)
        if len(result) > 0:
            return JsonHelper.ConvertSpecialChars(result[0])
        else:
            return ""