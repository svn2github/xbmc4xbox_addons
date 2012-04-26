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

from helpers import taghelperbase

#===============================================================================
# Make global object available
#===============================================================================
logFile = sys.modules['__main__'].globalLogFile

class XmlHelper(taghelperbase.TagHelperBase):
    """Class that helps getting the content of XML nodes"""

    def GetSingleNodeContent(self, nodeTag, *args, **kwargs):
        """Retreives a single node 
        
        Arguments:
        nodeTag : string     - Name of the node to retrieve 
        args    : dictionary - Dictionary holding the node's attributes. Should
                               occur in order of appearance.
        
        Keyword Arguments:
        stripCData : Bool - If True the <![CDATA[......]]> will be removed.
        
        Returns:
        the content of the first match that is found.
        
        The args should be a dictionary: {"size": "380x285"}, {"ratio":"4:3"} 
        will find a node with <nodename size="380x285" name="test" ratio="4:3">
        
        """
        
        if kwargs.has_key("stripCData"):
            stripCData = kwargs["stripCData"]
        else:
            stripCData = False
        
        result = self.GetNodesContent(nodeTag, *args)
        if len(result) > 0:
            if stripCData:
                return XmlHelper.StripCData(result[0])
            else:
                return result[0]
        else:
            return ""
    
    def GetNodesContent(self, nodeTag, *args):
        """Retreives all nodes with nodeTag as name 
        
        Arguments:
        nodeTag : string     - Name of the node to retrieve 
        args    : dictionary - Dictionary holding the node's attributes. Should
                               occur in order of appearance.
        
        Returns:
        A list of all the content of the found nodes.
        
        The args should be a dictionary: {"size": "380x285"}, {"ratio":"4:3"} 
        will find a node with <nodename size="380x285" name="test" ratio="4:3">
        
        """
        
        regex = "<%s" % (nodeTag,)
        
        for arg in args:
            regex = regex + '[^>]*%s\W*=\W*"%s"' % (arg.keys()[0], arg[arg.keys()[0]])
            # just do one pass
        
        regex = regex + "[^>]*>([\w\W]+?)</%s>" % (nodeTag,)
        #logFile.debug("XmlRegex = %s", regex)
        
        #regex = '<%s>([^<]+)</%s>' % (nodeTag, nodeTag)
        results = common.DoRegexFindAll(regex, self.data)
        #logFile.debug(results)
        return results
    
    @staticmethod
    def StripCData(data):
        """ Strips the <![CDATA[......]]> from XML data tags 
        
        Arguments:
        data : String - The data to strip from.
        
        """
        
        #logFile.debug(data)
        #logFile.debug(data.replace("<![CDATA[","").replace("]]>",""))
        return data.replace("<![CDATA[","").replace("]]>","")
        