import yaml
import logging
import logging.config
from pathlib import Path


def setup_logging(default_path: Path = Path("config.yaml"), default_level: int = logging.DEBUG):
    use_default: bool = True
    if default_path.is_file():
        with default_path.open('rt') as logging_config_file:
            try:
                logging_config_str: str = yaml.safe_load(
                    logging_config_file.read()
                )
                logging.config.dictConfig(
                    logging_config_str
                )
                use_default = False
            except Exception as e:
                print(f"Error while loading the logger configuration.{e}")
    if use_default:
        print("Fallback to defaults.")
        logging.basicConfig(level=default_level)


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
