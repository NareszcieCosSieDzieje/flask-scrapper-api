import pytest
from pytest_mock import MockerFixture
import random
from jinja2 import FileSystemLoader, Environment, Template
import os

# from src.logging_setup.init_logging import setup_logging  # FIXME
from src.scrapping.scrapper import GovScrapper
from src.models.schema import Smog, smog_factory

# setup_logging()  # FIXME


class TestGovScrapper:

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

    @pytest.fixture(scope="class")
    def dabrawskiego_template(self, jinja2_env: Environment) -> Template:
        return jinja2_env.get_template('dabrowskiego.j2')

    @pytest.fixture(scope="class")
    def polanka_template(self, jinja2_env: Environment) -> Template:
        return jinja2_env.get_template('polanka.j2')

    @pytest.fixture(scope="class")
    def smog_data(self) -> dict[str, str]:
        return {
            'pm10': "8,2",
            'pm2_5': "13,8",
            'o3': "44,7",
            'no2': "7,7",
            'so2': "24,2",
            'c6h6': "0,1",
            'co': "0,2",
            'measurement_timestamp': "2022-02-05 15:22:12",
        }

    @pytest.fixture(scope="class")  # FIXME function
    def polanka_smog(self, smog_data: dict[str, str]) -> Smog:
        # FIXME: DODAJ ZMIENNE
        return Smog(
            air_quality_index="FAIR",  # FIXME jak dodam co i c6j6 tresholdy moze sie zmienic
            site="Poznań , ul. Polanka",
            **smog_data,
        )

    @pytest.fixture(scope="class")  # FIXME function
    def dabrawskiego_smog(self, smog_data: dict[str, str]) -> Smog:
        # FIXME: DODAJ ZMIENNE
        return Smog(
            air_quality_index="FAIR",  # FIXME jak dodam co i c6j6 tresholdy moze sie zmienic
            site="Poznań, ul. Dąbrowskiego 169",
            **smog_data,
        )

    @pytest.fixture(scope="class")  # FIXME function
    def template_variables(
        self,
        smog_data: dict[str, str]
    ) -> dict[str, str | list[dict[str, str]]]:

        last_row_data: dict[str, str] = smog_data
        table_rows: list[dict[str, str]] = []
        random_measurement_hour: int = random.randint(1, 24)
        left_empty_hours: list[int] = list(range(24 - random_measurement_hour))
        days: tuple[int, ...] = tuple(range(1, 6))
        hours: tuple[int, ...] = tuple(range(1, 24 + 1))
        for day in days:  # TODO: JAKA LICZBA DNI?
            day_str: str = f"{day}" if len(str(day)) == 2 else f"0{day}"
            if day == days[-1]:
                hours = tuple(range(1, random_measurement_hour + 1))
                # jesli ostatni dzien to niepelne godziny  # FIXME
            date: str = f"{day_str}.04.2022"
            for hour in hours:
                hour_str: str = f"{hour}" if len(str(hour)) == 2 else f"0{hour}"
                hour_str += ":00"
                table_row: dict[str, str] = {
                    # FIXME VALUES
                    'date': date,
                    'time': hour_str,
                    'pm10': f"{float(random.randint(0, 10000))/10}".replace('.', ','),  # FIXME UPEWNIJ SIE ZE KROPKA A NIE PRZECINEK JAKO STRING
                    'pm2_5': f"{float(random.randint(0, 10000)/10)}".replace('.', ','),
                    'o3': f"{float(random.randint(0, 10000)/10)}".replace('.', ','),
                    'no2': f"{float(random.randint(0, 10000)/10)}".replace('.', ','),
                    'so2': f"{float(random.randint(0, 13000)/10)}".replace('.', ','),
                    'c6h6': f"{float(random.randint(0, 10)/10)}".replace('.', ','),
                    'co': f"{float(random.randint(0, 10)/10)}".replace('.', ','),
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
            'min_pm10': "6,1",
            'min_pm2_5': "5,1",
            'min_o3': "0",
            'min_no2': "8,8",
            'min_so2': "2,7",
            'min_c6h6': "0",
            'min_co': "0,1",
            'max_pm10': "67,9",
            'max_pm2_5': "52,1",
            'max_o3': "90",
            'max_no2': "91",
            'max_so2': "16,2",
            'max_c6h6': "0,3",
            'max_co': "1,2",
            'average_pm10': "19,1",
            'average_pm2_5': "14,3",
            'average_o3': "47,4",
            'average_no2': "23,5",
            'average_so2': "5,4",
            'average_c6h6': "0,1",
            'average_co': "0,3",
        }

    @pytest.fixture(scope="class")
    def dabrawskiego_html(
        self,
        template_variables: dict[str, str | list[dict[str, str]]],
        dabrawskiego_template: Template
    ) -> str:

        template_variables.update(
            {
                'title': (
                    "Dane pomiarowe 			Poznań"
                    "			, ul. Dąbrowskiego 169"
                    " , tabele - GIOŚ"
                ),
            }
        )

        return dabrawskiego_template.render(**template_variables)

    @pytest.fixture(scope="class")
    def polanka_html(
        self,
        template_variables: dict[str, str | list[dict[str, str]]],
        polanka_template: Template
    ) -> str:

        template_variables.update(
            {
                'title': (
                    "Dane pomiarowe 			Poznań"
                    "			, ul. Polanka"
                    " , tabele - GIOŚ"
                ),
            }
        )

        return polanka_template.render(**template_variables)

    def test_parse_dabrowskiego_url(
        self,
        mocker: MockerFixture,
        dabrawskiego_smog: Smog,
        dabrawskiego_html: str
    ) -> None:

        gov_scrapper: GovScrapper = GovScrapper()
        mocker.patch.object(
            gov_scrapper,
            'get_html',
            return_value=dabrawskiego_html
        )
        dabrawskiego_smog_parsed: Smog = gov_scrapper.parse_dabrowskiego_url()

        assert (
            dabrawskiego_smog_parsed == dabrawskiego_smog
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


if __name__ == '__main__':
    main()
