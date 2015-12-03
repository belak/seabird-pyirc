from PyIRC.extensions import BaseExtension
from PyIRC.signal import event

import requests

FCC_URL = 'http://data.fcc.gov/api/license-view/basicSearch/getLicenses'


class FccPlugin(BaseExtension):
    requires = ['CommandMux']

    @event('sb.command', 'call')
    def search_fcc(self, _, cmd):
        try:
            resp = requests.get(FCC_URL, params={
                'format': 'json',
                'searchValue': cmd.remainder,
            })
            resp.raise_for_status()
            data = resp.json()
        except (requests.RequestException, ValueError):
            cmd.mention_reply('Unable to get FCC callsigns')
            return

        try:
            license_data = data['Licenses']['License'][0]
            cmd.mention_reply('{} ({}): {}, {}, expires {}'.format(
                license_data['callsign'], license_data['serviceDesc'],
                license_data['licName'], license_data['statusDesc'],
                license_data['expiredDate']))
        except KeyError:
            cmd.mention_reply('Unable to get FCC callsigns')
