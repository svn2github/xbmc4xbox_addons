# -*- coding: utf-8 -*-

# Imports
import xbmc, xbmcgui, xbmcplugin, xbmcaddon

__settings__ = xbmcaddon.Addon(id='plugin.video.watchmojo')
__icon__ = __settings__.getAddonInfo('icon')
__language__ = __settings__.getLocalizedString

class Main:
  def __init__(self):
    RSS_FEED = 'http://www.watchmojo.com/rss/feeds.php?id=%s&type=mrss&max=all'
    folders = [{'title':__language__(30201), 'id':'01'},
               {'title':__language__(30202), 'id':'02'},
               {'title':__language__(30203), 'id':'03'},
               {'title':__language__(30204), 'id':'04'},
               {'title':__language__(30205), 'id':'05'},
               {'title':__language__(30206), 'id':'06'},
               {'title':__language__(30208), 'id':'08'},
               {'title':__language__(30209), 'id':'09'},
               {'title':__language__(30210), 'id':'10'},
               {'title':__language__(30211), 'id':'11'},
               {'title':__language__(30212), 'id':'12'},
               {'title':__language__(30213), 'id':'13'},
               {'title':__language__(30214), 'id':'14'},
               {'title':__language__(30215), 'id':'15'},
               {'title':__language__(30216), 'id':'16'}]
    for i in folders:
      listitem = xbmcgui.ListItem(i['title'], iconImage="DefaultFolder.png", thumbnailImage=__icon__)
      url = 'rss://www.watchmojo.com/rss/feeds.php?id=%s&type=mrss&max=100' % i['id']
      xbmcplugin.addDirectoryItems(int(sys.argv[1]), [(url, listitem, True)])
    # Disable sorting...
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_NONE)
    # End of list...
    xbmcplugin.endOfDirectory(int(sys.argv[1]), True)

if __name__ == '__main__':
  Main()
