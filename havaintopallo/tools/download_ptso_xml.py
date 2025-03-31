import argparse
import datetime
import gzip
import os

import httpx

from havaintopallo.download import download_fmi_observation_xml


def generate_date_pairs(start_date, end_date, delta):
    while start_date < end_date:
        date2 = start_date + delta
        yield (start_date, date2)
        start_date = date2


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--fmisid",
        required=True,
        help="FMI location ID (100949 for Turku!)",
        type=int,
    )
    ap.add_argument(
        "--start-date",
        required=True,
        help="Start date (ISO format)",
    )
    ap.add_argument(
        "--end-date",
        required=True,
        help="End date (ISO format)",
        default=datetime.date.today().isoformat(),
    )
    ap.add_argument("--dest-dir", default=".")
    ap.add_argument(
        "--compression",
        choices=["none", "gzip", "zstd"],
        default="none",
    )
    args = ap.parse_args()
    return args


def main():
    args = parse_args()
    start_date = datetime.date.fromisoformat(args.start_date)
    end_date = datetime.date.fromisoformat(args.end_date)
    assert end_date > start_date
    midnight = datetime.time()
    jobs = [
        (
            f"{args.fmisid}_{d1}_{d2}.xml",
            dict(
                fmisid=args.fmisid,
                start_time=datetime.datetime.combine(d1, midnight),
                end_time=datetime.datetime.combine(d2, midnight),
            ),
        )
        for (d1, d2) in generate_date_pairs(start_date, end_date, datetime.timedelta(days=7))
    ]
    os.makedirs(args.dest_dir, exist_ok=True)
    comp = args.compression
    with httpx.Client() as client:
        # TODO: could add multiprocessing here :)
        for i, (filename, job) in enumerate(jobs, 1):
            full_filename = os.path.join(args.dest_dir, filename)
            if comp != "none":
                if comp == "gzip":
                    full_filename += ".gz"
                elif comp == "zstd":
                    full_filename += ".zst"

            print(f"{i:d} / {len(jobs):d} – {full_filename} ...")
            if os.path.isfile(full_filename):
                print("  -> [*] skipping, already exists")
                continue
            xml = download_fmi_observation_xml(httpx_client=client, **job)
            write_file(full_filename, xml, comp)


def write_file(full_filename: str, xml_text: str, compression):
    assert "UTF-8" in xml_text
    xml_bytes = xml_text.encode("utf-8")
    if compression == "gzip":
        with gzip.open(full_filename, "wb") as outf:
            outf.write(xml_bytes)
    elif compression == "zstd":
        import zstandard

        with zstandard.open(full_filename, "wb") as outf:
            outf.write(xml_bytes)
    else:
        with open(full_filename, "wb") as outf:
            outf.write(xml_bytes)
    print(f"  -> [+] {os.path.getsize(full_filename)} bytes (compression: {compression})")


if __name__ == "__main__":
    main()
