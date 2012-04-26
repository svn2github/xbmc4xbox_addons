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
import common

logFile = sys.modules['__main__'].globalLogFile

class TagHelperBase:
    """Base class that holds the mutual code for XMLHelper and HTMLHelper"""
        
    def __init__(self, data):
        """Creates a class object with HTML <data>
        
        Arguments:
        data : string - HTML data to parse
        
        """
        
        self.data = data
    
    def GetTagAttribute(self, tag, *args, **kwargs):
        """Gets the content of an specific attribute of an HTML <tag>
        
        Arguments:
        tag    : string     - name of tag to search for.
        **args : dictionary - each argument is interpreted as a html 
                              attribute. 'cls' is translated to class 
                              attribute. The attribute with value None 
                              is retrieved.
        
        Keyword Arguments:
        firstOnly : [opt] boolean - only return the first result. Default: True
        
        Returns:
        The content of the attribute of the found tag. If no match is found 
        an empty string is returned.
        
        Example: ('div', {'cls':'test'}, {'id':'divTest'}, {'width':None}, {'alt':'test'}) will match 
        <div class="test" id="divTest" width="20" alt="test">...content...</div> and 
        will return 20. 
        
        """
        
        firstOnly = True
        if kwargs.keys().count("firstOnly") > 0:
            firstOnly = kwargs["firstOnly"]
            logFile.debug("Setting 'firstOnly' to '%s'", firstOnly)
            
        htmlRegex = '<%s' % (tag,)
        
        #logFile.debug(args)
        for arg in args:
            name = arg.keys()[0]
            value = arg[arg.keys()[0]]
            #logFile.debug("Name: %s, Value: %s", name, value)
            
            # to keep working with older versions where class could not be passed
            if name == "cls":
                name = "class"
            
            if value is None:
                htmlRegex = htmlRegex + '[^>]*%s\W*=\W*["\']([^"\']+)["\']' % (name,)
            else:
                htmlRegex = htmlRegex + '[^>]*%s\W*=\W*["\']%s["\']' % (name, value)
                
        htmlRegex = htmlRegex + "[^>]*>"
        #logFile.debug("HtmlRegex = %s", htmlRegex)
        #logFile.debug(self.data)
        
        result = common.DoRegexFindAll(htmlRegex , self.data)
        #logFile.debug(result)
        
        if len(result) > 0:
            if firstOnly:
                return result[0].lstrip()
            else:
                return result
        else:
            return ""
        