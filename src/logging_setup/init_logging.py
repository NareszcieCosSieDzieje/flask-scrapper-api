import yaml
import logging
import logging.config
from pathlib import Path
from functools import wraps
from typing import Callable, Any


def make_singleton(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        if not hasattr(func, '__singleton__'):
            setattr(func, '__singleton__', True)
            return func(*args, **kwargs)
        return None
    return wrapper


@make_singleton
def setup_logging(
    default_path: Path = (Path(__file__).parent / Path("config.yaml")),
    default_level: int = logging.DEBUG
) -> None:
    use_default: bool = True
    if default_path.is_file():
        with default_path.open('rt') as logging_config_file:
            try:
                logging_config_dict: dict[str, Any] = yaml.safe_load(
                    logging_config_file.read()
                )
                logging.config.dictConfig(
                    logging_config_dict
                )
                use_default = False
            except Exception as e:
                print(f"Error while loading the logger configuration.{e}")
    if use_default:
        print("Fallback to defaults.")
        logging.basicConfig(level=default_level)


# auto setup on import
# setup_logging()  # FIXME?


def main() -> None:
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.debug("Debugging...")
    logger.critical("Oh no a terrible accident has occured!")
    logger.error("Alas, an error!")
    logger.warning("Yikes, better watch out.")
    logger.info("The logger has been set.")


if __name__ == "__main__":
    main()
