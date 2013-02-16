"""
    Videos module: fetches a list of videos for a specific category
"""

# main imports
import sys
import os
import xbmc
import xbmcgui
import xbmcplugin

from urllib import unquote_plus, quote_plus

from BlipTVAPI.BlipTVClient import BlipTVClient


class _Info:
    def __init__( self, *args, **kwargs ):
        self.__dict__.update( kwargs )


class Main:
    # base paths
    BASE_PLUGIN_THUMBNAIL_PATH = os.path.join( os.getcwd().replace( ";", "" ), "thumbnails" )

    def __init__( self ):
        self._get_settings()
        self._get_strings()
        self._parse_argv()
        self._get_items()

    def _get_settings( self ):
        self.settings = {}
        self.settings[ "username" ] = xbmcplugin.getSetting( "username" )
        self.settings[ "password" ] = xbmcplugin.getSetting( "password" )
        self.settings[ "include_explicit" ] = ( 0, 1, )[ xbmcplugin.getSetting( "include_explicit" ) == "true" ]
        self.settings[ "pagelen" ] = ( 10, 15, 20, 25, 30, 40, 50, 75, 100, )[ int( xbmcplugin.getSetting( "pagelen" ) ) ]
        self.settings[ "language_code" ] = ( "", xbmcplugin.getSetting( "language_code" ), )[ xbmcplugin.getSetting( "language_code" ) != "-" ]
        self.settings[ "saved_searches" ] = ( 10, 20, 30, 40, )[ int( xbmcplugin.getSetting( "saved_searches" ) ) ]
        self.settings[ "fanart_image" ] = xbmcplugin.getSetting( "fanart_image" )

    def _get_strings( self ):
        self.localized_string = {}
        self.localized_string[ 30900 ] = xbmc.getLocalizedString( 30900 )
        self.localized_string[ 30901 ] = xbmc.getLocalizedString( 30901 )
        self.localized_string[ 30902 ] = xbmc.getLocalizedString( 30902 )
        self.localized_string[ 30903 ] = xbmc.getLocalizedString( 30903 )
        self.localized_string[ 30905 ] = xbmc.getLocalizedString( 30905 )

    def _parse_argv( self ):
        # call _Info() with our formatted argv to create the self.args object
        exec "self.args = _Info(%s)" % ( unquote_plus( sys.argv[ 2 ][ 1 : ].replace( "&", ", " ) ).replace( "\\u0027", "'" ).replace( "\\u0022", '"' ).replace( "\\u0026", "&" ), )

    def _get_items( self ):
        # get the videos and/or subcategories and fill the media list
        if ( self.args.category.startswith( "category_" ) ):
            ok, total = self.category()
        else:
            exec "ok, total = self.%s()" % ( self.args.category, )
        # send notification we're finished, successfully or unsuccessfully
        xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=ok, updateListing=self.args.update_listing )#, cacheToDisc=not self.args.issearch )
        # if there were videos and this was a search ask to save result as a preset
        if ( ok and total and self.args.issearch ):
            self.save_as_preset()

    def save_as_preset( self ):
        # select correct query
        query = ( self.args.vq, self.args.username, )[ self.args.issearch - 1 ]
        # if user search and user was found then proceed, should never be an issue for video search
        if ( query ):
            # fetch saved presets
            try:
                # read the queries
                presets = eval( xbmcplugin.getSetting( "presets_%s" % ( "videos", "users", )[ self.args.issearch - 1  ], ) )
                # if this is an existing search, move it up
                for count, preset in enumerate( presets ):
                    if ( repr( query + " | " )[ : -1 ] in repr( preset ) ):
                        del presets[ count ]
                        break
                # limit to number of searches to save
                if ( len( presets ) >= self.settings[ "saved_searches" ] ):
                    presets = presets[ : self.settings[ "saved_searches" ] - 1 ]
            except:
                # no presets found
                presets = []
            # insert our new search
            presets = [ query + " | " + self.query_thumbnail ] + presets
            # save search query
            xbmcplugin.setSetting( "presets_%s" % ( "videos", "users", )[ self.args.issearch - 1  ], repr( presets ) )

    def most_recent( self ):
        return self.fetch_videos( BlipTVClient.BASE_VIDEOS_URL, language_code=self.settings[ "language_code" ] )

    def search_videos( self ):
        # get the query to search for from the user
        self.args.vq = self._get_keyboard( heading=xbmc.getLocalizedString( 30906 ) )
        # if blank or the user cancelled the keyboard, return
        if ( not self.args.vq ): return False, 0
        # we need to set the title to our query
        self.args.title = self.args.vq
        # we need to set the function to videos
        self.args.category = "videos"
        return self.fetch_videos( BlipTVClient.BASE_VIDEOS_URL, language_code=self.settings[ "language_code" ] )

    def search_users( self ):
        # get the username to search for from the user
        self.args.username = self._get_keyboard( heading=xbmc.getLocalizedString( 30907 ) )
        # if blank or the user cancelled the keyboard, return
        if ( not self.args.username ): return False, 0
        # we need to set the title to our query
        self.args.title = self.args.username
        # we need to set the function to users
        self.args.category = "users"
        ok, total = self.fetch_videos( BlipTVClient.BASE_VIDEOS_URL, language_code=self.settings[ "language_code" ] )
        # if exact match was found return results
        if ( total ): return ok, total
        # if no exact match found we search using regular search engine
        # we need to set the function to videos
        self.args.category = "videos"
        # set the search query to the username
        self.args.vq = self.args.username
        # empty username
        self.args.username = ""
        return self.fetch_videos( BlipTVClient.BASE_VIDEOS_URL, language_code=self.settings[ "language_code" ] )

    def users__uploads( self ):
        # set author to user name
        self.args.username = self.settings[ "username" ]
        return self.fetch_videos( BlipTVClient.BASE_VIDEOS_URL, language_code=self.settings[ "language_code" ] )

    def users__favorites( self ):
        # set author to user name
        self.args.username = self.settings[ "username" ]
        return self.fetch_videos( BlipTVClient.BASE_VIDEOS_URL, language_code=self.settings[ "language_code" ] )

    def category( self ):
        category = self.args.category.split( "_" )[ 1 ]
        return self.fetch_videos( BlipTVClient.BASE_VIDEOS_URL, category=category, language_code=self.settings[ "language_code" ] )

    def videos( self ):
        return self.fetch_videos( BlipTVClient.BASE_VIDEOS_URL, language_code=self.settings[ "language_code" ] )

    def fetch_videos( self, url, **kwargs ):#url, category="", language_code="" ):
        # BlipTV client
        client = BlipTVClient( url )
        # set required parameters
        kwargs[ "show_nsfw" ] = self.settings[ "include_explicit" ]
        kwargs[ "pagelen" ] = self.settings[ "pagelen" ]
        kwargs[ "search" ] = self.args.vq
        kwargs[ "user" ] = self.args.username
        # fetch the videos
        videos = client.get_videos( kwargs )#category=category, language_code=language_code, show_nsfw=self.settings[ "include_explicit" ], pagelen=self.settings[ "pagelen" ], search=self.args.vq, user=self.args.username )
        # if there are results
        if ( videos ):
            return self._fill_media_list( True, videos )
        #else return failed
        return False, 0

    def _fill_media_list( self, ok, videos ):
        try:
            # calculate total items
            total_items = len( videos )
            # if ok (always is for now) fill directory
            if ( ok ):
                # set our thumbnail for queries
                self.query_thumbnail = videos[ 0 ][ "thumbnail" ]
                # enumerate through the list of pictures and add the item to the media list
                for c, video in enumerate( videos ):
                    # only add videos with a valid video url
                    if ( len( video[ "video_urls" ] ) ):
                        # plot
                        plot = xbmc.getLocalizedString( 30904 )
                        if ( video[ "desc" ] ):
                            plot = video[ "desc" ]
                            plot = self._clean_text( plot.strip() )
                        # format runtime as 00:00
                        run = int( video[ "runtime" ] )
                        runtime = ""
                        # video runtime
                        if ( run ):
                            runtime = "%02d:%02d" % ( int( run / 60 ), run % 60, )
                        # viewer rating
                        try:
                            rating = float( video[ "rating" ] )
                        except:
                            rating = 0.0
                        # genre
                        genre = video[ "genre" ]
                        # updated date
                        #<pubDate>Wed, 16 Apr 2008 18:00:30 +0000</pubDate>
                        mm = [ "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec" ].index(video[ "date" ][ 8 : 11 ] )
                        date = "%02d-%02d-%04d" % ( int( video[ "date" ][ 5 : 7 ] ), mm + 1, int( video[ "date" ][ 12 : 16 ] ), )                            
                        # construct our url
                        video_url = video[ "video_urls" ][ 0 ]
                        for vid in video[ "video_urls" ]:
                            if ( vid.endswith( ".flv" ) ):
                                video_url = vid
                                break
                        url = video_url
                        # set the default icon
                        icon = "DefaultVideo.png"
                        # only need to add label, icon and thumbnail, setInfo() and addSortMethod() takes care of label2
                        listitem=xbmcgui.ListItem( label=video[ "title" ], iconImage=icon, thumbnailImage=video[ "thumbnail" ] )
                        # add the different infolabels we want to sort by
                        listitem.setInfo( type="Video", infoLabels={ "Title": video[ "title" ], "Director": video[ "username" ], "Duration": runtime, "Plot": plot, "PlotOutline": plot, "Rating": rating, "Genre": genre, "Date": date } )
                        # add the video to the media list
                        ok = xbmcplugin.addDirectoryItem( handle=int( sys.argv[ 1 ] ), url=url, listitem=listitem, isFolder=False, totalItems=total_items )
                        # if user cancels, call raise to exit loop
                        if ( not ok ): raise
        except:
            # oops print error message
            print "ERROR: %s::%s (%d) - %s" % ( self.__class__.__name__, sys.exc_info()[ 2 ].tb_frame.f_code.co_name, sys.exc_info()[ 2 ].tb_lineno, sys.exc_info()[ 1 ], )
            ok = False
        # if successful and user did not cancel, add all the required sort methods
        if ( ok ):
            xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
            xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RATING )
            xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_DATE )
            xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RUNTIME )
            xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_GENRE )
            # set content
            xbmcplugin.setContent( handle=int( sys.argv[ 1 ] ), content="movies" )
            # set our plugin category
            xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=self.args.title )
            # if skin has fanart image use it
            fanart_image = os.path.join( sys.modules[ "__main__" ].__plugin__, self.args.category + "-fanart.png" )
            if ( xbmc.skinHasImage( fanart_image ) ):
                xbmcplugin.setPluginFanart( handle=int( sys.argv[ 1 ] ), image=fanart_image )
            # set our fanart from user setting
            elif ( self.settings[ "fanart_image" ] ):
                xbmcplugin.setPluginFanart( handle=int( sys.argv[ 1 ] ), image=self.settings[ "fanart_image" ] )
        return ok, total_items

    def _get_keyboard( self, default="", heading="", hidden=False ):
        """ shows a keyboard and returns a value """
        keyboard = xbmc.Keyboard( default, heading, hidden )
        keyboard.doModal()
        if ( keyboard.isConfirmed() ):
            return unicode( keyboard.getText(), "utf-8" )
        return default

    def _clean_text( self, text ):
        """ Convert line terminators and html entities """
        try:
            text = text.replace( "\t", "" )
            text = text.replace( "<p>", "" )
            text = text.replace( "</p>", "" )
            text = text.replace( "<em>", "" )
            text = text.replace( "</em>", "" )
            text = text.replace( "<strong>", "" )
            text = text.replace( "</strong>", "" )
            text = text.replace( "\t", "" )
            text = text.replace( "<br> ", "\n" )
            text = text.replace( "<br>", "\n" )
            text = text.replace( "<br /> ", "\n" )
            text = text.replace( "<br />", "\n" )
            text = text.replace( "<div>", "\n" )
            text = text.replace( "> ", "\n" )
            text = text.replace( ">", "\n" )
            text = text.replace( "&amp;", "&" )
            text = text.replace( "&gt;", ">" )
            text = text.replace( "&lt;", "<" )
            text = text.replace( "&quot;", '"' )
        except: 
            pass
        return text


