#===============================================================================
# LICENSE XOT-Framework - CC BY-NC-ND
#===============================================================================
# This work is licenced under the Creative Commons 
# Attribution-Non-Commercial-No Derivative Works 3.0 Unported License. To view a 
# copy of this licence, visit http://creativecommons.org/licenses/by-nc-nd/3.0/ 
# or send a letter to Creative Commons, 171 Second Street, Suite 300, 
# San Francisco, California 94105, USA.
#===============================================================================
import os.path
import sys
import traceback

import xbmcgui

try:
    import xbmcaddon
    addon = xbmcaddon.Addon()
    path = addon.getAddonInfo('path')
except:
    path = os.getcwd()
    
# the XBMC libs return unicode info, so we need to convert this
path = path.decode('utf-8')#.encode('latin-1')
sys.path.append(os.path.join(path.replace(";",""),'resources','libs'))

# SHOULD ONLY BE ENABLED FOR REMOTE DEBUGGING PURPOSES
import remotedebugger 
debugger = remotedebugger.RemoteDebugger()

# just make a dummy globalUriHandler to prevent import errors
globalUriHandler = None
globalLogFile = None

import envcontroller
envController = envcontroller.EnvController()
env = envController.GetEnvironmentFolder()

sys.path.append(os.path.join(path.replace(";",""),'resources','libs', env))
#===============================================================================
# Handles an AttributeError during intialization
#===============================================================================
def HandleInitAttributeError(loadedModules):
    if(globalLogFile):
        globalLogFile.critical("AtrributeError during intialization", exc_info=True)
        if ("config" in loadedModules):
            globalLogFile.debug("'config' was imported from %s", Config.__file__)
        if ("logger" in loadedModules):
            globalLogFile.debug("'logger' was imported from %s", logger.__file__)
        if ("uriopener" in loadedModules):
            globalLogFile.debug("'uriopener' was imported from %s", uriopener.__file__)
        if ("common" in loadedModules):
            globalLogFile.debug("'common' was imported from %s", common.__file__)
        if ("update" in loadedModules):
            globalLogFile.debug("'update' was imported from %s", update.__file__)
    else:
        traceback.print_exception(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2])
        if ("config" in loadedModules):
            print("'config' was imported from %s" % Config.__file__)
        if ("logger" in loadedModules):
            print("'logger' was imported from %s" % logger.__file__)
        if ("uriopener" in loadedModules):
            print("'uriopener' was imported from %s" % uriopener.__file__)
        if ("common" in loadedModules):
            print("'common' was imported from %s" % common.__file__)
        if ("update" in loadedModules):
            print("'update' was imported from %s" % update.__file__)   
    return  

#===============================================================================
# Here the script starts
#===============================================================================
# Check for function: Plugin or Script
if hasattr(sys, "argv") and len(sys.argv) > 1:
    #===============================================================================
    # PLUGIN: Import XOT stuff
    #===============================================================================
    try:
        from config import Config
        import logger
        
        if sys.argv[2].strip('?') == "":
            # first call in the cycle, so cleanup log
            appendLogFile = False
        else:
            appendLogFile = True
        globalLogFile = logger.Customlogger(os.path.join(Config.rootDir, Config.logFileNamePlugin), Config.logLevel, Config.logDual, append=appendLogFile)
        
        import uriopener
        import settings
        #useProgressBars = not envcontroller.EnvController.IsPlatform(envcontroller.Environments.Xbox)
        useCaching = settings.AddonSettings().CacheHttpResponses()
        globalUriHandler = uriopener.UriHandler(useProgressBars=False, useCaching=useCaching)        
        
        import common
        Config.skinFolder = envcontroller.EnvController.GetSkinFolder(Config.rootDir, globalLogFile)
        
        import plugin
        tmp = plugin.XotPlugin(sys.argv[0], sys.argv[2], sys.argv[1])
        
        # close the log to prevent locking on next call
        globalLogFile.CloseLog()
    except AttributeError:
        HandleInitAttributeError(dir())
    except:
        #globalLogFile.critical("Error initializing %s plugin", Config.appName, exc_info=True)
        try:
            orgEx = sys.exc_info()
            globalLogFile.critical("Error initializing %s plugin", Config.appName, exc_info=True)
        except:
            print "Exception during the initialisation of the script. No logging information was present because the logger was not loaded."
            traceback.print_exception(orgEx[0], orgEx[1], orgEx[2])       
else:
    #===============================================================================
    # SCRIPT: Setup the script
    #===============================================================================
    try:
        pb = xbmcgui.DialogProgress()
        from config import Config
        pb.create("Initialising %s" % (Config.appName), "Importing configuration")
        
        pb.update(10,"Initialising Logger")
        import logger
        globalLogFile = None
        globalLogFile = logger.Customlogger(os.path.join(Config.rootDir, Config.logFileName), Config.logLevel, Config.logDual)
        
        pb.update(25,"Initialising UriHandler")
        import uriopener
        import settings
        useCaching = settings.AddonSettings().CacheHttpResponses()
        globalUriHandler = uriopener.UriHandler(useCaching=useCaching)        
        
        pb.update(30,"Importing common libraries")
        import common
        envCntrl = envcontroller.EnvController(globalLogFile)
        envCntrl.DirectoryPrinter(Config, settings.AddonSettings())
        
        pb.update(40,"Determining SkinFolder")
        Config.skinFolder = envcontroller.EnvController.GetSkinFolder(Config.rootDir, globalLogFile)        
        
        globalLogFile.info("************** Starting %s version v%s **************", Config.appName, Config.Version)
        globalLogFile.info("Skinfolder = %s", Config.skinFolder)
        print("************** Starting %s version v%s **************" % (Config.appName, Config.Version))
        
        #check for updates
        pb.update(50,"Checking for updates")
        import update
        try:
            update.CheckVersion(Config.Version, Config.updateUrl)
            pass
        except:
            globalLogFile.critical("Error checking for updates", exc_info=True)
        
        pb.update(60,"Verifying the Repository")
        envCntrl.IsInstallMethodValid(Config)
        
        pb.update(70,"Checking for Cache folder")
        common.CacheCheck()
        
        pb.update(80, "Cleaning up Cachefolder")
        #cleanup the cachefolder
        common.CacheCleanUp()
        
        pb.close()
        
        #===============================================================================
        # Now starting the real app
        #===============================================================================
        if not pb.iscanceled():
            import progwindow
            
            MyWindow = progwindow.GUI(Config.appSkin ,Config.rootDir, Config.skinFolder)
            MyWindow.doModal()
            del MyWindow
        else:
            # close the log to prevent locking on next call
            globalLogFile.CloseLog()
        
    except AttributeError:
        HandleInitAttributeError(dir())        
    except:
        try:
            orgEx = sys.exc_info()
            globalLogFile.critical("Error initializing %s script", Config.appName, exc_info=True)
            
            # close the log to prevent locking on next call
            globalLogFile.CloseLog()        
        except:
            print "Exception during the initialisation of the script. No logging information was present because the logger was not loaded."
            traceback.print_exception(orgEx[0], orgEx[1], orgEx[2])            
        pb.close()