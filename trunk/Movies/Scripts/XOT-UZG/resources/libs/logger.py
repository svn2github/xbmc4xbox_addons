#===============================================================================
# LICENSE XOT-Framework - CC BY-NC-ND
#===============================================================================
# This work is licenced under the Creative Commons 
# Attribution-Non-Commercial-No Derivative Works 3.0 Unported License. To view a 
# copy of this licence, visit http://creativecommons.org/licenses/by-nc-nd/3.0/ 
# or send a letter to Creative Commons, 171 Second Street, Suite 300, 
# San Francisco, California 94105, USA.
#===============================================================================
import xbmc

import os
import sys
import string
import re
import traceback
import time
import datetime

#===============================================================================
# Define levels (same as Python's loglevels)
#===============================================================================
CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0

class Customlogger:
    """Logger class that is used for logging to a certain file. It's faster 
    than the normal Python logging class and has more custom options.  

    It appears as a default Python logger and has these log methods:
    * debug
    * info
    * warning
    * error
    * critical
    
    Has a subclass __Write that 
    does the work!
    
    """

    def __init__(self, logFileName, minLogLevel, logDual, append=False, logFreeMemory=True):
        """Intialises the Logger Instance and opens it for writing
        
        Arguments:
        logFile    : string  - Path of the log file to write to
        minLogLeve : integer - Minimum log level to log. Levels equal or higher 
                               are logged.
        logDual    : boolean - If set to True, exceptions are also written to the
                               standard out.
        
        Keyword Arguments:
        append     : [opt] bool - If set to True, the current log file is not deleted.
                                  Default value is False.
        logFreeMemory  : [opt] bool - If true, memory is logged as first parameter
        
        """

        self.logFileName = logFileName
        self.fileMode = "a"
        self.fileFlags = os.O_WRONLY|os.O_APPEND|os.O_CREAT
        self.logFreeMemory = logFreeMemory
        
        self.minLogLevel = minLogLevel
        self.logDual = logDual
        self.logEntryCount = 0
        self.flushInterval = 5
        self.encoding = 'cp1252'
        #self.logHandle = -1
        self.id = int(time.time())        
        
        if self.logFreeMemory:
            #self.logFormat = "%s%s, %-4s%s" % ('%s - [', self.id, xbmc.getFreeMem(), 'MB] %-8s - %-20s - %-4d - %s\n')
            self.logFormat = "%s%-4s%s" % ('%s - [', xbmc.getFreeMem(), 'MB] %-8s - %-20s - %-4d - %s\n')                            
        else:
            self.logFormat = '%s - %-8s - %-20s - %-4d - %s\n'
        
        self.logLevelNames = {
            CRITICAL : 'CRITICAL',
            ERROR : 'ERROR',
            WARNING : 'WARNING',
            INFO : 'INFO',
            DEBUG : 'DEBUG',
            NOTSET : 'NOTSET',
            'CRITICAL' : CRITICAL,
            'ERROR' : ERROR,
            'WARN' : WARNING,
            'WARNING' : WARNING,
            'INFO' : INFO,
            'DEBUG' : DEBUG,
            'NOTSET' : NOTSET,
        }
        
        if not append:
            self.CleanUpLog()
            
        # now open the file
        self.__OpenLog()
        #self.debug("LogFile opened with mode %s", self.logHandle.encoding)
    
    def CloseLog(self, logClosing = True):
        """Close the logfile. 
        
        Calling close() on a filehandle also closes the FileDescriptor
        
        Keyword Arguments:
        logClosing : boolean - indicates whether a log line is written on closure.
        
        """
        
        if logClosing:
            self.info("XOT Logger :: Flushing and closing logfile.")
        
        self.logHandle.flush()
        self.logHandle.close()
        
    def CleanUpLog(self):
        """Closes an old log file and creates a new one.
        
        This method renames the current log file to .old.log and creates a 
        new log file with the .log filename. 
        
        If the original file was open for writing/appending, the new file 
        will also be open for writing/appending
        
        """
        
        #create old.log file
        print "XOT-Uzg.v3 :: Cleaning up XOT logfile: %s" % (self.logFileName)
        try:
            wasOpen = True
            self.CloseLog(logClosing=False)
        except:
            wasOpen = False
            
        _oldFileName = string.replace(self.logFileName, ".log", ".old.log")
        if os.path.exists(self.logFileName):
            if os.path.exists(_oldFileName):
                os.remove(_oldFileName)
            os.rename(self.logFileName, _oldFileName)
            
        if wasOpen:
            self.__OpenLog()
        return            
            
    def __Write(self, msg, *args, **kwargs):
        """Writes the message to the log file taking into account 
        the given arguments and keyword arguments. 
        
        Arguments:
        msg    : string - The message to log
        args   : list   - List of arguments
        
        Keyword Arguments:
        kwargs : list - List of keyword arguments 
        
        The arguments and keyword arguments are used in a string format way
        so and will replace the parameters in the message. 
        
        """
        
        try:            
            self.timeFormat = "%Y%m%d %H:%M:%S"
            self.logLevel = kwargs["level"]
            
            formattedMessage = ""            
            
            #determine if write is needed:
            if self.logLevel < self.minLogLevel:
                return
            
            # convert possible tupple to string:
            msg = str(msg)
            
            # Fill the message with it's content
            if len(args)>0:
                #print "# of args: %s" % (len(args[0]))
                msg = msg % args
            else:
                msg = msg
                
            # get frame information
            (sourceFile, sourceLineNumber) = self.__FindCaller()
            
            # get time information
            timestamp = datetime.datetime.today().strftime(self.timeFormat)
            
            # check for exception info, if present, add to end of string:
            if kwargs.has_key("exc_info"):
                if self.logDual:
                    traceback.print_exc()
                msg = "%s\n%s" % (msg, traceback.format_exc())
            
            # now split lines and write everyline into the logfile:
            result = re.compile("[\r\n]+", re.DOTALL + re.IGNORECASE)
            lines = result.split(msg)
            
            try:
            # check if multiline
                if len(lines)>1:
                    for line in lines:
                        if len(line) > 0:
                            # if last line:
                            if line == lines[-1]:
                                line = '+ %s' %(line)
                            elif line == lines[0]:
                                line = line
                            else:
                                line = '| %s' %(line)
                            formattedMessage = self.logFormat % (timestamp, self.logLevelNames.get(self.logLevel),sourceFile, sourceLineNumber, line)
                            self.logHandle.write(formattedMessage)
                else:
                    formattedMessage = self.logFormat % (timestamp,self.logLevelNames.get(self.logLevel),sourceFile, sourceLineNumber, msg)
                    self.logHandle.write(formattedMessage)
            except UnicodeEncodeError:
                #self.error("Unicode logging error", exc_info=True)
                formattedMessage = formattedMessage.encode('raw_unicode_escape')
                self.logHandle.write(formattedMessage)
                raise
                
            
            # Finally close the filehandle
            self.logEntryCount = self.logEntryCount + 1
            if self.logEntryCount % self.flushInterval == 0:
                #self.logHandle.write("Saving")
                self.logEntryCount = 0
                self.logHandle.flush()
            return
        except:
            print("XOT Logger :: Error logging in Logger.py:")
            print "---------------------------"
            traceback.print_exc()
            print "---------------------------"
            print repr(msg)
            print repr(args)
            print repr(formattedMessage)
            print "---------------------------"            
            
    def __FindCaller(self):
        """Find the stack frame of the caller.
        
        Find the stack frame of the caller so that we can note the source
        file name, line number and function name.
        
        """
        returnValue = ("Unknown", 0)
        
        # get the current frame and descent down until the correct one is found
        currentFrame = sys._getframe(3) # could be _getframe(#) with # from () to (3)
        while hasattr(currentFrame, "f_code"):
            co = currentFrame.f_code
            sourceFile = os.path.normcase(co.co_filename)
            methodName = co.co_name
            # if currentFrame belongs to this logger.py, equals <string> or equals a private log 
            # method (_log or __Log) continue searching.
            if sourceFile == "<string>" or sourceFile == os.path.normcase(__file__) or methodName in ("_Log", "__Log"):
                currentFrame = currentFrame.f_back
                continue
            else:
                # get the sourcePath and sourceFile
                (sourcePath, sourceFile) = os.path.split(sourceFile)
                returnValue = (sourceFile, currentFrame.f_lineno)       
                break

        return returnValue    
    
    def __OpenLog(self):
        """Opens the log file for appending
        
        This method opens a logfile for writing. If one already exists, it will
        be appended. If it does not exist, a new one is created. 
        
        Problem:
        If we would use open(self.logFileName, "a") we would get an invalid
        filedescriptor error in Linux!
        
        Possible fixes:
        1 - Modding the flags to only have os.O_CREATE if the file does not exists
            works, but then the file is appended at position 0 instead of the end!
          
        2 - Using a custom filedescriptor. This works, but now the file just keeps 
            getting overwritten.
          
        3 - OR: why not do a manual append: first read the complete file into a 
            string. Then do an open(self.logFileName, "w"), write the previous
            content and then just continue!              
           
        Finally: stick to the basic open(file, mode) and changes modes depending on 
        the available files.
           
        """
        
        if os.path.exists(self.logFileName):
            # the file already exists. Now to prevent errors in Linux
            # we will open a file in Read + (Read and Update) mode
            # and set the pointer to the end.
            self.logHandle = open(self.logFileName, "r+")            
            self.logHandle.seek(0, 2)
            self.info("XOT Logger :: Appending Existing logFile")
        else:
            # no file exists, so just create a new one for writing
            self.logHandle = open(self.logFileName, "w")

        return

#        # Option 1)
#        if os.path.exists(self.logFileName):
#            self.logHandle = open(self.logFileName, "a")
#        else:
#            self.logHandle = open(self.logFileName, "w")        
        
#        # Option 2
#        flags = self.fileFlags
#        
#        if not os.path.exists(self.logFileName):
#            # if it does not exists, set the flag to create it.
#            flags = flags | os.O_CREAT
#            
#        self.fileDescriptor = os.open(self.logFileName, flags)
        
#        self.fileDescriptor = os.open(self.logFileName, self.fileFlags)
#        self.logHandle = os.fdopen(self.fileDescriptor, self.fileMode)

#        # Option 3
#        previousData = ""
#        if os.path.exists(self.logFileName):
#            oldFile = open(self.logFileName, "r")
#            previousData = oldFile.read()
#            oldFile.close() 
#
#        self.logHandle = open(self.logFileName, "w")
#        self.logHandle.write(previousData)         
    
    def info(self, msg, *args, **kwargs):
        """Logs an informational message (with loglevel 20)
        
        Arguments:
        msg    : string - The message to log
        args   : list   - List of arguments
        
        Keyword Arguments:
        kwargs : list - List of keyword arguments 
        
        The arguments and keyword arguments are used in a string format way
        so and will replace the parameters in the message. 
        
        """
        
        self.__Write(msg, level=INFO, *args, **kwargs)
        return
    
    def error(self, msg, *args, **kwargs):
        """Logs an error message (with loglevel 40)
        
        Arguments:
        msg    : string - The message to log
        args   : list   - List of arguments
        
        Keyword Arguments:
        kwargs : list - List of keyword arguments 
                
        The arguments and keyword arguments are used in a string format way
        so and will replace the parameters in the message. 
        
        """
        
        self.__Write(msg, level=ERROR, *args, **kwargs)
        return
    
    def warning(self, msg, *args, **kwargs):
        """Logs an warning message (with loglevel 30)
        
        Arguments:
        msg    : string - The message to log
        args   : list   - List of arguments
        
        Keyword Arguments:
        kwargs : list - List of keyword arguments 
        
        The arguments and keyword arguments are used in a string format way
        so and will replace the parameters in the message. 
        
        """
        
        self.__Write(msg, level=WARNING, *args, **kwargs)
        return
    
    def debug(self, msg, *args, **kwargs):
        """Logs an debug message (with loglevel 10)
        
        Arguments:
        msg    : string - The message to log
        args   : list   - List of arguments
        
        Keyword Arguments:
        kwargs : list - List of keyword arguments 
        
        The arguments and keyword arguments are used in a string format way
        so and will replace the parameters in the message. 
        
        """
        
        self.__Write(msg, level=DEBUG, *args, **kwargs)
        return
    
    def critical(self, msg, *args, **kwargs):
        """Logs an critical message (with loglevel 50)
        
        Arguments:
        msg    : string - The message to log
        args   : list   - List of arguments
        
        Keyword Arguments:
        kwargs : list - List of keyword arguments 
        
        The arguments and keyword arguments are used in a string format way
        so and will replace the parameters in the message. 
        
        """
        
        self.__Write(msg, level=CRITICAL, *args, **kwargs)
        return