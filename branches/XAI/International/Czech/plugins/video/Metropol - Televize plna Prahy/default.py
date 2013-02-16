# -*- coding: utf-8 -*-
import urllib2,urllib,re,os,string,time,base64,md5,datetime
from parseutils import *
import xbmcplugin,xbmcgui,xbmcaddon
__baseurl__ = 'http://www.metropol.cz/'
__dmdbase__ = 'http://iamm.uvadi.cz/xbmc/metropol/'
_UserAgent_ = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
addon = xbmcaddon.Addon('plugin.video.dmd-czech.voyo')
profile = xbmc.translatePath(addon.getAddonInfo('profile'))
REV = os.path.join( profile, 'list_revision')
__settings__ = xbmcaddon.Addon(id='plugin.video.dmd-czech.metropol')
home = __settings__.getAddonInfo('path')
icon = xbmc.translatePath( os.path.join( home, 'icon.png' ) )
nexticon = xbmc.translatePath( os.path.join( home, 'nextpage.png' ) )
fanart = xbmc.translatePath( os.path.join( home, 'fanart.jpg' ) )
page_pole_url = []
page_pole_no = []

def OBSAH():
    addDir('Pořady',__baseurl__+'porady/',1,icon)
    addDir('Videa',__baseurl__+'videa/',2,icon)

def PORADY(url):
    doc = read_page(url)
    items = doc.find('div', 'show-list')
    for item in items.findAll('div', 'show'):
            name = item.a
            name = name.getText(" ").encode('utf-8')
            url = item.findAll('li', 'archive')
            pocet = url[0].a
            pocet = pocet.getText(" ").encode('utf-8')
            pocet =  re.compile('([0-9]+)').findall(pocet)
            url = str(url[0].a['href'])
            thumb = str(item.img['src'])
            print name, thumb, url, pocet[0]
            addDir(name+' ('+pocet[0]+' dílů)',url,3,thumb)

def VIDEA(url):
    doc = read_page(url)
    items = doc.find('div', id='content')
    for item in items.findAll('div', 'video-box'):
            name = item.findAll('div', 'title title-grey')
            name = name[0].span
            name = name.getText(" ").encode('utf-8')
            url = str(item.a['href'])
            print name, url
            addDir(name,url,4,icon)

def INDEX_PORADY(url):
    doc = read_page(url)
    items = doc.find('div', 'video-list')
    for item in items.findAll('div', 'show'):
            name = item.a
            name = name.getText(" ").encode('utf-8')
            url = str(item.a['href'])
            thumb = str(item.img['src'])
            print name, thumb, url
            addDir(name,url,10,thumb)            
    try:
        items = doc.find('div', 'paging')
        print items
        for item in items.findAll('a','next btn-green'):
            page = item.text.encode('utf-8') 
            if re.match('Starší díly', page, re.U):
                next_url = item['href']
                print next_url
                addDir('>> Další strana >>',next_url,3,nexticon)
    except:
        print 'strankovani nenalezeno'

def INDEX_VIDEA(url):
    doc = read_page(url)
    items = doc.find('div', id='content')
    for item in items.findAll('div', 'video'):
            name = item.img['alt'].encode('utf-8') 
            url = str(item.a['href'])
            thumb = str(item.img['src'])
            print name, thumb, url
            addDir(name,url,10,thumb)            
    try:
        items = doc.find('div', 'paging')
        for item in items.findAll('a','next'):
            page = item.text.encode('utf-8') 
            if re.match('Starší videa', page, re.U):
                next_url = item['href']
                print next_url
                addDir('>> Další strana >>',next_url,4,nexticon)
    except:
        print 'strankovani nenalezeno'
        

        
def VIDEOLINK(url,name):
    req = urllib2.Request(url)
    req.add_header('User-Agent', _UserAgent_)
    response = urllib2.urlopen(req)
    httpdata = response.read()
    response.close()
    video_link = re.compile('file: "(.+?)"').findall(httpdata)
    addLink(name,video_link[0],icon,name)

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
        print ""+url
        PORADY(url)

elif mode==2:
        print ""+url
        VIDEA(url)
elif mode==3:
        print ""+url
        INDEX_PORADY(url)        
elif mode==4:
        print ""+url
        INDEX_VIDEA(url) 
elif mode==10:
        print ""+url
        VIDEOLINK(url,name)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
