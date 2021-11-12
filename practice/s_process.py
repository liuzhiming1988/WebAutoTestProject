#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : s_process.py
@Author  : liuzhiming
@Time    : 2021/11/9 14:34
"""

from multiprocessing import Process


def study_info(*args, **kwargs):
    print(args, kwargs)


def main():
    # 信息列表
    list_info = [{"name": "python 基础", "progress": "10%"},
                 {"name": "python 面向对象", "progress": "20%"},
                 {"name": "python 爬虫", "progress": "30%"},
                 {"name": "python pyqt5", "progress": "40%"},
                 {"name": "python 数据结构", "progress": "50%"}]

    # 创建进程
    for i in range(5):
        p = Process(target=study_info, args=(i,), kwargs=list_info[i])
        # 启动进程
        p.start()


"""进程Process和线程threading区别
1）地址空间和其它资源（如打开文件）：进程间相互独立，同一进程的各线程间共享。某进程内的线程在其它进程不可见。
2）通信：进程间通信IPC，线程间可以直接读写进程数据段（如全局变量）来进行通信——需要进程同步和互斥手段的辅助，以保证数据的一致性。
3）调度和切换：线程上下文切换比进程上下文切换要快得多。
4）在多线程OS中，进程不是一个可执行的实体。1.一个线程只能属于一个进程，而一个进程可以有多个线程，但至少有一个线程（线程是计算机的最小单位）；
2.资源分配给进程，同一进程的所有线程共享该进程的所有资源，进程与进程之间资源相互独立，互不影响（类似深拷贝）;

3.多进程模式最大的优点就是稳定性高，因为一个子进程崩溃了，不会影响主进程和其他子进程，多进程模式的缺点是在Windows下创建进程开销巨大。另外，操作系统能同时运行的进程数也是有限的，在内存和CPU的限制下，如果有几千个进程同时运行，操作系统连调度都会成问题（进程的创建比线程的创建更加占用计算机资源）；

4.多线程模式致命的缺点就是任何一个线程挂掉都可能直接造成整个进程崩溃，因为所有线程共享进程的内存；

5.由于GIL锁的缘故，python 中线程实际上是并发运行（即便有多个cpu，线程会在其中一个cpu来回切换，只占用一个cpu资源），而进程才是真正的并行（同时执行多个任务，占用多个cpu资源），下面关于并行和并发做一个简单的了解；
"""

if __name__ == "__main__":
    main()
