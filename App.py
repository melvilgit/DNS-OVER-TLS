import socket
import ssl
import binascii
import struct
from logger import logger

HOST, PORT = '1.1.1.1', 853


class dnsTLS:

    def extractIp(self, response):
        """Function will extract IP field from last 8 fields of HEXA ,REF - https://tools.ietf.org/html/rfc1035
           @params - response - DNS Response
           @return - The IP from the DNS Response
         """
        ip = ""
        ip_hex = response[-8:]

        for sub in range(0, len(ip_hex), 2):
            ip_octet = ip_hex[sub:sub + 2]
            ip += str(int(ip_octet, 16)) + "."
        return ip[:-1]

    def getLength(self, packet):
        """Function will gets the length of DNS TCP Packet for a domain
           @params - packet - DNS Packet
           @return - Packet Length in HEXA format
        """
        l = len(packet) / 2
        h = "{0:x}".format(l)
        diff = 4 - len(h)
        return diff * "0" + h

    def buildPacket(self, url):
        """Function will build a DNS packet as per rfc1035 - Uses struct to  Interpret strings as packed binary data
         @params - the url to query in dns
         @return - DNS PACKET !
         """
        packet = struct.pack(">H", 12049)  # Query Ids (Just 1 for now)
        packet += struct.pack(">H", 256)  # Flags
        packet += struct.pack(">H", 1)  # Questions
        packet += struct.pack(">H", 0)  # Answers
        packet += struct.pack(">H", 0)  # Authorities
        packet += struct.pack(">H", 0)  # Additional
        split_url = url.split(".")
        for part in split_url:
            packet += struct.pack("B", len(part))
            for byte in bytes(part):
                packet += struct.pack("c", byte)
        packet += struct.pack("B", 0)  # End of String
        packet += struct.pack(">H", 1)  # Query Type
        packet += struct.pack(">H", 1)  # Query Class
        logger.debug(packet)
        return packet

    def sendMessage(self, _message, sock):
        """Function will sends the DNS Packet Message to the DNS Over TLS Provider"""
        __message = _message.replace(" ", "").replace("\n", "")
        m = binascii.unhexlify(__message)
        sock.send(m)
        data = sock.recv(4096)
        return binascii.hexlify(data).decode("utf-8")

    def connect(self):
        """Function to create SSL session and return it """
        # CREATE SOCKET
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(100)

        context = ssl.create_default_context()
        context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        context.load_verify_locations('./ca-certificate.crt')

        wrappedSocket = context.wrap_socket(sock, server_hostname=HOST)

        # CONNECT AND PRINT REPLY
        wrappedSocket.connect((HOST, PORT))

        # CLOSE SOCKET CONNECTION
        return wrappedSocket
