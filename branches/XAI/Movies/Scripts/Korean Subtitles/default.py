# -*- coding: utf-8 -*-
"""
  Download subtitle from Korean sites
"""
import sys,os
import xbmc,xbmcaddon

__scriptname__ = "KorSubtitle"
__addonID__ = "script.xbmc-korea.subtitles"
__author__ = "xbmc-korea.com"
__url__ = "http://code.google.com/p/xbmc-korean"
__svn_url__ = "http://code.google.com/p/xbmc-korean/svn/trunk/addons/script.subtitle.xbmc-korea.com"
__credits__ = ""
__version__ = "1.2.1"

if not xbmc.getCondVisibility('Player.Paused') : xbmc.Player().pause()  #Pause if not paused

BASE_RESOURCE_PATH = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'lib' ) )

sys.path.append (BASE_RESOURCE_PATH)

__settings__ = xbmcaddon.Addon( id=__addonID__ )
__language__ = __settings__.getLocalizedString
_ = sys.modules[ "__main__" ].__language__

from gui import *

#############-----------------Is script runing from OSD? -------------------------------###############
if not xbmc.getCondVisibility('videoplayer.isfullscreen') :
  __settings__.openSettings()
  if xbmc.getCondVisibility('Player.Paused'): xbmc.Player().pause() # if Paused, un-pause
else:
  window = False
  skin = "main"
  skin1 = str(xbmc.getSkinDir().lower())
  skin1 = skin1.replace("-"," ")
  skin1 = skin1.replace("."," ")
  skin1 = skin1.replace("_"," ")
  if ( skin1.find( "eedia" ) > -1 ):
   skin = "MiniMeedia"
  if ( skin1.find( "tream" ) > -1 ):
   skin = "MediaStream"
  if ( skin1.find( "edux" ) > -1 ):
   skin = "MediaStream_Redux"
  if ( skin1.find( "aeon" ) > -1 ):
   skin = "Aeon"
  if ( skin1.find( "alaska" ) > -1 ):
   skin = "Alaska"
  if ( skin1.find( "confluence" ) > -1 ):
   skin = "confluence"     
  
  try: xbox = xbmc.getInfoLabel( "system.xboxversion" )
  except: xbox = ""
  if xbox != "" and len(skin) > 13:
    skin = skin.ljust(13)

  print "KorSubtitle version [" +  __version__ +"]"
  print "Skin Folder: [ " + skin1 +" ]"
  print "KorSubtitle skin XML: [ " + skin +" ]"
   
  if ( __name__ == "__main__" ):
    # main body
    gui()

    if xbmc.getCondVisibility('Player.Paused'): xbmc.Player().pause() # if Paused, un-pause
    sys.modules.clear()
  # end of __main__
# vim: softtabstop=2 shiftwidth=2 expandtab
