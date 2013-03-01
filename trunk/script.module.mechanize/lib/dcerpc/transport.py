# Copyright (c) 2003 CORE Security Technologies
#
# This software is provided under under a slightly modified version
# of the Apache Software License. See the accompanying LICENSE file
# for more information.
#
# $Id: transport.py,v 1.3 2003/10/28 19:50:29 jkohen Exp $
#
# Description:
#   Transport implementations for the DCE/RPC protocol.
#
# Author:
#   Alberto Solino (beto)
#   Javier Kohen (jkohen)

import re
import socket

from impacket import smb
from impacket import nmb

class DCERPCStringBinding:
    parser = re.compile(r'(?:([a-fA-F0-9-]{8}(?:-[a-fA-F0-9-]{4}){3}-[a-fA-F0-9-]{12})@)?' # UUID (opt.)
                        +'([_a-zA-Z0-9]*):' # Protocol Sequence
                        +'([^\[]*)' # Network Address (opt.)
                        +'(?:\[([^\]]*)\])?') # Endpoint and options (opt.)

    def __init__(self, stringbinding):
        match = DCERPCStringBinding.parser.match(stringbinding)
        self.__uuid = match.group(1)
        self.__ps = match.group(2)
        self.__na = match.group(3)
        options = match.group(4)
        if options:
            options = options.split(',')
            self.__endpoint = options[0]
            try:
                self.__endpoint.index('endpoint=')
                self.__endpoint = self.__endpoint[len('endpoint='):]
            except:
                pass
            self.__options = options[1:]
        else:
            self.__endpoint = ''
            self.__options = []

    def get_uuid(self):
        return self.__uuid

    def get_protocol_sequence(self):
        return self.__ps

    def get_network_address(self):
        return self.__na

    def get_endpoint(self):
        return self.__endpoint

    def get_options(self):
        return self.__options

    def __str__(self):
        return DCERPCStringBindingCompose(self.__uuid, self.__ps, self.__na, self.__endpoint, self.__options)

def DCERPCStringBindingCompose(uuid=None, protocol_sequence='', network_address='', endpoint='', options=[]):
    s = ''
    if uuid: s += uuid + '@'
    s += protocol_sequence + ':'
    if network_address: s += network_address
    if endpoint or options:
        s += '[' + endpoint
        if options: s += ',' + ','.join(options)
        s += ']'

    return s

def DCERPCTransportFactory(stringbinding):
    sb = DCERPCStringBinding(stringbinding)

    na = sb.get_network_address()
    ps = sb.get_protocol_sequence()
    if 'ncadg_ip_udp' == ps:
        port = sb.get_endpoint()
        if port:
            return UDPTransport(na, int(port))
        else:
            return UDPTransport(na)
    elif 'ncacn_ip_tcp' == ps:
        port = sb.get_endpoint()
        if port:
            return TCPTransport(na, int(port))
        else:
            return TCPTransport(na)
    elif 'ncacn_http' == ps:
        port = sb.get_endpoint()
        if port:
            return HTTPTransport(na, int(port))
        else:
            return HTTPTransport(na)
    elif 'ncacn_np' == ps:
        named_pipe = sb.get_endpoint()
        if named_pipe:
            named_pipe = named_pipe[len(r'\pipe'):]
            return SMBTransport(na, filename = named_pipe)
        else:
            return SMBTransport(na)
    else:
        raise Exception, "Unknown protocol sequence."


class DCERPCTransport:
    def __init__(self, dstip, dstport):
        self.__dstip = dstip
        self.__dstport = dstport

    def connect(self):
        raise RuntimeError, 'virtual function'
    def send(self,data=0):
        raise RuntimeError, 'virtual function'
    def recv(self):
        raise RuntimeError, 'virtual function'
    def disconnect(self):
        raise RuntimeError, 'virtual function'

    def get_dip(self):
        return self.__dstip
    def set_dip(self, dip):
        "This method only makes sense before connection for most protocols."
        self.__dstip = dip

    def get_dport(self):
        return self.__dstport
    def set_dport(self, dport):
        "This method only makes sense before connection for most protocols."
        self.__dstport = dport

    def get_addr(self):
        return (self.get_dip(), self.get_dport())
    def set_addr(self, addr):
        "This method only makes sense before connection for most protocols."
        self.set_dip(addr[0])
        self.set_dport(addr[1])


class UDPTransport(DCERPCTransport):
    "Implementation of ncadg_ip_udp protocol sequence"

    def __init__(self,dstip, dstport = 135):
        DCERPCTransport.__init__(self, dstip, dstport)
        self.__socket = 0

    def connect(self):
        try:
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                self.__socket.settimeout(30)
            except AttributeError:
                print "Warning: timeout not available."
        except socket.error, msg:
            self.__socket = None
            raise Exception, "Could not connect: %s" % msg

        return 1

    def disconnect(self):
        try:
            self.__socket.close()
        except socket.error, msg:
            self.__socket = None
            return 0
        return 1

    def send(self,data):
        self.__socket.sendto(data,(self.get_dip(),self.get_dport()))

    def recv(self):
        buffer, self.__recv_addr = self.__socket.recvfrom(8192)
        return buffer

    def get_recv_addr(self):
        return self.__recv_addr


class TCPTransport(DCERPCTransport):
    "Implementation of ncacn_ip_tcp protocol sequence"

    def __init__(self, dstip, dstport = 135):
        DCERPCTransport.__init__(self, dstip, dstport)
        self.__socket = 0

    def connect(self):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            try:
                self.__socket.settimeout(300)
            except AttributeError:
                print "Warning: timeout not available."
            self.__socket.connect((self.get_dip(), self.get_dport()))
        except socket.error, msg:
            self.__socket.close()
            raise Exception, "Could not connect: %s" % msg

        return 1

    def disconnect(self):
        try:
            self.__socket.close()
        except socket.error, msg:
            self.__socket = None
            return 0
        return 1

    def send(self,data):
        self.__socket.send(data)

    def recv(self):
        buffer = self.__socket.recv(8192)
        return buffer

class HTTPTransport(DCERPCTransport):
    "Implementation of ncacn_http protocol sequence"

    def __init__(self,dstip, dstport = 80):
        DCERPCTransport.__init__(self, dstip, dstport)
        self.__socket = 0
    def connect(self):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            try:
                self.__socket.settimeout(300)
            except AttributeError:
                print "Warning: timeout not available."
            self.__socket.connect((self.get_dip(), self.get_dport()))
        except socket.error, msg:
            self.__socket.close()
            raise Exception, "Could not connect: %s" % msg

        self.__socket.send('RPC_CONNECT ' + self.get_dip() + ':593 HTTP/1.0\r\n\r\n')
        data = self.__socket.recv(8192)
        if data[10:13] != '200':
            raise Exception("Service not supported.")

    def send(self, buffer):
        self.__socket.send(buffer)
    def recv(self):
        data = self.__socket.recv(8192)
        return data
    def disconnect(self):
        self.__socket.close()

class SMBTransport(DCERPCTransport):
    "Implementation of ncacn_np protocol sequence"

    def __init__(self, dstip, dstport = 445, filename = '', username='', password=''):
        DCERPCTransport.__init__(self, dstip, dstport)
        self.__socket = None
        self.__smb_server = 0
        self.__tid = 0
        self.__filename = filename
        self.__handle = 0
        self.set_credentials(username, password)

    def set_credentials(self, username, password):
        self.__username = username
        self.__password = password

    def connect(self):
        self.__smb_server = smb.SMB('*SMBSERVER',self.get_dip(), sess_port = self.get_dport())
        if self.__smb_server.is_login_required():
            self.__smb_server.login(self.__username, self.__password)
        self.__tid = self.__smb_server.connect_tree('\\\\*SMBSERVER\\IPC$', smb.SERVICE_ANY, None)
        self.__handle = self.__smb_server.nt_create(self.__tid, self.__filename)
        self.__socket = self.__smb_server.get_socket()
        return 1
    
    def disconnect(self):
        self.__smb_server.disconnect_tree(self.__tid)
        self.__smb_server.logoff()

    def send(self,data):
        self.__smb_server.send_trans(self.__tid,'\x26\x00' + self.__handle,'\\PIPE\\'+'\x00','',data)
        
    def recv(self):
        s = self.__smb_server.recv_packet()
        if self.__smb_server.isValidAnswer(s,smb.SMB.SMB_COM_TRANSACTION):
            trans = smb.TRANSHeader(s.get_parameter_words(), s.get_buffer())
            data = trans.get_data()
            return data
        return 0