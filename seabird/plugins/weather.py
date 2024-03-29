import asyncio
from json import JSONDecodeError

import aiohttp

from PyIRC.extensions import BaseExtension
from PyIRC.signal import event

WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather'


def kelvin_to_fahrenheit(temp):
    return 1.8 * (float(temp) - 273.15) + 32


class WeatherPlugin(BaseExtension):
    requires = ['CommandMux']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_key = kwargs['weather_api_key']

    @event('sb.command', 'weather')
    def get_weather(self, _, cmd):
        loop = asyncio.get_event_loop()
        loop.create_task(self.weather_callback(cmd))

    async def weather_callback(self, cmd):
        resp = await aiohttp.get(WEATHER_URL, params={
            'zip': '{},us'.format(cmd.remainder),
            'APPID': self.api_key,
        })

        if resp.status != 200:
            cmd.mention_reply('Unable to get weather for {}'.format(
                cmd.remainder))
            return

        try:
            data = resp.json()
            if data['cod'] != 200:
                cmd.mention_reply('{} is not a valid zipcode'.format(
                    cmd.remainder))
                return

            format_args = {
                'name':     data['name'],
                'temp':     kelvin_to_fahrenheit(data['main']['temp']),
                'temp_max': kelvin_to_fahrenheit(data['main']['temp_max']),
                'temp_min': kelvin_to_fahrenheit(data['main']['temp_min']),
                'desc':     '',
            }

            try:
                format_args['desc'] = '. {}'.format(
                    data['weather'][0]['description'])
            except KeyError:
                pass

            cmd.mention_reply('{name}: {temp:.2f} with a high of '
                              '{temp_max:.2f} and low of '
                              '{temp_min:.2f}{desc}.'.format(**format_args))
        except (ValueError, JSONDecodeError):
            cmd.mention_reply('Got malformed weather response')
