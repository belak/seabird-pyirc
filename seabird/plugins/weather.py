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
            cmd.mention_reply('Unable to get weather for {}'.format(cmd.remainder))
            return

        if resp.status_code != 200:
            cmd.mention_reply('{} is not a valid zipcode'.format(cmd.remainder))
            return

        try:
            data = resp.json()

            # Once again, I am terribly lazy
            desc = ''
            try:
                desc = '. {}'.format(data['weather'][0]['description'])
            except:
                # No description here
                pass

            cmd.mention_reply('{}: {:.2f} with a high of {:.2f} '
                'and low of {:.2f}{}.'.format(
                    data['name'],
                    self._kelvinToFahrenheit(data['main']['temp']),
                    self._kelvinToFahrenheit(data['main']['temp_max']),
                    self._kelvinToFahrenheit(data['main']['temp_min']),
                    desc))
        except:
            cmd.mention_reply('Got malformed weather response')
