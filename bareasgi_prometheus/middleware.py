"""Prometheus middleware"""

from socket import gethostname
from typing import Optional, Type

from bareasgi import (
    HttpRequest,
    HttpResponse,
    HttpRequestCallback
)

from jetblack_metrics import monitor

from .metrics import HttpRequestMetric, PrometheusHttpRequestMetric


class PrometheusMiddleware:
    """Prometheus Middleware"""

    def __init__(
            self,
            *,
            metric_type: Type[HttpRequestMetric] = None,
            host: Optional[str] = None,
            app_name: Optional[str] = None
    ):
        """Prometheus middleware

        Args:
            metric_type (Type[HttpRequestMetric], optional): The metric type.
                Defaults to None.
            host (Optional[str], optional): The host. Defaults to None.
            app_name (Optional[str], optional): The application name. Defaults
                to None.
        """
        self.metric_type = metric_type or PrometheusHttpRequestMetric
        self.host = host or gethostname()
        self.app_name = app_name or 'bareASGI'

    async def __call__(
            self,
            request: HttpRequest,
            handler: HttpRequestCallback
    ) -> HttpResponse:
        with monitor(self.metric_type(
                self.host,
                self.app_name,
                request
        )) as metric:
            response = await handler(request)
            metric.status = response.status
            return response
