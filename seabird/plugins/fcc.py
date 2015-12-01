from PyIRC.extensions import BaseExtension
from PyIRC.signal import event

import requests

FCC_URL = 'http://data.fcc.gov/api/license-view/basicSearch/getLicenses'

class FccPlugin(BaseExtension):
    requires = ['CommandMux']

    @event('seabird_command', 'call')
    def search_fcc(self, event, line, cmd, remainder):
        try:
            data = requests.get(FCC_URL, params={
                'format': 'json',
                'searchValue': remainder,
            }).json()
        except:
            self.base.mention_reply(line, 'Unable to get FCC callsigns')
            return

        try:
            license = data['Licenses']['License'][0]
            self.base.mention_reply(line, '{} ({}): {}, {}, expires {}'.format(
                license['callsign'], license['serviceDesc'], license['licName'],
                license['statusDesc'], license['expiredDate']))
        except KeyError:
            self.base.mention_reply(line, 'Unable to get FCC callsigns')
