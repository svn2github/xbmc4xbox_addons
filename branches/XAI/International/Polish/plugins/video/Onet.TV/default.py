__plugin__  = "Onet.TV"
__author__  = "pajretX"
__date__    = "11-03-10"
__version__ = "0.03"

import os
import sys

LIB_DIR = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'lib' ) )
sys.path.append (LIB_DIR)

#
# Wiadomości
#
if ( "wiado" in sys.argv[ 2 ] ):
	import wiadomosci as plugin
#
# Religia
#
elif ( "rel" in sys.argv[ 2 ] ):
    import religia as plugin
#
# Rozrywka
#
elif ( "rozr" in sys.argv[ 2 ] ):
    import rozrywka as plugin
#
# Film
#
elif ( "film" in sys.argv[ 2 ] ):
    import film as plugin
#
# Gry
#
elif ( "gry" in sys.argv[ 2 ] ):
    import gry as plugin
#
# Biznes
#
elif ( "biz" in sys.argv[ 2 ] ):
    import  biznes as plugin
#
# Gotowanie
#
elif ( "got" in sys.argv[ 2 ] ):
    import gotowanie as plugin
#
# Plejada talentów
#
elif ( "plej" in sys.argv[ 2 ] ):
    import plejada as plugin
#
# Sport
#
elif ( "sport" in sys.argv[ 2 ] ):
    import sport as plugin
#
# Styl życia
#
elif ( "styl" in sys.argv[ 2 ] ):
    import styl as plugin
#
# Muzyka
#
elif ( "muz" in sys.argv[ 2 ] ):
    import muzyka as plugin
#
# Podróże
#
elif ( "pod" in sys.argv[ 2 ] ):
    import podroze as plugin
#
# Edukacja
#
elif ( "edu" in sys.argv[ 2 ] ):
    import edukacja as plugin
#
# Moto
#
elif ( "moto" in sys.argv[ 2 ] ):
    import moto as plugin
#
# Świat dziecka
#
elif ( "swiat" in sys.argv[ 2 ] ):
    import swiat as plugin
#
# RSS nazwy i inne takie..
#
elif ( "RSS" in sys.argv[ 2 ] ):
   import RSSszperator as plugin
#
# Odtwarzaj
#

else :
	import onet_main as plugin

plugin.Main()
