# -*- coding: utf-8 -*-
"""
    proxy.py
    ~~~~~~~~
    ⚡⚡⚡ Fast, Lightweight, Pluggable, TLS interception capable proxy server focused on
    Network monitoring, controls & Application development, testing, debugging.

    :copyright: (c) 2013-present by Abhinav Singh and contributors.
    :license: BSD, see LICENSE for more details.
"""
import os
from urllib import parse as urlparse
from typing import Optional

from proxy.http.proxy import HttpProxyBasePlugin
from proxy.http.parser import HttpParser
from proxy.http.methods import httpMethods
import subprocess


class RedirectToCustomServerPlugin2(HttpProxyBasePlugin):
    """Modifies client request to redirect all incoming requests to a fixed server address."""

    UPSTREAM_SERVER = b'http://localhost:8080'

    def before_upstream_connection(
            self, request: HttpParser) -> Optional[HttpParser]:
        if request.has_header(b'Host'):
            print(request.headers)
            if request.headers[b'host'] == (b'Host', b'github.com'):
                repo_name, _ = request.path.split(b'.git', 1)
                repo_url = b'git@github.com:'+repo_name[1:]+b'.git'
                print('repo name: ', repo_name)
                if not os.path.exists((b'repos'+repo_name).decode()):
                    print('repo path: ', (b'repos'+repo_name).decode())
                    os.makedirs((b'repos'+repo_name).decode(), exist_ok=True)
                    print(*['git', 'clone', repo_url.decode(), '.'+repo_name.decode()], sep=' ')
                    subprocess.check_call(['git', '--bare', 'clone', repo_url.decode(), '.'+repo_name.decode()], cwd='repos')
                    subprocess.check_call(['mv',  '.'+repo_name.decode()+'/.git', '.'+repo_name.decode()+'.git'], cwd='repos')

                    print('path: ', (b'repos'+repo_name+b'/.git').decode())
                    subprocess.check_call(['git', '--bare', 'update-server-info'], cwd=(b'repos'+repo_name+b'.git').decode())


        # Redirect all non-https requests to inbuilt WebServer.
        if request.method != httpMethods.CONNECT:
            request.set_url(self.UPSTREAM_SERVER+request.url.path)
            print(request.url)
            # Update Host header too, otherwise upstream can reject our request
            if request.has_header(b'Host'):
                request.del_header(b'Host')
            request.add_header(
                b'Host', urlparse.urlsplit(
                    self.UPSTREAM_SERVER).netloc)
        return request

    def handle_client_request(
            self, request: HttpParser) -> Optional[HttpParser]:
        return request

    def handle_upstream_chunk(self, chunk: memoryview) -> memoryview:
        return chunk

    def on_upstream_connection_close(self) -> None:
        pass
