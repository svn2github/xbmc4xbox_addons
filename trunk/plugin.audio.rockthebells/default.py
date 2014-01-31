import urllib,urllib2,re
import xbmcplugin,xbmcgui,xbmcaddon
from t0mm0.common.addon import Addon
addon = Addon('plugin.video.videobull', sys.argv)
AddonPath = addon.get_path()
fanart = 'http://kozz-addons.googlecode.com/svn/trunk/addons/plugin.audio.rockthebells/resources/art/fanart.png'
IconPath = AddonPath + "resources/art/"
def CATEGORIES():
    addLink('RockTheBells 128k mp3 stream','http://108.61.73.120:40000/128k.mp3','http://kozz-addons.googlecode.com/svn/trunk/addons/plugin.audio.rockthebells/resources/art/rtb.png')
    addLink('RockTheBells 64k aac stream','http://108.61.73.120:40000/64k.aac','http://kozz-addons.googlecode.com/svn/trunk/addons/plugin.audio.rockthebells/resources/art/rtb.png')
    
  
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param

def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok

def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

params=get_params()
url=None
name=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
       
xbmcplugin.endOfDirectory(int(sys.argv[1]))