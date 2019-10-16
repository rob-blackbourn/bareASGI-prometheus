"""Helpers"""

from typing import Optional, Type, Dict, Any

from bareasgi import Application

from .monitors import BaseRequestMonitor
from .middleware import PrometheusMiddleware
from .view import prometheus_view

def add_prometheus_middleware(
        app: Application,
        request_monitor: Optional[Type[BaseRequestMonitor]] = None,
        request_monitor_args: Optional[Dict[str, Any]] = None,
        metrics_path: Optional[str] = '/metrics'
) -> Application:
    """Adds prometheus middleware as the first middleware.
    
    :param app: The ASGI application
    :type app: Application
    :param request_monitor: An optional custom request monitor
    :type request_monitor: Optional[Type[BaseRequestMonitor]]
    :param request_monitor_args: Optional arguments for the request monitor, defaults to None
    :type request_monitor_args: Optional[Dict[str, Any]], optional
    :param metrics_path: An optional path for the metrics, defaults to None
    :type metrics_path: Optional[str], optional
    :return: The ASGI application
    :rtype: Application
    """
    prometheus_middleware = PrometheusMiddleware(request_monitor, **(request_monitor_args or {}))
    app.middlewares.insert(0, prometheus_middleware)
    
    if metrics_path:
        app.http_router.add({'GET'}, metrics_path, prometheus_view)

    return app
