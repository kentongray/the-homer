from threading import Thread


def list_right_index(alist, value):
    return len(alist) - alist[-1::-1].index(value) - 1


# forget the ceremony just give me a thread
def thread_it(task):
    thread = Thread(target=task)
    thread.start()
