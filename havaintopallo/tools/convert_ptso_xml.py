import argparse
import csv
import json
import sys

from havaintopallo.conversion import convert_measurement_xml


def main():
    ap = argparse.ArgumentParser(
        description="Convert FMI PointTimeSeriesObservations to JSONL or CSV"
    )
    ap.add_argument("--format", "-f", default="jsonl", choices=("jsonl", "csv"))
    ap.add_argument("files", nargs="*", metavar="FILE")
    args = ap.parse_args()
    cw = csv.writer(sys.stdout)
    if args.format == "csv":
        cw.writerow(["file", "id", "timestamp", "value"])

    if not args.files:
        ap.error("no files to process")

    for filename in args.files:
        print(filename, file=sys.stderr)
        with open(filename, "r") as infp:
            for triple in convert_measurement_xml(infp.read()):
                row = [filename] + list(triple)
                if args.format == "csv":
                    cw.writerow(row)
                else:
                    print(json.dumps(row))


if __name__ == "__main__":
    main()
