from redis import Redis
from rq import Queue, SimpleWorker

redis_connection = Redis(
    host="localhost",
    port=6379
)

queue = Queue(
    "default",
    connection=redis_connection
)

worker = SimpleWorker(
    [queue],
    connection=redis_connection
)

worker.work()