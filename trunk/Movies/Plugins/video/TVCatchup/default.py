moduleNames= ['urllib2','os','sys','xbmcgui','xbmc','xbmcaddon','zipfile','re']
modules = map(__import__, moduleNames)
modules

modules[2].path.insert(0, modules[1].path.join(modules[1].getcwd(), 'lib'))
modules[2].path.insert(0, modules[1].path.join(modules[1].getcwd(), 'resources'))

tmp_lib=__import__('TVClibs')

__scriptname__ = "plugin.video.tvcatchup"
__author__     = 'dj_gerbil [tvc@killergerbils.co.uk]'
__svn_url__    = ""
__version__    = "1.4.4"
__phpurl__ = tmp_lib.Ii( "WVQvbHNDPXB3L3dyOUtJXVg1c3ApNHFpeC5qdj9fcTtUZmh6UFFmdGZ1ZHJrQFksS0h+Mld4Mm1meHJkOVtvXTgwbXFVZWV4ZmMyMGtVRWg+ZSB0a10jIGsgcyJMbSlSMg==" , 3 )    
__settings__ = modules [ 5 ] . Addon ( id = 'plugin.video.tvcatchup' )
__addon__ = modules [ 5 ].Addon('plugin.video.tvcatchup')

##addonxml = open(__addon__.getAddonInfo('path')+'/addon.xml',mode="rb")
##addonxmldata = addonxml.read()
##addonversion = modules[7] . compile ( 'version="(.+?)"' ) . findall (addonxmldata)
##addonxml.close()
##
##iIiiiI = modules[0].urlopen( __phpurl__ + "?func=version")
##version = iIiiiI.read ()
##if (not version == addonversion[1]):
##  updateneeded=False
##  explodedaddonversion=addonversion[1].split(".")
##  explodedversion=version.split(".")
##  if (explodedaddonversion[0]<explodedversion[0]):
##    updateneeded=True
##  elif (explodedaddonversion[1]<explodedversion[1]):
##    updateneeded=True
##  elif (explodedaddonversion[2]<explodedversion[2]):
##    updateneeded=True
##  if(updateneeded==True):
##    QqQ = __settings__ . getSetting ( 'autoupdate' )
##    if (QqQ<>"true"):
##      modules[4].executebuiltin( "xbmc.Notification('TVCatchup Plugin Update...', Please go to http://plugins.tvcatchup.com/~xbmc/ to download the updated plugin. , 10000,%s)" % (modules[1].path.join(__addon__.getAddonInfo('path'),"icon.png"),)) 
##    else:
##      print "Getting Update..."
##      iIiiiI = modules[0].urlopen("http://plugins.tvcatchup.com/~xbmc/"+__scriptname__+version.replace(".","")+".zip")
##      downloadedupdate = iIiiiI.read ()
##      updatefile = open(str(__addon__.getAddonInfo('path'))+version.replace(".","")+".zip",mode="wb")
##      updatefile.write(downloadedupdate)
##      updatefile.close()
##      
##      modules[4].executebuiltin("xbmc.Notification('Decompressing File...', 'Please Wait' , 1000,%s)"% ( modules[1].path.join( modules[1].getcwd(), "small.png" ),))
##      print str(__addon__.getAddonInfo('path'))+version.replace(".","")+".zip"
##      zfile = modules[6].ZipFile( str(__addon__.getAddonInfo('path'))+version.replace(".","")+".zip", "r" )
##      for info in zfile.infolist():
##        fname = info.filename
##        print fname
##        data = zfile.read(fname)
##        filename = fname.replace("/",modules[1].sep)
##        #test= m+filename
##        tester=filename.split(modules[1].sep)
##        l=""
##        for k in range(0,len(tester)-1):
##          l=l+str(tester[k])
##          l=l+modules[1].sep
##          if not modules[1].path.isdir(l):
##            if not modules[1].path.exists(__addon__.getAddonInfo('path').replace(__scriptname__,"") + l):
##              print "Creating Directory..."+__addon__.getAddonInfo('path').replace(__scriptname__,"") + l
##              modules[1].makedirs(__addon__.getAddonInfo('path').replace(__scriptname__,"") + l)
##          if not filename.endswith(modules[1].sep):
##            print "Creating File..." +__addon__.getAddonInfo('path').replace(__scriptname__,"")+ filename
##            if not(filename=="plugin.video.tvcatchup\default.py"):
##              if modules[1].path.exists(__addon__.getAddonInfo('path').replace(__scriptname__,"")+ filename):
##                print "Oooooops, looks like it's already here. Better get rid of it."
##                modules[1].remove(__addon__.getAddonInfo('path').replace(__scriptname__,"")+ filename)
##              fout = open(__addon__.getAddonInfo('path').replace(__scriptname__,"")+filename, "wb")
##              fout.write(data)
##              fout.close()
##      zfile.close()

iIiiiI = modules[0].urlopen( __phpurl__ + "?func=chansavailable")
chansavailable = iIiiiI.readlines()
settingsfile = open(__addon__.getAddonInfo('path')+'/resources/settings.xml',mode="rb")
settingsfile2 = open(__addon__.getAddonInfo('path')+'/resources/language/English/strings.xml',mode="rb")
lines = settingsfile.readlines()
lines2 = settingsfile2.readlines()
settingsfile.close()
settingsfile2.close()
differences = False
for bob2 in range(0,len(chansavailable)):
  lineexists = False
  for bob in range(1,len(lines)-1):
    if (lines[bob].find(chansavailable[bob2].replace(" ","_").replace("\n",""))<>-1):
      lineexists = True
  if (lineexists <> True):
    differences = True
if (differences <> False):
  settingsfile = open(__addon__.getAddonInfo('path')+'/resources/settings.xml',mode="wb")
  settingsfile2 = open(__addon__.getAddonInfo('path')+'/resources/language/English/strings.xml',mode="wb")
  settingsfile.write(lines[0])
  settingsfile2.write(lines2[0])
  for bob in range(1,len(lines)-1):
    settingsfile.write(lines[bob])
    settingsfile2.write(lines2[bob])
  for bob2 in range(0,len(chansavailable)):
    lineexists = False
    for bob in range(1,len(lines)-1):
      if (lines[bob].find(chansavailable[bob2].replace(" ","_").replace("\n",""))<>-1):
        lineexists = True
    if (lineexists <> True):
      settingsfile.write('\t<setting id="'+chansavailable[bob2].replace(" ","_").replace("\n","")+'" label="'+str(3000+len(lines)-2+bob2)+'" type="bool" default="true" />'+"\n")
      settingsfile2.write('\t<string id="'+str(3000+len(lines)-2+bob2)+'">'+chansavailable[bob2].replace("\n","")+'</string>'+"\n")
  settingsfile.write(lines[len(lines)-1])
  settingsfile2.write(lines2[len(lines2)-1])
  settingsfile.close()
  settingsfile2.close()

tmp_lib2=__import__('TVClibs2',globals())

tmp_lib2.oO00ooo0()

