from twisted.internet.protocol import Protocol, Factory

class Chat(Protocol):
    def __init__(self, rooms, plugins):
        self.rooms = rooms
        self.plugins = plugins
        self.room = None
        self.name = None
        self.is_connected = False
        self.admin = False

    def write_message(self, message):
        self.transport.write(bytes(message, 'utf-8'))

    def write_system_message(self, message, end='\n'):
        self.write_message(f"<system> {message}{end}")

    def send_message(self, message):
        if len(message) > 450:
            self.write_system_message("Message cannot exceed 450 characters.")
            return
        
        for user in self.rooms[self.room].values():
            if user != self:
                user.write_message(f"<{self.name}> {message}\n")

    def switch_room(self, new_room):
        created = False

        old_room = self.room

        if new_room not in self.rooms:
            self.rooms[new_room] = {}
            created = True
        
        if self.room and self.name in self.rooms[self.room]:
            del self.rooms[self.room][self.name]

        self.rooms[new_room][self.name] = self
        self.room = new_room
        self.admin = created

        for plugin in self.plugins:
            plugin.on_user_leave(self, old_room)
        for plugin in self.plugins:
            plugin.on_user_join(self, self.room)

    def handle_command(self, command, *args):
        match command:
            case "leave":
                self.write_system_message("Leaving chat room.")
                self.transport.loseConnection()
            case "room":
                self.write_system_message(f"You're currently in the '{self.room}' room.")
            case "switch":
                if len(args) == 0:
                    self.write_system_message("Please specify a room to switch to.")
                    return
                room = ' '.join(args)
                self.write_system_message(f"Switched to room '{room}'")
                self.switch_room(room)
            case "help":
                message = "\n"
                message += "\tsystem:\n"
                for i, command in enumerate(["leave", "room", "switch"]):
                    message += f"\t\t{i+1}. /{command}\n"
                for i, plugin in enumerate(self.plugins):
                    message += f"\t{plugin.name}:\n"
                    for i, command in enumerate(plugin.commands):
                        message += f"\t\t{i+1}. /{command}\n"
                self.write_system_message(message)
            case _:
                for plugin in self.plugins:
                    if command in plugin.commands:
                        plugin.on_command_received(self, command, *args)
                        return
                self.write_system_message("Command not found.")

    def handle_login(self, username):
        if len(username) > 20:
            self.write_system_message("Username must be less than 20 characters.")
            return
        
        # Username cannot be used in any room
        for room in self.rooms:
            if username in self.rooms[room]:
                self.write_system_message("That username is already taken, please try another one.")
                return

        self.write_system_message(f"Logging in as {username}")
        self.name = username
        self.is_connected = True
        self.rooms['chat'][self.name] = self
        self.room = 'chat'

        for plugin in self.plugins:
            plugin.on_user_join(self, self.room)

    def connectionMade(self):
        self.write_system_message("Welcome to the chat room!")
        self.write_system_message("You're not currently connected.")
        self.write_system_message("Please enter a username:")

    def connectionLost(self, reason):
        if not self.is_connected:
            return
        if self.name in self.rooms[self.room]:
            del self.rooms[self.room][self.name]
            
            for plugin in self.plugins:
                plugin.on_user_leave(self, self.room)

    def dataReceived(self, data):
        message = data.decode("utf-8").strip()

        if message == "":
            return

        if not self.is_connected:
            self.handle_login(message)
        else:
            if message.startswith('/'):
                command_data = message.split(' ')
                command_data[0] = command_data[0][1:]
                self.handle_command(command_data[0].lower(), *command_data[1:])
            else:
                self.send_message(message)
                for plugin in self.plugins:
                    plugin.on_message_received(self, message)


class ChatFactory(Factory):
    def __init__(self):
        self.rooms = {
            "chat": {}
        }
        self.plugins = []

    def add_plugin(self, plugin):
        self.plugins.append(plugin(self.rooms))

    def buildProtocol(self, addr):
        return Chat(self.rooms, self.plugins)