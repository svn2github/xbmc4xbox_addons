#
# Imports
#
import os
import sys
import xbmc
import xbmcgui
import xbmcplugin
import socket
import select
import time
from impacket  import ImpactDecoder
from impacket  import ImpactPacket
from threading import Thread

#
# Main class
#
class Main( xbmcgui.WindowXMLDialog ):
    ACTION_EXIT_SCRIPT = ( 9, 10, 216, 257, 61448, )
    
    #
    #
    # 
    def __init__( self, *args, **kwargs ):
        #
        # User to choose an address...
        #
        
        # Previously pinged addresses...
        try :
            ping_addrs = eval( xbmcplugin.getSetting( "ping_addrs" ) )
        except :
            ping_addrs = []

        # Insert entry for "New address"...
        ping_addrs.insert(0, xbmc.getLocalizedString(30302))

        # User choice...
        dialogAddrs    = xbmcgui.Dialog()
        index          = dialogAddrs.select( xbmc.getLocalizedString(30201), ping_addrs )
        self.ping_addr = ""
        
        # New address...
        if index == 0 :            
            keyboard = xbmc.Keyboard( "", xbmc.getLocalizedString( 30301 ) )
            keyboard.doModal()
            if keyboard.isConfirmed() :
                self.ping_addr = keyboard.getText()                

        # Previous address..
        if index > 0 :
            self.ping_addr = ping_addrs[ index ]

        #
        # User made a choice...
        #
        if self.ping_addr > "" :
            #
            # Save address for future use...
            #
            ping_addrs.pop( 0 )
            try :
                ping_addrs.index ( self.ping_addr )
            except :
                ping_addrs.append( self.ping_addr )
            ping_addrs.sort()
            xbmcplugin.setSetting( "ping_addrs", repr( ping_addrs ))
            
            #
            # Show text window (+ pinging, see onInit)...
            #            
            self.doModal()

    #
    #
    #
    def onInit( self ):
        #
        # Ping host...
        #
        self.textbox = self.getControl( 5 )

        self.pingerThread = PingerThread( self.ping_addr , self.textbox )
        self.pingerThread.start()

    #
    # onClick handler
    #
    def onClick( self, controlId ):
        pass

    #
    # onFocus handler
    #
    def onFocus( self, controlId ):
        pass

    #
    # onAction handler
    #
    def onAction( self, action ):
        if action and ( action in self.ACTION_EXIT_SCRIPT ):
            # Stop pinger thread...
            if self.pingerThread != None :
                self.pingerThread.stop()
            
            # Close window...
            self.close()
       
#
# Pinger thread...
#
class PingerThread( Thread ):
    #
    def __init__( self, dst_host, textbox ):
        Thread.__init__(self)
        
        #
        self.dst_host = dst_host
        self.text     = ""
        self.lines    = 0
        self.textbox  = textbox
                
    # Run...
    def run(self):
        self.should_stop = False
        
        # Ping host...
        self.ping( self.dst_host )

    # Stop...
    def stop(self):
        self.should_stop = True
        
    # Ping
    def ping(self, dst_host ):
        # Init...
        PAYLOAD_SIZE = 32
        
        # Source + Dest IPs...
        src_ip = socket.gethostbyname(socket.gethostname())        
        try :
            dst_ip = socket.gethostbyname( dst_host )
        except socket.gaierror, e :
            text = xbmc.getLocalizedString(30401) + os.linesep + dst_host
            self.displayText( text )
            return
        
        # Output...
        text = "Pinging %s [%s] with %d bytes of data:" % ( dst_host, dst_ip, PAYLOAD_SIZE )
        self.displayText( text )
         
        # Create a new IP packet and set its source and destination addresses.
        ip = ImpactPacket.IP()
        ip.set_ip_src(src_ip)
        ip.set_ip_dst(dst_ip)
         
        # Create a new ICMP packet of type ECHO...
        icmp = ImpactPacket.ICMP()
        icmp.set_icmp_type(icmp.ICMP_ECHO)
         
        # Include a N-character long payload inside the ICMP packet
        icmp.contains( ImpactPacket.Data( "A" * PAYLOAD_SIZE ) )
         
        # Have the IP packet contain the ICMP packet (along with its payload).
        ip.contains(icmp)
         
        # Open a raw socket. Special permissions are usually required.
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        
        # Start pingin...
        seq_id = 0
        while True :
            # Stop thread...
            if self.should_stop == True :
                break
            
            # Give the ICMP packet the next ID in the sequence.
            seq_id += 1
            icmp.set_icmp_id(seq_id)
            
            # Calculate checksum...
            icmp.set_icmp_cksum(0)
            icmp.auto_checksum = 1
         
            # Send packet to target host...
            startTime = time.time()
            sock.sendto(ip.get_packet(), (dst_ip, 0))
         
            # Wait for incoming replies (timeout = 2 sec)...
            reply = select.select([sock], [], [], 2)[0]
            
            # Check reply...
            if sock in reply:
                # Use ImpactDecoder to reconstruct the packet hierarchy.
                reply = sock.recvfrom(2000)[0]         
                rip   = ImpactDecoder.IPDecoder().decode(reply)
                ricmp = rip.child()
         
                # Calculate reply delay...
                icmp_delay = ( time.time() - startTime ) * 1000        

                # Reply...
                if rip.get_ip_dst() == src_ip and rip.get_ip_src() == dst_ip and icmp.ICMP_ECHOREPLY == ricmp.get_icmp_type():
                    text = xbmc.getLocalizedString(30402) % ( dst_ip, PAYLOAD_SIZE, icmp_delay )
                    self.displayText( text )
                # Timeout...
                else :
                    self.displayText( xbmc.getLocalizedString(30403) )
                
                # Sleep (1 sec)...
                time.sleep(1)

            # Timeout...
            if reply == [] :
                self.displayText( xbmc.getLocalizedString(30403) )
                
    #
    # Display text...
    #
    def displayText ( self, text ):
        self.lines = self.lines + 1
        
        # Clear text if too many lines (unable to scroll?!)
        if self.lines > 20 :
            self.text  = ""
            self.lines = 1

        # Display...
        self.text  = self.text + os.linesep + text
        self.textbox.setText( self.text )
        
