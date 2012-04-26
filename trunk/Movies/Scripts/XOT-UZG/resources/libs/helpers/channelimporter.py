#===============================================================================
# LICENSE XOT-Framework - CC BY-NC-ND
#===============================================================================
# This work is licenced under the Creative Commons 
# Attribution-Non-Commercial-No Derivative Works 3.0 Unported License. To view a 
# copy of this licence, visit http://creativecommons.org/licenses/by-nc-nd/3.0/ 
# or send a letter to Creative Commons, 171 Second Street, Suite 300, 
# San Francisco, California 94105, USA.
#===============================================================================

#===============================================================================
# Import the default modules
#===============================================================================
import sys
import os
import shutil

import settings
import common
import envcontroller
import guicontroller
import version
from stopwatch import StopWatch
from config import Config


#===============================================================================
# Make global object available
#===============================================================================
logFile = sys.modules['__main__'].globalLogFile

class ChannelImporter:
    """Class that handles the deploying and loading of available channels."""
    
    def __init__(self):
        """Initialize the importer by reading the channels from the channel 
        resource folder and will start the import of the channels
        
        The basic idea behind the class:
        - progwindow or plugin creates a single and global instance of this 
          item called "channelRegister"
        - all channel call channelRegister.RegisterChannel(..)
        - so all channels are known to this object
        - then we can query it for channels or a specific channel
        
        It also deploys the channels from the xot\deploy folder.
        
        """
        
        self.__INTERNAL_CHANNEL_PATH = "channels"
        
        # initialise the collections
        self.__channelsToImport = []      # list for channels to register themselves
        self.__enabledChannels = []       # list of all loaded channels (after checking languages and so)
        self.__allChannels = []           # list of all available channels
        self.__channelVersions = []       # list of channelname+version that were found
        
        self.__addonSettings = settings.AddonSettings()
        self.__DeployNewChannels()
        return
    
    def GetChannels(self, includeDisabled = False):
        """Retrieves the available channels. If the channels were not already
        loaded, it will import them.
        
        Keyword Arguments:
        includeDisabled : boolean - If set to true, all channels are loaded 
                                    including those that were disabled due to
                                    language restrictions or incompatible 
                                    operating systems.
        
        Returns:
        A list of <Channel> objects
        
        """
        if self.__enabledChannels == []:
            self.__ImportChannels()
        
        if (includeDisabled):
            result = self.__allChannels
        else:
            result = self.__enabledChannels
        
        # Order them by channelName MUST Also sort the buttons
        if len(result) > 0:            
            return result 
        else:
            return []

    def GetSingleChannel(self, className, channelCode):
        """Imports a single channel
        
        Arguments:
        className : string - class name of the channel to import.
    
        Returns:
        The channels in the requested class. So that could be more, but they
        can be distinguished using the channelcode. 
        
        Returns an empty list if no channels were found.
        
        """
        
        logFile.info("Loading channels for class '%s' and channelCode '%s'", className, channelCode)
        if self.__enabledChannels == []:
            self.__ImportChannels()
        
        # now we filter the channels
        results = filter(lambda c: c.moduleName.replace(".py", "") == className and c.channelCode == channelCode, self.__enabledChannels)
        
        # Order them by channelName MUST Also sort the buttons
        logFile.info("GetSingleChannel resulted in %s channel(s)", len(results))
        if len(results) == 1:
            logFile.info("GetSingleChannel found: %s", results[0])
            return results[0] 
        else:
            return None
    
    def RegisterChannel(self, className, channelCode = None):
        """Called by each channel to register itself
        
        Arguments:
        className : string - name of the class file to import
        
        Keyword Arguments:
        channelCode : [opt] string - channelcode to import from the channel in
                                     case a class holds more than one channel.
        
        """
        
        self.__channelsToImport.append((className, channelCode))        
        return        

    def IsChannelInstalled(self, zipFileName):
        """Checks if the requested channel in the zipfile is already installed"""
        
        return zipFileName.replace(".zip", "") in self.__channelVersions

    @staticmethod
    def GetRegister():
        """Returns the current active channel register."""
        
        # determine the current register
        if (sys.modules.has_key('progwindow')):
            channelRegister = sys.modules['progwindow'].channelRegister
            #.channelRegister
        elif (sys.modules.has_key('plugin')):
            channelRegister = sys.modules['plugin'].channelRegister
        
        return channelRegister
        
    def __DeployNewChannels(self):
        """Checks the deploy folder for new channels, if present, deploys them
        
        The last part of the folders in the deploy subfolder are considered the 
        channel names. The other part is replaced with the <addon base name>. 
        So if the deploy has a folder temp.channelOne and the addon is called 
        net.rieter.xot it will be deployed to net.rieter.xot.channel.channelOne.
        
        The folders are intially removed and then re-created. If the folder in 
        the deploy does not have a addon.xml it will not be imported.
        
        """
        
        logFile.debug("Checking for new channels to deploy")
        
        # location of new channels and list of subfolders
        deployPath = os.path.join(Config.rootDir, "deploy")
        toDeploy = os.listdir(deployPath)
        
        # addons folder, different for XBMC and XBMC4Xbox
        if envcontroller.EnvController.IsPlatform(envcontroller.Environments.Xbox):
            targetFolder = os.path.realpath(os.path.join(Config.rootDir, self.__INTERNAL_CHANNEL_PATH))
            if not os.path.exists(targetFolder):
                os.mkdir(targetFolder)
        else:
            targetFolder = os.path.realpath(os.path.join(Config.rootDir, ".."))
            
        for deploy in toDeploy:
            if deploy.startswith("."):
                continue
            sourcePath = os.path.join(deployPath, deploy)
            
            # find out if the scriptname is not net.rieter.xot and update
            deployParts = deploy.split(".")
            # channels addons always end with .channel.name
            destDeploy = "%s.channel.%s" % (Config.addonDir, deployParts[-1])
            
            destinationPath = os.path.join(targetFolder, destDeploy)
            logFile.info("Deploying Channel Addon '%s' to '%s'", deploy, destinationPath)
            
            if os.path.exists(destinationPath):
                logFile.info("Removing old channel at %s", destDeploy)
                shutil.rmtree(destinationPath)
            
            # only update if there was a real addon
            if os.path.exists(os.path.join(sourcePath, "addon.xml")):
                shutil.move(sourcePath, destinationPath)
            else:
                shutil.rmtree(sourcePath)
        
        return
    
    def __ShowFirstTime(self, channelName, channelPath):
        """ Checks if it is the first time a channel is executed 
        and if a first time message is available it will be shown
        
        Arguments:
        channelName : string - Name of the channelfile that is loaded
        channelPath : string - Path of the channelfile
        
        Shows a message dialog if the message should be shown.
        
        Make sure that each line fits in a single line of a XBMC Dialog box (50 chars)
        
        """
        
        MESSAGE_FILENAME = "message.txt"
        
        messagePath = os.path.join(channelPath, MESSAGE_FILENAME)
        if os.path.exists(messagePath):
            #logFile.debug("Channel Info %s found for channel chn_%s", MESSAGE_FILENAME, channelName)
            compiledName = "chn_%s.pyc" % (channelName,)
            optimizedName = "chn_%s.pyo" % (channelName,)
            
            # show the first time message when no Optimezed (.pyo) and no Compiled (.pyc) files are there 
            if not os.path.exists(os.path.join(channelPath, compiledName)) and not os.path.exists(os.path.join(channelPath, optimizedName)):
                logFile.info("Showing first time message '%s' for channel chn_%s", MESSAGE_FILENAME, channelName)
                title = "%s channel message" % (Config.appName,)
                
                content = open(messagePath, 'r')
                lines = content.readlines()
                content.close()
                
                guicontroller.GuiController.ShowDialog(title, lines)
            
        return
    
    def __ImportChannels(self):#, className = None):
        """Import the available channels
        
        This method will:
         - iterate through the Addons folder and find all the folders name 
           <basename>.channel.<channelname>.
         - then adds all the subfolders into a list (with paths).
         - then all paths are added to the system path, so they can be imported.
         - then imports all the channel class files. 
         - each file registers their channels in the self.__channelsToImport using 
           the RegisterChannel method.
         - then the channels in the self.__channelsToImport list are instantiated
           into the self.channels list.
        
        """
        
        logFile.info("Importing available channels")
        # import each channelPath. On import, the channelPath will call the RegisterChannel Method        
        try:            
            # clear a possible previous import
            self.__enabledChannels = []
            self.__allChannels = []
            self.__channelsToImport =  []
            self.__channelVersions = []
            
            # first find all folders with channels that we might need to import
            channelImport = []  
            importTimer = StopWatch("ChannelImporter :: importing channels", logFile)
            
            # get the script directory
            dirScript = Config.addonDir
            
            # different paths for XBMC and XBMC4Xbox
            if envcontroller.EnvController.IsPlatform(envcontroller.Environments.Xbox):
                addonPath = os.path.realpath(os.path.join(Config.rootDir, self.__INTERNAL_CHANNEL_PATH))
                pass
            else:
                addonPath = os.path.realpath(os.path.join(Config.rootDir, ".."))
            
            for directory in os.listdir(addonPath):
                if directory.count(dirScript +".channel") > 0 and directory.count("BUILD") == 0:
                    #logFile.debug(directory)        
                    path = os.path.join(addonPath, directory)    
                    #logFile.debug(path)
                    
                    # continue if no addon.xml exists 
                    if not os.path.exists(os.path.join(path, "addon.xml")):
                        continue
                    
                    f = open(os.path.join(path, "addon.xml"), 'r+')
                    addonXml = f.read()
                    f.close        
                    
                    packVersion = common.DoRegexFindAll('id="([^"]+)"\W+version="([^"]{5,10})"', addonXml)
                    if len(packVersion) > 0:
                        # Get the first match
                        packVersion = packVersion[0]
                        
                        packageId = packVersion[0]
                        packageVersion = version.Version(version=packVersion[1])                        
                        #channelAddon = os.path.split(path)[-1]
                        #packVersion = packVersion.
                        if Config.Version.EqualRevisions(packageVersion):
                            logFile.debug("Loading %s version %s", packageId, packageVersion)
                            
                            # save to the list of present items, for querying in the 
                            # future (xbox updates)
                            channelVersionID = "%s-%s" % (packVersion[0], packVersion[1])
                            self.__channelVersions.append(channelVersionID)
                        else:
                            logFile.debug("Skipping %s version %s: Versions do not match.", packageId, packageVersion)
                            continue                        
                    else:
                        logFile.critical("Cannot determine channel version. Not loading channel @ '%s'", path)
                        continue
                    

                    
                    subDirs = os.listdir(path)
                    
                    # if we need a specific class, just get that one
                    channelImport.extend([os.path.realpath(os.path.join(path, weapon)) for weapon in subDirs])

            channelImport.sort()
            importTimer.Lap()
            
            # we need to make sure we don't load multiple channel classes!
            loadedChannels = []
            for channelPath in channelImport:
                if os.path.isdir(channelPath):
                    #determine channelname                            
                    channelName = os.path.split(channelPath)[-1]
                    if loadedChannels.count(channelName) > 0:
                        logFile.warning("Not loading: chn_%s in %s because there is already a path with name %s that name loaded", channelName, channelPath, channelName)
                        continue
                    
                    if channelName.startswith("."):
                        continue
                    
                    # check for first time messages
                    self.__ShowFirstTime(channelName, channelPath)                    
                    
                    # now import
                    sys.path.append(channelPath)
                    loadedChannels.append(channelName)
                    
                    logFile.info("Importing chn_%s", channelName)
                    try:
                        exec("import chn_%s" % channelName)
                    except:
                        logFile.error("Error import chn_%s", channelName, exc_info=True)
                                             
            importTimer.Lap()
            #channels imported, but not initialised, that happens in the __init__!
            
            # What platform are we
            platform = envcontroller.EnvController.GetPlatform()
            
            # instantiate the registered channels   
            for (className, channelCode) in self.__channelsToImport:
                #logFile.debug("Creating channelPath '%s' with code '%s'", className, channelCode)
                # Create channelPath object        
                if channelCode == None:
                    channelCommand = '%s.Channel()' % (className,)
                else:
                    channelCommand = '%s.Channel(channelCode="%s")' % (className, channelCode)
                
                try:
                    channelPath = eval(channelCommand)
                    
#                    # Check for out of date channelPath
#                    if channelPath.OutOfDate:
#                        logFile.warning("Not loading: %s -> out of date", channelPath)
#                        #del channelPath
#                        continue
                    
                    if self.__enabledChannels.count(channelPath) > 0:
                        existingChannel = self.__enabledChannels[self.__enabledChannels.index(channelPath)]
                        logFile.error("Not loading: %s -> a channel with the same guid already exist:\n%s.", channelPath, existingChannel)
                        #del channelPath
                        continue
                    
                    # store all the channels except the out of date and duplicate ones, we might need them somewhere
                    self.__allChannels.append(channelPath)
                    
                    if not self.__addonSettings.ShowChannelWithLanguage(channelPath.language):
                        logFile.warning("Not loading: %s -> language (%s) is disabled", channelPath, channelPath.language)
                        #del channelPath
                        continue
                        
                    if not channelPath.compatiblePlatforms & platform == platform:
                        logFile.warning("Not loading: %s -> platform '%s' is not compatible", channelPath, envcontroller.Environments.Name(platform))
                        #del channelPath
                        continue
                    
                    logFile.debug("Initialized: %s", channelPath)
                    
                    #add to channelPath list        
                    self.__enabledChannels.append(channelPath)
                    #logFile.info("Adding %s to channels", channelPath)
                except:
                    logFile.error("Error Creating channel %s (%s) using command: %s", className, channelCode, channelCommand, exc_info=True)
                        
            # sort the channels
            self.__enabledChannels.sort()
            self.__allChannels.sort()
            logFile.info("Imported %s channels from which %s are enabled", len(self.__allChannels), len(self.__enabledChannels))
            importTimer.Stop()
        except:
            logFile.critical("Error loading channel modules", exc_info=True)        
    