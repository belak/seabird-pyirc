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

    @event('sb.command', 'hello')
    def world(self, event, cmd):
        cmd.reply('World')

    @event('sb.command', 'coin')
    def coin(self, event, cmd):
        if cmd.private:
            cmd.reply('Must be used in a channel')
            return

        if not cmd.remainder in self.coin_names:
            self.basicapi.kick(cmd.reply_target, cmd.who, reason="That's not a valid coin side! Options are: %s" % ', '.join(self.coin_names))
            return

        if cmd.remainder == choice(self.coin_names):
            self.reply(line, 'Lucky guess!')
        else:
            self.basicapi.kick(cmd.reply_target, cmd.who, reason='Sorry! Better luck next time!')

    @event('sb.command', 'roulette')
    def roulette(self, event, line, cmd, remainder):
        if cmd.private:
            cmd.reply('Must be used in a channel')
            return

        shots_left = self.roulette_shots[cmd.reply_target]
        if shots_left < 1:
            cmd.reply('Reloading the gun.')
            shots_left = randint(1, self.roulette_max)

        shots_left -= 1
        if shots_left < 1:
            cmd.reply('BANG!')
            self.base.basicapi.kick(cmd.reply_target, cmd.who, reason='Tough luck, kid')
        else:
            cmd.reply('Click.')

        self.roulette_shots[cmd.reply_target] = shots_left
