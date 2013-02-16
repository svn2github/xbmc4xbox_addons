# -*- coding: utf-8 -*-
import urllib2,urllib,re,os
from parseutils import *
from urlparse import urlparse
import xbmcplugin,xbmcgui,xbmcaddon
__baseurl__ = 'http://www.stream.cz'
__dmdbase__ = 'http://iamm.netuje.cz/xbmc/stream/'
__cdn_url__  = 'http://cdn-dispatcher.stream.cz/?id='
_UserAgent_ = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
addon = xbmcaddon.Addon('plugin.video.dmd-czech.stream')
profile = xbmc.translatePath(addon.getAddonInfo('profile'))
__settings__ = xbmcaddon.Addon(id='plugin.video.dmd-czech.stream')
home = __settings__.getAddonInfo('path')
REV = os.path.join( profile, 'list_revision')
icon = xbmc.translatePath( os.path.join( home, 'icon.png' ) )
nexticon = xbmc.translatePath( os.path.join( home, 'nextpage.png' ) )
fanart = xbmc.translatePath( os.path.join( home, 'fanart.jpg' ) )
page_pole_url = []
page_pole_no = []
searchurl = 'http://www.stream.cz/?a=search&search_text='
user_name =__settings__.getSetting('user_name')

def OBSAH():
    addDir('Televize','http://www.stream.cz/televize',1,icon)
    addDir('Uživatelská videa','http://www.stream.cz/kategorie/2-uzivatelska-videa',2,icon)
    addDir('Hudba','http://hudba.stream.cz',3,icon)
    addDir('Hledat...',__baseurl__,13,icon)
    addDir('Moje videa',__baseurl__,15,icon)
    #addDir('Filmový Stream','http://filmovy.stream.cz',4,icon)

def HUDBA_OBSAH():
    addDir('TOP20','http://music.stream.cz/klipy/top20',7,icon)
    addDir('Nejnovější klipy','http://music.stream.cz/klipy/nejnovejsi',7,icon)
    addDir('Výběr žánru','http://music.stream.cz/klipy/top20',8,icon)   
    addDir('Hudební pořady','http://music.stream.cz/porady',9,icon)   

def FILM_OBSAH():
    addDir('Film','http://filmovy.stream.cz/film',10,icon)
    addDir('Ukázky','http://filmovy.stream.cz/ukazka?sort=views',12,icon)
    addDir('Sestřihy','http://filmovy.stream.cz/sestrih',12,icon)   
    
def INDEX_TV(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', _UserAgent_)
    response = urllib2.urlopen(req)
    httpdata = response.read()
    response.close()
    match = re.compile('<li><a  href="(.+?)">(.+?)</a>').findall(httpdata)
    for link,name in match:
        if re.match('TV Prima', name, re.U):
            continue
        else:
            if not re.match('www.stream.cz', link, re.U):
                link = 'http://www.stream.cz'+link
                #print name,link
                addDir(name,link,5,icon)

def INDEX_UZIVATEL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', _UserAgent_)
    response = urllib2.urlopen(req)
    httpdata = response.read()
    response.close()
    match = re.compile('<li><a  href="(.+?)">(.+?)</a>').findall(httpdata)
    for link,name in match:
        if not re.match('http://www.stream.cz', link, re.U):
                link = 'http://www.stream.cz'+link
        #print name,link
        addDir(name,link,6,icon)

def MY_VIDEO(url):
    if url == __baseurl__:
        if user_name == '':
            xbmc.executebuiltin("XBMC.Notification('Doplněk DMD JOJ','Zadejte uživ.jméno nebo email!',30000,"+icon+")")
            __settings__.openSettings()
        if re.search('@', user_name, re.U):
            match = re.compile('(.+?)@(.+)').findall(user_name)
            for name,email in match:
                url = __baseurl__+ '/profil/' + email + '/'+ name
        else:
            url = __baseurl__+ '/profil/' + user_name
        print url            
        doc = read_page(url)
        items = doc.find('div', 'boxVideo txtRight')
        url = __baseurl__+str(items.a['href'])
        print url
    doc = read_page(url)
    items = doc.find('div', 'vertical670Box')
    for item in items.findAll('div', 'videoList'):
            name_a = item.find('h5')
            name_a = name_a.find('a') 
            name = name_a.getText(" ").encode('utf-8')
            link = __baseurl__+str(item.a['href'])
            thumb = item.find('a', 'videoListImg')
            thumb = thumb['style']
            thumb = thumb[(thumb.find('url(') + len('url(') + 1):] 
            thumb = thumb[:(thumb.find(')') - 1)]
            #print name, thumb, url
            addDir(name,link,20,thumb)
    try:
        pager = doc.find('div', 'paging')
        act_page_a = pager.find('strong',)
        act_page = act_page_a.getText(" ").encode('utf-8')
        next_page = int(act_page) + 1        
        next_url_no = int(act_page) - 1
        for item in pager.findAll('a'):
            page_url = item['href'].encode('utf-8')
            page_no = item.getText(" ").encode('utf-8')
            page_pole_url.append(page_url)
            page_pole_no.append(page_no)
        max_page_count = len(page_pole_no)-1
        url_page = int(max_page_count)-1
        if  re.match('další', page_pole_no[max_page_count], re.U):
            next_url = item['href']
            #next_url = page_pole_url[next_url_no]
            max_page = page_pole_no[url_page]
            next_label = 'Přejít na stranu '+str(next_page)+' z '+max_page
            #print next_label,__baseurl__+next_url
            addDir(next_label,__baseurl__+next_url,15,nexticon)
    except:
        print 'STRANKOVANI NENALEZENO!'

def LIST_TV(url):
    doc = read_page(url)
    items = doc.find('div', 'vertical540Box')
    for item in items.findAll('div', 'matrixThreeVideoList'):
            name_a = item.find('h5')
            name_a = name_a.find('a') 
            name = name_a.getText(" ").encode('utf-8')
            url = __baseurl__+str(item.a['href'])
            thumb = item.find('a', 'videoListImg')
            thumb = thumb['style']
            thumb = thumb[(thumb.find('url(') + len('url(') + 1):] 
            thumb = thumb[:(thumb.find(')') - 1)]
            #print name, thumb, url
            if re.match('Hudební videoarchiv', name, re.U):
                addDir('Hudební videoarchiv','http://hudba.stream.cz',3,icon)
            elif re.match('Filmové sestřihy', name, re.U):
                continue
            else:
                addDir(name,url,6,thumb)
    try:
        pager = doc.find('div', 'paging')
        act_page_a = pager.find('strong',)
        act_page = act_page_a.getText(" ").encode('utf-8')
        next_page = int(act_page) + 1        
        next_url_no = int(act_page)
        for item in pager.findAll('a'):
            page_url = item['href'].encode('utf-8')
            page_no = item.getText(" ").encode('utf-8')
            page_pole_url.append(page_url)
            page_pole_no.append(page_no)
        max_page_count = len(page_pole_no)-1
        url_page = int(max_page_count)-1
        if  re.match('další', page_pole_no[max_page_count], re.U):
            next_url = item['href']
            #next_url = page_pole_url[next_url_no]
            max_page = page_pole_no[url_page]
            next_label = 'Přejít na stranu '+str(next_page)+' z '+max_page
            #print next_label,__baseurl__+next_url
            addDir(next_label,__baseurl__+next_url,5,nexticon)
    except:
        print 'STRANKOVANI NENALEZENO!'

def LIST_UZIVATEL(url):
    doc = read_page(url)
    items = doc.find('div', 'vertical670Box')
    for item in items.findAll('div', 'matrixThreeVideoList'):
            name_a = item.find('h5')
            name_a = name_a.find('a') 
            name = name_a.getText(" ").encode('utf-8')
            link = __baseurl__+str(item.a['href'])
            thumb = item.find('a', 'videoListImg')
            thumb = thumb['style']
            thumb = thumb[(thumb.find('url(') + len('url(') + 1):] 
            thumb = thumb[:(thumb.find(')') - 1)]
            #print name, thumb, url
            addDir(name,link,20,thumb)
    try:
        pager = doc.find('div', 'paging')
        act_page_a = pager.find('strong',)
        act_page = act_page_a.getText(" ").encode('utf-8')
        next_page = int(act_page) + 1        
        next_url_no = int(act_page) - 1
        for item in pager.findAll('a'):
            page_url = item['href'].encode('utf-8')
            page_no = item.getText(" ").encode('utf-8')
            page_pole_url.append(page_url)
            page_pole_no.append(page_no)
        max_page_count = len(page_pole_no)-1
        url_page = int(max_page_count)-1
        if  re.match('další', page_pole_no[max_page_count], re.U):
            next_url = item['href']
            #next_url = page_pole_url[next_url_no]
            max_page = page_pole_no[url_page]
            next_label = 'Přejít na stranu '+str(next_page)+' z '+max_page
            #print next_label,__baseurl__+next_url
            addDir(next_label,__baseurl__+next_url,6,nexticon)
    except:
        print 'STRANKOVANI NENALEZENO!'


def SEARCH():
	keyb = xbmc.Keyboard('', 'Vyhledat na Stream.cz')
        keyb.doModal()
        if (keyb.isConfirmed()):
        	search = keyb.getText()
	        encode=urllib.quote(search)
		link = searchurl+encode
                doc = read_page(link)
                #items = doc.find('div', 'orderTabInner orderTabInnerG')
                #for item in items.findAll('a'):
                #    name = '>> '+item.getText(" ").encode('utf-8')+' <<'
                #    url = __baseurl__+str(item['href'])
                #    if re.match('>> Vše <<', name, re.U):
                #        continue
                #   #print name, url
                #    addDir(name,url,6,icon)		
                items = doc.find('div', 'vertical540Box')
                for item in items.findAll('div', 'videoList'):
                    name_a = item.find('h5')
                    name_a = name_a.find('a') 
                    name = name_a.getText(" ").encode('utf-8')
                    url = __baseurl__+str(item.a['href'])
                    thumb = item.find('a', 'videoListImg')
                    thumb = thumb['style']
                    thumb = thumb[(thumb.find('url(') + len('url(') + 1):] 
                    thumb = thumb[:(thumb.find(')') - 1)]
                    #print name, thumb, url
                    addDir(name,url,20,thumb)
                try:
                    pager = doc.find('div', 'paging')
                    act_page_a = pager.find('strong',)
                    act_page = act_page_a.getText(" ").encode('utf-8')
                    next_page = int(act_page) + 1        
                    next_url_no = int(act_page)
                    for item in pager.findAll('a'):
                        page_url = item['href'].encode('utf-8')
                        page_no = item.getText(" ").encode('utf-8')
                        page_pole_url.append(page_url)
                        page_pole_no.append(page_no)
                        max_page_count = len(page_pole_no)-1
                        url_page = int(max_page_count)-1
                        if  re.match('další', page_pole_no[max_page_count], re.U):
                            next_url = item['href']
                            #next_url = page_pole_url[next_url_no]
                            max_page = page_pole_no[url_page]
                            next_label = '>> Přejít na stranu '+str(next_page)+' z '+max_page
                            #print next_label,__baseurl__+next_url
                            addDir(next_label,__baseurl__+next_url,14,nexticon)
                except:
                    print 'STRANKOVANI NENALEZENO!'

def SEARCH2(url):
                doc = read_page(url)
                #items = doc.find('div', 'orderTabInner orderTabInnerG')
                #for item in items.findAll('a'):
                #    name = '>> '+item.getText(" ").encode('utf-8')+' <<'
                #    url = __baseurl__+str(item['href'])
                #    if re.match('>> Vše <<', name, re.U):
                #        continue
                #   #print name, url
                #    addDir(name,url,6,icon)		
                items = doc.find('div', 'vertical540Box')
                for item in items.findAll('div', 'videoList'):
                    name_a = item.find('h5')
                    name_a = name_a.find('a') 
                    name = name_a.getText(" ").encode('utf-8')
                    url = __baseurl__+str(item.a['href'])
                    thumb = item.find('a', 'videoListImg')
                    thumb = thumb['style']
                    thumb = thumb[(thumb.find('url(') + len('url(') + 1):] 
                    thumb = thumb[:(thumb.find(')') - 1)]
                    #print name, thumb, url
                    addDir(name,url,20,thumb)
                try:
                    pager = doc.find('div', 'paging')
                    act_page_a = pager.find('strong',)
                    act_page = act_page_a.getText(" ").encode('utf-8')
                    next_page = int(act_page) + 1        
                    next_url_no = int(act_page)
                    for item in pager.findAll('a'):
                        page_url = item['href'].encode('utf-8')
                        page_no = item.getText(" ").encode('utf-8')
                        page_pole_url.append(page_url)
                        page_pole_no.append(page_no)
                        max_page_count = len(page_pole_no)-1
                        url_page = int(max_page_count)-1
                        if  re.match('další', page_pole_no[max_page_count], re.U):
                            next_url = item['href']
                            #next_url = page_pole_url[next_url_no]
                            max_page = page_pole_no[url_page]
                            next_label = '>> Přejít na stranu '+str(next_page)+' z '+max_page
                            #print next_label,__baseurl__+next_url
                            addDir(next_label,__baseurl__+next_url,14,nexticon)
                except:
                    print 'STRANKOVANI NENALEZENO!'
    
def HUDBA_TOP20(url):
    doc = read_page(url)
    url = urlparse(url)
    url = url[1]+url[2]
    items = doc.find('ul', 'item_list')
    for item in items.findAll('li', 'clip'):
            name_full = item.find('div','text')
            name_a = name_full.find('a','title') 
            name_a = name_a.getText(" ").encode('utf-8')
            name_i = name_full.find('a','interpreter') 
            name_i = name_i.getText(" ").encode('utf-8')
            link = 'http://music.stream.cz'+str(item.a['href'])
            thumb = str(item.img['src'])
            #print name_a +' / '+ name_i, thumb, link
            addDir(name_a +' / '+ name_i,link,20,thumb)
    try:
        items = doc.find('div', 'pager')
        for item in items.findAll('a'):
            page = item.text.encode('utf-8') 
            if re.match('následující', page, re.U):
                next_url = item['href']
                #print next_url
                addDir('Další strana','http://'+url+next_url,7,nexticon)
    except:
        print 'Strankovani nenalezeno'


def HUDBA_ZANR(url):
    doc = read_page(url)
    items = doc.find('div', 'qf_genre_list')
    match = re.compile('<a href="(.+?)">(.+?)</a>').findall(str(items))
    for url,name in match:
        #print 'http://music.stream.cz'+url,name
        addDir(name,'http://music.stream.cz'+url,7,icon)

def HUDBA_PORADY(url):
    doc = read_page(url)
    url = urlparse(url)
    url = url[1]+url[2]
    items = doc.find('ul', 'item_list')
    for item in items.findAll('li', 'show'):
            name_full = item.find('div','text')
            name_a = name_full.find('a','title') 
            name_a = name_a.getText(" ").encode('utf-8')
            name_i = name_full.find('p','perex') 
            name_i = name_i.getText(" ").encode('utf-8')
            link = str(item.a['href'])
            if not re.match('music.stream.cz', link, re.U):
                link = 'http://music.stream.cz'+link
            thumb = str(item.img['src'])
            #print name_a +' / '+ name_i, thumb, link
            addDir(name_a +' / '+ name_i,link,20,thumb)
    try:
        items = doc.find('div', 'pager')
        for item in items.findAll('a'):
            page = item.text.encode('utf-8') 
            if re.match('následující', page, re.U):
                next_url = item['href']
                #print next_url
                addDir('Další strana','http://'+url+next_url,9,nexticon)
    except:
        print 'Strankovani nenalezeno'

def FILM_CAT(url):
    doc = read_page(url)
    items = doc.find('ul', 'movieList')
    match = re.compile('<li>(.+?)<a href="(.+?)" title=".+?">(.+?)</a></li>').findall(str(doc))
    for rok,link,name in match:
        if not re.match('filmovy.stream.cz', link, re.U):
                link = 'http://filmovy.stream.cz'+link
                #print name+rok,link
                addDir(name+' '+rok,link,11,icon)

def FILM_LIST(url):
    doc = read_page(url)
    items = doc.find('div', id='movieClips')
    for item in items.findAll('div', 'oneVideo'):
            name_a = item.find('h3')
            name_a = name_a.find('a') 
            name = name_a.getText(" ").encode('utf-8')
            url = 'http://filmovy.stream.cz'+str(item.a['href'])
            thumb = item.find('a', 'videoPic')
            thumb = thumb['style']
            thumb = thumb[(thumb.find('url(') + len('url(') + 1):] 
            thumb = thumb[:(thumb.find(')') - 1)]
            #print name, thumb, url
            addDir(name,url,20,thumb)

def FILM_LIST2(url):
    doc = read_page(url)
    url = urlparse(url)
    url = url[1]+url[2]
    items = doc.find('div', id='left')
    for item in items.findAll('div', 'oneVideo'):
            name_a = item.find('h3')
            name_a = name_a.find('a') 
            name = name_a.getText(" ").encode('utf-8')
            link = 'http://filmovy.stream.cz'+str(item.a['href'])
            thumb = item.find('a', 'videoPic')
            thumb = thumb['style']
            thumb = thumb[(thumb.find('url(') + len('url(') + 1):] 
            thumb = thumb[:(thumb.find(')') - 1)]
            #print name, thumb, link
            addDir(name,link,20,thumb)
    try:
        items = doc.find('div', 'paging')
        for item in items.findAll('a'):
            page = item.text.encode('utf-8') 
            if re.match('následující', page, re.U):
                next_url = item['href']
                #print 'http://'+url+next_url
                addDir('Další strana','http://'+url+next_url,12,nexticon)
    except:
        print 'Strankovani nenalezeno'

                
def VIDEOLINK(url,name):
    req = urllib2.Request(url)
    req.add_header('User-Agent', _UserAgent_)
    response = urllib2.urlopen(req)
    httpdata = response.read()
    response.close()
    try:
        hd_video = re.compile('cdnHD=([0-9]+)').findall(httpdata)
    except:
        print 'HD stream nenalezen'
    try:
        hq_video = re.compile('cdnHQ=([0-9]+)').findall(httpdata)
    except:
        print 'HQ stream nenalezen'
    try:
        lq_video = re.compile('cdnLQ=([0-9]+)').findall(httpdata)
    except:
        print 'LQ stream nenalezen'
    thumb = re.compile('<link rel="image_src" href="(.+?)" />').findall(httpdata)
    popis = re.compile('<meta name="title" content="(.+?)" />').findall(httpdata)
    if not len(popis) > 0:
        popis = re.compile('<title>(.+?)</title>').findall(httpdata)   

    #print name,urlhq,thumb
    if len(hd_video)>0:
        hdurl = __cdn_url__ + hd_video[0]
        #print 'HD '+'name',hdurl,popis[0]
        addLink('HD '+name,hdurl,'',popis[0])
    if len(hq_video)>0:
        hqurl = __cdn_url__ + hq_video[0]
        #print 'HQ '+'name',hqurl,'',popis[0]
        addLink('HQ '+name,hqurl,'',popis[0])
    if len(lq_video)>0:
        lqurl = __cdn_url__ + lq_video[0]
        #print'LQ '+'name',lqurl,'',popis[0]
        addLink('LQ '+name,lqurl,'',popis[0])

def PAGER(doc):
    try:
        pager = doc.find('div', 'paging')
        act_page_a = pager.find('strong',)
        act_page = act_page_a.getText(" ").encode('utf-8')
        next_page = int(act_page) + 1        
        next_url_no = int(act_page) - 1
        for item in pager.findAll('a'):
            page_url = item['href'].encode('utf-8')
            page_no = item.getText(" ").encode('utf-8')
            page_pole_url.append(page_url)
            page_pole_no.append(page_no)
        max_page_count = len(page_pole_no)-1
        url_page = int(max_page_count)-1
        if  re.match('další', page_pole_no[max_page_count], re.U):
            next_url = page_pole_url[next_url_no]
            max_page = page_pole_no[url_page]
            next_label = 'Přejít na stranu '+str(next_page)+' z '+max_page
            #print next_label,__baseurl__+next_url
            addDir(next_label,__baseurl__+next_url,5,nexticon)
    except:
        print 'STRANKOVANI NENALEZENO!'


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
        INDEX_TV(url)

elif mode==2:
        print ""+url
        INDEX_UZIVATEL(url)

elif mode==3:
        print ""+url
        HUDBA_OBSAH()

elif mode==4:
        print ""+url
        FILM_OBSAH()

elif mode==5:
        print ""+url
        LIST_TV(url)

elif mode==6:
        print ""+url
        LIST_UZIVATEL(url)

elif mode==7:
        print ""+url
        HUDBA_TOP20(url)

elif mode==8:
        print ""+url
        HUDBA_ZANR(url)

elif mode==9:
        print ""+url
        HUDBA_PORADY(url)

elif mode==10:
        print ""+url
        FILM_CAT(url)

elif mode==11:
        print ""+url
        FILM_LIST(url)

elif mode==12:
        print ""+url
        FILM_LIST2(url)

elif mode==13:
        print ""+url
        SEARCH()
elif mode==14:
        print ""+url
        SEARCH2(url)  

elif mode==15:
        print ""+url
        MY_VIDEO(url)       

elif mode==20:
        print ""+url
        VIDEOLINK(url,name)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
