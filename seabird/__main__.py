import asyncio

from .protocol import SeabirdProtocol

from config import args

# Connect to the server
#
# TODO: We probably should have a better way of passing in args.
inst = SeabirdProtocol(**args)
coro = inst.connect()

# Get the event loop
loop = asyncio.get_event_loop()

# Run the event loop
loop.run_until_complete(coro)
loop.run_forever()
loop.close()
