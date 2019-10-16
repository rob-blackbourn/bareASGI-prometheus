"""Monitors"""

from __future__ import annotations
from abc import ABCMeta, abstractmethod
import time
from typing import Optional

from prometheus_client import Counter, Gauge, Histogram

from baretypes import (
    Scope
)


class BaseRequestMonitor(metaclass=ABCMeta):
    """
    Base context manager from which to inherit for request monitoring
    """

    def __init__(
            self,
            scope: Scope,
            init_metrics: bool = True,
            end_metrics: bool = True
    ):
        self.scope = scope
        self.status: Optional[int] = None
        self.init_time: Optional[float] = None
        self.init_metrics: bool = init_metrics
        self.end_metrics: bool = end_metrics

    def __enter__(self) -> BaseRequestMonitor:
        self.init_time = time.time()
        if self.init_metrics:
            self.update_init_metrics()
        return self

    def __exit__(self, exc_type, *args) -> None:
        if exc_type is None:
            self._check_response_is_observed()
        else:
            self.status = 500
        if self.end_metrics:
            self.update_end_metrics()

    def observe(self, status: int) -> None:
        """Observe the status

        :param status: The status code
        :type status: int
        """
        self.status = status

    def _check_response_is_observed(self) -> None:
        """Check if the status has been observed"""
        if self.status is None:
            raise Exception(
                "The request response has not been observed. "
                "Use the method 'observe'"
            )

    @abstractmethod
    def update_init_metrics(self) -> None:
        """Called at the start of the context"""

    @abstractmethod
    def update_end_metrics(self) -> None:
        """Called at the end of the context"""


class RequestMonitor(BaseRequestMonitor):
    """
    Default context manager with request count, latency and in progress
    metrics.
    """

    REQUEST_COUNT = Counter(
        "request_count", "Number of requests received", ["method", "path", "status"]
    )
    REQUEST_LATENCY = Histogram(
        "request_latency", "Elapsed time per request", ["method", "path"]
    )
    REQUEST_IN_PROGRESS = Gauge(
        "requests_in_progress", "Requests in progress", ["method", "path"]
    )

    def update_init_metrics(self):
        self.REQUEST_IN_PROGRESS.labels(
            self.scope['method'],
            self.scope['path']
        ).inc()

    def update_end_metrics(self):
        resp_time = time.time() - self.init_time
        self.REQUEST_COUNT.labels(
            self.scope['method'],
            self.scope['path'],
            self.status
        ).inc()
        self.REQUEST_LATENCY.labels(
            self.scope['method'],
            self.scope['path']
        ).observe(resp_time)
        self.REQUEST_IN_PROGRESS.labels(
            self.scope['method'],
            self.scope['path']
        ).dec()
