import os

import redis


HOST = os.environ['REDIS_HOST']
PORT = os.environ.get('REDIS_PORT') or '6379'
USERNAME = os.environ['REDIS_USER']
PASSWORD = os.environ['REDIS_PASS']

redis_pool = redis.ConnectionPool().from_url(f'redis://{USERNAME}:{PASSWORD}@{HOST}:{PORT}')