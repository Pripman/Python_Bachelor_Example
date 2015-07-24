from os import path
from verifyjob import make_temp_xml_file


def test_make_temp_xml_file():
    with open("tests/train-gate.xml", "r") as f:
        xml = f.read()

    temp_xml_file = make_temp_xml_file(xml)
    temp_file_created = path.exists(temp_xml_file)

    assert temp_file_created

    if temp_file_created:
        with open(temp_xml_file, "r") as t:
            temp_file_content = t.read()

        assert temp_file_content == xml
