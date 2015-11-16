#!/usr/bin/env python
""" Get all notifications from postresql notification channel called 'events' using asyncio and psycopg2.
This is a POC to use asyncio BaseEventLoop.add_reader() on Psycopg2 connection file descriptor to get realtime
notifications from the database """

import os
import asyncio
import signal
import psycopg2
import psycopg2.extensions
from functools import partial

def listen(channel, dbconn):
    """ Listen to a channel """
    curs = dbconn.cursor()
    curs.execute('LISTEN {0};'.format(channel))


def receive(dbconn):
    """ Receive a notify message from the channel we are listening to """
    state = dbconn.poll()
    if state == psycopg2.extensions.POLL_OK:
        if dbconn.notifies:
            while len(dbconn.notifies) != 0:
                notify = dbconn.notifies.pop()
                print(notify.payload)


def ask_exit(signame, loop):
    """ Stop loop execution """
    print('Got signal {0}: exit'.format(signame))
    loop.stop()


def start():

    # Setup DB connection ###
    conn = psycopg2.connect(database='twdb',
                            user='twdb',
                            password='twdb',
                            host='localhost',
                            port='5432')

    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

    listen(channel='events', dbconn=conn)

    # Setup loop ###
    loop = asyncio.get_event_loop()
    loop.add_reader(fd=conn.fileno(), callback=partial(receive, dbconn=conn))

    for signame in ('SIGINT', 'SIGTERM'):
        loop.add_signal_handler(getattr(signal, signame), partial(ask_exit, signame, loop))

    print('Event loop running forever, press Ctrl+C to interrupt.')
    print('pid {0}: send SIGINT or SIGTERM to exit.'.format(os.getpid()))

    # Start loop ###
    try:
        loop.run_forever()
    finally:
        loop.close()

if __name__ == '__main__':
    start()
