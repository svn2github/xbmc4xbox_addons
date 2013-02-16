#
# Imports
#
import sys
import xbmc
import xbmcgui
import xbmcplugin
import socket
import struct

#
# Main class
#
class Main:
    def __init__( self ):
        #
        # Parse parameters...
        #
        params        = dict(part.split('=') for part in sys.argv[ 2 ][ 1: ].split('&'))    
        computer_name = params[ "name" ]
        computer_mac  = params[ "mac"  ]
        
        #
        # Show progress dialog...
        #
        dialog = xbmcgui.DialogProgress()
        dialog.create( xbmc.getLocalizedString(30902), computer_name, computer_mac )
        dialog.update( 100 )
        
        #
        # Remove separator (- or :)
        #
        if len(computer_mac) == 12 + 5 :
            computer_mac = computer_mac.replace(computer_mac[2], '') 
        
        #
        # Pad the synchronization stream.
        #
        data      = ''.join(['FFFFFFFFFFFF', computer_mac * 20])
        send_data = '' 

        #
        # Split up the hex values and pack.
        #
        for i in range(0, len(data), 2):
            send_data = ''.join([send_data, struct.pack('B', int(data[i: i + 2], 16))]) 

        #
        # Broadcast it to the LAN.
        #
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(send_data, ('<broadcast>', 7))
        sock.close()
        
        #
        # Return
        #
        xbmc.sleep( 1000 )
        dialog.close()