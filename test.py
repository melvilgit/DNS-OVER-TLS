import os
import unittest
import socket
from App import dnsTLS
from dnsOverTls import  ThreadedServer


class BasicTests(unittest.TestCase):


    def setUp(self):
        print "starting test"


    # executed after each test
    def tearDown(self):
        print "\n\n**********************************"

    def test_init1(self):
        tcp_packet = "2f110100000100000000000006616d617a6f6e03636f6d0000010001"
        obj = dnsTLS()
        self.assertEqual(obj.getLength(tcp_packet), "001c")




    def test_init3(self):
        dns_reponse = "002e2f1181800001000100000000086c696e6b6564696e03636f6d0000010001c00c000100010000030b00046cae0a0a"
        obj = dnsTLS()
        self.assertEqual(obj.extractIp(dns_reponse), socket.gethostbyname("linkedin.com"))


    def test_init2(self):
        dns_reponse = "002e2f1181800001000100000000086c696e6b6564696e03636f6d0000010001c00c000100010000030b00046cae0a0a"
        obj = ThreadedServer('', 53)
        self.assertEqual(socket.gethostbyaddr(obj.resolve("google.com")), "google.com")


if __name__ == "__main__":
    unittest.main()
