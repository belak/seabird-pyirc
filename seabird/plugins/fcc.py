import asyncio
from json import JSONDecodeError

import aiohttp

from PyIRC.extensions import BaseExtension
from PyIRC.signal import event

FCC_URL = 'http://data.fcc.gov/api/license-view/basicSearch/getLicenses'


class FCCPlugin(BaseExtension):
    requires = ['CommandMux']

    @event('sb.command', 'call')
    def search_fcc(self, _, cmd):
        loop = asyncio.get_event_loop()
        loop.create_task(self.fcc_callback(cmd))

    async def fcc_callback(self, cmd):
        resp = await aiohttp.get(FCC_URL, params={
            'format': 'json',
            'searchValue': cmd.remainder,
        })

        if resp.status != 200:
            cmd.mention_reply('Unable to get FCC callsigns')
            return

        try:
            data = resp.json()
            license_data = data['Licenses']['License'][0]
            cmd.mention_reply('{} ({}): {}, {}, expires {}'.format(
                license_data['callsign'], license_data['serviceDesc'],
                license_data['licName'], license_data['statusDesc'],
                license_data['expiredDate']))
        except (KeyError, JSONDecodeError):
            cmd.mention_reply('Unable to get FCC callsigns')
