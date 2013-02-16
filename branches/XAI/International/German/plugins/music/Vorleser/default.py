import urllib,urllib2,re,xbmcplugin,xbmcgui
import sys, os, os.path

#author:
#elypter
#-mail:elypter@yahoo.de

#description:
#This plugin provides access to all audiobooks of vorleser.net
#
#-If you think something in this plugin needs to be changed, send an email

#version-history:
#1_b1:
#-first release
#

baseurl="http://www.vorleser.net"

def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        liz.setInfo( type="Music", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok
		
def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Music", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

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
		
def MUSICDIR(url,name):
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		match=re.compile('\<A HREF\="\.\./html/([0-9a-zA-Z_]*\.html)"\>([^<>]*)\</A\>').findall(link)
		for url,name in match:
			addDir(name,baseurl+'/html/'+url,2,'')

def MUSICLINK(url,name):
		print "Zeige Autorenseite an: "+url
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		match=re.compile('href\="([^<>"]*/)([^<>"/]*\.mp3)"').findall(link.lower())
		#match=re.compile('href\="([^<>"]*\.mp3)"').findall(link.lower())
		#print match
		for base,url in match:
			addLink(url,base+url,'')
		
			
params=get_params()
url=None
name=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
		
if url==None or len(url)<1:
		MUSICDIR('http://www.vorleser.net/html/autoren.html','noname')
else:	
		MUSICLINK(url,'noname')
	

xbmcplugin.endOfDirectory(int(sys.argv[1]))
