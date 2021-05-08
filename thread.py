"""
Python 线程:
    线程何时切换? 一个线程无论何时开始睡眠或等待网络 I/O,其他线程总有机会获取 GIL 执行 Python 代码.
    这是协同式多任务处理.CPython 也还有抢占式多任务处理.如果一个线程不间断地在 Python 2 中运行 1000
    字节码指令，或者不间断地在 Python 3 运行15 毫秒,那么它便会放弃 GIL，而其他线程可以运行.即多个线
    程但只有一个 CPU 时的时间片.

协同式多任务处理:
    当执行一个比如网络IO请求任务时,该任务需要较长或不确定的时间的IO响应,而在此期间并不执行任何Python
    代码时,该线程会主动释放GIL,从而其它线程有机会获取GIL并执行Python代码.
    此种机制使得并发任务成为可能; 多线程可以同时等待不同的触发信号.

抢占式多任务:
    如果一个线程不间断地在 Python 2 中运行 1000字节码指令，或者不间断地在 Python 3 运行15 毫秒,那么
    它便会放弃 GIL，而其他线程可以运行


线程 vs 进程:
    线程: 更加适合IO密集型任务
    进程: 更加适合CPU密集型任务

"""
import multiprocessing
import random
import socket
import threading
import time


def connect():
    s = socket.socket(family=socket.AF_INET,type=socket.SOCK_STREAM)
    s.connect(('www.baidu.com',80))


# 在同一时间里两个线程中只有一个可以执行Python代码，但是只要该线程开始连接socket，它就会释放GIL锁，所以另一
# 个线程就可以运行了。这意味着两个线程现在可以同时等待socket连接，从而实现在同一段时间里可以做更多的任务
def connect_thread():
    for i in range(2):
        t = threading.Thread(target=connect)
        t.start()


def cup_task(n):  # CPU密集型的程序
    while n > 0:
        n -= 1


def single_thread():
    start_time = time.time()
    cup_task(10000000)
    print('{} s'.format(time.time() - start_time))  # 测量程序执行时间


def mutlti_thread():
    start_time = time.time()
    t1 = multiprocessing.Process(target=cup_task,args=(10000000,))
    t1.start()
    t2 = multiprocessing.Process(target=cup_task,args=(10000000,))
    t2.start()

    t1.join()
    t2.join()
    print('{} s'.format(time.time() - start_time))


"""
线程运行的条件:
    1.线程获取到cpu的时间片
    2.线程获取到全局的GIL锁

线程状态:
    New -> Runable -> Runing -> Dead
             \         /
               Blocked

    线程Runing到Blocked的情况:
        1.同步,线程中获取同步锁,但是资源已经被其他线程锁定,进入Locked状态,直到该资源可获取
        2.睡眠,线程运行sleep() 或 join() 方法之后,线程进入Sleeping状态.sleep()是等待固定
        的时长,join()是等待子程序执行完(join也可以指定一个超时时间). 注意: 如果两个线程a,b,
        在a中调用b.join(),相当于合并(join)成一个线程.最常见的是在主线程中join()所有的子线程
        3.等待,线程中执行wait()方法,线程进入Waiting状态,等待其他线程的通知(notify)


线程合并:
    主线程或者某个函数如果创建了子线程,只要调用了子线程的join方法,那么主线程就会被子线程所阻塞,
    直到子线程执行完毕再轮到主线程执.(join方法的作用是阻塞主线程,使得主线程无法执行join后面的语
    句)

    # 方式一,启动所有的线程之后执行执行join(),子线程执行的无序执行,但是每个线程都会等待主线程
    执行完毕
    for t in tasks:
        t.start()

    for t in tasks:
        t.join()

    # 方式二: 启动线程之后立即执行join(),子线程的按照固定的顺序执行,无法实现线程切换
    for t in tasks:
        t.start()
        t.join()

线程同步与互斥锁:
    threading.Lock() 创建互斥锁
    Lock方法:
        lock.acquire([blocking]) 获取锁,返回bool值.如果有必要,需要阻塞到锁的释放为止
        lock.release() 释放锁

    threading.Rlock()  创建可重入锁,一个资源可以同时假多把锁
    Rlock方法:
        lock.acquire([blocking]) 获取锁,返回bool值.如果有必要,需要阻塞到锁的释放为止
        lock.release() 释放锁


条件变量:
    关注特定的状态变化或事件的发生时将使用此种锁.[生产者-消费者]
    threading.Condition([lock]) lock是可选的Lock/Rlock实例,如果未提供,会创建一个新的Rlock实例
    供条件变量使用.

    Condition方法:
        acquire() 获取底层锁
        release() 释放锁

        wait([timeout]) 等待指定获得通知或出现超时为止.此方法在调用线程已获取到锁之后调用,调用的时候,
        会释放底层的锁,而且线程将进入睡醒状态,直到另一个线程在条件变量上执行notify()或者notify_all()
        方法将其唤醒为止.在被唤醒之后,线程将重新获取锁,方法也会返回

        notify([n]) 唤醒一个或多个等待此变量的线程.此方法在调用线程已获取到锁之后调用,而且如果没有正在
        等待的线程,它什么也不做.被唤醒的线程在它们获取锁之前不会从wait()调用返回.


事件:
    事件用于线程之间通信,一个线程发出事件信号,一个或多个其他线程等待它.Event实例管理着内部的标志,可以使
    用set()方法将它设置为True,使用clear()将其重置为False

    threading.Event() 创建Event实例,并且将其内部标志设置为False

    Event方法:
        is_set() 只有当内部标志为True时才返回True
        set() 设置内部标志为True
        clear() 重置内部标志
        wait([timeout]) 阻塞直到内部标志为True.如果进入时内部标志为True,此方法立即返回.否则一直阻塞,直到
        另外一个线程调用set()方法

信号量:
    基于计数器的同步原语,每次调用acquire()时计数器减1,每次调用release()时计数器加1.如果计数器值是0,
    acquire()方法会被阻塞,直到其他线程调用release()方法为止.

    threading.Semaphore([value]) value是信号量的初始值,默认是1

    Semaphone方法:
        acquire([blocking]) 获取信号量,如果计数器大于0,此方法把它的值减1,然后立即返回.如果它的值是0,此方法
        将被阻塞,直到另外一个线程调用release()方法为止.

        release() 通过内部计数器的值加1来释放一个信号量.如果计数器是0,而且另外一个线程正在等待,该线程会被唤
        醒.如果是多个线程正在等待,只能唤醒其中的一个线程.

    threading.BoundedSemaphore([value]) 工作方式与Semaphore的一致,但release()操作次数不能超过acquire()
        操作次数
"""

"""生产者-消费者"""
con = threading.Condition()
queue = []


def producer():
    while True:
        if con.acquire():
            if len(queue) > 100:
                con.wait()
            else:
                elem = random.randrange(100)
                queue.append(elem)
                print("Producer a elem {},Now size is {}".format(elem,len(queue)))
                time.sleep(random.random())
                con.notify()
            con.release()


def consumer():
    if con.acquire():
        if len(queue) < 0:
            con.wait()
        else:
            elem = queue.pop()
            print("Consumer a elem {}.Now size is {}".format(elem,len(queue)))
            time.sleep(random.random())
            con.notify()
        con.release()


def producer_consumer():
    produce = threading.Thread(target=producer)
    consume = threading.Thread(target=consumer)

    produce.start()
    consume.start()

    produce.join()
    consume.join()
