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
from xbmc4xbox_utils import HTTPCommunicator
from xbmc4xbox_utils import HTML2Text
import xbmc4xbox_utils

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
        self.getSkins()
            
    
    #
    # Get skins...
    #
    def getSkins( self ) :
        #
        # Init
        #
        html2text     = HTML2Text()
        os_platform   = os.getenv("OS")

        if os_platform == "xbox" :
            xbmc_revision = int( xbmc4xbox_utils.XBMC_BUILD_VERSION[xbmc4xbox_utils.XBMC_BUILD_VERSION.rfind('r') + 1 : ] )
        else :
            xbmc_revision = int( xbmc4xbox_utils.XBMC_BUILD_VERSION.split(' ')[1][1:] )            
        
        #
        # Debug
        #
        if self.DEBUG == True :
            print "Operating System  = " + os_platform
            print "XBMC Revision     = " + str( xbmc_revision )
        
        #
        # Get HTML page...
        #
        url = "http://www.xbmcsvn.com/?mode=SAPI"
        try :
            httpCommunicator = HTTPCommunicator()
            htmlSource       = httpCommunicator.get( url )
        except Exception, e :
            title = "%s - %s" % ( xbmc.getLocalizedString(30000), xbmc.getLocalizedString(257).upper() )
            xbmcgui.Dialog().ok( title, url, str(e) )
            return
        
        # Debug
        if (self.DEBUG) :
            f = open(os.path.join( xbmc.translatePath( "special://profile" ), "plugin_data", "programs", sys.modules[ "__main__" ].__plugin__, "skins.html" ), "w")
            f.write( htmlSource )
            f.close()
        
        #
        # Parse HTML page...
        #        
        blocks = str( htmlSource ).split( "<hr />" )
        skins  = []
        for block in blocks :
            # Skin...
            skin = {}
            
            # Parse Skin details...
            details = block.split( "<br />")
            for detail in details :
                # Name
                if detail.startswith( "Name:") :
                    skin[ "name" ] = detail[6:]
                
                # Build
                elif detail.startswith( "Build:") :
                    skin[ "version" ] = detail[7:]
                
                # Author
                elif detail.startswith( "Author:") :
                    skin[ "author" ] = detail[8:]
                
                # Description
                elif detail.startswith( "Desc:") :
                    skin[ "description" ] = detail[6:]
                
                # Xbox Compatible
                elif detail.startswith( "Xbox Compatible:" ) :
                    skin[ "xbox_compat" ] = ( "No", "Yes" ) [ detail[17:] == "1" ]
                
                # Download URL
                elif detail.startswith( "Download URL:" ) :
                    skin[ "download_url" ] = detail[14:]
                
                # Images
                elif detail.startswith( "Image Link:") :
                    image = detail[12:]
                    
                    if skin.get( "screenshots" ) == None :
                        skin[ "screenshots" ] = []
                        skin[ "thumbnail" ] = image
                    
                    skin[ "screenshots" ].append( image )
                
                # Downloads
                elif detail.startswith( "Downloaded:") :
                    skin[ "downloads" ] = detail[12:]
                
                # Xbox Revision Required (0)
                elif detail == "Pre28000" :
                    skin[ "xbmc_rev_req" ] = 0
                
                # Xbox Revision Required (20800)
                elif detail == "Post28000" :
                    skin[ "xbmc_rev_req" ] = 28000

            skin[ "rating" ]    = "?"
            
            #
            # Skip last empty entry...
            #
            if skin.get( "name" ) == None :
                continue
            
            #
            # Xbox platform (ignore incompatible skins)..
            #
            if (os_platform == "xbox") :
                if (skin[ "xbox_compat" ] == "No") :
                    continue
            #
            # Other platforms (check minimum revision required)...
            # 
            else :
                if (xbmc_revision < skin[ "xbmc_rev_req" ]) :
                    continue
                
                #
                # Look if skin already exists in the list, 
                # and remove the one requiring the older revision...
                #
                for search_skin in skins :
                    if search_skin.get( "xbmc_rev_req" ) < skin.get( "xbmc_rev_req" ) :
                        skins.remove( search_skin )
            
            #
            # Debug
            #
            if self.DEBUG :
                print "Name              = " + skin[ "name" ]
                print "Version           = " + skin[ "version" ]
                print "Author            = " + skin[ "author" ]
                print "Description       = " + skin[ "description" ]
                print "Xbox Compatible   = " + skin[ "xbox_compat" ]
                print "Download URL      = " + skin[ "download_url" ]
                print "Thumbnail         = " + skin[ "thumbnail" ]
                print "Screenshots       = " + repr( skin[ "screenshots" ] )
                print "Revision required = " + str ( skin[ "xbmc_rev_req" ] )
            
            #
            # Skin entry...
            #
            skins.append( skin )            
            
        #
        # Display skin entries...
        #
        for skin in skins :
            # View skin URL...
            view_skin_url = "%s?action=skin-view&name=%s&version=%s&rating=%s&downloads=%s&xbox_compat=%s&description=%s&screenshots=%s&download-url=%s" % \
                            ( sys.argv[0], 
                              urllib.quote_plus( skin[ "name" ] ),
                              urllib.quote_plus( skin[ "version" ] ), 
                              skin[ "rating" ], 
                              skin[ "downloads" ], 
                              skin[ "xbox_compat" ], 
                              skin[ "description" ], 
                              repr( skin[ "screenshots" ] ), 
                              urllib.quote_plus( skin[ "download_url" ] ) )

            # Add directory entry...
            listitem = xbmcgui.ListItem( label="%s %s" % ( skin[ "name" ], skin[ "version" ] ), iconImage=skin[ "thumbnail" ], thumbnailImage=skin[ "thumbnail" ] )
            xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = view_skin_url, listitem = listitem, isFolder=False)
        
        # Label (top-right)...
        xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=( "%s" % self.category ) )

        # Sorting...
        xbmcplugin.addSortMethod( int( sys.argv[ 1 ]), sortMethod=xbmcplugin.SORT_METHOD_LABEL )

        # End of directory...
        xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

    #
    # Convert HTML to readable strings...
    #
    def html2text ( self, html ):
        return xml.sax.saxutils.unescape( html, { "&#39;" : "'" } )
