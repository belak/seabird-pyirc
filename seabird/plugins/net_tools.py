from PyIRC.extensions import BaseExtension
from PyIRC.signal import event

import socket
import subprocess


class NetToolsPlugin(BaseExtension):
    requires = ['CommandMux']

    @event('sb.command', 'dig')
    def dig(self, _, cmd):
        # Port doesn't matter
        results = socket.getaddrinfo(cmd.remainder, 22)
        ipv6 = set()
        ipv4 = set()
        for res in results:
            family = res[0]
            res_ip = res[4][0]

            if family == socket.AF_INET:
                ipv4.add(res_ip)
            else:
                ipv6.add(res_ip)
        out = []
        for addrs in [ipv6, ipv4]:
            if addrs:
                out.append(', '.join(addrs))
        if out:
            cmd.mention_reply('; '.join(out))
        else:
            cmd.mention_reply('Unable to find results for {}'.format(
                cmd.remainder))

    @event('sb.command', 'rdns')
    def rdns(self, _, cmd):
        try:
            hostname, _, _ = socket.gethostbyaddr(cmd.remainder)
            cmd.mention_reply(hostname)
        except socket.herror:
            cmd.mention_reply('Unable to find results for {}'.format(
                cmd.remainder))

    @event('sb.command', 'ping')
    def ping(self, _, cmd):
        try:
            out = subprocess.Popen(
                ["/bin/ping", "-c1", "-w5", cmd.remainder],
                stdout=subprocess.PIPE
            ).stdout.read()
            cmd.mention_reply(out.decode('ascii').split('\n')[1])
        except (OSError, ValueError):
            cmd.mention_reply('Error pinging {}'.format(cmd.remainder))
