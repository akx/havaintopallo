import xml.etree.ElementTree as ET
from collections import namedtuple
from typing import Iterable

namespaces = {
    "OMSO": "http://inspire.ec.europa.eu/schemas/omso/3.0",
    "OM": "http://www.opengis.net/om/2.0",
    "WFS": "http://www.opengis.net/wfs/2.0",
    "FMIAF": "http://xml.fmi.fi/namespace/om/atmosphericfeatures/1.0",
    "WML2": "http://www.opengis.net/waterml/2.0",
    "GML": "http://www.opengis.net/gml/3.2",
}

PointTimeSeriesObservation = namedtuple(
    "PointTimeSeriesObservation", ("id", "time", "value")
)


def convert_measurement_xml(xml_string) -> Iterable[PointTimeSeriesObservation]:
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
