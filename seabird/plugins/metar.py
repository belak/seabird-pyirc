from PyIRC.extensions import BaseExtension
from PyIRC.signal import event

import requests

METAR_URL = 'http://weather.noaa.gov/pub/data/observations/metar/stations/' \
            '{}.TXT'


class MetarPlugin(BaseExtension):
    requires = ['CommandMux']

    @event('sb.command', 'metar')
    def get_metar(self, event, line, cmd, remainder):
        try:
            resp = requests.get(METAR_URL.format(remainder.upper()))
            if resp.status_code == 404:
                cmd.mention_reply('{} is not a valid METAR code'.format(
                    cmd.remainder))
                return

            resp.raise_for_status()
        except:
            cmd.mention_reply('Unable to get METAR for {}'.format(
                cmd.remainder))
            return

        try:
            data = resp.text.split('\n')[1]
            cmd.mention_reply(data)
        except:
            cmd.mention_reply('Malformed METAR data for {}'.format(
                cmd.remainder))
