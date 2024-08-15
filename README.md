# chatserver

Everyone has got to write a chat server as a project at some point.

# Client

There is no official client written for this, but it's simple enough that you can connect over telnet:

```
$ telnet localhost 8999
 Trying ::1...
Connection failed: Connection refused
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
<system> Welcome to the chat room!
<system> You're not currently connected.
<system> Please enter a username:
mike
<system> Logging in as mike
<helperbot> mike has joined the chat room!
hello, I'm mike
<jacob> hi mike I'm jacob
screw you jacob
```

By default, you're added to the 'chat' room. Use the `/switch` command to switch to a new room. If that room does not exist, it will be created and you'll be set as an admin.

```
/switch cool_room
<system> Switched to room 'cool_room'
<helperbot> mike has joined the chat room!
/users
<helperbot> Current online users:
<helperbot> 1. mike (admin)
```

"helperbot" is an optional plugin located under `chatserver/plugins`. It offers some basic utility commands such as `/w` for whispering to users across rooms, moderation commands like `/kick` and `/ban`, `/rooms` for showing all available chat rooms on the server.

It's loaded onto the server like this:

```py
from chatserver.server import ChatServer
from chatserver.plugins.helperbot import HelperBot

if __name__ == "__main__":
    server = ChatServer()

    # Add HelperBot Plugin
    server.add_plugin(HelperBot)

    server.run(port=8999)
```

chatserver can be easily extended with your own plugin:

```py
from chatserver.plugins import Plugin
from statistics import stdev
import time

class HelloBot(Plugin):
    def __init__(self, rooms):
        self.name = "hellobot"
        self.commands = []

        super().__init__(rooms, self.name, self.commands)

    def on_message_received(self, author, message):
        if message.lower().startswith("hello"):
            self.reply(author, f"Hello, {author.name}")

    def on_command_received(self, author, command, *args):
        # Command must be added to `self.commands` to be captured here
        pass
```