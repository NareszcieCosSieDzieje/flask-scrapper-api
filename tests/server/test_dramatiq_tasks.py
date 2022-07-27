import pytest
from pytest_mock import MockerFixture
import dramatiq
from dramatiq.brokers.rabbitmq import RabbitmqBroker
from dramatiq.brokers.stub import StubBroker
from dramatiq import Worker

from src.server import schedule_scrapping  # FIXME?

@pytest.mark.xfail(reason="Not implemented")
def test_todo():
    pass


# if os.getenv("UNIT_TESTS") == "1":
#     broker = StubBroker()
#     stub_backend = StubBackend()
#     broker.add_middleware(Results(backend=stub_backend))
#     dramatiq.set_broker(broker)
# else:
#     broker = RedisBroker(host="redis")
#     results_backend = RedisBackend(host="redis")
#     broker.add_middleware(Results(backend=results_backend))
#     dramatiq.set_broker(broker)

# @pytest.fixture()  # FIXME ADD SCOPE
# def stub_broker():
#     broker.flush_all()
#     return broker


# @pytest.fixture()  # FIXME ADD SCOPE
# def stub_worker():
#     worker = Worker(broker, worker_timeout=100)
#     worker.start()
#     yield worker
#     worker.stop()


# if os.getenv("UNIT_TESTS") == "1":
#     broker = StubBroker()
#     broker.emit_after("process_boot")
# else:
#     broker = RabbitmqBroker()


# def test_count_words(stub_broker, stub_worker):
#     count_words.send("http://example.com")
#     stub_broker.join(count_words.queue_name)
#     stub_worker.join()

# def test_count_words(stub_broker, stub_worker):
#     count_words.send("http://example.com")
#     stub_broker.join(count_words.queue_name, fail_fast=True)
#     stub_worker.join()


def main() -> None:
    import sys
    sys.exit(pytest.main(["-qq -s"], plugins=[]))


if __name__ == "__main__":
    main()
