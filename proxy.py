#!/usr/bin/env python

import socket, sys
from thread import *

try:
    listening_port=int(raw_input("[*] Enter Listening Port Number: "))
except KeyboardInterrupt:
    print ("\n[*] User Requested An Interrupt")
    print ("[*] Application Exiting ...")
    sys.exit()

max_conn = 10 #Max Connection Queues To Hold
buffer_size = 65535 # Max Socket Buffer Size

def start():
    try:
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('',listening_port)) # Bind Socket For Listen
        s.listen(max_conn) #Start Listening For Incoming Connections
        print ("[*] Initializing Sockets ... Done")
        print ("[*] Sockets Binded Successfully ...")
        print("[*] Server Started Successfully [ %d ]\n" % (listening_port))

    except Exception, e:
        #Execute This Block If Socket Anything Fails
        print ("[*] Unable To Initialize Socket")
        sys.exit(2)

    while 1:
        try:
            conn, addr=s.accept() #Accept connection from Client browser
            print("received connection from %s" % str(addr))

            data=conn.recv(buffer_size) #Receive Client data
            print("received data \n %s" % data)

            start_new_thread(conn_string,(conn,data,addr))
        except KeyboardInterrupt:
            #Execute This Block If Client Socket Failed
            s.close()
            print "\n[*] Proxy Server Shutting Down ..."
            print "[*] Have A Nice Day ...sir"
            sys.exit(1)

    s.close()

def conn_string(conn,data,addr):
    # Client Browser Request Appears here
    try:
        first_line=data.split('\n')[0]
        print("first_line \n %s" % first_line)
        url=first_line.split(' ')[1]
        print("url \n %s" % url)
        http_pos=url.find("://") #Find the posiiton of ://
        print("http_pos \n %s" % http_pos)

        if (http_pos==-1):
            temp=url
        else:
            temp=url[(http_pos+3):] #Get the rest of the url

        print("temp \n %s" % temp)

        port_pos=temp.find(":") #Find the pos of the port (if any)
        print("port_pos \n %s" % port_pos)

        webserver_pos=temp.find("/")
        if webserver_pos==-1:
            webserver_pos=len(temp)
        webserver=""
        port = -1

        if (port_pos==-1 or webserver_pos < port_pos):
            port=80
            webserver=temp[:webserver_pos]
        else:
            port=int((temp[(port_pos+1):])[:webserver_pos-port_pos-1])
            webserver=temp[:port_pos]

        print("webserver\n %s" % webserver)
        print("port\n %s" % port)
        proxy_server(webserver,port,conn,data,addr)

    except Exception, e:
        pass

def proxy_server(webserver,port,conn,data,addr):
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((webserver,port))
        s.send(data)

        while 1:
            #read reply or data to from end web server
            reply=s.recv(buffer_size)
            print("reply \n %s" % reply)

            if (len(reply) > 0):
                conn.send(reply) # Send reply back to Client

                'Print A custom message for request complete'
                print "[*] Request Done: %s => %s <=" % (str(addr[0]),str(dar))
            else:
                #Break the connection if receiving data Failed
                break
        #Feel Free To Close Our Server Sockets
        s.close()
        #Now that everything is sent, We may now close client socket
        conn.close()
    except socket.error, (value, message):
        s.close()
        conn.close()
        sys.exit(1)

start()
