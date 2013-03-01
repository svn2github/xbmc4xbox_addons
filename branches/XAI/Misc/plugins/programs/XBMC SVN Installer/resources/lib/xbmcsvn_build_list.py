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
from BeautifulSoup import BeautifulSoup, SoupStrainer
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

        # Xbox only (anyways)
        html_url = "http://www.xbmc4xbox.org.uk/nightly/"            
        
        #
        # Get RSS feed...
        #
        try :
            httpCommunicator = HTTPCommunicator()
            htmlData         = httpCommunicator.get( html_url )
            
            soupStrainer     = SoupStrainer( "pre" )
            beautifulSoup    = BeautifulSoup( htmlData, soupStrainer )
        except Exception, e :
            title = "%s - %s" % ( xbmc.getLocalizedString(30000), xbmc.getLocalizedString(257).upper() )
            xbmcgui.Dialog().ok( title, html_url, str(e) )
            return
        
        
        #
        # Parse XML...
        #
        for a_node in beautifulSoup.findAll( "a" ):
            #
            # Init
            #
            title       = ""
            link        = ""
            date        = ""
            description = ""
            
            #
            # Parse entry details...
            #
            title = a_node.text
            if (title == "../") :
                continue

            # Title
            revision = title[ title.rfind("r") + 1 : ].replace( ".zip", "" )
            title    = "XBMC4Xbox [COLOR=FFe2ff43]r%s[/COLOR]" % ( revision )
            
            # Link
            link     = html_url + a_node[ "href" ]
            
            # Date
            text_after_a_node = a_node.nextSibling.string.strip()
            pubDate           = text_after_a_node[ : text_after_a_node.find(" ") ]
            date_elements     = time.strptime(pubDate, "%d-%b-%Y")
            date              = "%02u-%02u-%04u" % ( date_elements[2], date_elements[1], date_elements[0] )
                        
            # Description
            description       = text_after_a_node + "\n\n" + link
            
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
        # Sorting...
        #
        xbmcplugin.addSortMethod( int( sys.argv[ 1 ]), sortMethod=xbmcplugin.SORT_METHOD_DATE )

        # End of directory...
        xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )        

    #
    # Convert HTML to readable strings...
    #
    def parseDescription ( self, description ):
        description = ""

        xmlString = description[description.find("<log>") : description.find("</log>") + 6 ]		
        if xmlString != "" :
            xmlDom    = minidom.parseString( xmlString )
            
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
                description = description + "Revision %s - %s\n"                  % ( revision, msg )
                description = description + "%s - [COLOR=FFe2ff43]%s[/COLOR]\n\n" % ( date_display, author )

        # Return value            
        return description
