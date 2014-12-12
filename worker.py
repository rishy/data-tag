#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import redis
from rq import Worker, Queue, Connection

from config import REDIS_HOST
from config import REDIS_PORT
from config import REDIS_DB
from config import QUEUES_LISTEN


# Get redis url
redis_url = 'redis://' + REDIS_HOST + ':' + str(REDIS_PORT)

# Get redis connection
redis_conn = redis.from_url(redis_url)

# Get redis queue object for each listing
qH = Queue('high', connection=redis_conn)
qN = Queue('normal', connection=redis_conn)
qL = Queue('low', connection=redis_conn)

# Create redis database object
rDB = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)


if __name__ == '__main__':
    # start a worker
    with Connection(redis_conn):
        worker = Worker(map(Queue, QUEUES_LISTEN))
        worker.work()
