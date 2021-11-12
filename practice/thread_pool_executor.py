#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : thread_pool_executor.py
@Author  : liuzhiming
@Time    : 2021/11/8 16:33
"""

from concurrent.futures import ThreadPoolExecutor
import time
import random
import multiprocessing as m

print("本机CPU核心数：{}个".format(m.cpu_count()))


def get_num(num):
    stop = random.randint(1, 5)
    time.sleep(stop)
    a = random.randint(5, 99)
    print("{} * {} = {}".format(num, a, num*a))
    return a*num


executor = ThreadPoolExecutor(max_workers=10000)
t3 = time.time()
for data in executor.map(get_num, range(10000)):
    pass
t4 = time.time()
print("耗时：{}s".format(t4-t3))


# 参数times用来模拟网络请求的时间
def get_html(times):
    time.sleep(times)
    print("get page {}s finished".format(times))
    return times


executor = ThreadPoolExecutor(max_workers=2)
# 通过submit函数提交执行的函数到线程池中，submit函数立即返回，不阻塞
task1 = executor.submit(get_html, (3))
task2 = executor.submit(get_html, (2))
# done方法用于判定某个任务是否完成
print(task1.done())
# cancel方法用于取消某个任务,该任务没有放入线程池中才能取消成功
print(task2.cancel())
time.sleep(4)
print(task1.done())
# result方法可以获取task的执行结果
print(task1.result())

# 执行结果
# False  # 表明task1未执行完成
# False  # 表明task2取消失败，因为已经放入了线程池中
# get page 2s finished
# get page 3s finished
# True  # 由于在get page 3s finished之后才打印，所以此时task1必然完成了
# 3     # 得到task1的任务返回值

"""
ThreadPoolExecutor构造实例的时候，传入max_workers参数来设置线程池中最多能同时运行的线程数目。
使用submit函数来提交线程需要执行的任务（函数名和参数）到线程池中，并返回该任务的句柄（类似于文件、画图），注意submit()不是阻塞的，而是立即返回。
通过submit函数返回的任务句柄，能够使用done()方法判断该任务是否结束。上面的例子可以看出，由于任务有2s的延时，在task1提交后立刻判断，task1还未完成，而在延时4s之后判断，task1就完成了。
使用cancel()方法可以取消提交的任务，如果任务已经在线程池中运行了，就取消不了。这个例子中，线程池的大小设置为2，任务已经在运行了，所以取消失败。如果改变线程池的大小为1，那么先提交的是task1，task2还在排队等候，这是时候就可以成功取消。
使用result()方法可以获取任务的返回值。查看内部代码，发现这个方法是阻塞的。
"""
