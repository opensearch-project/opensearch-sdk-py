#!/usr/bin/env python

import json

from aiohttp import web

class WebServer:
    def __init__(self):
        self.app = web.Application()
        self.host = 'localhost'
        self.port = 1234

    async def initializer(self) -> web.Application:
        self.app.router.add_get('/', self.root_handler)
        self.app.router.add_get('/{tail:.*}', self.default_handler)
        return self.app

    def run(self):
        web.run_app(self.initializer(), host=self.host, port=self.port)

    async def root_handler(self, request: web.Request) -> web.Response:
        return web.json_response({ 'ok': True })
    
    async def default_handler(self, request: web.Request) -> web.Response:
        print(request)
        raise web.HTTPNotImplemented()
    
if __name__ == '__main__':
    WebServer().run()
