#!/usr/bin/env python
from argparse import ArgumentParser
from random import randrange
import socket

from aiohttp import web

async def index(req):
    return web.Response(text='hello')


app = web.Application()
app.router.add_get('/', index)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-H', '--host', default='127.0.0.1',
                        help='Host to bind to (defaults to localhost)')
    parser.add_argument('-p', '--port', type=int,
                        help='Port to bind to (defaults to random)')
    args = parser.parse_args()

    while True:
        port = args.port or randrange(1000, 65535)
        # check if port is available
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.bind((args.host, port))
        except OSError:
            # address is already in use?
            if args.port:
                parser.error('Port is busy')
        else:
            sock.close()
            print('Will listen on port %d' % port)
            break

    web.run_app(app, host=args.host, port=port)
