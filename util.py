def list_right_index(alist, value):
    return len(alist) - alist[-1::-1].index(value) - 1