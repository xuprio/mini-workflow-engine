import os

import redis


HOST = os.getenv('REDIS_HOST')
PORT = os.getenv('REDIS_PORT') or '10663'
USERNAME = os.getenv('REDIS_USER')
PASSWORD = os.getenv('REDIS_PASS')

redis_pool = redis.ConnectionPool().from_url(f'redis://{USERNAME}:{PASSWORD}@{HOST}:{PORT}')