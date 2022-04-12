import pytest
from typing import Any

from src.models.closest_dict import ClosestDict, AirQualityIndexDict


class TestClosestDict:

    @pytest.fixture(scope="function")
    def temperature_dict(self) -> ClosestDict:
        return ClosestDict(
            {
                -20: 'Super Freezing',
                -10: 'Freezing',
                0: 'Cold',
                10: 'Chilly',
                20: 'Warm',
                30: 'Hot',
            }
        )

    @pytest.fixture(scope="class")
    def shared_dict(self) -> ClosestDict():
        return ClosestDict()

    @pytest.mark.parametrize('key,closest_key',
        [
            (-100, -20),
            (-21, -20),
            (-20, -10),
            (-11, -10),
            (-10, 0),
            (-1, 0),
            (0, 10),
            (5, 10),
            (10, 20),
            (19, 20),
            (20, 30),
            (27, 30),
            (30, 30),
            (41, 30),
        ]
    )
    def test_get_closest_key_ceiling(
        self,
        temperature_dict: ClosestDict,
        key: int,
        closest_key: int
    ):
        assert closest_key == temperature_dict._get_closest_key_ceiling(key)

    @pytest.mark.parametrize('key,value',
        [
            (-124, "Some String Value"),
            (-124, 999),
            (-124, 12.05),
            (-124, -5.2),
        ]
    )
    def test__setitem__(
        self,
        shared_dict: ClosestDict,
        key: int | float,
        value: Any
    ):
        shared_dict[key] = value
        assert shared_dict[key] == value

    @pytest.mark.parametrize("temperature,description",
        [
            (-80, "Super Freezing"),
            (-70, "Super Freezing"),
            (-21, "Super Freezing"),
            (-20, "Freezing"),
            (-11, "Freezing"),
            (-10, "Cold"),
            (-1, "Cold"),
            (0, "Chilly"),
            (2, "Chilly"),
            (9, "Chilly"),
            (10, "Warm"),
            (16, "Warm"),
            (19, "Warm"),
            (20, "Hot"),
            (31, "Hot"),
            (40, "Hot"),
            (50, "Hot"),
            (70, "Hot"),
        ]
    )
    def test__getitem__(self, temperature_dict, temperature, description):
        assert temperature_dict[temperature] == description

    @pytest.mark.parametrize("non_number_key",
        [
            ("some string", ),
            ((1, 2), ),
            (("a", "b", "c"), ),
            ([1, 2, "3"], ),
        ]
    )
    def test_integer_key_restriction__setitem__(self, non_number_key: Any):
        closest_dict: ClosestDict = ClosestDict()
        with pytest.raises(ValueError) as NonNumberValueError:  # FIXME e
            closest_dict[non_number_key] = None
            assert (
                "Dictionary accepts number keys only (int | float)."
                in str(NonNumberValueError.value)
            )

    @pytest.mark.parametrize("non_number_key",
        [
            ("some string", ),
            ((1, 2), ),
            (("a", "b", "c"), ),
            ([1, 2, "3"], ),
        ]
    )
    def test_integer_key_restriction__getitem__(
        self,
        temperature_dict: ClosestDict,
        non_number_key: Any
    ):
        with pytest.raises(ValueError) as NonNumberValueError:
            _ = temperature_dict[non_number_key]
            assert (
                "Dictionary accepts number keys only (int | float)."
                in str(NonNumberValueError.value)
            )

    def test_empty_dict__getitem__(self):
        empty_dict: ClosestDict = ClosestDict()
        with pytest.raises(KeyError) as EmptyDictKeyError:
            key: int = 10
            _ = empty_dict[key]
            assert (
                f"Cannot get value for key: ({key}) from an empty dictionary."
                in str(EmptyDictKeyError.value)
            )

    def test_lower_bound__getitem__(
        self,
        temperature_dict: ClosestDict
    ):
        import sys
        with pytest.raises(KeyError) as LowerBoundKeyError:
            key: int = ~sys.maxsize - 1
            _ = temperature_dict[key]
            assert (
                f"Given key: ({key}) is less than the lower bound: ({temperature_dict.lower_bound})"
                in str(LowerBoundKeyError.value)
            )


class TestAirQualityIndexDict:

    @pytest.fixture(scope="class")
    def pm2_5_treshold(self) -> AirQualityIndexDict:
        return AirQualityIndexDict(
            {
                10: AirQualityIndexDict.AirQualityIndexScale.GOOD,
                20: AirQualityIndexDict.AirQualityIndexScale.FAIR,
                25: AirQualityIndexDict.AirQualityIndexScale.MODERATE,
                50: AirQualityIndexDict.AirQualityIndexScale.POOR,
                75: AirQualityIndexDict.AirQualityIndexScale.VERY_POOR,
                800: AirQualityIndexDict.AirQualityIndexScale.EXTREMELY_POOR,
            }
        )

    @pytest.fixture(scope="class")
    def pm10_treshold(self) -> AirQualityIndexDict:
        return AirQualityIndexDict(
            {
                10: AirQualityIndexDict.AirQualityIndexScale.GOOD,
                20: AirQualityIndexDict.AirQualityIndexScale.FAIR,
                25: AirQualityIndexDict.AirQualityIndexScale.MODERATE,
                50: AirQualityIndexDict.AirQualityIndexScale.POOR,
                75: AirQualityIndexDict.AirQualityIndexScale.VERY_POOR,
                800: AirQualityIndexDict.AirQualityIndexScale.EXTREMELY_POOR,
            }
        )

    @pytest.fixture(scope="class")
    def no2_treshold(self) -> AirQualityIndexDict:
        return AirQualityIndexDict(
            {
                40: AirQualityIndexDict.AirQualityIndexScale.GOOD,
                90: AirQualityIndexDict.AirQualityIndexScale.FAIR,
                120: AirQualityIndexDict.AirQualityIndexScale.MODERATE,
                230: AirQualityIndexDict.AirQualityIndexScale.POOR,
                340: AirQualityIndexDict.AirQualityIndexScale.VERY_POOR,
                1000: AirQualityIndexDict.AirQualityIndexScale.EXTREMELY_POOR,
            }
        )

    @pytest.fixture(scope="class")
    def o3_treshold(self) -> AirQualityIndexDict:
        return AirQualityIndexDict(
            {
                50: AirQualityIndexDict.AirQualityIndexScale.GOOD,
                100: AirQualityIndexDict.AirQualityIndexScale.FAIR,
                130: AirQualityIndexDict.AirQualityIndexScale.MODERATE,
                240: AirQualityIndexDict.AirQualityIndexScale.POOR,
                380: AirQualityIndexDict.AirQualityIndexScale.VERY_POOR,
                800: AirQualityIndexDict.AirQualityIndexScale.EXTREMELY_POOR,
            }
        )

    @pytest.fixture(scope="class")
    def so2_treshold(self) -> AirQualityIndexDict:
        return AirQualityIndexDict(
            {
                100: AirQualityIndexDict.AirQualityIndexScale.GOOD,
                200: AirQualityIndexDict.AirQualityIndexScale.FAIR,
                350: AirQualityIndexDict.AirQualityIndexScale.MODERATE,
                500: AirQualityIndexDict.AirQualityIndexScale.POOR,
                750: AirQualityIndexDict.AirQualityIndexScale.VERY_POOR,
                1250: AirQualityIndexDict.AirQualityIndexScale.EXTREMELY_POOR,
            }
        )

    class TestAirQualityIndexScale:

        def test_air_quality_index_scale_gt(self):
            assert (
                AirQualityIndexDict.AirQualityIndexScale.GOOD >
                AirQualityIndexDict.AirQualityIndexScale.FAIR >
                AirQualityIndexDict.AirQualityIndexScale.MODERATE >
                AirQualityIndexDict.AirQualityIndexScale.POOR >
                AirQualityIndexDict.AirQualityIndexScale.VERY_POOR >
                AirQualityIndexDict.AirQualityIndexScale.EXTREMELY_POOR
            )

        def test_air_quality_index_scale_lt(self):
            assert (
                AirQualityIndexDict.AirQualityIndexScale.EXTREMELY_POOR <
                AirQualityIndexDict.AirQualityIndexScale.VERY_POOR <
                AirQualityIndexDict.AirQualityIndexScale.POOR <
                AirQualityIndexDict.AirQualityIndexScale.MODERATE <
                AirQualityIndexDict.AirQualityIndexScale.FAIR <
                AirQualityIndexDict.AirQualityIndexScale.GOOD
            )

        def test_air_quality_index_scale_min(
            self,
            pm2_5_treshold: AirQualityIndexDict,
            pm10_treshold: AirQualityIndexDict,
            no2_treshold: AirQualityIndexDict,
            o3_treshold: AirQualityIndexDict,
            so2_treshold: AirQualityIndexDict
        ):
            min: AirQualityIndexDict.AirQualityIndexScale = \
                AirQualityIndexDict.AirQualityIndexScale.min(
                    pm2_5_treshold[9],  # good
                    pm10_treshold[11],  # fair
                    no2_treshold[119],  # moderate
                    o3_treshold[239],  # poor
                    so2_treshold[749],  # very poor
                )
            assert (
                min == AirQualityIndexDict.AirQualityIndexScale.VERY_POOR
            )

        def test_air_quality_index_scale_max(
            self,
            pm2_5_treshold: AirQualityIndexDict,
            pm10_treshold: AirQualityIndexDict,
            no2_treshold: AirQualityIndexDict,
            o3_treshold: AirQualityIndexDict,
            so2_treshold: AirQualityIndexDict
        ):
            max: AirQualityIndexDict.AirQualityIndexScale = \
                AirQualityIndexDict.AirQualityIndexScale.max(
                    pm2_5_treshold[9],  # good
                    pm10_treshold[11],  # fair
                    no2_treshold[119],  # moderate
                    o3_treshold[239],  # poor
                    so2_treshold[749],  # very poor
                )
            assert (
                max == AirQualityIndexDict.AirQualityIndexScale.GOOD
            )

        def test_air_quality_index_scale_min_raises_value_error(
            self,
            pm2_5_treshold: AirQualityIndexDict,
            pm10_treshold: AirQualityIndexDict,
            no2_treshold: AirQualityIndexDict,
            o3_treshold: AirQualityIndexDict,
            so2_treshold: AirQualityIndexDict
        ):
            with pytest.raises(ValueError) as ArgsValueError:
                AirQualityIndexDict.AirQualityIndexScale.min(
                    pm2_5_treshold[9],  # good
                    pm10_treshold[11],  # fair
                    no2_treshold[119],  # moderate
                    o3_treshold[239],  # poor
                    so2_treshold[749],  # very poor
                    "some label",
                    1,
                    2.2,
                )
                assert (
                    ("Method accepts "
                     "AirQualityIndexDict.AirQualityIndexScale arguments only.")
                    in str(ArgsValueError.value)
                )

    def test_get_air_quality_index(
        self,
        pm2_5_treshold: AirQualityIndexDict,
        pm10_treshold: AirQualityIndexDict,
        no2_treshold: AirQualityIndexDict,
        o3_treshold: AirQualityIndexDict,
        so2_treshold: AirQualityIndexDict
    ):
        min: AirQualityIndexDict.AirQualityIndexScale = \
            AirQualityIndexDict.get_air_quality_index(
                *(
                    pm2_5_treshold[9],  # good
                    pm10_treshold[11],  # fair
                    no2_treshold[119],  # moderate
                    o3_treshold[239],  # poor
                    so2_treshold[749],  # very poor
                )
            )

        assert (
            min == AirQualityIndexDict.AirQualityIndexScale.VERY_POOR
        )


def main() -> None:
    import sys
    sys.exit(pytest.main(["-qq -s"], plugins=[]))


if __name__ == '__main__':
    main()
