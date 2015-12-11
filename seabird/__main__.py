import asyncio

from .config import SeabirdConfig
from .protocol import SeabirdProtocol


def main():
    conf = SeabirdConfig()
    conf.from_module('config')

    # Get the event loop
    loop = asyncio.get_event_loop()

    for network_config in conf.networks:
        inst = SeabirdProtocol(**network_config)
        coro = inst.connect()
        loop.run_until_complete(coro)

    # Run the event loop
    loop.run_forever()
    loop.close()

main()
