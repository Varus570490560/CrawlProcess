import threading


def fun(params):
    for param in params:
        print(param)


task = [
    (fun, 1, 2, 3),
    (fun, 4, 5, 6),
    (fun, 1, 2, 3),
    (fun, 4, 5, 6),
    (fun, 1, 2, 3),
    (fun, 4, 5, 6),
    (fun, 1, 2, 3),
    (fun, 4, 5, 6),
    (fun, 1, 2, 3),
    (fun, 4, 5, 6),
]
task_index: int = 0
lock: threading.Lock = threading.Lock()


def proc():
    while True:
        execute = get_task()
        if execute is None:
            break
        else:
            func = execute[0]
            params = execute[1:]
            func(params)


def get_task():
    lock.acquire()
    global task_index
    if task_index == len(task):
        lock.release()
        return None
    else:
        func = task[task_index]
        task_index = task_index + 1
        lock.release()
        return func


class MutiThreadExecute(threading.Thread):
    def __init__(self, thread_id: int):
        threading.Thread.__init__(self)
        self.thread_id = thread_id

    def run(self):
        print("Thread {} start...".format(self.thread_id))
        proc()
        print("Thread {} end!".format(self.thread_id))


def muti_thread_execute(thread_count: int):
    for i in range(0, thread_count):
        MutiThreadExecute(i).start()


if __name__ == '__main__':
    muti_thread_execute(2)
