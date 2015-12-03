from PyIRC.extensions import BaseExtension
from PyIRC.signal import event

import requests

from config import args

WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather'


class WeatherPlugin(BaseExtension):
    requires = ['CommandMux']

    def _kelvinToFahrenheit(self, temp):
        return 1.8 * (float(temp) - 273.15) + 32

    @event('sb.command', 'weather')
    def get_weather(self, event, cmd):
        try:
            resp = requests.get(WEATHER_URL, params={
                'zip': '{},us'.format(cmd.remainder),
                'APPID': args['weather']['api_key'],
            })
        except:
            cmd.mention_reply('Unable to get weather for {}'.format(
                cmd.remainder))
            return

        if resp.status_code != 200:
            cmd.mention_reply('{} is not a valid zipcode'.format(
                cmd.remainder))
            return

        try:
            data = resp.json()

            format_args = {
                'name':     data['name'],
                'temp':     self._kelvinToFahrenheit(data['main']['temp']),
                'temp_max': self._kelvinToFahrenheit(data['main']['temp_max']),
                'temp_min': self._kelvinToFahrenheit(data['main']['temp_min']),
                'desc':     '',
            }

            try:
                format_args['desc'] = '. {}'.format(
                    data['weather'][0]['description'])
            except:
                pass

            cmd.mention_reply('{name}: {temp:.2f} with a high of '
                              '{temp_max:.2f} and low of '
                              '{temp_min:.2f}{desc}.'.format(**format_args))
        except:
            cmd.mention_reply('Got malformed weather response')
