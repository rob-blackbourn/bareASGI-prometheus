"""Tests for monitor"""

from time import sleep
from bareasgi_prometheus.metrics import Metric, TimedMetric, HttpRequestMetric
from bareasgi_prometheus.monitor import monitor

def test_metric():
    """Test the basic metric"""

    metric = Metric()
    try:
        with monitor(metric):
            1.0 / 0 # pylint: disable=pointless-statement
    except ZeroDivisionError:
        pass
    assert metric.error is not None


def test_timed_metric():
    """Test the timed metric"""

    metric = TimedMetric()
    with monitor(metric):
        sleep(1)
    assert metric.error is None
    assert round(metric.elapsed) >= 1

def test_http_request_metric():
    """Test the HTTP request metric"""

    scope = {'method': 'GET', 'path': '/index.html'}
    name = 'test'
    metric = HttpRequestMetric(scope, name)
    with monitor(metric):
        sleep(1)
        metric.status = 200
    assert metric.error is None
    assert round(metric.elapsed) == 1
    assert metric.status == 200
    assert metric.scope == scope
    assert metric.name == name
    
