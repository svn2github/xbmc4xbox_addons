#===============================================================================
# LICENSE XOT-Framework - CC BY-NC-ND
#===============================================================================
# This work is licenced under the Creative Commons 
# Attribution-Non-Commercial-No Derivative Works 3.0 Unported License. To view a 
# copy of this licence, visit http://creativecommons.org/licenses/by-nc-nd/3.0/ 
# or send a letter to Creative Commons, 171 Second Street, Suite 300, 
# San Francisco, California 94105, USA.
#===============================================================================
import os
import sys

import xbmc
import xbmcgui

class EnvController:
    """Controller class for getting all kinds of information about the
    XBMC environment."""
    
    def __init__(self, logger=None):
        """Class to determine platform depended stuff
        
        Keyword Arguments:
        logger : Logger - a logger object that is used to log information to
                
        """
        
        self.logger = logger
        pass
    
    def GetPythonVersion(self):
        """Returns the current python version
        
        Returns:
        Python version in the #.#.# format
        
        """
        
        major = sys.version_info[0]
        minor = sys.version_info[1]
        build = sys.version_info[2]
        return "%s.%s.%s" % (major, minor, build)
    
    def GetEnvironmentFolder(self):
        """Returns the correct environment folder to import libraries from
        
        Returns:
        A folder name that can be used append to the Python path to import platform 
        dependent packages from for current environment:
        
        * Linux   - Normal Linux packages
        * Linux64 - 64-bit Linux packages
        * OS X    - For Apple devices
        * win32   - Windows / Native Xbox packages
        
        If the Python version is higher than 2.4, then a non standard XBMC Python is used 
        from which we import packages. In that case we return "".
        
        """

        major = sys.version_info[0]
        minor = sys.version_info[1]
        
        if major > 2 or minor > 4:            
            # this is not the default XBMC python, so use it's own modules
            return "" 
        else:
            return self.GetEnvironment()
    
    def GetEnvironment(self):
        """Gets the type of environment
        
        Returns:
        A string defining the OS:
        * Linux   - Normal Linux
        * Linux64 - 64-bit Linux
        * OS X    - For Apple decices
        * win32   - Windows / Native Xbox       
        
        """
        
        env = os.environ.get("OS", "win32")        
        if env == "Linux":
#            (bits, type) = platform.architecture()
#            if bits.count("64") > 0:
#                # first the bits of platform.architecture is checked
#                return "Linux64"
            if sys.maxint >> 33:
                # double check using the sys.maxint
                # and see if more than 32 bits are present
                return "Linux64"
            else:
                return "Linux"
        elif env == "OS X":
            return "OS X"
        else: 
            return "win32"
        
    def IsInstallMethodValid(self, config):
        """ Validates that XOT-uzg.v3 is installed using the repository. If not
        it will popup a dialog box.        
        
        Arguments:
        config : Config - The XOT-Uzg.v3 config object.
        
        """
        
        repoAvailable = self.__IsRepoAvailable(config)
        
        if (not repoAvailable):
            # show alert
            msgBox = xbmcgui.Dialog()
            ok = msgBox.ok("Repository Warning", "The XOT-Uzg.v3 repository is not installed.\nPlease install it to allow future updates.")
        
        return repoAvailable
        
    
    def DirectoryPrinter(self, config, settingInfo):
        """Prints out all the XOT related directories to the logFile.
        
        This method is mainly used for debugging purposes to provide developers a better insight
        into the system of the user. 
        
        """
        
        try:
            directory = "<Unknown>"
            
            version = xbmc.getInfoLabel("system.buildversion")
            buildDate = xbmc.getInfoLabel("system.builddate")

            repoName = self.__IsRepoAvailable(config, returnName=True) 
            
            envCtrl = EnvController()
            env = envCtrl.GetEnvironment()
            
            infoString = "%s: %s" % ("Version", version)
            infoString = "%s\n%s: %s" % (infoString, "BuildDate", buildDate)
            infoString = "%s\n%s: %s (folder=\libs\%s)" % (infoString, "Environment", env, envCtrl.GetEnvironmentFolder())
            infoString = "%s\n%s: %s" % (infoString, "Platform", envCtrl.GetPlatform(True))
            infoString = "%s\n%s: %s" % (infoString, "Python Version", envCtrl.GetPythonVersion())
            infoString = "%s\n%s: %s" % (infoString, "XOT-Uzg.v3 Version", config.Version)
            infoString = "%s\n%s: %s" % (infoString, "AddonID", config.addonId)
            infoString = "%s\n%s: %s" % (infoString, "Path", config.rootDir)
            infoString = "%s\n%s: %s" % (infoString, "ProfilePath", config.profileDir)
            infoString = "%s\n%s: %s" % (infoString, "PathDetection",config.pathDetection)
            infoString = "%s\n%s: %s" % (infoString, "Encoding", sys.getdefaultencoding())
            infoString = "%s\n%s: %s" % (infoString, "Repository", repoName)
            self.logger.info("XBMC Information:\n%s", infoString)
            
            # log the settings
            self.logger.info("XOT-Uzg Settings:\n%s", settingInfo)
            
            # get the script directory
            dirScript = config.addonDir
            dirWalker = os.walk(os.path.realpath(os.path.join(config.rootDir, "..")))
            dirPrint = "Folder Structure of %s (%s)" % (config.appName, dirScript)        
            
            excludePattern = os.path.join('a','.svn').replace("a","")
            for directory, folders, files in dirWalker:
                if directory.count(excludePattern) == 0:
                    if directory.count(dirScript) > 0 and directory.count("BUILD") == 0:
                        for fileName in files:
                            if not fileName.startswith(".") and not fileName.endswith(".pyo"):
                                dirPrint = "%s\n%s" % (dirPrint, os.path.join(directory, fileName))
            self.logger.debug("%s" % (dirPrint))
        except:
            self.logger.critical("Error printing folder %s", directory, exc_info=True)
    #===========================================================================
    @staticmethod
    def GetPlatform(returnName=False):
        """Returns the platform that XBMC returns as it's host:
        
        Keyword Arguments:
        returnName : boolean - If true a string value is returned
        
        Returns:
        A string representing the host OS:        
        * linux   - Normal Linux
        * Xbox    - Native Xbox
        * OS X    - Apple OS
        * Windows - Windows OS  
        * unknown - in case it's undetermined
                
        """
        
        platform = Environments.Unknown
        
        if xbmc.getCondVisibility("system.platform.linux"):
            platform = Environments.Linux
        elif xbmc.getCondVisibility("system.platform.xbox"):
            platform = Environments.Xbox
        elif xbmc.getCondVisibility("system.platform.windows"):
            platform = Environments.Windows
        elif xbmc.getCondVisibility("system.platform.ios"):
            platform = Environments.IOS
        elif xbmc.getCondVisibility("system.platform.atv2"):
            platform = Environments.ATV2        
        elif xbmc.getCondVisibility("system.platform.osx"):
            platform = Environments.OSX
        
        if (returnName):
            return Environments.Name(platform)
        else:
            return platform
    
    @staticmethod
    def IsPlatform(platform):
        """Checks if the current platform matches the requested on
        
        Arguments:
        platform : string - The requested platform
        
        Returns:
        True if the <platform> matches EnvController.GetPlatform().
        
        """
        
        plat = EnvController.GetPlatform()        
        
        # check if the actual platform is in the platform bitmask        
        #return plat & platform  == platform   
        return platform  & plat == plat
    
    @staticmethod
    def GetSkinFolder(rootDir, logFile):
        """Returns the folder that matches the currently active XBMC skin
        
        Arguments:
        rootDir : String - rootfolder of XOT
        logFile : Logger - logger to write logging to
        
        Returns:
        The name of the skinfolder that best matches the XBMC skin.
        
        It looks at the current XBMC skin folder name and tries to match it to
        a skin in the resources/skins/skin.<skin> or resources/skins/<skin> path. 
        If a match was found that foldername is returned. If no match was found
        the default skin for XOT (skin.xot) is returned.
        
        """
        
        skinName = xbmc.getSkinDir()
        if (os.path.exists(os.path.join(rootDir,"resources","skins",skinName))):
            skinFolder = skinName
        elif (os.path.exists(os.path.join(rootDir, "resources", "skins", "skin." + skinName.lower()))):
            skinFolder = "skin.%s" % (skinName.lower(), )
        else:
            skinFolder = "skin.xot"    
        logFile.info("Setting Skin to: " + skinFolder)
        return skinFolder
 
    def __IsRepoAvailable(self, config, returnName=False):
        """ Checks if the repository is available in XBMC and returns it's name.
        
        Arguments:
        config     : Config  - The configuration object of XOT-Uzg.v3
        
        Keyword Arguments:
        returnName : Boolean - [opt] If set to True the name of the repository will
                               be returned or a label with the reason why no repo 
                               was found.
        
        """
        
        NOT_INSTALLED = "<not installed>" 
        
        if (EnvController.IsPlatform(Environments.Xbox)):
            if returnName:
                # on Xbox it's never installed.
                return NOT_INSTALLED
            else:
                # always return True for Xbox
                return True
        
        try:
            repoName = "%s.repository" % (config.addonId,)
            repoAvailable = xbmc.getCondVisibility('System.HasAddon("%s")' % (repoName,)) == 1

            if not returnName:
                # return a boolean
                return repoAvailable
            elif repoAvailable:
                # return the name if it was available
                return repoName
            else:
                # return not installed if non was available
                return NOT_INSTALLED 
        except:
            self.logger.error("Error determining Repository Status", exc_info=True)
            if not returnName:
                # in case of error, return True
                return True
            else:
                return "<error>"
    
class Environments:

    """Enum class that holds the environments"""

    Unknown = 1
    Xbox = 2
    Linux = 4
    Windows = 8
    OSX = 16
    ATV2 = 32
    IOS = 64
    
    # special groups
    All = Unknown | Xbox | Linux | Windows | OSX | ATV2 | IOS
    Apple = OSX | ATV2 | IOS

    @staticmethod
    def Name(environment):
        """Returns a string representation of the Environments
        
        Arguments:
        environment : integer - The integer matching one of the  
                                environments enums.
        
        Returns a string                
        """
        
        if (environment == Environments.OSX):
            return "OS X"
        elif (environment == Environments.Windows):
            return "Windows"
        elif (environment == Environments.Xbox):
            return "Xbox"
        elif (environment == Environments.Linux):
            return "Linux" 
        elif (environment == Environments.IOS):
            return "iOS"
        elif (environment == Environments.ATV2):
            return "Apple TV2"
        else:
            return "Unknown"