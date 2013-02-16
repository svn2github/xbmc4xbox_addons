# -*- coding: iso-8859-1 -*-
import urllib,urllib2,re,xbmcplugin,xbmcgui
import xbmcaddon

pluginhandle = int(sys.argv[1])

baseurl = 'http://www.sat1.de'
__settings__ = xbmcaddon.Addon(id='plugin.video.sat1')

if (__settings__.getSetting("hd_logo") == '0'):
	hd_logo = "0"
elif (__settings__.getSetting("hd_logo") == '1'):
	hd_logo = "1"


def CATEGORIES():
	#print "###########################################################################hdlogo"+hd_logo
        req = urllib2.Request(baseurl+'/tv')
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
	match_section=re.compile('<section class="shows_box module_group">(.+?)</section>', re.DOTALL).findall(link)
	namelist = ''
        for section in match_section:
#		print section
        	match_shows=re.compile('<figure>.+?href="(.+?)".+?src="(.+?)".+?alt="(.+?)"', re.DOTALL).findall(section)
		for url,thumb,name in match_shows:
			if url != '/tv/criminal-minds' and url != '/tv/navy-cis' and url != '/tv/navy-cis-la':
				name = name.replace('bitte-melde-dich-citylight','Julia Leischik sucht: Bitte melde dich')
				name = name.replace('Knallerfrauen_citylight','Knallerfrauen - Sketch-Comedy mit Martina Hill')
				name = name.replace('biggest_loser_citylight','The Biggest Loser - Abspecken im Doppelpack')
				name = name.replace('tiermessies_citylight','Tiermessies außer Kontrolle')
				name = name.replace('Die_dreisten_Drei_jetzt_noch_dreister_citylight','Die dreisten Drei - jetzt noch dreister')
				name = name.replace('haraldschmidt-citylight','Die Harald Schmidt Show')
				name = name.replace('" title=','Schicksale')
				name = name.replace('24-stunden-citylight','24 Stunden')
				name = name.replace('akte_citylight','Akte 20.12')
				name = name.replace('akte_thema_citylight','Akte Thema')
				name = name.replace('alarm_citylight','Alarm!')
				name = name.replace('citylight_Britt_Neu','Britt')
				name = name.replace('danni-lowinski-citylight','Danni Lowinski')
				name = name.replace('Das große Allgemeinwissensquiz - dasgrosseallgemeinwissensquiz_citylight','Das große Allgemeinwissensquiz')
				name = name.replace(' - dasgrosseallgemeinwissensquiz_citylight','')
				name = name.replace('sat1-magazin','Das Sat1 Magazin')
				name = name.replace('der-letzte-bulle','Der letzte Bulle')
				name = name.replace('die-dreisten-drei-citylight','Die dreisten Drei')
				name = name.replace('dieperfekteminute-citylight','Die perfekte Minute')
				name = name.replace('dna-unbekannt-citylight','DNA unbekannt')
				name = name.replace('einsgegeneins-citylight','Eins gegen Eins')
				name = name.replace('erziehungs-alarm-citylight','Erziehungs Alarm')
				name = name.replace('ffs-citylight','Sat1 Frühstücksfernsehen')
				name = name.replace('genial-daneben-citylight','Genial daneben')
				name = name.replace('hawaii-five-o-citylight','Hawaii Five-O')
				name = name.replace('k11-citylight','K11-Kommissare im Einsatz')
				name = name.replace('kilo-alarm-citylight','Kilo Alarm')
				name = name.replace('ladykracher-citylight','Ladykracher')
				name = name.replace('lenssen2_citylight','Lenssen')
				name = name.replace('lenssen-citylight','Lenssen & Partner')
				name = name.replace('love-green-citylight','Love Green')
				name = name.replace('mein-mann-kann-citylight','Mein Mann kanns')
				name = name.replace('mensch-markus-citylight','Mensch Markus')
				name = name.replace('NCSI-citylight','NCIS')
				name = name.replace('NCSILA-citylight','NCIS: Los Angeles')
				name = name.replace('pastewka-citylight','Pastewka')
				name = name.replace('Pures_Leben_citylight','Pures Leben - Mitten in Deutschland')
				name = name.replace('richter-alexander-hold-citylight','Richter Alexander Hold')
				name = name.replace('richterin-barbara-salesch-citylight','Richterin Barbara Salesch')
				name = name.replace('schillerstrasse-citylight','Schillerstraße')
				name = name.replace('schoenheitsalarm_citylight','Schönheits Alarm')
				name = name.replace('schwer-verliebt-citylight','Schwer Verliebt')
				name = name.replace('sechserpack-citylight','Sechserpack')
				name = name.replace('so-gesehen-citylight','So gesehen')
				name = name.replace('the-mentalist-citylight','The Mentalist')
				name = name.replace('TheWinneris_Citylight_vorlaeufig','The Winner is')
				name = name.replace('vom-eigene-vater-entfuehrt-muetter-kaempfen-um-ihre-kinder-citylight','Vom eigenen Vater entführt - Mütter kämpfen um ihre Kinder')
				name = name.replace('zeugen-gesucht-citylight','Zeuge gesucht')
				name = name.replace('kallwass-citylight','Zwei bei Kallwass')

	                	addDir(name,baseurl+url+'/video',1,baseurl+thumb)



def VIDEOLINKS(url,name):#1
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()

	if 'NCIS' in name:
		print 'Ignoriere NCIS'

		#match_videos=re.compile('<section class="stage stage_single stage_1_topic module_group trackable_teaser">.+?<a href="(.+?)".+?src="(.+?)".+?<h2>(.+?)</h2>.+?</section>', re.DOTALL).findall(link)
		#for url,thumb,name in match_videos:
               	#	addLink(name,baseurl+url,2,thumb)
	else:

		match_videos=re.compile('<div class="video_teaser class-clip">(.+?)</div>', re.DOTALL).findall(link)

		match_next=re.compile('<a class="next" href="(.+?)">', re.DOTALL).findall(link)

		for video in match_videos:
			match_video=re.compile('<a href="(.+?)".+?src="(.+?)".+?<strong>(.+?)</strong>', re.DOTALL).findall(video)

			for url,thumb,name in match_video:
				if hd_logo == '1':
					thumb = thumb.replace('154x87.jpg','410x250.jpg')

                		addLink(name,baseurl+url,2,thumb)
	"""
	x = "0"
	for next in match_next:
		if x == "0":
			url = next
		if x == "1":
			addDir('Nächste Seite',baseurl+url,1,'')
		x = x + "1"
	"""

		


                
def PLAY(url,name):#2
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()

	if '"geoblocking":"ww"' in link:
		rtmp = 'rtmp://pssimsat1fs.fplive.net/pssimsat1ls/geo_worldwide/'
		app = ' app=pssimsat1ls/geo_worldwide'

	if '"geoblocking":"de_at_ch"' in link:
		rtmp = 'rtmp://pssimsat1fs.fplive.net/pssimsat1ls/geo_d_at_ch/'
		app = ' app=pssimsat1ls/geo_d_at_ch'

	if '"geoblocking":"de"' in link:
		rtmp = 'rtmp://pssimsat1fs.fplive.net/pssimsat1ls/geo_d/'
		app = ' app=pssimsat1ls/geo_d'

	swfurl =' swfurl=http://www.sat1.de/static/videoplayer/prod/gvp_all_2012-02-06/player/loader/1.0.0-SNAPSHOT-sat1/MingLoader.swf'
        match_playpath=re.compile('"downloadFilename":"(.+?)"').findall(link)

	if 'navy-cis' in url:
		rtmp = match_playpath[0]
		playpath = ''
		app = 'pssevenone/S1'
		rtmp = rtmp.replace('\\','')
	else:
		playpath = ' playpath=mp4:'+match_playpath[0]




	url = rtmp+playpath+swfurl+' swfVfy=true'+app+' pageUrl=http://www.sat1.de'
        item = xbmcgui.ListItem(path=url)
	return xbmcplugin.setResolvedUrl(pluginhandle, True, item)

                
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


def addLinkOld(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok

def addLink(name,url,mode,iconimage):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	liz.setProperty('IsPlayable', 'true')
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
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
        VIDEOLINKS(url,name)

elif mode==2:
        print ""+url
        PLAY(url,name)


xbmcplugin.endOfDirectory(int(sys.argv[1]))
