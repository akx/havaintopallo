import datetime

import httpx


def download_fmi_observation_xml(
    httpx_client: httpx.Client,
    fmisid: str,
    start_time: datetime.datetime,
    end_time: datetime.datetime,
) -> str:
    resp = httpx_client.get(
        "https://opendata.fmi.fi/wfs",
        params={
            "request": "getFeature",
            "storedquery_id": "fmi::observations::weather::timevaluepair",
            "crs": "EPSG::3067",
            "fmisid": fmisid,
            "starttime": start_time.isoformat(sep="T"),
            "endtime": end_time.isoformat(sep="T"),
        },
    )
    resp.raise_for_status()
    return resp.text
