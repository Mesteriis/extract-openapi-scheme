import argparse

from extractor import Extractor

parser = argparse.ArgumentParser(prog="extract-openapi.py")
parser.add_argument("app", help='App import string. Eg. "main:app"', default="main:app")
parser.add_argument(
    "--out",
    help="Output file ending in .json or .yaml",
    default="openapi.json",
)

PASS = 0
FAIL = 1


def main() -> int:
    args = parser.parse_args()
    try:
        ext = Extractor(args.app)
        ext.extract_scheme()
        ext.save()
    except Exception as e:  # noqa: BLE001
        print(f"Error: {e}")  # noqa
        return FAIL

    return PASS


if __name__ == "__main__":
    raise SystemExit(main())
