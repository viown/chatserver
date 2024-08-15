from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor
from chatserver.protocol import ChatFactory

class ChatServer:
    def __init__(self, port):
        self.port = port or 8999
        self.endpoint = TCP4ServerEndpoint(reactor, self.port)
        self.factory = ChatFactory()

    def add_plugin(self, plugin):
        self.factory.add_plugin(plugin)

    def run(self):
        self.endpoint.listen(self.factory)
        reactor.run()