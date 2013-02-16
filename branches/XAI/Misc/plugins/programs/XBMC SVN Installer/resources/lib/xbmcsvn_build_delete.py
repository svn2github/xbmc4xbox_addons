#
# Imports
#
import os
import xbmc
import xbmcgui
import xbmcplugin
import shutil
import fnmatch

#
# Main class
#
class Main:
    #
    #
    #
    def __init__(self) :
        #
        # Init
        #
        self.install_path      = xbmcplugin.getSetting( "install_path" )
        
        # Check path...
        if not os.path.isdir( self.install_path ) :
            xbmcgui.Dialog().ok( xbmc.getLocalizedString(30000), xbmc.getLocalizedString(30450), self.install_path)
            return
        
        #
        # Get a list of build zips and build folders...
        #
        list = []
        for entry in os.listdir( self.install_path ):
            isfile = os.path.isfile( os.path.join( self.install_path, entry ) )
            isdir  = os.path.isdir ( os.path.join( self.install_path, entry ) )
            
            if ( fnmatch.fnmatch(entry, "*xbmc*.zip") and isfile ) or \
               ( fnmatch.fnmatch(entry, "*XBMC*"    ) and isdir  ) or \
               ( fnmatch.fnmatch(entry, "*svn*.zip" ) and isfile ) or \
               ( fnmatch.fnmatch(entry, "*SVN*"     ) and isdir  ) :
                
                # Skip current XBMC build...
                if not self.is_xbmc_home ( os.path.join( self.install_path, entry ) ) :
                    list.append( entry )
        
        #
        # Show choose dialog...
        #        
        dialog = xbmcgui.Dialog()
        index  = dialog.select( xbmc.getLocalizedString(30401), list )
        if index != -1 :
            # Progress...
            dialogProgress = xbmcgui.DialogProgress()
            dialogProgress.create( xbmc.getLocalizedString(30000) )  
            
            # Delete selected entry...
            path = os.path.join( self.install_path, list[ index ] ) 
            dialogProgress.update( 0, xbmc.getLocalizedString( 30406 ), path )

            if os.path.isdir( path ) :
                shutil.rmtree( path )
            elif os.path.isfile( path ) :
                os.remove( path )
                
            # Progress...
            dialogProgress.update( 100 )
            dialogProgress.close()
            
    #
    # Check if the path to current XBMC...
    #
    def is_xbmc_home( self, path ):
        # Init
        is_xbmc_home = False
        
        # path/BUILD exists?
        if os.path.isdir( os.path.join( path, "BUILD" ) ) :
            path = os.path.join( path, "BUILD" )
        
        # path/XBMC exists?
        if os.path.isdir( os.path.join( path, "XBMC" ) ) :
            path = os.path.join( path, "XBMC" )
        
        # Try renaming xbmc.log - if in use, it will fail...
        try :
            if os.path.isfile( os.path.join( path, "xbmc.log") ) :
                os.rename( os.path.join( path, "xbmc.log"),       os.path.join( path, "xbmc.log.test" ) )
                os.rename( os.path.join( path, "xbmc.log.test" ), os.path.join( path, "xbmc.log" ) )
        except :
            is_xbmc_home = True
            
        # Return value
        return is_xbmc_home

#
# EOF
#