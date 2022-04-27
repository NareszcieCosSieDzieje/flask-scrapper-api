import dramatiq
from dramatiq.brokers.redis import RedisBroker
import logging
from scrapping.scrapper import SmogScrapper, GovScrapper, SmogMapScrapper
from models.schema import (
    sqlite_db,
    Email,
    Smog,
    smog_factory
)
from config import (
    RedisConfig,
)

logger: logging.Logger = logging.getLogger(__name__)

# Code run by a dramatiq worker

redis_broker = RedisBroker(
    url=RedisConfig.REDIS_URL,
)
#, middleware=[]) # middleware = [] to remove prometheus
dramatiq.set_broker(redis_broker)


scrappers: tuple[GovScrapper, SmogMapScrapper] = (
    GovScrapper(),
    SmogMapScrapper(),
)


# @dramatiq.actor(store_results=True)
@dramatiq.actor
def do_smog_scrapping():
    parsed_smog_list: list[Smog] = []
    for scrapper in scrappers:
        parsed_smog_list.extend(scrapper.parse_urls())
    if parsed_smog_list:
        with sqlite_db.atomic():
            # FIXME WRZUC DO BAZY CZY ZWROC JAKIEGOS JSONA?
            Smog.bulk_create(parsed_smog_list, batch_size=10)  # FIXME OR UPDATE AS WELL?


def main() -> None:
    from logging_setup.init_logging import setup_logging
    setup_logging()


if __name__ == "__main__":
    main()
