#
# Imports
#
import os
import re
import sys
import xbmc
import xbmcgui
import xbmcplugin
import urllib
import time
import datetime
from xml.dom import minidom
from xbmcsvn_utils import HTTPCommunicator
from xbmcsvn_utils import HTML2Text
import xbmcsvn_utils

#
# Main class
#
class Main:
    #
    # Init
    #
    def __init__( self ) :
        # Constants
        self.DEBUG       = False
        
        # Parse parameters...
        params           = dict(part.split('=', 1) for part in sys.argv[ 2 ][ 1: ].split('&'))
        self.category    = params[ "category" ] 

        #
        # Get the videos...
        #
        self.getBuilds()
            
    
    #
    # Get skins...
    #
    def getBuilds( self ) :
        #
        # Init
        #
        html2text     = HTML2Text()
        os_platform   = os.environ.get("OS")

        # Xbox only (anyways)
        rss_url = "http://sshcs.com/xbmc/?mode=RSS&a=XBOX"            
        
        #
        # Get RSS feed...
        #
        try :
            httpCommunicator = HTTPCommunicator()
            xmlText          = httpCommunicator.get( rss_url )
            xmlDom           = minidom.parseString( xmlText )
        except Exception, e :
            title = "%s - %s" % ( xbmc.getLocalizedString(30000), xbmc.getLocalizedString(257).upper() )
            xbmcgui.Dialog().ok( title, rss_url, str(e) )
            return
        
        #
        # Parse XML...
        #
        for node in xmlDom.getElementsByTagName("item") :
            #
            # Init
            #
            title       = ""
            link        = ""
            pubDate     = ""
            description = ""
            
            #
            # Parse entry details...
            #
            for childNode in node.childNodes:
                if childNode.nodeName == "title" :
                    title = childNode.firstChild.data
                elif childNode.nodeName == "link" :
                    link  = childNode.firstChild.data
                elif childNode.nodeName == "pubDate" :
                    pubDate = childNode.firstChild.data
                elif childNode.nodeName == "description" :
                    description = childNode.firstChild.data

            # Title
            revision = title[ title.rfind("r") + 1 : ]
            title    = title[ : title.rfind("r") ].strip()
            title    = "%s [COLOR=FFe2ff43]r%s[/COLOR]" % ( title, revision )
            
            # Date
            date_elements = time.strptime(pubDate, "%a, %d %b %Y %H:%M:%S CST")
            date          = "%02u-%02u-%04u" % ( date_elements[2], date_elements[1], date_elements[0] )
            
            # Description
            description       = self.parseDescription( description )

            #
            # View build URL...
            #
            view_build_url = "%s?action=build-view&title=%s&date=%s&revision=%s&link=%s&description=%s" % \
                            ( sys.argv[0], 
                              title,
                              urllib.quote_plus( date ),
                              revision,
                              urllib.quote_plus( link ),
                              urllib.quote_plus( description) )

            #
            # Add directory entry...
            #
            listitem = xbmcgui.ListItem( label=title, iconImage="DefaultProgram.png" )
            listitem.setInfo( type = "Video", infoLabels = { "Date" : date })
            xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = view_build_url, listitem = listitem, isFolder=False)
            
        #
        # Add "Set running XBMC as dashboard"
        #
        dashboard_set_url = "%s?action=dash-set" % sys.argv[0]
        listitem          = xbmcgui.ListItem( label=xbmc.getLocalizedString(30400), iconImage="DefaultProgram.png" )
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = dashboard_set_url, listitem = listitem, isFolder=False)

        #
        # Add "Delete old installations"
        #
        delete_build_url = "%s?action=build-delete" % sys.argv[0]
        listitem         = xbmcgui.ListItem( label=xbmc.getLocalizedString(30401), iconImage="DefaultProgram.png" )
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = delete_build_url, listitem = listitem, isFolder=False)
        
        #
        # Show current XBMC version (notification)
        #
        xbmc.executebuiltin( "XBMC.Notification(XBMC4Xbox,%s (%s),10000)" % ( xbmcsvn_utils.XBMC_BUILD_VERSION, xbmcsvn_utils.XBMC_BUILD_DATE ) )
        
        #   
        # Label (top-right)...
        #
        xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=( "%s" % self.category ) )

        # Sorting...
        xbmcplugin.addSortMethod( int( sys.argv[ 1 ]), sortMethod=xbmcplugin.SORT_METHOD_DATE )

        # End of directory...
        xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )        

    #
    # Convert HTML to readable strings...
    #
    def parseDescription ( self, description ):
        xmlString = description[description.find("<log>") : description.find("</log>") + 6 ]
        xmlDom    = minidom.parseString( xmlString )
        
        text = ""
        for node in xmlDom.getElementsByTagName("logentry") :
            revision = node.attributes[ "revision" ].value
            author   = ""
            date     = ""
            msg      = ""
            
            for childNode in node.childNodes:
                if childNode.nodeName == "author" :
                    author = childNode.firstChild.data
                elif childNode.nodeName == "date" :
                    date   = childNode.firstChild.data
                elif childNode.nodeName == "msg" :
                    msg   = childNode.firstChild.data.strip()
            
            # Date display...
            date          = date[ : date.find(".") ]
            date_elements = time.strptime(date, "%Y-%m-%dT%H:%M:%S")
            date_format   = xbmc.getRegion( "datelong" ).replace( "DDDD", "%a" ).replace( "D", "%d" ).replace( "MMMM", "%b" ).replace("YYYY", "%Y").strip()
            date_display  = datetime.date( date_elements[0], date_elements[1], date_elements[2] ).strftime( date_format )
            
             
            # Add change entry...
            text = text + "Revision %s - %s\n"                  % ( revision, msg )
            text = text + "%s - [COLOR=FFe2ff43]%s[/COLOR]\n\n" % ( date_display, author )

        # Return value            
        return text

