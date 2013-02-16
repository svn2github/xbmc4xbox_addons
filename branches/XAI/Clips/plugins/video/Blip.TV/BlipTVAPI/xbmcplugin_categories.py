"""
    Category module: list of categories to use as folders
"""

# main imports
import sys
import os
import xbmc
import xbmcgui
import xbmcplugin

from urllib import quote_plus, unquote_plus

from BlipTVAPI.BlipTVClient import BlipTVClient


class _Info:
    def __init__( self, *args, **kwargs ):
        self.__dict__.update( kwargs )


class Main:
    # base paths
    BASE_PLUGIN_THUMBNAIL_PATH = os.path.join( os.getcwd().replace( ";", "" ), "thumbnails" )

    def __init__( self ):
        # parse sys.argv
        self._parse_argv()
        # set username
        self._get_user()
        if ( not sys.argv[ 2 ] ):
            self.get_categories()
        else:
            self.get_categories( False )

    def _parse_argv( self ):
        if ( not sys.argv[ 2 ] ):
            self.args = _Info( title="" )
        else:
            # call _Info() with our formatted argv to create the self.args object
            exec "self.args = _Info(%s)" % ( unquote_plus( sys.argv[ 2 ][ 1 : ].replace( "&", ", " ) ).replace( "\\u0027", "'" ).replace( "\\u0022", '"' ).replace( "\\u0026", "&" ), )

    def _get_user( self ):
        # if this is first run open settings
        self.openSettings()
        # get the username
        self.username = xbmcplugin.getSetting( "username" )

    def openSettings( self ):
        try:
            # is this the first time plugin was run and user has not set email
            if ( not sys.argv[ 2 ] and xbmcplugin.getSetting( "username" ) == "" and xbmcplugin.getSetting( "runonce" ) == "" ):
                # set runonce
                xbmcplugin.setSetting( "runonce", "1" )
                # sleep for xbox so dialogs don't clash. (TODO: report this as a bug?)
                if ( os.environ.get( "OS", "n/a" ) == "xbox" ):
                    xbmc.sleep( 2000 )
                # open settings
                xbmcplugin.openSettings( sys.argv[ 0 ] )
        except:
            # new methods not in build
            pass

    def get_categories( self, root=True ):
        try:
            # default categories
            if ( root ):
                categories = (
                                        ( xbmc.getLocalizedString( 30950 ), "presets_videos", "", "", True, 0, xbmc.getLocalizedString( 30970 ), False, "", ),
                                        ( xbmc.getLocalizedString( 30951 ), "presets_users", "", "", True, 0, xbmc.getLocalizedString( 30971 ), False, "", ),
                                        ( xbmc.getLocalizedString( 30954 ), "users__uploads", "", "", True, 0, xbmc.getLocalizedString( 30974 ), True, "", ),
                                        ( xbmc.getLocalizedString( 30955 ), "users__favorites", "", "", True, 0, xbmc.getLocalizedString( 30975 ), True, "", ),
                                        ( xbmc.getLocalizedString( 30956 ), "most_recent", "", "", True, 0, xbmc.getLocalizedString( 30976 ), False, "", ),
                                    )
                # now add Blip TV's categories
                client = BlipTVClient( BlipTVClient.BASE_URL )
                # fetch the categories
                blip_categories = client.get_categories()
                # if successful, enumerate thru the list and add the category to our list
                if ( blip_categories ):
                    for category in blip_categories:
                        # TODO: use this for localizing category - xbmc.getLocalizedString( 30900 + category[ "id" ] )
                        categories += ( category[ "name" ], "category_%s" % ( category[ "id" ].replace( "-", "_" ), ), "", "", True, 0, category[ "desc" ], False, "", ),
            # search preset category
            elif ( "category='presets_videos'" in sys.argv[ 2 ] ):
                categories = self.get_presets()
            # user preset category
            elif ( "category='presets_users'" in sys.argv[ 2 ] ):
                categories = self.get_presets( True )
            # fill media list
            ok = self._fill_media_list( categories )
        except:
            # oops print error message
            print "ERROR: %s::%s (%d) - %s" % ( self.__class__.__name__, sys.exc_info()[ 2 ].tb_frame.f_code.co_name, sys.exc_info()[ 2 ].tb_lineno, sys.exc_info()[ 1 ], )
            ok = False
        # set cache to disc
        cacheToDisc = ( ok and not ( "category='presets_videos'" in sys.argv[ 2 ] or "category='presets_users'" in sys.argv[ 2 ] ) )
        # send notification we're finished, successfully or unsuccessfully
        xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=ok, cacheToDisc=cacheToDisc )

    def get_presets( self, ptype=False ):
        # set category
        category = ( "videos", "users", )[ ptype ]
        # initialize our category tuple
        categories = ()
        # add our new search item
        if ( ptype ):
            categories += ( ( xbmc.getLocalizedString( 30953 ), "search_users", "", "", True, 2, xbmc.getLocalizedString( 30973 ), False, "", ), )
        else:
            categories += ( ( xbmc.getLocalizedString( 30952 ), "search_videos", "", "", True, 1, xbmc.getLocalizedString( 30972 ), False, "", ), )
        # fetch saved presets
        try:
            # read the queries
            presets = eval( xbmcplugin.getSetting( "presets_%s" % ( category, ) ) )
            # sort items
            presets.sort()
        except:
            # no presets found
            presets = []
        # enumerate through the presets list and read the query
        for query in presets:
            try:
                # set video query and user query to empty
                vq = username = u""
                # set thumbnail
                thumbnail = query.split( " | " )[ 1 ].encode( "utf-8" )
                # if this is the user presets set username else set video query
                if ( ptype ):
                    username = query.split( " | " )[ 0 ].encode( "utf-8" )
                else:
                    vq = query.split( " | " )[ 0 ].encode( "utf-8" )
                # add preset to our dictionary
                categories += ( ( query.split( " | " )[ 0 ].encode( "utf-8" ), "videos", vq, username, True, 0, xbmc.getLocalizedString( 30977 + ptype ), False, thumbnail, ), )
            except:
                # oops print error message
                print "ERROR: %s::%s (%d) - %s" % ( self.__class__.__name__, sys.exc_info()[ 2 ].tb_frame.f_code.co_name, sys.exc_info()[ 2 ].tb_lineno, sys.exc_info()[ 1 ], )
        return categories

    def _fill_media_list( self, categories ):
        try:
            ok = True
            # enumerate through the tuple of categories and add the item to the media list
            for ( title, method, vq, username, isfolder, issearch, description, idrequired, thumbnail, ) in categories:
                # if a idrequired is required for category and none supplied, skip category
                if ( idrequired and self.username == "" ): continue
                # set the callback url
                url = '%s?title=%s&category=%s&vq=%s&username=%s&issearch=%d&update_listing=%d' % ( sys.argv[ 0 ], quote_plus( repr( title ) ), repr( method ), quote_plus( repr( vq ) ), quote_plus( repr( username ) ), issearch, False, )
                # check for a valid custom thumbnail for the current category
                thumbnail = thumbnail or self._get_thumbnail( method )
                # set the default icon
                icon = "DefaultFolderBig.png"
                # only need to add label, icon and thumbnail, setInfo() and addSortMethod() takes care of label2
                listitem=xbmcgui.ListItem( title, iconImage=icon, thumbnailImage=thumbnail )
                # add the item to the media list
                ok = xbmcplugin.addDirectoryItem( handle=int( sys.argv[ 1 ] ), url=url, listitem=listitem, isFolder=isfolder, totalItems=len( categories ) )
                # if user cancels, call raise to exit loop
                if ( not ok ): raise
            # we do not want to sort queries list
            if ( "category='presets_videos'" in sys.argv[ 2 ] or "category='presets_users'" in sys.argv[ 2 ] ):
                xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
            # set our plugin category
            xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=self.args.title )
            # set our fanart from user setting
            if ( xbmcplugin.getSetting( "fanart_image" ) ):
                xbmcplugin.setPluginFanart( handle=int( sys.argv[ 1 ] ), image=xbmcplugin.getSetting( "fanart_image" ) )
        except:
            # user cancelled dialog or an error occurred
            print "ERROR: %s::%s (%d) - %s" % ( self.__class__.__name__, sys.exc_info()[ 2 ].tb_frame.f_code.co_name, sys.exc_info()[ 2 ].tb_lineno, sys.exc_info()[ 1 ], )
            ok = False
        return ok

    def _get_thumbnail( self, title ):
        # create the full thumbnail path for skins directory
        thumbnail = os.path.join( sys.modules[ "__main__" ].__plugin__, title + ".png" )
        # use a plugin custom thumbnail if a custom skin thumbnail does not exists
        if ( not xbmc.skinHasImage( thumbnail ) ):
            # create the full thumbnail path for plugin directory
            thumbnail = os.path.join( self.BASE_PLUGIN_THUMBNAIL_PATH, title + ".png" )
            # use a default thumbnail if a custom thumbnail does not exists
            if ( not os.path.isfile( thumbnail ) ):
                thumbnail = "DefaultFolderBig.png"
        return thumbnail
