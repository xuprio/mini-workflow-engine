def task_a():
    print("Running task A")
    return True

def task_b():
    print("Running task B")
    return True

def task_c():
    print("Running task C")
    return False


TASK_SWITCHER = {
    'task_a': task_a,
    'task_b': task_b,
    'task_c': task_c
}
