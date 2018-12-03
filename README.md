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





