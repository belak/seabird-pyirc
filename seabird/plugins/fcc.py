from PyIRC.extensions import BaseExtension
from PyIRC.signal import event

import requests

FCC_URL = 'http://data.fcc.gov/api/license-view/basicSearch/getLicenses'


class FccPlugin(BaseExtension):
    requires = ['CommandMux']

    @event('sb.command', 'call')
    def search_fcc(self, event, cmd):
        try:
            data = requests.get(FCC_URL, params={
                'format': 'json',
                'searchValue': cmd.remainder,
            }).json()
        except:
            cmd.mention_reply('Unable to get FCC callsigns')
            return

        try:
            license = data['Licenses']['License'][0]
            cmd.mention_reply('{} ({}): {}, {}, expires {}'.format(
                license['callsign'], license['serviceDesc'],
                license['licName'], license['statusDesc'],
                license['expiredDate']))
        except KeyError:
            cmd.mention_reply('Unable to get FCC callsigns')
