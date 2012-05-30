# -*- coding: utf-8 -*-
import urllib2,urllib,re,os
from parseutils import *
from urlparse import urlparse
import xbmcplugin,xbmcgui,xbmcaddon
__baseurl__='http://www.muvi.cz'
_UserAgent_ = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
addon = xbmcaddon.Addon('plugin.video.dmd-czech.muvi')
profile = xbmc.translatePath(addon.getAddonInfo('profile'))
__settings__ = xbmcaddon.Addon(id='plugin.video.dmd-czech.muvi')
home = __settings__.getAddonInfo('path')
REV = os.path.join( profile, 'list_revision')
icon = xbmc.translatePath( os.path.join( home, 'icon.png' ) )
nexticon = xbmc.translatePath( os.path.join( home, 'nextpage.png' ) )
fanart = xbmc.translatePath( os.path.join( home, 'fanart.jpg' ) )



def OBSAH():
    zakazane = ['/aerokratas-2011']
    addDir('Top20',__baseurl__+'/video/top20',1,icon)    
    addDir('Nejnovější',__baseurl__+'/video/nejnovejsi',1,icon)    
    addDir('Seriály',__baseurl__+'/video/porad/37',1,icon)    
    req = urllib2.Request(__baseurl__+'/porady/vsechny')
    req.add_header('User-Agent', _UserAgent_)
    response = urllib2.urlopen(req)
    httpdata = response.read()
    response.close()
    match = re.compile('<a href="(.+?)"><img src="(.+?)" alt="(.+?)" /></a>').findall(httpdata)
    for url,thumb,name in match:
        if url in zakazane:
            continue
        addDir(name,__baseurl__+url,1,__baseurl__+thumb)    

            
def INDEX(url): 
    doc = read_page(url)
    items = doc.find('div', 'videoClipsWrapper')
    for item in items.findAll('li','listItem'):
        thumb = item.find('a', 'framedThumbnail')
        thumb = str(item.img['src'])            
        info = item.find('div', 'carouselListItemText')
        name = info.find('a')
        name = name.getText(" ").encode('utf-8')
        name2 = info.find('div','showTitle')
        name2 = name2.getText(" ").encode('utf-8')
        link = str(info.a['href'])
        #print name+' '+name2,__baseurl__+link,2,thumb
        addDir(name+' '+name2,__baseurl__+link,2,thumb)    
    try:
        items = doc.find('div', 'pager')
        for item in items.findAll('a'):
            page = item.text.encode('utf-8') 
            if re.match('následující', page, re.U):
                next_url = item['href'].replace('.','')
                cast_url = urlparse(url)
                #print 'http://'+cast_url[1]+cast_url[2]+next_url
                addDir('>> Další strana >>','http://'+cast_url[1]+cast_url[2]+next_url,1,nexticon)
    except:
        print 'strankovani nenalezeno'              


def VIDEOLINK(url):
    doc = read_page(url)
    name = re.compile('<title>(.+?)</title>').findall(str(doc))
    thumb = re.compile('<link rel="image_src" href="(.+?)"').findall(str(doc))
    low_hq = re.compile("'file','(.+?)'").findall(str(doc))        
    high_hq = re.compile("'hd.file','(.+?)'").findall(str(doc))    
    if __settings__.getSetting('kvalita_sel') == "false":
        addLink('LQ '+name[0],low_hq[0],thumb[0],name[0])
    if __settings__.getSetting('kvalita_sel') == "true":
        addLink('HQ '+name[0],high_hq[0],thumb[0],name[0])
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



def addLink(name,url,iconimage,popis):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": popis} )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok

def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
    
params=get_params()
url=None
name=None
thumb=None
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
        OBSAH()
       
elif mode==1:
        print ""
        INDEX(url)
elif mode==2:
        print ""
        VIDEOLINK(url)
        
xbmcplugin.endOfDirectory(int(sys.argv[1]))
