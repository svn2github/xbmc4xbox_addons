import urllib,urllib2,re,xbmcplugin,xbmcgui
import xbmc
import urlresolver
import xbmcaddon
import os
pluginhandle = int(sys.argv[1])

rootDir = os.getcwd()
if rootDir[-1] == ';':rootDir = rootDir[0:-1]
imageDir = os.path.join(rootDir, 'thumbnails') + '/'
fanart=imageDir+"fanart.jpg"


def CATEGORIES():
        addDir('Search','url',2,imageDir+"Search.jpg")
        addDir('New Releases','http://movie25.com/movies/new-releases/index-1.html',1,imageDir+"new releases.jpg")
        addDir('Latest Added','http://movie25.com/movies/latest-added/index-1.html',1,imageDir+"Latest added.jpg")
        addDir('Featured Movies','http://movie25.com/movies/featured-movies/index-1.html',1,imageDir+"Featured Movies.jpg")
        addDir('DVD Releases','http://movie25.com/movies/dvd-releases/index-1.html',1,imageDir+"DVD Releases.jpg")
        addDir('Most Viewed','http://movie25.com/movies/most-viewed/index-1.html',1,imageDir+"Most Viewed.jpg")
        addDir('Most Voted','http://movie25.com/movies/most-voted/index-1.html',1,imageDir+"Most Voted.jpg") 
        addDir('Genres','http://movie25.com/genres.html',3,imageDir+"Genres.jpg")
        addDir('A-Z','http://movie25.com',6,imageDir+"A-Z.jpg")		
        addDir('0-9','http://movie25.com/movies/0-9/index-1.html',7,imageDir+"0-9.jpg")
		
def Index(url):
        newurl=url
        content = getUrl(url)
        match=re.compile('<div class="movie_pic"><a href="(.*?)" ><img src="(.*?)" width=".*?" height=".*?" /></a></div>\n  <div class="movie_about">\n    <div class="movie_about_text">\n      <h1><a href=".*?" >(.*?)</a>').findall(content)
        for url,thumbnail,name in match:
          addDir(name,url,4,thumbnail)
        content = getUrl(newurl)				
        curent=re.compile('selected.*?value="(.*?)..?Page').findall(content)
        for nexturl in curent:
          newurl=str(newurl) 
          deln=re.sub("\D", "", newurl) #sucht only digits
          print deln
          deln1=deln[2:] #nimmt die ersten beiden digits also 25 von movie25.com weg
          print deln1  #es bleibt eintig die Zahl des indexes
          finish=deln1+'.html' #add .html to deln1
          print finish
          next1=newurl.replace(finish, '').replace('index-', '')
          print next1
          next_page=next1+nexturl
          print next_page		  
          addDir('Next',next_page,1,imageDir+"Next.jpg")   
       

def MovieSearch(url):
    search_entered =search()
    name=str(search_entered).replace('+','')
    req=urllib2.Request('http://movie25.com/search.php?key=' + search_entered + '&submit=')
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('<div class="movie_pic"><a href="(.*?)" target="_blank">\n.*? <img src="(.*?)" width=".*?" height=".*?" />\n.*?</a></div>\n.*?<div class=".*?">\n.*?<div class=".*?">\n.*?<h1><a href=".*?" target=".*?">\n(.*?)</a>').findall(link)
    for url,thumbnail,name in match:
        name=name.replace(' ', '')
        url='http://movie25.com/'+url
        addDir(name,url,4,thumbnail)
         		
def Genre(url):
        content = getUrl(url)
        match=re.compile('<li><a href="/movies/(.*?)">(.*?)</a></li>').findall(content)
        for url,name in match:
          url = 'http://movie25.com'+ '/movies/'+url      		
          print url
          print name
          addDir(name,url,1,'')		
		
def search():
        search_entered = ''
        keyboard = xbmc.Keyboard(search_entered, 'Search Movies on Movies25.com')
        keyboard.doModal()
        if keyboard.isConfirmed():
            search_entered = keyboard.getText() .replace(' ','+')  # sometimes you need to replace spaces with + or %20
            if search_entered == None:
                return False          
        return search_entered
         

def ABC(url):
        content = getUrl(url)
        Letter=re.compile('(http://movie25.com/movies/[a-z]").*?([A-Z])').findall(content)
        for url,name in Letter:
          url=url.replace('"', '')
          url=url+'/'
          print url
          print name
          addDir(name,url,1,imageDir+"A-Z.jpg")
		  	  
		  	  
def Index2(url):
        newurl=url
        content = getUrl(url)
        match=re.compile('<div class="movie_pic"><a href="(.*?)" ><img src="(.*?)" width=".*?" height=".*?" /></a></div>\n  <div class="movie_about">\n    <div class="movie_about_text">\n      <h1><a href=".*?" >(.*?)</a>').findall(content)
        for url,thumbnail,name in match:
          addDir(name,url,4,thumbnail)
        content = getUrl(newurl)				
        curent=re.compile('selected.*?value="(.*?)..?Page').findall(content)
        for nexturl in curent:
          newurl=str(newurl) 
          deln=re.sub("\D", "", newurl) #sucht only digits
          print deln
          deln1=deln[4:] #nimmt die ersten beiden digits also 25 von movie25.com weg
          print deln1  #es bleibt eintig die Zahl des indexes
          finish=deln1+'.html' #add .html to deln1
          print finish
          next1=newurl.replace(finish, '').replace('index-', '')
          print next1
          next_page=next1+nexturl
          print next_page		  
          addDir('Next',next_page,7,imageDir+"Next.jpg")  

def VIDEOLINKS(url,name):
        content = getUrl(url)
        match=re.compile('<li class=link_name>(.*?)</li><li class=".*?"><span><a href=(.*?) target="_blank">Full Movie</a></span><font id=".*?"></font></li>').findall(content)
        for name,url in match:
          addDir(name,url,5,"")
        
		  


def playVid(url):
        content = getUrl(url)
        match1=re.compile('"Javascript.*\http\://www.(.*).\"').findall(content)
        for url in match1:
          url = 'http://www.' + url
          url = url[:-5]
          url = url
          hostUrl = url
          videoLink = urlresolver.resolve(hostUrl)
          addLink(name,url,'')
          xbmc.Player().play(videoLink)         
		
            
def getUrl(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:16.0) Gecko/20100101 Firefox/16.0')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        return link

			
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
        liz.setProperty('IsPlayable','true')
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok


def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image', fanart)
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
        Index(url)
        
elif mode==2:
        print ""+url
        MovieSearch(url)

elif mode==3:
        print ""+url
        Genre(url)
       
elif mode==4:
        print ""+url
        VIDEOLINKS(url,name)

elif mode==5:
        print ""+url
        playVid(url)

elif mode==6:
        print ""+url
        ABC(url)

		
elif mode==7:
        print ""+url
        Index2(url)
		


xbmcplugin.endOfDirectory(int(sys.argv[1]))
