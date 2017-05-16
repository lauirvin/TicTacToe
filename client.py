# This networking code has been written in order to simplify the creation 
# of your tictactoe games. You are free to use it but you must report if 
# you used this code instead of writting your own inside your group report
# and you must leave this header intact.
# David

import socket, select, sys, time

class AlreadyConnected(Exception):
    pass

class NotConnected(Exception):
    pass

class Client:
    def __init__(self, host = None, port=12346):
        if host == None:
            host = input("Enter IP: ")

        self.__host = host
        self.__port = port
        
        self.client = None
        self.connect()

    def connect(self):
        """ connect to the server, client will automatically attempt to connect when created anyway """

        if self.connected(): raise AlreadyConnected()

        self.__sendbuffer = []
        self.__recvbuffer = ""

        self.client = socket.socket()         # Create a socket object
        self.client.connect((self.__host,self.__port))   # Bind to the port

    def connected(self):
        """ returns if the client is connected to the server """

        return self.client != None

    def shutdown(self):
        """ shutdown the connections cleanly """
        
        if not self.connected(): return 

        self.client.close()
        self.client = None
        self.__recvbuffer = ""

    def send_message(self, msg):
        """ queue a message to be sent the text time poll() is called """

        self.__sendbuffer.append(msg)

    def poll(self):
        """ send all the queued messages, recieve the new messages, handle network issues """

        if not self.connected(): raise NotConnected() 

        read, write, error = select.select( [self.client], [self.client], [self.client], 0 )

        messages = []

        # list of sockets that have had errors
        if error != []:
            pass

        try:
            # go through the list of sockets that are ready to recieve data
            if write != []:
                while len(self.__sendbuffer) != 0:
                    msg = self.__sendbuffer[0]

                    self.client.send( "{}\n".format(msg).encode('utf8') )
                    self.__sendbuffer.pop(0)

            # socket has data to read
            if read != []:
                msg = self.client.recv(1024)

                if len(msg) == 0:      # empty message means client disconnection
                    self.client.close()
                    raise ConnectionResetError()

                else:
                    self.__recvbuffer += msg.decode('utf8')

                    msgs = self.__recvbuffer.split('\n')
                    messages = msgs[:-1]
                    self.__recvbuffer = msgs[-1]
            
        except ConnectionResetError:
            self.shutdown()

        return messages