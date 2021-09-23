"""The promethues monitor page"""

from prometheus_client import (  # type: ignore
    CONTENT_TYPE_LATEST,
    generate_latest
)

from bareasgi import bytes_writer

from bareasgi import (
    HttpRequest,
    HttpResponse
)


async def prometheus_view(_request: HttpRequest) -> HttpResponse:
    """The endpoint for prometheus stats

    Args:
        _request (HttpRequest): The request.

    Returns:
        HttpResponse: The prometheus statistics
    """
    headers = [
        (b'content-type', CONTENT_TYPE_LATEST.encode('ascii'))
    ]
    body = generate_latest()
    return HttpResponse(200, headers, bytes_writer(body))
