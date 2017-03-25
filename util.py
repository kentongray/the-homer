from threading import Thread, Timer


def list_right_index(alist, value):
    return len(alist) - alist[-1::-1].index(value) - 1


# forget the ceremony just give me a thread
def thread_it(task):
    print("i am starting a thread", task)
    thread = Thread(target=task)
    thread.start()


def delay(f, delay=0.):
    timer = Timer(delay, f)
    timer.start()
