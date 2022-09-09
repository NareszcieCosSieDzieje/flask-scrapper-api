import pytest
from pytest_mock import MockerFixture
from jinja2 import Template

from tests.scrapping.scrapper_base import TestScrapper
from src.scrapping.scrapper import SmogMapScrapper
from src.scrapping.scrapper import Smog, smog_factory
TestScrapper.__abstractmethods__ = set()  # FIXME?


class TestSmogMapScrapper(TestScrapper):

    @pytest.mark.xfail(reason="Not implemented")
    def test_todo():
        pass

    def get_dir(self) -> str:
        return "smogmapscrapper"

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
    def dabrowskiego_html(
        self,
        template_variables: dict[str, list[dict[str, str]]],
        dabrowskiego_template: Template,
    ) -> str:

        # template_variables.update(
        #     {}  # FIXME
        # )

        return dabrowskiego_template.render(**template_variables)

    @pytest.fixture(scope="class")
    def dabrowskiego_html_empty(
        self,
        dabrowskiego_template: Template
    ) -> str:

        # TODO: site !
        template_variables: dict = {}  # FIXME?

        return dabrowskiego_template.render(**template_variables)

    @pytest.fixture(scope="class")
    def polanka_html(
        self,
        template_variables: dict[str, list[dict[str, str]]],
        polanka_template: Template,
    ) -> str:

        # template_variables.update(
        #     {}  # FIXME
        # )

        return polanka_template.render(**template_variables)

    def polanka_html_empty(
        self,
        polanka_template: Template
    ) -> str:

        template_variables: dict = {}  # FIXME?

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
        dabrowskiego_smog_empty: Smog,
        dabrowskiego_html_empty: str
    ) -> None:

        smogmap_scrapper: SmogMapScrapper = SmogMapScrapper()
        mocker.patch.object(
            smogmap_scrapper,
            'get_html',
            return_value=dabrowskiego_html_empty
        )
        dabrowskiego_smog_parsed: Smog = smogmap_scrapper.parse_dabrowskiego_url()
        breakpoint()
        assert (
            dabrowskiego_smog_parsed == dabrowskiego_smog_empty
        )

    def test_parse_dabrowskiego_url(
        self,
        mocker: MockerFixture,
        dabrowskiego_smog: Smog,
        dabrowskiego_html: str
    ) -> None:

        smogmap_scrapper: SmogMapScrapper = SmogMapScrapper()
        mocker.patch.object(
            smogmap_scrapper,
            'get_html',
            return_value=dabrowskiego_html
        )
        dabrowskiego_smog_parsed: Smog = smogmap_scrapper.parse_dabrowskiego_url()
        assert (
            dabrowskiego_smog_parsed == dabrowskiego_smog
        )

    def test_parse_polanka_url_empty(
        self,
        mocker: MockerFixture,
        polanka_smog_empty: Smog,
        polanka_html_empty: str
    ) -> None:

        smogmap_scrapper: SmogMapScrapper = SmogMapScrapper()
        mocker.patch.object(
            smogmap_scrapper,
            'get_html',
            return_value=polanka_html_empty
        )
        polanka_smog_parsed: Smog = smogmap_scrapper.parse_polanka_url()

        assert (
            polanka_smog_parsed == polanka_smog_empty
        )

    def test_parse_polanka_url(
        self,
        mocker: MockerFixture,
        polanka_smog: Smog,
        polanka_html: str
    ) -> None:

        smogmap_scrapper: SmogMapScrapper = SmogMapScrapper()
        mocker.patch.object(
            smogmap_scrapper,
            'get_html',
            return_value=polanka_html
        )
        polanka_smog_parsed: Smog = smogmap_scrapper.parse_polanka_url()

        assert (
            polanka_smog_parsed == polanka_smog
        )

    # def test_parse_rataje_url_empty(
    #     self,
    #     mocker: MockerFixture,
    #     rataje_smog_empty: Smog,
    #     rataje_html_empty: str
    # ) -> None:

    #     smogmap_scrapper: SmogMapScrapper = SmogMapScrapper()
    #     mocker.patch.object(
    #         smogmap_scrapper,
    #         'get_html',
    #         return_value=rataje_html_empty
    #     )
    #     rataje_smog_parsed: Smog = smogmap_scrapper.parse_rataje_url()

    #     assert (
    #         rataje_smog_parsed == rataje_smog_empty
    #     )

    # def test_parse_rataje_url(
    #     self,
    #     mocker: MockerFixture,
    #     rataje_smog: Smog,
    #     rataje_html: str
    # ) -> None:

    #     smogmap_scrapper: SmogMapScrapper = SmogMapScrapper()
    #     mocker.patch.object(
    #         smogmap_scrapper,
    #         'get_html',
    #         return_value=rataje_html
    #     )
    #     rataje_smog_parsed: Smog = smogmap_scrapper.parse_rataje_url()

    #     assert (
    #         rataje_smog_parsed == rataje_smog
    #     )



    # def test_stuff(self):
    #     smog_map_scrapper: SmogMapScrapper = SmogMapScrapper()
    #     x1 = smog_map_scrapper.parse_polanka()
    #     x2 = smog_map_scrapper.parse_dabrowskiego()
    #     x3 = smog_map_scrapper.parse_rataje()
    #     breakpoint()



# FIXME ADD GLOBAL TESTS FOR PARSE_URLS TO SEE IF THE LIST IS FLAT!

def main() -> None:
    import sys
    sys.exit(pytest.main(["-qq -s"], plugins=[]))


if __name__ == "__main__":
    main()
