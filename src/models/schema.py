from peewee import DatabaseProxy, Model, TextField, FloatField, FixedCharField, DateTimeField
import logging

logger = logging.getLogger(__name__)

try:
    from closest_dict import AirQualityIndexDict
except ImportError as ie:
    # relative import if run from other package with the same level in the hierarchy
    logger.warning(f"Could perform an import of a module inside a package, using a relative import.{ie}")
    from .closest_dict import AirQualityIndexDict

sqlite_db = DatabaseProxy()


class BaseModel(Model):
    class Meta:
        database = sqlite_db


# TODO: ID FOR SITE?
class Smog(BaseModel):
    site = TextField(null=False)
    air_quality_index = TextField(default=None)
    PM10 = FloatField(default=None)
    PM2_5 = FloatField(default=None)
    O3 = FloatField(default=None)
    NO2 = FloatField(default=None)
    SO2 = FloatField(default=None)
    C6H6 = FloatField(default=None)
    CO = FloatField(default=None)
    PM10_unit = FixedCharField(max_length=5, default="µg/m3")
    PM2_5_unit = FixedCharField(max_length=5, default="µg/m3")
    O3_unit = FixedCharField(max_length=5, default="µg/m3")
    NO2_unit = FixedCharField(max_length=5, default="µg/m3")
    SO2_unit = FixedCharField(max_length=5, default="µg/m3")
    C6H6_unit = FixedCharField(max_length=5, default="µg/m3")
    CO_unit = FixedCharField(max_length=5, default="mg/m3")
    measurement_timestamp = DateTimeField(
        formats=r"%Y-%m-%d %H:%M:%S",
        null=False
    )

    def __eq__(self, other) -> bool:
        return (
            self.site == other.site and
            self.air_quality_index == other.air_quality_index and
            self.PM10 == other.PM10 and
            self.PM2_5 == other.PM2_5 and
            self.O3 == other.O3 and
            self.NO2 == other.NO2 and
            self.SO2 == other.SO2 and
            self.C6H6 == other.C6H6 and
            self.CO == other.CO and
            self.PM10_unit == other.PM10_unit and
            self.PM2_5_unit == other.PM2_5_unit and
            self.O3_unit == other.O3_unit and
            self.NO2_unit == other.NO2_unit and
            self.SO2_unit == other.SO2_unit and
            self.C6H6_unit == other.C6H6_unit and
            self.CO_unit == other.CO_unit and
            self.measurement_timestamp == other.measurement_timestamp
        )

    def __str__(self) -> str:
        return (
            f"{self.site=}\n"
            f"{self.air_quality_index=}\n"
            f"{self.measurement_timestamp=}\n"
            f"{self.PM10=} {self.PM10_unit}\n"
            f"{self.PM2_5=} {self.PM2_5_unit}\n"
            f"{self.O3=} {self.O3_unit}\n"
            f"{self.NO2=} {self.NO2_unit}\n"
            f"{self.SO2=} {self.SO2_unit}\n"
            f"{self.C6H6=} {self.C6H6_unit}\n"
            f"{self.CO=} {self.CO_unit}\n"
        )

    def __repr__(self) -> str:
        return f"{vars(self)}"

    def get_air_quality_index(self) -> str | None:
        # Taken in 2022 from | "https://airindex.eea.europa.eu/Map/AQI/Viewer/#"
        # starts from 0 in um3
        pm2_5_treshold: AirQualityIndexDict = AirQualityIndexDict(
            {
                10: AirQualityIndexDict.AirQualityIndexScale.GOOD,
                20: AirQualityIndexDict.AirQualityIndexScale.FAIR,
                25: AirQualityIndexDict.AirQualityIndexScale.MODERATE,
                50: AirQualityIndexDict.AirQualityIndexScale.POOR,
                75: AirQualityIndexDict.AirQualityIndexScale.VERY_POOR,
                800: AirQualityIndexDict.AirQualityIndexScale.EXTREMELY_POOR,
            }
        )

        pm10_treshold: AirQualityIndexDict = AirQualityIndexDict(
            {
                10: AirQualityIndexDict.AirQualityIndexScale.GOOD,
                20: AirQualityIndexDict.AirQualityIndexScale.FAIR,
                25: AirQualityIndexDict.AirQualityIndexScale.MODERATE,
                50: AirQualityIndexDict.AirQualityIndexScale.POOR,
                75: AirQualityIndexDict.AirQualityIndexScale.VERY_POOR,
                800: AirQualityIndexDict.AirQualityIndexScale.EXTREMELY_POOR,
            }
        )

        no2_treshold: AirQualityIndexDict = AirQualityIndexDict(
            {
                40: AirQualityIndexDict.AirQualityIndexScale.GOOD,
                90: AirQualityIndexDict.AirQualityIndexScale.FAIR,
                120: AirQualityIndexDict.AirQualityIndexScale.MODERATE,
                230: AirQualityIndexDict.AirQualityIndexScale.POOR,
                340: AirQualityIndexDict.AirQualityIndexScale.VERY_POOR,
                1000: AirQualityIndexDict.AirQualityIndexScale.EXTREMELY_POOR,
            }
        )

        o3_treshold: AirQualityIndexDict = AirQualityIndexDict(
            {
                50: AirQualityIndexDict.AirQualityIndexScale.GOOD,
                100: AirQualityIndexDict.AirQualityIndexScale.FAIR,
                130: AirQualityIndexDict.AirQualityIndexScale.MODERATE,
                240: AirQualityIndexDict.AirQualityIndexScale.POOR,
                380: AirQualityIndexDict.AirQualityIndexScale.VERY_POOR,
                800: AirQualityIndexDict.AirQualityIndexScale.EXTREMELY_POOR,
            }
        )

        so2_treshold: AirQualityIndexDict = AirQualityIndexDict(
            {
                100: AirQualityIndexDict.AirQualityIndexScale.GOOD,
                200: AirQualityIndexDict.AirQualityIndexScale.FAIR,
                350: AirQualityIndexDict.AirQualityIndexScale.MODERATE,
                500: AirQualityIndexDict.AirQualityIndexScale.POOR,
                750: AirQualityIndexDict.AirQualityIndexScale.VERY_POOR,
                1250: AirQualityIndexDict.AirQualityIndexScale.EXTREMELY_POOR,
            }
        )

        # TODO:? so far no thresholds found for these pollutants
        # c6h6_treshold: AirQualityIndexDict = AirQualityIndexDict(
        #     {
        #         "good": 0,
        #         "fair": 0,
        #         "moderate": 0,
        #         "poor": 0,
        #         "very poor": 0,
        #         "extremely poor": 0,
        #     }
        # )

        # co_treshold: AirQualityIndexDict = AirQualityIndexDict(
        #     {
        #         "good": 0,
        #         "fair": 0,
        #         "moderate": 0,
        #         "poor": 0,
        #         "very poor": 0,
        #         "extremely poor": 0,
        #     }
        # )

        pollutants: tuple[str, ...] = (
            "PM10",
            "PM2_5",
            "O3",
            "NO2",
            "SO2",
            "C6H6",
            "CO",
        )

        air_quality_descriptions: list[AirQualityIndexDict.AirQualityIndexScale] = []
        for pollutant in pollutants:
            pollutant_tresholds: AirQualityIndexDict = (
                locals()
                .get(f'{pollutant.lower()}_treshold', None)
            )
            self_pollutant: float | None = getattr(self, pollutant, None)
            if pollutant_tresholds and self_pollutant:
                pollutant_air_quality_description: AirQualityIndexDict.AirQualityIndexScale = \
                    pollutant_tresholds[self_pollutant]
                air_quality_descriptions.append(pollutant_air_quality_description)

        air_quality_index: AirQualityIndexDict.AirQualityIndexScale = \
            AirQualityIndexDict.get_air_quality_index(*air_quality_descriptions)

        if air_quality_index:
            return air_quality_index.name.replace('_', ' ')  # TODO: lowercase?

    def set_air_quality_index(self) -> None:
        self.air_quality_index = self.get_air_quality_index()


def smog_factory(*args, **kwargs) -> Smog:
    smog: Smog = Smog(*args, **kwargs)
    smog.set_air_quality_index()
    return smog


class Email(BaseModel):
    # TODO: ...
    email = TextField(null=False)


def main() -> None:
    print('-' * 40)
    print('Smog1')
    smog1: Smog = Smog(
        PM10=12,
        PM2_5=800,
        O3=291,
        NO2=20,
        SO2=2,
        C6H6=1,
        CO=40,
    )
    air_quality_index: str | None = smog1.get_air_quality_index()
    print(f"{air_quality_index = }")
    print(f"\nRepr of smog: {smog1!r}")
    print('-' * 40)
    # equivalent to
    smog2: Smog = smog_factory(
        PM10=12,
        PM2_5=800,
        O3=291,
        NO2=20,
        SO2=2,
        C6H6=1,
        CO=40,
    )
    print('\n')
    print('-' * 40)
    print('Smog2')
    print(vars(smog2))


if __name__ == '__main__':
    main()
