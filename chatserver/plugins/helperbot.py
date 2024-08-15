from chatserver.plugins import Plugin

class HelperBot(Plugin):
    def __init__(self, rooms):
        self.name = "helperbot"
        self.commands = [
            "users",
            "kick",
            "ban",
            "w",
            "rooms"
        ]
        self.banned = {}

        super().__init__(rooms, self.name, self.commands)

    def on_user_join(self, user, room):
        if user.name in self.banned and room in self.banned[user.name]:
            user.switch_room('chat')
            self.reply(user, "You're banned from this room and cannot join. You've been returned to 'chat'")
            return
        self.broadcast(room, f"{user.name} has joined the chat room!")

    def on_user_leave(self, user, room):
        self.broadcast(room, f"{user.name} has left the chat room!")

    def on_message_received(self, author, message):
        if "helperbot" in message:
            self.reply(author, "that's me!")

    def on_command_received(self, author, command, *args):
        match command:
            case "users":
                self.reply(author, "Current online users:")

                for i, user in enumerate(self.rooms[author.room].keys()):
                    self.reply(author, f"{i+1}. {user}" + (" (admin)" if self.rooms[author.room][user].admin else ""))
            case "kick":
                if not author.admin:
                    self.reply(author, "You must be an admin to kick.")
                    return
                
                name = ' '.join(args)

                if name not in self.rooms[author.room]:
                    self.reply(author, "Could not find someone with that username.")
                    return
                
                user = self.rooms[author.room][name]

                user.switch_room('chat')
                self.reply(user, f"You've been kicked from the '{author.room}' room. You've been returned to 'chat'.")
            case "ban":
                if not author.admin:
                    self.reply(author, "You must be an admin to ban.")
                    return
                
                name = ' '.join(args)

                if name not in self.rooms[author.room]:
                    self.reply(author, "Could not find someone with that username.")
                    return
                
                user = self.rooms[author.room][name]

                if name not in self.banned:
                    self.banned[name] = [author.room]
                else:
                    self.banned[name].append(author.room)

                user.switch_room('chat')
                self.reply(user, f"You've been banned from the '{author.room}' room. You've been returned to 'chat'.")
            case "w":
                name = args[0]
                user = None

                for room in self.rooms:
                    for cuser in self.rooms[room].values():
                        if cuser.name == name:
                            user = cuser

                if not user:
                    self.reply(author, "Could not find someone with that username.")
                    return
                
                self.reply(user, f"{author.name} whispered to you: {' '.join(args[1:])}")
            case "rooms":
                self.reply(author, "Currently active rooms:")
                for i, room in enumerate(self.rooms):
                    self.reply(author, f"{i+1}. {room}")
                 