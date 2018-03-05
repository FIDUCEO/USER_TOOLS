import sys

from fiduceo.tool.radprop.rad_prop_processor import RadPropProcessor


def main(args=None):
    processor = RadPropProcessor()
    processor.run(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
