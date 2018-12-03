# DNS-OVER-DNS
##TLS OVER DNS written in python
This is a python  app which can establish DNS conn over TLS .It Follows https://tools.ietf.org/html/rfc7858 and uses cloudfare 1.1.1.1 DNS Server

     
     
     To run ** 
              - docker build -t tlsdns .
              - sudo docker run -d -p 53:53 tlsdns
               **
              
     How to Test ?
           Run python client.py outside docker container 
      
            ##sample Test cases #### - python test.py




>>> What are the security concerns for this kind of service?

<<< We could add the encrypt data from locally , with our digital cert ,and the data retrieved can be decrypted by the client's private key . (Just a thought !)
>>> Considering a microservice architecture; how would you see this the dns to
dns-over-tls proxy used? 

<<< There can be a microservice which will listen on port 53 DNS . It can listen for all the incoming traffic .It can act as Cache and incase of cache misse it  redirect it to another  TCP  Micro Service (port 853) which will   establishes  a TLS  connection and retrieve the record and stores in Cache with specified TTL

>>What other improvements do you think would be interesting to add to the project? 

<<< Better handling incase of roundrobin dns , CNAMES and other DNS queries for  AXFR,MX etc  Add caches , ADD UDP Supports , Inplace metrics .
