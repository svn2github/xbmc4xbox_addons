# -*- coding: utf-8 -*-
import urllib2,urllib,re,os,random,decimal
from parseutils import *
import xbmcplugin,xbmcgui,xbmcaddon
__baseurl__ = 'http://www.iprima.cz/videoarchiv'
__cdn_url__  = 'http://cdn-dispatcher.stream.cz/?id='
__dmdbase__ = 'http://iamm.netuje.cz/xbmc/prima/'
_UserAgent_ = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
addon = xbmcaddon.Addon('plugin.video.dmd-czech.prima')
profile = xbmc.translatePath(addon.getAddonInfo('profile'))
__settings__ = xbmcaddon.Addon(id='plugin.video.dmd-czech.prima')
home = __settings__.getAddonInfo('path')
REV = os.path.join( profile, 'list_revision')
icon = xbmc.translatePath( os.path.join( home, 'icon.png' ) )
nexticon = xbmc.translatePath( os.path.join( home, 'nextpage.png' ) )
family = xbmc.translatePath( os.path.join( home, 'family.png' ) )
love = xbmc.translatePath( os.path.join( home, 'love.png' ) )
cool = xbmc.translatePath( os.path.join( home, 'cool.png' ) )
fanart = xbmc.translatePath( os.path.join( home, 'fanart.jpg' ) )
file = __settings__.getSetting('xml_file')
kvalita =__settings__.getSetting('kvalita')
if kvalita == '':
    xbmc.executebuiltin("XBMC.Notification('Doplněk Prima PLAY','Vyberte preferovanou kvalitu!',30000,"+icon+")")
    __settings__.openSettings() 

def replace_words(text, word_dic):
    rc = re.compile('|'.join(map(re.escape, word_dic)))
    def translate(match):
        return word_dic[match.group(0)]
    return rc.sub(translate, text)

word_dic = {
'\u00e1': 'á',
'\u00e9': 'é',
'\u00ed': 'í',
'\u00fd': 'ý',
'\u00f3': 'ó',
'\u00fa': 'ú',
'\u016f': 'ů',
'\u011b': 'ě',
'\u0161': 'š',
'\u0165': 'ť',
'\u010d': 'č',
'\u0159': 'ř',
'\u017e': 'ž',
'\u010f': 'ď',
'\u0148': 'ň',
'\u00C0': 'Á',
'\u00c9': 'É',
'\u00cd': 'Í',
'\u00d3': 'Ó',
'\u00da': 'Ú',
'\u016e': 'Ů',
'\u0115': 'Ě',
'\u0160': 'Š',
'\u010c': 'Č',
'\u0158': 'Ř',
'\u0164': 'Ť',
'\u017d': 'Ž',
'\u010e': 'Ď',
'\u0147': 'Ň'
}

def OBSAH():
    addDir('Family','http://play.iprima.cz/iprima',1,family,'','1')
    addDir('Love','http://play.iprima.cz/love',1,love,'','3')
    addDir('COOL','http://play.iprima.cz/cool',1,cool,'','2')
    
def KATEGORIE(url,page,kanal):
    porady = []
    request = urllib2.Request(url)
    con = urllib2.urlopen(request)
    data = con.read()
    con.close()
    match = re.compile('"name":"(.+?)","tid":"(.+?)"').findall(data)
    for porad,porad_id in match:
        porady.append([porad,porad_id])
        porady.sort()   
    for porad, porad_id in porady:
        #print porad, porad_id
        #porad=replace_words(porad)
        addDir(replace_words(porad, word_dic),porad_id,4,__dmdbase__+porad_id+'.jpg',0,kanal)


    
def INDEX(url,page,kanal):
    if int(page) != 0:
        strquery = '?method=json&action=relevant&per_page=12&channel='+str(kanal)+'&page='+str(page)
    else:
        strquery = '?method=json&action=relevant&per_page=12&channel='+str(kanal)
    doc = read_page('http://play.iprima.cz/videoarchiv_ajax/all/'+str(url)+strquery)
    tid = re.compile('"tid":"(.+?)"').findall(str(doc))
    match = re.compile('"nid":"(.+?)","title":"(.+?)","image":"(.+?)","date":"(.+?)"').findall(str(doc))
    for videoid,name,thumb,datum in match:
            name = replace_words(name, word_dic)
            thumb = replace_words(thumb, word_dic)
            thumb = re.sub('98x55','280x158',thumb)
            if kanal == 1:
                addDir(str(name),'http://play.iprima.cz/iprima/'+videoid+'/'+tid[0],10,'http://www.iprima.cz/'+thumb,'','')
            elif kanal == 2:
                addDir(str(name),'http://play.iprima.cz/cool/'+videoid+'/'+tid[0],10,'http://www.iprima.cz/'+thumb,'','')
            elif kanal == 3:
                addDir(str(name),'http://play.iprima.cz/love/'+videoid+'/'+tid[0],10,'http://www.iprima.cz/'+thumb,'','')
    strankovani = re.compile('"total":(.+?),"from":.+?,"to":.+?,"page":(.+?),').findall(str(doc))
    for page_total,act_page in strankovani:
        print page_total,act_page
        if int(page_total) > 12:
            act_page = act_page.replace('"','')
            next_page = int(act_page)  + 1
            max_page =  int(round(int(page_total)/12 ) )
            if next_page < max_page+1:
                max_page = str(max_page+1)
                #print '>> Další strana >>',url,1,next_page
                addDir('>> Další strana ('+str(next_page+1)+' z '+max_page+')',url,4,nexticon,next_page,kanal)
        
def VIDEOLINK(url,name):
    strquery = '?method=json&action=video'
    request = urllib2.Request(url, strquery)
    con = urllib2.urlopen(request)
    data = con.read()
    con.close()
    print url
    stream_video = re.compile('cdnID=([0-9]+)').findall(data)
    if len(stream_video) > 0:
        print 'LQ '+__cdn_url__+name,stream_video[0],icon,''
        addLink('LQ '+name,__cdn_url__+stream_video[0],icon,'')        
    else:
        hq_stream = re.compile("'hq_id':'(.+?)'").findall(data)
        lq_stream = re.compile("'lq_id':'(.+?)'").findall(data)
        hd_stream = re.sub('_1000','_1500',hq_stream[0])
        geo_zone = re.compile("'zoneGEO':(.+?),").findall(data)        
        thumb = re.compile("'thumbnail':'(.+?)'").findall(data)
        nahled = 'http://embed.livebox.cz/iprima/'+thumb[0]
        print geo_zone[0]
        key = 'http://embed.livebox.cz/iprimaplay/player-embed-v2.js?__tok'+str(gen_random_decimal(1073741824))+'__='+str(gen_random_decimal(1073741824))
        req = urllib2.Request(key)
        req.add_header('User-Agent', _UserAgent_)
        req.add_header('Referer', url)
        response = urllib2.urlopen(req)
        keydata = response.read()
        response.close()
        keydata = re.compile("auth=(.*?)'").findall(keydata)
        if geo_zone[0] == "1":
            hd_url = 'rtmp://bcastiw.livebox.cz:80/iprima_token_'+geo_zone[0]+'?auth='+keydata[0]+'/mp4:'+hd_stream
            hq_url = 'rtmp://bcastiw.livebox.cz:80/iprima_token_'+geo_zone[0]+'?auth='+keydata[0]+'/mp4:'+hq_stream[0]
            lq_url = 'rtmp://bcastiw.livebox.cz:80/iprima_token_'+geo_zone[0]+'?auth='+keydata[0]+'/mp4:'+lq_stream[0]
        else:
            hd_url = 'rtmp://bcastnw.livebox.cz:80/iprima_token?auth='+keydata[0]+'/mp4:'+hd_stream
            hq_url = 'rtmp://bcastnw.livebox.cz:80/iprima_token?auth='+keydata[0]+'/mp4:'+hq_stream[0]
            lq_url = 'rtmp://bcastnw.livebox.cz:80/iprima_token?auth='+keydata[0]+'/mp4:'+lq_stream[0]

        #print nahled, hq_url, lq_url
        if kvalita == "HD":
            print 'HD '+name,hq_url,nahled,name
            addLink('HD '+name,hd_url,nahled,name)
            addLink('HQ '+name,hq_url,nahled,name)            
        elif kvalita == "HQ":
            print 'HQ '+name,lq_url,nahled,name
            addLink('HQ '+name,hq_url,nahled,name)
            addLink('LQ '+name,lq_url,nahled,name)
        else:            
            print 'LQ '+name,lq_url,nahled,name
            addLink('LQ '+name,lq_url,nahled,name)


def gen_random_decimal(d):
        return decimal.Decimal('%d' % (random.randint(0,d)))

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

def addDir(name,url,mode,iconimage,page,kanal):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&page="+str(page)+"&kanal="+str(kanal)
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
page=None
kanal=None
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
try:
        page=int(params["page"])
except:
        pass
try:
        kanal=int(params["kanal"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Page: "+str(page)
print "Kanal: "+str(kanal)

if mode==None or url==None or len(url)<1:
        OBSAH()
       
elif mode==1:
        print ""+str(url)
        print ""+str(kanal)
        print ""+str(page)
        KATEGORIE(url,page,kanal)

elif mode==4:
        print ""+str(url)
        print ""+str(kanal)
        print ""+str(page)
        INDEX(url,page,kanal)
        
elif mode==10:
        print ""+url
        VIDEOLINK(url,name)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
