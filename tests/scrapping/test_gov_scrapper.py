from re import template
from flask import get_template_attribute
import pytest
from pytest_mock import MockerFixture, mocker
from unittest.mock import patch
import random
from jinja2 import Template

# from src.logging_setup.init_logging import setup_logging  # FIXME
from src.scrapping.scrapper import GovScrapper, Smog, smog_factory
from scrapper import TestScrapper
TestScrapper.__abstractmethods__ = set()  # FIXME?
# setup_logging()  # FIXME


class TestGovScrapper(TestScrapper):

    def get_dir(self) -> str:
        return "govscrapper"

    @pytest.fixture(scope="class")
    def timestamp_parameters(self) -> dict[str, int]:
        return {
            'day': 5,
            'hour': 17,
            'month': 4,
            'year': 2022,
        }

    @pytest.fixture(scope="class")
    def smog_data_empty(
        self,
    ) -> dict[str, str]:
        return {
            'measurement_timestamp': ''
        }

    @pytest.fixture(scope="class")
    def smog_data(
        self,
        timestamp_parameters: dict[str, int]
    ) -> dict[str, str | float]:
        year: int = timestamp_parameters['year']
        month: int = timestamp_parameters['month']
        day: int = timestamp_parameters['day']
        hour: int = timestamp_parameters['hour']
        return {
            'PM10': 8.2,
            'PM2_5': 13.8,
            'O3': 44.7,
            'NO2': 7.7,
            'SO2': 24.2,
            'C6H6': 0.1,
            'CO': 0.2,
            'measurement_timestamp': f"{year}-0{month}-0{day} {hour}:00",
        }

    @pytest.fixture(scope="class")
    def polanka_smog_empty(
        self,
        smog_data_empty: dict[str, str | float]
    ) -> Smog:
        return smog_factory(
            site="Poznań , ul. Polanka",
            **smog_data_empty,
        )

    @pytest.fixture(scope="class")
    def polanka_smog(
        self,
        smog_data: dict[str, str | float]
    ) -> Smog:
        return smog_factory(
            site="Poznań , ul. Polanka",
            **smog_data,
        )

    @pytest.fixture(scope="class")
    def dabrowskiego_smog_empty(
        self,
        smog_data_empty: dict[str, str | float]
    ) -> Smog:
        return smog_factory(
            site="Poznań , ul. Dąbrowskiego 169",
            **smog_data_empty,
        )

    @pytest.fixture(scope="class")
    def dabrowskiego_smog(
        self,
        smog_data: dict[str, str | float]
    ) -> Smog:
        return smog_factory(
            site="Poznań , ul. Dąbrowskiego 169",
            **smog_data,
        )

    @pytest.fixture(scope="class")
    def template_variables(
        self,
        smog_data: dict[str, str | float],
        timestamp_parameters: dict[str, int]
    ) -> dict[str, str | list[dict[str, str]]]:

        last_row_data: dict[str, str] = smog_data
        table_rows: list[dict[str, str]] = []
        MEASUREMENT_DAY: int = timestamp_parameters['day']
        MEASUREMENT_HOUR: int = timestamp_parameters['hour']
        left_empty_hours: list[int] = list(range(24 - MEASUREMENT_HOUR))
        days: tuple[int, ...] = tuple(range(1, MEASUREMENT_DAY + 1))
        hours: tuple[int, ...] = tuple(range(1, 24 + 1))
        for day in days:
            day_str: str = f"{day}" if len(str(day)) == 2 else f"0{day}"
            if day == days[-1]:
                hours = tuple(range(1, MEASUREMENT_HOUR + 1))
                # jesli ostatni dzien to niepelne godziny  # FIXME
            date: str = f"{day_str}.0{timestamp_parameters['month']}.{timestamp_parameters['year']}"
            for hour in hours:
                hour_str: str = f"{hour}" if len(str(hour)) == 2 else f"0{hour}"
                hour_str += ":00"
                table_row: dict[str, str] = {
                    'date': date,
                    'time': hour_str,
                    'PM10': f"{float(random.randint(0, 10000))/10}".replace('.', ','),
                    'PM2_5': f"{float(random.randint(0, 10000)/10)}".replace('.', ','),
                    'O3': f"{float(random.randint(0, 10000)/10)}".replace('.', ','),
                    'NO2': f"{float(random.randint(0, 10000)/10)}".replace('.', ','),
                    'SO2': f"{float(random.randint(0, 13000)/10)}".replace('.', ','),
                    'C6H6': f"{float(random.randint(0, 10)/10)}".replace('.', ','),
                    'CO': f"{float(random.randint(0, 10)/10)}".replace('.', ','),
                }
                if hour == hours[-1]:
                    table_row.update(last_row_data)
                table_rows.append(table_row)
        empty_rows: list[dict[str, str]] = []
        day_str: str = f"{days[-1]}" if len(str(days[-1])) == 2 else f"0{days[-1]}"
        date: str = f"{day_str}.04.2022"
        for left_hour in left_empty_hours:
            left_hour_str: str = f"{left_hour}" if len(str(left_hour)) == 2 else f"0{left_hour}"
            left_hour_str += ":00"
            empty_rows.append(
                {
                    'date': date,
                    'time': left_hour_str,
                }
            )

        return {
            'table_rows': table_rows,
            'empty_rows': empty_rows,
            'min_PM10': "6,1",
            'min_PM2_5': "5,1",
            'min_O3': "0",
            'min_NO2': "8,8",
            'min_SO2': "2,7",
            'min_C6H6': "0",
            'min_CO': "0,1",
            'max_PM10': "67,9",
            'max_PM2_5': "52,1",
            'max_O3': "90",
            'max_NO2': "91",
            'max_SO2': "16,2",
            'max_C6H6': "0,3",
            'max_CO': "1,2",
            'average_PM10': "19,1",
            'average_PM2_5': "14,3",
            'average_O3': "47,4",
            'average_NO2': "23,5",
            'average_SO2': "5,4",
            'average_C6H6': "0,1",
            'average_CO': "0,3",
        }

    @pytest.fixture(scope="class")
    def dabrowskiego_html_empty(
        self,
        dabrowskiego_template: Template
    ) -> str:

        template_variables: dict[str, str] = {
            'site': (
                "Dane pomiarowe 			Poznań"
                "			, ul. Dąbrowskiego 169"
                " , tabele - GIOŚ"
            ),
        }

        return dabrowskiego_template.render(**template_variables)

    @pytest.fixture(scope="class")
    def dabrowskiego_html(
        self,
        template_variables: dict[str, str | list[dict[str, str]]],
        dabrowskiego_template: Template
    ) -> str:

        template_variables.update(
            {
                'site': (
                    "Dane pomiarowe 			Poznań"
                    "			, ul. Dąbrowskiego 169"
                    " , tabele - GIOŚ"
                ),
            }
        )

        return dabrowskiego_template.render(**template_variables)

    @pytest.fixture(scope="class")
    def polanka_html_empty(
        self,
        polanka_template: Template
    ) -> str:

        template_variables: dict[str, str] = {
            'site': (
                "Dane pomiarowe 			Poznań"
                "			, ul. Polanka"
                " , tabele - GIOŚ"
            ),
        }

        return polanka_template.render(**template_variables)

    @pytest.fixture(scope="class")
    def polanka_html(
        self,
        template_variables: dict[str, str | list[dict[str, str]]],
        polanka_template: Template
    ) -> str:

        template_variables.update(
            {
                'site': (
                    "Dane pomiarowe 			Poznań"
                    "			, ul. Polanka"
                    " , tabele - GIOŚ"
                ),
            }
        )

        return polanka_template.render(**template_variables)

    def test_parse_dabrowskiego_url_empty(
        self,
        mocker: MockerFixture,
        dabrowskiego_smog_empty: Smog,
        dabrowskiego_html_empty: str
    ) -> None:

        gov_scrapper: GovScrapper = GovScrapper()
        mocker.patch.object(
            gov_scrapper,
            'get_html',
            return_value=dabrowskiego_html_empty
        )
        dabrowskiego_smog_parsed: Smog = gov_scrapper.parse_dabrowskiego_url()

        assert (
            dabrowskiego_smog_parsed == dabrowskiego_smog_empty
        )

    def test_parse_dabrowskiego_url(
        self,
        mocker: MockerFixture,
        dabrowskiego_smog: Smog,
        dabrowskiego_html: str
    ) -> None:

        gov_scrapper: GovScrapper = GovScrapper()
        mocker.patch.object(
            gov_scrapper,
            'get_html',
            return_value=dabrowskiego_html
        )
        dabrowskiego_smog_parsed: Smog = gov_scrapper.parse_dabrowskiego_url()

        assert (
            dabrowskiego_smog_parsed == dabrowskiego_smog
        )

    def test_parse_polanka_url_empty(
        self,
        mocker: MockerFixture,
        polanka_smog_empty: Smog,
        polanka_html_empty: str
    ) -> None:

        gov_scrapper: GovScrapper = GovScrapper()
        mocker.patch.object(
            gov_scrapper,
            'get_html',
            return_value=polanka_html_empty
        )
        polanka_smog_parsed: Smog = gov_scrapper.parse_polanka_url()

        assert (
            polanka_smog_parsed == polanka_smog_empty
        )

    def test_parse_polanka_url(
        self,
        mocker: MockerFixture,
        polanka_smog: Smog,
        polanka_html: str
    ) -> None:

        gov_scrapper: GovScrapper = GovScrapper()
        mocker.patch.object(
            gov_scrapper,
            'get_html',
            return_value=polanka_html
        )
        polanka_smog_parsed: Smog = gov_scrapper.parse_polanka_url()

        assert (
            polanka_smog_parsed == polanka_smog
        )


def main() -> None:
    import sys
    sys.exit(pytest.main(["-qq -s"], plugins=[]))


if __name__ == "__main__":
    main()
