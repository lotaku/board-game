from SocketServer import UDPServer, \
        DatagramRequestHandler, \
        ForkingMixIn, \
        BaseRequestHandler #, ForkingUDPServer
import struct
#class boardGameRequestHandler(BaseRequestHandler):
class boardGameRequestHandler(BaseRequestHandler):
    def handle(self):
            receivedData = self.request[0].strip()
            socket = self.request[1]
            unpackedreceivedData = struct.unpack('!3s',receivedData)
            print "{} wrote:".format(self.client_address[0])
            print "Wellcome {}.".format(unpackedreceivedData)
            #socket.sendto(data.upper(), self.client_address)
            respondedData = 'True'
            #respondedDataPacked = struct
            socket.sendto(struct.pack('!4s', respondedData), self.client_address)

class boardGameServer(UDPServer):
#class boardGameServer(ForkingMixIn, UDPServer):
    allow_reuse_address = 1

if __name__ == "__main__":
    serveraddr = ('', 51423)
    server =  boardGameServer(serveraddr,boardGameRequestHandler)
    server.serve_forever()

