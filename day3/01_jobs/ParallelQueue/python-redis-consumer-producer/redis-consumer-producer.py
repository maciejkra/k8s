import pickle
import redis
import os
import time


class RedisDataProvider:
    def __init__(self):
        print("Connecting to redis")
        redis_host =  os.environ.get("REDIS_HOST","redis")
        redis_port =  os.environ.get("REDIS_PORT",6379)
        self.r = redis.Redis(host=redis_host, port=redis_port, db=0)

    def add_to_list(self, key, item):
        self.r.rpush(key, pickle.dumps(item))

    def take_from_list(self, key):
        i = self.r.lpop(key)
        if i is not None:
            return pickle.loads(i)
        return None

rdp = RedisDataProvider()
list_name = os.environ.get("LIST_NAME","consumables")
consume_delay = int(os.environ.get("CONSUME_DELAY","30"))

is_consumer = os.environ.get("IS_CONSUMER","TRUE")
print(f'Is consumer: {is_consumer}')

if is_consumer.upper() == "TRUE":
  print('Consuming')
  elem = rdp.take_from_list(list_name)
  print(f'Consumed {elem}')
  while elem is not None:
    print(f'Consumed {elem}')
    print(f'Waiting {consume_delay}')
    time.sleep(consume_delay)
    elem = rdp.take_from_list(list_name)
else:
  print('Producing')
  for i in range(10):
    elem = {"my_item":i}
    print(f'Populating into {list_name} {elem}')
    rdp.add_to_list(list_name, i)
