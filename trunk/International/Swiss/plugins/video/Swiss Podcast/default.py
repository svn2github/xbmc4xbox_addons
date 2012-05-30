#!/usr/bin/python
# -*- coding: utf-8 -*-
#########################################################
# SCRIPT  : default.py                                  #
#########################################################
# AUTHOR  : The project is a fork form the              # 
#           podcasts-xbmc-plugin programmed by          # 
#           afishe2000@gmail.com                        #
#           I only added a few lines of code  ....      #
#           The real work did afishe2000@gmail.com      #
#                                                       #
#           Hans Weber                                  #
#                                                       #
# EMAIL   : linuxluemmel.ch@gmail.com                   #
# XBMC    : Version 10.0 or higher                      #
# PYTHON  : internal xbmc python 2.4.X                  #
# OS      : all OS that xbmc is running                 #
# TASKS   : - plays several podcasts from switzerland   #
#           - Schweizer Fernsehen                       #
#           - Schweizer Radio                           #
# VERSION : 0.1.3                                       #
# DATE    : 09-18-10                                    #
# STATE   : Alpha 3                                     #
# LICENCE : GPL 3.0                                     #
#########################################################



####################### IMPORTS #########################

import xbmc, xbmcgui,xbmcplugin,xbmcaddon
import os, sys, thread, stat, time, string, re
import urllib, urlparse, urllib2, xml.dom.minidom

#########################################################

def syslog(msg):
    xbmc.output("[%s]: [pluginlog] %s\n" % ("swiss-podcasts",str(msg))) 
    return (0)

def addPodcasts():

      # switzerland puplic television station SF 

     addFeed('SF Aeschbacher','http://feeds.sf.tv/podcast/aeschbacher')
     addFeed('SF al dente','http://feeds.sf.tv/podcast/aldente')
     addFeed('SF Arena','http://feeds.sf.tv/podcast/arena') 
     addFeed('SF Auf und davon','http://feeds.sf.tv/podcast/aufunddavon')    
     addFeed('SF Box Office','http://feeds.sf.tv/podcast/boxoffice') 
     addFeed('SF Club','http://feeds.sf.tv/podcast/club')
     addFeed('SF Gesundheitsfee','http://feeds.sf.tv/podcast/diegesundheitsfee')
     addFeed('SF DOK','http://feeds.sf.tv/podcast/dok') 
     addFeed('SF ECO','http://feeds.sf.tv/podcast/eco') 
     addFeed('SF Edelmais','http://feeds.sf.tv/podcast/edelmais') 
     addFeed('SF Einstein','http://feeds.sf.tv/podcast/einstein')
     addFeed('SF Fortsetzung folgt','http://feeds.sf.tv/podcast/fortsetzungfolgt')
     addFeed('SF Giacobbo / Müller','http://feeds.sf.tv/podcast/giacobbomueller')
     addFeed('SF Glanz & Gloaria','http://feeds.sf.tv/podcast/glanzundgloria')
     addFeed('SF Kairo Kapstadt','http://feeds.sf.tv/podcast/kairokapstadt')  
     addFeed('SF Kassensturz','http://feeds.sf.tv/podcast/kassensturz') 
     addFeed('SF Kulturplatz','http://feeds.sf.tv/podcast/kulturplatz') 
     addFeed('SF Leichter Leben','http://feeds.sf.tv/podcast/leichterleben')
     addFeed('SF Literaturclub','http://feeds.sf.tv/podcast/literaturclub')
     addFeed('SF Mitenand','http://feeds.sf.tv/podcast/mitenand')
     addFeed('SF Puls','http://feeds.sf.tv/podcast/puls')
     addFeed('SF Reporter','http://feeds.sf.tv/podcast/reporter')  
     addFeed('SF Rundschau','http://feeds.sf.tv/podcast/rundschau')
     addFeed('SF Börse','http://feeds.sf.tv/podcast/boerse')
     addFeed('SF Bi de Lüt','http://feeds.sf.tv/podcast/sfbideluet') 
     addFeed('SF Bi de Lüt Live','http://feeds.sf.tv/podcast/sfbideluetlive')
     addFeed('SF Unterwegs','http://feeds.sf.tv/podcast/sfunterwegs')
     addFeed('SF Sommerlacher','http://feeds.sf.tv/podcast/sommerlacher')   
     addFeed('SF Sternstunde Kunst','http://feeds.sf.tv/podcast/sternstundekunst')    
     addFeed('SF Sternstunde Philosophie','http://feeds.sf.tv/podcast/sternstundephilosophie')
     addFeed('SF Sternstunde Religion','http://feeds.sf.tv/podcast/sternstundereligion')
     addFeed('SF Tierische Freunde','http://feeds.sf.tv/podcast/tierischefreunde')
     addFeed('SF Total Birgit','http://feeds.sf.tv/podcast/totalbirgit') 
     addFeed('SF Üsi Badi','http://feeds.sf.tv/podcast/uesibadi')
     addFeed('SF Wort zum Sonntag','http://feeds.sf.tv/podcast/wortzumsonntag')  
     addFeed('SF Zambooster','http://feeds.sf.tv/podcast/zambooster') 
     addFeed('SF Zamborium','http://feeds.sf.tv/podcast/zamborium') 

     # switzerland puplic radio sr drs  (you can add more .... seeh here http://www.drs.ch/www/de/drs/podcasts.html

     addFeed('SR DRS 100 Sekunden Wissen', 'http://pod.drs.ch/100_sekunden_wissen_mpx.xml') 
     addFeed('SR DRS Atlas','http://pod.drs.ch/atlas_mpx.xml')
     addFeed('SR DRS Best of Auslandswoche','http://pod.drs.ch/drs4_bestof_ausland_mpx.xml') 
     addFeed('SR DRS Best of Inlandswoche','http://pod.drs.ch/drs4_bestof_inland_mpx.xml')     
     addFeed('SR DRS Best of Höhrpunkt','http://pod.drs.ch/best_of_hoerpunkt_mpx.xml')
     addFeed('SR DRS Bestseller auf dem Plattenteller','http://pod.drs.ch/bestseller_auf_dem_plattenteller_mpx.xml')
     addFeed('SR DRS Blickpunkt Religion','http://pod.drs.ch/blickpunkt_religion_mpx.xml')
     addFeed('SR DRS Buchzeichen','http://pod.drs.ch/BuchZeichen_mpx.xml')
     addFeed('SR DRS Info 3','http://pod.drs.ch/info3_mpx.xml')
     addFeed('SR DRS Wissen aktuell','http://pod.drs.ch/wissen_aktuell_mpx.xml') 

     # Pour la romandie ....

     addLink('La première (MP3, 128kb/s)',    'http://broadcast.infomaniak.ch/rsr-la1ere-high.mp3','')
     addLink('Espace 2 (MP3, 128kb/s)',       'http://broadcast.infomaniak.ch/rsr-espace2-high.mp3','')
     addLink('Couleur 3 (MP3, 128kb/s)',      'http://broadcast.infomaniak.ch/rsr-couleur3-high.mp3','')
     addLink('Option Musique (MP3, 128kb/s)', 'http://broadcast.infomaniak.ch/rsr-optionmusique-high.mp3','')
     addLink('La première (AAC, 96kb/s)',     'http://broadcast.infomaniak.ch/rsr-la1ere-high.aac','')
     addLink('Espace 2 (AAC, 96kb/s)',        'http://broadcast.infomaniak.ch/rsr-espace2-high.aac','')
     addLink('Couleur 3 (AAC, 96kb/s)',       'http://broadcast.infomaniak.ch/rsr-couleur3-high.aac','')
     addLink('Option Musique (AAC, 96kb/s)',  'http://broadcast.infomaniak.ch/rsr-optionmusique-high.aac','')
     addLink('La première (MP3, 48kb/s)',     'http://broadcast.infomaniak.ch/rsr-la1ere-low.mp3','')
     addLink('Espace 2 (MP3, 48kb/s)',        'http://broadcast.infomaniak.ch/rsr-espace2-low.mp3','')
     addLink('Couleur 3 (MP3, 48kb/s)',       'http://broadcast.infomaniak.ch/rsr-couleur3-low.mp3','')
     addLink('Option Musique (MP3, 48kb/s)',  'http://broadcast.infomaniak.ch/rsr-optionmusique-low.mp3','')


def addFeed(name, url):
    addDir(name, url, 10,'swiss-podcasts')

def getPodcasts(url):

    syslog ("getPodcasts :"  + url) 

    # Get HTML-Code from the site

    url = url.replace('feed://', 'http://')


    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()

    # Analyze HTML-Code

    syslog ("-------------------------------")
    syslog ("Analyze URL :" + url)
    syslog ("-------------------------------")  
    match=re.compile('<item>(.+?)</item>',re.S).findall(link)
    syslog ("found links :" + str(len(match)))
    found = len(match)
    if (found >= 1): 
        for i in range(len(match)):
              title=re.compile('<title>(.+?)</title>',re.S,).findall(match[i])
              audioLink=re.compile('<enclosure url=\"(.+?)\"',re.S,).findall(match[i])
              addLink(str(i+1) + '. ' + title[0],audioLink[0], '')
              syslog ("-------------------------------")
              syslog ("Title     : " + title[0])
              syslog ("AudioLink : " + audioLink[0]) 
              syslog ("-------------------------------")
        syslog ("-------------------------------")
        syslog ("Addlink successull")
        syslog ("-------------------------------")
    else:
         syslog ("-------------------------------")
         syslog ("Extract mv4 / airdate from  :" + url)
         syslog ("-------------------------------")  

         list1 = re.findall('<enclosure url=\"(.+?)\"',link, re.M)
         list2 = re.findall('<title>(.+?)</title>',link, re.M)
  
         # The first element can allways be removed .... it contains only show-name 
 
         indexes = len(list2)
         if (indexes >= 1):           
             del list2[0]       
             syslog ("list1 :" + str(list1))
             syslog ("list2 :" + str(list2))
             index = len(list1)
             for index in range(0,index):
                 addLink(str(index+1) + '. ' + str (list2[index]),str(list1[index]) + 'm4v', '')
             syslog ("-------------------------------")
             syslog ("Extract mv4 done")
             syslog ("-------------------------------")    

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

#########################################################
####################### MAIN ############################
#########################################################
if __name__ == '__main__':
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
        print ""
        addPodcasts()
   elif mode==10:
        print ""+url
        getPodcasts(url)
   xbmcplugin.endOfDirectory(int(sys.argv[1]))
#########################################################
#########################################################
#########################################################