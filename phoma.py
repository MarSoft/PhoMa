#!/usr/bin/env python
from argparse import ArgumentParser
from random import randrange
import socket
import logging

import muffin
from aiohttp import web

app = muffin.Application(__name__, DEBUG=True)

logging.basicConfig(level=logging.DEBUG)

@app.register('/')
async def index(req):
    with open('static/index.html', 'r') as i:
        indexfile = i.read()
    return indexfile


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
        except OSError as e:
            print(e)
            # address is already in use?
            if args.port:
                break
                parser.error('Port %d is busy?' % port)
        else:
            sock.close()
            print('Will listen on port %d' % port)
            break

    app.loop.run_until_complete(app.start())
    web.run_app(app, host=args.host, port=port)
