import argparse
import datetime
import os

import requests

from havaintopallo.download import download_fmi_observation_xml


def generate_date_pairs(start_date, end_date, delta):
    while start_date < end_date:
        date2 = start_date + delta
        yield (start_date, date2)
        start_date = date2


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fmisid", required=True, help="FMI location ID (100949 for Turku!)")
    ap.add_argument("--start-date", required=True, help="Start date (ISO format)")
    ap.add_argument("--end-date", required=True, help="End date (ISO format)")
    ap.add_argument("--dest-dir", default=".")
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
    # TODO: could add multiprocessing here :)
    os.makedirs(args.dest_dir, exist_ok=True)
    sess = requests.Session()
    for i, (filename, job) in enumerate(jobs, 1):
        full_filename = os.path.join(args.dest_dir, filename)
        print(f"{i:d} / {len(jobs):d} – {full_filename} ...")
        if os.path.isfile(full_filename):
            print("  -> [*] skipping, already exists")
            continue
        xml = download_fmi_observation_xml(requests_session=sess, **job)
        with open(full_filename, "w") as outf:
            outf.write(xml)
            print(f"  -> [+] {outf.tell()} bytes")


if __name__ == "__main__":
    main()
