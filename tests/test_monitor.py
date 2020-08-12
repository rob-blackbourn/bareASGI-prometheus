"""Tests for monitor"""

from time import sleep

from jetblack_metrics import monitor

from baretypes import (
    Scope,
    Info,
    RouteMatches
)

from bareasgi_prometheus.metrics import HttpRequestMetric


def test_http_request_metric():
    """Test the HTTP request metric"""

    host = 'host'
    app_name = 'test'
    scope: Scope = {'method': 'GET', 'path': '/index.html'}
    info: Info = {}
    matches: RouteMatches = {}
    metric = HttpRequestMetric(host, app_name, scope, info, matches)
    with monitor(metric):
        sleep(1)
        metric.status = 200
    assert metric.error is None
    assert round(metric.elapsed) == 1
    assert metric.status == 200
    assert metric.scope == scope
    assert metric.app_name == app_name
