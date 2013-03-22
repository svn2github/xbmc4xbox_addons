#This test program is for finding the correct Regular expressions on a page to insert into the plugin template.
#After you have entered the url between the url='here' - use ctrl-v
#Copy the info from the source html and put it between the match=re.compile('here')
#press F5 to run if match is blank close and try again.
import urllib,urllib2,re
import xbmcplugin,xbmcgui
#import urlresolver
#from t0mm0.common.net import Net
#net = Net()
import time
#from xml.etree import ElementTree as ET
#fullurl = urllib.quote("http://videobull.com",safe="%/:=&?~#+!$,;'@()*[]")
#url=fullurl
#req = urllib2.Request(url)
#response = urllib2.urlopen(req)
#req = urllib2.Request(url)
#req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
#link=response.read()
#response.close()
movielink = "http://www.videobull.com/feeds/"
def CATEGORIES():
        addLink('2GB Sydney Talk Radio','http://shoutcast.2gb.com:80/2ch','http://www.2gb.com/sites/all/themes/two_gb/logo.png')
#        addDir( 'TV-SHOWS','http://www.videobull.com/',2,'http://videobull.com/wp-content/themes/videozoom/images/logo.png')
                       
def INDEX(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        
        response.close()
        match = re.compile('/*/?<item>.+?title>(.+?).?/title>.+?link>(.+?).?/link>.+?/item>', re.DOTALL).findall(link)
        for name,url in match:
                addDir(name,url,4,'')
def INDEX2(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('/*/?<li>.+?a href="(.+?)" rel="bookmark" title="(.+?)">.+?img src="(.+?)".+?/>.?/a>.+?/li>', re.DOTALL).findall(link)
        for url,name,thumb in match:
                addDir(name,url,4,thumb)

def read(url):
#    _log("read "+url)

    f = urllib2.urlopen(url)
    data = f.read()
    f.close()
    
    return data
                
def EPISODES(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('/*/?<li>.+?a href="(.+?)" rel="bookmark" title="(.+?)">.+?img src="(.+?)".+?/>.?/a>.+?/li>').findall(link)
        for url,name,thumb in match:
                if not thumb.find('http://')>0:
                        thumb='http://www.tvdash.com/'+thumb
                        addDir(name,'http://www.videobull.com/'+url,4,thumb)

def VIDEOLINKS(url,name):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('''<a id='.+?' href='http://adf.ly/369307/(.+?)' target='_blank' rel='nofollow'>(.+?)</a>''', re.DOTALL).findall(link)
        print match
        for url,name in match:
              
                 
                
              

                        
                
                addLink(name,url,'')
				
def AUDIOLINKS(url,name):
        addLink(name,'http://shoutcast.2gb.com:80/2ch','')
        
          
          
        
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
       
elif mode==1:
        print ""+url
        INDEX(url)
        
elif mode==2:
        print ""+url
        INDEX2(url)

elif mode==3:
        print ""+url
        EPISODES(url)

elif mode==4:
        print ""+url
        VIDEOLINKS(url,name)
		
elif mode==5:
        print ""+url
        AUDIOLINKS(url,name)



xbmcplugin.endOfDirectory(int(sys.argv[1]))
#movielink = "http://www.videobull.com/feeds/" + "decrypt'/'un[0]" + "k1[0]" + "k2[0]" + "/"
#match = re.compile('movielink + <item> + <title>"(.+?)"</item> + </title>').findall(link)
#name="title"
#addDir('match[0],name=".+?","link=(.+?)",')
#print match[0]
#match=re.compile('<a href="(.+?)" title=".+?">(.+?)/a>').findall(link)



