from PyIRC.extensions import BaseExtension
from PyIRC.signal import event

class RandomPlugin(BaseExtension):
    requires = ['CommandMux']

    @event("commands", "JOIN")
    def say_hi(self, _, line):
        basic_rfc = self.base.basic_rfc
        if self.casecmp(line.hostmask.nick, basic_rfc.nick):
            self.base.reply(line, 'Hi!')
        else:
            self.base.reply(line, 'Hi %s!' % line.hostmask.nick)

    @event('seabird_command', 'hello')
    def world(self, event, line, cmd, remainder):
        self.base.mention_reply(line, 'World')
