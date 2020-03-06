import warnings
import xml.etree.ElementTree as ET
from collections import namedtuple
from datetime import datetime
from typing import Iterable

namespaces = {
    "FMIAF": "http://xml.fmi.fi/namespace/om/atmosphericfeatures/1.0",
    "GML": "http://www.opengis.net/gml/3.2",
    "GMLCOV": "http://www.opengis.net/gmlcov/1.0",
    "OM": "http://www.opengis.net/om/2.0",
    "OMSO": "http://inspire.ec.europa.eu/schemas/omso/3.0",
    "SWE": "http://www.opengis.net/swe/2.0",
    "WFS": "http://www.opengis.net/wfs/2.0",
    "WML2": "http://www.opengis.net/waterml/2.0",
}

PointTimeSeriesObservation = namedtuple(
    "PointTimeSeriesObservation", ("id", "time", "value")
)

GridObservation = namedtuple(
    "GridObservation", ("position", "id", "value")
)

Spatiotemporal = namedtuple(
    "Spatiotemporal", ("lon", "lat", "time")
)


def convert_point_xml(xml_string) -> Iterable[PointTimeSeriesObservation]:
    xtree: ET.Element = ET.fromstring(xml_string)
    for ptso in xtree.findall(
        "WFS:member/OMSO:PointTimeSeriesObservation", namespaces=namespaces
    ):
        ts: ET.Element
        for ts in ptso.findall("*/WML2:MeasurementTimeseries", namespaces=namespaces):
            id = ts.attrib["{http://www.opengis.net/gml/3.2}id"]
            for tvp in ts.findall("*/WML2:MeasurementTVP", namespaces=namespaces):
                time = tvp.find("WML2:time", namespaces=namespaces)
                value = tvp.find("WML2:value", namespaces=namespaces)
                yield PointTimeSeriesObservation(id, time.text, value.text)


def convert_compound_crs_unixtime(pos_triple: tuple) -> Spatiotemporal:
    lon, lat, unixtime = pos_triple
    return Spatiotemporal(
        lon=float(lon),
        lat=float(lat),
        time=datetime.fromtimestamp(int(unixtime)),
    )


def convert_grid_xml(xml_string, *, position_converter=None) -> Iterable[GridObservation]:
    xtree: ET.Element = ET.fromstring(xml_string)
    for ptso in xtree.findall(
        "WFS:member/OMSO:GridSeriesObservation", namespaces=namespaces
    ):
        for mpc in ptso.findall("*/GMLCOV:MultiPointCoverage", namespaces=namespaces):
            # Parse domain set
            domain_set = mpc.find("GML:domainSet", namespaces=namespaces)
            smp = domain_set.find("GMLCOV:SimpleMultiPoint", namespaces=namespaces)
            if smp is not None:
                dimension_count = int(smp.attrib["srsDimension"])
                positions = smp.find("GMLCOV:positions", namespaces=namespaces).text.strip().split()
                positions = [
                    positions[ix: ix + dimension_count]
                    for ix in range(0, len(positions), dimension_count)
                ]
            else:
                warnings.warn("unsupported domainset in mpc")
                continue

            # Parse range types
            range_type = mpc.find("GMLCOV:rangeType", namespaces=namespaces)
            field_names = [fd.attrib["name"] for fd in range_type.findall("*/SWE:field", namespaces=namespaces)]

            range_set = mpc.find("GML:rangeSet", namespaces=namespaces)
            tlist = range_set.find("*/GML:doubleOrNilReasonTupleList", namespaces=namespaces)
            print(tlist)
            if tlist is not None:
                values = tlist.text.strip().split()
            else:
                warnings.warn("unsupported rangeset in mpc")
                continue

            for i, position in enumerate(positions):
                if position_converter:
                    position = position_converter(position)
                for field_name, value in zip(field_names, values[i * len(field_names):]):
                    yield GridObservation(position=position, id=field_name, value=value)
