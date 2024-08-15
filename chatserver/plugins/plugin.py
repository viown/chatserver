class Plugin:
    def __init__(self, rooms, name, commands):
        self.rooms = rooms
        self.name = name
        self.commands = commands

    def reply(self, author, message, end='\n'):
        author.write_message(f"<{self.name}> {message}{end}")

    def broadcast(self, room, message, end='\n'):
        for user in self.rooms[room].values():
            user.write_message(f"<{self.name}> {message}{end}")

    def on_user_join(self, user, room):
        """
        Called when a user joins the chat room.
        """
        pass

    def on_user_leave(self, user, room):
        """
        Called when a user leaves the chat room.
        """
        pass

    def on_message_received(self, author, message):
        """
        Called when a message is sent (does not include commands).
        """
        pass

    def on_command_received(self, author, command, *args):
        """
        Called when a command registered in self.commands is received
        """
        pass