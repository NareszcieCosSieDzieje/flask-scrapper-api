import pytest
from pytest_mock import MockerFixture

@pytest.mark.xfail("Not implemented")
def test_todo():
    pass


# FIXME ADD GLOBAL TESTS FOR PARSE_URLS TO SEE IF THE LIST IS FLAT!

def main() -> None:
    import sys
    sys.exit(pytest.main(["-qq -s"], plugins=[]))


if __name__ == "__main__":
    main()
