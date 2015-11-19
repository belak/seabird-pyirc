from PyIRC.extensions import bot_recommended
from PyIRC.formatting.pprint import PrettyPrintedIRCMixin 
from PyIRC.io.asyncio import IRCProtocol

# We need to make sure all plugins are imported so PyIRC can find all
# subclasses of BaseExtension.
from .random import RandomPlugin

from config import args


class SeabirdProtocol(IRCProtocol, PrettyPrintedIRCMixin):
    def __init__(self, **kwargs):
        # Update extensions to ensure we have bot_recommended and maybe add all
        # the seabird plugins if none are defined.
        extensions = kwargs.get('extensions', [
            'RandomPlugin'
        ])

        extensions = bot_recommended + extensions
        kwargs['extensions'] = extensions

        super().__init__(**kwargs)

    def reply(self, line, msg):
        # If the first param isn't the bot's nick, we should send it back to
        # the first param, as that will be the channel name.
        target = line.hostmask.nick
        if not self.casecmp(self.basic_rfc.nick, line.params[0]):
            target = line.params[0]

        self.send('PRIVMSG', [target, msg])

    def mention_reply(self, line, msg):
        if not self.casecmp(self.basic_rfc.nick, line.params[0]):
            msg = '%s: %s' % (line.hostmask.nick, msg)

        self.reply(line, msg)

