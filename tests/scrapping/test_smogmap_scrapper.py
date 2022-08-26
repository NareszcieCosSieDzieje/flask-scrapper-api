import pytest
from pytest_mock import MockerFixture

from src.scrapping.scrapper import SmogMapScrapper
from scrapper import TestScrapper


class TestSmogMapScrapper(TestScrapper):

    def get_dir(self) -> str:
        return "smogmapscrapper"

    @pytest.mark.xfail(reason="Not implemented")
    def test_todo():
        pass

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
