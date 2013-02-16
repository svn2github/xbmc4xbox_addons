#
# Imports
#
import os
import sys
import urllib
import xbmc
import xbmcgui
import zipfile
import shutil
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
        skin_name          = urllib.unquote_plus ( params[ "name" ] )
        skin_archive_url   = urllib.unquote_plus ( params[ "url" ] )
        skin_archive_local = os.path.join( xbmc.translatePath( "special://temp" ), "xbmcsvn-skin.archive" )
        
        # Strip version from skin name...
        skin_name = skin_name.rsplit(" ", 1)[0].strip()

        # Debug info
        if debug :
            print "=== xbmcsvn_skin_install.py ==="
            print "NAME          = " + skin_name
            print "DOWNLOAD URL  = " + skin_archive_url
            print "ARCHIVE LOCAL = " + skin_archive_local

        # Download skin...
        download_success = self.download_skin ( skin_name, skin_archive_url, skin_archive_local )

        # Install skin...
        if download_success :
            self.install_skin ( skin_name, skin_archive_local )

    #
    # Download skin...
    #
    def download_skin (self, skin_name, skin_archive_url, skin_archive_local) :
        try :
            success = True
            
            dp = xbmcgui.DialogProgress()
            self.reporthook_msg1             = xbmc.getLocalizedString(30302) % skin_name
            self.reporthook_datetime_start   = datetime.now()
            self.reporthook_downloaded_bytes = 0
            self.reporthook_estim_time_left  = ""
            dp.create(xbmc.getLocalizedString(30000), self.reporthook_msg1)
        
            urllib._urlopener = AppURLopener()        
            urllib.urlretrieve( skin_archive_url, skin_archive_local, lambda nb, bs, fs, url=skin_archive_url : self.download_progress_hook( nb, bs, fs, skin_archive_local, dp ) )
        except :
            success = False
        
        urllib.urlcleanup()
        dp.close()
        
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
            seconds_estim_total = int( (filesize * seconds_passed) / downloaded_bytes )
            seconds_estim_left  = seconds_estim_total - seconds_passed
            
            if seconds_estim_left > 0 :
                # Minutes left...
                if seconds_estim_left > 60 :
                    minutes_estim_left = int( seconds_estim_left / 60 )
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
    # Install skin...
    #
    def install_skin(self, skin_name, skin_archive_local) :
        skin_install_dir     = os.path.join( xbmc.translatePath( "special://home/" ), "skin" )
        skin_install_success = True
        
        # ZipFile
        if zipfile.is_zipfile( skin_archive_local ) :
            dp = xbmcgui.DialogProgress()
            dp.create(xbmc.getLocalizedString(30000), xbmc.getLocalizedString(30303) % skin_name)
            
            # Open zip...
            zip = zipfile.ZipFile (skin_archive_local, "r")
            zip_entry_total = len( zip.namelist() )
            zip_entry_count = 0
            
            # Loop through zip entries...
            for zip_entry in zip.namelist():
                zip_entry_count = zip_entry_count + 1
                                
                # Directory...
                if zip_entry.endswith( '/' ):
                    dir_path = os.path.join ( skin_install_dir, zip_entry )
                    
                    # Directory exists, ask to overwrite...
                    if os.path.isdir(dir_path):
                        answer_do_install = xbmcgui.Dialog().yesno( xbmc.getLocalizedString(30000), xbmc.getLocalizedString(30304) % skin_name )
                        if answer_do_install :
                            shutil.rmtree (dir_path)
                            os.mkdir (dir_path)
                        else :
                            skin_install_success = False
                            break
                    # Create directory...
                    else :
                        os.mkdir (dir_path)
                #
                # File...
                #
                else:
                    # Progress...
                    dp.update( int( zip_entry_count * 100 / zip_entry_total ), xbmc.getLocalizedString(30210) % skin_name, zip_entry )

                    # Extract file...
                    file_path = os.path.join(skin_install_dir, zip_entry)
                    outfile   = open(file_path, "wb")
                    outfile.write( zip.read(zip_entry) )
                    outfile.close()
            
            # Clean-up...
            zip.close()
            dp.close()
            
        # RAR
        else :
            dp = xbmcgui.DialogProgress()
            dp.create(xbmc.getLocalizedString(30000), xbmc.getLocalizedString(30303) % skin_name)        
            xbmc.executebuiltin( "XBMC.extract(%s,%s)" % ( skin_archive_local, skin_install_dir ) )
            dp.close()
        
        # Done
        if skin_install_success :
            xbmcgui.Dialog().ok( xbmc.getLocalizedString(30000), xbmc.getLocalizedString(30305) + "\n" + skin_install_dir)
        
        # Cleanup...
        os.remove( xbmc.translatePath( skin_archive_local ) )

#
# AppURLOpener
#
class AppURLopener(urllib.FancyURLopener):
    version = "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729)"

#
# EOF
#