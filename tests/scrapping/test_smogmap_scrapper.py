import pytest
from pytest_mock import MockerFixture
from jinja2 import Template

from tests.scrapping.scrapper_base import TestScrapper
from src.scrapping.scrapper import SmogMapScrapper
from src.scrapping.scrapper import Smog, smog_factory
TestScrapper.__abstractmethods__ = set()  # FIXME?


class TestSmogMapScrapper(TestScrapper):

    # @pytest.mark.xfail(reason="Not implemented")  # FIXME remove

    def get_dir(self) -> str:
        return "smogmapscrapper"

    @pytest.fixture(scope="class")
    def template_variables(
        self,
        template_variables_first: dict[str, list[dict[str, str]]],
    ) -> dict[str, str | list[dict[str, str]]]:

        template_variables: dict = {} # FIXME
        template_variables |= template_variables_first

        return template_variables

    @pytest.fixture(scope="class")
    def polanka_district_name(
        self,
    ) -> str:
        return "Poznan-Polanka"

    @pytest.fixture(scope="class")
    def dabrowskiego_district_name(
        self,
    ) -> str:
        return "Poznan-Dabrowskiego"

    # @pytest.fixture(scope="class")
    # def rataje_district_name(
    #     self,
    # ) -> str:
    #     return ""  # FIXME

    @pytest.fixture(scope="class")
    def smog_map_html(
        self,
    ) -> str:
        smogmap_scrapper: SmogMapScrapper = SmogMapScrapper()
        return smogmap_scrapper.get_html(url="https://smogmap.pl/poznan/")

    @pytest.fixture(scope="class")
    def dabrowskiego_html(
        self,
        template_variables: dict[str, list[dict[str, str]]],
        dabrowskiego_template: Template,
    ) -> str:

        template_variables.update(
            {
                'site': "Poznan-Dabrowskiego",
            }  # FIXME?
        )
        return dabrowskiego_template.render(**template_variables)

    @pytest.fixture(scope="class")
    def dabrowskiego_html_empty(
        self,
        dabrowskiego_template: Template
    ) -> str:

        template_variables: dict = {
            'site': "Poznan-Dabrowskiego",
        }  # FIXME?

        return dabrowskiego_template.render(**template_variables)

    @pytest.fixture(scope="class")
    def polanka_html(
        self,
        template_variables: dict[str, list[dict[str, str]]],
        polanka_template: Template,
    ) -> str:

        template_variables.update(
            {
                'site': "Poznan-Polanka",
            }  # FIXME?
        )

        # FIXME SET SMOG-LEVEL?

        return polanka_template.render(**template_variables)

    @pytest.fixture(scope="class")
    def polanka_html_empty(
        self,
        polanka_template: Template
    ) -> str:

        template_variables: dict = {
            "site": "Poznan-Polanka",
        }  # FIXME?

        return polanka_template.render(**template_variables)

    def test_parse_polanka_url(
        self,
    ) -> None:
        pass

    def test_parse_polanka_url_empty() -> None:
        pass

    def test_parse_dabrowskiego_url_empty() -> None:
        pass

    def test_parse_dabrowskiego_url() -> None:
        pass

    def test_parse_dabrowskiego_url_empty(
        self,
        mocker: MockerFixture,
        smog_map_html: str,
        dabrowskiego_smog_empty: Smog,
        dabrowskiego_html_empty: str
    ) -> None:

        smogmap_scrapper: SmogMapScrapper = SmogMapScrapper()
        mocker.patch.object(
            smogmap_scrapper,
            'get_html',
            side_effect=[smog_map_html, dabrowskiego_html_empty],
        )
        dabrowskiego_smog_parsed: Smog = smogmap_scrapper.parse_dabrowskiego_url()

        assert (
            dabrowskiego_smog_parsed == dabrowskiego_smog_empty
        )

    def test_parse_dabrowskiego_url(
        self,
        mocker: MockerFixture,
        smog_map_html: str,
        dabrowskiego_smog: Smog,
        dabrowskiego_html: str
    ) -> None:

        smogmap_scrapper: SmogMapScrapper = SmogMapScrapper()
        mocker.patch.object(
            smogmap_scrapper,
            'get_html',
            side_effect=[smog_map_html, dabrowskiego_html],
        )
        dabrowskiego_smog_parsed: Smog = smogmap_scrapper.parse_dabrowskiego_url()

        assert (
            dabrowskiego_smog_parsed == dabrowskiego_smog
        )

    def test_parse_polanka_url_empty(
        self,
        mocker: MockerFixture,
        smog_map_html: str,
        polanka_smog_empty: Smog,
        polanka_html_empty: str
    ) -> None:

        smogmap_scrapper: SmogMapScrapper = SmogMapScrapper()
        mocker.patch.object(
            smogmap_scrapper,
            'get_html',
            side_effect=[smog_map_html, polanka_html_empty],
        )
        polanka_smog_parsed: Smog = smogmap_scrapper.parse_polanka_url()

        assert (
            polanka_smog_parsed == polanka_smog_empty
        )

    def test_parse_polanka_url(
        self,
        mocker: MockerFixture,
        smog_map_html: str,
        polanka_smog: Smog,
        polanka_html: str
    ) -> None:

        smogmap_scrapper: SmogMapScrapper = SmogMapScrapper()
        mocker.patch.object(
            smogmap_scrapper,
            'get_html',
            side_effect=[smog_map_html, polanka_html],
        )
        polanka_smog_parsed: Smog = smogmap_scrapper.parse_polanka_url()

        assert (
            polanka_smog_parsed == polanka_smog
        )


def main() -> None:
    import sys
    sys.exit(pytest.main(["-qq -s"], plugins=[]))


if __name__ == "__main__":
    main()
