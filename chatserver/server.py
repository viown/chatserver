from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor
from chatserver.protocol import ChatFactory

class ChatServer:
    def __init__(self):
        self.factory = ChatFactory()

    def add_plugin(self, plugin):
        self.factory.add_plugin(plugin)

    def run(self, port=8989):
        endpoint = TCP4ServerEndpoint(reactor, port)
        endpoint.listen(self.factory)
        reactor.run()