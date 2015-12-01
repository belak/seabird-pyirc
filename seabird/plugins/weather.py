from PyIRC.extensions import BaseExtension
from PyIRC.signal import event

import requests

from config import args

WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather'

class WeatherPlugin(BaseExtension):
    requires = ['CommandMux']

    def _kelvinToFahrenheit(self, temp):
        return 1.8 * (float(temp) - 273.15) + 32

    @event('seabird_command', 'weather')
    def get_weather(self, event, line, cmd, remainder):
        try:
            resp = requests.get(WEATHER_URL, params={
                'zip': '{},us'.format(remainder),
                'APPID': args['weather']['api_key'],
            })
        except:
            self.base.mention_reply(line, 'Unable to get weather for {}'.format(
                remainder))
            return

        if resp.status_code != 200:
            self.base.mention_reply(line, '{} is not a valid zipcode'.format(
                remainder))
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

            self.base.mention_reply(line, '{}: {:.2f} with a high of {:.2f} '
                'and low of {:.2f}{}.'.format(
                    data['name'],
                    self._kelvinToFahrenheit(data['main']['temp']),
                    self._kelvinToFahrenheit(data['main']['temp_max']),
                    self._kelvinToFahrenheit(data['main']['temp_min']),
                    desc))
        except:
            self.base.mention_reply(line, 'Got malformed weather response')
