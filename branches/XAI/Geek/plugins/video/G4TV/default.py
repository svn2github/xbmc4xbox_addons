
__scriptname__ = "G4TV"
__author__ = 'stacked [http://xbmc.org/forum/member.php?u=26908]'
__svn_url__ = "https://xbmc-addons.googlecode.com/svn/trunk/plugins/video/G4TV"
__date__ = '06-14-2010'
__version__ = "2.3"

import xbmc, xbmcgui, xbmcplugin, urllib2, urllib, re, string, sys, os, traceback
from urllib2 import Request, urlopen, URLError, HTTPError
HEADER = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.10) Gecko/2009042316 Firefox/3.0.10'
HEADER2 = 'NonWapUserAgent=1; __utma=1; __utmb=1; __utmc=1; __utmz=1; s_cc=1; s_lv=1; s_lv_s=; s_nr=1; photo=1; s_photo_viewer=no-photo; contribution=1; s_contributor=no-contributions; s_sq=1; _csoot=1; s_vi=1; _csuid=1; p=1'
THUMBNAIL_PATH = os.path.join(os.getcwd().replace( ";", "" ),'resources','media')

def _check_for_update():
	print "G4TV v"+__version__
	url = 'http://code.google.com/p/xbmc-addons/source/browse/trunk/plugins/video/G4TV/default.py'
	req = urllib2.Request(url)
	req.add_header('User-Agent', HEADER)
	f=urllib2.urlopen(req)
	a=f.read()
	f.close()
	ALL = re.compile('<td class="source">__version__ = &quot;(.+?)&quot;<br></td>').findall(a)
	for link in ALL :
		if link.find(__version__) != 0:
			newVersion=link
			dia = xbmcgui.Dialog()
			ok = dia.ok("G4TV", xbmc.getLocalizedString( 30720 )+'\n\n'+xbmc.getLocalizedString( 30721 )+' '+__version__+'\n'+xbmc.getLocalizedString( 30722 )+' '+newVersion)

def main():
	li3=xbmcgui.ListItem("1. Most Recent",iconImage="DefaultVideo.png", thumbnailImage=os.path.join(THUMBNAIL_PATH, 'tv_icon.png'))
	u3=sys.argv[0]+"?mode=2&name="+urllib.quote_plus('Most Recent')+"&url="+urllib.quote_plus('http://g4tv.com/videos/?sort=mostrecent&q=null&ajax=true')+"&cat="+urllib.quote_plus('Most Recent')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u3,li3,True)
	li3=xbmcgui.ListItem("2. Shows",iconImage="DefaultVideo.png", thumbnailImage=os.path.join(THUMBNAIL_PATH, 'tv_icon.png'))
	u3=sys.argv[0]+"?mode=1&type="+urllib.quote_plus('showName')+"&name="+urllib.quote_plus('Shows')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u3,li3,True)
	li3=xbmcgui.ListItem("3. Content Types",iconImage="DefaultVideo.png", thumbnailImage=os.path.join(THUMBNAIL_PATH, 'tv_icon.png'))
	u3=sys.argv[0]+"?mode=1&type="+urllib.quote_plus('subType')+"&name="+urllib.quote_plus('Content Types')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u3,li3,True)
	li3=xbmcgui.ListItem("4. Events",iconImage="DefaultVideo.png", thumbnailImage=os.path.join(THUMBNAIL_PATH, 'tv_icon.png'))
	u3=sys.argv[0]+"?mode=1&type="+urllib.quote_plus('eventName')+"&name="+urllib.quote_plus('Events')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u3,li3,True)
	li3=xbmcgui.ListItem("5. Platforms",iconImage="DefaultVideo.png", thumbnailImage=os.path.join(THUMBNAIL_PATH, 'tv_icon.png'))
	u3=sys.argv[0]+"?mode=1&type="+urllib.quote_plus('platform')+"&name="+urllib.quote_plus('Platforms')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u3,li3,True)
	li3=xbmcgui.ListItem("6. Genres",iconImage="DefaultVideo.png", thumbnailImage=os.path.join(THUMBNAIL_PATH, 'tv_icon.png'))
	u3=sys.argv[0]+"?mode=1&type="+urllib.quote_plus('genre')+"&name="+urllib.quote_plus('Genres')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u3,li3,True)
	li3=xbmcgui.ListItem("7. Search",iconImage="DefaultVideo.png", thumbnailImage=os.path.join(THUMBNAIL_PATH, 'search_icon.png'))
	u3=sys.argv[0]+"?mode=7&name="+urllib.quote_plus('Search')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u3,li3,True)
	li3=xbmcgui.ListItem("8. Podcasts",iconImage="DefaultVideo.png", thumbnailImage=os.path.join(THUMBNAIL_PATH, 'rss_icon.png'))
	u3=sys.argv[0]+"?mode=4&name="+urllib.quote_plus('Podcasts')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u3,li3,True)

def get_shows_list(name,type):
	cat_name=name
	url='http://g4tv.com/videos/index.html'
	try:
		req=urllib2.Request(url)
		req.add_header('User-Agent', HEADER)
		req.add_header('Cookie', HEADER2)
		response=urllib2.urlopen(req)
	except URLError, e:
		dialog = xbmcgui.Dialog()
		ok = dialog.ok('G4TV', 'HTTP Error: '+str(e.code))
		xbmc.executebuiltin( "Container.Refresh" )
		#return
	data=response.read()
	response.close()
	menu=re.compile('<div id="search_media_filters" class="search_facets_wrap">(.+?)var G4Search',re.DOTALL).findall(data)
	shows=re.compile('<a href="#" rel="search-'+type+'_(.+?)">(.+?)</a><span class="count">(.+?)</span></li>').findall(menu[0])
	item_count=0
	for trash, title, count in shows:
		name = str(int(item_count+1))+'. '+title+' '+ count
		showName=title.replace(' ','+')
		url='http://g4tv.com/videos/?sort=mostrecent&q=null&ajax=true&'+type+'='+showName
		item=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage="DefaultFolder.png")
		item.setInfo( type="Video", infoLabels={ "Title": title+' '+count } )
		u=sys.argv[0]+"?mode=2&name="+urllib.quote_plus(cat_name+' / '+title)+"&url="+urllib.quote_plus(url)+"&cat="+urllib.quote_plus(cat_name+' / '+title)
		xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,isFolder=True)
		item_count=item_count+1
		
def runKeyboard():
	searchStr = ''
	keyboard = xbmc.Keyboard(searchStr, "Search")
	keyboard.doModal()
	if (keyboard.isConfirmed() == False):
		return
	searchstring = keyboard.getText()
	newStr = searchstring.replace(' ','%20')
	if len(newStr) == 0:
		return
	url = 'http://g4tv.com/videos/?sort=mostrecent&q='+newStr+'&ajax=true'
	newStr = searchstring.replace('%20',' ')
	name='Search: '+newStr
	get_shows_data(name,url,name)

def get_shows_data(name,url,cat):
	cat_name=cat
	nexturl=url
	try:
		req=urllib2.Request(url+'&page='+str(page))
		req.add_header('User-Agent', HEADER)
		req.add_header('Cookie', HEADER2)
		response=urllib2.urlopen(req)
	except URLError, e:
		dialog = xbmcgui.Dialog()
		ok = dialog.ok('G4TV', 'HTTP Error: '+str(e.code))
		xbmc.executebuiltin( "Container.Refresh" )
		#return
	data=response.read()
	response.close()
	url_title=re.compile('<h4><a href="(.+?)" title="(.*?)">(.+?)</a></h4>').findall(data)
	desc=re.compile('<p class="desc">\r\n\t\t\t\t\r\n\t\t\t\t\r\n(.*?)\r\n\t\t\t\t\r\n\t\t\t\t</p>',re.DOTALL).findall(data)
	thumb=re.compile('<img src="(.+?)" alt').findall(data)
	video_info=re.compile('Posted: <span title="(.+?)">').findall(data)
	item_count=0
	for url, trash, title in url_title:
		if len(video_info) != len(url_title):
			date = ' '
		else:
			date = video_info[item_count]
		name = str(int(item_count+1)+(15*(page-1)))+'. '+clean(title)+': '+clean(desc[item_count])+' ('+date+')'
		item=xbmcgui.ListItem(name, iconImage=thumb[item_count], thumbnailImage=thumb[item_count])
		item.setInfo( type="Video", infoLabels={ "Title": name, "Plot": clean(desc[item_count])+' (Posted: '+date+')' } )
		u=sys.argv[0]+"?mode=3&name="+urllib.quote_plus(clean(title))+"&url="+urllib.quote_plus(url)+"&cat="+urllib.quote_plus(cat_name)
		xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,isFolder=False)
		item_count=item_count+1
	if len(url_title) >= 15:
		item=xbmcgui.ListItem("Next Page",iconImage="DefaultVideo.png", thumbnailImage=os.path.join(THUMBNAIL_PATH, 'next.png'))
		u=sys.argv[0]+"?mode=2&name="+urllib.quote_plus(cat)+"&url="+urllib.quote_plus(nexturl)+"&page="+str(int(page)+1)+"&cat="+urllib.quote_plus(cat)
		xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,isFolder=True)

def get_video(name,url,cat):
	videokey=re.compile('videos/(.+?)/(.+?)/').findall(url)
	url='http://g4tv.com/xml/broadbandplayerservice.asmx/GetEmbeddedVideo?videoKey='+videokey[0][0]+'&playLargeVideo=true&excludedVideoKeys=&playlistType=normal&maxPlaylistSize=0'
	try:
		req=urllib2.Request(url)
		req.add_header('User-Agent', HEADER)
		req.add_header('Cookie', HEADER2)
		response=urllib2.urlopen(req)
	except URLError, e:
		dialog = xbmcgui.Dialog()
		ok = dialog.ok('G4TV', 'HTTP Error: '+str(e.code))
		#xbmc.executebuiltin( "Container.Refresh" )
		return
	data=response.read()
	response.close()
	file=re.compile('&amp;r=(.+?)</FilePath>').findall(data)
	thumb=re.compile('<ThumbnailImage>(.+?)</ThumbnailImage>').findall(data)
	url=file[0].replace('%3a', ':')
	url=url.replace('%2f', '/')
	play_video(name,url,cat)

def RSSList():
	url='http://g4tv.com/podcasts/index.html'
	try:
		req=urllib2.Request(url)
		req.add_header('User-Agent', HEADER)
		response=urllib2.urlopen(req)
	except URLError, e:
		dialog = xbmcgui.Dialog()
		ok = dialog.ok('G4TV', 'HTTP Error: '+str(e.code))
		xbmc.executebuiltin( "Container.Refresh" )
		#return
	data=response.read()
	response.close()
	p=re.compile('href="(.+?)"><img title="RSS"')
	o=re.compile('style="background:url(.+?) no-repeat;;')
	q=re.compile('<span>(.+?)</span><br />')
	URLS=p.findall(data)
	thumbs=o.findall(data)
	names=q.findall(data)
	x=0
	for url in URLS:
		thumb=thumbs[x]
		thumb=thumb.replace('(','')
		thumb=thumb.replace('landing.gif)','RSS.jpg')
		thumb=thumb.replace('landing.jpg)','RSS.jpg')
		name = names[x]
		name = name.replace('’', '\'')
		li=xbmcgui.ListItem(name, iconImage=thumb, thumbnailImage=thumb)
		li.setInfo( type="Video", infoLabels={ "Title": name } )
		u=sys.argv[0]+"?mode=5&name="+urllib.quote_plus('Podcasts / '+name)+"&url="+urllib.quote_plus(url)
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
		x=x+1

def getRSSLink(name,url):
	cat_name=name
	try:
		req=urllib2.Request(url)
		req.add_header('User-Agent', HEADER)
		response=urllib2.urlopen(req)
	except URLError, e:
		dialog = xbmcgui.Dialog()
		ok = dialog.ok('G4TV', 'HTTP Error: '+str(e.code))
		#xbmc.executebuiltin( "Container.Refresh" )
		return
	data=response.read()
	response.close()
	p=re.compile('<item>(.+?)<title>(.+?)</title>', re.DOTALL)
	o=re.compile('<link>http://www.podtrac.com/pts/redirect.mp4(.+?)</link>')
	match=p.findall(data)
	URLS=o.findall(data)
	x=0
	for add in URLS:
		names = clean(match[x][1])
		name = str(int(x+1))+'. '+names
		url='http://www.podtrac.com/pts/redirect.mp4'+add
		li=xbmcgui.ListItem(name,iconImage="DefaultVideo.png", thumbnailImage=os.path.join(THUMBNAIL_PATH, 'rss_icon.png'))
		li.setInfo( type="Video", infoLabels={ "Title": name } )
		icon="DefaultVideo.png"
		u=sys.argv[0]+"?mode=6&name="+urllib.quote_plus(names)+"&url="+urllib.quote_plus(url)+"&thumb="+urllib.quote_plus(icon)+"&cat="+urllib.quote_plus(cat_name)
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)
		x=x+1

def clean(name):
    remove=[('&amp;','&'),('&quot;','\"')]
    for old, new in remove:
        name=name.replace(old,new)
    return name
	
def clean_file(name):
    remove=[(':',' - '),('\"',''),('|',''),('>',''),('<',''),('?',''),('*','')]
    for old, new in remove:
        name=name.replace(old,new)
    return name

def play_video(name,url,cat):
	title=name
	name=clean_file(name)
	name=name[:+32]
	def Download(url,dest):
		dp = xbmcgui.DialogProgress()
		dp.create('Downloading',title,'Filename: '+name+'.flv')
		urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp))
	def _pbhook(numblocks, blocksize, filesize, url=None,dp=None):
		try:
				percent = min((numblocks*blocksize*100)/filesize, 100)
				dp.update(percent)
		except:
				percent = 100
				dp.update(percent)
		if dp.iscanceled():
				dp.close()
	flv_file = None
	stream = 'false'
	if (xbmcplugin.getSetting('download') == 'true'):
			dialog = xbmcgui.Dialog()
			flv_file = dialog.browse(3, 'Choose Download Directory', 'video', '', False, False, '')
			Download(url,flv_file+name+'.flv')
	elif (xbmcplugin.getSetting('download') == 'false' and xbmcplugin.getSetting('download_ask') == 'true'):
		dia = xbmcgui.Dialog()
		ret = dia.select(xbmc.getLocalizedString( 30005 ), [xbmc.getLocalizedString( 30001 ), xbmc.getLocalizedString( 30007 ), xbmc.getLocalizedString( 30006 )])
		if (ret == 0):
			dialog = xbmcgui.Dialog()
			flv_file = dialog.browse(3, 'Choose Download Directory', 'video', '', False, False, '')
			Download(url,flv_file+name+'.flv')
		elif (ret == 1):
			stream = 'true'
		else:
			pass
	elif (xbmcplugin.getSetting('download') == 'false' and xbmcplugin.getSetting('download_ask') == 'false'):
		stream = 'true'
	if xbmcplugin.getSetting("dvdplayer") == "true":
		player_type = xbmc.PLAYER_CORE_DVDPLAYER
	else:
		player_type = xbmc.PLAYER_CORE_MPLAYER
	g_thumbnail = xbmc.getInfoImage( "ListItem.Thumb" )
	listitem=xbmcgui.ListItem(title ,iconImage="DefaultVideo.png", thumbnailImage=g_thumbnail)
	listitem.setInfo( type="Video", infoLabels={ "Title": title, "Director": "G4TV", "Studio": "G4TV", "Genre": cat } )
	if (flv_file != None and os.path.isfile(flv_file+name+'.flv')):
		xbmc.Player(player_type).play(flv_file+name+'.flv', listitem)
	elif (stream == 'true'):
		xbmc.Player(player_type).play(str(url), listitem)
	xbmc.sleep(200)

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

params=get_params()
mode=None
name=None
url=None
page=1
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
		type=urllib.unquote_plus(params["type"])
except:
        pass
try:
		cat=urllib.unquote_plus(params["cat"])
except:
        pass

if mode==None:
	name = ''
	_check_for_update()
	main()
elif mode==1:
	get_shows_list(name,type)
elif mode==2:
	get_shows_data(name,url,cat)
elif mode==3:
	get_video(name,url,cat)
elif mode==4:
	RSSList()
elif mode==5:
	getRSSLink(name,url)
elif mode==6:
	play_video(name,url,cat)
elif mode==7:
	runKeyboard()

xbmcplugin.setPluginCategory(int(sys.argv[1]), name )
xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
xbmcplugin.endOfDirectory(int(sys.argv[1]))
	
