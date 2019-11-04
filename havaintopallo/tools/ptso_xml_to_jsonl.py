import argparse
import json

from havaintopallo.conversion import convert_measurement_xml


def main():
    ap = argparse.ArgumentParser(
        description="Convert FMI PointTimeSeriesObservations to JSONL"
    )
    ap.add_argument("files", nargs="*", metavar="FILE")
    args = ap.parse_args()
    for filename in args.files:
        with open(filename, "r") as infp:
            for triple in convert_measurement_xml(infp.read()):
                print(json.dumps([filename] + list(triple)))


if __name__ == "__main__":
    main()
