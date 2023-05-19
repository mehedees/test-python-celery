from datetime import datetime

from cassandra.cqlengine import columns

from cassandra.cqlengine.models import Model


class TestModel(Model):
    __keyspace__ = "test_db"

    req_number = columns.Integer(primary_key=True)
    req_exec = columns.Boolean()
    req_rec = columns.Boolean()
    rec_ack = columns.Boolean()
    created_at = columns.DateTime(default=datetime.now)
    updated_at = columns.DateTime(default=datetime.now)
