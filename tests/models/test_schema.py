import pytest
from pathlib import Path
import peewee
from peewee import SqliteDatabase, DatabaseProxy
import faker

from src.models.schema import (
    sqlite_db,
    Smog,
    smog_factory,
    Email
)


@pytest.fixture(scope="module")  # FIXME CHECK SCOPE
def database() -> DatabaseProxy:
    test_database: SqliteDatabase = SqliteDatabase(":memory:")
    sqlite_db.initialize(test_database)
    test_database.connect()
    # FIXME db.connect(reuse_if_open=True)
    yield sqlite_db
    test_database.close()


@pytest.fixture(scope="module", autouse=True)
def smog_db(database: DatabaseProxy) -> DatabaseProxy:
    database.create_tables([Smog, ])
    return database


@pytest.fixture(scope="function")
def smog_dict_data_full() -> dict[str, str | int | float]:
    # FIXME ADD TEST THAT DOES NOT HAVE ALL DATA!!
    #  TODO: USE FAKER TO ADD FAKE DATA
    return dict(
        site="Test Location",
        PM10=12,
        PM2_5=800,
        O3=291,
        NO2=20,
        SO2=2,
        C6H6=1,
        CO=40,
        measurement_timestamp="2022-03-04 12:00"
    )

@pytest.fixture(scope="function")
def smog_dict_data_missing() -> dict[str, str | int | float]:
    return dict(
        site="Test Location",
        PM10=12,
        O3=None,
        C6H6=1,
        measurement_timestamp="2022-03-04 12:00"
    )

@pytest.fixture(scope="function")
def smog_data_full(smog_dict_data_full: dict[str, str | int | float]) -> Smog:
    return smog_factory(
        **smog_dict_data_full
    )

@pytest.fixture(scope="function")
def smog_data_missing(smog_dict_data_missing: dict[str, str | int | float]) -> Smog:
    return smog_factory(
        **smog_dict_data_missing
    )


def test_smog_full_save(
    smog_data_full: Smog
) -> None:
    smog_id: int = Smog.save(smog_data_full)
    assert len(Smog.select()) == 1
    Smog.delete_by_id(smog_id)
    assert len(Smog.select()) == 0


def test_smog_missing_save(
    smog_data_missing: Smog
) -> None:
    smog_id: int = Smog.save(smog_data_missing)
    assert len(Smog.select()) == 1
    Smog.delete_by_id(smog_id)
    assert len(Smog.select()) == 0


def test_smog_save_raises_not_null_constraint(
    smog_dict_data_full: dict[str, str | int | float],
) -> None:
    with pytest.raises(peewee.IntegrityError):
        smog_dict_data_full.pop('site')
        _ = Smog().save(smog_dict_data_full)


def main() -> None:
    import sys
    sys.exit(pytest.main(["-qq -s"], plugins=[]))


if __name__ == '__main__':
    main()
