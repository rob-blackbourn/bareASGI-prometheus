"""Helpers"""

from typing import Optional, Type

from bareasgi import Application

from .metrics import HttpRequestMetric
from .middleware import PrometheusMiddleware
from .view import prometheus_view


def add_prometheus_middleware(
        app: Application,
        *,
        metric_type: Optional[Type[HttpRequestMetric]] = None,
        host: Optional[str] = None,
        app_name: Optional[str] = None,
        path_prefix: str = '',
        metrics_path: str = '/metrics'
) -> Application:
    """Adds prometheus middleware as the first middleware.

    Args:
        app (Application): The ASGI application
        metric_type (Optional[Type[HttpRequestMetric]], optional): An optional
            custom request monitor. Defaults to None.
        host (Optional[str], optional): An optional path for the metrics.
            Defaults to None.
        app_name (Optional[str], optional): The application name. Defaults to
            None.
        path_prefix (str, optional): The prefix for the path from which the
            metrics will be served. Defaults to ''.
        metrics_path (str, optional): The path from which the metrics
            will be served. Defaults to '/metrics'. Note the path_prefix will be
            prepended to this path.

    Returns:
        Application: The ASGI application
    """

    prometheus_middleware = PrometheusMiddleware(
        metric_type=metric_type,
        host=host,
        app_name=app_name
    )
    app.middlewares.insert(0, prometheus_middleware)

    app.http_router.add({'GET'}, path_prefix + metrics_path, prometheus_view)

    return app
