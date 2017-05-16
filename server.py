# This networking code has been written in order to simplify the creation 
# of your tictactoe games. You are free to use it but you must report if 
# you used this code instead of writting your own inside your group report
# and you must leave this header intact.
# David

import time, socket, select

class Server:
    def __init__(self, port=12346):
        self.__connections = {}
        self.__port = port

        self.__server = socket.socket()     # Create a socket object
        self.__uid = 0                      # uid is a unique number to give to each client

        self.__server.bind(('', self.__port))      # Bind to the port
        self.__server.listen(5)             # Now wait for client connection.

    def port(self):
        """ returns the port that the server is running on """
        return self.__port

    def shutdown(self):
        """ make sure you call this before your program exits """

        for c, data in self.__connections.items():
            data["socket"].close()

        self.__server.shutdown(1)
        self.__server.close()

    def num_clients(self):
        """ return the number of clients currently connected """
        
        return len(self.__connections)

    def send_message(self, msg, client=None):
        """ schedule a message to be sent next time poll() is run
            if no client is supplied then message will be sent to all connected clients """

        if client == None:
            for c in self.__connections:
                self.__connections[c]['sendbuffer'].append(msg)

        elif client in self.__connections:
            self.__connections[client]['sendbuffer'].append(msg)

        else:
            raise self.Client('No such client')

    def __list_of_sockets(self):
        """ return a list of all the open client connections """

        return [ self.__connections[i]['socket'] for i in self.__connections ]

    def poll(self):
        """ must be called reguarly, accepts new connections, handles dicsonnections, sent scheduled messages and 
            recieves new messages.
            returns 3 lists, messages recieved, new clients and disconnected clients """

        connections = self.__list_of_sockets()
        read, write, error = select.select( connections+[self.__server], connections, connections, 0 )

        messages, connected, disconnected = [], [], []

        # ====== process all the connections that had errors ======
        for conn in error:
            print( "error", conn )

        # ====== process all the connections that we are able to send data to ===
        for uid, data in self.__connections.items():
            if data['socket'] in write: # if this is a socket that is ready to get some data
                while data['sendbuffer'] != []: # while we have some data to send
                    msg = data['sendbuffer'][0]

                    try:
                        data['socket'].send( "{}\n".format(msg).encode('utf8') )
                        data['sendbuffer'].pop(0)
                    except:
                        break

        # ====== process all the connections that are trying to send us data ===
        for conn in read:
            if conn is self.__server:                       # new client connecting
                c, addr = conn.accept()
                
                self.__connections[self.__uid] = {'socket':c, 'address':addr, 'sendbuffer':[], 'recvbuffer':""}  # add to list of open self.__connections
                connected.append(self.__uid)
                self.__uid += 1

            else:
                msgbytes = conn.recv(1024)

                for uid, data in self.__connections.items():
                    if data['socket'] == conn:
                        if not msgbytes:                # treat empty message as a disconnection
                            disconnected.append( uid )

                        else:
                            """ for everything else only consider a message complete once a newline character has been recieved """
                            data['recvbuffer'] += msgbytes.decode('utf8')

                            msgs = data['recvbuffer'].split('\n')
                            for msg in msgs[:-1]:
                                messages.append( (uid,msg) )

                            data['recvbuffer'] = msgs[-1]

                        break

        # ====== remove any clients that have disconnected from the connections store ===
        for uid in disconnected:
            self.__connections[uid]["socket"].close()
            self.__connections.pop(uid)

        return messages, connected, disconnected

if __name__ == '__main__':
    s = Server()

    try:
        print( "Server running on port {}".format( s.port() ) )

        while True:
            messages, connected, disconnected = s.poll()

            for client, message in messages:                
                if (message[0:15] == "SENDING X VALUE"):
                    print( "Client {} sent \"{}\"".format( client, message ) )
                    s.send_message("Server received X Value from client " + str(client) + " for button " + message[27:28])
                    s.poll()
                elif (message[0:15] == "SENDING O VALUE"):
                    print( "Client {} sent \"{}\"".format( client, message ) )
                    s.send_message("Server received O Value from client " + str(client) + " for button " + message[27:28])
                    s.poll()
            
            for client in connected:
                print( "Client {} connected".format(client) )
                s.send_message( "Hello client {}".format(client) )

            for client in disconnected:
                print( "Client {} disconnected".format(client) )
                        
            time.sleep(1)

    except KeyboardInterrupt:
        pass

    finally:
        print( "Shutdown" )
        s.shutdown()