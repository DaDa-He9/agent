import logging
import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.core.request_context import request_id_context

logger = logging.getLogger(__name__)


class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next,
    ) -> Response:
        request_id = uuid.uuid4().hex
        request.state.request_id = request_id

        context_token = request_id_context.set(request_id)
        started_at = time.perf_counter()
        status_code = 500

        try:
            response = await call_next(request)
            status_code = response.status_code

            response.headers["X-Request-ID"] = request_id

            return response

        except Exception:
            logger.exception(
                "Unhandled exception during request: method=%s path=%s",
                request.method,
                request.url.path,
            )
            raise

        finally:
            elapsed_ms = (
                time.perf_counter() - started_at
            ) * 1000

            logger.info(
                "HTTP request completed: method=%s path=%s "
                "status_code=%s duration_ms=%.2f",
                request.method,
                request.url.path,
                status_code,
                elapsed_ms,
            )

            request_id_context.reset(context_token)