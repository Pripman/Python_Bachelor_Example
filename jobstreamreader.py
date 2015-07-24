#standard libs
from threading import Thread
from subprocess import Popen, PIPE
import sys
import logging
import site
site.addsitedir("../libs")

#own libs
import config
from dhash import DistributedHash

log = logging.getLogger("verifyta_statusreader")

if config.debug():
    log.setLevel(logging.DEBUG)
else:
    log.setLevel(logging.INFO)


class JobStreamReader:
    def __init__(self, stream, uid):
        self._stream = stream
        self._uid = uid
        self._loadtable = DistributedHash("uppaal_load")
        self._throughputtable = DistributedHash("uppaal_throughput")
        self._finalresult = ""

    def startreading(self):
        log.info("Started reading output from verifyta with id: {}"
                 .format(self._uid))
        while True:
            word = self._next_word()
            if(word is None):
                return self._finalresult
            if word == "Load:":
                log.info("read Load")
                self._loadtable[self._uid] = self._next_word()
                sys.stdout.flush()

            if word == "Throughput:":
                self._throughputtable[self._uid] = self._next_word()
                sys.stdout.flush()

    def _next_word(self):
        word = ""
        out = self._readchar()
        if(out == ""):
            return None

        while out == " ":
            out = self._readchar()

        while out != " " and out != "":
            word += out
            out = self._readchar()

        return word

    def _readchar(self):
        out = self._stream.read(1)
        self._finalresult += out
        return out

if __name__ == "__main__":
    p = Popen([config.verifytapath, "../xmlfiles/train-gate.xml"],
              stdout=PIPE, stderr=PIPE)
    reader = JobStreamReader(p.stdout, "asdasd")
    output = reader.startreading()
    log.info("output was {}".format(output))
