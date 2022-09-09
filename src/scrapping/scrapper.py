# import requests
from requests_html import HTMLSession
import bs4
import re
from bs4 import BeautifulSoup
from abc import ABC
from functools import wraps
from cachetools import cached, TTLCache
import logging
import logging
from frozendict import frozendict
from typing import Callable, Any
from enum import Enum

logger: logging.Logger = logging.getLogger(__name__)

try:
    from utils import to_float
except ImportError as ie:
    # relative import if run from other package with the same level in the hierarchy
    logger.warning(
        f"Could perform an import of a module inside a package ({ie}), "
        "using a relative import."
    )
    from .utils import to_float

if not __package__:
    import sys
    from pathlib import Path
    sys.path.insert(1, f"{Path(__file__).parent.parent}")

from models.schema import Smog, smog_factory


class Site(Enum):  # FIXME Is this of any use?
    POLANKA=0
    DABROWSKIEGO=1
    RATAJE=2


class SmogScrapper(ABC):

    __name__: str

    _parameter_re_patterns: frozendict[str, re.Pattern] = frozendict({
        'PM10': re.compile(r"pm10", re.IGNORECASE),
        'PM2_5': re.compile(r"pm2([,\._])?5", re.IGNORECASE),
        'O3': re.compile(r"o3", re.IGNORECASE),
        'NO2': re.compile(r"no2", re.IGNORECASE),
        'SO2': re.compile(r"so2", re.IGNORECASE),
        'C6H6': re.compile(r"c6h6", re.IGNORECASE),
        'CO': re.compile(r"co", re.IGNORECASE),
    })

    def _is_url_valid(self, url: str) -> bool:
        try:
            HTMLSession().get(url)
        except Exception as e:
            error_message: str = f"The given URL is invalid ({url})\n\t{e}"
            logger.error(error_message)
            return False
        return True

    @cached(cache=TTLCache(maxsize=100, ttl=60 * 60))  # FIXME MAXSIZE!!! USTALIC NA BAZIE LICZBY URL
    def get_html(self, url: str) -> str:
        if self._is_url_valid(url):
            try:
                return HTMLSession().get(url).content.decode()
            except Exception as e:
                error_message = f"Failed to perform a GET request on: ({url})\n\t{e}"
                logger.error(error_message)
                return ""
        else:
            error_message = "Failed to get_html for an invalid URL"
            logger.error(error_message)
            return ""

    def parse_urls(self) -> list[Smog]:
        smog_list: list[Smog] = []
        parse_methods: list[str] = [
            x for x in dir(self) if 'parse' in x
        ]
        for method_name in parse_methods:
            if method_name == 'parse_urls' or method_name.startswith('_'):
                continue
            parse_method: Callable[[], Smog] = getattr(self, method_name)
            scrapper_result: Smog = parse_method()
            smog_list.append(scrapper_result)
        return smog_list


class GovScrapper(SmogScrapper):

    def __init__(self):
        self.__name__ = "GovScrapper"

    @staticmethod
    def _find_district_name(soup: BeautifulSoup) -> str:
        district_name: str = ""
        if district_paragraph := soup.find('p', class_="col-md-3 col-sm-10 col-xs-10 stacjainfo"):
            district_name = district_paragraph.text  # FIXME: obetnij?
            for re_pattern, repl in (
                (r"\s*Szczegółowe informacje o stacji:\s+", ""), (r"\s+", " ")
            ):
                if district_sub := re.sub(re_pattern, repl, district_name, re.IGNORECASE):
                    district_name = district_sub
                district_name = district_name.strip()
        return district_name

    # TODO: divide into smaller chunks?
    @cached(cache=TTLCache(maxsize=100, ttl=60 * 60))
    def _parse_url(
        self,
        url: str,
        district_name: str = ""
    ) -> Smog:

        html: str = self.get_html(url=url)
        soup: BeautifulSoup = BeautifulSoup(html, 'html.parser')

        new_district_name: str = self._find_district_name(soup)
        if new_district_name:
            district_name = new_district_name

        if data_table := soup.find(class_="table table-bordered"):

            table_rows: dict[int, bs4.element.Tag] = \
                dict(enumerate(data_table.find_all("tr")))  # FIXME TYP

            contamination_metrics_rows: zip[Any] = zip(
                *([th.text for th in table_rows[i].find_all("th")[1:]] for i in range(2))
            )
            parameter_re_patterns = self._parameter_re_patterns

            parameter_columns: dict[str, int] = {
                parameter: -1 for parameter in parameter_re_patterns
            }

            measurement_units: dict[str, str] = {}
            for idx, (metric, unit) in enumerate(contamination_metrics_rows):
                for parameter, parameter_re in parameter_re_patterns.items():
                    if parameter_re.match(metric):
                        parameter_columns[parameter] = idx
                        measurement_units[f"{parameter}_unit"] = unit

            measurement_timestamp: str = ""
            latest_measurement: list[str | float] = []
            not_found_indexes: set[int] = set([])
            datetime_re: re.Pattern = re.compile(
                r"(?P<Day>\d{2})\.(?P<Month>\d{2})\.(?P<Year>\d{4}),\s+(?P<Time>\d+:\d+)"
            )

            for _, latest_data_row in list(reversed(table_rows.items()))[3:][:-2]:
                current_measurement: list[str | float] = [
                    td.text.strip() for td in latest_data_row.find_all("td")
                ]
                if all(map(lambda x: x == '', current_measurement)):
                    continue
                current_measurement = [
                    m for i, m in enumerate(current_measurement) if i in parameter_columns.values()
                ]
                current_measurement = [
                    to_float(m) for m in current_measurement
                ]

                if not latest_measurement:
                    # Initialize the variables
                    latest_measurement = current_measurement
                    not_found_indexes = {
                        i for i, m in enumerate(latest_measurement) if not to_float(m)
                    }
                    timestamp: list[str] = [
                        th.text.strip() for th in latest_data_row.find_all("th")
                    ]
                    if timestamp_match := datetime_re.match("".join(timestamp)):
                        measurement_timestamp = (
                            f"{timestamp_match['Year']}-"
                            f"{timestamp_match['Month']}-"
                            f"{timestamp_match['Day']} "
                            f"{timestamp_match['Time']}"
                        )
                else:
                    # Update empty values with latest older values
                    for i, m in enumerate(current_measurement):
                        if i not in not_found_indexes or not to_float(m):
                            continue
                        latest_measurement[i] = to_float(m)
                        not_found_indexes.remove(i)
                # Stop condition if measurements for all params are collected
                if all(map(lambda x: x != "", latest_measurement)):
                    break

        measurements: dict[str, str | float] = {}
        if latest_measurement:
            measurements = {
                parameter: latest_measurement[column_idx]
                for parameter, column_idx in parameter_columns.items()
            }
        return smog_factory(
            site=district_name,
            **measurements,
            **measurement_units,
            measurement_timestamp=measurement_timestamp,
        )

    def parse_dabrowskiego_url(self) -> Smog:
        DABROWSKIEGO_URL: str = "https://powietrze.gios.gov.pl/pjp/current/station_details/table/944/3/0"
        DISTRICT_NAME: str = "Poznań, ul. Dąbrowskiego 169"
        return self._parse_url(url=DABROWSKIEGO_URL, district_name=DISTRICT_NAME)

    def parse_polanka_url(self) -> Smog:
        POLANKA_URL: str = "https://powietrze.gios.gov.pl/pjp/current/station_details/table/943/3/0"
        DISTRICT_NAME: str = "Poznań, ul. Polanka"
        return self._parse_url(url=POLANKA_URL, district_name=DISTRICT_NAME)


class SmogMapScrapper(SmogScrapper):

    def __init__(self):
        self.__name__ = "SmogMapScrapper"


    #  TODO: This method works, see if it could be useful in the future
    # def parse_smog_map_url_general(self) -> list[Smog]: # FIXME RET VAL
    #     SMOG_MAP_URL: str = "https://smogmap.pl/poznan/"
    #     smog_list: list[Smog] = []
    #     html: str = self.get_html(url=SMOG_MAP_URL)
    #     soup: BeautifulSoup = BeautifulSoup(html, 'html.parser')  # FIXME WRZUCIC TO DO GET_HTML?

    #     if data_button := soup.find(id="panel_sound_btn"):
    #         measurements_timestamp: str = data_button.text
    #         timestamp_re: re.Pattern = re.compile(
    #             r"(?s).*?(?P<TimeStamp>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})"
    #         )
    #         if timestamp_match := timestamp_re.match(measurements_timestamp):
    #             # if measurement_timestamp := timestamp_match['TimeStamp']:
    #             #     measurement_timestamp =  # FIXME RESTRUCTURE AND MAKE A TIMESTAMP FOR PEEWEE
    #             measurement_timestamp = timestamp_match['TimeStamp']
    #     if data_table := soup.find(id="relayList"):
    #         measurement_re: re.Pattern = re.compile(
    #             r"(?s).*?:\s+(?P<Measurement>\d+([\.\,]\d+)?)\s+(?P<Unit>\S+)"
    #         )
    #         for table in data_table.find_all(class_="city"):
    #             if relay := table.find(class_="relay"):
    #                 district_smog_data: dict[int, str] = dict(
    #                     enumerate(div.text for div in relay.find_all("div"))
    #                 )
    #                 district_name: str = district_smog_data.get(0, '')  # FIXME?
    #                 air_quality_index: str = ""
    #                 air_quality_index_re: re.Pattern = re.compile(
    #                     r"polski\s+indeks\s+powietrze:\s+(?P<AirIndex>\S+)",
    #                     re.IGNORECASE
    #                 )

    #                 parameter_re_patterns = self._parameter_re_patterns
    #                 measurement_units: dict[str, str] = {}
    #                 measurements: dict[str, float] = {}

    #                 for row_text in district_smog_data.values():
    #                     row_text: str = row_text.lower()
    #                     if (
    #                         not air_quality_index and
    #                         (air_quality_index_match := air_quality_index_re.match(row_text))
    #                     ):
    #                         air_quality_index = air_quality_index_match['AirIndex']

    #                     for parameter, parameter_re in parameter_re_patterns.items():
    #                         if (
    #                             (parameter_re.match(row_text)) and
    #                             (parameter_match := measurement_re.match(row_text))
    #                         ):
    #                             measurements[parameter] = to_float(parameter_match['Measurement'])
    #                             measurement_units[f"{parameter}_unit"] = parameter_match['Unit']

    #                 parsed_smog: Smog = smog_factory(
    #                     site=district_name,
    #                     air_quality_index=air_quality_index,
    #                     measurement_timestamp=measurement_timestamp,  # FIXME
    #                     **measurements,
    #                     **measurement_units,
    #                 )
    #                 smog_list.append(parsed_smog)
    #         return smog_list

    @cached(cache=TTLCache(maxsize=100, ttl=60 * 60))
    def _parse_url(
        self,
        url: str,
        district_name: str = ""
    ) -> Smog:
        html: str = self.get_html(url=url)
        soup: BeautifulSoup = BeautifulSoup(html, 'html.parser')

        measurement_timestamp: str = ""  # FIXME
        measurements: dict[str, float | int] = {}
        measurement_units: dict[str, str] = {}  # FIXME

        if data_table := soup.find("table", class_="smogRelayInfo"):

            parameter_re_patterns = self._parameter_re_patterns

            parameter_columns: dict[str, int] = {
                parameter: -1 for parameter in parameter_re_patterns
            }

            measurement_re: re.Pattern = re.compile(
                r"(?s)\s*(?P<Measurement>\d+([\.\,]\d+)?)"
            )

            # measurement_units: dict[str, str] = {}  # FIXME DATA IS MISSING ON THE SITE'S DETAILED PAGE (only available on general)
            table_head_columns: dict[int, str] = {}

            if table_head := data_table.find("thead"):
                table_head_columns = dict(
                    enumerate(th.text for th in table_head.find_all("th"))
                )

            for idx, metric in table_head_columns.items():
                for parameter, parameter_re in parameter_re_patterns.items():
                    if parameter_re.match(metric):
                        parameter_columns[parameter] = idx
                        # measurement_units[f"{parameter}_unit"] = unit  # TODO:?

            if table_body := data_table.find("tbody"):
                indexes_not_found: set[int] = set()
                datetime_re: re.Pattern = re.compile(
                    r"(?P<Year>\d{4})-(?P<Month>\d{2})-(?P<Day>\d{2})\s+(?P<Time>\d+:\d+)"
                )

                for data_row in table_body.find_all("tr"):
                    smog_data: dict[int, str] = dict(
                        enumerate(td.text for td in data_row.find_all("td"))
                    )
                    # FIXME ADD MEASUREMENT TIMESTAMP AS 'DATA' in DICT
                    for parameter, column_idx in parameter_columns.items():
                        if(
                            (parameter_match := measurement_re.match(smog_data[column_idx]))
                            and
                            (measurement := parameter_match['Measurement'])
                        ):
                            measurements[parameter] = to_float(measurement)
                            if column_idx in indexes_not_found:
                                indexes_not_found.remove(column_idx)
                        else:
                            indexes_not_found.add(column_idx)
                    if measurements and not measurement_timestamp:
                        timestamp_match: re.Match | None = None
                        for data in smog_data.values():
                            if timestamp_match := datetime_re.match(data):
                                break
                        if timestamp_match:
                            measurement_timestamp = (
                                f"{timestamp_match['Year']}-"
                                f"{timestamp_match['Month']}-"
                                f"{timestamp_match['Day']} "
                                f"{timestamp_match['Time']}"
                            )
                    if not indexes_not_found:
                        break
                    # measurement_units[f"{parameter}_unit"] = parameter_match['Unit']

        return smog_factory(
            site=district_name,
            **measurements,
            **measurement_units,
            measurement_timestamp=measurement_timestamp,
        )

    # cache for 1hr
    @cached(cache=TTLCache(maxsize=100, ttl=60 * 60))
    def _get_site_urls(self) -> dict[str, str]:
        SMOG_MAP_URL: str = "https://smogmap.pl/poznan/"
        site_urls: dict[str, str] = {}
        html: str = self.get_html(url=SMOG_MAP_URL)
        soup: BeautifulSoup = BeautifulSoup(html, 'html.parser')
        if data_table := soup.find(id="relayList"):
            for a_elem in data_table.find_all('a'):
                link: str = a_elem['href']
                site_urls[a_elem.text] = SMOG_MAP_URL + link
        return site_urls

    @cached(cache=TTLCache(maxsize=100, ttl=60 * 60))
    def _get_site_url_and_district_name(self, site: str) -> tuple[str, str]:
        site_urls: dict[str, str] = self._get_site_urls()
        site = site.lower()
        for site_name, site_url in site_urls.items():
            if site in site_name.lower():
                return site_url, site_name
        return "", ""

    def parse_polanka_url(self) -> Smog:
        polanka_detail_url, district_name = (
            self._get_site_url_and_district_name(site='polanka')
        )
        return self._parse_url(url=polanka_detail_url, district_name=district_name)

    def parse_dabrowskiego_url(self) -> Smog:
        dabrowskiego_detail_url, district_name = (
            self._get_site_url_and_district_name(site='dabrowskiego')
        )
        return self._parse_url(url=dabrowskiego_detail_url, district_name=district_name)

    def parse_rataje_url(self) -> Smog:
        rataje_detail_url, district_name = (
            self._get_site_url_and_district_name(site='rataje')
        )
        return self._parse_url(url=rataje_detail_url, district_name=district_name)


def main() -> None:
    from pprint import pprint
    scrappers: tuple[SmogScrapper, ...] = (GovScrapper(), SmogMapScrapper(), )
    for scrapper in scrappers:
        parsed_smog_list: list[Smog] = scrapper.parse_urls()
        print(f"{scrapper.__name__} parsed:")
        pprint(parsed_smog_list)


if __name__ == '__main__':
    from logging_setup.init_logging import setup_logging
    setup_logging()
    main()
