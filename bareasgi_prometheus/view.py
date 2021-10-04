"""The promethues monitor page"""

from bareasgi import HttpRequest, HttpResponse, bytes_writer
from bareutils import header, response_code
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest


async def prometheus_view(_request: HttpRequest) -> HttpResponse:
    """The endpoint for prometheus stats

    Args:
        _request (HttpRequest): The request.

    Returns:
        HttpResponse: The prometheus statistics
    """
    headers = [
        (header.CONTENT_TYPE, CONTENT_TYPE_LATEST.encode('ascii'))
    ]
    body = generate_latest()
    return HttpResponse(response_code.OK, headers, bytes_writer(body))
