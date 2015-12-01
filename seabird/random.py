from PyIRC.casemapping import IRCDefaultDict
from PyIRC.extensions import BaseExtension
from PyIRC.signal import event

from random import randint, choice

class RandomPlugin(BaseExtension):
    requires = ['CommandMux']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.roulette_shots = IRCDefaultDict(self.base.case, lambda: 0)
        self.roulette_max = 6

        self.coin_names = ["heads", "tails"]

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

    @event('seabird_command', 'coin')
    def coin(self, event, line, cmd, remainder):
        basic_rfc = self.base.basic_rfc
        if not self.casecmp(line.hostmask.nick, basic_rfc.nick):
            self.reply(line, 'Must be used in a channel')
            return

        if not remainder in self.coin_names:
            self.basicapi.kick(line.params[0], line.hostmask.nick, reason="That's not a valid coin side! Options are: %s" % ', '.join(self.coin_names))

        if remainder == choice(self.coin_names):
            self.reply(line, 'Lucky guess!')
        else:
            self.basicapi.kick(line.params[0], line.hostmask.nick, reason='Sorry! Better luck next time!')

    @event('seabird_command', 'roulette')
    def roulette(self, event, line, cmd, remainder):
        basic_rfc = self.base.basic_rfc
        if not self.casecmp(line.hostmask.nick, basic_rfc.nick):
            self.reply(line, 'Must be used in a channel')
            return

        shots_left = self.roulette_shots[line.params[0]]
        if shots_left < 1:
            self.reply(line, 'Reloading the gun.')
            shots_left = randint(1, self.roulette_max)

        shots_left -= 1
        if shots_left < 1:
            self.reply(line, 'BANG!')
            self.base.basicapi.kick(line.params[0], line.hostmask.nick, reason='Tough luck, kid')
        else:
            self.reply(line, 'Click.')

        self.roulette_shots[line.params[0]] = shots_left
