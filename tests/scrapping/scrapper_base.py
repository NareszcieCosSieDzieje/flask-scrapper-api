
import pytest
from abc import ABC, abstractmethod
from jinja2 import FileSystemLoader, Environment, Template
import os
from pathlib import Path
from typing import Callable
import random

from src.scrapping.scrapper import Smog, smog_factory


class TestScrapper(ABC):
# class TestScrapper:

    @pytest.fixture(scope="class")
    def jinja2_env(self) -> Environment:
        return Environment(
            loader=FileSystemLoader(
                os.path.abspath(
                    os.path.dirname(__file__)
                ) + '/templates',
                encoding='utf8'
            ),
            trim_blocks=True,
            lstrip_blocks=True
        )

    @abstractmethod
    def get_dir(self) -> str:
        pass

    @pytest.fixture(scope="class")
    def get_template_in_dir(
        self,
        get_template,
    ) -> Callable[[str], Callable[[str], str]]:
        def _get_template_in_dir(
            template_name: str,
        ) -> Template:
            path_to_template: Path = Path(self.get_dir()) / template_name
            return get_template(str(path_to_template))
        return _get_template_in_dir

    @pytest.fixture(scope="class")
    def get_template(
        self,
        jinja2_env,
    ) -> Callable[[str], str]:
        def _get_template(
            template_file: str,
        ):
            return jinja2_env.get_template(template_file)
        return _get_template

    @pytest.fixture(scope="class")
    def dabrowskiego_template(
        self,
        get_template_in_dir,
    ) -> Template:
        return get_template_in_dir('dabrowskiego.j2')

    @pytest.fixture(scope="class")
    def polanka_template(
        self,
        get_template_in_dir,
    ) -> Template:
        return get_template_in_dir('polanka.j2')

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
    def template_variables(
        self,
        smog_data: dict[str, str | float],
        timestamp_parameters: dict[str, int],
    ) -> dict[str, list[dict[str, str]]]:

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
                # If it's the last day, a non 24 hour cycle is possible  # FIXME
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
                    table_row |= last_row_data
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
        }

    @abstractmethod
    @pytest.fixture(scope="class")
    def polanka_district_name(
        self,
    ) -> str:
        pass

    @abstractmethod
    @pytest.fixture(scope="class")
    def dabrowskiego_district_name(
        self,
    ) -> str:
        pass

    # @pytest.fixture(scope="class")
    # def rataje_district_name(
    #     self,
    # ) -> str:
    #     return ""  # FIXME

    @pytest.fixture(scope="class")
    def polanka_smog_empty(
        self,
        smog_data_empty: dict[str, str | float],
        polanka_district_name: str,
    ) -> Smog:
        return smog_factory(
            site=polanka_district_name,
            **smog_data_empty,
        )

    @pytest.fixture(scope="class")
    def polanka_smog(
        self,
        smog_data: dict[str, str | float],
        polanka_district_name: str,
    ) -> Smog:
        return smog_factory(
            site=polanka_district_name,
            **smog_data,
        )

    @pytest.fixture(scope="class")
    def dabrowskiego_smog_empty(
        self,
        smog_data_empty: dict[str, str | float],
        dabrowskiego_district_name: str,
    ) -> Smog:
        return smog_factory(
            site=dabrowskiego_district_name,
            **smog_data_empty,
        )

    @pytest.fixture(scope="class")
    def dabrowskiego_smog(
        self,
        smog_data: dict[str, str | float],
        dabrowskiego_district_name: str,
    ) -> Smog:
        return smog_factory(
            site=dabrowskiego_district_name,
            **smog_data,
        )