Wake On LAN
http://en.wikipedia.org/wiki/Wake-on-LAN

~~~~~ autoexec.py ~~~~~
import xbmc

# Wake Computer #1 [00-00-00-00-00-00]...
xbmc.executebuiltin( "XBMC.RunPlugin(plugin://programs/Wake on LAN/?action=%s&name=%s&mac=%s)" % ( "wake", "Computer #1", "00-00-00-00-00-00" ) )
~~~~~~~~~~~~~~~~~~~~~~~