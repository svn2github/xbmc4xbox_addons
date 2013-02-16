#
# Imports
#
import re
import os
import glob
import xbmc
import xbmcgui

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
        xbmc_home = self.getXbmcHome()
        
        if not xbmc_home :
            xbmcgui.Dialog().ok( xbmc.getLocalizedString(30000), xbmc.getLocalizedString(30452) )
            return
        
        #
        # Find and update x2config.ini...
        #
        x2config_path = self.findX2config() 
        if x2config_path :
            self.updateX2config( x2config_path, xbmc_home )
            return
        
        #
        # Find and update .cfg file...
        #
        shortcut_cfg_path = self.findShortcutCfg()
        if shortcut_cfg_path :
            self.updateShortcutCfg( shortcut_cfg_path, xbmc_home )
            return
        
        #
        # Sorry, could not find any of the above...
        #
        xbmcgui.Dialog().ok( xbmc.getLocalizedString(30000), xbmc.getLocalizedString(30427) )
            
    #
    # Check if the path to current XBMC...
    #
    def getXbmcHome( self ):
        # Init
        xbmc_home = None
        
        # Parse the log file for the location...
        logfile = open( os.path.join( xbmc.translatePath( "special://xbmc" ), "xbmc.log" ), "r" )
        regexp  = re.compile( "The executable running is: (.*)", re.IGNORECASE)
        
        for line in logfile :
            matches = regexp.search( line )
            if matches :
                xbmc_home = matches.group(1)
                break

        # Close file
        logfile.close()
        
        # Return value
        return xbmc_home

    #
    # Find x2config.ini
    #
    def findX2config( self ):
        # Init...
        x2config_path = None
        drives        = [ "E:\\", "F:\\" ]

        for drive in drives :
            path = os.path.join( drive, "x2config.ini" )
            if os.path.isfile( path ) :
                x2config_path = path
                break
            
        # Return value...
        return x2config_path
    
    #
    # Update x2config
    #
    def updateX2config(self, x2config_path, xbmc_home ):
        #
        # Confirm...
        #
        dash1Name = "dash1Name = %s" % ( xbmc_home[ 0:2 ] + xbmc_home[ 3: ] )
        answer    = xbmcgui.Dialog().yesno( xbmc.getLocalizedString(30000), 
                                            xbmc.getLocalizedString(30426) % x2config_path,
                                            "", dash1Name )
        # Cancel and return...
        if not answer :
            return

        #
        # Update...
        #
        infile  = open( x2config_path,          "r" )
        outfile = open( x2config_path + ".new", "w" )
        
        regexp  = re.compile( "^dash1Name", re.IGNORECASE) 
        
        for line in infile :
            if regexp.match( line ) :
                outfile.write( dash1Name + os.linesep )
            else :
                outfile.write( line )
                
        # Close files...
        outfile.close()
        infile.close()
        
        # Backup old x2config.ini and rename new...
        if os.path.isfile( os.path.join( x2config_path + ".old" ) ) :
            os.remove( os.path.join( x2config_path + ".old" ) )
        os.rename( x2config_path,          x2config_path + ".old" )
        os.rename( x2config_path + ".new", x2config_path )
    
    #
    # Find shortcut .cfg
    #
    def findShortcutCfg( self ):
        # Init...
        shortcut_cfg_path = None
        paths             = [ "C:\\fonts\\dashboard", "C:\\", "E:\\", "F:\\", "E:\\Dash", "E:\\Dashboard" ]

        # Look through defined locations...
        for path in paths :
            files = glob.glob( os.path.join( path, "*.cfg" ) )
            if files :
                # Pick the first fine that's a one liner...
                for file in files :
                    # Count number of lines...
                    f     = open(file, "r")
                    lines = f.readlines()
                    f.close()
                    
                    # Great, found one...
                    if len(lines) == 1 :
                        shortcut_cfg_path = file
                        break
            
        # Return value...
        return shortcut_cfg_path
    
    #
    # Update shortcut .cfg
    #
    def updateShortcutCfg( self, shortcut_cfg_path, xbmc_home ):
        #
        # Confirm...
        #
        answer = xbmcgui.Dialog().yesno( xbmc.getLocalizedString(30000), 
                                         xbmc.getLocalizedString(30426) % shortcut_cfg_path,
                                         "", xbmc_home )
        # Cancel and return...
        if not answer :
            return

        #
        # Update...
        #
        outfile = open( shortcut_cfg_path + ".new", "w" )
        outfile.write( xbmc_home )
        outfile.close()

        #
        # Backup old shortcut .cfg and rename new...
        #
        if os.path.isfile( os.path.join( shortcut_cfg_path + ".old" ) ) :
            os.remove( os.path.join( shortcut_cfg_path + ".old" ) )
        os.rename( shortcut_cfg_path,          shortcut_cfg_path + ".old" )
        os.rename( shortcut_cfg_path + ".new", shortcut_cfg_path )       
#
# EOF
#