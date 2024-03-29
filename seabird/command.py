from PyIRC.signal import event
from PyIRC.extensions import BaseExtension

from .message import SeabirdMessage


class SeabirdCommand(SeabirdMessage):
    def __init__(self, proto, prefix, line):
        super().__init__(proto, line)

        # Split into 3 parts on the space, then unpack the tuple.
        result = self.trailing[len(prefix):].partition(' ')
        self.cmd, _, self.remainder = result


class CommandMux(BaseExtension):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.prefix = kwargs.pop('command_prefix', '!')

    @event('commands', 'PRIVMSG')
    def privmsg(self, _, line):
        trailing = line.params[-1]
        if not trailing.startswith(self.prefix):
            return

        cmd = SeabirdCommand(self.base, self.prefix, line)

        # Call the event. Each command should have the following signature:
        # def cmd(event, cmd)
        self.call_event('sb.command', cmd.cmd, cmd)
