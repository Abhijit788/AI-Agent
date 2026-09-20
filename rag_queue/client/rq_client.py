from dotenv import load_dotenv
load_dotenv()
from redis import Redis
from rq import Queue

queue = Queue(connection=Redis(
  host='localhost', 
  port="6379"
  ))
