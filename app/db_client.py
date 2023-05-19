import os

from cassandra.cluster import Cluster, Session, ShardAwareOptions
from cassandra.cqlengine import connection, management
from cassandra.io.eventletreactor import EventletConnection
from cassandra.policies import DCAwareRoundRobinPolicy

from .db_model import TestModel


CQLELGN_CONN_NAME = "cqlengine"
CQLELGN_SYNC_CONN_NAME = "cqlengine_sync"


class DB:
    cluster: Cluster = None
    session: Session = None


db = DB()


def create_session() -> Session:
    cluster = Cluster(
        ['scylla'],
        connection_class=EventletConnection,
        protocol_version=4,
        shard_aware_options=ShardAwareOptions(disable=True, disable_shardaware_port=True),
        load_balancing_policy=DCAwareRoundRobinPolicy(local_dc='datacenter1')
    )
    db.cluster = cluster
    session: Session = cluster.connect()
    return session


async def connect_to_db_async():
    session: Session = create_session()
    os.environ["CQLENG_ALLOW_SCHEMA_MANAGEMENT"] = "true"
    connection.register_connection(CQLELGN_CONN_NAME, session=session, default=True)
    # Need to create keyspace for the first time or create with cqlsh
    # management.create_keyspace_simple('test_db', replication_factor=1)
    session.set_keyspace('test_db')
    management.sync_table(TestModel)
    db.session = session


def connect_to_db_sync():
    session: Session = create_session()
    connection.register_connection(CQLELGN_SYNC_CONN_NAME, session=session, default=True)
    session.set_keyspace('test_db')
    db.session = session


def shutdown_db(conn_name: str):
    if db.session is not None:
        db.session.shutdown()
        db.session = None
    if db.cluster is not None:
        db.cluster.shutdown()
        db.cluster = None
    connection.unregister_connection(conn_name)


async def shutdown_db_async():
    shutdown_db(CQLELGN_CONN_NAME)


def shutdown_db_sync():
    shutdown_db(CQLELGN_SYNC_CONN_NAME)
