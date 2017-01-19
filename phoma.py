#!/usr/bin/env python
from argparse import ArgumentParser
from random import randrange
import socket
import logging
import subprocess as sp

import muffin
from aiohttp import web

from protocol import AdbProtocol

app = muffin.Application(__name__, DEBUG=True)

logging.basicConfig(level=logging.DEBUG)
protocol = AdbProtocol('/sdcard/DCIM/Camera', 'MarSoftS4A')

def url_for(route, **kwargs):
    return app.router[route].url(parts=kwargs)

@app.register('/')
async def index(req):
    with open('static/index.html', 'r') as i:
        indexfile = i.read()
    return indexfile

@app.register('/page/{n:[0-9]+}')
async def page(req):
    dirpage = protocol.list_directory_page(
        int(req.match_info['n']),
        12,
    )
    if dirpage in (None, False):
        return dict(error='Failed to fetch directory listing')
    return dict(files=[
        dict(
            name=name,
            href=url_for('fetch', name=name),
            preview=url_for('preview', name=name),
        )
        for name in dirpage
    ])

@app.register('/fetch/{name}')
def fetch(req):
    data = protocol.get_file(req.match_info['name'])
    if data is False:
        return 'Error'

    if req.GET.get('dl'):
        ctype = 'application/octet-stream'
    else:
        ctype = 'image/jpeg'

    return web.Response(
        body=data,
        content_type=ctype,
    )

@app.register('/preview/{name}')
def preview(req):
    # TODO: compress?
    data = protocol.get_file(req.match_info['name'])
    if data is False:
        return 'Error'

    return web.Response(
        body=data,
        content_type='image/jpeg',
    )

@app.register('/delete', methods=['POST'])
async def delete(req):
    await req.post()
    names = req.POST.get('names')
    if not names:
        return 'Error - filenames required'
    ret = await protocol.delete_list(names)
    if ret:
        return 'Success: ' + ret
    else:
        return 'Failed'

def main():
    parser = ArgumentParser()
    parser.add_argument('-H', '--host', default='127.0.0.1',
                        help='Host to bind to (defaults to localhost)')
    parser.add_argument('-p', '--port', type=int,
                        help='Port to bind to (defaults to random)')
    parser.add_argument('-s', '--service', action='store_true',
                        help='Don\'t start browser')
    parser.add_argument('-P', '--phone',
                        help='Network address of phone')
    args = parser.parse_args()

    if args.phone:
        # FIXME dirty way to specify phone's network host
        protocol.host = args.phone

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

    if not args.service:
        @app.register_on_start
        def run_browser(app):
            url = 'http://{}:{}/'.format(args.host, port)
            try:
                sp.check_call(['xdg-open', url])
            except sp.CalledProcessError:
                try:
                    sp.check_call(['open', url])
                except sp.CalledProcessError:
                    print('Failed to open url')

    app.loop.run_until_complete(app.start())
    web.run_app(app, host=args.host, port=port)

if __name__ == '__main__':
    main()
