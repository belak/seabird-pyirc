from PyIRC.extensions import BaseExtension
from PyIRC.signal import event

class RandomPlugin(BaseExtension):
    @event("commands", "JOIN")
    def say_hi(self, _, line):
        basic_rfc = self.base.basic_rfc
        if self.casecmp(line.hostmask.nick, basic_rfc.nick):
            self.base.send('PRIVMSG', [line.params[0], 'Hi!'])
        else:
            self.base.send('PRIVMSG', [line.params[0], 'Hi %s!' % line.hostmask.nick])
