from PyIRC.extensions import BaseExtension
from PyIRC.signal import event

class RandomPlugin(BaseExtension):
    @event("commands", "JOIN")
    def say_hi(self, _, line):
        basic_rfc = self.base.basic_rfc
        if self.casecmp(line.hostmask.nick, basic_rfc.nick):
            self.base.reply(line, 'Hi!')
        else:
            self.base.reply(line, 'Hi %s!' % line.hostmask.nick)
