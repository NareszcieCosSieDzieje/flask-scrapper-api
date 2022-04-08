import pytest
from pytest_mock import MockerFixture



def main() -> None:
    import sys
    sys.exit(pytest.main(["-qq -s"], plugins=[]))


if __name__ == '__main__':
    main()
