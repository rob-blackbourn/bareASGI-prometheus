"""
A metrics example
"""
import asyncio
import logging
import os
import socket

from bareasgi import (
    Application,
    text_writer
)
from baretypes import (
    Scope,
    Info,
    RouteMatches,
    Content,
    HttpResponse,
)

from bareasgi_prometheus import add_prometheus_middleware

logging.basicConfig(level=logging.DEBUG)

LOGGER = logging.getLogger('server_sent_events')


async def index(
        _scope: Scope,
        _info: Info,
        _matches: RouteMatches,
        _content: Content
) -> HttpResponse:
    """Redirect to the example"""
    return 303, [(b'Location', b'/example1')]


async def test_page1(
        _scope: Scope,
        _info: Info,
        _matches: RouteMatches,
        _content: Content
) -> HttpResponse:
    """A request handler which returns some html"""
    html = """
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Example 1</title>
  </head>
  <body>
    <h1>Example 1</h1>
    
    <p>This is simple<p>
  </body>
</html>

"""
    return 200, [(b'content-type', b'text/html')], text_writer(html)


async def test_page2(
        _scope: Scope,
        _info: Info,
        _matches: RouteMatches,
        _content: Content
) -> HttpResponse:
    """A request handler which returns HTML"""
    html = """
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Example 2</title>
  </head>
  <body>
    <h1>Example 2</h1>

    <p>This is simple<p>
  </body>
</html>
"""
    return 200, [(b'content-type', b'text/html')], text_writer(html)


async def test_empty(
        _scope: Scope,
        _info: Info,
        _matches: RouteMatches,
        _content: Content
) -> HttpResponse:
    """A request handler which only returns a valid "no content" status"""
    return 204


if __name__ == "__main__":
    # prometheus_middleware = PrometheusMiddleware()
    # app = Application(middlewares=[prometheus_middleware])
    # app.http_router.add({'GET'}, '/metrics', prometheus_view)

    app = Application()
    add_prometheus_middleware(app)

    app.http_router.add({'GET'}, '/', index)
    app.http_router.add({'GET'}, '/example1', test_page1)
    app.http_router.add({'GET'}, '/example2', test_page2)
    app.http_router.add({'GET'}, '/empty', test_empty)


    import uvicorn
    from hypercorn.asyncio import serve
    from hypercorn.config import Config

    logging.basicConfig(level=logging.DEBUG)

    USE_UVICORN = False
    hostname = socket.gethostname()
    certfile = os.path.expanduser(f"~/.keys/{hostname}.crt")
    keyfile = os.path.expanduser(f"~/.keys/{hostname}.key")

    if USE_UVICORN:
        uvicorn.run(app, host='0.0.0.0', port=9009, ssl_keyfile=keyfile, ssl_certfile=certfile)
    else:
        config = Config()
        config.bind = ["0.0.0.0:9009"]
        config.loglevel = 'debug'
        config.certfile = certfile
        config.keyfile = keyfile
        asyncio.run(serve(app, config))
