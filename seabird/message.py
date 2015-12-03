class SeabirdMessage:
    def __init__(self, proto, line):
        self.proto = proto

        self.line = line
        self.trailing = line.params[-1]

        # Who the message is from
        self.who = self.line.hostmask.nick

        # If the message target is the bot's name, we know it's a pm
        if self.proto.casecmp(line.params[0], self.proto.basic_rfc.nick):
            self.private = True
            self.reply_target = self.line.hostmask.nick
        else:
            self.private = False
            self.reply_target = self.line.params[0]

    def reply(self, message):
        self.proto.send("PRIVMSG", [self.reply_target, message])

    def mention_reply(self, message):
        # If it's not private, we need to prepend the user's nick.
        if not self.private:
            message = '%s: %s' % (self.who, message)

        self.reply(message)
