from typing import Any
import logging

logger: logging.Logger = logging.getLogger(__name__)


def to_float(number: Any) -> float | None:
    try:
        return float(str(number).replace(',', '.'))
    except ValueError as e:
        logger.debug(f"Float conversion error: {e}")
        return None
