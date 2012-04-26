import urllib,urllib2,re,sys,xbmcplugin,xbmcgui,xbmcaddon
pluginhandle = int(sys.argv[1])

def CATS():
        addDir('Looney Tunes','http://staticswf.kidswb.com/kidswb/xml/videofeedlight.xml',1,'http://staticswf.kidswb.com/franchise/content/images/touts/video_channel_thumbs/LooneyTunes_video.jpg','')
        addDir('The Flintstones','http://staticswf.kidswb.com/kidswb/xml/videofeedlight.xml',2,'http://staticswf.kidswb.com/franchise/content/images/touts/video_channel_thumbs/Flintstones_video.jpg','')
        addDir('The Jetsons','http://staticswf.kidswb.com/kidswb/xml/videofeedlight.xml',3,'http://staticswf.kidswb.com/franchise/content/images/touts/video_channel_thumbs/Jetsons_video.jpg','')
        addDir('The New Scoobydoo Mysteries','http://staticswf.kidswb.com/kidswb/xml/videofeedlight.xml',4,'http://staticswf.kidswb.com/franchise/content/images/touts/video_channel_thumbs/ScoobyDooMysteries_video.jpg','')
        addDir('Shaggy and Scoobydoo Get A Clue','http://staticswf.kidswb.com/kidswb/xml/videofeedlight.xml',5,'http://staticswf.kidswb.com/franchise/content/images/touts/video_channel_thumbs/ShaggyScoobyGetAClue_video.jpg','')
        addDir('The Smurfs','http://staticswf.kidswb.com/kidswb/xml/videofeedlight.xml',6,'http://staticswf.kidswb.com/franchise/content/images/touts/video_channel_thumbs/smurf_video.jpg','')
        addDir('Thundercats','http://staticswf.kidswb.com/kidswb/xml/videofeedlight.xml',7,'http://staticswf.kidswb.com/franchise/content/images/touts/video_channel_thumbs/Thundercats.jpg','')
        addDir('Tom and Jerry Tales','http://staticswf.kidswb.com/kidswb/xml/videofeedlight.xml',8,'http://staticswf.kidswb.com/franchise/content/images/touts/video_channel_thumbs/TomJerryTales_video.jpg','')
        addDir('Ozzy and Drix','http://staticswf.kidswb.com/kidswb/xml/videofeedlight.xml',9,'http://staticswf.kidswb.com/franchise/content/images/touts/video_channel_thumbs/OzzieDrix_video.jpg','')
        addDir('Xiaolin Showdown','http://staticswf.kidswb.com/kidswb/xml/videofeedlight.xml',10,'http://staticswf.kidswb.com/franchise/content/images/touts/video_channel_thumbs/XiaolinShowdown_video.jpg','')


def LOON(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req).read()
	code=re.sub('&quot;','',response)
	code1=re.sub('&#039;','',code)
	code2=re.sub('&#215;','',code1)
	code3=re.sub('&#038;','',code2)
	code4=re.sub('&#8216;','',code3)
	code5=re.sub('&#8217;','',code4)
	code6=re.sub('&#8211;','',code5)
	code7=re.sub('&#8220;','',code6)
	code8=re.sub('&#8221;','',code7)
	code9=re.sub('&#8212;','',code8)
    	code10=re.sub('&amp;','&',code9)
        code11=re.sub("`",'',code10)
        names = re.compile('url=".+?looneytunes/(.+?)".+?title>(.+?)<.+?isPermaLink="false">(.+?)</guid>').findall(code11)
	for thumb,name,url in names:
	        u=sys.argv[0]+"?url="+urllib.quote_plus('http://metaframe.digitalsmiths.tv/v2/WBtv/assets/'+url+'/partner/11?format=json',name)+"&mode="+str(11)
                item=xbmcgui.ListItem(name.replace('&amp;','&'), thumbnailImage='http://pdl.warnerbros.com/wbtv/channels/thumbs/looneytunes/'+thumb)
          	item.setInfo( type="Video", infoLabels={ "Title": name} )                
		item.setProperty('IsPlayable', 'true')
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item)
url="http://pdl.warnerbros.com/wbtv/channels/thumbs/looneytunes/01/looneytunes_01_983_brm_w0315_103x69.jpg"
def FLINTSTONES(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req).read()
	print response
	code=re.sub('&quot;','',response)
	code1=re.sub('&#039;','',code)
	code2=re.sub('&#215;','',code1)
	code3=re.sub('&#038;','',code2)
	code4=re.sub('&#8216;','',code3)
	code5=re.sub('&#8217;','',code4)
	code6=re.sub('&#8211;','',code5)
	code7=re.sub('&#8220;','',code6)
	code8=re.sub('&#8221;','',code7)
	code9=re.sub('&#8212;','',code8)
    	code10=re.sub('&amp;','&',code9)
        code11=re.sub("`",'',code10)
        names = re.compile('url=".+?theflintstones/(.+?)".+?title>(.+?)<.+?isPermaLink="false">(.+?)</guid>').findall(code11)
	for thumb,name,url in names:
	        u=sys.argv[0]+"?url="+urllib.quote_plus('http://metaframe.digitalsmiths.tv/v2/WBtv/assets/'+url+'/partner/11?format=json',name)+"&mode="+str(11)
                item=xbmcgui.ListItem(name.replace('&amp;','&'), thumbnailImage='http://pdl.warnerbros.com/wbtv/channels/thumbs/theflintstones/'+thumb)
          	item.setInfo( type="Video", infoLabels={ "Title": name} )                
		item.setProperty('IsPlayable', 'true')
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item)

def JETSONS(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req).read()
	print response
	code=re.sub('&quot;','',response)
	code1=re.sub('&#039;','',code)
	code2=re.sub('&#215;','',code1)
	code3=re.sub('&#038;','',code2)
	code4=re.sub('&#8216;','',code3)
	code5=re.sub('&#8217;','',code4)
	code6=re.sub('&#8211;','',code5)
	code7=re.sub('&#8220;','',code6)
	code8=re.sub('&#8221;','',code7)
	code9=re.sub('&#8212;','',code8)
    	code10=re.sub('&amp;','&',code9)
        code11=re.sub("`",'',code10)
        names = re.compile('url=".+?thejetsons/(.+?)".+?title>(.+?)<.+?isPermaLink="false">(.+?)</guid>').findall(code11)  
	for thumb,name,url in names:
	        u=sys.argv[0]+"?url="+urllib.quote_plus('http://metaframe.digitalsmiths.tv/v2/WBtv/assets/'+url+'/partner/11?format=json',name)+"&mode="+str(11)
                item=xbmcgui.ListItem(name.replace('&amp;','&'), thumbnailImage='http://pdl.warnerbros.com/wbtv/channels/thumbs/thejetsons/'+thumb)
          	item.setInfo( type="Video", infoLabels={ "Title": name} )                
		item.setProperty('IsPlayable', 'true')
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item)

def NEWSCOOBY(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req).read()
	print response
	code=re.sub('&quot;','',response)
	code1=re.sub('&#039;','',code)
	code2=re.sub('&#215;','',code1)
	code3=re.sub('&#038;','',code2)
	code4=re.sub('&#8216;','',code3)
	code5=re.sub('&#8217;','',code4)
	code6=re.sub('&#8211;','',code5)
	code7=re.sub('&#8220;','',code6)
	code8=re.sub('&#8221;','',code7)
	code9=re.sub('&#8212;','',code8)
    	code10=re.sub('&amp;','&',code9)
        code11=re.sub("`",'',code10)
        names = re.compile('url=".+?thenewscoobydoomysteries/(.+?)".+?title>(.+?)<.+?isPermaLink="false">(.+?)</guid>').findall(code11)  
	for thumb,name,url in names:
	        u=sys.argv[0]+"?url="+urllib.quote_plus('http://metaframe.digitalsmiths.tv/v2/WBtv/assets/'+url+'/partner/11?format=json',name)+"&mode="+str(11)
                item=xbmcgui.ListItem(name.replace('&amp;','&'), thumbnailImage='http://pdl.warnerbros.com/wbtv/channels/thumbs/thenewscoobydoomysteries/'+thumb)
          	item.setInfo( type="Video", infoLabels={ "Title": name} )                
		item.setProperty('IsPlayable', 'true')
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item)

def SHAGGY(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req).read()
	print response
	code=re.sub('&quot;','',response)
	code1=re.sub('&#039;','',code)
	code2=re.sub('&#215;','',code1)
	code3=re.sub('&#038;','',code2)
	code4=re.sub('&#8216;','',code3)
	code5=re.sub('&#8217;','',code4)
	code6=re.sub('&#8211;','',code5)
	code7=re.sub('&#8220;','',code6)
	code8=re.sub('&#8221;','',code7)
	code9=re.sub('&#8212;','',code8)
    	code10=re.sub('&amp;','&',code9)
        code11=re.sub("`",'',code10)
        names = re.compile('url=".+?shaggyandscoobydoogetaclue/(.+?)".+?title>(.+?)<.+?isPermaLink="false">(.+?)</guid>').findall(code11)  
	for thumb,name,url in names:
	        u=sys.argv[0]+"?url="+urllib.quote_plus('http://metaframe.digitalsmiths.tv/v2/WBtv/assets/'+url+'/partner/11?format=json',name)+"&mode="+str(11)
                item=xbmcgui.ListItem(name.replace('&amp;','&'), thumbnailImage='http://pdl.warnerbros.com/wbtv/channels/thumbs/shaggyandscoobydoogetaclue/'+thumb)
          	item.setInfo( type="Video", infoLabels={ "Title": name} )                
		item.setProperty('IsPlayable', 'true')
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item)

def SMURFS(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req).read()
	print response
	code=re.sub('&quot;','',response)
	code1=re.sub('&#039;','',code)
	code2=re.sub('&#215;','',code1)
	code3=re.sub('&#038;','',code2)
	code4=re.sub('&#8216;','',code3)
	code5=re.sub('&#8217;','',code4)
	code6=re.sub('&#8211;','',code5)
	code7=re.sub('&#8220;','',code6)
	code8=re.sub('&#8221;','',code7)
	code9=re.sub('&#8212;','',code8)
    	code10=re.sub('&amp;','&',code9)
        code11=re.sub("`",'',code10)
        names = re.compile('url=".+?smurfs/(.+?)".+?title>(.+?)<.+?isPermaLink="false">(.+?)</guid>').findall(code11)  
	for thumb,name,url in names:
	        u=sys.argv[0]+"?url="+urllib.quote_plus('http://metaframe.digitalsmiths.tv/v2/WBtv/assets/'+url+'/partner/11?format=json',name)+"&mode="+str(11)
                item=xbmcgui.ListItem(name.replace('&amp;','&'), thumbnailImage='http://pdl.warnerbros.com/wbtv/channels/thumbs/smurfs/'+thumb)
          	item.setInfo( type="Video", infoLabels={ "Title": name} )                
		item.setProperty('IsPlayable', 'true')
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item)

def THUNDERCATS(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req).read()
	print response
	code=re.sub('&quot;','',response)
	code1=re.sub('&#039;','',code)
	code2=re.sub('&#215;','',code1)
	code3=re.sub('&#038;','',code2)
	code4=re.sub('&#8216;','',code3)
	code5=re.sub('&#8217;','',code4)
	code6=re.sub('&#8211;','',code5)
	code7=re.sub('&#8220;','',code6)
	code8=re.sub('&#8221;','',code7)
	code9=re.sub('&#8212;','',code8)
    	code10=re.sub('&amp;','&',code9)
        code11=re.sub("`",'',code10)
        names = re.compile('url=".+?thundercats/(.+?)".+?title>(.+?)<.+?isPermaLink="false">(.+?)</guid>').findall(code11)  
	for thumb,name,url in names:
	        u=sys.argv[0]+"?url="+urllib.quote_plus('http://metaframe.digitalsmiths.tv/v2/WBtv/assets/'+url+'/partner/11?format=json',name)+"&mode="+str(11)
                item=xbmcgui.ListItem(name.replace('&amp;','&'), thumbnailImage='http://pdl.warnerbros.com/wbtv/channels/thumbs/thundercats/'+thumb)
          	item.setInfo( type="Video", infoLabels={ "Title": name} )                
		item.setProperty('IsPlayable', 'true')
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item)

def TOM(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req).read()
	print response
	code=re.sub('&quot;','',response)
	code1=re.sub('&#039;','',code)
	code2=re.sub('&#215;','',code1)
	code3=re.sub('&#038;','',code2)
	code4=re.sub('&#8216;','',code3)
	code5=re.sub('&#8217;','',code4)
	code6=re.sub('&#8211;','',code5)
	code7=re.sub('&#8220;','',code6)
	code8=re.sub('&#8221;','',code7)
	code9=re.sub('&#8212;','',code8)
    	code10=re.sub('&amp;','&',code9)
        code11=re.sub("`",'',code10)
        names = re.compile('url=".+?tomandjerrytales/(.+?)".+?title>(.+?)<.+?isPermaLink="false">(.+?)</guid>').findall(code11)  
	for thumb,name,url in names:
	        u=sys.argv[0]+"?url="+urllib.quote_plus('http://metaframe.digitalsmiths.tv/v2/WBtv/assets/'+url+'/partner/11?format=json',name)+"&mode="+str(11)
                item=xbmcgui.ListItem(name.replace('&amp;','&'), thumbnailImage='http://pdl.warnerbros.com/wbtv/channels/thumbs/tomandjerrytales/'+thumb)
          	item.setInfo( type="Video", infoLabels={ "Title": name} )                
		item.setProperty('IsPlayable', 'true')
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item)

def OZZY(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req).read()
	print response
	code=re.sub('&quot;','',response)
	code1=re.sub('&#039;','',code)
	code2=re.sub('&#215;','',code1)
	code3=re.sub('&#038;','',code2)
	code4=re.sub('&#8216;','',code3)
	code5=re.sub('&#8217;','',code4)
	code6=re.sub('&#8211;','',code5)
	code7=re.sub('&#8220;','',code6)
	code8=re.sub('&#8221;','',code7)
	code9=re.sub('&#8212;','',code8)
    	code10=re.sub('&amp;','&',code9)
        code11=re.sub("`",'',code10)
        names = re.compile('url=".+?ozzyanddrix/(.+?)".+?title>(.+?)<.+?isPermaLink="false">(.+?)</guid>').findall(code11)  
	for thumb,name,url in names:
	        u=sys.argv[0]+"?url="+urllib.quote_plus('http://metaframe.digitalsmiths.tv/v2/WBtv/assets/'+url+'/partner/11?format=json',name)+"&mode="+str(11)
                item=xbmcgui.ListItem(name.replace('&amp;','&'), thumbnailImage='http://pdl.warnerbros.com/wbtv/channels/thumbs/ozzyanddrix/'+thumb)
          	item.setInfo( type="Video", infoLabels={ "Title": name} )                
		item.setProperty('IsPlayable', 'true')
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item)

def XIAO(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req).read()
	print response
	code=re.sub('&quot;','',response)
	code1=re.sub('&#039;','',code)
	code2=re.sub('&#215;','',code1)
	code3=re.sub('&#038;','',code2)
	code4=re.sub('&#8216;','',code3)
	code5=re.sub('&#8217;','',code4)
	code6=re.sub('&#8211;','',code5)
	code7=re.sub('&#8220;','',code6)
	code8=re.sub('&#8221;','',code7)
	code9=re.sub('&#8212;','',code8)
    	code10=re.sub('&amp;','&',code9)
        code11=re.sub("`",'',code10)
        names = re.compile('url=".+?xiaolinshowdown/(.+?)".+?title>(.+?)<.+?isPermaLink="false">(.+?)</guid>').findall(code11)  
	for thumb,name,url in names:
	        u=sys.argv[0]+"?url="+urllib.quote_plus('http://metaframe.digitalsmiths.tv/v2/WBtv/assets/'+url+'/partner/11?format=json',name)+"&mode="+str(11)
                item=xbmcgui.ListItem(name.replace('&amp;','&'), 'http://pdl.warnerbros.com/wbtv/channels/thumbs/xiaolinshowdown/'+thumb)
          	item.setInfo( type="Video", infoLabels={ "Title": name} )                
		item.setProperty('IsPlayable', 'true')
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item)


def PLAY(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        page = urllib2.urlopen(req)
	link = page.read()
	finalurl = re.compile('"rtmpe(.+?)"}').findall(link)
     	item = xbmcgui.ListItem(path='rtmpe'+finalurl[0])
        xbmcplugin.setResolvedUrl(pluginhandle, True, item)


	
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

def addDir(name,url,mode,thumbnail,plot=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
        liz.setInfo( type="Video", infoLabels={ "Title": name,
                                                "plot": plot} )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

      
def addLink(name,url,iconimage,plot,date):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setInfo( type="Video", infoLabels={ "Plot": plot} )
        liz.setInfo( type="Video", infoLabels={ "Date": date} )
	liz.setProperty("IsPlayable","true");
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
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
        print "categories"
        CATS()
elif mode==1:
        print "PAGE"
        LOON(url)
elif mode==2:
        print "PAGE"
        FLINTSTONES(url)
elif mode==3:
        print "PAGE"
        JETSONS(url)
elif mode==4:
        print "PAGE"
        NEWSCOOBY(url)
elif mode==5:
        print "PAGE"
        SHAGGY(url)
elif mode==6:
        print "PAGE"
        SMURFS(url)
elif mode==7:
        print "PAGE"
        THUNDERCATS(url)
elif mode==8:
        print "PAGE"
        TOM(url)
elif mode==9:
        print "PAGE"
        OZZY(url)
elif mode==10:
        print "PAGE"
        XIAO(url)
elif mode==11:
        print "PAGE"
        PLAY(url)
        
xbmcplugin.endOfDirectory(int(sys.argv[1]))