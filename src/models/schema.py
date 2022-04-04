from peewee import DatabaseProxy, Model, TextField, FloatField, FixedCharField, DateTimeField
from closest_dict import AirQualityIndexDict

sqlite_db = DatabaseProxy()


class BaseModel(Model):
    class Meta:
        database = sqlite_db


# TODO: JAKIES ID NA SITE?!
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
    CO_unit = FixedCharField(max_length=5, default="µg/m3")
    measurement_timestamp = DateTimeField(formats=r"%Y-%m-%d %H:%M:%S",
                                          null=False)
    ''' 2022-02-05 15:22:12 ''' # FIXME

    def __str__(self): # FIXME
        #  FIXME? return f"{vars(self)}"
        smog_str: str = \
            f"""
            {self.site=}
            {self.air_quality_index=}
            {self.measurement_timestamp=}
            {self.PM10=} {self.PM10_unit}
            {self.PM2_5=} {self.PM2_5_unit}
            {self.O3=} {self.O3_unit}
            {self.NO2=} {self.NO2_unit}
            {self.SO2=} {self.SO2_unit}
            {self.C6H6=} {self.C6H6_unit}
            {self.CO=} {self.CO_unit}
            """
        return smog_str

    def __repr_(self): # FIXME
        #  FIXME? return f"{vars(self)}"
        smog_str: str = \
            f"""
            {self.site=}
            {self.air_quality_index=}
            {self.measurement_timestamp=}
            {self.PM10=}
            {self.PM2_5=}
            {self.O3=}
            {self.NO2=}
            {self.SO2=}
            {self.C6H6=}
            {self.CO=}
            {self.PM10_unit=}
            {self.PM2_5_unit=}
            {self.O3_unit=}
            {self.NO2_unit=}
            {self.SO2_unit=}
            {self.C6H6_unit=}
            {self.CO_unit=}
            """
        return smog_str

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

        # FIXME ADD THESE VALUES?
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

        # FIXME SET QUALITY INDEX?!
        air_quality_index: AirQualityIndexDict.AirQualityIndexScale = \
            AirQualityIndexDict.get_air_quality_index(*air_quality_descriptions)

        if air_quality_index:
            return air_quality_index.name  # TODO: lowercase?


class Email(BaseModel):
    email = TextField(null=False)


def main() -> None:
    smog: Smog = Smog(  # FIXME CHANGE VALUES
        PM10=12,
        PM2_5=800,
        O3=291,
        NO2=20,
        SO2=2,
        C6H6=1,
        CO=40,
    )
    air_quality_index: str = smog.get_air_quality_index()
    print(f"{air_quality_index = }")


if __name__ == '__main__':
    main()
