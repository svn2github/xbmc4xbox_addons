#
# Imports
#
import urllib
from xml.dom import minidom
import HTMLParser
import xbmcgui
import xbmcplugin
import sys
import time
from xbmcplugin_utils import HTTPCommunicator

#
# Main class
#
class Main:
    #
    # Init
    #
    def __init__(self):
        #
        # Settings
        #
        numberOfEntries = int( xbmcplugin.getSetting( "num_entries" ) )
        
        #
        # Get revisions...
        #
        self.getRevisions( numberOfEntries )
        
    #
    #  Get revisions...
    #
    def getRevisions(self, numberOfEntries):
        #
        # Get XML feed...
        #
        httpCommunicator = HTTPCommunicator()
        xmlText          = httpCommunicator.get( "http://redmine.exotica.org.uk/projects/xbmc4xbox/repository/xbmc4xbox/revisions.atom" )
        xmlDom           = minidom.parseString( xmlText )
        
        for node in xmlDom.getElementsByTagName("entry") :                    
            #
            # Init
            #
            developer   = ""
            pubDate     = ""
            title       = ""
            description = ""
            
            #
            # Parse entry details...
            #
            for childNode in node.childNodes:
                if childNode.nodeName == "author" :
                    for node in childNode.childNodes :
                        if node.nodeName == "name" :
                            developer = node.firstChild.data
                elif childNode.nodeName == "updated" :
                    pubDate = childNode.firstChild.data
                elif childNode.nodeName == "title" :
                    title = childNode.firstChild.data
                elif childNode.nodeName == "content" and childNode.firstChild :
                    description = self.html2text(childNode.firstChild.data)            
            
            # Title
            title = title.replace("\n", " ")
            title = title.replace("Revision ", "")
            title = title.replace(" (xbmc4xbox)", "")
            
            # Date
            datetime_elements = time.strptime(pubDate, "%Y-%m-%dT%H:%M:%SZ")
            revisionDate = "%02u-%02u-%04u" % ( datetime_elements[2], datetime_elements[1], datetime_elements[0] )
            
            # Description
            description = title[ title.find(":") + 1 : ] + '\n' + description 
                
            #
            # Create list item...
            #
            listitem = xbmcgui.ListItem( title, description, iconImage = "DefaultProgram.png" )
            listitem.setInfo( type = "Video", infoLabels = { "Title" : "%s [[COLOR=FFe2ff43]%s[/COLOR]]" % ( title, developer ), "Date" : revisionDate })
            url = "%s?action=revision-info&title=%s&date-time=%s&developer=%s&description=%s" % ( sys.argv[0], urllib.quote_plus(title), urllib.quote_plus(pubDate), urllib.quote_plus(developer), urllib.quote_plus(description) )
            xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = url, listitem=listitem, isFolder=False)
    
        #    
        # End of directory...
        #
        xbmcplugin.addSortMethod ( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_DATE )
        xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
            
    #
    # Convert HTML to readable strings...
    #
    def html2text ( self, html ):
        htmlStripper = HTMLStripper()
        htmlStripper.feed( html )
        return htmlStripper.get_fed_data()

#
# HTMLStripper class - strip HTML tags from text
#
class HTMLStripper (HTMLParser.HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    
    def handle_startendtag(self, tag, attrs):
        if tag == 'br':
            self.fed.append('\n')
                
    def handle_data(self, d):
        self.fed.append(d)
    
    def get_fed_data(self):
        return ''.join(self.fed).strip()
