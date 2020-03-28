import os
from locust import HttpLocust, TaskSet, task
import locust.events
import random
import re
from requests.auth import HTTPBasicAuth
import socket
import time


USER = 'test_user'
PASSWORD = 'test_password'

URL = os.environ.get('URL', 'http://localhost/api')
AUTH = HTTPBasicAuth(USER, PASSWORD)
TIME_RANGES = [0, 3600, 7200, 21600, 32400, 43200, 86400]  # /time_range=86400


def get_url() -> str:
    time_range = random.choice(TIME_RANGES)
    return f'/time_range={time_range}'


def get_name(name: str) -> str:
    # 0, 3600, 7200, 21600, 32400, 43200, 86400
    name = re.findall('time_range=(\S+)', name)[0]
    return name


class requestRandomRange(TaskSet):
    @task()
    def get_random_range(self):
        url = get_url()
        self.client.get(url, auth=AUTH)


class MyLocust(HttpLocust):
    task_set = requestRandomRange
    host = URL
    min_wait = 0
    max_wait = 1000  # 5000

    def __init__(self):
        super(MyLocust, self).__init__()
 
        self.sock = socket.socket()
        self.sock.connect(('influxdb', 2003))

        # Hook up the event listeners
        locust.events.request_success += self.hook_request_success
        locust.events.request_failure += self.hook_request_fail
        locust.events.hatch_complete += self.hook_hatch_complete
    
    def hook_request_success(self, request_type, name, response_time, response_length, **kw):
        name = get_name(name)
        # <metric path> <metric value> <metric timestamp>
        string = '%s %d %d\n' % ('range.' + name, response_time, time.time())
        self.sock.send(string.encode('utf-8'))

    def hook_request_fail(self, request_type, name, response_time, exception, *kw):
        name = get_name(name)
        # <metric path> <metric value> <metric timestamp>
        string = '%s %d %d\n' % ('fails.' + name, response_time, time.time())
        self.sock.send(string.encode('utf-8'))

    def hook_hatch_complete(self, user_count, **kw):
        # <metric path> <metric value> <metric timestamp>
        string = '%s %d %d\n' % ('users', user_count, time.time())
        self.sock.send(string.encode('utf-8'))
