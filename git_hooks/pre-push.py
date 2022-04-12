#!/usr/bin/env python

# FIXME JESZCZE NIE DZIALA DOBRZE BO STDERROR NIE OGARNIETY!

import sys

__MAJOR_VERSION__: int = 3
__MINOR_VERSION__: int = 10

if (
    sys.version_info.major < __MAJOR_VERSION__
    or sys.version_info.minor < __MINOR_VERSION__
):

    sys.exit(
        f"Used Python version ({sys.version_info.major}.{sys.version_info.minor}) "
        f"for githook is below {__MAJOR_VERSION__}.{__MINOR_VERSION__}"
    )

# print(sys.executable)

from pathlib import Path

project_dir: Path = Path(__file__).parent.parent.parent

venv_subdir_exists: bool = False
test_subdir_exists: bool = False

if project_dir.is_dir():
    for sub_dir in project_dir.iterdir():
        match sub_dir.name:
            case "tests":
                test_subdir_exists = True
            case "venv":
                venv_subdir_exists = True

if venv_subdir_exists and test_subdir_exists:

    import platform

    platform_str: str = platform.system().lower()

    os_cmd: list[str] = []

    if "lin" in platform_str:
        os_cmd = [
            "bash",
            "-c",
            "source ./venv/scripts/activate",
            "&&",
            "python -m pytest tests",
        ]
    elif "darwin" in platform_str:
        pass
    elif "win" in platform_str:
        os_cmd = [
            "powershell",
            "-Command",
            r".\venv\Scripts\activate",
            "; if($?)",
            "{python -m pytest tests}",
        ]

    import subprocess

    result = subprocess.run(os_cmd, capture_output=True, text=True)
    print("stdout:", result.stdout)
    print("stderr:", result.stderr)

    if result.stderr:
        print(
            'The tests failed! Push stopped.\nTo skip the hooks try "git push --no-verify"'
        )
        sys.exit(1)
