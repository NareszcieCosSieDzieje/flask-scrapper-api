from re import template
from flask import get_template_attribute
import pytest
from pytest_mock import MockerFixture, mocker
from unittest.mock import patch
import random
from jinja2 import Template

# from src.logging_setup.init_logging import setup_logging  # FIXME
from src.scrapping.scrapper import GovScrapper, Smog, smog_factory
from tests.scrapping.scrapper_base import TestScrapper
TestScrapper.__abstractmethods__ = set()  # FIXME?
# setup_logging()  # FIXME


class TestGovScrapper(TestScrapper):

    def get_dir(self) -> str:
        return "govscrapper"

    @pytest.fixture(scope="class")
    def template_variables(
        self,
    ) -> dict[str, str | list[dict[str, str]]]:

        template_variables: dict[str, list[dict[str, str]]] = (
            super().template_variables()
        )

        template_variables |= {
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

        return template_variables

    @pytest.fixture(scope="class")
    def polanka_district_name(
        self,
    ) -> str:
        return "Poznań , ul. Polanka"

    @pytest.fixture(scope="class")
    def dabrowskiego_district_name(
        self,
    ) -> str:
        return "Poznań , ul. Dąbrowskiego 169"

    # TODO: Rataje?

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
        dabrowskiego_template: Template,
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
        polanka_template: Template,
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
        polanka_template: Template,
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
        dabrowskiego_html_empty: str,
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
        dabrowskiego_html: str,
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
        polanka_html_empty: str,
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
        polanka_html: str,
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
