from chatserver.server import ChatServer
from chatserver.plugins.helperbot import HelperBot

if __name__ == "__main__":
    server = ChatServer(port=8999)

    # Add plugins
    server.add_plugin(HelperBot)

    server.run()