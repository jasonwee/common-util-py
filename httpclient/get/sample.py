# -*- coding: utf-8 -*-
from multiprocessing import Pool, Process, Queue, Pipe, Lock, Value, Array, Manager, TimeoutError
import time
import os
import logging
import multiprocessing

def f(x):
    return x * x;

def f1(name):
    print('hello', name)

def info(title):
    print(title)
    print('module name:', __name__)
    if hasattr(os, 'getppid'): # only available on unix
        print('parent process:', os.getppid())
    print('process id:', os.getpid())

def f2(name):
    info('function f2')
    print('hello', name)

def f3(q):
    q.put([42, None, 'hello'])

def f4(conn):
    conn.send([42, None, 'hello'])
    conn.close()

def f5(l, i):
    l.acquire()
    print('hello world', i)
    l.release()

def f6(n, a):
    n.value = 3.1415927
    for i in range(len(a)):
        a[i] = -a[i]

def f7(d, l):
    d[1] = '1'
    d['2'] = 2
    d[0.25] = None
    l.reverse()


if __name__ == '__main__':
    p = Pool(5)
    print(p.map(f, [1,2,3]))

    p = Process(target=f1, args=('bob',))
    p.start()
    p.join()
    print('')

    info('main line')
    p = Process(target=f2, args=('charlie',))
    p.start()
    p.join()
    print('')

    q = Queue()
    p = Process(target=f3, args=(q,))
    p.start()
    print(q.get())
    p.join()
    print('')

    parent_conn, child_conn = Pipe()
    p = Process(target=f4, args=(child_conn,))
    p.start()
    print(parent_conn.recv())
    p.join()
    print('')

    lock = Lock()
    for num in range(10):
        Process(target=f5, args=(lock, num)).start()

    # next

    num = Value('d', 0.0)
    arr = Array('i', range(10))

    p = Process(target=f6, args=(num, arr))
    p.start()
    p.join()

    print(num.value)
    print(arr[:])
    print('')

    manager = Manager()

    d = manager.dict()
    l = manager.list(range(10))

    p = Process(target=f7, args=(d, l))
    p.start()
    p.join()

    print(d)
    print(l)
    print('')

    pool = Pool(processes=4)
    
    print(pool.map(f, range(10)))

    for i in pool.imap_unordered(f, range(10)):
        print(i)

    # evaluate "f(20)" asynchronously
    res = pool.apply_async(f, (20,))
    print(res.get(timeout=1))

    res = pool.apply_async(os.getpid, ())
    print(res.get(timeout=1))

    multiple_results = [pool.apply_async(os.getpid, ()) for i in range(4)]
    print([res.get(timeout=1) for res in multiple_results])

    res = pool.apply_async(time.sleep, (10,))
    try:
        print(res.get(timeout=1))
    except TimeoutError:
        print("We lacked patience and got a multiprocessing.TimeoutError")

    logger = multiprocessing.log_to_stderr()
    logger.setLevel(logging.INFO)
    logger.warning('doomed')
    m = multiprocessing.Manager()
