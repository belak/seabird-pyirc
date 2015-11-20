from PyIRC.extensions import bot_recommended, BaseExtension
from PyIRC.formatting.pprint import PrettyPrintedIRCMixin
from PyIRC.io.asyncio import IRCProtocol
from PyIRC.util.classutil import get_all_subclasses

# We need to make sure all plugins are imported so PyIRC can find all
# subclasses of BaseExtension.
from .command import CommandMux
from .random import RandomPlugin
from .fcc import FccPlugin

from config import args


class SeabirdProtocol(IRCProtocol, PrettyPrintedIRCMixin):
    def __init__(self, **kwargs):
        # Update extensions to ensure we have bot_recommended and maybe add all
        # the seabird plugins if none are defined.
        extensions = kwargs.get('extensions')
        if not extensions:
            extensions = []
            for cls in get_all_subclasses(BaseExtension):
                if not cls.__module__.startswith('seabird.'):
                    continue

                extensions.append(cls.__name__)

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

