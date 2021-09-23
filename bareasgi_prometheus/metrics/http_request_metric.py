"""An HTTP Request metric"""

from bareasgi import HttpRequest

from jetblack_metrics import TimedMetric


class HttpRequestMetric(TimedMetric):
    """A metric which holds HTTP information."""

    def __init__(
            self,
            host: str,
            app_name: str,
            request: HttpRequest
    ) -> None:
        """Create an HTTP request metric

        Args:
            host (str): The host
            app_name (str): The name of the application
            request (HttpRequest): The request
        """
        super().__init__()
        self.host = host
        self.app_name = app_name
        self.request = request
        self.status = 500
