from App import dnsTLS
import socket
import threading
from logger import logger


class ThreadedServer(object):
    def __init__(self, host, port):
        """ Initialization of each socket attributes"""
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def resolve(self, url):
        """Function resolves a url/domain to the Corresponding DNS Record
        Since We are using TCP DNS We PREPEND The length of the message (packet_length) REF - RFC7766 #section-8
        Establishes a TLS conn with cloudfare and returns the Response
        @params - url - the domain/url/hostname
        """
        dnsTLdObj = dnsTLS()
        tcp_packet = dnsTLdObj.buildPacket(url).encode("hex")
        packet_length = dnsTLdObj.getLength(tcp_packet)
        message = packet_length + tcp_packet
        conn = dnsTLdObj.connect()
        dns_response = dnsTLdObj.sendMessage(message, conn)

        ip = dnsTLdObj.extractIp(dns_response)
        return ip

    def listen(self):
        """Function creates different Threads for parallel socket processing via python inbuilt threading """
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            threading.Thread(target=self.listenToClient, args=(client, address)).start()

    def listenToClient(self, client, address):
        """Function will listen to client on TCP 53 and check for messages with format "domain:url"  and calls resolve subroutine
        @params client - The TCP client which will talk to the callee
        """
        size = 1024
        while True:
            try:
                data = client.recv(size)
                logger.debug(data)
                if data:
                    query = str(data).split(":")
                    if query[0] == 'domain':
                        # Set the response to echo back the recieved data
                        url = query[1]
                        dns_response = self.resolve(url)
                        logger.info("{0} retrieved for DNS query on {1}".format(dns_response, url))
                        client.send(dns_response)
                else:
                    raise error('Client disconnected')
            except:
                client.close()
                return False


if __name__ == "__main__":
    port_num = 53
    ThreadedServer('', port_num).listen()
