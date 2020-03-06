from havaintopallo.conversion import convert_grid_xml, convert_compound_crs_unixtime


def test_grid_conversion():
    with open("examples/grid_hirlam.xml") as infp:
        obs = list(convert_grid_xml(infp.read(), position_converter=convert_compound_crs_unixtime))
        assert obs  # TODO: Improve test
