import asyncio

import aiohttp

from PyIRC.extensions import BaseExtension
from PyIRC.signal import event

METAR_URL = 'http://weather.noaa.gov/pub/data/observations/metar/stations/' \
            '{}.TXT'


class MetarPlugin(BaseExtension):
    requires = ['CommandMux']

    @event('sb.command', 'metar')
    def get_metar(self, _, cmd):
        loop = asyncio.get_event_loop()
        loop.create_task(self.metar_callback(cmd))

    async def metar_callback(self, cmd):
        resp = await aiohttp.get(METAR_URL.format(cmd.remainder.upper()))
        if resp.status == 404:
            cmd.mention_reply('{} is not a valid METAR code'.format(
                cmd.remainder))
            return
        elif resp.status != 200:
            cmd.mention_reply('Unable to get METAR for {}'.format(
                cmd.remainder))
            return

        try:
            data = await resp.text()
            cmd.mention_reply(data.split('\n')[1])
        except KeyError:
            cmd.mention_reply('Malformed METAR data for {}'.format(
                cmd.remainder))
