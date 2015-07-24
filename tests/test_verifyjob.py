from verifyjob import runverifyta
import uuid


def test_runverifyta():
    uid = uuid.uuid1()
    with open("tests/train-gate-output.txt", "r") as f:
        output = f.read()

    with open("tests/train-gate.xml", "r") as f:
        inputstring = f.read()

    args = ["-t", "0"]

    partial_verify_output = runverifyta(inputstring, args, uid)[0]
    out = output.split("\n")
    off = partial_verify_output.split("\n")
    verify_outputs(out, off, ["Seed", "-- Throughput"])

    print(partial_verify_output)
    print("==" * 30)
    print(output)


def verify_outputs(out, off, not_check):
    for it in not_check:
        out = filter(lambda x:  x.startswith(it), out)
        off = filter(lambda x:  x.startswith(it), off)

    for i in range(0, len(out)):
        assert out[i] == off[i]
