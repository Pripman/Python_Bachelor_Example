from verifyjob import make_command_array
from site import addsitedir
from os import path
addsitedir("../libs")
import config


def test_make_command_array():
    args = ["-t", "0", "-o", "0", "-n", "0"]

    xmlpath = path.join("tests", "train-gate.xml")
    command_array = make_command_array(xmlpath, args)

    expected_array = [config.verifytapath, xmlpath,
                      "-t", "0", "-o", "0", "-n", "0"]

    assert command_array == expected_array
