"""Tests for monitor"""

from time import sleep

from jetblack_metrics import monitor

from bareasgi import HttpRequest

from bareasgi_prometheus.metrics import HttpRequestMetric


def test_http_request_metric():
    """Test the HTTP request metric"""

    host = 'host'
    app_name = 'test'
    scope = {'method': 'GET', 'path': '/index.html'}
    request = HttpRequest(scope, {}, {}, {}, None)  # type: ignore
    metric = HttpRequestMetric(host, app_name, request)
    with monitor(metric):
        sleep(1)
        metric.status = 200
    assert metric.error is None
    assert round(metric.elapsed) == 1
    assert metric.status == 200
    assert metric.request.scope == scope
    assert metric.app_name == app_name
