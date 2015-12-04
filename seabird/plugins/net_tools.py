import socket
import subprocess

from PyIRC.extensions import BaseExtension
from PyIRC.signal import event


class NetToolsPlugin(BaseExtension):
    requires = ['CommandMux']

    family_mapping = {
        'A':    socket.AF_INET,
        'AAAA': socket.AF_INET6,
    }

    @event('sb.command', 'dig')
    def dig(self, _, cmd):
        target, _, result_type = cmd.remainder.partition(' ')
        if not result_type:
            result_type = "A"

        if result_type not in self.family_mapping:
            cmd.mention_reply('Address type %s not supported', result_type)
            return

        result_family = self.family_mapping[result_type]

        results = {
            socket.AF_INET:  set(),
            socket.AF_INET6: set(),
        }

        # Port doesn't matter, so we just pick one.
        addr_results = socket.getaddrinfo(target, 22)
        for res in addr_results:
            family = res[0]
            if family not in results:
                continue

            res_ip = res[4][0]
            results[family].add(res_ip)

        if not results[result_family]:
            cmd.mention_reply('Unable to find results for {}'.format(
                cmd.remainder))
            return

        cmd.mention_reply(', '.join(results[result_family]))

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
