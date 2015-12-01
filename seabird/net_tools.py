from PyIRC.extensions import BaseExtension
from PyIRC.signal import event

import requests
import socket
import subprocess

class NetToolsPlugin(BaseExtension):
    requires = ['CommandMux']

    @event('seabird_command', 'dig')
    def dig(self, event, line, cmd, remainder):
        # Port doesn't matter
        results = socket.getaddrinfo(remainder, 22)
        ipv6 = set()
        ipv4 = set()
        for res in results:
            family = res[0]
            ip = res[4][0]

            if family == socket.AF_INET:
                ipv4.add(ip)
            else:
                ipv6.add(ip)
        out = []
        for addrs in [ipv6, ipv4]:
            if addrs:
                out.append(', '.join(addrs))
        if out:
            self.base.mention_reply(line, '; '.join(out))
        else:
            self.base.mention_reply(line, 'Unable to find results for {}'.format(
                remainder))

    @event('seabird_command', 'rdns')
    def rdns(self, event, line, cmd, remainder):
        try:
            hostname, _, _ = socket.gethostbyaddr(remainder)
            self.base.mention_reply(line, hostname)
        except socket.herror:
            self.base.mention_reply(line, 'Unable to find results for {}'.format(
                remainder))

    @event('seabird_command', 'ping')
    def ping(self, event, line, cmd, remainder):
        # As always, the laziness runs deep
        try:
            out = subprocess.Popen(
                ["/bin/ping", "-c1", "-w5", remainder],
                stdout=subprocess.PIPE
            ).stdout.read()
            self.base.mention_reply(line, out.decode('ascii').split('\n')[1])
        except:
            self.base.mention_reply(line, 'Error pinging {}'.format(remainder))
