#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# Redis configuration
REDIS_HOST = 'localhost'
REDIS_PORT = 6379

# You can also specify the Redis DB to use
REDIS_DB = 0
# REDIS_PASSWORD = 'very secret'

# Queues to listen on
QUEUES_LISTEN = ['high', 'normal', 'low']
