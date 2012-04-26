"""
"""

__all__ = [
    # public names
    "parseAddonXml",
    "parseAddonElt",
    "createItemListFromXml",
    "ListItemFromXML"
    ]


# Modules general
#import os
import sys

from traceback import print_exc

import elementtree.ElementTree as ET

# Modules custom
try:
    #from specialpath import *
    #from utilities import *
    from Item import TYPE_ADDON, TYPE_ADDON_MUSIC, TYPE_ADDON_PICTURES, TYPE_ADDON_PROGRAMS, TYPE_ADDON_VIDEO, TYPE_ADDON_MODULE, TYPE_ADDON_REPO, TYPE_ADDON_SCRIPT  
except:
    print_exc()

#FONCTION POUR RECUPERER LES LABELS DE LA LANGUE.
_ = sys.modules[ "__main__" ].__language__


# Types of Extension
TYPE_EXT_UI_SKIN                = "xbmc.gui.skin"
TYPE_EXT_REPO                   = "xbmc.addon.repository"
TYPE_EXT_SERVICE                = "xbmc.service"
TYPE_EXT_SCRAPER_ALBUMS         = "xbmc.metadata.scraper.albums"
TYPE_EXT_SCRAPER_ARTISTS        = "xbmc.metadata.scraper.artists"
TYPE_EXT_SCRAPER_MOVIES         = "xbmc.metadata.scraper.movies"
TYPE_EXT_SCRAPER_MUSICVIDEOS    = "xbmc.metadata.scraper.musicvideos"
TYPE_EXT_SCRAPER_TVSHOWS        = "xbmc.metadata.scraper.tvshows"
TYPE_EXT_SCRAPER_LIB            = "xbmc.metadata.scraper.library"
TYPE_EXT_UI_SCREENSAVER         = "xbmc.ui.screensaver"
TYPE_EXT_PLAYER_MUSICVIZ        = "xbmc.player.musicviz"
TYPE_EXT_PLUGINSOURCE           = "xbmc.python.pluginsource"
TYPE_EXT_SCRIPT                 = "xbmc.python.script"
TYPE_EXT_SCRIPT_WEATHER         = "xbmc.python.weather"
TYPE_EXT_SCRIPT_SUBTITLE        = "xbmc.python.subtitles"
TYPE_EXT_SCRIPT_LYRICS          = "xbmc.python.lyrics"
TYPE_EXT_SCRIPT_MODULE          = "xbmc.python.module"
TYPE_EXT_SCRIPT_LIB             = "xbmc.python.library"

supportedExtList = [ TYPE_EXT_REPO,
                     TYPE_EXT_PLUGINSOURCE,
                     TYPE_EXT_SCRIPT,
                     TYPE_EXT_SCRIPT_WEATHER,
                     TYPE_EXT_SCRIPT_SUBTITLE,
                     TYPE_EXT_SCRIPT_LYRICS,
                     TYPE_EXT_SCRIPT_LIB,
                     TYPE_EXT_SCRIPT_MODULE,
                   ]

scriptExtList = [ TYPE_EXT_SCRIPT_WEATHER,
                  TYPE_EXT_SCRIPT_SUBTITLE,
                  TYPE_EXT_SCRIPT_LYRICS,
                  TYPE_EXT_SCRIPT_LIB,
                  TYPE_EXT_SCRIPT,
                ]

def parseAddonXml( xmlData, itemInfo ):
    """
    Get Item Info from addon.xml and set itemInfo object 
    Look at http://wiki.xbmc.org/index.php?title=Add-ons_for_XBMC_(Developement) for XML format description
    """
    # id
    # name
    # type
    # version
    # author
    # disclaimer
    # summary
    # description
    # icon
    # fanart
    # changelog
    # library: path of python script
    # raw_item_sys_type: file | archive | dir
    # raw_item_path
    # install_path
    # extracted_path
    # provides
    # required_lib
    
    status = 'OK'
    try:
        if ( xmlData ):
            xmlElt = ET.parse( xmlData ).getroot()
            print 'xmlElt'
            print xmlElt
            status = parseAddonElt( xmlElt, itemInfo )
    except:
        status = 'ERROR'
        print_exc()
    
    return status
            



def parseAddonElt( addonElt, itemInfo ):
    """
    Get Item Info from addon.xml and set itemInfo object 
    """
    # id
    # name
    # type
    # version
    # author
    # disclaimer
    # summary
    # description
    # icon
    # fanart
    # changelog
    # library: path of python script file i.e default.py
    # raw_item_sys_type: file | archive | dir
    # raw_item_path
    # install_path
    # extracted_path
    # provides
    # required_lib
    
    status = 'OK'
    try:
        if ( addonElt ):
            #print "parseAddonElt"
            #print ET.tostring(addonElt)
            #print "--"
            libPoint = None
            itemInfo [ "id" ]      = addonElt.attrib.get( "id" )
            #itemInfo [ "name" ]    = addonElt.attrib.get( "name" ).encode( "utf8" )
            itemInfo [ "name" ]    = addonElt.attrib.get( "name" )
            itemInfo [ "version" ] = addonElt.attrib.get( "version" )
            itemInfo [ "author" ]  = addonElt.attrib.get( "provider-name" )
            itemInfo [ "type" ]    = TYPE_ADDON # Unsupported type of addon (default value)
            extensions = addonElt.findall("extension")
            if extensions:
                for extension in extensions:
                    point = extension.attrib.get( "point" )
                    if point in supportedExtList:
                        # Map the type
                        itemInfo [ "type" ] = _getType(itemInfo [ "id" ], point)
                        if extension.attrib.get("library"):
                            # Info on lib
                            itemInfo [ "library" ] = extension.attrib.get( "library" )
                            itemInfo [ "provides" ] = extension.findtext( "provides" )
                            libPoint = extension.attrib.get( "point" )
                            
                        # Get repo info in case of repo:
#                        <extension point="xbmc.addon.repository"
#                            name="Passion-XBMC Add-on Repository">
#                            <info compressed="true">http://passion-xbmc.org/addons/addons.php</info>
#                            <checksum>http://passion-xbmc.org/addons/addons.xml.md5</checksum>
#                            <datadir zip="true">http://passion-xbmc.org/addons/Download.php</datadir>
#                        </extension>
                        if point == TYPE_EXT_REPO:
                            itemInfo [ "repo_url" ] = extension.findtext( "info" ) 
                            datadir = extension.find( "datadir" )
                            itemInfo [ "repo_datadir" ] = datadir.text 
                            zip = datadir.attrib.get( "zip" )
                            print "Repo format zip attribute: %s"%zip
                            if zip == "true":
                                itemInfo [ "repo_format" ] = "zip"
                            else:
                                itemInfo [ "repo_format" ] = "dir"
                            
                    elif point == "xbmc.addon.metadata":
                        # Metadata
                        itemInfo [ "platform" ]    = extension.findtext( "platform" ) 
                        itemInfo [ "nofanart" ]    = extension.findtext( "nofanart" ) 
                        itemInfo [ "description" ] = extension.findtext( "description" ) 
                        itemInfo [ "disclaimer" ]  = extension.findtext( "disclaimer" ) 
                        
                        #TODO: Check case where tag is not present: what is returned?
                        
            requires = addonElt.find("requires")
            if requires:
                modules2import = requires.findall("import")
                requiredModuleList = []
                for module in modules2import:
                    addonId = module.attrib.get( "addon" )
                    if module.attrib.get( "addon" ) != 'xbmc.python': # we ignore default python lib
                        moduleInfo = {}
                        moduleInfo [ "id" ]      = addonId
                        moduleInfo [ "version" ] = module.attrib.get( "version" )
                        requiredModuleList.append( moduleInfo )
                itemInfo [ "required_lib" ] = requiredModuleList
                    
                
            if itemInfo [ "type" ] == TYPE_ADDON:
                print "Not supported type of Addon"
                status = 'NOT_SUPPORTED'
        else:
            print "addonElt not defined"
            #status = 'ERROR'

    except:
        #status = 'ERROR'
        print_exc()

    print itemInfo
    
    return status

def _getType(id, extension):
    """
    Determine the Type of the addon
    """
    type = TYPE_ADDON # Unsupported type of addon
    #print "id: __%s__ / extension: __%s__"%(id, extension)
    #print "TYPE_EXT_REPO = __%s__"%TYPE_EXT_REPO
    #print "TYPE_ADDON_REPO = __%s__"%TYPE_ADDON_REPO
    if  extension == TYPE_EXT_PLUGINSOURCE:
        # Plugin: we need to check the addons id
        print "_getType - This is a Plugin"
        if TYPE_ADDON_MUSIC in id:
            type = TYPE_ADDON_MUSIC
            print "_getType - This is a MUSIC Plugin"
        elif TYPE_ADDON_PICTURES in id:
            type = TYPE_ADDON_PICTURES
            print "_getType - This is a PICTURES Plugin"
        elif TYPE_ADDON_PROGRAMS in id:
            type = TYPE_ADDON_PROGRAMS
            print "_getType - This is a PROGRAMS Plugin"
        elif TYPE_ADDON_VIDEO in id:
            print "_getType - This is a VIDEO Plugin"
            type = TYPE_ADDON_VIDEO
    elif extension == TYPE_EXT_SCRIPT_MODULE:
        print "_getType - This is a LIB script"
        type = TYPE_ADDON_MODULE
    elif extension == TYPE_EXT_REPO:
        print "_getType - This is a REPOSITORY"
        type = TYPE_ADDON_REPO
    elif extension in scriptExtList:
        print "_getType - This is a SCRIPT"
        type = TYPE_ADDON_SCRIPT
    else:
        print "_getType - unsupported type: %s"%type
    #print "_getType - Type is: %s"%type
    return type
                        
    

def createItemListFromXml( xmlData ):
    """
    Create and return the list of addons from XML data
    Returns list and name of the list
   """
    status = 'OK'
    list = []

    try:
        if ( xmlData ):
            xmlElt = ET.parse( xmlData ).getroot() # root: <addons>
            print 'xmlElt'
            print xmlElt
            if ( xmlElt ):
                addons = xmlElt.findall("addon")
                for addon in addons:
                    # dictionary to hold addon info
                    itemInfo = {}
                    status = parseAddonElt( addon, itemInfo )
                    if status == 'OK':
                        list.append(itemInfo)
    except:
        status = 'ERROR'
        print_exc()
    
    return status, list

class ListItemFromXML:
    currentParseIdx = 0
    addons = []
    def __init__( self, xmlData ):
        try:
            if ( xmlData ):
                #print xmlData
                rootXmlElt = ET.parse( xmlData ).getroot() # root: <addons>
                print 'rootXmlElt'
                print rootXmlElt
                
                if ( rootXmlElt ):
                    self.addons = rootXmlElt.findall("addon")
                    #for i in range(len(self.addons)):
                    #    print ET.tostring(self.addons[i])
        except:
            status = 'ItemList::__init__: ERROR'
            print_exc()
    
        
    def _parseAddonElement(self, addonElt, itemInfo):
        return parseAddonElt( addonElt, itemInfo )
    
    
    def getNextItem(self):
        result = None
        if len(self.addons) > 0 and self.currentParseIdx < len(self.addons):
            itemInfo = {}
            status = self._parseAddonElement( self.addons[self.currentParseIdx], itemInfo )
            self.currentParseIdx = self.currentParseIdx + 1
            print "status = %s"%status
#            if status == 'OK':
#                result = itemInfo
            result = itemInfo
        print "getNextItem - result:"
        print result
        return result
    
    
#    
#    # List the main categories at the root level
#    for entry in dicdata:
#        if Item.isSupported( categories[ entry['xbmc_type'] ] ):
#            item = {}
#            item['id']                = int( entry['id'] )
#            item['name']              = entry['title']#.encode( "utf8" )
#            item['parent']            = int( entry['idparent'] )
#            item['downloadurl']       = entry['fileurl']
#            item['type']              = entry['type']#'CAT'
#            item['totaldownloads']    = entry['totaldownloads']
#            item['xbmc_type']         = categories[ entry['xbmc_type'] ]
#            #item['cattype']           = entry
#            if LANGUAGE_IS_FRENCH:
#                item['description']       = self.strip_off_passionCDT( unescape( urllib.unquote( entry['description'] ) ) )#.encode("cp1252").
#            else:
#                item['description']       = self.strip_off_passionCDT( unescape( urllib.unquote( entry['description_en'] ) ) )#.encode("cp1252").decode('string_escape')
#            if item['description'] == 'None':
#                item['description'] = _( 604 ) 
#            item['language']          = entry['script_language']
#            item['version']           = entry['version']
#            item['author']            = entry['author']
#            item['date']              = entry['createdate']
#            if entry['date'] != '':
#                item['added'] = strftime( '%d-%m-%Y', localtime( int (entry['date'] ) ) )
#            else:
#                item['added'] = entry['date']
#            if entry['filesize'] != '':
#                item['filesize'] = int( entry['filesize'] )
#            else:
#                item['filesize'] = 0 # ''
#            item['thumbnail']         = Item.get_thumb( item['xbmc_type'] )
#            item['previewpictureurl'] = entry['image']
#            item['previewpicture']    = ""#Item.get_thumb( entry )
#            item['image2retrieve']    = False # Temporary patch for reseting the flag after downlaad (would be better in the thread in charge of the download)
#            
#            item['orginalfilename']     = entry['orginalfilename']
#            #TODO: deprecated??? Check server side
#            item['fileexternurl']     = "None"
#            self._setDefaultImages( item )
#            list.append(item)
#            print item
#        else:
#            print "Type not supported by the installer:"
#            print entry
#        
#    return list

