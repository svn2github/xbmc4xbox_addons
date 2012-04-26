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
import re
import sys
import time

from config import Config

#===============================================================================
# Make global object available
#===============================================================================
logFile = sys.modules['__main__'].globalLogFile
uriHandler = sys.modules['__main__'].globalUriHandler
#===============================================================================
    
#===============================================================================
def DoRegexFindAll(regex, data):
    """Performs a regular expression
    
    Arguments:
    regex : string - the regex to perform on the data.
    data  : string - the data to perform the regex on.
    
    Returns:
    A list of matches that came from the regex.findall method.
    
    Performs a regular expression findall on the <data> and returns the results
    that came from the method.     
    
    From the sre.py library:
    If one or more groups are present in the pattern, return a
    list of groups; this will be a list of tuples if the pattern
    has more than one group.

    Empty matches are included in the result.
    
    """
    
    try:
        result = re.compile(regex, re.DOTALL + re.IGNORECASE)
        if "?P<" in regex:        
            it = result.finditer(data)    
            return map(lambda x : x.groupdict(), it)
        else:
            return result.findall(data)
    except:
        logFile.critical('error regexing', exc_info=True)
        return []

def CacheCheck():
    """Checks if the cache folder exists. If it does not exists
    It will be created.
    
    Returns False it the folder initially did not exist
    
    """
    
    #check for cache folder. If not present. Create it!
    if not os.path.exists(Config.cacheDir):
        logFile.info("Creating cache folder at: %s", Config.cacheDir)
        os.makedirs(Config.cacheDir)
        return False
    
    return True
    

def CacheCleanUp():
    """Cleans up the XOT cache folder. 
    
    Check the cache files create timestamp and compares it with the current datetime extended
    with the amount of seconds as defined in Config.cacheValidTime.
    
    Expired items are deleted. 
    
    """
    
    try:
        deleteCount = 0
        fileCount = 0
        for item in os.listdir(Config.cacheDir):
            fileName = os.path.join(Config.cacheDir, item)
            if os.path.isfile(fileName):
                fileCount = fileCount + 1
                createTime = os.path.getctime(fileName)
                if createTime + Config.cacheValidTime < time.time():
                    os.remove(fileName)
                    deleteCount = deleteCount + 1
        logFile.info("Removed %s of %s files from cache in: '%s'", deleteCount, fileCount, Config.cacheDir)
    except:
        logFile.critical("Error cleaning the cachefolder", exc_info=True)    