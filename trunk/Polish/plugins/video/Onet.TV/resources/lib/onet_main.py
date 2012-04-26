#
# Imports
#
import os
import sys
import xbmc
import xbmcgui
import xbmcplugin
HOME_DIR = os.getcwd()
names = xbmc.Language( HOME_DIR ).getLocalizedString

wiad = (names (30000))
rel = (names (30001))
roz = (names (30002))
fil = (names (30003))
gry = (names (30004))
biz = (names (30005))
got = (names (30006))
ple = (names (30007))
spo = (names (30008))
sty = (names (30009))
muz = (names (30010))
pod = (names (30011))
edu = (names (30012))
mot = (names (30013))
swi = (names (30014))
#
# Main class
#
class Main:
	def __init__( self ):
        
        #
        # Wiadomości
        #
		listitem = xbmcgui.ListItem( wiad, iconImage="DefaultFolder.png" )
		xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1] ), url = '%s?wiado&po_co=%s' % ( sys.argv[ 0 ], "Wiadomości" ), listitem=listitem, isFolder=True)		
        #
        # Religia
        #
		listitem = xbmcgui.ListItem( rel, iconImage="DefaultFolder.png" )
		xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?rel&po_co=%s' % ( sys.argv[ 0 ], "Religia" ), listitem=listitem, isFolder=True)
		
        #		
        # Rozrywka
        #
		listitem = xbmcgui.ListItem( roz, iconImage="DefaultFolder.png" )
		xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?rozr&po_co=%s' % ( sys.argv[ 0 ], "Rozrywka" ), listitem=listitem, isFolder=True)

        #
        # Film
        #
		listitem = xbmcgui.ListItem( fil, iconImage="DefaultFolder.png" )
		xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?film&po_co=%s' % ( sys.argv[ 0 ], "Film" ), listitem=listitem, isFolder=True)

        #
        # Gry
        #
		listitem = xbmcgui.ListItem( gry, iconImage="DefaultFolder.png" )
		xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?gry&po_co=%s' % ( sys.argv[ 0 ], "Gry" ), listitem=listitem, isFolder=True)

        #
        # Biznes
        #
		listitem = xbmcgui.ListItem( biz, iconImage="DefaultFolder.png" )
		xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?biz&po_co=%s' % ( sys.argv[ 0 ], "Biznes" ), listitem=listitem, isFolder=True)
        
        #
        # Gotowanie
        #
		listitem = xbmcgui.ListItem( got, iconImage="DefaultFolder.png" )
		xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?got&po_co=%s' % ( sys.argv[ 0 ], "Gotowanie" ), listitem=listitem, isFolder=True)

        #
        # Plajada talentów
        #
		listitem = xbmcgui.ListItem( ple, iconImage = "DefaultFolder.png" )
		xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?plej&po_co=%s' % ( sys.argv[ 0 ], "Plejada Talentów" ), listitem=listitem, isFolder=True)
        
        #
        #  Sport
        #
		listitem = xbmcgui.ListItem( spo, iconImage = "DefaultFolder.png" )
		xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?sport&po_co=%s' % ( sys.argv[ 0 ], "Sport" ), listitem=listitem, isFolder=True)

        #
        #  Styl życia
        #
		listitem = xbmcgui.ListItem( sty, iconImage = "DefaultFolder.png" )
		xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?styl&po_co=%s' % ( sys.argv[ 0 ], "Styl życia" ), listitem=listitem, isFolder=True)

        #
        #  Muzyka
        #
		listitem = xbmcgui.ListItem( muz, iconImage = "DefaultFolder.png" )
		xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?muz&po_co=%s' % ( sys.argv[ 0 ], "Muzyka" ), listitem=listitem, isFolder=True)

        #
        #  Podróże
        #
		listitem = xbmcgui.ListItem( pod, iconImage = "DefaultFolder.png" )
		xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?pod&po_co=%s' % ( sys.argv[ 0 ], "Podróże" ), listitem=listitem, isFolder=True)

        #
        #  Edukacja
        #
		listitem = xbmcgui.ListItem( edu, iconImage = "DefaultFolder.png" )
		xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?edu&po_co=%s' % ( sys.argv[ 0 ], "Edukacja" ), listitem=listitem, isFolder=True)

        #
        #  Moto
        #
		listitem = xbmcgui.ListItem( mot, iconImage = "DefaultFolder.png" )
		xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?moto&po_co=%s' % ( sys.argv[ 0 ], "Moto" ), listitem=listitem, isFolder=True)

        #
        #  Świat dziecka
        #
		listitem = xbmcgui.ListItem( swi, iconImage = "DefaultFolder.png" )
		xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?swiat&po_co=%s' % ( sys.argv[ 0 ], "Świat dziecka" ), listitem=listitem, isFolder=True)

        # Disable sorting...
		xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
		
        # End of list...
		xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
