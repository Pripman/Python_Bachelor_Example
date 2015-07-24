#standard libs
from subprocess import Popen, PIPE
import os
import logging
import tempfile
import sys
from site import addsitedir
addsitedir("../libs")

#own libs
from notifier import Notifier
import config
from jobstreamreader import JobStreamReader
from dataaccesslayer import \
    dbread, \
    dbupdate


log = logging.getLogger("Verifyjob_script")

if config.debug():
    log.setLevel(logging.DEBUG)
else:
    log.setLevel(logging.INFO)


def getargument(index):
    if len(sys.argv) > index:
        return sys.argv[index]
    else:
        return None


def make_temp_xml_file(xml):
    fd, filename = tempfile.mkstemp(suffix='.xml', dir=config.tempxmldir)
    f = os.fdopen(fd, 'wt')
    f.write(xml)
    f.close()
    return filename


def make_command_array(filename, args):
    command_array = [config.verifytapath, filename]
    for arg in args:
        command_array.append(arg)

    return command_array


def runverifyta(xml, args, DBid):
    filename = make_temp_xml_file(xml)
    command_array = make_command_array(filename, args)
    log.info("Running {} with xmlfile:{}".format(config.verifytapath,
                                                 filename))
    p = Popen(command_array, stdout=PIPE, stderr=PIPE)
    reader = JobStreamReader(p.stdout, DBid)
    out = reader.startreading()
    _, err = p.communicate()

    if p.returncode != 0:
        log.error("""verifyta returned an error for job with uid:\n{},
                    the error was: {}""".format(DBid, err))
        return "---------------------------------------ERROR---------------------------! verifyta output:\n\n{}".format(err), err

    log.info("Verifyta finished")
    return out, ""


def write_to_db(DBid, res):
    #TODO: error handling, hvilke exceptions smider SQL?
    dbupdate.job_set_result(DBid, res)


def notify(jobid, ntypes):
    log.debug("ntypes in notify is {}".format(ntypes))
    for ntype in ntypes:
        log.info("Putting result into notifier queue:{} \
                with addr:{}".format(ntype["ntype"], ntype["naddr"]))

        notifier = Notifier(config.redisserver, ntype["ntype"])
        notifier.notify(jobid, ntype["naddr"])


def main():
    log.info("Starting script on node")
    DBid = getargument(1)
    xml, args, ntypes = dbread.job_execution_data(DBid)
    log.info("Recived args, {} from database \
            with ntypes {}".format(args, ntypes))

    if xml is None:
        log.error("Could not find the database id: {}".format(DBid))
        return

    res, err = runverifyta(xml, args, DBid)
    if not (err == ""):
        #TODO:handle this
        log.error("NOT IMPLEMENTED: Handle error in verifyta:{}".format(err))
        write_to_db(DBid, err)
    else:
        write_to_db(DBid, res)
        notify(DBid, ntypes)

if __name__ == "__main__":
    main()
