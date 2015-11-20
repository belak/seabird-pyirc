from PyIRC.signal import event
from PyIRC.extensions import BaseExtension


# TODO: This is a temporary class which will just emit a seabird_command event
# for each event that comes in. This should be expanded to include support for
# !help and other such conveniences.
class CommandMux(BaseExtension):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.prefix = kwargs.pop('command_prefix', '!')

    @event('commands', 'PRIVMSG')
    def privmsg(self, _, line):
        trailing = line.params[-1]
        if not trailing.startswith(self.prefix):
            return

        cmd, _, remainder = trailing[len(self.prefix):].partition(' ')

        # Call the event. Each command should have the following signature:
        # def cmd(event, line, cmd, remainder)
        #
        # Note that even though they registered this to get a callback using
        # seabird_command, it's possible to register different commands to the
        # same named callback, so we need to pass it in as an arg.
        self.call_event('seabird_command', cmd, line, cmd, remainder)
