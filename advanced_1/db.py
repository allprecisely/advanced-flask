import os
from datetime import timedelta

from flask_sqlalchemy import SQLAlchemy
import redis

ACCESS_EXPIRES = timedelta(hours=1)

db = SQLAlchemy()

jwt_redis_blocklist = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))
