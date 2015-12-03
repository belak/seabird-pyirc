from PyIRC.extensions import BaseExtension
from PyIRC.signal import event

from random import randint
import re


class DicePlugin(BaseExtension):
    requires = ['CommandMux']

    @event('commands', 'PRIVMSG')
    def roll_dice(self, event, line):
        """Looks for strings like "3d6" in strings to roll
        As it looks in every string, it doesn't notify users on
        error.
        """
        matches = re.findall(r'\b(\d+)d(\d+)\b', line.params[-1])
        # My laziness knows no bounds
        for num_dice, dice_magnitude in [(int(n), int(d)) for n, d in matches]:
            if num_dice < 1 or num_dice > 100:
                # Too many dice
                pass
            if dice_magnitude < 2 or dice_magnitude > 100:
                # Too much die
                pass

            rolls = ['{}d{}:'.format(num_dice, dice_magnitude)]
            for i in range(num_dice):
                rolls.append(str(randint(1, dice_magnitude)))
            self.base.mention_reply(line, ' '.join(rolls))
