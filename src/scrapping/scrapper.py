import sys
from pathlib import Path
sys.path.insert(1, f"{Path(__file__).parent.parent}") # FIXME XD
import requests
import bs4
import re
from bs4 import BeautifulSoup
from abc import ABC
from functools import wraps # FIXME , cache
from cachetools import cached, TTLCache
import logging
from logging import Logger # FIXME
from frozendict import frozendict

from models.schema import Smog
from utils import to_float

# FIXME CREATE UTILITY FOR GET LOGGING
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)
sh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(sh)


class SmogScrapper(ABC):

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
            requests.get(url=url)
        except requests.exceptions.InvalidURL as e:
            error_message: str = f"The given URL is invalid ({url})\n\t{e}"
            self._logger.error(error_message)  # LOGGER?
            return False
        return True

    @cached(cache=TTLCache(maxsize=100, ttl=60 * 60))  # FIXME MAXSIZE!!! USTALIC NA BAZIE LICZBY URL
    def get_html(self, url: str):
        if self._is_url_valid(url):
            try:
                response: requests.Request = requests.get(url)
                html: str = response.content.decode()
                return html
            except requests.exceptions.RequestException as e:
                error_message = f"Failed to perform a GET request on: ({url})\n\t{e}"
                self._logger.error(error_message)
                # TODO: EXIT?
        else:
            raise Exception("Invalid url")  # FIXME CZY WGL UCZYAC TEGO A JESLI TAK TO POPRAWIC

    def parse_urls(self) -> list[Smog]:
        smog_list: list[Smog] = []
        # parse_methods: dict[str, Callable[[Any], Smog]] = dict(filter(lambda item: 'parse' in item[0], vars(self).items()))
        parse_methods = [x for x in dir(self) if 'parse' in x]
        for method_name in parse_methods:
            if method_name == 'parse_urls' or method_name.startswith('_'):
                continue
            parse_method = getattr(self, method_name)
            scrapper_result: Smog = parse_method()
            smog_list.append(scrapper_result)
        return smog_list


class GovScrapper(SmogScrapper):

    def __init__(self):
        self._logger = logger  # FIXME add a more specific logger
        self.__name__ = "GovScrapper"

    @staticmethod
    def _find_district_name(soup: BeautifulSoup):
        district_name: str = ""
        if district_paragraph := soup.find('p', class_="col-md-3 col-sm-10 col-xs-10 stacjainfo"):
            district_name = district_paragraph.text  # FIXME: obetnij?
            for re_pattern, repl in ((r"\s*Szczegółowe informacje o stacji:\s+", ""), (r"\s+", " ")):
                if district_sub := re.sub(re_pattern, repl, district_name, re.IGNORECASE):
                    district_name = district_sub
                district_name = district_name.strip()
        return district_name

    # TODO: divide into smaller chunks?
    def _parse_url(self,
                   url: str,
                   district_name: str = "") -> Smog:

        smog_list: list[Smog] = []
        html: str = self.get_html(url=url)
        soup: BeautifulSoup = BeautifulSoup(html, 'html.parser')

        new_district_name: str = self._find_district_name(soup)
        if new_district_name:
            district_name = new_district_name

        if data_table := soup.find(class_="table table-bordered"):

            table_rows: dict[int, bs4.element.Tag] = \
                dict(enumerate(data_table.find_all("tr")))  # FIXME TYP

            contamination_metrics_rows: list[tuple[str, str]] = zip(
                *([th.text for th in table_rows[i].find_all("th")[1:]] for i in range(2))
            )

            parameter_re_patterns = self._parameter_re_patterns

            parameter_columns: dict[str, int] = {
                parameter: -1 for parameter in parameter_re_patterns
            }

            measurement_units: dict[str, str] = {}

            for idx, (metric, unit) in enumerate(contamination_metrics_rows):
                for parameter, parameter_re in parameter_re_patterns.items():
                    # TODO: USUN variable przed walrusem w ifach
                    if parameter_match := parameter_re.match(metric):
                        parameter_columns[parameter] = idx
                        measurement_units[f"{parameter}_unit"] = unit

            measurement_timestamp: str = ""
            latest_measurement: list[str] = []
            not_found_indexes: set[int] = set([])
            datetime_re: re.Pattern = re.compile(r"(?P<Day>\d{2})\.(?P<Month>\d{2})\.(?P<Year>\d{4}),\s+(?P<Time>\d+:\d+)")

            for _, latest_data_row in list(reversed(table_rows.items()))[3:][:-2]:
                current_measurement: list[str] = \
                    [td.text.strip() for td in latest_data_row.find_all("td")]
                if all(map(lambda x: x == '', current_measurement)):
                    continue
                current_measurement = [
                    m for i, m in enumerate(current_measurement) if i in parameter_columns.values()
                ]
                current_measurement: list[float | str] = [
                    to_float(m) for m in current_measurement
                ]
                if not latest_measurement:
                    # Initialize the variables
                    latest_measurement = current_measurement
                    not_found_indexes = {
                        i for i, m in enumerate(latest_measurement) if not to_float(m)
                    }
                    timestamp: list[str] = [th.text.strip() for th in latest_data_row.find_all("th")]
                    if timestamp_match := datetime_re.match("".join(timestamp)):
                        measurement_timestamp = \
                            f"{timestamp_match.group('Year')}-"\
                            f"{timestamp_match.group('Month')}-"\
                            f"{timestamp_match.group('Day')} "\
                            f"{timestamp_match.group('Time')}"
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

            measurements: dict[str, float] = {
                parameter: latest_measurement[column_idx] for parameter, column_idx in parameter_columns.items()
            }

            parsed_smog: Smog = Smog(
                site=district_name,
                **measurements,
                **measurement_units,
                # air_quality_index? # FIXME?
                measurement_timestamp=measurement_timestamp,
            )
            smog_list.append(parsed_smog)
        return smog_list

    def parse_dabrowskiego_url(self) -> Smog:
        dabrowskiego_url: str = "https://powietrze.gios.gov.pl/pjp/current/station_details/table/944/3/0"
        district_name: str = "Poznań, ul. Dąbrowskiego 169"
        return self._parse_url(url=dabrowskiego_url, district_name=district_name)

    def parse_polanka_url(self) -> Smog:
        polanka_url: str = "https://powietrze.gios.gov.pl/pjp/current/station_details/table/943/3/0"
        district_name: str = "Poznań , ul. Polanka"
        return self._parse_url(url=polanka_url, district_name=district_name)


class SmogMapScrapper(SmogScrapper):

    def __init__(self):
        self._logger: Logger = logger # FIXME!
        self.__name__ = "SmogMapScrapper"

    # def parse_polanka(self) -> Smog:
    #     pass

    # def parse_dabrowskiego(self) -> Smog:
    #     pass

    # def parse_smog_map_url(self) -> Tuple[Exception, Smog]: # FIXME RET VAL
    def parse_smog_map_url(self) -> Smog: # FIXME RET VAL
        smog_map_url: str = "https://smogmap.pl/poznan/"
        smog_list: list[Smog] = []
        html: str = self.get_html(url=smog_map_url)
        soup: BeautifulSoup = BeautifulSoup(html, 'html.parser')  # FIXME WRZUCIC TO DO GET_HTML?

        if data_button := soup.find(id="panel_sound_btn"):
            measurements_timestamp: str = data_button.text
            timestamp_re: re.Pattern = re.compile(r"(?s).*?(?P<TimeStamp>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})")
            if timestamp_match := timestamp_re.match(measurements_timestamp):
                # if measurement_timestamp := timestamp_match.group('TimeStamp'):
                #     measurement_timestamp =  # FIXME RESTRUCTURE AND MAKE A TIMESTAMP FOR PEEWEE
                measurement_timestamp = timestamp_match.group('TimeStamp')
        if data_table := soup.find(id="relayList"):
            measurement_re: re.Pattern = re.compile(
                r"(?s).*?:\s+(?P<Measurement>\d+([\.\,]\d+)?)\s+(?P<Unit>\S+)"
            )
            for table in data_table.find_all(class_="city"):
                if relay := table.find(class_="relay"):
                    district_smog_data: dict[int, str] = dict(
                        enumerate(div.text for div in relay.find_all("div"))
                    )
                    district_name: str = district_smog_data.get(0, '') # FIXME?
                    air_quality_index: str = ""
                    air_quality_index_re: re.Pattern = re.compile(
                        r"polski\s+indeks\s+powietrze:\s+(?P<AirIndex>\S+)",
                        re.IGNORECASE
                    )

                    parameter_re_patterns = self._parameter_re_patterns
                    measurement_units: dict[str, str] = {}
                    measurements: dict[str, float] = {}

                    for row_text in district_smog_data.values():
                        row_text: str = row_text.lower()
                        if (not air_quality_index and
                            (air_quality_index_match := air_quality_index_re.match(row_text))
                        ):
                            air_quality_index = air_quality_index_match.group('AirIndex')

                        for parameter, parameter_re in parameter_re_patterns.items():
                            if ((parameter_re.match(row_text)) and
                                (parameter_match := measurement_re.match(row_text))):
                                measurements[parameter] = to_float(parameter_match.group('Measurement'))
                                measurement_units[f"{parameter}_unit"] = parameter_match.group('Unit')

                    parsed_smog: Smog = Smog(
                        site=district_name,
                        air_quality_index=air_quality_index,
                        measurement_timestamp=measurement_timestamp,  # FIXME
                        **measurements,
                        **measurement_units,
                    )
                    smog_list.append(parsed_smog)
            return smog_list


def main() -> None:
    from pprint import pprint
    scrappers = (GovScrapper(), SmogMapScrapper(), )
    for scrapper in scrappers:
        parsed_smog_list: list[Smog] = scrapper.parse_urls()
        print(f"{scrapper.__name__} parsed:")
        pprint(parsed_smog_list)


if __name__ == '__main__':
    import sys
    assert sys.version_info >= (3, 10), "Script requires Python 3.10+."
    # here = pathlib.Path(__file__).parent # FIXME WYWAL
    main()
