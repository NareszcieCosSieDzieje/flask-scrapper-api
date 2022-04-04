from typing import Any


def to_float(number: Any) -> float | None:
    try:
        return float(str(number).replace(',', '.'))
    except ValueError as e:
        #  FIXME LOGGING {e}
        print(f"Float conversion error: {e}") # FIXME CHANGE TO LOGGER
        return None
