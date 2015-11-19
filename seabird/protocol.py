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

