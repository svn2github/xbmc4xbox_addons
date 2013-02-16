#
# Imports
#
import os
import sys
import urllib
import xbmc
import xbmcgui
import xbmcplugin
import shutil
import zipfile  
import zipstream  
from datetime import datetime

#
# Main class
#
class Main:
    def __init__(self) :
        # Init
        debug = False
        
        #
        # Parse parameters...
        #
        params = dict(part.split('=', 1) for part in sys.argv[ 2 ][ 1: ].split('&'))
        
        #
        # Init
        #
        self.action   = urllib.unquote_plus ( params[ "action" ] )
        self.title    = urllib.unquote_plus ( params[ "title" ] )
        self.date     = urllib.unquote_plus ( params[ "date" ] )
        self.revision = urllib.unquote_plus ( params[ "revision" ] )
        self.link     = urllib.unquote_plus ( params[ "link" ] )
        
        #
        # Check installation path...
        #
        if xbmcplugin.getSetting ("install_path") == "" :
          # Open plugin settings...
          xbmcplugin.openSettings(url=sys.argv[0])
          
          # User didn't select an installation path, return with no action...
          if xbmcplugin.getSetting ("install_path") == "" :
            return
        
        # Set installation / download path...
        self.install_path = xbmcplugin.getSetting ("install_path")
        
        # Check path...
        if not os.path.isdir( self.install_path ) :
            xbmcgui.Dialog().ok( xbmc.getLocalizedString(30000), xbmc.getLocalizedString(30450), self.install_path)
            return
        
        #
        # Prepare zip name / location...
        #
        date_elements = self.date.split("-")      
        self.zip      = "SVN%s%s%s_%s.zip" % ( date_elements[2], date_elements[1], date_elements[0], self.revision )
        self.zip      = os.path.join( self.install_path, self.zip )
        
        #
        # Download build...
        #
        if self.action == "build-download" or ( self.action == "build-install" and not os.path.isfile(self.zip) ) :
            download_success = self.download_build ( self.title, self.link, self.zip )
            if not download_success :
                return
        
        #
        # Install build...
        #
        if self.action == "build-install" and os.path.isfile( self.zip ) :
            build_dir = "XBMC_%s%s%s_%s" % ( date_elements[2], date_elements[1], date_elements[0], self.revision )
            self.install_build( self.zip, self.install_path, build_dir )

    #
    # Download build...
    #
    def download_build (self, build_title, build_link, build_zip) :
        #
        # Check if file already exists...
        #
        if os.path.isfile( build_zip ) :
            answer_overwrite = xbmcgui.Dialog().yesno( xbmc.getLocalizedString(30000), xbmc.getLocalizedString(30405), build_zip )
        
            # Do not overwrite (give up)...
            if not answer_overwrite :
                return
            
        #
        # Download...
        #
        try :
            success = True
            
            dp = xbmcgui.DialogProgress()
            self.reporthook_msg1             = xbmc.getLocalizedString(30403) % build_title
            self.reporthook_datetime_start   = datetime.now()
            self.reporthook_downloaded_bytes = 0
            self.reporthook_estim_time_left  = ""
            dp.create(xbmc.getLocalizedString(30000), self.reporthook_msg1)
            dp.update( 0 )
        
            urllib._urlopener = AppURLopener()        
            urllib.urlretrieve( build_link, build_zip, lambda nb, bs, fs, url=build_link : self.download_progress_hook( nb, bs, fs, build_zip, dp ) )        
        except :
            success = False
        
        # Cleanup...
        urllib.urlcleanup()
        dp.close()
        
        if success :
            xbmcgui.Dialog().ok( xbmc.getLocalizedString(30000), xbmc.getLocalizedString(30404), build_zip)
        
        # Return value        
        return success        

    #
    # Download progressbar handler...
    #
    def download_progress_hook (self, numblocks, blocksize, filesize, url=None, dp=None, ratio=1.0 ):
        # Calculate sizes...
        downloaded_bytes  = numblocks * blocksize
        downloaded_mbytes = downloaded_bytes / 1048576.0
        filesize_mbytes   = filesize         / 1048576.0
        
        # Estimate time left...            
        if (downloaded_bytes - self.reporthook_downloaded_bytes > 100000 ) :
            self.reporthook_downloaded_bytes = downloaded_bytes
                            
            duration_passed     = datetime.now() - self.reporthook_datetime_start
            seconds_passed      = duration_passed.seconds
            seconds_estim_total = int( round( (filesize * seconds_passed) / downloaded_bytes, 0 ) )
            seconds_estim_left  = seconds_estim_total - seconds_passed
            
            if seconds_estim_left > 0 :
                # Minutes left...
                if seconds_estim_left > 60 :
                    minutes_estim_left = int( round( seconds_estim_left / 60, 0 ) )
                    if minutes_estim_left == 1 :
                        self.reporthook_estim_time_left = ", " + xbmc.getLocalizedString(30503) % minutes_estim_left
                    else :
                        self.reporthook_estim_time_left = ", " + xbmc.getLocalizedString(30504) % minutes_estim_left
                # Seconds left...
                else :
                    if seconds_estim_left == 1 :
                        self.reporthook_estim_time_left = ", " + xbmc.getLocalizedString(30505) % seconds_estim_left
                    else :
                        self.reporthook_estim_time_left = ", " + xbmc.getLocalizedString(30506) % seconds_estim_left
            else :
                self.reporthook_estim_time_left = ""
        
        # Report progress...
        percent = min( downloaded_bytes * 100 / filesize, 100 )
        dp.update( int( percent * ratio ), self.reporthook_msg1, "", "%.01f / %.01f MB%s" % ( downloaded_mbytes, filesize_mbytes, self.reporthook_estim_time_left ) )

        # Cancel
        if dp.iscanceled():
            raise IOError
        
    #
    # Install build...
    #
    def install_build (self, build_zip, install_path, build_dir ) :
        #
        # Init
        #
        install_build_path = os.path.join( install_path, build_dir )
        
        dialogProgress     = None

        #
        # Check if new build folder already exists (previous installation?)...
        #
        if os.path.isdir( install_build_path ) :
            answer_overwrite = xbmcgui.Dialog().yesno( xbmc.getLocalizedString(30000), xbmc.getLocalizedString(30405), install_build_path )
        
            # Remove and re-create..
            if answer_overwrite :
                dialogProgress = xbmcgui.DialogProgress()
                dialogProgress.create( xbmc.getLocalizedString(30000) )
                dialogProgress.update(0, xbmc.getLocalizedString(30406), install_build_path )
                
                shutil.rmtree ( install_build_path )
                os.mkdir      ( install_build_path )          
            else :
                return
        #
        # Create build directory...
        #
        else :
            os.mkdir( install_build_path )
        
        #
        # Extract build zip...
        #
        try :
            # Init...
            zip         = zipstream.ChunkingZipFile( build_zip, "r" )
            zipInfoList = zip.infolist()
            zipNameList = zip.namelist()
            num_entries = len( zipNameList )
        
            # Progress...
            if dialogProgress == None :
                dialogProgress = xbmcgui.DialogProgress()
                dialogProgress.create( xbmc.getLocalizedString(30000) )            
            dialogProgress.update( 0, xbmc.getLocalizedString(30407), "", "" )

            # Extract zip files...
            for counter, zip_entry in enumerate(zipNameList):
                zip_info = zipInfoList[ counter ]
            
                #
                # Analyse ZIP entry...
                #
                ( dir, file ) = os.path.split( zip_entry )
                if dir == "BUILD" :
                    dir = ""
                if dir.startswith( "BUILD/" ) :
                    dir = dir.replace( "BUILD/", "" )
                
                #
                # Create sub-directory (if doesn't exist already)...
                #
                if dir != "" :
                    dir_path = os.path.join( install_build_path, dir )
                    if not os.path.exists( dir_path ) :
                        os.makedirs( os.path.join( install_build_path, dir ) )
                
                #
                # Write file...
                #
                if file != "" :
                    # Update progress...
                    percent = int( ( counter * 100 ) / num_entries )
                    dialogProgress.update(percent, xbmc.getLocalizedString(30407), os.path.join( install_build_path, dir ), file )
                
                    # Unzip file... 
                    file_path = os.path.join( install_build_path, dir, file)
                
                    infile  = zip.readfile( zip_entry )
                    outfile = open(file_path, "wb")

                    while infile.tell() < zip_info.file_size :
                        chunk = infile.read( 65536 )       # 64 KB
                        outfile.write( chunk )
                
                    outfile.flush()
                    outfile.close()
                    infile.close()
            
            # Cleanup
            zip.close()
            del zip  

            # Clear progress...        
            dialogProgress.close()
            del dialogProgress
            
        except zipfile.BadZipfile :
            # Error - invalid zip archive
            xbmcgui.Dialog().ok( xbmc.getLocalizedString(30000), xbmc.getLocalizedString(30451), build_zip )
            return
        
        #
        # Transferring data? (upgrade)...
        #
        answer_upgrade = xbmcgui.Dialog().yesno( xbmc.getLocalizedString(30000), xbmc.getLocalizedString(30408), "", xbmc.getLocalizedString(30409) )
        if answer_upgrade :
            # Progress dialog...
            dialogProgress = xbmcgui.DialogProgress()
            dialogProgress.create( xbmc.getLocalizedString(30000) )
            
            ##########################
            #
            # (1) Transfer System files...
            #
            ##########################
            old_system_path = os.path.join( xbmc.translatePath( "special://home" ), "system" )
            new_system_path = os.path.join( install_build_path,                     "system" )
            
            for file in [ "profiles.xml", "FileZilla Server.xml" ] :
                src_file_path = os.path.join( old_system_path, file )
                dst_file_path = os.path.join( new_system_path, file )
                
                # Progress bar...
                dialogProgress.update(0, xbmc.getLocalizedString(30410), src_file_path, dst_file_path )
                
                if os.path.isfile( src_file_path ) :
                    shutil.copyfile( src_file_path, dst_file_path)
            

            ##########################
            #
            # (2) Transfer UserData... 
            #
            ##########################
            old_userdata_path = xbmc.translatePath( "special://masterprofile" )
            new_userdata_path = os.path.join( install_build_path, "UserData" )
            
            #
            # Clean new UserData...
            #
            dialogProgress.update(20, xbmc.getLocalizedString(30411), old_userdata_path, new_userdata_path )
            shutil.rmtree( new_userdata_path, ignore_errors=True )
            
            #
            # Copy old UserData...
            #
            shutil.copytree( old_userdata_path, new_userdata_path )
            
            #######################
            #
            # (3) Transfer skins...
            #
            #######################
            old_skins_path = os.path.join( xbmc.translatePath( "special://home" ), "skin" )
            new_skins_path = os.path.join( install_build_path, "skin" )
            
            # Check if new skin folder exists, and create if not..
            if not os.path.isdir( new_skins_path ) :
                os.mkdir( new_skins_path )

            # Analyse old skins..
            skin_entries = os.listdir( old_skins_path )
            
            # Copy old skins...
            for skin_entry in skin_entries :                
                # Prepare skin copy...
                old_skin = os.path.join( old_skins_path, skin_entry )
                new_skin = os.path.join( new_skins_path, skin_entry )
                
                # Progress bar...
                dialogProgress.update(40, xbmc.getLocalizedString(30412), old_skin, new_skin )

                # (dir) If the new skin folder exists, skip (maintained in SVN)...
                if os.path.isdir( old_skin ) :
                    if not os.path.exists( new_skin ) :
                        shutil.copytree( old_skin, new_skin )
                # (file) If the file exists, overwrite...
                else :
                    shutil.copyfile( old_skin, new_skin )

            #########################
            #
            # (4) Transfer scripts...
            #
            #########################
            
            # (A) Q:\scripts...
            old_scripts_path = os.path.join( xbmc.translatePath( "special://home" ), "scripts" )
            new_scripts_path = os.path.join( install_build_path, "scripts" )

            # Create new scripts folder if doesn't exist...
            if not os.path.isdir( new_scripts_path ) :
                os.mkdir( new_scripts_path )

            # Analyse old scripts..
            script_entries = os.listdir( old_scripts_path )

            # Copy old scripts...
            for script_entry in script_entries :                
                # Prepare script copy...
                old_script = os.path.join( old_scripts_path, script_entry )
                new_script = os.path.join( new_scripts_path, script_entry )
                
                # Progress bar...
                dialogProgress.update(60, xbmc.getLocalizedString(30413), old_script, new_script )

                # (dir) If the new script folder exists, skip (maintained in SVN)...
                if os.path.isdir( old_script ) :
                    if not os.path.exists( new_script ) :
                        shutil.copytree( old_script, new_script )
                # (file) If the file exists, overwrite...
                else :
                    shutil.copyfile( old_script, new_script )
                    
            # (B) Q:\scripts\.modules...
            old_script_modules_path = os.path.join( old_scripts_path, ".modules" )
            new_script_modules_path = os.path.join( new_scripts_path, ".modules" )
            
            # Create new scripts\.modules folder if doesn't exist...
            if not os.path.isdir( new_script_modules_path ) :
                os.mkdir( new_script_modules_path )

            # Analyse old modules...                
            script_module_entries = os.listdir( old_script_modules_path )
            
            # Copy old modules...
            for script_module_entry in script_module_entries :                
                # Prepare script copy...
                old_script_module = os.path.join( old_script_modules_path, script_module_entry )
                new_script_module = os.path.join( new_script_modules_path, script_module_entry )
                
                # Progress bar...
                dialogProgress.update(60, xbmc.getLocalizedString(30413), old_script_module, new_script_module )

                # (dir) If the new script folder exists, skip (maintained in SVN)...
                if os.path.isdir( old_script_module ) :
                    if not os.path.exists( new_script_module ) :
                        shutil.copytree( old_script_module, new_script_module )            

            #########################
            #
            # (5) Transfer plugins...
            #
            #########################
            old_plugins_path = os.path.join( xbmc.translatePath( "special://home" ), "plugins" )
            new_plugins_path = os.path.join( install_build_path, "plugins" )

            # Check if new plugins folder exists, and create if not..
            if not os.path.isdir( new_plugins_path ) :
                os.mkdir( new_plugins_path )

            # Analyse old plugin categories...
            plugin_categories = os.listdir( old_plugins_path )

            #
            # Copy old plugins (per category)...
            #
            for plugin_category in plugin_categories :
                #
                # Prepare plugin category...
                #
                old_plugin_category_dir = os.path.join( old_plugins_path, plugin_category )
                new_plugin_category_dir = os.path.join( new_plugins_path, plugin_category )
                
                if not os.path.isdir( new_plugin_category_dir ) :
                    os.mkdir( new_plugin_category_dir ) 

                #
                # Copy old plugins (in one category)...
                #
                old_plugin_entries = os.listdir( old_plugin_category_dir )
                for plugin_entry in old_plugin_entries :
                    # Prepare plugin copy...
                    old_plugin = os.path.join( old_plugin_category_dir, plugin_entry)
                    new_plugin = os.path.join( new_plugin_category_dir, plugin_entry )
                
                    # Progress bar...
                    dialogProgress.update(80, xbmc.getLocalizedString(30414), old_plugin, new_plugin )
                    
                    # If the new plugin folder exists, skip (maintained in SVN)...
                    if not os.path.exists( new_plugin ) :
                        shutil.copytree( old_plugin, new_plugin )
            
            #########################
            #
            # (6) Transfer web...
            #
            #########################
            old_web_path = os.path.join( xbmc.translatePath( "special://home" ), "web" )
            new_web_path = os.path.join( install_build_path, "web" )
            
            # Check if old web exists, and no new web folder...
            if os.path.isdir(old_web_path) and not os.path.isdir(new_web_path) :
                # Progress bar...
                dialogProgress.update(100, xbmc.getLocalizedString(30415), old_web_path, new_web_path )

                # Copy...                
                shutil.copytree( old_web_path, new_web_path )
            
            #
            # Upgrade finished
            #
            dialogProgress.update(100, "", "", "" )
            dialogProgress.close()
            
        #
        # Installation complete
        #
        answer_run = xbmcgui.Dialog().yesno( xbmc.getLocalizedString(30000), xbmc.getLocalizedString(30425), install_build_path )
        if answer_run :
            xbmc.executebuiltin('XBMC.RunXBE(%s)' % os.path.join( install_build_path, "default.xbe" ) )

#
# AppURLOpener
#
class AppURLopener(urllib.FancyURLopener):
    version = "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729)"

#
# EOF
#