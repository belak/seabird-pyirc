from PyIRC.extensions import BaseExtension
from PyIRC.signal import event

import requests

METAR_URL = 'http://weather.noaa.gov/pub/data/observations/metar/stations/' \
    '{}.TXT'

class MetarPlugin(BaseExtension):
    requires = ['CommandMux']

    @event('seabird_command', 'metar')
    def get_metar(self, event, line, cmd, remainder):
        try:
            resp = requests.get(METAR_URL.format(remainder.upper()))
        except:
            self.base.mention_reply(line, 'Unable to get METAR for {}'.format(
                remainder))
            return

        if resp.status_code != 200:
            self.base.mention_reply(line, '{} is not a valid METAR code'.format(
                remainder))
            return

        try:
            data = resp.text.split('\n')[1]
            self.base.mention_reply(line, data)
        except:
            self.base.mention_reply(line, 'Malformed METAR data for {}'.format(
                remainder))
