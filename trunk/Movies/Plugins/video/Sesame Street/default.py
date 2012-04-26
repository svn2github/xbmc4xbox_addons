import urllib,urllib2,re,sys,xbmcplugin,xbmcgui,xbmcaddon
pluginhandle = int(sys.argv[1])

def CATS():
        addDir('Videos','http://www.sesamestreet.org/browseallvideos',1,'','')
        addDir('Sesame Playlists','http://www.sesamestreet.org/browseallplaylists',2,'','')
        addDir('Sesame Parents','http://www.sesamestreet.org/parents/topics',11,'','')
        addDir('Search','http://www.sesamestreet.org/',8,'','')

def VIDS(url):
        addDir('By Character','http://www.sesamestreet.org/browsevideosbycharacter',3,'','')
        addDir('By Subject','http://www.sesamestreet.org/browsevideosbysubject',3,'','')
        addDir('By Theme','http://www.sesamestreet.org/browsevideosbytheme',3,'','')
        addDir('Songs','http://www.sesamestreet.org/browseallvideos?p_p_id=browsegpv_WAR_browsegpvportlet&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-2&p_p_col_count=1&_browsegpv_WAR_browsegpvportlet_assetType=SONG',4,'','')
	addDir('Classic Clips','http://www.sesamestreet.org/browseallvideos?p_p_id=browsegpv_WAR_browsegpvportlet&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-2&p_p_col_count=1&_browsegpv_WAR_browsegpvportlet_assetType=CLASSIC',4,'','')
        addDir('Browse All','http://www.sesamestreet.org/browseallvideos',4,'','')


def PLISTS(url):
        addDir('By Character','http://www.sesamestreet.org/browseplaylistsbycharacter',9,'','')
        addDir('By Subject','http://www.sesamestreet.org/browseplaylistsbysubject',9,'','')
        addDir('By Theme','http://www.sesamestreet.org/browseplaylistsbytheme',9,'','')
        addDir('Browse All','http://www.sesamestreet.org/browseallplaylists',10,'','')

def SCRAP1(url):
	addDir('Abby Cadabby','http://www.sesamestreet.org/browseallvideos?p_p_id=browsegpv_WAR_browsegpvportlet&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-2&p_p_col_count=1&_browsegpv_WAR_browsegpvportlet_elementType=character&_browsegpv_WAR_browsegpvportlet_character=Abby+Cadabby',4,'http://t3.gstatic.com/images?q=tbn:ANd9GcTY6lshVvhKhevQmQ-f9aYANFMp7D6IvoV33r_gYQKuU48XeB7Vdw','')
	addDir('Bert','http://www.sesamestreet.org/browseallvideos?p_p_id=browsegpv_WAR_browsegpvportlet&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-2&p_p_col_count=1&_browsegpv_WAR_browsegpvportlet_elementType=character&_browsegpv_WAR_browsegpvportlet_character=Bert',4,'http://t1.gstatic.com/images?q=tbn:ANd9GcRzLcotJCIkxvi8sVwu9GBs_J_8JGMeqTCHOISvNYoUSZRC8IHt','')
	addDir('Big Bird','http://www.sesamestreet.org/browseallvideos?p_p_id=browsegpv_WAR_browsegpvportlet&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-2&p_p_col_count=1&_browsegpv_WAR_browsegpvportlet_elementType=character&_browsegpv_WAR_browsegpvportlet_character=Big+Bird',4,'http://t1.gstatic.com/images?q=tbn:ANd9GcTYFMF9T3fZq2lpoL8l7c-MLckx-DmV6JXeEB2LIL5PhDbqIxcbTg','')
	addDir('Cookie Monster','http://www.sesamestreet.org/browseallvideos?p_p_id=browsegpv_WAR_browsegpvportlet&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-2&p_p_col_count=1&_browsegpv_WAR_browsegpvportlet_elementType=character&_browsegpv_WAR_browsegpvportlet_character=Cookie+Monster',4,'http://t0.gstatic.com/images?q=tbn:ANd9GcSE0LcH4HzacYlQJ3FGkf-Ry_-gaHmERo_3jG-voLUMQ0ZlkHZBfg','')
	addDir('Count Von Count','http://www.sesamestreet.org/browseallvideos?p_p_id=browsegpv_WAR_browsegpvportlet&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-2&p_p_col_count=1&_browsegpv_WAR_browsegpvportlet_elementType=character&_browsegpv_WAR_browsegpvportlet_character=Count+Von+Count',4,'http://t1.gstatic.com/images?q=tbn:ANd9GcSz2HZmLrr9OcUmhsX0bud5L46vagSw_kquCGzl4GCDjnPxGjiUjQ','')
	addDir('Elmo','http://www.sesamestreet.org/browseallvideos?p_p_id=browsegpv_WAR_browsegpvportlet&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-2&p_p_col_count=1&_browsegpv_WAR_browsegpvportlet_elementType=character&_browsegpv_WAR_browsegpvportlet_character=Elmo',4,'http://t1.gstatic.com/images?q=tbn:ANd9GcRoT1Kv4YOgLfRiDMcSBZoIHic6GZWjg_vC0QtzYOgQysePmd-9jg','')
	addDir('Ernie','http://www.sesamestreet.org/browseallvideos?p_p_id=browsegpv_WAR_browsegpvportlet&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-2&p_p_col_count=1&_browsegpv_WAR_browsegpvportlet_elementType=character&_browsegpv_WAR_browsegpvportlet_character=Ernie',4,'http://t1.gstatic.com/images?q=tbn:ANd9GcQMLI3HKP7yXYofA381tVwXspPVikHaWY5GM1647Md9eaYGtNKI7Q','')
	addDir('Grover','http://www.sesamestreet.org/browseallvideos?p_p_id=browsegpv_WAR_browsegpvportlet&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-2&p_p_col_count=1&_browsegpv_WAR_browsegpvportlet_elementType=character&_browsegpv_WAR_browsegpvportlet_character=Grover',4,'http://t2.gstatic.com/images?q=tbn:ANd9GcTNV8I_gDBV_gqCw5a89goDenLONFjJgdEx-d0gAigbYNDunUKc','')
	addDir('Oscar','http://www.sesamestreet.org/browseallvideos?p_p_id=browsegpv_WAR_browsegpvportlet&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-2&p_p_col_count=1&_browsegpv_WAR_browsegpvportlet_elementType=character&_browsegpv_WAR_browsegpvportlet_character=Oscar',4,'http://t0.gstatic.com/images?q=tbn:ANd9GcQVMVF4TE5hnS3GXZyQAMsTS2Iau1CAogAUJgEjivXZCC5IP7RSNQ','')
	addDir('Rosita','http://www.sesamestreet.org/browseallvideos?p_p_id=browsegpv_WAR_browsegpvportlet&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-2&p_p_col_count=1&_browsegpv_WAR_browsegpvportlet_elementType=character&_browsegpv_WAR_browsegpvportlet_character=Rosita',4,'http://t0.gstatic.com/images?q=tbn:ANd9GcSgnops4tqWDtPtzfT8a1uA5Xj0Nt-d9qeNYACFWd-rG1Kgz1H1','')
	addDir('Telly Monster','http://www.sesamestreet.org/browseallvideos?p_p_id=browsegpv_WAR_browsegpvportlet&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-2&p_p_col_count=1&_browsegpv_WAR_browsegpvportlet_elementType=character&_browsegpv_WAR_browsegpvportlet_character=Telly+Monster',4,'http://t0.gstatic.com/images?q=tbn:ANd9GcR2alJTdXicA3OQ4SqRVylR6hdWO3eLpe0oGNhoFvS4s6GgeO_h','')
	addDir('Zoe','http://www.sesamestreet.org/browseallvideos?p_p_id=browsegpv_WAR_browsegpvportlet&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-2&p_p_col_count=1&_browsegpv_WAR_browsegpvportlet_elementType=character&_browsegpv_WAR_browsegpvportlet_character=Zoe',4,'http://t3.gstatic.com/images?q=tbn:ANd9GcQbetCE3OoBl0XEYsOrnlvTrLx_6iOr2PSgmLZjflyGIsYL_P4K','')

def SCRAP2(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        page = urllib2.urlopen(req)
	link=page.read()
        all=re.compile('<span>List View</span>.+?<div class="container-footer">', re.DOTALL).findall(link)
	match=re.compile('href="(.+?)" target="_self">	<img src="(.+?)" alt="" width="120" height="90" border="0" /><span class=".+?"></span>	</a>	</div></div><div class="text">.+?="title">	<a href=".+?" target="_self"><span>(.+?)</span>').findall(all[0])
        nxt=re.compile('class="button more" href="(.+?)">').findall(link)
	for url,thumb,name in match:
	        u=sys.argv[0]+"?url="+urllib.quote_plus(url,name)+"&mode="+str(5)
                item=xbmcgui.ListItem(name, thumbnailImage='http://www.sesamestreet.org/'+thumb)
          	item.setInfo( type="Video", infoLabels={ "Title": name} )                
		item.setProperty('IsPlayable', 'true')
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item)
	for url in nxt:
		addDir('More',url,4,'','')

def SCRAP3(url):
	addDir('Abby Cadabby','http://www.sesamestreet.org/browseallplaylists?p_p_id=browsegpv_WAR_browsegpvportlet&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-2&p_p_col_count=1&_browsegpv_WAR_browsegpvportlet_elementType=character&_browsegpv_WAR_browsegpvportlet_character=Abby+Cadabby',10,'http://t3.gstatic.com/images?q=tbn:ANd9GcTY6lshVvhKhevQmQ-f9aYANFMp7D6IvoV33r_gYQKuU48XeB7Vdw','')
	addDir('Bert','http://www.sesamestreet.org/browseallplaylists?p_p_id=browsegpv_WAR_browsegpvportlet&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-2&p_p_col_count=1&_browsegpv_WAR_browsegpvportlet_elementType=character&_browsegpv_WAR_browsegpvportlet_character=Bert',10,'http://t1.gstatic.com/images?q=tbn:ANd9GcRzLcotJCIkxvi8sVwu9GBs_J_8JGMeqTCHOISvNYoUSZRC8IHt','')
	addDir('Big Bird','http://www.sesamestreet.org/browseallplaylists?p_p_id=browsegpv_WAR_browsegpvportlet&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-2&p_p_col_count=1&_browsegpv_WAR_browsegpvportlet_elementType=character&_browsegpv_WAR_browsegpvportlet_character=Big+Bird',10,'http://t1.gstatic.com/images?q=tbn:ANd9GcTYFMF9T3fZq2lpoL8l7c-MLckx-DmV6JXeEB2LIL5PhDbqIxcbTg','')
	addDir('Cookie Monster','http://www.sesamestreet.org/browseallplaylists?p_p_id=browsegpv_WAR_browsegpvportlet&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-2&p_p_col_count=1&_browsegpv_WAR_browsegpvportlet_elementType=character&_browsegpv_WAR_browsegpvportlet_character=Cookie+Monster',10,'http://t0.gstatic.com/images?q=tbn:ANd9GcSE0LcH4HzacYlQJ3FGkf-Ry_-gaHmERo_3jG-voLUMQ0ZlkHZBfg','')
	addDir('Count Von Count','http://www.sesamestreet.org/browseallplaylists?p_p_id=browsegpv_WAR_browsegpvportlet&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-2&p_p_col_count=1&_browsegpv_WAR_browsegpvportlet_elementType=character&_browsegpv_WAR_browsegpvportlet_character=Count+Von+Count',10,'http://t1.gstatic.com/images?q=tbn:ANd9GcSz2HZmLrr9OcUmhsX0bud5L46vagSw_kquCGzl4GCDjnPxGjiUjQ','')
	addDir('Elmo','http://www.sesamestreet.org/browseallplaylists?p_p_id=browsegpv_WAR_browsegpvportlet&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-2&p_p_col_count=1&_browsegpv_WAR_browsegpvportlet_elementType=character&_browsegpv_WAR_browsegpvportlet_character=Elmo',10,'http://t1.gstatic.com/images?q=tbn:ANd9GcRoT1Kv4YOgLfRiDMcSBZoIHic6GZWjg_vC0QtzYOgQysePmd-9jg','')
	addDir('Ernie','http://www.sesamestreet.org/browseallplaylists?p_p_id=browsegpv_WAR_browsegpvportlet&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-2&p_p_col_count=1&_browsegpv_WAR_browsegpvportlet_elementType=character&_browsegpv_WAR_browsegpvportlet_character=Ernie',10,'http://t1.gstatic.com/images?q=tbn:ANd9GcQMLI3HKP7yXYofA381tVwXspPVikHaWY5GM1647Md9eaYGtNKI7Q','')
	addDir('Grover','http://www.sesamestreet.org/browseallplaylists?p_p_id=browsegpv_WAR_browsegpvportlet&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-2&p_p_col_count=1&_browsegpv_WAR_browsegpvportlet_elementType=character&_browsegpv_WAR_browsegpvportlet_character=Grover',10,'http://t2.gstatic.com/images?q=tbn:ANd9GcTNV8I_gDBV_gqCw5a89goDenLONFjJgdEx-d0gAigbYNDunUKc','')
	addDir('Oscar','http://www.sesamestreet.org/browseallplaylists?p_p_id=browsegpv_WAR_browsegpvportlet&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-2&p_p_col_count=1&_browsegpv_WAR_browsegpvportlet_elementType=character&_browsegpv_WAR_browsegpvportlet_character=Oscar',10,'http://t0.gstatic.com/images?q=tbn:ANd9GcQVMVF4TE5hnS3GXZyQAMsTS2Iau1CAogAUJgEjivXZCC5IP7RSNQ','')
	addDir('Rosita','http://www.sesamestreet.org/browseallplaylists?p_p_id=browsegpv_WAR_browsegpvportlet&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-2&p_p_col_count=1&_browsegpv_WAR_browsegpvportlet_elementType=character&_browsegpv_WAR_browsegpvportlet_character=Rosita',10,'http://t0.gstatic.com/images?q=tbn:ANd9GcSgnops4tqWDtPtzfT8a1uA5Xj0Nt-d9qeNYACFWd-rG1Kgz1H1','')
	addDir('Telly Monster','http://www.sesamestreet.org/browseallplaylists?p_p_id=browsegpv_WAR_browsegpvportlet&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-2&p_p_col_count=1&_browsegpv_WAR_browsegpvportlet_elementType=character&_browsegpv_WAR_browsegpvportlet_character=Telly+Monster',10,'http://t0.gstatic.com/images?q=tbn:ANd9GcR2alJTdXicA3OQ4SqRVylR6hdWO3eLpe0oGNhoFvS4s6GgeO_h','')
	addDir('Zoe','http://www.sesamestreet.org/browseallplaylists?p_p_id=browsegpv_WAR_browsegpvportlet&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-2&p_p_col_count=1&_browsegpv_WAR_browsegpvportlet_elementType=character&_browsegpv_WAR_browsegpvportlet_character=Zoe',10,'http://t3.gstatic.com/images?q=tbn:ANd9GcQbetCE3OoBl0XEYsOrnlvTrLx_6iOr2PSgmLZjflyGIsYL_P4K','')


def SCRAP4(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        page = urllib2.urlopen(req)
	link=page.read()
        all=re.compile('<span>List View</span>.+?<div class="container-footer">', re.DOTALL).findall(link)
	match=re.compile('href="(.+?)" target="_self">	<img src="(.+?)" alt="" width="120" height="90" border="0" /><span class=".+?"></span>	</a>	</div></div><div class="text">.+?="title">	<a href=".+?" target="_self"><span>(.+?)</span>').findall(all[0])
        nxt=re.compile('class="button more" href="(.+?)">').findall(link)
	for url,thumb,name in match:
	        u=sys.argv[0]+"?url="+urllib.quote_plus(url,name)+"&mode="+str(6)
                item=xbmcgui.ListItem(name, thumbnailImage='http://www.sesamestreet.org/'+thumb)
          	item.setInfo( type="Video", infoLabels={ "Title": name} )                
		item.setProperty('IsPlayable', 'true')
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item)
	for url in nxt:
		addDir('More',url,10,'','')

def SCRAP5(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        page = urllib2.urlopen(req)
	link=page.read()
        all=re.compile('"Parents Topics".+?id="kidtivities"', re.DOTALL).findall(link)
	match=re.compile('<a href="(.+?)">(.+?)</a>').findall(all[0])
	for url,name in match:
	        u=sys.argv[0]+"?url="+urllib.quote_plus('http://www.sesamestreet.org'+url,name)+"&mode="+str(12)
                item=xbmcgui.ListItem(name.replace('&amp;','&'))
          	item.setInfo( type="Video", infoLabels={ "Title": name} )                
		item.setProperty('IsPlayable', 'true')
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item)

def SEARCHURL(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        page = urllib2.urlopen(req)
	link=page.read()
        all=re.compile('<span>List View</span>.+?<div class="container-footer">', re.DOTALL).findall(link)
	match=re.compile('<a href="(.+?)" ><div class="search-title">(.+?)</div></a>').findall(link)
	nxt=re.compile('<a href="(.+?)" class="button more"><span>Next</span>').findall(link)
	for url,name in match:
	        u=sys.argv[0]+"?url="+urllib.quote_plus("http://www.sesamestreet.org"+url,name)+"&mode="+str(5)
                item=xbmcgui.ListItem(name)
          	item.setInfo( type="Video", infoLabels={ "Title": name} )                
		item.setProperty('IsPlayable', 'true')
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item)
	for url in nxt:
		addDir('More',url,7,'','')

def PLAYSINGLE(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        page = urllib2.urlopen(req)
	link=page.read()
	code=re.compile('videoQueueBrowseAll&uid=(.+?)"').findall(link)[0]
        req = urllib2.Request('http://www.sesamestreet.org/cms_services/services?action=player&type=videoQueueBrowseAll&uid='+code)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        page = urllib2.urlopen(req)
	link2=page.read()
	code2=re.compile('<filename><.+?CDATA.+?(.+?)]]></filename>').findall(link2)[0]
     	item = xbmcgui.ListItem(path=code2)
        xbmcplugin.setResolvedUrl(pluginhandle, True, item)

def PLAYLIST(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        page = urllib2.urlopen(req)
	link=page.read()
	code=re.compile('type=playlist&uid=(.+?)"').findall(link)[0]
        req = urllib2.Request('http://www.sesamestreet.org/cms_services/services?action=player&type=playlist&uid='+code)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        page = urllib2.urlopen(req)
	link2=page.read()
        stacked_url = 'stack://'
	code2=re.compile('<filename><.+?CDATA.+?rtmp(.+?)]]></filename>').findall(link2)
	for url in code2:
	        stacked_url += 'rtmp'+ url +' , '
        stacked_url2 = stacked_url[:-3]
	print stacked_url
     	item = xbmcgui.ListItem(path=stacked_url2)
        xbmcplugin.setResolvedUrl(pluginhandle, True, item)

def PLAYLISTPARENT(url):
	if url.find('grief')>0:
			req = urllib2.Request('http://www.sesameworkshop.org/cms_services/services?action=player&type=VIDEOLISTObject&groupId=10174&uid=5333601')
        		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        		page = urllib2.urlopen(req)
			link2=page.read()
        		stacked_url = 'stack://'
			code2=re.compile('<filename><.+?CDATA.+?rtmp(.+?)]]></filename>').findall(link2)
			for url in code2:
				stacked_url += 'rtmp'+ url +' , '
        		stacked_url2 = stacked_url[:-3]
     			item = xbmcgui.ListItem(path=stacked_url2)
        		xbmcplugin.setResolvedUrl(pluginhandle, True, item)
			return

        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        page = urllib2.urlopen(req)
	link=page.read()
	code=re.compile('configURL="/cms_services/services.+?action=player&type=VIDEOLISTObject&groupId=(.+?)"').findall(link)
	match=re.compile('".+?_PLAYER","(.+?)","(.+?)"').findall(link)
	for code1,code2 in match:
        		req = urllib2.Request('http://www.sesamestreet.org/cms_services/services?action=player&type=VIDEOLISTObject&groupId='+code1+'&uid='+code2)
        		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        		page = urllib2.urlopen(req)
			link2=page.read()
        		stacked_url = 'stack://'
			code2=re.compile('<filename><.+?CDATA.+?rtmp(.+?)]]></filename>').findall(link2)
			for url in code2:
	        		stacked_url += 'rtmp'+ url +' , '
        		stacked_url2 = stacked_url[:-3]
     			item = xbmcgui.ListItem(path=stacked_url2)
        		xbmcplugin.setResolvedUrl(pluginhandle, True, item)
			return
	req = urllib2.Request('http://www.sesamestreet.org/cms_services/services?action=player&type=VIDEOLISTObject&groupId='+code[0])
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        page = urllib2.urlopen(req)
	link2=page.read()
        stacked_url = 'stack://'
	code2=re.compile('<filename><.+?CDATA.+?rtmp(.+?)]]></filename>').findall(link2)
	for url in code2:
		stacked_url += 'rtmp'+ url +' , '
        stacked_url2 = stacked_url[:-3]
     	item = xbmcgui.ListItem(path=stacked_url2)
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

def SEARCH():
        keyb = xbmc.Keyboard('', 'Search Sesame')
        keyb.doModal()
        if (keyb.isConfirmed()):
                search = keyb.getText()
                encode=urllib.quote(search)
                req = urllib2.Request('http://www.sesamestreet.org/globalsearch?p_p_id=search_WAR_searchportlet&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_count=1&_search_WAR_searchportlet_javax.portlet.action=search&_search_WAR_searchportlet_keywords='+encode+'&_search_WAR_searchportlet_type=VIDEO')
	        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        	page = urllib2.urlopen(req)
		link=page.read()
		match=re.compile('<a href="(.+?)" ><div class="search-title">(.+?)</div></a>').findall(link)
		nxt=re.compile('<a href="(.+?)" class="button more"><span>Next</span>').findall(link)
		for url,name in match:
	        	u=sys.argv[0]+"?url="+urllib.quote_plus("http://www.sesamestreet.org"+url,name)+"&mode="+str(5)
                	item=xbmcgui.ListItem(name)
          		item.setInfo( type="Video", infoLabels={ "Title": name} )                
			item.setProperty('IsPlayable', 'true')
                	xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item)
		for url in nxt:
			addDir(' Next',url,7,'')

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
        VIDS(url)
elif mode==2:
        print "PAGE"
        PLISTS(url)
elif mode==3:
        print "PAGE"
        SCRAP1(url)
elif mode==4:
        print "PAGE"
        SCRAP2(url)
elif mode==9:
        print "PAGE"
        SCRAP3(url)
elif mode==10:
        print "PAGE"
        SCRAP4(url)
elif mode==11:
        print "PAGE"
        SCRAP5(url)
elif mode==5:
        print "PAGE"
        PLAYSINGLE(url)
elif mode==6:
        print "PAGE"
        PLAYLIST(url)
elif mode==12:
        print "PAGE"
        PLAYLISTPARENT(url)
elif mode==7:
        print "PAGE"
        SEARCHURL(url)
elif mode==8:
        print "SEARCH  :"+url
        SEARCH()
        
xbmcplugin.endOfDirectory(int(sys.argv[1]))