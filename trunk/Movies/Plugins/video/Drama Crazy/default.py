import urllib,urllib2,re,sys,xbmcplugin,xbmcgui
import cookielib,os,string,cookielib,StringIO
import os,time,base64,logging
import xbmcaddon
from datetime import datetime
try:
    import json
except ImportError:
    import simplejson as json
    

#Dramacrazy
dc=xbmcaddon.Addon(id='plugin.video.dramacrazy')
addonPath=dc.getAddonInfo('path')
artPath=addonPath+'/resources/art'

def HOME():
        icon = os.path.join(xbmc.translatePath( addonPath ), 'icon.png')
        
        addDir('Index','http://www.dramacrazy.net/drama-index/',2,icon)
        addDir('Genres','http://www.dramacrazy.net/drama-index/',3,icon)
        addDir('A-Z list','http://www.dramacrazy.net/drama-index/',4,icon)
        addDir('Most Popular','http://www.dramacrazy.net/most-popular/',5,icon)
        addDir('Most Recent','http://www.dramacrazy.net/most-recent/',6,icon)
        searchIcon = os.path.join(xbmc.translatePath( artPath ), 'search-icon.png')
        addDir('Search','http://www.dramacrazy.net/drama-index/',7,searchIcon)
        #addDir('What is next AJ?', 'http://www.dramacrazy.net/', 50, os.path.join(xbmc.translatePath( artPath ), "AJ.png"))


def WHAT_IS_COMING(url):
        d = xbmcgui.Dialog()
        d.ok('ANIME Crazy [RELEASED]', 'DONATE today: \n[B]http://code.google.com/p/apple-tv2-xbmc/[/B]')
        

def INDEX(url):
        url = 'http://www.dramacrazy.net/drama-index/'
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        link = ''.join(link.splitlines()).replace('\t','')

        match=re.compile('<ul class="truindexlist">(.+?)</ul>').findall(link)
        if(len(match) >= 1):
                quickLinks=re.compile('<li><a href="#(.+?)">(.+?)</a></li>').findall(match[0])
                for quickLink, quickLinkName in quickLinks:
                        match = re.compile('<h2 style="padding: 20px 10px 10px 5px;border-top: 4px solid rgb\(0, 0, 0\); background-color: rgb\(12, 148, 158\); color: rgb\(255, 255, 255\);clear:both">(.+?)<a name="'+quickLink+'"></a></h2>(.+?)(</div>|<h2)').findall(link)
                        addDir(quickLinkName,match[0][1],21,'')


def INDEX_A_Z(url):
        matches = re.compile('<ul class="truindexlist"><p class="truindexlistheader">(.+?)</p>(.+?)</ul>').findall(url)
        for char, videoList in matches:
                addDir(char,videoList,22,'')


def INDEX_A_Z_VIDEOS(url):
        videoLinks = re.compile('<li><a href="/(.+?)">(.+?)</li>').findall(url)
        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Retrieving video info and image,5000)")
        for videoLink, videoName in videoLinks:
                addVideoInfo_Image('http://www.dramacrazy.net/' + videoLink)
                        

def GENRES(url):
        url = 'http://www.dramacrazy.net/drama-index/'
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        link = ''.join(link.splitlines()).replace('\t','')
        
        match=re.compile('<strong>Genre:</strong>(.+?)</div>').findall(link)
        if(len(match) >= 1):
                genres=re.compile('<a href="/(.+?)">(.+?)</a>').findall(match[0])
                for genreLink, genreName in genres:
                        addDir(genreName,'http://www.dramacrazy.net/'+genreLink,31,'')


def GENRE_VIDEOS(url):
        Video_List_Searched(url)


def A_Z_LIST(url):
        addDir('A','http://www.dramacrazy.net/alpha-a/',41,'')
        addDir('B','http://www.dramacrazy.net/alpha-b/',41,'')
        addDir('C','http://www.dramacrazy.net/alpha-c/',41,'')
        addDir('D','http://www.dramacrazy.net/alpha-d/',41,'')
        addDir('E','http://www.dramacrazy.net/alpha-e/',41,'')
        addDir('F','http://www.dramacrazy.net/alpha-f/',41,'')
        addDir('G','http://www.dramacrazy.net/alpha-g/',41,'')
        addDir('H','http://www.dramacrazy.net/alpha-h/',41,'')
        addDir('I','http://www.dramacrazy.net/alpha-i/',41,'')
        addDir('J','http://www.dramacrazy.net/alpha-j/',41,'')
        addDir('K','http://www.dramacrazy.net/alpha-k/',41,'')
        addDir('L','http://www.dramacrazy.net/alpha-l/',41,'')
        addDir('M','http://www.dramacrazy.net/alpha-m/',41,'')
        addDir('N','http://www.dramacrazy.net/alpha-n/',41,'')
        addDir('O','http://www.dramacrazy.net/alpha-o/',41,'')
        addDir('P','http://www.dramacrazy.net/alpha-p/',41,'')
        addDir('Q','http://www.dramacrazy.net/alpha-q/',41,'')
        addDir('R','http://www.dramacrazy.net/alpha-r/',41,'')
        addDir('S','http://www.dramacrazy.net/alpha-s/',41,'')
        addDir('Q','http://www.dramacrazy.net/alpha-q/',41,'')
        addDir('U','http://www.dramacrazy.net/alpha-u/',41,'')
        addDir('V','http://www.dramacrazy.net/alpha-v/',41,'')
        addDir('W','http://www.dramacrazy.net/alpha-w/',41,'')
        addDir('X','http://www.dramacrazy.net/alpha-x/',41,'')
        addDir('Y','http://www.dramacrazy.net/alpha-y/',41,'')
        addDir('Z','http://www.dramacrazy.net/alpha-z/',41,'')
        

def A_Z_LIST_VIDEOS(url):
        Video_List_And_Pagination(url)
        

def MOST_POPULAR(url):
        Video_List_And_Pagination(url)
        

def MOST_RECENT(url):
        Video_List_And_Pagination(url)
        

def SEARCH(url):
        keyb = xbmc.Keyboard('', 'Enter search text')
        keyb.doModal()
        searchText = ''
        if (keyb.isConfirmed()):
                searchText = urllib.quote_plus(keyb.getText())
        url = 'http://www.dramacrazy.net/search/'+searchText
        Video_List_Searched(url)


def PAGES(url):
        Video_List_And_Pagination(url)
        

def Video_List_Searched(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        link = ''.join(link.splitlines()).replace('\t','')
        match=re.compile('<div class="top4">(.+?)<div class="clear"> </div></div>').findall(link)
        if(len(match) >= 1):
                videoInfo=re.compile('<a href="/(.+?)"><p>(.+?)</p><img src="(.+?)" alt="" width="150px" /></a>').findall(match[0])
                xbmc.executebuiltin("XBMC.Notification(Please Wait!,Retrieving video info and image,5000)")
                for videoLink, videoName, imgSrc in videoInfo:
                        addVideoInfo_Image('http://www.dramacrazy.net/' + videoLink)
        
        match=re.compile('<div class="moreActionResults contentModule">(.+?)</div><div class="clear"></div></div>').findall(link)
        if(len(match) >= 1):
                videoInfo=re.compile('<p class="longTitle floatLeft"><a href="/(.+?)">(.+?)</p>').findall(match[0])
                for videoLink, videoName in videoInfo:
                        addVideoInfo_Image('http://www.dramacrazy.net/' + videoLink)
                        

def Video_List_And_Pagination(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        link = ''.join(link.splitlines()).replace('\t','')

        match=re.compile('<h1><a href="/(.+?)">(.+?)</a></h1>').findall(link)
        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Retrieving video info and image,5000)")
        for videoLink, videoName in match:
                addVideoInfo_Image('http://www.dramacrazy.net/' + videoLink)
        match=re.compile('<div class="paginationDiv">(.+?)<div class="clear"></div></div>').findall(link)
        if(len(match) >= 1):
                pages=re.compile('<a href="(.+?)">(.+?)</a>').findall(match[0])
                for pageUrl, page in pages:
                        pageNbr = page.replace('&lsaquo;','<').replace('&rsaquo;','>').replace('&gt;','>').replace('&lt;','<')
                        icon = ''
                        dirName = ''
                        if(pageNbr == '<'):
                                dirName = '< PREVIOUS Page'
                                icon = os.path.join(xbmc.translatePath( artPath ), 'prev-icon.png')
                        elif(pageNbr == '>'):
                                dirName = 'NEXT Page >'
                                icon = os.path.join(xbmc.translatePath( artPath ), 'next-icon.png')
                        elif(pageNbr == '< First'):
                                dirName = '< FIRST Page'
                                icon = os.path.join(xbmc.translatePath( artPath ), 'first-icon.png')
                        elif(pageNbr == 'Last >'):
                                dirName = 'LAST Page >'
                                icon = os.path.join(xbmc.translatePath( artPath ), 'last-icon.png')
                        else:
                                dirName = 'TO Page: '+pageNbr
                        addDir(dirName,pageUrl,8,icon)


def addVideoInfo_Image(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        link = ''.join(link.splitlines()).replace('\t','')

        imgUrl=re.compile('<img src="(.+?)" width="150px" alt="(.+?)Image" />').findall(link)[0][0]
        match=re.compile('<div class="text floatLeft">(.+?)</div>').findall(link)
        videoName=re.compile('<h1>(.+?)</h1>').findall(match[0])
        ranks=re.compile('<span class="position">(.+?)</span><br /><span class="totalNr">of (.+?)</span>').findall(match[0])
        videoTitle = videoName[0] + ' (Rank: ' + ranks[0][0] + ' of ' + ranks[0][1] +')'
        videoEpisodesUrl = url[0:len(url)-1] + '-episode-list/'
        addDir(videoTitle,videoEpisodesUrl,9,imgUrl)


def EPISODES_OR_MOVIE(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        link = ''.join(link.splitlines()).replace('\t','')
        if re.search('404 Page Not Found', link):
                d = xbmcgui.Dialog()
                d.ok('NO episodes found','There are no episodes added for this drama.','Be the first to add episode, visit www.dramacrazy.net now','')
                return        
        imgUrl=re.compile('<img src="/(.+?)" width="150px" alt="(.+?)Image" />').findall(link)[0][0]
        episodes=re.compile('<a class="floatLeft" id="episode(.+?)" href="/(.+?)">(.+?)</a>  <p class="floatRight"> (.+?) </p>').findall(link)
        if(len(episodes) > 0):
                for episodeId, episodeUrl, episodeName, episodeAddedDate in episodes:
                        episodeTitle = unescape(episodeName) +' (Added on: '+episodeAddedDate+')'
                        addDir(episodeTitle,'http://www.dramacrazy.net/' + episodeUrl,10,'http://www.dramacrazy.net/' + imgUrl)
        else:
                PARTS('http://www.dramacrazy.net/' + re.compile('<a class="floatLeft" href="/(.+?)">(.+?)</a>').findall(link)[0][0])
        
                

def PARTS(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        link = ''.join(link.splitlines()).replace('\t','').replace('\'','"')

        streamingLinksModule=re.compile('<!-- Small Div alternate streaming mirros -->(.+?)<!--End of alternate streaming mirrors -->').findall(link)
        streamingLinks=re.compile('<div class="row">(.+?)<div class="clear"></div></div>').findall(streamingLinksModule[0])
        for stramingLinkRow in streamingLinks:
                parts = re.compile('<a (.+?) onclick="return encLink\("/(.+?)"\);" (.+?)>').findall(stramingLinkRow.replace(')"',');"'))
                streamingName = re.compile('Watch(.+?)\)').findall(stramingLinkRow)
                streamTypeName =  'Watch' + streamingName[0] + ')'
                if re.search('\(Wat\)', streamTypeName):
                        continue
                
                matchCount = len(parts)
                if(matchCount > 1):
                        i = 0
                        playList = ''
                        for temp1, partLink, temp2 in parts:
                                i = i + 1
                                print ' - PART: '+str(i)+' PART link = '+partLink
                                partName = streamTypeName + ' - PART: '+str(i)
                                addPlayableLink(partName,'http://www.dramacrazy.net/' + partLink,16,'')
                                playList = playList + 'http://www.dramacrazy.net/' + partLink
                                if(i < matchCount):
                                        playList = playList + ':;'
                        addPlayListLink('------------->[B]Direct PLAY[/B]<------------- [I]Playlist of above ' + str(matchCount) + ' videos[/I]',playList,12,'')

                else:
                        addPlayableLink('[B]SINGLE LINK[/B] ' + streamTypeName,'http://www.dramacrazy.net/' + parts[0][1],16,'')


def PLAYLIST_VIDEOLINKS(url,name):
        ok=True
        playList = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playList.clear()
        #time.sleep(2)
        links = url.split(':;')
        pDialog = xbmcgui.DialogProgress()
        ret = pDialog.create('Loading playlist...')
        totalLinks = len(links)
        loadedLinks = 0
        remaining_display = 'Videos loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B] into XBMC player playlist.'
        pDialog.update(0,'Please wait for the process to retrieve video link.',remaining_display)
        
        for videoLink in links:
                loadVideos(videoLink,name,True,True)
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                #print percent
                remaining_display = 'Videos loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B] into XBMC player playlist.'
                pDialog.update(percent,'Please wait for the process to retrieve video link.',remaining_display)
                if (pDialog.iscanceled()):
                        return False
                        
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(playList)
        if not xbmcPlayer.isPlayingVideo():
                d = xbmcgui.Dialog()
                d.ok('INVALID VIDEO PLAYLIST', 'The playlist videos were removed due to copyright issue.','Check other links.')
        return ok



def LOAD_AND_PLAY_VIDEO(url,name):
        xbmc.executebuiltin("XBMC.Notification(PLease Wait!, Loading video link into XBMC Media Player,5000)")
        ok=True
        print url
        videoUrl = loadVideos(url,name,True,False)
        if videoUrl == None:
                d = xbmcgui.Dialog()
                d.ok('NO VIDEO FOUND', 'This video was removed due to copyright issue.','Check other links.')
                return False
        elif videoUrl == 'ERROR':
                return False
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(videoUrl)
        return ok

def VIDEOLINKS(url,name):
        loadVideos(url,name,False,False)


def loadVideos(url,name,isRequestForURL,isRequestForPlaylist):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        link = ''.join(link.splitlines()).replace('\t','').replace('\'','"')
        streamingPlayer = re.compile('document.write\(unescape\("(.+?)"\)\);').findall(link)
        print streamingPlayer
        print url
        if(len(streamingPlayer) == 0):
        
                episodeContent = re.compile('<div class="episodeContent">(.+?)</div>').findall(link)[0]
                url = re.compile('src="(.+?)"').findall(episodeContent)[0]
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                link = ''.join(link.splitlines()).replace('\t','').replace('\'','"')
                streamingPlayer = re.compile('document.write\(unescape\("(.+?)"\)\);').findall(link)
                if(len(streamingPlayer) == 0):
                        streamingPlayer = [ urllib.quote_plus(link) ]
                
        frame =  urllib.unquote_plus(streamingPlayer[0]).replace('\'','"').replace(' =','=').replace('= ','=')
        videoUrl = re.compile('config=(.+?)&amp;').findall(frame)
        if(len(videoUrl) == 0):
                videoUrl = re.compile('data="(.+?)"').findall(frame)
        if(len(videoUrl) == 0):
                videoUrl = re.compile('file=(.+?)&amp;autostart').findall(frame)
        if(len(videoUrl) == 0):
                videoUrl = re.compile('href="(.+?)"').findall(frame)
        if(len(videoUrl) == 0):
                videoUrl = re.compile('src="(.+?)"').findall(frame)
        url =  videoUrl[0] + '&AJ;'

                
                
        print 'VIDEO LINK = '+url
        #ANIMECRAZY
        try:
                match=re.compile('http://www.animecrazy.net/(.+?)&AJ;').findall(url)[0]
                req = urllib2.Request('http://www.animecrazy.net/'+match)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=urllib.unquote(response.read())
                response.close()
                link = ''.join(link.splitlines()).replace('\'','"')
                
                url = re.compile('<iframe src ="(.+?)"').findall(link)[0] + '&AJ;'
                print 'NEW url = '+url
        except: pass
        
        #DRAMACRAZY
        try:
                match=re.compile('http://www.dramacrazy.net/(.+?)&AJ;').findall(url)[0]
                req = urllib2.Request('http://www.dramacrazy.net/'+match)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=urllib.unquote(response.read())
                response.close()
                link = ''.join(link.splitlines()).replace('\'','"')
                
                url = re.compile('<iframe src ="(.+?)"').findall(link)[0] + '&AJ;'
                print 'NEW url = '+url
        except: pass
        
        
        #Gamedorm
        try:
                match=re.compile('gamedorm.net/(.+?)&AJ;').findall(url)[0]
                req = urllib2.Request('http://gamedorm.net/'+match)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=urllib.unquote(response.read())
                response.close()
                link = ''.join(link.splitlines()).replace('\'','"')
                
                videoUrl = re.compile('"file": "(.+?)"').findall(link)[0]
                imgUrl = ''
                if(isRequestForURL):
                        if(isRequestForPlaylist):
                                liz = xbmcgui.ListItem('[B]PLAY VIDEO[/B]', thumbnailImage=imgUrl)
                                playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
                                playlist.add(url=videoUrl, listitem=liz)
                        else:
                                return videoUrl
                else:
                        addLink ('[B]PLAY VIDEO[/B]',videoUrl,imgUrl)
        except: pass
        
         #Gamedorm.org
        try:
                match=re.compile('gamedorm.org/(.+?)&AJ;').findall(url)[0]
                req = urllib2.Request('http://www.gamedorm.org/'+match)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=urllib.unquote(response.read())
                response.close()
                link = ''.join(link.splitlines()).replace('\'','"')
                
                playlist = re.compile('playlist:\[(.+?)\]').findall(link)[0]
                
                playItems = re.compile('url: "(.+?)"').findall(playlist)
                videoUrl = ''
                for playItem in playItems:
                        if not playItem.lower().endswith('jpg'):
                                videoUrl = playItem
                                break
                
                if(isRequestForURL): 
                        if(isRequestForPlaylist):
                                liz = xbmcgui.ListItem('[B]PLAY VIDEO[/B]', thumbnailImage='')
                                playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
                                playlist.add(url=videoUrl, listitem=liz)
                        else:
                                return videoUrl
                else:
                        addLink ('[B]PLAY VIDEO[/B]',videoUrl,'')
        except: pass
        
        #Play File
        try:
                videoUrl = re.compile('play\?file\=(.+?)&AJ;').findall(url)[0]
                if(isRequestForURL): 
                        if(isRequestForPlaylist):
                                liz = xbmcgui.ListItem('[B]PLAY VIDEO[/B]', thumbnailImage='')
                                playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
                                playlist.add(url=videoUrl, listitem=liz)
                        else:
                                return videoUrl
                else:
                        addLink ('[B]PLAY VIDEO[/B]',videoUrl,'')
        except: pass
        
        #MP4
        try:
                match=re.compile('http://(.+?).mp4&AJ;').findall(url)
                videoUrl = 'http://'+match[0]+'.mp4'
                imgUrl = ''
                if(isRequestForURL):
                        if(isRequestForPlaylist):
                                liz = xbmcgui.ListItem(name, thumbnailImage=imgUrl)
                                playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
                                playlist.add(url=videoUrl, listitem=liz)
                        else:
                                return videoUrl
                else:
                        addLink ('[B]PLAY VIDEO[/B]: '+name,videoUrl,imgUrl)
                
        except: pass
        
        #YOUTUBE
        try:
                
                match=re.compile('http://www.youtube.com/watch\?v=(.+?)&AJ;').findall(url)
                if(len(match) == 0):
                        match=re.compile('http://www.youtube.com/v/(.+?)&fs=1&AJ;').findall(url)
                code = match[0]
                linkImage = 'http://i.ytimg.com/vi/'+code+'/default.jpg'
                req = urllib2.Request('http://www.youtube.com/watch?v='+code+'&fmt=18')
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                
                if len(re.compile('shortlink" href="http://youtu.be/(.+?)"').findall(link)) == 0:
                        if len(re.compile('\'VIDEO_ID\': "(.+?)"').findall(link)) == 0:
                                req = urllib2.Request('http://www.youtube.com/get_video_info?video_id='+code+'&asv=3&el=detailpage&hl=en_US')
                                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                                response = urllib2.urlopen(req)
                                link=response.read()
                                response.close()
                map = None
                match=re.compile('fmt_stream_map=(.+?)&').findall(link)
                if len(match) == 0:
                        map=(re.compile('fmt_stream_map": "(.+?)"').findall(link)[0]).replace('\\/', '/')
                else:
                        map=urllib.unquote(match[0]).decode('utf8').split('url=')
                if re.search('status=fail', link):
                        return
                if map == None:
                        return
                #print map
                highResoVid = ''
                youtubeVideoQual = dc.getSetting('videoQual')
                for attr in map:
                        if attr == '':
                                continue
                        parts = attr.split('&qual')
                        url = urllib.unquote(parts[0]).decode('utf8')
                        print url
                        qual = re.compile('&itag=(.+?)&').findall(url)[0]
                        print qual
                        if(qual == '13'):
                                if(not(isRequestForURL)):
                                        addLink ('PLAY 3GP Low Quality - 176x144',url,linkImage)
                                elif(highResoVid == ''):
                                        highResoVid = url
                        if(qual == '17'):
                                if(not(isRequestForURL)):
                                        addLink ('PLAY 3GP Medium Quality - 176x144',url,linkImage)
                                elif(highResoVid == ''):
                                        highResoVid = url
                        if(qual == '36'):
                                if(not(isRequestForURL)):
                                        addLink ('PLAY 3GP High Quality - 320x240',url,linkImage)
                                elif(highResoVid == ''):
                                        highResoVid = url
                        if(qual == '5'):
                                if(not(isRequestForURL)):
                                        addLink ('PLAY FLV Low Quality - 400\\327226',url,linkImage)
                                elif(highResoVid == ''):
                                        highResoVid = url
                        if(qual == '34'):
                                if(not(isRequestForURL)):
                                        addLink ('PLAY FLV Medium Quality - 480x360',url,linkImage)
                                elif(highResoVid == ''):
                                        highResoVid = url
                        if(qual == '6'):
                                if(not(isRequestForURL)):
                                        addLink ('PLAY FLV Medium Quality - 640\\327360',url,linkImage)
                                elif(highResoVid == ''):
                                        highResoVid = url
                        if(qual == '35'):
                                if(not(isRequestForURL)):
                                        addLink ('PLAY FLV High Quality - 854\\327480',url,linkImage)
                                else:
                                        highResoVid = url
                        if(qual == '18'):
                                if(not(isRequestForURL)):
                                        addLink ('PLAY MP4 High Quality - 480x360',url,linkImage)
                                else:
                                        highResoVid = url
                                        
                        if(qual == '22'):
                                if(not(isRequestForURL)):
                                        addLink ('PLAY MP4 High Quality - 1280x720',url,linkImage)
                                else:
                                        highResoVid = url
                                        if youtubeVideoQual == '1' or youtubeVideoQual == '2':
                                                break
                        if(qual == '37'):
                                if(not(isRequestForURL)):
                                        addLink ('PLAY MP4 High-2 Quality - 1920x1080',url,linkImage)
                                else:
                                        highResoVid = url
                                        if youtubeVideoQual == '2':
                                                break
                        if(qual == '38'):
                                if(not(isRequestForURL)):
                                        addLink ('PLAY MP4 Epic Quality - 4096\\3272304',url,linkImage)
                                else:
                                        highResoVid = url
                                        if youtubeVideoQual == '2':
                                                break
                        if(qual == '43'):
                                if(not(isRequestForURL)):
                                        addLink ('PLAY WEBM Medium Quality - 4096\\3272304',url,linkImage)
                                else:
                                        highResoVid = url
                        if(qual == '44'):
                                if(not(isRequestForURL)):
                                        addLink ('PLAY WEBM High Quality - 4096\\3272304',url,linkImage)
                                else:
                                        highResoVid = url
                                        if youtubeVideoQual == '1' or youtubeVideoQual == '2':
                                                break
                        if(qual == '45'):
                                if(not(isRequestForURL)):
                                        addLink ('PLAY WEBM High-2 Quality - 4096\\3272304',url,linkImage)
                                else:
                                        highResoVid = url
                                        if youtubeVideoQual == '2':
                                                break
                print highResoVid
                if(isRequestForURL):
                        if(isRequestForPlaylist):
                                liz = xbmcgui.ListItem('VIDEO PART', thumbnailImage=linkImage)
                                xbmc.PlayList(xbmc.PLAYLIST_VIDEO).add(url = highResoVid, listitem=liz)
                                return highResoVid
                        else:
                                return highResoVid

        except: pass
        
        #GOOGLE VIDEO
        try:
                id=re.compile('docId=(.+?)&AJ;').findall(url)
                req = urllib2.Request('http://video.google.com/docinfo?%7B"docid":"' + id[0] + '"%7D')
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                print link
                link = ''.join(link.splitlines()).replace('\t','').replace('\'','"')
        
                videoTitle=re.compile('"Title":"(.+?)",').findall(link)[0]
                
                imgUrl=re.compile('"thumbnail_url":"(.+?)"').findall(link)[0].replace('\\u0026','&')
                videoUrl=re.compile('"streamer_url":"(.+?)"').findall(link)[0].replace('\\u0026','&')
                
                if(isRequestForURL): 
                        if(isRequestForPlaylist):
                                liz = xbmcgui.ListItem(videoTitle, thumbnailImage=imgUrl)
                                playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
                                playlist.add(url=videoUrl, listitem=liz)
                        else:
                                return videoUrl
                else:
                        addLink ('[B]PLAY VIDEO[/B]: '+videoTitle,videoUrl,imgUrl)
                
        except: pass
        
        
        #SATSUKAI
        try:
                match=re.compile('http://www.satsukai.com/(.+?)&AJ;').findall(url)[0]
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=urllib.unquote(response.read())
                response.close()
                link = ''.join(link.splitlines()).replace('\t','').replace('\'','"')
                imgUrl=re.compile('so.addVariable\("image","(.+?)"\);').findall(link)[0]
                videoUrl=re.compile('so.addVariable\("file","(.+?)"\);').findall(link)[0]
                videoTitle = name
                if(isRequestForURL): 
                        if(isRequestForPlaylist):
                                liz = xbmcgui.ListItem(videoTitle, thumbnailImage=imgUrl)
                                playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
                                playlist.add(url=videoUrl, listitem=liz)
                        else:
                                return videoUrl
                else:
                        addLink ('[B]PLAY VIDEO[/B]: '+videoTitle,videoUrl,imgUrl)
                
        except: pass
        
        
        #DRAMACRAZY
        try:
                match=re.compile('http://www.dramacrazy.net/(.+?)&AJ;').findall(url)[0]
                req = urllib2.Request('http://www.dramacrazy.net/'+match)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=urllib.unquote(response.read())
                response.close()
                link = ''.join(link.splitlines()).replace('\'','"')
                
                match = re.compile('<iframe src ="(.+?)"').findall(link)
                if len(match) > 0:
                        frameUrl = match[0]
                        req = urllib2.Request(frameUrl)
                        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                        response = urllib2.urlopen(req)
                        link=urllib.unquote(response.read())
                        response.close()
                        link = ''.join(link.splitlines()).replace('\'','"')
                match = re.compile('"file": "(.+?)",').findall(link)
                if len(match) == 0:
                        match = re.compile('<file>(.+?)</file>').findall(link)
                videoUrl = match[0]
                imgUrl = ''
                videoTitle = name
                if(isRequestForURL): 
                        if(isRequestForPlaylist):
                                liz = xbmcgui.ListItem(videoTitle, thumbnailImage=imgUrl)
                                playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
                                playlist.add(url=videoUrl, listitem=liz)
                        else:
                                return videoUrl
                else:
                        addLink ('[B]PLAY VIDEO[/B]: '+videoTitle,videoUrl,imgUrl)
                
        except: pass
        
        #DAILYMOTION
        try:
                match=re.compile('http://www.dailymotion.com/swf/(.+?)&AJ;').findall(url)
                if(len(match) == 0):
                        match=re.compile('http://www.dailymotion.com/video/(.+?)&AJ;').findall(url)
                link = 'http://www.dailymotion.com/video/'+str(match[0])
                req = urllib2.Request(link)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                sequence=re.compile('"sequence",  "(.+?)"').findall(link)
                newseqeunce = urllib.unquote(sequence[0]).decode('utf8').replace('\\/','/')
                imgSrc=re.compile('og:image" content="(.+?)"').findall(link)
                if(len(imgSrc) == 0):
                	imgSrc=re.compile('/jpeg" href="(.+?)"').findall(link)
                dm_low=re.compile('"sdURL":"(.+?)"').findall(newseqeunce)
                dm_high=re.compile('"hqURL":"(.+?)"').findall(newseqeunce)
                if(isRequestForURL):
                        videoUrl = ''
                        if(len(dm_high) == 0):
                                videoUrl = dm_low[0]
                        else:
                                videoUrl = dm_high[0]
                        if(isRequestForPlaylist):
                                liz = xbmcgui.ListItem('EPISODE', thumbnailImage=imgSrc[0])
                                playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
                                playlist.add(url=videoUrl, listitem=liz)
                        else:
                                return videoUrl
                else:
                        if(len(dm_low) > 0):
                                addLink ('PLAY Standard Quality ',dm_low[0],imgSrc[0])
                        if(len(dm_high) > 0):
                                addLink ('PLAY High Quality ',dm_high[0],imgSrc[0])
        except: pass
        
        
        #YAHOO
        try:
                id=re.compile('http://d.yimg.com/static.video.yahoo.com/yep/YV_YEP.swf\?id=(.+?)&AJ;').findall(url)
                req = urllib2.Request('http://cosmos.bcst.yahoo.com/up/yep/process/getPlaylistFOP.php?node_id='+id[0])
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                link = ''.join(link.splitlines()).replace('\t','').replace('\'','"')
        
                server=re.compile('<STREAM APP="(.+?)"').findall(link)
                urlPath=re.compile('FULLPATH="(.+?)"').findall(link)
                videoUrl=(server[0]+urlPath[0]).replace('&amp;','&')
                imgInfo = re.compile('<THUMB TYPE="FULLSIZETHUMB"><\!\[CDATA\[(.+?)\]\]></THUMB>').findall(link)
                imgUrl = ''
                if(len(imgInfo) > 0):
                        imgUrl = imgInfo[0]
                videoTitle = name
                if(isRequestForURL): 
                        if(isRequestForPlaylist):
                                liz = xbmcgui.ListItem(videoTitle, thumbnailImage=imgUrl)
                                playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
                                playlist.add(url=videoUrl, listitem=liz)
                        else:
                                return videoUrl
                else:
                        addLink ('[B]PLAY VIDEO[/B]: '+videoTitle,videoUrl,imgUrl)
        except: pass


        #MEGAVIDEO
        try:
                if not re.search('megavideo.com', url):
                        raise
                id=re.compile('http://www.megavideo.com/v/(.+?)&').findall(url)
                if len(id) > 0:
                        url = get_redirected_url('http://www.megavideo.com/v/'+id[0], None) + '&AJ;'
                id=re.compile('v=(.+?)&').findall(url)
                video_id = id[0].replace('p://www.megavideo.com/?d=','')
                print 'MEGAVIDEO ID = ' + video_id
                req = urllib2.Request('http://www.megavideo.com/xml/videolink.php?v=' + video_id)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                link = ''.join(link.splitlines()).replace('\t','').replace('\'','"')
                print link
                un=re.compile(' un="(.+?)"').findall(link)
                k1=re.compile(' k1="(.+?)"').findall(link)
                k2=re.compile(' k2="(.+?)"').findall(link)
                hashresult = decrypt(un[0], k1[0], k2[0])
                
                s=re.compile(' s="(.+?)"').findall(link)
                
                title=re.compile(' title="(.+?)"').findall(link)
                videoTitle = urllib.unquote_plus(title[0].replace('+',' '))
                
                imgUrl = ''
                videoUrl = "http://www" + s[0] + ".megavideo.com/files/" + hashresult + "/" + videoTitle + ".flv";
                print 'MEGA VIDEO url = '+videoUrl
                if(isRequestForURL): 
                        if(isRequestForPlaylist):
                                liz = xbmcgui.ListItem(videoTitle, thumbnailImage=imgUrl)
                                playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
                                playlist.add(url=videoUrl, listitem=liz)
                        else:
                                return videoUrl
                else:
                        addLink ('[B]PLAY VIDEO[/B]: '+videoTitle,videoUrl,imgUrl)
        except: pass

        
        #VEOH
        try:
                if not re.search('veoh.com', url):
                        raise
                id=re.compile('permalinkId=v(.+?)&').findall(url)
                if len(id) == 0:
                        id=re.compile('http://www.veoh.com/v(.+?)&').findall(url)
                
                url='http://www.veoh.com/rest/v2/execute.xml?method=veoh.video.findByPermalink&permalink=v'+id[0]+'&apiKey=E97FCECD-875D-D5EB-035C-8EF241F184E2'
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                domObj = parseString(link)
                print domObj.toprettyxml()
                if len(domObj.getElementsByTagName("error")) > 0:
                        print domObj.getElementsByTagName("error")[0].getAttribute('errorMessage')
                        return
                videoUrl = get_redirected_url(domObj.getElementsByTagName("video")[0].getAttribute('ipodUrl'), None)
                imgUrl = domObj.getElementsByTagName("video")[0].getAttribute('fullHighResImagePath')
                videoTitle = name
                if(isRequestForURL):
                        if(isRequestForPlaylist):
                                liz = xbmcgui.ListItem(videoTitle, thumbnailImage=imgUrl)
                                playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
                                playlist.add(url=videoUrl, listitem=liz)
                        else:
                                return videoUrl
                else:
                        addLink ('[B]PLAY VIDEO[/B]: '+videoTitle,videoUrl,imgUrl)
        except: pass
        
        
        
        #TUDOU
        try:
                id=re.compile('http://www.tudou.com/(.+?)&AJ;').findall(url)
                quotedUrl = urllib.quote('http://www.tudou.com/'+id[0])
                url = 'http://clipnabber.com/?url='+quotedUrl
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                link = ''.join(link.splitlines()).replace('\t','').replace('\'','"')
        
                match=re.compile('<div id="Math">(.+?)</div>').findall(link)
        
                url = 'http://clipnabber.com/gethint.php?url='+quotedUrl+'&sid='+match[0]
        
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                link = ''.join(link.splitlines()).replace('\t','').replace('\'','"')
                videoUrl=unescape(re.compile('<a href="(.+?)">').findall(link)[0])
                imgUrl = ''
                print 'TUDOU url = '+videoUrl
                videoTitle = name
                if(isRequestForURL): 
                        if(isRequestForPlaylist):
                                liz = xbmcgui.ListItem(videoTitle, thumbnailImage=imgUrl)
                                playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
                                playlist.add(url=videoUrl, listitem=liz)
                        else:
                                return videoUrl
                else:
                        addLink ('[B]PLAY VIDEO[/B]: '+videoTitle,videoUrl,imgUrl)
        except: pass
        
        
        #TFCNOW
        try:
                p=re.compile('http://playlist.tfcnow.net/(.+?)&AJ;')
                match=p.findall(url)
                link = match[0]
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                link = ''.join(link.splitlines()).replace('\'','"')
                match=re.compile('src="(.+?)"').findall(link)
                loadVideos (match[0],name,False,False)
        except: pass


        #FACEBOOK
        try:
                match=re.compile('http://www.facebook.com/v/(.+?)&AJ;').findall(url)
                url='http://facebook.com/video/external_video.php?v='+match[0]
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=urllib.unquote(response.read())
                response.close()
                link = ''.join(link.splitlines()).replace('\\/','/')
                videoTitle=re.compile('"video_title":"(.+?)"').findall(link)[0]
                imgUrl=re.compile('"thumb_url":"(.+?)"').findall(link)[0]
                videoUrl=re.compile('"video_src":"(.+?)"').findall(link)[0]
                if(isRequestForURL): 
                        if(isRequestForPlaylist):
                                liz = xbmcgui.ListItem(videoTitle, thumbnailImage=imgUrl)
                                playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
                                playlist.add(url=videoUrl, listitem=liz)
                        else:
                                return videoUrl
                else:
                        addLink ('[B]PLAY VIDEO[/B]: '+videoTitle,videoUrl,imgUrl)
                
        except: pass
        
        #MOVSHARE
        try:
                p=re.compile('http://www.movshare.net/video/(.+?)&AJ;')
                match=p.findall(url)
                movUrl = 'http://www.movshare.net/video/'+match[0]
                req = urllib2.Request(movUrl)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                link = ''.join(link.splitlines()).replace('\t','').replace('\'','"')
                if re.search('Video hosting is expensive. We need you to prove you"re human.',link):
                        values = {'wm': '1'}
                        headers = { 'User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3' }
                        data = urllib.urlencode(values)
                        req = urllib2.Request(movUrl, data, headers)
                        response = urllib2.urlopen(req)
                        link=response.read()
                        response.close()
                        link = ''.join(link.splitlines()).replace('\t','').replace('\'','"')
                
                match=re.compile('<param name="src" value="(.+?)" />').findall(link)
                if(len(match) == 0):
                        match=re.compile('flashvars.file="(.+?)"')
                imgUrl = ''
                videoUrl=match[0]
                videoTitle = name
                if(isRequestForURL):
                        if(isRequestForPlaylist):
                                liz = xbmcgui.ListItem(videoTitle, thumbnailImage=imgUrl)
                                playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
                                playlist.add(url=videoUrl, listitem=liz)
                        else:
                                return videoUrl
                else:
                        addLink ('[B]PLAY VIDEO[/B]: '+videoTitle,videoUrl,imgUrl)
        except: pass
        
        
        #VIDEOWEED
        try:
                p=re.compile('http://(.+?).videoweed(.+?)&AJ;')
                match=p.findall(url)
                link = match[0]
                req = urllib2.Request(url.replace('&AJ;',''))
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                imgUrl = ''
                file=re.compile('.file="(.+?)"').findall(link)[0]
                filekey=re.compile('.filekey="(.+?)"').findall(link)[0]
                newUrl = "http://www.videoweed.es/api/player.api.php?user=undefined&codes=undefined&pass=undefined&file=" + file + "&key=" + filekey
                req = urllib2.Request(newUrl)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                videoUrl = re.compile('url=(.+?)&').findall(link)[0]
                videoTitle = name
                if(isRequestForURL):
                        if(isRequestForPlaylist):
                                liz = xbmcgui.ListItem(videoTitle, thumbnailImage=imgUrl)
                                playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
                                playlist.add(url=videoUrl, listitem=liz)
                        else:
                                return videoUrl
                else:
                        addLink ('[B]PLAY VIDEO[/B]: '+videoTitle,videoUrl,imgUrl)
        except: pass
        
        
        #LOOMBO
        try:
                p=re.compile('http://loombo.com/(.+?)&AJ;')
                match=p.findall(url)
                link = match[0]
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                link = ''.join(link.splitlines()).replace('\'','"')
                match=re.compile('s1.addVariable\("file","(.+?)"\);').findall(link)
                imgUrl = ''
                videoUrl=match[0]
                videoTitle = name
                if(isRequestForURL):
                        if(isRequestForPlaylist):
                                liz = xbmcgui.ListItem(videoTitle, thumbnailImage=imgUrl)
                                playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
                                playlist.add(url=videoUrl, listitem=liz)
                        else:
                                return videoUrl
                else:
                        addLink ('[B]PLAY VIDEO[/B]: '+videoTitle,videoUrl,imgUrl)
        except: pass
        
        
        #VIDEO BAM MP4
        try:
                p=re.compile('http://videobam.com/(.+?)&AJ;')
                match=p.findall(url)
                link = match[0]
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                link = ''.join(link.splitlines()).replace('\'','"')
                match=re.compile('<source src="(.+?)"').findall(link)
                imgUrl = ''
                videoUrl=match[0]
                videoTitle = name
                if(isRequestForURL):
                        if(isRequestForPlaylist):
                                liz = xbmcgui.ListItem(videoTitle, thumbnailImage=imgUrl)
                                playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
                                playlist.add(url=videoUrl, listitem=liz)
                        else:
                                return videoUrl
                else:
                        addLink ('[B]PLAY VIDEO[/B]: '+videoTitle,videoUrl,imgUrl)
        except: pass
        
        
        #VIDBUX
        try:
                p=re.compile('http://www.vidbux.com/(.+?)&AJ;')
                match=p.findall(url)
                link = match[0]
                xbmc.executebuiltin("XBMC.Notification(SKIPPING...,Low Quality links are skipped,5000)")
                if(isRequestForURL and not isRequestForPlaylist):
                        return 'ERROR'
        except: pass
        
        
        #VIDEOBB
        try:
                p=re.compile('videobb.com/e/(.+?)&AJ;')
                match=p.findall(url)
                url='http://www.videobb.com/player_control/settings.php?v='+match[0]
                settingsObj = json.load(urllib.urlopen(url))['settings']
                imgUrl = str(settingsObj['config']['thumbnail'])
                videoUrl = str(base64.b64decode(settingsObj['config']['token1']))
                videoTitle = name
                if(isRequestForURL):
                        if(isRequestForPlaylist):
                                liz = xbmcgui.ListItem(videoTitle, thumbnailImage=imgUrl)
                                playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
                                playlist.add(url=videoUrl, listitem=liz)
                        else:
                                return videoUrl
                else:
                        addLink ('[B]PLAY VIDEO[/B]: '+videoTitle,videoUrl,imgUrl)
        except: pass
        
        
        #Z-SHARE
        try:
                id=re.compile('http://www.zshare.net/(.+?)&AJ;').findall(url)[0]
                url = 'http://www.zshare.net/'+id.replace(' ','%20')
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                videoUrl = re.compile('file: "(.+?)"').findall(link)[0]
                videoUrl = videoUrl.replace(' ','%20')+'|User-Agent='+urllib.quote_plus('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_1) AppleWebKit/534.48.3 (KHTML, like Gecko) Version/5.1 Safari/534.48.3'+'&Accept='+urllib.quote_plus('text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')+'&Accept_Encoding='+urllib.quote_plus('gzip, deflate'))
                
                if(isRequestForURL):
                        if(isRequestForPlaylist):
                                liz = xbmcgui.ListItem('EPISODE', thumbnailImage='')
                                xbmc.PlayList(xbmc.PLAYLIST_VIDEO).add(url = link, listitem=liz)
                        else:
                                return videoUrl
                else:
                        addLink ('PLAY High Quality Video',link,'')
        except: pass




####################################################################################################################
# MegaVideo Routine
####################################################################################################################
        
#Python Video Decryption and resolving routines.
#Courtesy of Voinage, Coolblaze.
#Megavideo - Coolblaze # Part 1 put this below VIDEOLINKS function.

def ajoin(arr):
        strtest = ''
        for num in range(len(arr)):
                strtest = strtest + str(arr[num])
        return strtest

def asplit(mystring):
        arr = []
        for num in range(len(mystring)):
                arr.append(mystring[num])
        return arr
                
def decrypt(str1, key1, key2):

        __reg1 = []
        __reg3 = 0
        while (__reg3 < len(str1)):
                __reg0 = str1[__reg3]
                holder = __reg0
                if (holder == "0"):
                        __reg1.append("0000")
                else:
                        if (__reg0 == "1"):
                                __reg1.append("0001")
                        else:
                                if (__reg0 == "2"): 
                                        __reg1.append("0010")
                                else: 
                                        if (__reg0 == "3"):
                                                __reg1.append("0011")
                                        else: 
                                                if (__reg0 == "4"):
                                                        __reg1.append("0100")
                                                else: 
                                                        if (__reg0 == "5"):
                                                                __reg1.append("0101")
                                                        else: 
                                                                if (__reg0 == "6"):
                                                                        __reg1.append("0110")
                                                                else: 
                                                                        if (__reg0 == "7"):
                                                                                __reg1.append("0111")
                                                                        else: 
                                                                                if (__reg0 == "8"):
                                                                                        __reg1.append("1000")
                                                                                else: 
                                                                                        if (__reg0 == "9"):
                                                                                                __reg1.append("1001")
                                                                                        else: 
                                                                                                if (__reg0 == "a"):
                                                                                                        __reg1.append("1010")
                                                                                                else: 
                                                                                                        if (__reg0 == "b"):
                                                                                                                __reg1.append("1011")
                                                                                                        else: 
                                                                                                                if (__reg0 == "c"):
                                                                                                                        __reg1.append("1100")
                                                                                                                else: 
                                                                                                                        if (__reg0 == "d"):
                                                                                                                                __reg1.append("1101")
                                                                                                                        else: 
                                                                                                                                if (__reg0 == "e"):
                                                                                                                                        __reg1.append("1110")
                                                                                                                                else: 
                                                                                                                                        if (__reg0 == "f"):
                                                                                                                                                __reg1.append("1111")

                __reg3 = __reg3 + 1

        mtstr = ajoin(__reg1)
        __reg1 = asplit(mtstr)
        __reg6 = []
        __reg3 = 0
        while (__reg3 < 384):
        
                key1 = (int(key1) * 11 + 77213) % 81371
                key2 = (int(key2) * 17 + 92717) % 192811
                __reg6.append((int(key1) + int(key2)) % 128)
                __reg3 = __reg3 + 1
        
        __reg3 = 256
        while (__reg3 >= 0):

                __reg5 = __reg6[__reg3]
                __reg4 = __reg3 % 128
                __reg8 = __reg1[__reg5]
                __reg1[__reg5] = __reg1[__reg4]
                __reg1[__reg4] = __reg8
                __reg3 = __reg3 - 1
        
        __reg3 = 0
        while (__reg3 < 128):
        
                __reg1[__reg3] = int(__reg1[__reg3]) ^ int(__reg6[__reg3 + 256]) & 1
                __reg3 = __reg3 + 1

        __reg12 = ajoin(__reg1)
        __reg7 = []
        __reg3 = 0
        while (__reg3 < len(__reg12)):

                __reg9 = __reg12[__reg3:__reg3 + 4]
                __reg7.append(__reg9)
                __reg3 = __reg3 + 4
                
        
        __reg2 = []
        __reg3 = 0
        while (__reg3 < len(__reg7)):
                __reg0 = __reg7[__reg3]
                holder2 = __reg0
        
                if (holder2 == "0000"):
                        __reg2.append("0")
                else: 
                        if (__reg0 == "0001"):
                                __reg2.append("1")
                        else: 
                                if (__reg0 == "0010"):
                                        __reg2.append("2")
                                else: 
                                        if (__reg0 == "0011"):
                                                __reg2.append("3")
                                        else: 
                                                if (__reg0 == "0100"):
                                                        __reg2.append("4")
                                                else: 
                                                        if (__reg0 == "0101"): 
                                                                __reg2.append("5")
                                                        else: 
                                                                if (__reg0 == "0110"): 
                                                                        __reg2.append("6")
                                                                else: 
                                                                        if (__reg0 == "0111"): 
                                                                                __reg2.append("7")
                                                                        else: 
                                                                                if (__reg0 == "1000"): 
                                                                                        __reg2.append("8")
                                                                                else: 
                                                                                        if (__reg0 == "1001"): 
                                                                                                __reg2.append("9")
                                                                                        else: 
                                                                                                if (__reg0 == "1010"): 
                                                                                                        __reg2.append("a")
                                                                                                else: 
                                                                                                        if (__reg0 == "1011"): 
                                                                                                                __reg2.append("b")
                                                                                                        else: 
                                                                                                                if (__reg0 == "1100"): 
                                                                                                                        __reg2.append("c")
                                                                                                                else: 
                                                                                                                        if (__reg0 == "1101"): 
                                                                                                                                __reg2.append("d")
                                                                                                                        else: 
                                                                                                                                if (__reg0 == "1110"): 
                                                                                                                                        __reg2.append("e")
                                                                                                                                else: 
                                                                                                                                        if (__reg0 == "1111"): 
                                                                                                                                                __reg2.append("f")
                                                                                                                                        
                __reg3 = __reg3 + 1

        endstr = ajoin(__reg2)
        return endstr


def DOWNLOAD_VIDEO(url,name):
        if re.search('AJLBDAJ', name):
                name.replace('AJLBDAJ', '')
                url = loadVideos(url,name,True,False)
                if url == None:
                        d = xbmcgui.Dialog()
                        d.ok('NO VIDEO FOUND', 'This video was removed due to copyright issue.','Check other links.')
                        return False
        download_video_file(url,name, False, False)

def DOWNLOAD_QUIETLY(url,name):
        if re.search('AJLBDAJ', name):
                name.replace('AJLBDAJ', '')
                url = loadVideos(url,name,True,False)
                if url == None:
                        d = xbmcgui.Dialog()
                        d.ok('NO VIDEO FOUND', 'This video was removed due to copyright issue.','Check other links.')
                        return False
        download_video_file(url,name, True, False)

        
def DOWNLOAD_AND_PLAY_VIDEO(url,name):
        if re.search('AJLBDAJ', name):
                name.replace('AJLBDAJ', '')
                url = loadVideos(url,name,True,False)
                if url == None:
                        d = xbmcgui.Dialog()
                        d.ok('NO VIDEO FOUND', 'This video was removed due to copyright issue.','Check other links.')
                        return False
        download_video_file(url,name, False, True)
                                
                                
def download_video_file(url,name, isDownloadQuietly = False, playVideo = False):

        downloadFolder = dc.getSetting('download_folder')

        print 'MYPATH: '+downloadFolder
        if downloadFolder is '':
                d = xbmcgui.Dialog()
                d.ok('Download Error','You have not set the download folder.\n Please set the addon settings and try again.','','')
                dc.openSettings(sys.argv[ 0 ])
        else:
                if not os.path.exists(downloadFolder):
                        print 'Download Folder Doesnt exist. Trying to create it.'
                        os.makedirs(downloadFolder)
                extn = '.flv'
                last = url.rfind(extn)
                if last == -1:
                        extn = '.avi'
                        last = url.rfind(extn)
                        if last == -1:
                                extn = '.mp4'
                                last = url.rfind(extn)
                                if last == -1:
                                        extn = '.flv'
                if last != -1:
                        first = url.rfind('/')
                        newName = url[(first+1):last]
                        if(newName != ''):
                                name = newName
                
                askFilename=dc.getSetting('ask_filename')
                if askFilename == 'true':
                        keyb = xbmc.Keyboard('', 'Enter filename')
                        keyb.doModal()
                        if (keyb.isConfirmed()):
                                filenameInput = urllib.quote_plus(keyb.getText())
                                if filenameInput != '':
                                        name = filenameInput
                                else:
                                        name = name[0:25] + ' ' + datetime.utcnow().strftime("%Y-%m-%d %H%M")
                        else:
                                name = name[0:25] + ' ' + datetime.utcnow().strftime("%Y-%m-%d %H%M")
                else:
                        name = name[0:25] + ' ' + datetime.utcnow().strftime("%Y-%m-%d %H%M")
                name = name.replace('\\','-')
                mypath=os.path.join(downloadFolder,name + extn)
                if os.path.isfile(mypath) is True:
                        d = xbmcgui.Dialog()
                        d.ok('Download Error','The video you are trying to download already exists!','','')
                else:              
                        print 'About to download file using url = '+url
                        try:
                                if isDownloadQuietly == False:
                                        downloadSuccess = Download(url, mypath, name)
                                        if downloadSuccess == True and playVideo == True:
                                                xbmcPlayer = xbmc.Player()
                                                xbmcPlayer.play(mypath)
                                                return True
                                else:
                                        Download_Quietly(url, mypath, name)
                        except:
                                print 'download failed'
                                raise



class StopDownloading(Exception): 
        def __init__(self, value): 
                self.value = value 
        def __str__(self): 
                return repr(self.value)
            

def Download(url, dest, displayname=False):
        #get settings
        ok = True
        if displayname == False:
                displayname=url
        deleteIncomplete=dc.getSetting('del_incomplete_dwnld')
        dp = xbmcgui.DialogProgress()
        dp.create('Downloading', '', displayname)
        print 'downloading will start now and will be saved at = '+dest
        start_time = time.time() 
        try: 
                urllib.urlretrieve(url, dest, lambda nb, bs, fs: dwnld_percent_hook(nb, bs, fs, dp, start_time, displayname))
        except:
                if deleteIncomplete == 'true':
                #delete partially downloaded file if setting says to.
                        while os.path.exists(dest): 
                                try: 
                                        os.remove(dest) 
                                        break 
                                except: 
                                        pass 
        #only handle StopDownloading (from cancel), ContentTooShort (from urlretrieve), and OS (from the race condition); let other exceptions bubble 
                if sys.exc_info()[0] in (urllib.ContentTooShortError, StopDownloading, OSError): 
                        ok=False
        return ok



def dwnld_percent_hook(numblocks, blocksize, filesize, dp, start_time, filename):
        try: 
                percent = min(numblocks * blocksize * 100 / filesize, 100) 
                currently_downloaded = float(numblocks) * blocksize / (1024 * 1024) 
                kbps_speed = numblocks * blocksize / (time.time() - start_time) 
                if kbps_speed > 0: 
                        eta = (filesize - numblocks * blocksize) / kbps_speed 
                else: 
                        eta = 0 
                kbps_speed = kbps_speed / 1024 
                total = float(filesize) / (1024 * 1024) 
                mbs = '%.02f MB of %.02f MB' % (currently_downloaded, total) 
                e = 'Speed: %.02f Kb/s ' % kbps_speed 
                e += 'ETA: %02d:%02d' % divmod(eta, 60)
                file = 'File: '+filename
                dp.update(percent, file, mbs, e)
        except: 
                percent = 100 
                dp.update(percent) 
        if dp.iscanceled(): 
                dp.close() 
                raise StopDownloading('Stopped Downloading')

def Download_Quietly(url, dest, displayname=False):
        #get settings
        ok = True
        deleteIncomplete=dc.getSetting('del_incomplete_dwnld')
        if displayname == False:
                displayname=url
        print 'downloading QUIELTY will start now and will be saved at = '+dest
        start_time = time.time() 
        try:
                xbmc.executebuiltin("XBMC.Notification(Download started!,"+displayname+",5000)")
                urllib.urlretrieve(url, dest, lambda nb, bs, fs: dwnld_percent_notify(nb, bs, fs, start_time, displayname))
        except:
                if deleteIncomplete == 'true':
                #delete partially downloaded file if setting says to.
                        while os.path.exists(dest): 
                                try: 
                                        os.remove(dest) 
                                        break 
                                except: 
                                        pass 
        #only handle StopDownloading (from cancel), ContentTooShort (from urlretrieve), and OS (from the race condition); let other exceptions bubble 
                xbmc.executebuiltin("XBMC.Notification(Download failed!,"+displayname+",5000)")
                if sys.exc_info()[0] in (urllib.ContentTooShortError, StopDownloading, OSError): 
                        ok=False 
                else: 
                        raise
        if(ok == True):
                xbmc.executebuiltin("XBMC.Notification(Download completed!,"+displayname+",5000)")
        return ok


def dwnld_percent_notify(numblocks, blocksize, filesize, start_time, filename):
        try: 
                percent = min(numblocks * blocksize * 100 / filesize, 100) 
                currently_downloaded = float(numblocks) * blocksize / (1024 * 1024) 
                kbps_speed = numblocks * blocksize / (time.time() - start_time) 
                if kbps_speed > 0: 
                        eta = (filesize - numblocks * blocksize) / kbps_speed 
                else: 
                        eta = 0 
                kbps_speed = kbps_speed / 1024 
                total = float(filesize) / (1024 * 1024) 
                mbs = '%.02f MB of %.02f MB' % (currently_downloaded, total) 
                e = 'Speed: %.02f Kb/s ' % kbps_speed 
                e += 'ETA: %02d:%02d' % divmod(eta, 60)
                file = 'File: '+filename
                #xbmc.executebuiltin("XBMC.Notification(Downloading "+percent+"%,"+displayname+",2000)")
        except: 
                percent = 100
         


def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        # adding context menus
        contextMenuItems = []
        contextMenuItems.append(('Download', 'XBMC.RunPlugin(%s?mode=13&name=%s&url=%s)' % (sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(url))))
        contextMenuItems.append(('Download and Play', 'XBMC.RunPlugin(%s?mode=15&name=%s&url=%s)' % (sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(url))))
        contextMenuItems.append(('Download Quietly', 'XBMC.RunPlugin(%s?mode=14&name=%s&url=%s)' % (sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(url))))
        contextMenuItems.append(('Download with jDownloader', 'XBMC.RunPlugin(plugin://plugin.program.jdownloader/?action=addlink&url=%s)' % (urllib.quote_plus(url))))
        
        liz.addContextMenuItems(contextMenuItems, replaceItems=True)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok


def addPlayableLink(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        # adding context menus
        #new name LOAD BEFORE DOWNLOAD AJ
        loadName = name + 'AJLBDAJ'
        contextMenuItems = []
        contextMenuItems.append(('Download', 'XBMC.RunPlugin(%s?mode=13&name=%s&url=%s)' % (sys.argv[0], urllib.quote_plus(loadName), urllib.quote_plus(url))))
        contextMenuItems.append(('Download and Play', 'XBMC.RunPlugin(%s?mode=15&name=%s&url=%s)' % (sys.argv[0], urllib.quote_plus(loadName), urllib.quote_plus(url))))
        contextMenuItems.append(('Download Quietly', 'XBMC.RunPlugin(%s?mode=14&name=%s&url=%s)' % (sys.argv[0], urllib.quote_plus(loadName), urllib.quote_plus(url))))
        
        liz.addContextMenuItems(contextMenuItems, replaceItems=True)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok

def addPlayListLink(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok
        

def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def get_redirected_url(url, data):
        opener = urllib2.build_opener(urllib2.HTTPRedirectHandler)
        if data == None:
                return opener.open(url).url
        else:
                return opener.open(url,data).url

def unescape(url):
        htmlCodes = [
                ['&', '&amp;'],
                ['<', '&lt;'],
                ['>', '&gt;'],
                ['"', '&quot;'],
                [' ', '&nbsp;']
        ]
        for code in htmlCodes:
                url = url.replace(code[1], code[0])
        return url

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

                

if mode==None or url==None or len(url)<1:
        HOME()
       
elif mode==2:
        INDEX(url)
        
elif mode==21:
        INDEX_A_Z(url)
        
elif mode==22:
        INDEX_A_Z_VIDEOS(url)

elif mode==3:
        GENRES(url)

elif mode==31:
        GENRE_VIDEOS(url)

elif mode==4:
        A_Z_LIST(url)

elif mode==41:
        A_Z_LIST_VIDEOS(url)

elif mode==5:
        MOST_POPULAR(url) 

elif mode==6:
        MOST_RECENT(url) 
        
elif mode==7:
        SEARCH(url) 
        
elif mode==8:
        PAGES(url)
        
elif mode==9:
        EPISODES_OR_MOVIE(url)

elif mode==10:
        PARTS(url)

elif mode==11:
        VIDEOLINKS(url,name)
        
elif mode==12:
        PLAYLIST_VIDEOLINKS(url,name)
        
elif mode==13:
        DOWNLOAD_VIDEO(url,name)
        
elif mode==14:
        DOWNLOAD_QUIETLY(url,name)
        
elif mode==15:
        DOWNLOAD_AND_PLAY_VIDEO(url,name)
        
elif mode==16:
        LOAD_AND_PLAY_VIDEO(url,name)
        
elif mode==50:
        WHAT_IS_COMING(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
