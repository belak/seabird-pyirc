import asyncio

from .config import SeabirdConfig
from .protocol import SeabirdProtocol


def main():
    conf = SeabirdConfig()
    conf.from_module('config')

    # Connect to the server
    inst = SeabirdProtocol(**conf)
    coro = inst.connect()

    # Get the event loop
    loop = asyncio.get_event_loop()

    # Run the event loop
    loop.run_until_complete(coro)
    loop.run_forever()
    loop.close()

main()
