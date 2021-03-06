# Usage

The middleware can either be configured manually or with a helper.

## Manual Configuration

```python
from bareasgi import Application
from bareasgi_prometheus import PrometheusMiddleware, prometheus_view

...

prometheus_middleware = PrometheusMiddleware()
app = Application(middlewares=[prometheus_middleware])
app.http_router.add({'GET'}, '/metrics', prometheus_view)
```


## Helper Configuration

```python
from bareasgi import Application
from bareasgi_prometheus import add_prometheus_middleware

...

app = Application()
add_prometheus_middleware(app)
```
