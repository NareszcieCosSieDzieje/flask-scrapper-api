import logging
import dramatiq
from dramatiq.results import Results
from dramatiq.brokers.redis import RedisBroker
from dramatiq.results.backends import RedisBackend
from peewee import SqliteDatabase
from scrapping.scrapper import GovScrapper, SmogMapScrapper
from models.schema import (
    sqlite_db,
    Email,
    Smog,
)
from config import (
    RedisConfig,
    DatabaseConfig,
)

logger: logging.Logger = logging.getLogger(__name__)

# Code run by a dramatiq worker
redis_broker: RedisBroker = RedisBroker(
    host=RedisConfig.REDIS_HOST,
    port=RedisConfig.REDIS_PORT,
    # url=RedisConfig.REDIS_URL,
)
results_backend: RedisBackend = RedisBackend(
    host=RedisConfig.REDIS_HOST,
    port=RedisConfig.REDIS_PORT,
    # url=RedisConfig.REDIS_URL,
)
redis_broker.add_middleware(
    Results(backend=results_backend)
)
dramatiq.set_broker(redis_broker)


smog_db_path: str = DatabaseConfig.DB_PATH
database = SqliteDatabase(smog_db_path)
sqlite_db.initialize(database)

scrappers: tuple[GovScrapper, SmogMapScrapper] = (
    GovScrapper(),
    SmogMapScrapper(),
)

# either can migrate later to postgres or try to retrieve data from redis
# @dramatiq.actor(store_results=True)
@dramatiq.actor
def do_smog_scrapping():
    parsed_smog_list: list[Smog] = []
    for scrapper in scrappers:
        parsed_smog_list.extend(scrapper.parse_urls())
    if parsed_smog_list:
        with sqlite_db.atomic():
            Smog.bulk_create(parsed_smog_list, batch_size=10)


def main() -> None:
    from logging_setup.init_logging import setup_logging
    setup_logging()


if __name__ == "__main__":
    main()
