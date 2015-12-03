from PyIRC.extensions import BaseExtension
from PyIRC.signal import event

import requests

METAR_URL = 'http://weather.noaa.gov/pub/data/observations/metar/stations/' \
            '{}.TXT'


class MetarPlugin(BaseExtension):
    requires = ['CommandMux']

    @event('sb.command', 'metar')
    def get_metar(self, _, cmd):
        try:
            resp = requests.get(METAR_URL.format(cmd.remainder.upper()))
            if resp.status_code == 404:
                cmd.mention_reply('{} is not a valid METAR code'.format(
                    cmd.remainder))
                return

            resp.raise_for_status()
        except requests.RequestException:
            cmd.mention_reply('Unable to get METAR for {}'.format(
                cmd.remainder))
            return

        try:
            data = resp.text.split('\n')[1]
            cmd.mention_reply(data)
        except KeyError:
            cmd.mention_reply('Malformed METAR data for {}'.format(
                cmd.remainder))
