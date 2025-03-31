from havaintopallo.conversion import (
    convert_compound_crs_unixtime,
    convert_grid_xml,
    convert_point_xml,
)


def test_grid_conversion():
    with open("examples/grid_hirlam.xml") as infp:
        obs = list(convert_grid_xml(infp.read(), position_converter=convert_compound_crs_unixtime))
        assert obs  # TODO: Improve test


def test_point_conversion():
    with open("examples/point_harmonie.xml") as infp:
        obs = list(convert_point_xml(infp.read()))
        assert obs  # TODO: Improve test
