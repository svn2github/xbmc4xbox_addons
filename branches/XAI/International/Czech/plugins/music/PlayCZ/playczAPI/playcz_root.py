""" PlayCZ API Module for generating plugin root virtual folder """

import xbmc
import xbmcgui
import xbmcplugin
import urllib


class Root:
    """ PlayCZ plugin root directory class """

    def __init__(self, baseurl, handle):
        """ Constructor """
        self.baseurl = baseurl
        self.handle  = int(handle)

        # add czradio item 
        self.add_item(30000, 'czradio')
        
        xbmcplugin.endOfDirectory(self.handle)


    def add_item(self, label_id, folderName, type='Music'):
        """ Add virtual directory to output list """
        label = xbmc.getLocalizedString(30000)
        listitem = xbmcgui.ListItem(label)
        listitem.setInfo(type=type, infoLabels={'Title': label})
        url = self.baseurl + '?folder=' + urllib.quote_plus(folderName)
        xbmcplugin.addDirectoryItem(self.handle, url, listitem, isFolder=1)

