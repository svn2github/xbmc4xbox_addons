#===============================================================================
# LICENSE XOT-Framework - CC BY-NC-ND
#===============================================================================
# This work is licenced under the Creative Commons 
# Attribution-Non-Commercial-No Derivative Works 3.0 Unported License. To view a 
# copy of this licence, visit http://creativecommons.org/licenses/by-nc-nd/3.0/ 
# or send a letter to Creative Commons, 171 Second Street, Suite 300, 
# San Francisco, California 94105, USA.
#===============================================================================

import sys
import datetime
import time
import random

import xbmc
import xbmcgui

from helpers import htmlentityhelper
from helpers import prefixhelper
from helpers import encodinghelper
import settings

#===============================================================================
# Make global object available
#===============================================================================
logFile = sys.modules['__main__'].globalLogFile
uriHandler = sys.modules['__main__'].globalUriHandler

class MediaItem:
    """Main class that represent items that are retrieved in XOT. They are used
    to fill the lists and have MediaItemParts which have MediaStreams in this 
    hierarchy:
    
    MediaItem
        +- MediaItemPart
        |    +- MediaStream
        |    +- MediaStream
        |    +- MediaStream
        +- MediaItemPart
        |    +- MediaStream
        |    +- MediaStream
        |    +- MediaStream

    """
    
    def __init__(self, title, url, type="folder", parent=None):
        """Creates a new MediaItem
        
        Arguments:
        title  : string - the title of the item, used for appearance in lists.
        url    : string - url that used for further information retrieval.
        
        Keyword Arguments:
        type   : [opt] string    - type of MediaItem (folder, video, audio).
                                   Defaults to 'folder'.
        parent : [opt] MediaItem - the parent of the current item. None is 
                                   the default.
        
        The <url> can contain an url to a site more info about the item can be 
        retrieved, for instance for a video item to retrieve the media url, or 
        in case of a folder where child items can be retrieved.
        
        The tile will be de-prefixed using the prefixhelper.PrefixHelper class.
        Essential is that no encoding (like UTF8) is specified in the title of 
        the item. This is all taken care of when creating XBMC items in the 
        different methods.
         
        """
        
        dePrefixer = prefixhelper.PrefixHelper()
        name = title.strip()        
        self.name = dePrefixer.GetDePrefixedName(name)
        
        self.url = url
        self.MediaItemParts = []
        self.description = ""
        self.thumb = ""        # image of episode
        self.thumbUrl = ""
        self.icon = ""        # icon for list
        
        self.__date = ""      # value show in interface
        self.__timestamp = datetime.datetime.min    # value for sorting, this one is set to minimum so if non is set, it's shown at the bottom
        
        self.type = type     # video, audio, folder, append, page
        self.parent = parent
        self.complete = False
        self.error = False
        self.downloaded = False
        self.downloadable = False
        self.items = []
        self.rating = None
        self.decoder = encodinghelper.EncodingHelper()   
        
        # GUID used for identifcation of the object. Do not set from script, MD5 needed
        # to prevent UTF8 issues
        try:
            self.guid = ("%s-%s" % (encodinghelper.EncodingHelper.EncodeMD5(title), url)).replace(" ", "")
        except:
            logFile.error("Error setting GUID for title:'%s' and url:'%s'. Falling back to UUID", title, url, exc_info=True)
            self.guid = self.__GetUUID()
    
        self.channels = []    # only needed for Kanalenkiezer 
    
    def AppendSingleStream(self, url, bitrate=0, subtitle=None):
        """Appends a single stream to a new MediaPart of this MediaItem
        
        Arguments:
        url        : string - url of the stream.
        
        Keyword Arguments:
        bitrate    : [opt] integer - bitrate of the stream (default = 0)
        subtitle   : [opt] string  - url of the subtitle of the mediapart 
        
        Returns a reference to the created MediaPart
        
        This methods creates a new MediaPart item and adds the provided
        stream to its MediaStreams collection. The newly created MediaPart
        is then added to the MediaItem's MediaParts collection.        
        
        """
        
        newPart = MediaItemPart(self.name, url, bitrate, subtitle)
        self.MediaItemParts.append(newPart)
        return newPart
    
    def CreateNewEmptyMediaPart(self):
        """Adds an empty MediaPart to the MediaItem
        
        Returns:
        The new MediaPart object (as a reference) that was appended.
        
        This method is used to create an empty MediaPart that can be used to 
        add new stream to. The newly created MediaPart is appended to the 
        MediaItem.MediaParts list.
                
        """
        
        newPart = MediaItemPart(self.name)
        self.MediaItemParts.append(newPart)
        return newPart
    
    def HasMediaItemParts(self):
        """Return True if there are any MediaItemParts present with streams for 
        this MediaItem
        
        """
        
        for part in self.MediaItemParts:
            if len(part.MediaStreams) > 0:
                return True
        
        return False
    
    def IsPlayable(self):
        """Returns True if the item can be played in a Media Player.
        
        At this moment it returns True for:
        * type = 'video'
        * type = 'audio'
        
        """
        
        return self.type.lower() == 'video' or self.type.lower() == 'audio'
    
    def HasDate(self):
        """Returns if a date was set """
        
        return self.__timestamp > datetime.datetime.min
    
    def SetDate(self, year, month, day, hour = None, minutes = None, seconds = None, onlyIfNewer=False, text=None):
        """Sets the datetime of the MediaItem
        
        Arguments:
        year       : integer - the year of the datetime
        month      : integer - the month of the datetime
        day        : integer - the day of the datetime
        
        Keyword Arguments:
        hour       : [opt] integer - the hour of the datetime
        minutes    : [opt] integer - the minutes of the datetime
        seconds    : [opt] integer - the seconds of the datetime
        onlyIfNewer: [opt] integer - update only if the new date is more 
                                     recent then the currently set one
        text       : [opt] string  - if set it will overwrite the text in the 
                                     date label the datetime is also set.
        
        Sets the datetime of the MediaItem in the self.__date and the 
        corresponding text representation of that datetime. 
        
        <hour>, <minutes> and <seconds> can be optional and will be set to 0 in
        that case. They must all be set or none of them. Not just one or two of 
        them.
        
        If <onlyIfNewer> is set to True, the update will only occur if the set 
        datetime is newer then the currently set datetime.
        
        The text representation can be overwritten by setting the <text> keyword
        to a specific value. In that case the timestamp is set to the given time
        values but the text representation will be overwritten. 
        
        If the values form an invalid datetime value, the datetime value will be 
        reset to their default values. 
        
        """

        #dateFormat = xbmc.getRegion('dateshort')
        # correct a small bug in XBMC
        #dateFormat = dateFormat[1:].replace("D-M-", "%D-%M")        
        #dateFormatLong = xbmc.getRegion('datelong')
        #timeFormat = xbmc.getRegion('time')
        #dateTimeFormat = "%s %s" % (dateFormat, timeFormat)

        try:
            dateFormat = "%Y-%m-%d" #"%x"
            dateTimeFormat = dateFormat + " %H:%M"
            
            if hour is None and minutes is None and seconds is None:
                timeStamp = datetime.datetime(int(year), int(month), int(day), 0, 0,0)            
                date = timeStamp.strftime(dateFormat)
            else:
                timeStamp = datetime.datetime(int(year), int(month), int(day), int(hour), int(minutes), int(seconds))
                date = timeStamp.strftime(dateTimeFormat)
                
            if onlyIfNewer and self.__timestamp > timeStamp:
                return
            
            self.__timestamp = timeStamp
            if (text is None):
                self.__date = date
            else:
                self.__date = text
                
        except ValueError:
            logFile.error("Error setting date: Year=%s, Month=%s, Day=%s, Hour=%s, Minutes=%s, Seconds=%s", year, month, day, hour, minutes, seconds, exc_info=True)
            self.__timestamp = datetime.datetime.min
            self.date = ""
    
    def SetErrorState(self, errorMessage=None, error=True, complete=False):
        """Sets the item in error
        
        Keyword Arguments:
        errorMessage : [opt] string - error message
        error        : [opt] bool   - error is set. If set to false, error is reset
        complete     : [opt] bool   - sets the complete bit to false
        
        """
        
        self.error = error
        self.complete = complete
        return
    
    def GetXBMCItem(self, pluginMode=False, name=None):
        """Creates an XBMC item with the same data is the MediaItem. 
        
        Keyword Arguments:
        pluginMode : [opt] boolean - Indication if it's called from a plugin.
        name       : [opt] string  - Overwrites the name of the XBMC item.
        
        Returns:
        A complete XBMC ListItem
        
        This item is used for displaying purposes only and changes to it will 
        not be passed on to the MediaItem. 
        
        If pluginMode = True date labels will be slightly different because 
        for folder items the second label cannot be used in XBMC. The date 
        will therefore be shown in the title. If the MediaItem is of type 'page'
        the prefix "Page " will be added.    
        
        Eventually the self.UpdateXBMCItem is called to set all the parameters. 
        For the mapping and Encoding of MediaItem properties to XBMCItem 
        properties the __doc__ can be used. 
        
        """
        
        #logFile.debug("Creating XBMC ListItem: ListItem(%s, %s, %s, %s)",self.name, self.__date, self.icon, self.thumb)
        
        if name == None:
            itemName = self.name
        else:
            itemName = name
        #name = self.__FullDecodeText(name) This is done in the update. Saves CPU
        
        
        if pluginMode and self.type == 'page':
            # in plugin mode we need to add the Page prefix to the item 
            itemName = "Page %s" % (itemName,)
            logFile.debug("GetXBMCItem :: Adding Page Prefix")
        
        elif pluginMode and self.__date != '':
            if not self.IsPlayable():
                # not playable items should always show date
                itemName = "%s (%s)" % (itemName, self.__date)
            
            # it's playable, check other conditions
            elif not self.complete and not settings.AddonSettings().UseAdvancedPlugin():
                # A playable file that is not complete and we are in normal mode
                itemName = "%s (%s)" % (itemName, self.__date)                
        
        # if there was a thumbUrl and we are in pluginMode, just pass it to XBMC
        if pluginMode and not self.thumbUrl == "":
            self.thumb = self.thumbUrl
            
        item = xbmcgui.ListItem(itemName, self.__date, self.icon, self.thumb)
        
        # now just call the update XBMCItem
        self.UpdateXBMCItem(item, name=itemName)
        return item
    
    def UpdateXBMCItem(self, item, name=None):
        """Updates an existing XBMC ListItem with properties and InfoLabels
        
        Arguments:
        item : ListItem - The XBMC ListItem to update.
        
        Keyword Arguments:
        name : [opt] string - Can be used to overwrite the name of the item.
        
        Returns:
        Nothing! The update of the XBMC ListItem is done by reference! 
        
        See for the InfoLabels: http://wiki.xbmc.org/index.php?title=InfoLabels
        
        Mapping:
         * ListItem.Type           -> self.type
         * ListItem.Label          -> self.name 
         * ListItem.Title          -> self.name 
         * ListItem.Date           -> self.__timestamp the format "%d.%m.%Y"
         * ListItem.PlotOutline    -> self.description
         * ListItem.Plot           -> self.description         
         * ListItem.Label2         -> self.__date
         * ListItem.ThumbnailImage -> self.thumb
         
        Besides these mappings, the following XOT mappings are set which are 
        by the XOT skin only:
         * XOT_Description         -> self.description
         * XOT_Complete            -> self.complete
         * XOT_Type                -> self.type
         * XOT_Rating              -> self.rating (-1 if self.rating is None)
         * XOT_Error               -> self.error
        
        Encoding:
        All string values are set in UTF8 encoding and with the HTML characters
        converted to UTF8 characters. This is done by the self.__FullDecodeText 
        method.
        
        """
        
        if name == None:
            name = self.name
        
        # the likelihood of getting an name with both HTML entities and Unicode is very low. So do both 
        # conversions, one will be unnecessary
        name = self.__FullDecodeText(name)
        description = self.__FullDecodeText(self.description)
        if description is None:
            description = ""
        
        #the XBMC ListItem date
        #date          : string (%d.%m.%Y / 01.01.2009) - file date
        if self.__timestamp > datetime.datetime.min:
            xbmcDate = self.__timestamp.strftime("%d.%m.%Y")
            xbmcYear = self.__timestamp.year
        else:
            xbmcDate = ""
            xbmcYear = 0
        
        # specific items
        if self.type == "audio":
            item.setInfo(type="Audio", infoLabels={"Label":name, "title": name, "Year": xbmcYear})
            pass
        else:
            item.setInfo(type="Video", infoLabels={"Label":name, "date": xbmcDate, "title": name, "PlotOutline": description, "Plot": description, "Year": xbmcYear})
            pass
        
        # all items
        item.setLabel(name)
        item.setLabel2(self.__date)
        
        #logFile.debug("Setting Description on XBMC Item:\nXOT_Complete=%s\nXOT_Type=%s", str(self.complete), str(self.type))
        item.setProperty("XOT_Description", description)
        item.setProperty("XOT_Complete", str(self.complete))
        item.setProperty("XOT_Type", str(self.type))
        item.setProperty("XOT_Error", str(self.error))
        
        if self.rating == None:
            #logFile.debug("setting rating to: -1")            
            item.setProperty("XOT_Rating", str(-1))            
        else:
            #logFile.debug("setting rating to: xot_rating%s.png", self.rating)
            item.setProperty("XOT_Rating", "xot_rating%s.png" % (self.rating,))
                
        item.setThumbnailImage("") # this one forces the update of the complete item, so always do this 
        item.setThumbnailImage(self.thumb) # this one forces the update of the complete item, so always do this  
    
    def GetXBMCPlayList(self, bitrate=None):
        """ Creates a XBMC Playlist containing the MediaItemParts in this MediaItem
        
        Keyword Arguments:
        bitrate : [opt] integer - The bitrate of the streams that should be in
                                  the playlist. Given in kbps
                                                                      
        Returns:
        a XBMC Playlist for this MediaItem
        
        If the Bitrate keyword is omitted the the bitrate is retrieved using the
        default bitrate settings:
        
        """    
        
        playList = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playList.clear()
        srt = None
            
        logText ="Creating playlist for Bitrate: %s kbps\n%s\nSelected Streams:\n" % (bitrate, self)             
        # for each MediaItemPart get the URL
        for part in self.MediaItemParts:
            if len(part.MediaStreams) == 0:
                logFile.warning("Ignoring empty MediaPart: %s", part)
                continue
            
            (stream, xbmcItem) = part.GetXBMCPlayListItem(self, bitrate=bitrate)
            logText = "%s\n + %s" % (logText, stream)
            if part.UserAgent is None:
                playList.add(stream.Url, xbmcItem)
            else:
                url = "%s|User-Agent=%s" % (stream.Url, htmlentityhelper.HtmlEntityHelper.UrlEncode(part.UserAgent))
                playList.add(url, xbmcItem)
                
            # for now we just add the last subtitle, this will not work if each
            # part has it's own subtitles. 
            srt = part.Subtitle
        
        logFile.debug(logText)                    
        return (playList, srt)     
    
    def __GetUUID(self):
        """Generates a Unique Identifier based on Time and Random Integers"""
        
        t = long( time.time() * 1000 )
        r = long( random.random()*100000000000000000L )
        a = random.random()*100000000000000000L
        data = str(t)+' '+str(r)+' '+str(a)
        data = encodinghelper.EncodingHelper.EncodeMD5(data)
        return data
    
    def __FullDecodeText(self, stringValue):
        """ Decodes a byte encoded string with HTML content into Unicode String
        
        Arguments:
        stringValue : string - The byte encoded string to decode
        
        Returns:
        An Unicode String with all HTML entities replaced by their UTF8 characters
        
        The decoding is done by first decode the string to UTF8 and then replace
        the HTML entities to their UTF8 characters.
        
        """
        
        if stringValue is None:
            return None
        
        if stringValue == "":
            return ""
        
        # first decode to Unicode
        stringValue = self.decoder.Decode(stringValue)        
        
        # then get rid of the HTML entities
        stringValue = htmlentityhelper.HtmlEntityHelper.ConvertHTMLEntities(stringValue)
        return stringValue
    
    def __str__(self):
        """ String representation """
        
        value = self.name
        
        if self.IsPlayable():
            if len(self.MediaItemParts) > 0:
                value = "MediaItem: %s [Type=%s, Complete=%s, Error=%s, Date=%s, Downloadable=%s]" % (value, self.type, self.complete, self.error, self.__date, self.downloadable)
                for mediaPart in self.MediaItemParts:
                    value = "%s\n%s" % (value, mediaPart)
                value = "%s" % (value,)
            else:
                value = "%s [Type=%s, Complete=%s, unknown urls, Error=%s, Date=%s, Downloadable=%s]" % (value, self.type, self.complete, self.error, self.__date, self.downloadable)
        else:
            value = "%s [Type=%s, Url=%s, Date=%s]" % (value, self.type, self.url, self.__date)
        
        return value
    
    def __eq__(self, item):
        """ checks 2 items for Equality
        
        Arguments:
        item : MediaItem - The item to check for equality.
        
        Returns:
        the output of self.Equals(item).
         
        """
        return self.Equals(item)
    
    def __ne__(self, item):
        """ returns NOT Equal 
        
        Arguments:
        item : MediaItem - The item to check for equality.
        
        Returns:
        the output of not self.Equals(item).
         
        """
            
        return not self.Equals(item)
    
    def __cmp__(self, other):
        """ Compares 2 items based on their appearance order
        
        Arguments:
        other : MediaItem - The item to compare to
        
        Returns:
         * -1 : If the item is lower than the current one
         *  0 : If the item is order is equal
         *  1 : If the item is higher than the current one
        
        The comparison is done base on:
         * the type of the item. Non-playable items appear first.
         * the defined sorting algorithm. This is a Add-on setting retrieved 
           using the AddonSettings() method. Options are: Name or Timestamp. 
        
        """
        
        if other is None:
            return -1
        
        if self.type == other.type:
            #logFile.debug("Comparing :: same types")                
            sortMethod = settings.AddonSettings().GetSortAlgorithm()
            
            # date sorting
            if sortMethod == "date":
                #logFile.debug("Comparing :: Settings: Sorting by date")
            
                # at this point both have timestamps or dates, so we can compare
                if self.__timestamp == other.__timestamp:
                    # same timestamps, compare names
                    return cmp(self.name, other.name)                
                else:
                    # compare timestamps
                    return cmp(other.__timestamp, self.__timestamp)
                
            # name sorting
            elif sortMethod == "name":
                #logFile.debug("Comparing :: Settings: Sorting by name")
                return cmp(self.name, other.name)
            else:
                return 0
        else:
            # one is folder other one is playable. Folders are always sorted first
            logFile.debug("Comparing :: different types, none playable first")
            if self.IsPlayable():
                return - 1
            else:
                return 1       
    
    def Equals(self, item):
        """ Compares two items
        
        Arguments:
        item : MediaItem - The item to compare to
        
        Returns:
        True if the item's GUID's match. 
         
        """
        
        if item == None:
            return False
        
        if self.name == item.name and self.guid != item.guid:
            logFile.debug("Duplicate names, but different guid: %s (%s), %s (%s)", self.name, self.url, item.name, item.url)
        return self.guid == item.guid
    
class MediaItemPart:
    """Class that represents a MediaItemPart"""
    
    def __init__(self, name, url="", bitrate=0, subtitle=None, *args):
        """ Creates a MediaItemPart with <name> with at least one MediaStream 
        instantiated with the values <url> and <bitrate>.
        The MediaPart could also have a <subtitle> or Properties in the <*args>
        
        Arguments:
        name : string       - the name of the MediaItemPart
        url  : string       - the URL of the stream of the MediaItemPart 
        args : list[string] - a list of arguments that will be set as properties
                              when getting an XBMC Playlist Item
        
        Keyword Arguments:
        bitrate  : [opt] integer - The bitrate of the stream of the MediaItemPart        
        subtitle : [opt] string  - The url of the subtitle of this MediaItemPart
        
        If a subtitles was provided, the subtitle will be downloaded and stored
        in the XOT cache. When played, the subtitle is shown. Due to the XBMC
        limitation only one subtitle can be set on a playlist, this will be
        the subtitle of the first MediaPartItem
        
        """
        
        logFile.debug("Creating MediaItemPart '%s' for '%s'", name, url)
        self.Name = name
        self.MediaStreams = []
        self.Subtitle = ""
        self.CanStream = True
        self.UserAgent = None  #: Used for downloading a stream is needed

        # set a subtitle
        if not subtitle is None:
            self.Subtitle = subtitle
        
        if not url == "":
            # set the stream that was passed        
            self.AppendMediaStream(url, bitrate)        
        
        # set properties
        self.Properties = []
        for prop in args:
            self.Properties.append(prop)
        return
    
    def AppendMediaStream(self, url, bitrate):
        """Appends a mediastream item to the current MediaPart
        
        Arguments:
        url     : string  - the url of the MediaStream
        bitrate : integer - the bitrate of the MediaStream
        
        Returns:
        the newly added MediaStream by reference.
        
        The bitrate could be set to None. 
        
        """
        
        stream = MediaStream(url, bitrate)
        self.MediaStreams.append(stream)
        return stream
    
    def AddProperty(self, name, value):
        """Adds a property to the MediaPart
        
        Arguments:
        name  : string - the name of the property
        value : stirng - the value of the property
        
        Appends a new property to the self.Properties dictionary. On playback
        these properties will be set to the XBMC PlaylistItem as properties.
        
        """
        
        logFile.debug("Adding property: %s = %s", name, value)
        self.Properties.append((name, value))
    
    def GetXBMCPlayListItem(self, parent, bitrate=None, pluginMode=False, name=None):
        """Returns a XBMC List Item than can be played or added to an XBMC 
        PlayList. 
            
        Arguments:
        parent : MediaItem - the parent MediaItem
        
        Keyword Arguments:
        quality    : [opt] integer - The quality of the requested XBMC 
                                     PlayListItem streams. 
        pluginMode : [opt] boolean - Indicates if it was called from a
                                     plugin instead of script.
        name       : [opt] string  - If set, it overrides the original
                                     name of the MediaItem (mainly used 
                                     in the plugin.
        
        Returns:
        A tuple with (stream url, XBMC PlayListItem). The XBMC PlayListItem 
        can be used to add to a XBMC Playlist. The stream url can be used
        to set as the stream for the PlayListItem using xbmc.PlayList.add()
        
        If quality is not specified the quality is retrieved from the add-on
        settings.
        
        """
        
        if name == None:
            logFile.debug("Creating XBMC ListItem '%s' [PluginMode=%s]", self.Name, pluginMode)
        else:
            logFile.debug("Creating XBMC ListItem '%s' [PluginMode=%s]", name, pluginMode)
        item = parent.GetXBMCItem(pluginMode=pluginMode, name=name)
        
        if bitrate == None:
            bitrate = settings.AddonSettings().GetMaxStreamBitrate()
            
        for prop in self.Properties:
            #logFile.debug("Adding property: %s", prop)
            item.setProperty(prop[0], prop[1])
        
        # now find the correct quality stream
        stream = self.GetMediaStreamForBitrate(bitrate)        
        return (stream, item)
    
    def GetMediaStreamForBitrate(self, bitrate, roundUp=True):
        """Returns the MediaStream for the requested bitrate. 

        Arguments:
        bitrate : integer - The bitrate of the stream in kbps
        
        Keyword Arguments:
        roundUp : boolean - In case of an even number of items, this determines
                            if the higher or lower medium is taken.
        
        Returns:
        The url of the stream with the requested bitrate. 
                             
        If bitrate is not specified the highest bitrate stream will be used.
         
        """
        
        # order the items by bitrate
        self.MediaStreams.sort()
        bestStream = None
        bestDistance = None
    
        for stream in self.MediaStreams:
            if stream.Bitrate is None:
                # no bitrate set, see if others are availabe
                continue
            
            # this is the bitrate-as-max-limit-method
            if stream.Bitrate > bitrate:
                # if the bitrate is higher, continue for more
                continue
            # if commented ^^ , we get the closest-match-method 
            
            # determine the distance till the bitrate
            distance = abs(bitrate-stream.Bitrate)
            
            if bestDistance is None or bestDistance > distance:
                # this stream is better, so store it.
                bestDistance = distance
                bestStream = stream
        
        if bestStream is None:
            # no match, take the lowest bitrate
            return self.MediaStreams[0]
    
        return bestStream  
    
    def __cmp__(self, other):
        """ Compares 2 items based on their appearance order
        
        Arguments:
        other : MediaItemPart - The part to compare to
        
        Returns:
         * -1 : If the item is lower than the current one
         *  0 : If the item is order is equal
         *  1 : If the item is higher than the current one
        
        The comparison is done base on the Name only.  
        
        """
        if other is None:
            return -1
        
        # compare names        
        return cmp(self.Name, other.Name)
    
    def __eq__(self, other):
        """ checks 2 items for Equality
        
        Arguments:
        item : MediaItemPart - The part to check for equality.
        
        Returns:
        the True if the items are equal. Equality takes into consideration:
         * Name
         * Subtitle
         * Length of the MediaStreams
         * Compares all the MediaStreams in the slef.MediaStreams
         
        """
        
        if other is None:
            return False
        
        if not other.Name == self.Name:
            return False 
        
        if not other.Subtitle == self.Subtitle:
            return False
        
        # now check the strea
        if not len(self.MediaStreams) == len(other.MediaStreams):
            return False
        
        for i in range(0, len(self.MediaStreams)):
            if not self.MediaStreams[i] == other.MediaStreams[i]:
                return False
        
        # if we reach this point they are equal.
        return True

    def __str__(self):
        """ String representation """
        
        text = "MediaPart: %s [CanStream=%s, UserAgent=%s]" % (self.Name, self.CanStream, self.UserAgent)
        
        if self.Subtitle != "":
            text = "%s\n + Subtitle: %s" % (text, self.Subtitle)
                         
        for prop in self.Properties:
            text = "%s\n + Property: %s=%s" % (text, prop[0], prop[1]) 
        
        for stream in self.MediaStreams:
            text = "%s\n + %s" % (text, stream)
        return text

class MediaStream:
    """Class that represents a Mediastream with <url> and a specific <bitrate>"""
    
    def __init__(self, url, bitrate=0):
        """Initialises a new MediaStream
        
        Arguments:
        url : string - the URL of the stream
        
        Keyworkd Arguments:
        bitrate : [opt] integer - the bitrate of the stream (defaults to 0)
        
        """        
        
        logFile.debug("Creating MediaStream '%s' with bitrate '%s'", url, bitrate)
        self.Url = url
        self.Bitrate = int(bitrate)
        self.Downloaded = False     
        return

    def __cmp__(self, other):
        """Compares two MediaStream based on the bitrate
        
        Arguments:
        other : MediaStream - The stream to compare to
        
        Returns:
         * -1 : If the item is lower than the current one
         *  0 : If the item is order is equal
         *  1 : If the item is higher than the current one
        
        The comparison is done base on the bitrate only.  
        
        """
        
        if other is None:
            return -1
        
        return cmp(self.Bitrate, other.Bitrate)
    
    def __eq__(self, other):
        """Checks 2 items for Equality
        
        Arguments:
        other : MediaStream - The stream to check for equality.
        
        Returns:
        the True if the items are equal. Equality takes into consideration:
         * The url of the MediaStream
         
        """
        
        # also check for URL
        if other is None:
            return False
        
        return self.Url == other.Url

    def __str__(self):
        """String representation"""
        
        text = "MediaStream: %s [bitrate=%s, downloaded=%s]" % (self.Url, self.Bitrate, self.Downloaded)
        return text