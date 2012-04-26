# -*- coding: utf-8 -*-
"""
  UI for subtitle download
"""
import sys,os,xbmc

_ = sys.modules[ "__main__" ].__language__
__scriptname__ = sys.modules[ "__main__" ].__scriptname__
__settings__ = sys.modules[ "__main__" ].__settings__

from gomtv_jmdb import *
from qple_jamak import *
from subt_down  import *

def gui():
  movieFullPath = xbmc.Player().getPlayingFile()
  smiFullPath = movieFullPath[:movieFullPath.rfind('.')]+'.smi'
  
  try:
    f=open(movieFullPath,"rb")
  except IOError:
    xbmc.log("can not open movie file, %s" % movieFullPath, xbmc.LOGERROR)
    xbmcgui.Dialog().ok("can not open movie file", movieFullPath)
    sys.exit(1)

  ###----- fetch list of available subtitles
  subt_list = []
  dialog = xbmcgui.DialogProgress()
  ignored = dialog.create(__scriptname__ )
  if __settings__.getSetting( "GomTV" )=='true':
    dialog.update( 0, _(100)%_(200) )
    found = gomtv_jamak_from_file(f)
    if found is None:
      xbmcgui.Dialog().ok(__scriptname__, _(101)%_(200), _(108) )
    else:
      subt_list += found
  if __settings__.getSetting( "Qple" )=='true':
    dialog.update( 50, _(100)%_(201) )
    found = qple_jamak_from_file(f)
    if found is None:
      xbmcgui.Dialog().ok(__scriptname__, _(101)%_(201), _(108) )
    else:
      subt_list += found
  dialog.close()
  f.close()

  ###----- select a subtitle to download
  if len(subt_list)==0:
    dialog = xbmcgui.Dialog()
    ignored = dialog.ok(__scriptname__,
                        _(102).encode('utf-8')%os.path.basename(movieFullPath) )
  else:
    title_list = []
    for i in range(0,len(subt_list)):
      if subt_list[i][0] == 'gomtv':
        title = "[Gom] "+subt_list[i][1]
      elif subt_list[i][0] == 'qple':
        title = "[Tok] "+subt_list[i][1]
      else:
        title = subt_list[i][1]
      title_list.append( title )
    print title_list

    dialog = xbmcgui.Dialog()
    selected = dialog.select( _(103)%len(title_list), title_list )

    if selected >= 0:
      if subt_list[selected][0] == 'gomtv':
        smiAddr = gomtv_jamak_url( subt_list[selected][2] )
        if not smiAddr:
          xbmcgui.Dialog().ok(__scriptname__, _(101)%_(200), _(108) )
      else:
        smiAddr = subt_list[selected][2]

      if smiAddr and download_subtitle(smiAddr, smiFullPath):
        # enable the downloaded subtitle
        xbmc.Player().setSubtitles(smiFullPath)
# vim: softtabstop=2 shiftwidth=2 expandtab
