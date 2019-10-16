"""Prometheus middleware"""

from typing import Type, Optional

from baretypes import (
    Scope,
    Info,
    RouteMatches,
    Content,
    HttpRequestCallback,
    HttpResponse
)

from .monitors import RequestMonitor, BaseRequestMonitor

class PrometheusMiddleware:
    """Prometheus Middleware"""

    def __init__(self, request_monitor: Optional[Type[BaseRequestMonitor]] = None, **kwargs):
        self._request_monitor = request_monitor or RequestMonitor
        self._monitor_args = kwargs

    async def __call__(
            self,
            scope: Scope,
            info: Info,
            matches: RouteMatches,
            content: Content,
            handler: HttpRequestCallback
    ) -> HttpResponse:
        with self._request_monitor(scope, **self._monitor_args) as monitor:
            status, headers, content, pushes = await handler(scope, info, matches, content)
            monitor.observe(status)
            return status, headers, content, pushes
