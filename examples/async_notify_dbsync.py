#!/usr/bin/env python
""" The idea is to copy all changes from magic_project to magic_project_mirror using postgresql notifications to get
updates from the DB and in this way, keep both tables on data sync.
This is a proof of concept to use python3 + asyncio + ThreadPoolExecutor + Postgresql notifications + psycopg2 +
sqlalchemy.
If you want to perform the same operation is highly recommended ed that you choose a different approach as might be
triggers + postgres_fdw at the postgresql DB or any supported replication mechanism """

import os
import asyncio
import signal
import json
from functools import partial
from concurrent.futures import ThreadPoolExecutor
import psycopg2
import psycopg2.extensions
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from shared.models import MagicProjectMirror


db = {'user': 'twdb',
      'password': 'twdb',
      'host': 'localhost',
      'port': '5432',
      'dbname': 'twdb',
      'channel': 'events'}


def listen(channel, dbconn):
    """ Listen to a channel """
    curs = dbconn.cursor()
    curs.execute('LISTEN {0};'.format(channel))


def insert_mirror(session, payload):
    data = json.loads(payload)
    if data['operation'] == 'INSERT':
        mpm = MagicProjectMirror(**data['data'])
        session.add(mpm)
    elif data['operation'] == 'UPDATE':
        mpm = session.query(MagicProjectMirror).filter(MagicProjectMirror.id == data['data']['id']).first()
        for k, d in data['data'].items():
            setattr(mpm, k, d)
    elif data['operation'] == 'DELETE':
        mpm = session.query(MagicProjectMirror).filter(MagicProjectMirror.id == data['data']['id']).first()
        session.delete(mpm)
    session.commit()


def receive(pool, loop, dbconn, mirror):
    """ Receive a notify message from the channel we are listening to """
    state = dbconn.poll()
    if state == psycopg2.extensions.POLL_OK:
        if dbconn.notifies:
            while len(dbconn.notifies) != 0:
                notify = dbconn.notifies.pop()
                loop.run_in_executor(pool, partial(mirror, payload=notify.payload))


def ask_exit(signame, loop, session):
    """ Stop loop execution """
    print('Got signal {0}: exit'.format(signame))
    loop.stop()
    session.close()


def get_conn():
    """ Provides a psycopg2 db connection"""
    return psycopg2.connect(database=db['dbname'],
                            user=db['user'],
                            password=db['password'],
                            host=db['host'],
                            port=db['port'])


def get_session():
    """ Provides a SQL Alchemy Scoped Session which is thread safe """
    engine = create_engine('postgresql+psycopg2://', creator=get_conn)  # DRY
    session_factory = sessionmaker(bind=engine)
    return scoped_session(session_factory)


def start():

    # Thread pool ###
    pool = ThreadPoolExecutor(10)  # The pool is relative small. It's not intended for bulk updates

    # Setup DB connection ###
    conn = get_conn()
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

    listen(channel=db['channel'], dbconn=conn)
    session = get_session()
    insert_mirror_session = partial(insert_mirror, session=session)

    # Setup loop ###
    loop = asyncio.get_event_loop()
    loop.add_reader(fd=conn.fileno(),
                    callback=partial(receive,
                                     pool=pool,
                                     loop=loop,
                                     dbconn=conn,
                                     mirror=insert_mirror_session))

    for signame in ('SIGINT', 'SIGTERM'):
        loop.add_signal_handler(getattr(signal, signame), partial(ask_exit,
                                                                  signame=signame,
                                                                  loop=loop,
                                                                  session=session))

    print('Event loop running forever, press Ctrl+C to interrupt.')
    print('pid {0}: send SIGINT or SIGTERM to exit.'.format(os.getpid()))

    # Start loop ###
    try:
        loop.run_forever()
    finally:
        loop.close()

if __name__ == '__main__':
    start()
