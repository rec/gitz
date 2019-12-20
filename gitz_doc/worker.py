from queue import Empty
import threading
import time
import multiprocessing as mp

DEFAULT_COUNT = 4

"""
Distribute tasks amongst workers
Originally from:  https://github.com/rec/bbcprc/blob/master/bbcprc/worker.py
"""


class Worker(mp.Process):
    def __init__(self, queue, counter, reply_queue=None):
        super().__init__()
        self.time = time.time()
        self.queue = queue
        self.counter = counter
        if reply_queue:
            self.reply = reply_queue.put

    def reply(self, item):
        pass

    def run(self):
        for command, arg in iter(self.queue.get, None):
            self.reply(command(arg))
            self._increment_counter()

    def _increment_counter(self):
        with self.counter.get_lock():
            self.counter.value += 1
            return self.counter.value


class Workers:
    def __init__(self, count=DEFAULT_COUNT, reply_queue=None):
        self.queue = mp.Queue()
        self.counter = mp.Value('i')
        self.reply_queue = reply_queue
        args = self.queue, self.counter, self.reply_queue
        self.workers = [Worker(*args) for i in range(count)]

    def __enter__(self):
        for w in self.workers:
            w.start()
        return self

    def __exit__(self, type, value, traceback):
        for w in self.workers:
            self.queue.put(None)

    def run(self, *args):
        self.queue.put(args)


def service_queue(queue, function=print, timeout=0.1):
    def target():
        while True:
            try:
                value = queue.get(timeout=timeout)
            except (mp.TimeoutError, Empty):
                continue
            function(*value)

    thread = threading.Thread(target=target, daemon=True)
    thread.start()
    return thread


def work_on(function, items, count=DEFAULT_COUNT, reply=None, timeout=0.1):
    reply_queue = reply and mp.Queue()
    with Workers(count, reply_queue) as workers:
        for item in items:
            workers.run(function, item)
    if reply:
        service_queue(reply_queue, reply, timeout)


if __name__ == '__main__':
    import random

    def function(x):
        for i in range(3):
            print(x, i)
            time.sleep(random.uniform(0.05, 0.15))
        return x, 'reply'

    work_on(function, 'abcdefghi', 4, print)