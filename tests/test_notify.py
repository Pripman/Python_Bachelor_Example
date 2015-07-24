from verifyjob import notify
from site import addsitedir
addsitedir("../libs")
from notifier import Notifier
import uuid
import config


def test_notify():
    ntype1 = str(uuid.uuid1())
    ntype2 = str(uuid.uuid1())

    ntypes = [{"ntype": ntype1, "naddr": "127.0.0.1"},
              {"ntype": ntype2, "naddr": "test@test.com"}]

    notifier1 = Notifier(config.redisserver, ntype1)
    notifier2 = Notifier(config.redisserver, ntype2)

    notify("test-id", ntypes)

    jid, data = notifier1.get()
    assert data == "127.0.0.1"

    jid, data = notifier2.get()
    assert data == "test@test.com"
