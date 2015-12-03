# pylint: disable=abstract-method
from pkgutil import iter_modules

from PyIRC.extensions import bot_recommended, BaseExtension
from PyIRC.formatting.pprint import PrettyPrintedIRCMixin
from PyIRC.io.asyncio import IRCProtocol
from PyIRC.util.classutil import get_all_subclasses

# NOTE: All modules that are valid in the extensions config value need to be
# imported so they can be found by the get_all_subclasses method.

# Helper extensions. These need to be imported here because they're a part of
# core, but still need to find them with get_all_subclasses. They have noqa on
# them because we don't actually use them in this file.
from .db import Database         # noqa # pylint: disable=unused-import
from .command import CommandMux  # noqa # pylint: disable=unused-import

from . import plugins


class SeabirdProtocol(IRCProtocol, PrettyPrintedIRCMixin):
    def __init__(self, **kwargs):
        # Iterate over all packages in the plugins submodule so
        # get_all_subclasses can find all the plugins in there.
        for _, name, _ in iter_modules(plugins.__path__, 'seabird.plugins.'):
            __import__(name)

        # Update extensions to ensure we have bot_recommended and maybe add all
        # the seabird plugins if none are defined.
        extensions = kwargs.get('extensions')
        if not extensions:
            extensions = []
            for cls in get_all_subclasses(BaseExtension):
                if not cls.__module__.startswith('seabird.plugins.'):
                    continue

                extensions.append(cls.__name__)

        extensions = bot_recommended + extensions
        kwargs['extensions'] = extensions

        super().__init__(**kwargs)

    def reply(self, line, msg):
        # If the first param isn't the bot's nick, we should send it back to
        # the first param, as that will be the channel name.
        target = line.hostmask.nick

        basic_rfc = self.get_extension('BasicRFC')
        if not self.casecmp(basic_rfc.nick, line.params[0]):
            target = line.params[0]

        self.send('PRIVMSG', [target, msg])

    def mention_reply(self, line, msg):
        basic_rfc = self.get_extension('BasicRFC')
        if not self.casecmp(basic_rfc.nick, line.params[0]):
            msg = '%s: %s' % (line.hostmask.nick, msg)

        self.reply(line, msg)
