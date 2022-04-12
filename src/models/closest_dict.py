from typing import Any, Callable
from functools import wraps
import sys
from enum import Enum
# from collections.abc import MutableMapping


class ClosestDict(dict):

    @classmethod
    def __new__(cls, *args, **kwargs):
        if(
            (
                args and type(args) is dict
                and any(list(map(lambda k: type(k) not in (int, float), args.keys())))
            )
            or
            (
                kwargs and type(kwargs) is dict
                and any(list(map(lambda k: type(k) not in (int, float), kwargs.keys())))
            )
        ):
            raise ValueError("Dictionary accepts number keys only (int | float).")
        return super(ClosestDict, cls).__new__(cls)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lower_bound: int = ~sys.maxsize  # FIXME?!
        self.upper_bound: int = sys.maxsize

    @staticmethod
    def _is_key_valid(func: Callable) -> Callable:
        wraps(func)

        def wrapper(self, key: int | float | None, value: Any | None = None) -> Any:
            if type(key) not in (int, float):
                raise ValueError("Dictionary accepts integer and float keys only.")
            elif key < self.lower_bound:
                raise KeyError(
                    f"Given key: ({key}) is less than the lower bound: ({self.lower_bound})"
                )
            if func.__name__ == "__setitem__":
                return func(self, key, value)
            return func(self, key)
        return wrapper

    def _get_closest_key_ceiling(self, key: int | float) -> int | None:

        keys: list[int] = sorted(self.keys())
        last_key_idx: int = len(keys) - 1
        return next(
            (k for i, k in enumerate(keys) if key >= k and i >= last_key_idx or key < k),
            None
        )

    @_is_key_valid
    def __getitem__(self, key: int | float):
        if len(self) == 0:
            raise KeyError(f"Cannot get value for key: ({key}) from an empty dictionary.")
        new_key: int | None = self._get_closest_key_ceiling(key)
        return super(ClosestDict, self).__getitem__(new_key)

    @_is_key_valid
    def __setitem__(self, key: int | float, value: Any):
        return super(ClosestDict, self).__setitem__(key, value)

    @_is_key_valid
    def __delitem__(self, key: int | float):
        if key not in self:
            key = self.__getitem__(key)
        super(ClosestDict, self).__delitem__(key)

    def __str__(self) -> str:
        sorted_index_dict: dict[int | float, Any] = dict(sorted(self.items(), key=lambda k: k[0]))
        return f"{sorted_index_dict}"

    def __repr__(self):
        return f"{type(self).__name__}({self})"

    # def update(self, *args, **kwargs):
    #     for k, v in dict(*args, **kwargs).iteritems():
    #         self[k] = v


class AirQualityIndexDict(ClosestDict):

    class AirQualityIndexScale(Enum):  # FIXME ADD A POLISH MAPPING?
        EXTREMELY_POOR = 0
        VERY_POOR = 1
        POOR = 2
        MODERATE = 3
        FAIR = 4
        GOOD = 5

        def __gt__(self, other) -> bool:
            return self.value > other.value

        def __lt__(self, other) -> bool:
            return self.value < other.value

        @staticmethod
        def _check_args(func: Callable) -> Callable:
            wraps(func)

            def wrapper(*args):
                if any(
                    type(a) is not AirQualityIndexDict.AirQualityIndexScale for a in args
                ):
                    raise ValueError(
                        "Method accepts "
                        "AirQualityIndexDict.AirQualityIndexScale arguments only."
                    )
                return func(*args)
            return wrapper

        @staticmethod
        @_check_args
        def min(*args):
            ascending_list: list[AirQualityIndexDict.AirQualityIndexScale] = \
                list(sorted(args))
            if ascending_list:
                return ascending_list[0]

        @staticmethod
        @_check_args
        def max(*args):
            descending_list: list[AirQualityIndexDict.AirQualityIndexScale] = \
                list(sorted(args, reverse=True))
            if descending_list:
                return descending_list[0]

    def __init__(self, *args, **kwargs):
        if(
            (
                args and type(args) is dict
                and any(list(map(
                    lambda k: type(k) is not AirQualityIndexDict.AirQualityIndexScale,
                    args.values()))
                )
            )
            or
            (
                kwargs and type(kwargs) is dict
                and any(list(map(
                    lambda k: type(k) is not AirQualityIndexDict.AirQualityIndexScale,
                    kwargs.values()))
                )
            )
        ):
            raise ValueError(
                "Dictionary accepts "
                "AirQualityIndexDict.AirQualityIndexScale values only."
            )
        super(AirQualityIndexDict, self).__init__(*args, **kwargs)
        self.lower_bound: float = 0.0

    @staticmethod
    def get_air_quality_index(*args):
        return AirQualityIndexDict.AirQualityIndexScale.min(*args)


def main() -> None:
    x = AirQualityIndexDict(
        {
            1: '2',
            20: '20',
            7: '19',
        }
    )
    print(f"{x=}")
    z = x[14]
    print(f"{z=}")
    print(f"{x!r}")
    del x[1]
    print(x)


if __name__ == '__main__':
    main()
