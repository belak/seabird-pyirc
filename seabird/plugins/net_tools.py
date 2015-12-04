import socket
import subprocess

from PyIRC.extensions import BaseExtension
from PyIRC.signal import event

from dns.resolver import query, NXDOMAIN
from dns.exception import DNSException


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
            result_type = "AAAA"

        try:
            answers = query(target, result_type)
        except DNSException as e:
            cmd.mention_reply(str(e))
        else:
            cmd.mention_reply(', '.join(str(answer) for answer in answers))


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
