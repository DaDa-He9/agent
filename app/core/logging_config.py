import logging

from app.core.request_context import request_id_context


class RequestIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_context.get()
        return True


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s "
            "%(levelname)s "
            "[request_id=%(request_id)s] "
            "%(name)s: %(message)s"
        ),
    )

    root_logger = logging.getLogger()

    for handler in root_logger.handlers:
        if not any(
            isinstance(item, RequestIdFilter)
            for item in handler.filters
        ):
            handler.addFilter(RequestIdFilter())